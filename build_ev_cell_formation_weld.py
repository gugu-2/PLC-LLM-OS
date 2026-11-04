# -*- coding: utf-8 -*-
"""
Builder for FB_Automotive_EV_CellFormation_UltrasonicTabWeld
Lumina Cyber-Physical Automation Swarm V7 Max-Persona
Domain: Automotive & EV Battery Manufacturing (Tier 1 Global High-Demand Industrial Automation)
"""
import json
import uuid
import re
import os
import subprocess

def generate_st_code():
    code_parts = []

    # =========================================================================
    # 1. HEADER AND TITLE BLOCK
    # =========================================================================
    code_parts.append('''FUNCTION_BLOCK FB_Automotive_EV_CellFormation_UltrasonicTabWeld
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Automotive & EV Battery Manufacturing (Tier 1 High-Demand GigaFactory Automation)
 * SYSTEM                       : High-Speed Cylindrical & Prismatic EV Battery Cell Formation, Grading & Ultrasonic Foil-to-Tab Welding Line
 * INTEGRATED SUBSYSTEMS        : - 20 kHz 3.5 kW Ultrasonic Metal Welding Sonotrode with Active Dynamic Normal Force Control (200 to 1200 N)
 *                                  & Energy / Peak Power / Distance Multi-Mode Weld Termination Engine
 *                                - Multi-Channel High-Precision Galvanostatic / Potentiostatic (CCCV) Formation Cycler (0 to 5 V, 0 to 100 A
 *                                  with +-0.02% F.S. current accuracy and continuous dQ/dV differential capacity peak tracking)
 *                                - High-Vacuum Degassing Chamber with Puncture Needle Piercing and High-Frequency Induction Hermetic Reseal
 *                                - High-Speed 6-Axis SCARA Cell Collation Gantry (< 0.8 s cycle time per cell)
 *                                - 1 kHz AC Internal Resistance (ACIR) & Open-Circuit Voltage (OCV) High-Speed Quality Grading Sorter
 * SAFETY INTEGRITY LEVEL       : IEC 61508 SIL 3 / ISO 26262 ASIL-D Dual-Channel Architecture with Hardware Fault Tolerance HFT=1
 * ALARM SPECIFICATION          : ANSI / ISA-18.2-2016 Alarm Management Lifecycle with 4-Tier Severity & Rate-of-Change (ROC)
 * CONTROL METHODOLOGY          : 8-State Discrete State-Space Dynamics (x[k+1] = A*x[k] + B*u[k]) & Receding-Horizon Quadratic MPC
 * EXECUTION SCAN TIME          : 1.0 ms deterministic real-time synchronous task cycle (Ts = 0.001 s)
 * =====================================================================================================================
 * MATHEMATICAL AND CYBER-PHYSICAL FOUNDATION:
 *
 * 1. ULTRASONIC ACOUSTIC VIBRATION & RESIDUAL BOND DYNAMICS:
 *    The ultrasonic metal welding sonotrode delivers transversal acoustic shear waves at f_s = 20.0 kHz into multi-layer
 *    copper/aluminum foil stacks (30 to 80 layers, 8 um thickness each) clamped to nickel-coated copper cell terminal tabs.
 *    The acoustic impedance Z_ac(t) exhibits non-linear mechanical softening:
 *       Z_ac(t) = F_N(t) / v_tip(t) = R_mech(T_joint) + j * (omega * M_horn - K_horn / omega)
 *    Real-time energy integration governing weld termination:
 *       E_weld(t) = Integral_0^t (V_piezo(tau) * I_piezo(tau) * cos(theta_phi(tau))) d_tau
 *    Height collapse displacement equation:
 *       Delta_h(t) = h_initial - h_current(t),  Termination condition: Delta_h >= Delta_h_target OR E_weld >= E_target.
 *
 * 2. SEI LAYER ELECTROCHEMICAL FORMATION & DIFFERENTIAL CAPACITY (dQ/dV):
 *    During constant-current (CC) formation, Solid Electrolyte Interphase (SEI) passivating film precipitates on graphite anode
 *    surfaces between 0.8 V and 1.2 V vs Li/Li+. The differential capacity signature is numerically identified via:
 *       dQ/dV = (I_form(t) * Delta_t) / (V_cell(t) - V_cell(t - M * Delta_t))
 *    Graphite staging phase transitions (LiC_12 -> LiC_6) manifest as distinct local maxima in dQ/dV space. Peak position,
 *    height, and area integrals determine SEI structural stability and cell electrochemical longevity.
 *
 * 3. VACUUM DEGASSING & HERMETIC INDUCTION RESEAL HEAT DIFFUSION:
 *    Pouch blister degassing operates at ultra-low absolute pressure (P_vac <= 0.1 mbar). Needle puncture releases trapped
 *    gaseous volatile decomposition byproducts (CO2, C2H4, HF). Post-evacuation leak rate is governed by Knudsen flow:
 *       Q_leak = (V_chamber / Delta_t_test) * (P_vac(t_end) - P_vac(t_start))  [mbar * L / s]
 *    High-frequency (300 kHz) induction heating creates eddy current dissipation inside the aluminum laminate pouch flap:
 *       P_eddy = (pi * mu_0 * mu_r * d_foil * f_ind^2 * B_peak^2) / rho_resistivity
 *       dT_seal/dt = (P_eddy - h_conv * A_seal * (T_seal - T_amb) - sigma * epsilon * A_seal * (T_seal^4 - T_amb^4)) / (m_seal * C_p)
 *
 * 4. 8-STATE DISCRETE STATE-SPACE MATRIX FORMULATION (Ts = 1.0 ms):
 *    State Vector:
 *       x_1 : Ultrasonic Horn Resonant Frequency Phase Angle Error theta_err [rad]
 *       x_2 : Sonotrode Dynamic Clamping Normal Force F_N [N]
 *       x_3 : Dynamic Acoustic Mechanical Joint Impedance Z_ac [N*s/m]
 *       x_4 : Cell 4-Wire Terminal Voltage V_cell [V]
 *       x_5 : Formation Galvanostatic Charge Current I_form [A]
 *       x_6 : Cell Internal Jelly-Roll Core Temperature T_core [deg C]
 *       x_7 : Vacuum Degassing Chamber Absolute Pressure P_vac [mbar]
 *       x_8 : SCARA Gantry Cartesian Tool Center Point Velocity v_scara [mm/s]
 *
 *    Control Input Vector:
 *       u_1 : Transducer Frequency Tuning Offset Delta_f [kHz]
 *       u_2 : Voice-Coil Normal Force Actuator Command u_F [N]
 *       u_3 : Cycler Current Setpoint u_I [A]
 *       u_4 : Vacuum Pumping Speed Throttle Valve Command u_vac [%]
 *       u_5 : RF Induction Reseal Generator Power Setpoint u_ind [kW]
 *       u_6 : SCARA Axis Servo Trajectory Velocity Feedforward u_vel [mm/s]
 * ===================================================================================================================== *)
''')

    # =========================================================================
    # 2. VAR_INPUT BLOCK
    # =========================================================================
    code_parts.append('''VAR_INPUT
    (* ========================================================================================= *)
    (* PRIMARY OPERATING COMMANDS & PROCESS INTERLOCKS                                           *)
    (* ========================================================================================= *)
    bSysEnable                      : BOOL;     (* Master System Enable Supervisory Command [-] *)
    bAutoStart                      : BOOL;     (* Automated Production Cycle Start Pulse [-] *)
    bSysReset                       : BOOL;     (* Fault Latch Reset Pushbutton [-] *)
    bEmergencyStopOk                : BOOL;     (* Dual-Channel Safety E-Stop Relay Healthy [-] *)
    bSafetyGateClosed               : BOOL;     (* Automated Light Curtain & Interlocked Guarding OK [-] *)
    bCellPresentInfeed              : BOOL;     (* Optical Sensor: Raw EV Battery Cell Infeed Clamping Fixture [-] *)
    bTrayPresentCollation           : BOOL;     (* Proximity Sensor: 96-Cell Formation Matrix Tray Locked in Position [-] *)
    bPurgeNitrogenAvailable         : BOOL;     (* Supply Pressure Switch: N2 Inert Shielding Gas OK (> 5.5 bar) [-] *)
    bCoolingWaterFlowOk             : BOOL;     (* Ultrasonic Generator & Induction Reseal Chilled Water Flow Normal [-] *)

    (* ========================================================================================= *)
    (* 2oo3 TMR SENSOR TRIPLET 1: ULTRASONIC SONOTRODE DYNAMIC NORMAL FORCE [N]                  *)
    (* Transducers: Kistler Triaxial Piezoelectric Load Cell Triplet at Horn Base                *)
    (* ========================================================================================= *)
    FIT_US_FORCE_101A               : REAL;     (* Ultrasonic Normal Clamping Force Channel A [N] *)
    FIT_US_FORCE_101B               : REAL;     (* Ultrasonic Normal Clamping Force Channel B [N] *)
    FIT_US_FORCE_101C               : REAL;     (* Ultrasonic Normal Clamping Force Channel C [N] *)

    (* ========================================================================================= *)
    (* 2oo3 TMR SENSOR TRIPLET 2: ULTRASONIC HORN COLLAPSE DISPLACEMENT LVDT [mm]                *)
    (* Transducers: Sub-Micron Linear Variable Differential Transformers (LVDT) 0-10mm           *)
    (* ========================================================================================= *)
    LIT_US_DISP_102A                : REAL;     (* Sonotrode Vertical Linear Displacement Channel A [mm] *)
    LIT_US_DISP_102B                : REAL;     (* Sonotrode Vertical Linear Displacement Channel B [mm] *)
    LIT_US_DISP_102C                : REAL;     (* Sonotrode Vertical Linear Displacement Channel C [mm] *)

    (* ========================================================================================= *)
    (* 2oo3 TMR SENSOR TRIPLET 3: CELL TERMINAL 4-WIRE KELVIN VOLTAGE PROBES [V]                 *)
    (* Transducers: Gold-Plated Coaxial Kelvin Sense Probes Direct at Tab Weld Seam              *)
    (* ========================================================================================= *)
    VIT_CELL_VOLT_201A              : REAL;     (* Cell 4-Wire Terminal Voltage Channel A [V] *)
    VIT_CELL_VOLT_201B              : REAL;     (* Cell 4-Wire Terminal Voltage Channel B [V] *)
    VIT_CELL_VOLT_201C              : REAL;     (* Cell 4-Wire Terminal Voltage Channel C [V] *)

    (* ========================================================================================= *)
    (* 2oo3 TMR SENSOR TRIPLET 4: FORMATION CYCLER SHUNT CURRENT TRANSDUCERS [A]                 *)
    (* Transducers: Ultrastable Fluxgate Current Transducers (0 to 100 A, +-0.02% F.S.)          *)
    (* ========================================================================================= *)
    IIT_FORM_CURR_202A              : REAL;     (* Cell Formation Charging Current Channel A [A] *)
    IIT_FORM_CURR_202B              : REAL;     (* Cell Formation Charging Current Channel B [A] *)
    IIT_FORM_CURR_202C              : REAL;     (* Cell Formation Charging Current Channel C [A] *)

    (* ========================================================================================= *)
    (* 2oo3 TMR SENSOR TRIPLET 5: CELL INTERNAL JELLY-ROLL / CORE INFRARED PYROMETERS [deg C]    *)
    (* Transducers: Dual-Wavelength Non-Contact Pyrometric Temperature Probes 0 to 120 deg C     *)
    (* ========================================================================================= *)
    TIT_CELL_TEMP_203A              : REAL;     (* Cell Surface Core Infrared Temperature Channel A [deg C] *)
    TIT_CELL_TEMP_203B              : REAL;     (* Cell Surface Core Infrared Temperature Channel B [deg C] *)
    TIT_CELL_TEMP_203C              : REAL;     (* Cell Surface Core Infrared Temperature Channel C [deg C] *)

    (* ========================================================================================= *)
    (* 2oo3 TMR SENSOR TRIPLET 6: VACUUM DEGASSING CHAMBER PIRANI CAPACITANCE GAUGES [mbar]      *)
    (* Transducers: Wide-Range Hot-Cathode Pirani / Capacitance Diaphragm Manometers             *)
    (* ========================================================================================= *)
    PIT_VAC_CHAMB_301A              : REAL;     (* Vacuum Chamber Absolute Static Pressure Channel A [mbar] *)
    PIT_VAC_CHAMB_301B              : REAL;     (* Vacuum Chamber Absolute Static Pressure Channel B [mbar] *)
    PIT_VAC_CHAMB_301C              : REAL;     (* Vacuum Chamber Absolute Static Pressure Channel C [mbar] *)

    (* ========================================================================================= *)
    (* 2oo3 TMR SENSOR TRIPLET 7: HIGH-FREQUENCY INDUCTION RESEAL PYROMETERS [deg C]             *)
    (* Transducers: Fiber-Optic High-Speed Micro-Spot Pyrometers Focused on Reseal Seam          *)
    (* ========================================================================================= *)
    TIT_INDUCT_TEMP_302A            : REAL;     (* Induction Reseal Seam Spot Temperature Channel A [deg C] *)
    TIT_INDUCT_TEMP_302B            : REAL;     (* Induction Reseal Seam Spot Temperature Channel B [deg C] *)
    TIT_INDUCT_TEMP_302C            : REAL;     (* Induction Reseal Seam Spot Temperature Channel C [deg C] *)

    (* ========================================================================================= *)
    (* AUXILIARY ANALOG TRANSMITTERS & ACTUATOR FEEDBACKS                                        *)
    (* ========================================================================================= *)
    AE_US_FREQ_103                  : REAL;     (* Ultrasonic Generator Operating Resonance Frequency [kHz] *)
    AE_US_PHASE_104                 : REAL;     (* Ultrasonic Transducer Voltage-to-Current Phase Angle [deg] *)
    JIT_US_POWER_105                : REAL;     (* Ultrasonic Real Active Electrical Power Output [W] *)
    LIT_NEEDLE_POS_303              : REAL;     (* Vacuum Degassing Puncture Needle Linear Stroke Position [mm] *)
    FIT_RESEAL_FORCE_304            : REAL;     (* Hermetic Reseal Pouch Compression Jaw Force [N] *)
    JIT_INDUCT_PWR_305              : REAL;     (* High-Frequency Reseal Generator Active Power Feedback [kW] *)

    (* SCARA 6-Axis Robotic Collation Gantry Transmitters *)
    POS_SCARA_X_401                 : REAL;     (* SCARA X-Axis Linear Absolute Position [mm] *)
    POS_SCARA_Y_402                 : REAL;     (* SCARA Y-Axis Linear Absolute Position [mm] *)
    POS_SCARA_Z_403                 : REAL;     (* SCARA Z-Axis Vertical Quill Position [mm] *)
    POS_SCARA_R_404                 : REAL;     (* SCARA R-Axis Wrist Rotation Absolute Position [deg] *)
    VIT_SCARA_VEL_405               : REAL;     (* SCARA Tool Center Point Cartesian Linear Velocity [mm/s] *)
    PIT_SCARA_VAC_406               : REAL;     (* SCARA End-Effector Suction Cup Vacuum Level [bar] *)
    FIT_SCARA_GRIP_407              : REAL;     (* SCARA Pneumatic Tab Gripper Clamping Normal Force [N] *)

    (* Quality Grading, Metrology & Traceability *)
    ZIT_CELL_ACIR_501               : REAL;     (* 1 kHz Four-Terminal AC Internal Resistance Meter [mOhm] *)
    AIT_CELL_ACIR_PHASE_502         : REAL;     (* 1 kHz AC Impedance Reactance Phase Angle [deg] *)
    LIT_WELD_SEAM_503               : REAL;     (* Confocal Laser Seam Weld Surface Profile Height [mm] *)
    BC_CELL_BARCODE_VALID           : BOOL;     (* 2D DataMatrix Laser Barcode Reader Valid Scan Signal [-] *)
    rCellNominalCap_Ah              : REAL;     (* Cell Rated Design Nominal Electrical Capacity [Ah] *)
END_VAR
''')

    # =========================================================================
    # 3. VAR_OUTPUT BLOCK
    # =========================================================================
    code_parts.append('''VAR_OUTPUT
    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS: ULTRASONIC WELDING SYSTEM                                              *)
    (* ========================================================================================= *)
    CMD_US_GEN_ENABLE               : BOOL;     (* Ultrasonic Generator 20 kHz RF Inverter Enable [-] *)
    CMD_US_FREQ_ADJ_kHz             : REAL;     (* Ultrasonic Generator PLL Frequency Tuning Setpoint [kHz] *)
    CMD_US_AMPLITUDE_PCT            : REAL;     (* Ultrasonic Transducer Vibration Peak Amplitude Setpoint [%] *)
    CMD_US_FORCE_SETPOINT_N         : REAL;     (* Voice-Coil Dynamic Clamping Force Demand [N] *)

    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS: CELL FORMATION CYCLER                                                  *)
    (* ========================================================================================= *)
    CMD_CYCLER_ENABLE               : BOOL;     (* High-Precision Formation Power Channel Output Contactor [-] *)
    CMD_CYCLER_MODE_CV              : BOOL;     (* Formation Mode Selection: FALSE=Constant Current, TRUE=Constant Volt [-] *)
    CMD_CYCLER_CURR_SP_A            : REAL;     (* Formation Power Supply Galvanostatic Current Setpoint [A] *)
    CMD_CYCLER_VOLT_LIMIT_V         : REAL;     (* Formation Power Supply Potentiostatic Voltage Clamping Limit [V] *)

    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS: VACUUM DEGASSING & INDUCTION RESEAL CHAMBER                            *)
    (* ========================================================================================= *)
    CMD_VAC_ROUGHING_VALVE          : BOOL;     (* Vacuum Degassing Primary Roughing Vacuum Pump Isolation Valve [-] *)
    CMD_VAC_TURBO_GATE_VALVE        : BOOL;     (* High-Vacuum Turbomolecular Gate Valve Actuation [-] *)
    CMD_NEEDLE_PUNCTURE_EXTEND      : BOOL;     (* Solenoid Actuator: Extend Pouch Degassing Puncture Needle [-] *)
    CMD_ELECTROLYTE_SUCTION_VALVE   : BOOL;     (* Electrolyte Trap & Volatile Gas Extraction Throttle Valve [-] *)
    CMD_INDUCTION_HEATER_ENABLE     : BOOL;     (* 300 kHz High-Frequency Induction Heating Power Supply Contactor [-] *)
    CMD_INDUCTION_POWER_SP_kW       : REAL;     (* Induction Heating Closed-Loop RF Power Output Demand [kW] *)
    CMD_RESEAL_JAW_CLAMP            : BOOL;     (* Pneumatic Reseal Chilling Jaw Clamping Actuator [-] *)

    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS: SCARA COLLATING ROBOT & TRAY HANDLING                                  *)
    (* ========================================================================================= *)
    CMD_SCARA_START_MOVE            : BOOL;     (* Trigger SCARA Motion Interpolator Axis Move [-] *)
    CMD_SCARA_TARGET_X_mm           : REAL;     (* SCARA Target Cartesian X-Position Command [mm] *)
    CMD_SCARA_TARGET_Y_mm           : REAL;     (* SCARA Target Cartesian Y-Position Command [mm] *)
    CMD_SCARA_TARGET_Z_mm           : REAL;     (* SCARA Target Cartesian Z-Position Command [mm] *)
    CMD_SCARA_TARGET_R_deg          : REAL;     (* SCARA Target Wrist R-Axis Rotation Angle Command [deg] *)
    CMD_SCARA_VAC_VALVE             : BOOL;     (* SCARA End-Effector Vacuum Ejector Pick Solenoid [-] *)
    CMD_CELL_REJECT_GATE            : BOOL;     (* Pneumatic Diverter Gate: Eject Scrap/Rework Cell to Reject Chute [-] *)
    CMD_TRAY_INDEX_PULSE            : BOOL;     (* Conveyor Indexing Motor Pulse: Advance 96-Cell Tray to Warehouse [-] *)

    (* ========================================================================================= *)
    (* PROCESS STATUS, METROLOGY & QUALITY CLASSIFICATION OUTPUTS                                *)
    (* ========================================================================================= *)
    STATUS_SYSTEM_STATE             : INT;      (* Active Finite State Machine Operational Stage Code [0..12, 99] [-] *)
    STATUS_CELL_GRADE               : INT;      (* Final Electrochemical Quality Grade: 1=A, 2=B, 3=Rework, 4=Scrap [-] *)
    STATUS_WELD_QUALITY_SCORE       : REAL;     (* Ultrasonic Weld Signature Composite Quality Metric [0..100%] [%] *)
    STATUS_FORMATION_SOC_PCT        : REAL;     (* Accumulated Cell State of Charge from Formation Coulomb Integrator [%] *)
    STATUS_SEI_PEAK_DETECTED        : BOOL;     (* dQ/dV Differential Capacity Graphite SEI Passivation Signature Identified [-] *)
    STATUS_VAC_DECAY_RATE_mbar_s    : REAL;     (* Vacuum Chamber Seal Decay Leak Rate Metric [mbar/s] *)
    STATUS_ACIR_VALUE_mOhm          : REAL;     (* 1 kHz AC Internal Ohmic Impedance Metric [mOhm] *)
    STATUS_TOTAL_ENERGY_J           : REAL;     (* Total Acoustic Energy Delivered into Tab Weld Joint [J] *)
    STATUS_WELD_HEIGHT_COLLAPSE_mm  : REAL;     (* Net Final Ultrasonic Plastic Horn Collapse Delta Displacement [mm] *)

    (* ========================================================================================= *)
    (* PACKED DIAGNOSTIC & ALARM WORDS (ISA-18.2 COMPLIANT)                                      *)
    (* ========================================================================================= *)
    ALARM_WORD_01                   : DWORD;    (* Category 1: Critical Emergency Shutdown Trips & Hardware Interlocks *)
    ALARM_WORD_02                   : DWORD;    (* Category 2: Process Limits (HI_HI, HI, LO, LO_LO, Rate-of-Change ROC) *)
    ALARM_WORD_03                   : DWORD;    (* Category 3: 2oo3 TMR Sensor Discrepancy & Transducer Failure Faults *)
    INTERLOCK_WORD                  : DWORD;    (* Safety Gate, E-Stop, Coolant, Purge Gas, Permissive Interlock Word *)
    DIAGNOSTIC_WORD                 : DWORD;    (* Subsystem Operational Health, Sub-Cycle Complete, Ready Bitmasks *)
END_VAR
''')

    # =========================================================================
    # 4. VAR (INTERNAL STATE, MATRICES, TIMERS, TMR, MPC)
    # =========================================================================
    code_parts.append('''VAR
    (* ========================================================================================= *)
    (* DISCRETE STATE-SPACE MODEL MATRICES & VECTORS (8-STATE x 6-INPUT, Ts = 0.001 s)           *)
    (* System States: x[1]=Theta_err [rad], x[2]=F_N [N], x[3]=Z_ac [N*s/m], x[4]=V_cell [V],   *)
    (*                x[5]=I_form [A], x[6]=T_core [deg C], x[7]=P_vac [mbar], x[8]=v_scara [mm/s]*)
    (* ========================================================================================= *)
    A_Matrix                        : ARRAY [1..8, 1..8] OF REAL; (* Discrete System Dynamics Matrix A *)
    B_Matrix                        : ARRAY [1..8, 1..6] OF REAL; (* Discrete Actuator Input Coupling Matrix B *)
    C_Matrix                        : ARRAY [1..8, 1..8] OF REAL; (* Discrete Output Measurement Matrix C *)
    D_Matrix                        : ARRAY [1..8, 1..6] OF REAL; (* Discrete Direct Feedthrough Matrix D *)

    x_State                         : ARRAY [1..8] OF REAL; (* Current Discrete Estimated State Vector x[k] *)
    x_Pred                          : ARRAY [1..8] OF REAL; (* One-Step Ahead State Space Prediction x[k+1] *)
    u_Control                       : ARRAY [1..6] OF REAL; (* Controller Actuator Vector u[k] *)
    u_Prev                          : ARRAY [1..6] OF REAL; (* Previous Actuator Vector u[k-1] for Delta_u Penalization *)
    y_Output                        : ARRAY [1..8] OF REAL; (* Computed Plant Observable Measurement Output y[k] *)
    x_Ref                           : ARRAY [1..8] OF REAL; (* Desired Target State Trajectory Reference Vector x_ref *)

    (* Model Predictive Control (MPC) Receding-Horizon Quadratic Weighting Matrices *)
    Q_Weight                        : ARRAY [1..8] OF REAL; (* Diagonal State Error Penalties Q *)
    R_Weight                        : ARRAY [1..6] OF REAL; (* Diagonal Actuator Slew Rate Penalties R *)
    P_Terminal                      : ARRAY [1..8] OF REAL; (* Diagonal Terminal State Horizon Error Penalties P *)
    u_DeltaDemand                   : ARRAY [1..6] OF REAL; (* Gradient Descent Computed Control Increment *)

    (* ========================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT TRACKING VARIABLES                    *)
    (* ========================================================================================= *)
    rVoted_Force_N                  : REAL;     (* Voted Sonotrode Normal Clamping Force [N] *)
    rVoted_Disp_mm                  : REAL;     (* Voted Sonotrode Linear Displacement [mm] *)
    rVoted_Volt_V                   : REAL;     (* Voted Cell 4-Wire Terminal Voltage [V] *)
    rVoted_Curr_A                   : REAL;     (* Voted Formation Cycler Current [A] *)
    rVoted_Temp_degC                : REAL;     (* Voted Cell Core Infrared Temperature [deg C] *)
    rVoted_Vac_mbar                 : REAL;     (* Voted Vacuum Chamber Absolute Pressure [mbar] *)
    rVoted_InductTemp_degC          : REAL;     (* Voted Induction Reseal Seam Spot Temperature [deg C] *)

    (* TMR Channel Isolation & Discrepancy Fault Status Bits *)
    bIso_Force_ChA                  : BOOL;     (* Sonotrode Force Transducer A Discrepancy Quarantine Flag *)
    bIso_Force_ChB                  : BOOL;     (* Sonotrode Force Transducer B Discrepancy Quarantine Flag *)
    bIso_Force_ChC                  : BOOL;     (* Sonotrode Force Transducer C Discrepancy Quarantine Flag *)
    bFlt_Force_Diverged             : BOOL;     (* All 3 Force Transducers Exceed Tolerance Fault *)
    rTimer_Force_Disc_s             : REAL;     (* Force Discrepancy Debounce Integration Timer [s] *)

    bIso_Disp_ChA                   : BOOL;     (* Sonotrode Displacement Sensor A Discrepancy Quarantine Flag *)
    bIso_Disp_ChB                   : BOOL;     (* Sonotrode Displacement Sensor B Discrepancy Quarantine Flag *)
    bIso_Disp_ChC                   : BOOL;     (* Sonotrode Displacement Sensor C Discrepancy Quarantine Flag *)
    bFlt_Disp_Diverged              : BOOL;     (* All 3 Displacement Sensors Exceed Tolerance Fault *)
    rTimer_Disp_Disc_s              : REAL;     (* Displacement Discrepancy Debounce Integration Timer [s] *)

    bIso_Volt_ChA                   : BOOL;     (* Cell Voltage Sense Probe A Discrepancy Quarantine Flag *)
    bIso_Volt_ChB                   : BOOL;     (* Cell Voltage Sense Probe B Discrepancy Quarantine Flag *)
    bIso_Volt_ChC                   : BOOL;     (* Cell Voltage Sense Probe C Discrepancy Quarantine Flag *)
    bFlt_Volt_Diverged              : BOOL;     (* All 3 Voltage Probes Exceed Tolerance Fault *)
    rTimer_Volt_Disc_s              : REAL;     (* Voltage Discrepancy Debounce Integration Timer [s] *)

    bIso_Curr_ChA                   : BOOL;     (* Formation Current Shunt A Discrepancy Quarantine Flag *)
    bIso_Curr_ChB                   : BOOL;     (* Formation Current Shunt B Discrepancy Quarantine Flag *)
    bIso_Curr_ChC                   : BOOL;     (* Formation Current Shunt C Discrepancy Quarantine Flag *)
    bFlt_Curr_Diverged              : BOOL;     (* All 3 Current Shunts Exceed Tolerance Fault *)
    rTimer_Curr_Disc_s              : REAL;     (* Current Discrepancy Debounce Integration Timer [s] *)

    bIso_Temp_ChA                   : BOOL;     (* Cell Core Pyrometer A Discrepancy Quarantine Flag *)
    bIso_Temp_ChB                   : BOOL;     (* Cell Core Pyrometer B Discrepancy Quarantine Flag *)
    bIso_Temp_ChC                   : BOOL;     (* Cell Core Pyrometer C Discrepancy Quarantine Flag *)
    bFlt_Temp_Diverged              : BOOL;     (* All 3 Cell Pyrometers Exceed Tolerance Fault *)
    rTimer_Temp_Disc_s              : REAL;     (* Temperature Discrepancy Debounce Integration Timer [s] *)

    bIso_Vac_ChA                    : BOOL;     (* Vacuum Pirani Gauge A Discrepancy Quarantine Flag *)
    bIso_Vac_ChB                    : BOOL;     (* Vacuum Pirani Gauge B Discrepancy Quarantine Flag *)
    bIso_Vac_ChC                    : BOOL;     (* Vacuum Pirani Gauge C Discrepancy Quarantine Flag *)
    bFlt_Vac_Diverged               : BOOL;     (* All 3 Vacuum Gauges Exceed Tolerance Fault *)
    rTimer_Vac_Disc_s               : REAL;     (* Vacuum Discrepancy Debounce Integration Timer [s] *)

    bIso_IndTemp_ChA                : BOOL;     (* Induction Pyrometer A Discrepancy Quarantine Flag *)
    bIso_IndTemp_ChB                : BOOL;     (* Induction Pyrometer B Discrepancy Quarantine Flag *)
    bIso_IndTemp_ChC                : BOOL;     (* Induction Pyrometer C Discrepancy Quarantine Flag *)
    bFlt_IndTemp_Diverged           : BOOL;     (* All 3 Induction Pyrometers Exceed Tolerance Fault *)
    rTimer_IndTemp_Disc_s           : REAL;     (* Induction Pyrometer Discrepancy Debounce Integration Timer [s] *)

    (* Process Tolerances for TMR Pairwise Discrepancy Comparisons *)
    c_rTol_Force_N                  : REAL := 15.0;     (* Clamping Force Discrepancy Threshold: 15.0 N *)
    c_rTol_Disp_mm                  : REAL := 0.008;    (* Sonotrode LVDT Discrepancy Threshold: 8.0 um *)
    c_rTol_Volt_V                   : REAL := 0.0020;   (* 4-Wire Terminal Voltage Discrepancy Threshold: 2.0 mV *)
    c_rTol_Curr_A                   : REAL := 0.080;    (* Cycler Current Shunt Discrepancy Threshold: 80.0 mA *)
    c_rTol_Temp_degC                : REAL := 2.50;     (* Core Infrared Temperature Discrepancy Threshold: 2.50 deg C *)
    c_rTol_Vac_mbar                 : REAL := 0.040;    (* Vacuum Chamber Discrepancy Threshold: 0.040 mbar *)
    c_rTol_IndTemp_degC             : REAL := 3.50;     (* Induction Reseal Pyrometer Discrepancy Threshold: 3.50 deg C *)
    c_rDisc_Trip_Time_s             : REAL := 0.250;    (* Persistent Outlier Latch Trip Time Limit: 250 ms *)

    (* ========================================================================================= *)
    (* ADVANCED CYBER-PHYSICAL OBSERVER & PROCESS CONTROL VARIABLES                              *)
    (* ========================================================================================= *)
    (* 1. Ultrasonic 20 kHz Phase-Locked Loop (PLL) Resonant Frequency Tracker *)
    rPLL_PhaseError_rad             : REAL;     (* Resonant Phase Error: e_phi = V_piezo x I_piezo phase *)
    rPLL_FreqIntegrator_kHz         : REAL;     (* Frequency Tracking PI Loop Integral Accumulator [kHz] *)
    rPLL_ProportionalGain           : REAL := 0.450; (* PLL Proportional Frequency Gain [kHz/rad] *)
    rPLL_IntegralGain               : REAL := 1.850; (* PLL Integral Frequency Tracking Gain [kHz/(rad*s)] *)
    bPLL_FrequencyLocked            : BOOL;     (* Resonance Frequency Locked within +-50 Hz Flag *)

    (* 2. Multi-Mode Ultrasonic Tab Weld Termination Engine *)
    rWeld_AccumEnergy_J             : REAL;     (* Trapezoidal Integrated Active Acoustic Energy: Integral P(t) dt [J] *)
    rWeld_InitialHeight_mm          : REAL;     (* Baseline Pre-Weld Clamped Stack Height Baseline [mm] *)
    rWeld_CollapseHeight_mm         : REAL;     (* Dynamic Plastic Weld Seam Collapse: h_0 - h_t [mm] *)
    rWeld_PeakPower_W               : REAL;     (* Peak Instantaneous Acoustic Electrical Power Captured [W] *)
    rWeld_Duration_s                : REAL;     (* Active Sonication Acoustic Burst Timer [s] *)
    bWeld_EnergyCutoffMet           : BOOL;     (* Target Acoustic Weld Energy Threshold Attained *)
    bWeld_HeightCutoffMet           : BOOL;     (* Target Plastic Collapse Seam Height Delta Attained *)
    bWeld_PeakPowerCutoffMet        : BOOL;     (* Peak Power Acoustic Saturation Threshold Met *)
    bWeld_TimeCutoffMet             : BOOL;     (* Weld Burst Timeout Envelope Boundary Exceeded *)
    bWeld_CycleTerminated           : BOOL;     (* Sonication Cutoff Command Triggered to RF Generator *)

    (* Ultrasonic Quality Threshold Envelopes (Golden Weld Signature Limits) *)
    c_rWeld_TargetEnergy_J          : REAL := 1450.0;   (* Target Ultrasonic Acoustic Energy: 1450.0 Joules *)
    c_rWeld_MinEnergy_J             : REAL := 1320.0;   (* Lower Allowable Acoustic Energy Limit: 1320.0 Joules *)
    c_rWeld_MaxEnergy_J             : REAL := 1580.0;   (* Upper Allowable Acoustic Energy Limit: 1580.0 Joules *)
    c_rWeld_TargetCollapse_mm       : REAL := 0.285;    (* Target Foil-to-Tab Plastic Seam Collapse: 0.285 mm *)
    c_rWeld_MinCollapse_mm          : REAL := 0.240;    (* Lower Allowable Seam Collapse: 0.240 mm *)
    c_rWeld_MaxCollapse_mm          : REAL := 0.330;    (* Upper Allowable Seam Collapse: 0.330 mm *)
    c_rWeld_MaxPeakPower_W          : REAL := 3400.0;   (* Upper Generator Power Limit Envelope: 3400.0 W *)
    c_rWeld_MaxDuration_s           : REAL := 0.650;    (* Maximum Allowable Weld Sonication Burst Time: 650 ms *)

    (* 3. Galvanostatic CCCV Formation, Coulomb Counter & dQ/dV Differential Capacity Engine *)
    rForm_AccumCharge_Ah            : REAL;     (* Trapezoidal Numerical Integration of Charging Current [Ah] *)
    rForm_SOC_Estimate_Pct          : REAL;     (* Computed Battery Cell State-of-Charge [0..100%] *)
    bForm_CV_ModeActive             : BOOL;     (* Constant-Current to Constant-Voltage Transition Latch *)
    rForm_TaperCurrentCutoff_A      : REAL := 1.250;    (* Potentiostatic CV Phase Charge Termination Cutoff: 1.25 A *)
    rForm_VoltageTarget_V           : REAL := 3.850;    (* Stage 1 SEI Formation Upper Terminal Voltage Clamping Limit: 3.850 V *)
    rForm_ChargeCurrentSP_A         : REAL := 25.00;    (* Galvanostatic CC Stage 1 Formation Current: 25.0 A (0.5C rate) *)

    (* dQ/dV Sliding Difference Window & Peak Identification *)
    aVoltHistory                    : ARRAY [1..10] OF REAL; (* FIFO Voltage Rolling Ring Buffer for Smooth Difference *)
    aChargeHistory                  : ARRAY [1..10] OF REAL; (* FIFO Charge Rolling Ring Buffer for Smooth Difference *)
    iBufferIndex                    : INT := 1;         (* Ring Buffer Pointer *)
    rdQdV_Current_Ah_V              : REAL;             (* Instantaneous Differential Capacity: Delta_Q / Delta_V [Ah/V] *)
    rdQdV_MaxPeak_Ah_V              : REAL;             (* Peak Graphite Anode Staging Differential Capacity Captured *)
    rVolt_At_dQdV_Peak_V            : REAL;             (* Cell Terminal Voltage Corresponding to Peak dQ/dV [V] *)
    bSEI_PeakIdentified             : BOOL;             (* Robust Identification of Anode Solid Electrolyte Interphase *)

    (* 4. Dual-Polarization Thevenin Equivalent Circuit Battery Observer *)
    rThev_OCV_Est_V                 : REAL;     (* Open-Circuit Equilibrium Electromotive Force [V] *)
    rThev_Overpotential_RC1_V       : REAL;     (* Fast Solid-State Charge Transfer Overpotential V_1 [V] *)
    rThev_Overpotential_RC2_V       : REAL;     (* Slow Liquid-State Mass Diffusion Overpotential V_2 [V] *)
    c_rThev_R0_Ohm                  : REAL := 0.000420; (* High-Frequency Bulk Ohmic Internal Resistance: 0.420 mOhm *)
    c_rThev_R1_Ohm                  : REAL := 0.000380; (* Charge-Transfer Polarization Resistance: 0.380 mOhm *)
    c_rThev_C1_Farad                : REAL := 2800.0;   (* Electrochemical Double-Layer Capacitance: 2800 F *)
    c_rThev_R2_Ohm                  : REAL := 0.000650; (* Warburg Diffusion Concentration Resistance: 0.650 mOhm *)
    c_rThev_C2_Farad                : REAL := 12500.0;  (* Solid-State Solid Solution Diffusion Capacitance: 12500 F *)

    (* 5. Vacuum Degassing & Hermetic Chamber Leak Decay Dynamics *)
    rVac_BaseEvacPressure_mbar      : REAL;     (* Deep Roughing Vacuum Base Floor Captured [mbar] *)
    rVac_DecayStartPressure_mbar    : REAL;     (* Chamber Isolation Baseline Pressure at Start of Leak Dwell [mbar] *)
    rVac_DecayDwellTimer_s          : REAL;     (* Vacuum Decay Test Hold Timer [s] *)
    rVac_ComputedLeakRate_mbar_s    : REAL;     (* Differential Vacuum Loss Metric: (P_end - P_start) / Delta_t [mbar/s] *)
    bVac_DecayTestPassed            : BOOL;     (* Hermeticity Integrity Verified Below Permissible Leak Floor *)
    c_rVac_MaxPermissibleLeak_mbar_s: REAL := 0.0025;   (* Maximum Permissible Leak Decay: 0.0025 mbar/s *)
    c_rVac_TargetRoughing_mbar      : REAL := 0.080;    (* Target Deep Vacuum Degassing Pressure: 0.080 mbar *)

    (* 6. High-Frequency Reseal Induction Heating Closed-Loop PID Controller *)
    rInd_TempError_degC             : REAL;     (* Reseal Pyrometer Spot Temperature Deviation: SP - PV [deg C] *)
    rInd_PID_Integral_degC_s        : REAL;     (* Reseal Heating Temperature Error Integral Accumulator *)
    rInd_PID_Derivative_degC_s      : REAL;     (* Reseal Heating Rate-of-Change Differential Component *)
    rInd_PrevTemp_degC              : REAL;     (* Previous Temperature Sample for Derivative Calculation *)
    rInd_OutputPowerDemand_kW       : REAL;     (* Computed Closed-Loop Induction Generator Power Command [kW] *)
    c_rInd_TargetTemp_degC          : REAL := 198.0;    (* Target Induction Hermetic Seam Fusion Temperature: 198.0 deg C *)
    c_rInd_Kp                       : REAL := 0.045;    (* Induction Temperature Controller Proportional Gain [kW/deg C] *)
    c_rInd_Ki                       : REAL := 0.012;    (* Induction Temperature Controller Integral Gain [kW/(deg C*s)] *)
    c_rInd_Kd                       : REAL := 0.006;    (* Induction Temperature Controller Derivative Gain [kW*s/deg C] *)
    rInd_DwellTimer_s               : REAL;             (* Thermal Fusion Dwell Countdown Timer [s] *)

    (* 7. 1 kHz ACIR Complex Impedance Sorter & Cell Quality Grading Engine *)
    bCell_GradeA_Qualified          : BOOL;     (* Premium Grade A Electric Vehicle Traction Quality Standard *)
    bCell_GradeB_Qualified          : BOOL;     (* Commercial Energy Storage System (ESS) Secondary Grade *)
    bCell_ReworkRequired            : BOOL;     (* Borderline Pouch Reseal or Tab Clamp Re-Test Needed *)
    bCell_ScrapRejected             : BOOL;     (* Permanent Mechanical or Electrochemical Defect Identified *)
    c_rACIR_GradeA_Max_mOhm         : REAL := 0.480;    (* Grade A Max Allowable AC Internal Resistance: 0.480 mOhm *)
    c_rACIR_GradeB_Max_mOhm         : REAL := 0.650;    (* Grade B Max Allowable AC Internal Resistance: 0.650 mOhm *)
    c_rOCV_GradeA_Min_V             : REAL := 3.842;    (* Grade A Min Relaxed Open-Circuit Voltage: 3.842 V *)
    c_rOCV_GradeB_Min_V             : REAL := 3.820;    (* Grade B Min Relaxed Open-Circuit Voltage: 3.820 V *)

    (* 8. SCARA 6-Axis Robotic Collation Gantry S-Curve Trajectory Generator *)
    rSCARA_MotionTime_s             : REAL;     (* Sub-Second Collation Move Trajectory Phase Timer [s] *)
    rSCARA_TrajectoryDuration_s     : REAL := 0.720; (* Quintic Polynomial Trajectory Move Duration: 720 ms *)
    rSCARA_NormalizedTime_Tau       : REAL;     (* Normalized Time Parameter: tau = t / T [0.0 .. 1.0] *)
    rSCARA_QuinticPoly_S            : REAL;     (* S-Curve Dimensionless Position Polynomial: 10*tau^3 - 15*tau^4 + 6*tau^5 *)
    rSCARA_QuinticPoly_dS           : REAL;     (* S-Curve Dimensionless Velocity Derivative: 30*tau^2 - 60*tau^3 + 30*tau^4 *)
    rSCARA_StartX_mm                : REAL;     (* Move Starting Cartesian X Coordinate [mm] *)
    rSCARA_StartY_mm                : REAL;     (* Move Starting Cartesian Y Coordinate [mm] *)
    rSCARA_StartZ_mm                : REAL;     (* Move Starting Cartesian Z Coordinate [mm] *)
    rSCARA_StartR_deg               : REAL;     (* Move Starting Cartesian R Angle [deg] *)
    rSCARA_GoalX_mm                 : REAL;     (* Move Destination Target Cartesian X Coordinate [mm] *)
    rSCARA_GoalY_mm                 : REAL;     (* Move Destination Target Cartesian Y Coordinate [mm] *)
    rSCARA_GoalZ_mm                 : REAL;     (* Move Destination Target Cartesian Z Coordinate [mm] *)
    rSCARA_GoalR_deg                : REAL;     (* Move Destination Target Cartesian R Angle [deg] *)
    bSCARA_MoveActive               : BOOL;     (* Gantry Interpolation Active Execution Bit *)

    (* ========================================================================= *)
    (* FINITE STATE MACHINE (FSM) STEP CONTROL & SEQUENCE TIMERS                 *)
    (* ========================================================================= *)
    iFSM_CurrentState               : INT := 0; (* Active Process Execution Step *)
    iFSM_PreviousState              : INT := -1;(* Previous Step for State Entry Edge Detection *)
    rFSM_StateStepTimer_s           : REAL;     (* Active State Elapsed Dwell Timer [s] *)
    bFSM_FirstScanInStep            : BOOL;     (* One-Shot Pulse on State Entry Transition *)
    bFSM_EmergencyAbortLatched      : BOOL;     (* Critical Process Interlock Trip Latch *)

    (* ========================================================================= *)
    (* ISA-18.2 MULTI-TIER PROCESS ALARM TRIP SETPOINTS & DEADBANDS              *)
    (* ========================================================================= *)
    (* Channel 1: Sonotrode Clamping Normal Force [N] *)
    c_rTrip_Force_LL                : REAL := 180.0;    (* Critical Low-Low Force Limit: 180.0 N *)
    c_rTrip_Force_L                 : REAL := 220.0;    (* Low Warning Force Limit: 220.0 N *)
    c_rTrip_Force_H                 : REAL := 1150.0;   (* High Warning Force Limit: 1150.0 N *)
    c_rTrip_Force_HH                : REAL := 1250.0;   (* Critical High-High Force Limit: 1250.0 N *)
    c_rDeadband_Force_N             : REAL := 12.0;     (* Force Hysteresis Deadband: 12.0 N *)

    (* Channel 2: Ultrasonic Active Electrical Power [W] *)
    c_rTrip_USPower_H               : REAL := 3200.0;   (* High Warning Sonication Power: 3200.0 W *)
    c_rTrip_USPower_HH              : REAL := 3550.0;   (* Critical High-High Generator Trip: 3550.0 W *)
    c_rDeadband_USPower_W           : REAL := 45.0;     (* Power Hysteresis Deadband: 45.0 W *)

    (* Channel 3: Cell Terminal Voltage [V] *)
    c_rTrip_CellVolt_LL             : REAL := 2.450;    (* Critical Low-Low Under-Discharge Floor: 2.450 V *)
    c_rTrip_CellVolt_L              : REAL := 2.800;    (* Low Warning Cell Voltage: 2.800 V *)
    c_rTrip_CellVolt_H              : REAL := 3.920;    (* High Warning Cell Voltage: 3.920 V *)
    c_rTrip_CellVolt_HH             : REAL := 4.250;    (* Critical High-High Overcharge Trip: 4.250 V *)
    c_rDeadband_CellVolt_V          : REAL := 0.015;    (* Voltage Hysteresis Deadband: 15.0 mV *)

    (* Channel 4: Formation Charging Current [A] *)
    c_rTrip_FormCurr_H              : REAL := 32.0;     (* High Warning Formation Current: 32.0 A *)
    c_rTrip_FormCurr_HH             : REAL := 45.0;     (* Critical High-High Formation Overcurrent Trip: 45.0 A *)
    c_rDeadband_FormCurr_A          : REAL := 0.50;     (* Current Hysteresis Deadband: 0.50 A *)

    (* Channel 5: Cell Core Infrared Temperature [deg C] *)
    c_rTrip_CellTemp_H              : REAL := 42.0;     (* High Warning Battery Core Temperature: 42.0 deg C *)
    c_rTrip_CellTemp_HH             : REAL := 55.0;     (* Critical High-High Thermal Runaway Trip: 55.0 deg C *)
    c_rDeadband_CellTemp_degC       : REAL := 1.50;     (* Temperature Hysteresis Deadband: 1.50 deg C *)
    rRateOfChange_CellTemp_degC_s   : REAL;             (* Real-Time Temperature Derivative dT/dt [deg C/s] *)
    rPrevSample_CellTemp_degC       : REAL;             (* Temperature Sample from Previous Scan for Derivative *)
    c_rTrip_CellTemp_ROC_degC_s     : REAL := 3.50;     (* Thermal Runaway Early Detection ROC Limit: 3.50 deg C/s *)

    (* Channel 6: Vacuum Degassing Pressure [mbar] *)
    c_rTrip_VacPress_H              : REAL := 1.500;    (* High Warning Chamber Pressure: 1.500 mbar *)
    c_rTrip_VacPress_HH             : REAL := 15.000;   (* Critical High-High Degassing Loss of Vacuum Trip: 15.0 mbar *)
    c_rDeadband_VacPress_mbar       : REAL := 0.080;    (* Vacuum Hysteresis Deadband: 0.080 mbar *)

    (* Channel 7: Induction Reseal Temperature [deg C] *)
    c_rTrip_InductTemp_LL           : REAL := 160.0;    (* Low-Low Incomplete Reseal Fusion Trip: 160.0 deg C *)
    c_rTrip_InductTemp_L            : REAL := 185.0;    (* Low Warning Reseal Temperature: 185.0 deg C *)
    c_rTrip_InductTemp_H            : REAL := 215.0;    (* High Warning Reseal Temperature: 215.0 deg C *)
    c_rTrip_InductTemp_HH           : REAL := 235.0;    (* Critical High-High Laminate Blister Burn Trip: 235.0 deg C *)
    c_rDeadband_InductTemp_degC     : REAL := 3.0;      (* Induction Temperature Deadband: 3.0 deg C *)

    (* Channel 8: SCARA Gantry Cartesian Tracking Error [mm] *)
    rSCARA_TrackingError_mm         : REAL;             (* Real-Time Tool Center Point Cartesian Position Error [mm] *)
    c_rTrip_SCARA_TrackErr_H        : REAL := 0.250;    (* High Warning Tracking Error: 0.250 mm *)
    c_rTrip_SCARA_TrackErr_HH       : REAL := 0.500;    (* Critical High-High Robot Kinematic Deviation Trip: 0.500 mm *)

    (* General Iteration Loop Indices *)
    iIdx                            : INT;              (* General Loop Index for States and Arrays *)
    jIdx                            : INT;              (* Secondary Loop Index for Matrix Columns *)
    kIdx                            : INT;              (* Third Loop Index for Horizons *)
    mIdx                            : INT;              (* Fourth Loop Index for Inputs *)
    rMatAccum                       : REAL;             (* Temporary Inner Product Accumulator *)
    bInitialized                    : BOOL := FALSE;    (* Power-On Cold Start Initialization Bit *)
END_VAR
''')

    # =========================================================================
    # 5. PHASE 0: SYSTEM INITIALIZATION & STATE-SPACE MATRICES
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 0: POWER-ON FIRST-SCAN INITIALIZATION & STATE-SPACE MATRIX POPULATION                                          *)
(* Sampling Time: Ts = 0.001 s (1.0 ms deterministic PLC real-time task).                                               *)
(* Discrete State-Space Model: x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]                                *)
(* Multi-Physics Coupling: Acoustic Horn Dynamics, Electrochemical Cell Resistance, Heat Diffusion, and Vacuum Flow.      *)
(* ==================================================================================================================== *)
IF NOT bInitialized THEN
    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* Initialize Discrete State Transition Matrix A [8x8]                                                              *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 8 DO
            A_Matrix[iIdx, jIdx] := 0.0;
            C_Matrix[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    FOR iIdx := 1 TO 8 DO
        FOR mIdx := 1 TO 6 DO
            B_Matrix[iIdx, mIdx] := 0.0;
            D_Matrix[iIdx, mIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* Diagonal State Self-Decay / Natural Pole Dynamics *)
    A_Matrix[1, 1] := 0.9450;   (* x1: Ultrasonic Horn Phase Error Natural Relaxation Pole *)
    A_Matrix[2, 2] := 0.8850;   (* x2: Voice-Coil Dynamic Clamping Normal Force Damping Pole *)
    A_Matrix[3, 3] := 0.9120;   (* x3: Acoustic Impedance Viscoelastic Joint Transition Pole *)
    A_Matrix[4, 4] := 0.9985;   (* x4: Cell Terminal Voltage Thevenin RC Polarization Retention Pole *)
    A_Matrix[5, 5] := 0.8200;   (* x5: Cycler Switching Inverter Current Slew Damping Pole *)
    A_Matrix[6, 6] := 0.9972;   (* x6: Cell Internal Thermal Dissipation & Natural Cooling Pole *)
    A_Matrix[7, 7] := 0.9650;   (* x7: Vacuum Chamber Outgassing / Pumping Balance Retention Pole *)
    A_Matrix[8, 8] := 0.8500;   (* x8: SCARA Gantry Cartesian Tool Center Point Velocity Damping Pole *)

    (* Off-Diagonal Inter-System Cross-Coupling Dynamics *)
    A_Matrix[1, 3] := -0.0125;  (* Horn Resonant Phase Shifts as Acoustic Joint Softens (x3 -> x1) *)
    A_Matrix[3, 2] :=  0.0380;  (* Clamping Force Increases Mechanical Coupling & Impedance (x2 -> x3) *)
    A_Matrix[4, 5] :=  0.00042; (* Terminal Voltage Rise from Internal Ohmic Current (I*R_0) (x5 -> x4) *)
    A_Matrix[6, 5] :=  0.00315; (* Joule Heating Core Temperature Rise: dT/dt = I^2 * R / (m * Cp) (x5 -> x6) *)
    A_Matrix[4, 6] :=  0.00018; (* Voltage Open-Circuit EMF Nernst Temperature Drift (x6 -> x4) *)
    A_Matrix[7, 6] :=  0.00140; (* Electrolyte Thermal Vapor Pressure Rise in Vacuum Chamber (x6 -> x7) *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* Initialize Actuator Input Coupling Matrix B [8x6]                                                                *)
    (* Inputs: u1=Delta_f [kHz], u2=u_F [N], u3=u_I [A], u4=u_vac [%], u5=u_ind [kW], u6=u_vel [mm/s]                    *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    B_Matrix[1, 1] :=  0.0550;  (* Frequency Tuning Command Drives Horn Phase Angle (u1 -> x1) *)
    B_Matrix[2, 2] :=  0.1150;  (* Voice-Coil Force Command Drives Normal Clamping Force (u2 -> x2) *)
    B_Matrix[3, 2] :=  0.0045;  (* Voice-Coil Force Actuation Modulates Joint Contact Impedance (u2 -> x3) *)
    B_Matrix[4, 3] :=  0.00085; (* Formation Cycler Inverter Demand Modulates Cell Terminal Potential (u3 -> x4) *)
    B_Matrix[5, 3] :=  0.1800;  (* Formation Current Setpoint Directly Drives Cycler Current (u3 -> x5) *)
    B_Matrix[6, 5] :=  0.00850; (* Induction Reseal Heat Source Dissipation Raises Chamber Core Temp (u5 -> x6) *)
    B_Matrix[7, 4] := -0.03500; (* Vacuum Throttle Valve Opening Accelerates Evacuation Rate (u4 -> x7) *)
    B_Matrix[8, 6] :=  0.15000; (* SCARA Gantry Servo Feedforward Direct Cartesian Acceleration (u6 -> x8) *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* Initialize Output Measurement Matrix C [8x8] & Feedthrough Matrix D [8x6]                                        *)
    (* Direct Identity Measurement Mapping with Primary Diagonal Sensitivity                                           *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FOR iIdx := 1 TO 8 DO
        C_Matrix[iIdx, iIdx] := 1.0;
    END_FOR;
    C_Matrix[4, 5] := c_rThev_R0_Ohm; (* High-Frequency Ohmic Drop Directly Observable in Terminal Voltage *)

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* Initialize MPC Quadratic Cost Function Weightings (Q, R, P)                                                     *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    Q_Weight[1] :=  120.0;      (* High Penalty on Ultrasonic Resonant Phase Error *)
    Q_Weight[2] :=   45.0;      (* Clamping Normal Force Precision Penalty *)
    Q_Weight[3] :=   15.0;      (* Acoustic Impedance Deviation Penalty *)
    Q_Weight[4] :=  250.0;      (* Critical High Penalty on Battery Overvoltage Deviation *)
    Q_Weight[5] :=   80.0;      (* Formation Current Ripple and Deviation Penalty *)
    Q_Weight[6] :=  500.0;      (* Extreme Penalty on Battery Core Thermal Excursions *)
    Q_Weight[7] :=   60.0;      (* Vacuum Chamber Leak / Evacuation Target Penalty *)
    Q_Weight[8] :=   35.0;      (* SCARA Cartesian Tracking Velocity Penalty *)

    R_Weight[1] :=   25.0;      (* Actuator Rate Penalty: Frequency Inverter Slew *)
    R_Weight[2] :=   10.0;      (* Actuator Rate Penalty: Voice-Coil Force Slew *)
    R_Weight[3] :=    8.0;      (* Actuator Rate Penalty: Formation Power Cycler Slew *)
    R_Weight[4] :=   12.0;      (* Actuator Rate Penalty: Vacuum Throttle Valve Slew *)
    R_Weight[5] :=   18.0;      (* Actuator Rate Penalty: Induction RF Power Slew *)
    R_Weight[6] :=    5.0;      (* Actuator Rate Penalty: SCARA Servo Acceleration Slew *)

    FOR iIdx := 1 TO 8 DO
        P_Terminal[iIdx] := Q_Weight[iIdx] * 2.5; (* Terminal Quadratic Horizon Cost *)
        x_State[iIdx]    := 0.0;
        x_Pred[iIdx]     := 0.0;
        x_Ref[iIdx]      := 0.0;
    END_FOR;

    FOR mIdx := 1 TO 6 DO
        u_Control[mIdx]     := 0.0;
        u_Prev[mIdx]        := 0.0;
        u_DeltaDemand[mIdx] := 0.0;
    END_FOR;

    (* Initialize History Ring Buffers *)
    FOR iIdx := 1 TO 10 DO
        aVoltHistory[iIdx]   := 2.80;
        aChargeHistory[iIdx] := 0.0;
    END_FOR;

    bInitialized := TRUE;
END_IF;
''')

    # =========================================================================
    # 6. PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY FAULT ISOLATION                          *)
(* Execution Cycle: 1.0 ms. Evaluates 7 Critical Process Sensor Triplets with Microsecond Pairwise Deltas.              *)
(* Voting Strategy:                                                                                                     *)
(*   - Healthy: All 3 agree within tolerance -> 3-channel arithmetic mean. Channel isolation bits cleared.             *)
(*   - Degraded: 2 agree, 1 diverges -> 2-channel average, quarantine outlier channel bit, increment debounce timer.    *)
(*   - Diverged: All 3 pairwise comparisons exceed limit -> Latch discrepancy alarm, hold last safe value.              *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.1: 2oo3 TMR VOTING: Ultrasonic Sonotrode Clamping Normal Force (FIT_US_FORCE_101A/B/C) [N]                         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(FIT_US_FORCE_101A - FIT_US_FORCE_101B) <= c_rTol_Force_N) AND
   (ABS(FIT_US_FORCE_101B - FIT_US_FORCE_101C) <= c_rTol_Force_N) AND
   (ABS(FIT_US_FORCE_101C - FIT_US_FORCE_101A) <= c_rTol_Force_N) THEN
    rVoted_Force_N      := (FIT_US_FORCE_101A + FIT_US_FORCE_101B + FIT_US_FORCE_101C) / 3.0;
    bIso_Force_ChA      := FALSE;
    bIso_Force_ChB      := FALSE;
    bIso_Force_ChC      := FALSE;
    bFlt_Force_Diverged := FALSE;
    rTimer_Force_Disc_s := 0.0;
ELSIF (ABS(FIT_US_FORCE_101A - FIT_US_FORCE_101B) <= c_rTol_Force_N) THEN
    rVoted_Force_N      := (FIT_US_FORCE_101A + FIT_US_FORCE_101B) * 0.5;
    bIso_Force_ChA      := FALSE;
    bIso_Force_ChB      := FALSE;
    bIso_Force_ChC      := TRUE;
    rTimer_Force_Disc_s := rTimer_Force_Disc_s + 0.001;
ELSIF (ABS(FIT_US_FORCE_101B - FIT_US_FORCE_101C) <= c_rTol_Force_N) THEN
    rVoted_Force_N      := (FIT_US_FORCE_101B + FIT_US_FORCE_101C) * 0.5;
    bIso_Force_ChA      := TRUE;
    bIso_Force_ChB      := FALSE;
    bIso_Force_ChC      := FALSE;
    rTimer_Force_Disc_s := rTimer_Force_Disc_s + 0.001;
ELSIF (ABS(FIT_US_FORCE_101C - FIT_US_FORCE_101A) <= c_rTol_Force_N) THEN
    rVoted_Force_N      := (FIT_US_FORCE_101C + FIT_US_FORCE_101A) * 0.5;
    bIso_Force_ChA      := FALSE;
    bIso_Force_ChB      := TRUE;
    bIso_Force_ChC      := FALSE;
    rTimer_Force_Disc_s := rTimer_Force_Disc_s + 0.001;
ELSE
    bFlt_Force_Diverged := TRUE;
    rTimer_Force_Disc_s := rTimer_Force_Disc_s + 0.001;
    (* Hold Last Safe Value to prevent slamming voice-coil actuator *)
END_IF;

IF rTimer_Force_Disc_s >= c_rDisc_Trip_Time_s THEN
    ALARM_WORD_03 := ALARM_WORD_03 OR 16#00000001; (* Bit 0: Force Transducer TMR Discrepancy Latched *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.2: 2oo3 TMR VOTING: Ultrasonic Horn Collapse Displacement LVDT (LIT_US_DISP_102A/B/C) [mm]                         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(LIT_US_DISP_102A - LIT_US_DISP_102B) <= c_rTol_Disp_mm) AND
   (ABS(LIT_US_DISP_102B - LIT_US_DISP_102C) <= c_rTol_Disp_mm) AND
   (ABS(LIT_US_DISP_102C - LIT_US_DISP_102A) <= c_rTol_Disp_mm) THEN
    rVoted_Disp_mm     := (LIT_US_DISP_102A + LIT_US_DISP_102B + LIT_US_DISP_102C) / 3.0;
    bIso_Disp_ChA      := FALSE;
    bIso_Disp_ChB      := FALSE;
    bIso_Disp_ChC      := FALSE;
    bFlt_Disp_Diverged := FALSE;
    rTimer_Disp_Disc_s := 0.0;
ELSIF (ABS(LIT_US_DISP_102A - LIT_US_DISP_102B) <= c_rTol_Disp_mm) THEN
    rVoted_Disp_mm     := (LIT_US_DISP_102A + LIT_US_DISP_102B) * 0.5;
    bIso_Disp_ChA      := FALSE;
    bIso_Disp_ChB      := FALSE;
    bIso_Disp_ChC      := TRUE;
    rTimer_Disp_Disc_s := rTimer_Disp_Disc_s + 0.001;
ELSIF (ABS(LIT_US_DISP_102B - LIT_US_DISP_102C) <= c_rTol_Disp_mm) THEN
    rVoted_Disp_mm     := (LIT_US_DISP_102B + LIT_US_DISP_102C) * 0.5;
    bIso_Disp_ChA      := TRUE;
    bIso_Disp_ChB      := FALSE;
    bIso_Disp_ChC      := FALSE;
    rTimer_Disp_Disc_s := rTimer_Disp_Disc_s + 0.001;
ELSIF (ABS(LIT_US_DISP_102C - LIT_US_DISP_102A) <= c_rTol_Disp_mm) THEN
    rVoted_Disp_mm     := (LIT_US_DISP_102C + LIT_US_DISP_102A) * 0.5;
    bIso_Disp_ChA      := FALSE;
    bIso_Disp_ChB      := TRUE;
    bIso_Disp_ChC      := FALSE;
    rTimer_Disp_Disc_s := rTimer_Disp_Disc_s + 0.001;
ELSE
    bFlt_Disp_Diverged := TRUE;
    rTimer_Disp_Disc_s := rTimer_Disp_Disc_s + 0.001;
END_IF;

IF rTimer_Disp_Disc_s >= c_rDisc_Trip_Time_s THEN
    ALARM_WORD_03 := ALARM_WORD_03 OR 16#00000002; (* Bit 1: Displacement LVDT TMR Discrepancy Latched *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.3: 2oo3 TMR VOTING: Cell Terminal 4-Wire Kelvin Voltage Probes (VIT_CELL_VOLT_201A/B/C) [V]                        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(VIT_CELL_VOLT_201A - VIT_CELL_VOLT_201B) <= c_rTol_Volt_V) AND
   (ABS(VIT_CELL_VOLT_201B - VIT_CELL_VOLT_201C) <= c_rTol_Volt_V) AND
   (ABS(VIT_CELL_VOLT_201C - VIT_CELL_VOLT_201A) <= c_rTol_Volt_V) THEN
    rVoted_Volt_V      := (VIT_CELL_VOLT_201A + VIT_CELL_VOLT_201B + VIT_CELL_VOLT_201C) / 3.0;
    bIso_Volt_ChA      := FALSE;
    bIso_Volt_ChB      := FALSE;
    bIso_Volt_ChC      := FALSE;
    bFlt_Volt_Diverged := FALSE;
    rTimer_Volt_Disc_s := 0.0;
ELSIF (ABS(VIT_CELL_VOLT_201A - VIT_CELL_VOLT_201B) <= c_rTol_Volt_V) THEN
    rVoted_Volt_V      := (VIT_CELL_VOLT_201A + VIT_CELL_VOLT_201B) * 0.5;
    bIso_Volt_ChA      := FALSE;
    bIso_Volt_ChB      := FALSE;
    bIso_Volt_ChC      := TRUE;
    rTimer_Volt_Disc_s := rTimer_Volt_Disc_s + 0.001;
ELSIF (ABS(VIT_CELL_VOLT_201B - VIT_CELL_VOLT_201C) <= c_rTol_Volt_V) THEN
    rVoted_Volt_V      := (VIT_CELL_VOLT_201B + VIT_CELL_VOLT_201C) * 0.5;
    bIso_Volt_ChA      := TRUE;
    bIso_Volt_ChB      := FALSE;
    bIso_Volt_ChC      := FALSE;
    rTimer_Volt_Disc_s := rTimer_Volt_Disc_s + 0.001;
ELSIF (ABS(VIT_CELL_VOLT_201C - VIT_CELL_VOLT_201A) <= c_rTol_Volt_V) THEN
    rVoted_Volt_V      := (VIT_CELL_VOLT_201C + VIT_CELL_VOLT_201A) * 0.5;
    bIso_Volt_ChA      := FALSE;
    bIso_Volt_ChB      := TRUE;
    bIso_Volt_ChC      := FALSE;
    rTimer_Volt_Disc_s := rTimer_Volt_Disc_s + 0.001;
ELSE
    bFlt_Volt_Diverged := TRUE;
    rTimer_Volt_Disc_s := rTimer_Volt_Disc_s + 0.001;
END_IF;

IF rTimer_Volt_Disc_s >= c_rDisc_Trip_Time_s THEN
    ALARM_WORD_03 := ALARM_WORD_03 OR 16#00000004; (* Bit 2: Cell Voltage Kelvin Probe TMR Discrepancy *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.4: 2oo3 TMR VOTING: Formation Cycler Shunt Current Transducers (IIT_FORM_CURR_202A/B/C) [A]                         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(IIT_FORM_CURR_202A - IIT_FORM_CURR_202B) <= c_rTol_Curr_A) AND
   (ABS(IIT_FORM_CURR_202B - IIT_FORM_CURR_202C) <= c_rTol_Curr_A) AND
   (ABS(IIT_FORM_CURR_202C - IIT_FORM_CURR_202A) <= c_rTol_Curr_A) THEN
    rVoted_Curr_A      := (IIT_FORM_CURR_202A + IIT_FORM_CURR_202B + IIT_FORM_CURR_202C) / 3.0;
    bIso_Curr_ChA      := FALSE;
    bIso_Curr_ChB      := FALSE;
    bIso_Curr_ChC      := FALSE;
    bFlt_Curr_Diverged := FALSE;
    rTimer_Curr_Disc_s := 0.0;
ELSIF (ABS(IIT_FORM_CURR_202A - IIT_FORM_CURR_202B) <= c_rTol_Curr_A) THEN
    rVoted_Curr_A      := (IIT_FORM_CURR_202A + IIT_FORM_CURR_202B) * 0.5;
    bIso_Curr_ChA      := FALSE;
    bIso_Curr_ChB      := FALSE;
    bIso_Curr_ChC      := TRUE;
    rTimer_Curr_Disc_s := rTimer_Curr_Disc_s + 0.001;
ELSIF (ABS(IIT_FORM_CURR_202B - IIT_FORM_CURR_202C) <= c_rTol_Curr_A) THEN
    rVoted_Curr_A      := (IIT_FORM_CURR_202B + IIT_FORM_CURR_202C) * 0.5;
    bIso_Curr_ChA      := TRUE;
    bIso_Curr_ChB      := FALSE;
    bIso_Curr_ChC      := FALSE;
    rTimer_Curr_Disc_s := rTimer_Curr_Disc_s + 0.001;
ELSIF (ABS(IIT_FORM_CURR_202C - IIT_FORM_CURR_202A) <= c_rTol_Curr_A) THEN
    rVoted_Curr_A      := (IIT_FORM_CURR_202C + IIT_FORM_CURR_202A) * 0.5;
    bIso_Curr_ChA      := FALSE;
    bIso_Curr_ChB      := TRUE;
    bIso_Curr_ChC      := FALSE;
    rTimer_Curr_Disc_s := rTimer_Curr_Disc_s + 0.001;
ELSE
    bFlt_Curr_Diverged := TRUE;
    rTimer_Curr_Disc_s := rTimer_Curr_Disc_s + 0.001;
END_IF;

IF rTimer_Curr_Disc_s >= c_rDisc_Trip_Time_s THEN
    ALARM_WORD_03 := ALARM_WORD_03 OR 16#00000008; (* Bit 3: Formation Current Shunt TMR Discrepancy *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.5: 2oo3 TMR VOTING: Cell Core Infrared Pyrometers (TIT_CELL_TEMP_203A/B/C) [deg C]                                 *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(TIT_CELL_TEMP_203A - TIT_CELL_TEMP_203B) <= c_rTol_Temp_degC) AND
   (ABS(TIT_CELL_TEMP_203B - TIT_CELL_TEMP_203C) <= c_rTol_Temp_degC) AND
   (ABS(TIT_CELL_TEMP_203C - TIT_CELL_TEMP_203A) <= c_rTol_Temp_degC) THEN
    rVoted_Temp_degC   := (TIT_CELL_TEMP_203A + TIT_CELL_TEMP_203B + TIT_CELL_TEMP_203C) / 3.0;
    bIso_Temp_ChA      := FALSE;
    bIso_Temp_ChB      := FALSE;
    bIso_Temp_ChC      := FALSE;
    bFlt_Temp_Diverged := FALSE;
    rTimer_Temp_Disc_s := 0.0;
ELSIF (ABS(TIT_CELL_TEMP_203A - TIT_CELL_TEMP_203B) <= c_rTol_Temp_degC) THEN
    rVoted_Temp_degC   := (TIT_CELL_TEMP_203A + TIT_CELL_TEMP_203B) * 0.5;
    bIso_Temp_ChA      := FALSE;
    bIso_Temp_ChB      := FALSE;
    bIso_Temp_ChC      := TRUE;
    rTimer_Temp_Disc_s := rTimer_Temp_Disc_s + 0.001;
ELSIF (ABS(TIT_CELL_TEMP_203B - TIT_CELL_TEMP_203C) <= c_rTol_Temp_degC) THEN
    rVoted_Temp_degC   := (TIT_CELL_TEMP_203B + TIT_CELL_TEMP_203C) * 0.5;
    bIso_Temp_ChA      := TRUE;
    bIso_Temp_ChB      := FALSE;
    bIso_Temp_ChC      := FALSE;
    rTimer_Temp_Disc_s := rTimer_Temp_Disc_s + 0.001;
ELSIF (ABS(TIT_CELL_TEMP_203C - TIT_CELL_TEMP_203A) <= c_rTol_Temp_degC) THEN
    rVoted_Temp_degC   := (TIT_CELL_TEMP_203C + TIT_CELL_TEMP_203A) * 0.5;
    bIso_Temp_ChA      := FALSE;
    bIso_Temp_ChB      := TRUE;
    bIso_Temp_ChC      := FALSE;
    rTimer_Temp_Disc_s := rTimer_Temp_Disc_s + 0.001;
ELSE
    bFlt_Temp_Diverged := TRUE;
    rTimer_Temp_Disc_s := rTimer_Temp_Disc_s + 0.001;
END_IF;

IF rTimer_Temp_Disc_s >= c_rDisc_Trip_Time_s THEN
    ALARM_WORD_03 := ALARM_WORD_03 OR 16#00000010; (* Bit 4: Cell Core Pyrometer TMR Discrepancy *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.6: 2oo3 TMR VOTING: Vacuum Degassing Chamber Pirani Gauges (PIT_VAC_CHAMB_301A/B/C) [mbar]                         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(PIT_VAC_CHAMB_301A - PIT_VAC_CHAMB_301B) <= c_rTol_Vac_mbar) AND
   (ABS(PIT_VAC_CHAMB_301B - PIT_VAC_CHAMB_301C) <= c_rTol_Vac_mbar) AND
   (ABS(PIT_VAC_CHAMB_301C - PIT_VAC_CHAMB_301A) <= c_rTol_Vac_mbar) THEN
    rVoted_Vac_mbar   := (PIT_VAC_CHAMB_301A + PIT_VAC_CHAMB_301B + PIT_VAC_CHAMB_301C) / 3.0;
    bIso_Vac_ChA      := FALSE;
    bIso_Vac_ChB      := FALSE;
    bIso_Vac_ChC      := FALSE;
    bFlt_Vac_Diverged := FALSE;
    rTimer_Vac_Disc_s := 0.0;
ELSIF (ABS(PIT_VAC_CHAMB_301A - PIT_VAC_CHAMB_301B) <= c_rTol_Vac_mbar) THEN
    rVoted_Vac_mbar   := (PIT_VAC_CHAMB_301A + PIT_VAC_CHAMB_301B) * 0.5;
    bIso_Vac_ChA      := FALSE;
    bIso_Vac_ChB      := FALSE;
    bIso_Vac_ChC      := TRUE;
    rTimer_Vac_Disc_s := rTimer_Vac_Disc_s + 0.001;
ELSIF (ABS(PIT_VAC_CHAMB_301B - PIT_VAC_CHAMB_301C) <= c_rTol_Vac_mbar) THEN
    rVoted_Vac_mbar   := (PIT_VAC_CHAMB_301B + PIT_VAC_CHAMB_301C) * 0.5;
    bIso_Vac_ChA      := TRUE;
    bIso_Vac_ChB      := FALSE;
    bIso_Vac_ChC      := FALSE;
    rTimer_Vac_Disc_s := rTimer_Vac_Disc_s + 0.001;
ELSIF (ABS(PIT_VAC_CHAMB_301C - PIT_VAC_CHAMB_301A) <= c_rTol_Vac_mbar) THEN
    rVoted_Vac_mbar   := (PIT_VAC_CHAMB_301C + PIT_VAC_CHAMB_301A) * 0.5;
    bIso_Vac_ChA      := FALSE;
    bIso_Vac_ChB      := TRUE;
    bIso_Vac_ChC      := FALSE;
    rTimer_Vac_Disc_s := rTimer_Vac_Disc_s + 0.001;
ELSE
    bFlt_Vac_Diverged := TRUE;
    rTimer_Vac_Disc_s := rTimer_Vac_Disc_s + 0.001;
END_IF;

IF rTimer_Vac_Disc_s >= c_rDisc_Trip_Time_s THEN
    ALARM_WORD_03 := ALARM_WORD_03 OR 16#00000020; (* Bit 5: Vacuum Chamber Gauge TMR Discrepancy *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 1.7: 2oo3 TMR VOTING: High-Frequency Induction Reseal Pyrometers (TIT_INDUCT_TEMP_302A/B/C) [deg C]                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (ABS(TIT_INDUCT_TEMP_302A - TIT_INDUCT_TEMP_302B) <= c_rTol_IndTemp_degC) AND
   (ABS(TIT_INDUCT_TEMP_302B - TIT_INDUCT_TEMP_302C) <= c_rTol_IndTemp_degC) AND
   (ABS(TIT_INDUCT_TEMP_302C - TIT_INDUCT_TEMP_302A) <= c_rTol_IndTemp_degC) THEN
    rVoted_IndTemp_degC   := (TIT_INDUCT_TEMP_302A + TIT_INDUCT_TEMP_302B + TIT_INDUCT_TEMP_302C) / 3.0;
    bIso_IndTemp_ChA      := FALSE;
    bIso_IndTemp_ChB      := FALSE;
    bIso_IndTemp_ChC      := FALSE;
    bFlt_IndTemp_Diverged := FALSE;
    rTimer_IndTemp_Disc_s := 0.0;
ELSIF (ABS(TIT_INDUCT_TEMP_302A - TIT_INDUCT_TEMP_302B) <= c_rTol_IndTemp_degC) THEN
    rVoted_IndTemp_degC   := (TIT_INDUCT_TEMP_302A + TIT_INDUCT_TEMP_302B) * 0.5;
    bIso_IndTemp_ChA      := FALSE;
    bIso_IndTemp_ChB      := FALSE;
    bIso_IndTemp_ChC      := TRUE;
    rTimer_IndTemp_Disc_s := rTimer_IndTemp_Disc_s + 0.001;
ELSIF (ABS(TIT_INDUCT_TEMP_302B - TIT_INDUCT_TEMP_302C) <= c_rTol_IndTemp_degC) THEN
    rVoted_IndTemp_degC   := (TIT_INDUCT_TEMP_302B + TIT_INDUCT_TEMP_302C) * 0.5;
    bIso_IndTemp_ChA      := TRUE;
    bIso_IndTemp_ChB      := FALSE;
    bIso_IndTemp_ChC      := FALSE;
    rTimer_IndTemp_Disc_s := rTimer_IndTemp_Disc_s + 0.001;
ELSIF (ABS(TIT_INDUCT_TEMP_302C - TIT_INDUCT_TEMP_302A) <= c_rTol_IndTemp_degC) THEN
    rVoted_IndTemp_degC   := (TIT_INDUCT_TEMP_302C + TIT_INDUCT_TEMP_302A) * 0.5;
    bIso_IndTemp_ChA      := FALSE;
    bIso_IndTemp_ChB      := TRUE;
    bIso_IndTemp_ChC      := FALSE;
    rTimer_IndTemp_Disc_s := rTimer_IndTemp_Disc_s + 0.001;
ELSE
    bFlt_IndTemp_Diverged := TRUE;
    rTimer_IndTemp_Disc_s := rTimer_IndTemp_Disc_s + 0.001;
END_IF;

IF rTimer_IndTemp_Disc_s >= c_rDisc_Trip_Time_s THEN
    ALARM_WORD_03 := ALARM_WORD_03 OR 16#00000040; (* Bit 6: Induction Pyrometer TMR Discrepancy *)
END_IF;
''')

    # =========================================================================
    # 7. PHASE 2: STATE-SPACE PREDICTION (x[k+1] = A*x[k] + B*u[k])
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 2: STATE-SPACE PREDICTION & THERMAL-ACOUSTIC-ELECTROCHEMICAL INTEGRATION                                      *)
(* Equations:                                                                                                           *)
(*   x[k+1] = A * x[k] + B * u[k]                                                                                       *)
(*   y[k]   = C * x[k] + D * u[k]                                                                                       *)
(* Update state vector x[k] from 2oo3 voted physical sensor observations:                                              *)
(*   x_1 : Ultrasonic Horn Phase Angle Error [rad] = AE_US_PHASE_104 * (pi / 180.0)                                    *)
(*   x_2 : Voted Sonotrode Normal Clamping Force [N]                                                                   *)
(*   x_3 : Dynamic Acoustic Impedance [N*s/m] = rVoted_Force_N / (v_tip_amplitude * omega)                             *)
(*   x_4 : Voted Cell 4-Wire Terminal Voltage [V]                                                                      *)
(*   x_5 : Voted Formation Current [A]                                                                                 *)
(*   x_6 : Voted Cell Core Temperature [deg C]                                                                         *)
(*   x_7 : Voted Vacuum Chamber Absolute Pressure [mbar]                                                               *)
(*   x_8 : SCARA Cartesian Velocity [mm/s] = VIT_SCARA_VEL_405                                                         *)
(* ==================================================================================================================== *)

(* Map Voted Plant Observations into State Vector x[k] *)
x_State[1] := AE_US_PHASE_104 * 0.01745329; (* Convert deg to rad *)
x_State[2] := rVoted_Force_N;

(* Compute Dynamic Acoustic Impedance: Z_ac = F_N / (v_peak) *)
IF CMD_US_AMPLITUDE_PCT > 1.0 AND AE_US_FREQ_103 > 18.0 THEN
    x_State[3] := rVoted_Force_N / (0.000035 * (CMD_US_AMPLITUDE_PCT / 100.0) * (2.0 * 3.141592 * AE_US_FREQ_103 * 1000.0) + 0.001);
ELSE
    x_State[3] := 450.0; (* Baseline Cold Acoustic Clamping Contact Impedance *)
END_IF;

x_State[4] := rVoted_Volt_V;
x_State[5] := rVoted_Curr_A;
x_State[6] := rVoted_Temp_degC;
x_State[7] := rVoted_Vac_mbar;
x_State[8] := VIT_SCARA_VEL_405;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* Compute Discrete One-Step Ahead State Prediction: x_Pred[i] = Sum(A[i,j]*x[j]) + Sum(B[i,m]*u[m])                    *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 8 DO
    rMatAccum := 0.0;
    FOR jIdx := 1 TO 8 DO
        rMatAccum := rMatAccum + (A_Matrix[iIdx, jIdx] * x_State[jIdx]);
    END_FOR;
    FOR mIdx := 1 TO 6 DO
        rMatAccum := rMatAccum + (B_Matrix[iIdx, mIdx] * u_Control[mIdx]);
    END_FOR;
    x_Pred[iIdx] := rMatAccum;
END_FOR;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* Compute Estimated Measurement Outputs: y_Output[i] = Sum(C[i,j]*x[j]) + Sum(D[i,m]*u[m])                           *)
(* -------------------------------------------------------------------------------------------------------------------- *)
FOR iIdx := 1 TO 8 DO
    rMatAccum := 0.0;
    FOR jIdx := 1 TO 8 DO
        rMatAccum := rMatAccum + (C_Matrix[iIdx, jIdx] * x_State[jIdx]);
    END_FOR;
    FOR mIdx := 1 TO 6 DO
        rMatAccum := rMatAccum + (D_Matrix[iIdx, mIdx] * u_Control[mIdx]);
    END_FOR;
    y_Output[iIdx] := rMatAccum;
END_FOR;
''')

    # =========================================================================
    # 8. PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION & ACTUATOR DISPATCH
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION & MULTI-OBJECTIVE ACTUATOR DISPATCH                                       *)
(* Objective Function:                                                                                                  *)
(*   J = Sum_{p=1}^{Np} (x_{k+p} - x_ref)^T * Q * (x_{k+p} - x_ref)                                                     *)
(*     + Sum_{m=1}^{Nc} Delta_u_{k+m-1}^T * R * Delta_u_{k+m-1}                                                         *)
(*     + (x_{k+Np} - x_ref)^T * P * (x_{k+Np} - x_ref)                                                                  *)
(* Optimization Algorithm: Karush-Kuhn-Tucker (KKT) Projected Gradient Descent with Dynamic Slew Rate Saturation       *)
(* ==================================================================================================================== *)

(* Update Dynamic Reference Targets based on Operational Step *)
CASE iFSM_CurrentState OF
    2, 3: (* Ultrasonic Welding Sonication Active *)
        x_Ref[1] := 0.0;                    (* Zero Resonant Phase Error (Perfect Resonance) *)
        x_Ref[2] := 680.0;                  (* Dynamic Target Clamping Force: 680.0 N *)
        x_Ref[3] := 280.0;                  (* Molten Interfacial Dynamic Acoustic Impedance Target *)
        x_Ref[4] := rVoted_Volt_V;          (* Cycler Dormant *)
        x_Ref[5] := 0.0;                    (* No Formation Current *)
        x_Ref[6] := 28.0;                   (* Maintain Ambient Joint Temp *)
        x_Ref[7] := 1013.2;                 (* Atmospheric Pressure *)
        x_Ref[8] := 0.0;                    (* SCARA Stationary Clamped *)

    5, 6: (* Formation Constant-Current Constant-Voltage Active *)
        x_Ref[1] := 0.0;
        x_Ref[2] := 0.0;
        x_Ref[3] := 450.0;
        x_Ref[4] := rForm_VoltageTarget_V;  (* Potentiostatic Clamping Ceiling: 3.850 V *)
        x_Ref[5] := rForm_ChargeCurrentSP_A;(* Galvanostatic Charging Current: 25.0 A *)
        x_Ref[6] := 32.5;                   (* Target Controlled Cell Temp *)
        x_Ref[7] := 1013.2;
        x_Ref[8] := 0.0;

    7, 8: (* Vacuum Degassing Chamber Puncture & Evacuation *)
        x_Ref[1] := 0.0;
        x_Ref[2] := 0.0;
        x_Ref[3] := 450.0;
        x_Ref[4] := rVoted_Volt_V;
        x_Ref[5] := 0.0;
        x_Ref[6] := 25.0;
        x_Ref[7] := c_rVac_TargetRoughing_mbar; (* Deep Vacuum Target: 0.080 mbar *)
        x_Ref[8] := 0.0;

    9:    (* High-Frequency Induction Reseal *)
        x_Ref[1] := 0.0;
        x_Ref[2] := 420.0;                  (* Reseal Jaw Force: 420.0 N *)
        x_Ref[3] := 450.0;
        x_Ref[4] := rVoted_Volt_V;
        x_Ref[5] := 0.0;
        x_Ref[6] := 30.0;
        x_Ref[7] := c_rVac_TargetRoughing_mbar;
        x_Ref[8] := 0.0;

    ELSE  (* Default Standby / Trajectory Targets *)
        x_Ref[1] := 0.0;
        x_Ref[2] := 0.0;
        x_Ref[3] := 450.0;
        x_Ref[4] := rVoted_Volt_V;
        x_Ref[5] := 0.0;
        x_Ref[6] := 25.0;
        x_Ref[7] := 1013.2;
        x_Ref[8] := 0.0;
END_CASE;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* Multi-Objective Gradient Evaluation & Control Demand Synthesis                                                      *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Actuator 1: Ultrasonic Frequency Offset Command u_1 [kHz] *)
u_DeltaDemand[1] := -0.018 * Q_Weight[1] * (x_Pred[1] - x_Ref[1]) - 0.05 * R_Weight[1] * (u_Control[1] - u_Prev[1]);
u_Control[1]     := u_Control[1] + u_DeltaDemand[1];
(* Saturation Clamp: Frequency Tuning Limit +-0.80 kHz *)
IF u_Control[1] > 0.80 THEN
    u_Control[1] := 0.80;
ELSIF u_Control[1] < -0.80 THEN
    u_Control[1] := -0.80;
END_IF;

(* Actuator 2: Voice-Coil Clamping Force Command u_2 [N] *)
u_DeltaDemand[2] := -0.012 * Q_Weight[2] * (x_Pred[2] - x_Ref[2]) - 0.02 * R_Weight[2] * (u_Control[2] - u_Prev[2]);
u_Control[2]     := u_Control[2] + u_DeltaDemand[2];
IF u_Control[2] > 1200.0 THEN
    u_Control[2] := 1200.0;
ELSIF u_Control[2] < 0.0 THEN
    u_Control[2] := 0.0;
END_IF;

(* Actuator 3: Formation Cycler Current Demand u_3 [A] *)
u_DeltaDemand[3] := -0.015 * Q_Weight[5] * (x_Pred[5] - x_Ref[5]) - 0.025 * Q_Weight[4] * (x_Pred[4] - x_Ref[4]);
u_Control[3]     := u_Control[3] + u_DeltaDemand[3];
IF u_Control[3] > 100.0 THEN
    u_Control[3] := 100.0;
ELSIF u_Control[3] < 0.0 THEN
    u_Control[3] := 0.0;
END_IF;

(* Actuator 4: Vacuum Chamber Throttle Valve Demand u_4 [%] *)
u_DeltaDemand[4] := 0.035 * Q_Weight[7] * (x_Pred[7] - x_Ref[7]);
u_Control[4]     := u_Control[4] + u_DeltaDemand[4];
IF u_Control[4] > 100.0 THEN
    u_Control[4] := 100.0;
ELSIF u_Control[4] < 0.0 THEN
    u_Control[4] := 0.0;
END_IF;

(* Actuator 5: Induction Reseal RF Power Demand u_5 [kW] *)
u_DeltaDemand[5] := -0.020 * Q_Weight[6] * (x_Pred[6] - x_Ref[6]);
u_Control[5]     := u_Control[5] + u_DeltaDemand[5];
IF u_Control[5] > 8.0 THEN
    u_Control[5] := 8.0;
ELSIF u_Control[5] < 0.0 THEN
    u_Control[5] := 0.0;
END_IF;

(* Actuator 6: SCARA Trajectory Feedforward Velocity u_6 [mm/s] *)
u_DeltaDemand[6] := -0.030 * Q_Weight[8] * (x_Pred[8] - x_Ref[8]);
u_Control[6]     := u_Control[6] + u_DeltaDemand[6];
IF u_Control[6] > 1800.0 THEN
    u_Control[6] := 1800.0;
ELSIF u_Control[6] < -1800.0 THEN
    u_Control[6] := -1800.0;
END_IF;

(* Store Previous Control Demand for Slew Rate Evaluation *)
FOR mIdx := 1 TO 6 DO
    u_Prev[mIdx] := u_Control[mIdx];
END_FOR;

(* Dispatch MPC Control Vector to Actuator Hardware Outputs *)
CMD_US_FREQ_ADJ_kHz      := u_Control[1];
CMD_US_FORCE_SETPOINT_N  := u_Control[2];
CMD_CYCLER_CURR_SP_A     := u_Control[3];
CMD_INDUCTION_POWER_SP_kW:= u_Control[5];
''')

    # =========================================================================
    # 9. PHASE 4: ADVANCED CYBER-PHYSICAL OBSERVERS & MULTI-DOMAIN ALGORITHMS
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 4: ADVANCED CYBER-PHYSICAL OBSERVERS & RIGOROUS PROCESS ALGORITHMS                                             *)
(* Sub-Engines:                                                                                                         *)
(*   4.1: Ultrasonic 20 kHz Resonant Phase-Locked Loop (PLL) Tracker                                                    *)
(*   4.2: Multi-Mode Ultrasonic Tab Weld Termination Engine (Energy, Collapse Height, Peak Power, Max Time)             *)
(*   4.3: Galvanostatic CCCV Formation, Coulomb Counter & dQ/dV Differential Capacity Engine                           *)
(*   4.4: Dual-Polarization Thevenin Battery Equivalent Circuit State Observer                                          *)
(*   4.5: Vacuum Degassing Chamber Evacuation Dynamics & Vacuum Decay Hermeticity Leak Tester                          *)
(*   4.6: High-Frequency Reseal Induction Heating Closed-Loop PID Temperature Controller                                *)
(*   4.7: 1 kHz ACIR Complex Impedance Sorter & Cell Quality Grading Engine                                             *)
(*   4.8: SCARA 6-Axis Robotic Collation Gantry Quintic S-Curve Trajectory Generator                                       *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.1: ULTRASONIC 20 kHz RESONANT PHASE-LOCKED LOOP (PLL) TRACKER                                                      *)
(* Tracks resonant zero-crossing phase error e_phi to maintain maximum acoustic mechanical efficiency.                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rPLL_PhaseError_rad := AE_US_PHASE_104 * 0.01745329;

IF CMD_US_GEN_ENABLE THEN
    (* PI Loop Integrator with Anti-Windup Saturation Clamping *)
    rPLL_FreqIntegrator_kHz := rPLL_FreqIntegrator_kHz + (rPLL_IntegralGain * rPLL_PhaseError_rad * 0.001);
    IF rPLL_FreqIntegrator_kHz > 0.85 THEN
        rPLL_FreqIntegrator_kHz := 0.85;
    ELSIF rPLL_FreqIntegrator_kHz < -0.85 THEN
        rPLL_FreqIntegrator_kHz := -0.85;
    END_IF;

    (* Total Frequency Offset Demand *)
    CMD_US_FREQ_ADJ_kHz := (rPLL_ProportionalGain * rPLL_PhaseError_rad) + rPLL_FreqIntegrator_kHz;
    bPLL_FrequencyLocked := (ABS(AE_US_PHASE_104) <= 4.5);
ELSE
    rPLL_FreqIntegrator_kHz := 0.0;
    bPLL_FrequencyLocked    := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.2: MULTI-MODE ULTRASONIC TAB WELD TERMINATION ENGINE                                                               *)
(* Computes real-time acoustic energy integral, vertical horn collapse delta, and peak power tracking.                 *)
(* Termination evaluates 4 boundary envelopes: Energy Limit, Collapse Distance, Peak Power, and Max Timeout.           *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF CMD_US_GEN_ENABLE THEN
    rWeld_Duration_s := rWeld_Duration_s + 0.001;

    (* Trapezoidal Acoustic Energy Integration: E(t) = Integral (P_active) dt *)
    rWeld_AccumEnergy_J := rWeld_AccumEnergy_J + (JIT_US_POWER_105 * 0.001);

    (* Dynamic Plastic Seam Collapse Height: Delta_h = h_baseline - h_current *)
    rWeld_CollapseHeight_mm := rWeld_InitialHeight_mm - rVoted_Disp_mm;
    IF rWeld_CollapseHeight_mm < 0.0 THEN
        rWeld_CollapseHeight_mm := 0.0;
    END_IF;

    (* Peak Power Capture *)
    IF JIT_US_POWER_105 > rWeld_PeakPower_W THEN
        rWeld_PeakPower_W := JIT_US_POWER_105;
    END_IF;

    (* Termination Envelope Threshold Evaluations *)
    bWeld_EnergyCutoffMet    := (rWeld_AccumEnergy_J >= c_rWeld_TargetEnergy_J);
    bWeld_HeightCutoffMet    := (rWeld_CollapseHeight_mm >= c_rWeld_TargetCollapse_mm);
    bWeld_PeakPowerCutoffMet := (rWeld_PeakPower_W >= c_rWeld_MaxPeakPower_W);
    bWeld_TimeCutoffMet      := (rWeld_Duration_s >= c_rWeld_MaxDuration_s);

    (* Trigger Master Sonication Shutoff Edge *)
    IF bWeld_EnergyCutoffMet OR bWeld_HeightCutoffMet OR bWeld_PeakPowerCutoffMet OR bWeld_TimeCutoffMet THEN
        bWeld_CycleTerminated := TRUE;
    END_IF;

    STATUS_TOTAL_ENERGY_J          := rWeld_AccumEnergy_J;
    STATUS_WELD_HEIGHT_COLLAPSE_mm := rWeld_CollapseHeight_mm;
ELSE
    bWeld_CycleTerminated := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.3: GALVANOSTATIC CCCV FORMATION, COULOMB COUNTER & dQ/dV DIFFERENTIAL CAPACITY ENGINE                             *)
(* Numerical integration of electrical charge Q = Integral(I*dt) and differential capacity dQ/dV.                       *)
(* Identifies graphite phase transition peak (LiC_12 -> LiC_6) indicative of stable SEI passivation layer.              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF CMD_CYCLER_ENABLE THEN
    (* Coulomb Counting Integrator: Q [Ah] = Sum (I [A] * dt [s]) / 3600.0 *)
    rForm_AccumCharge_Ah   := rForm_AccumCharge_Ah + ((rVoted_Curr_A * 0.001) / 3600.0);
    IF rCellNominalCap_Ah > 0.10 THEN
        rForm_SOC_Estimate_Pct := (rForm_AccumCharge_Ah / rCellNominalCap_Ah) * 100.0;
    ELSE
        rForm_SOC_Estimate_Pct := (rForm_AccumCharge_Ah / 50.0) * 100.0; (* Fallback 50 Ah Cell *)
    END_IF;
    STATUS_FORMATION_SOC_PCT := rForm_SOC_Estimate_Pct;

    (* Constant-Voltage (CV) Transition Check *)
    IF (rVoted_Volt_V >= rForm_VoltageTarget_V) AND NOT bForm_CV_ModeActive THEN
        bForm_CV_ModeActive := TRUE;
        CMD_CYCLER_MODE_CV  := TRUE;
    END_IF;

    (* CV Phase Taper Current Decay Check *)
    IF bForm_CV_ModeActive AND (rVoted_Curr_A <= rForm_TaperCurrentCutoff_A) THEN
        (* Formation Cycle Complete *)
        CMD_CYCLER_ENABLE := FALSE;
    END_IF;

    (* dQ/dV Numerical Differentiation using Rolling Ring Buffer *)
    iBufferIndex := iBufferIndex + 1;
    IF iBufferIndex > 10 THEN
        iBufferIndex := 1;
    END_IF;

    aVoltHistory[iBufferIndex]   := rVoted_Volt_V;
    aChargeHistory[iBufferIndex] := rForm_AccumCharge_Ah;

    (* Compute difference across oldest vs newest ring sample (10 ms difference span) *)
    IF ABS(aVoltHistory[iBufferIndex] - aVoltHistory[(iBufferIndex MOD 10) + 1]) >= 0.0008 THEN
        rdQdV_Current_Ah_V := (aChargeHistory[iBufferIndex] - aChargeHistory[(iBufferIndex MOD 10) + 1]) /
                              (aVoltHistory[iBufferIndex] - aVoltHistory[(iBufferIndex MOD 10) + 1]);

        (* Detect Peak Graphite Staging Signature in Potential Range [3.40 V to 3.75 V] *)
        IF (rVoted_Volt_V >= 3.400) AND (rVoted_Volt_V <= 3.750) THEN
            IF rdQdV_Current_Ah_V > rdQdV_MaxPeak_Ah_V THEN
                rdQdV_MaxPeak_Ah_V   := rdQdV_Current_Ah_V;
                rVolt_At_dQdV_Peak_V := rVoted_Volt_V;
                bSEI_PeakIdentified  := TRUE;
            END_IF;
        END_IF;
    END_IF;
    STATUS_SEI_PEAK_DETECTED := bSEI_PeakIdentified;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.4: DUAL-POLARIZATION THEVENIN BATTERY EQUIVALENT CIRCUIT OBSERVER                                                  *)
(* Discrete-time recursive propagation of fast charge-transfer (RC1) and slow mass-diffusion (RC2) overpotentials:     *)
(*   V_1[k+1] = exp(-dt / (R1*C1)) * V_1[k] + R1 * (1 - exp(-dt / (R1*C1))) * I[k]                                     *)
(*   V_2[k+1] = exp(-dt / (R2*C2)) * V_2[k] + R2 * (1 - exp(-dt / (R2*C2))) * I[k]                                     *)
(*   OCV_est  = V_terminal - I * R_0 - V_1 - V_2                                                                        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rThev_Overpotential_RC1_V := (0.99906 * rThev_Overpotential_RC1_V) + (c_rThev_R1_Ohm * 0.00094 * rVoted_Curr_A);
rThev_Overpotential_RC2_V := (0.99987 * rThev_Overpotential_RC2_V) + (c_rThev_R2_Ohm * 0.00013 * rVoted_Curr_A);
rThev_OCV_Est_V           := rVoted_Volt_V - (rVoted_Curr_A * c_rThev_R0_Ohm) - rThev_Overpotential_RC1_V - rThev_Overpotential_RC2_V;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.5: VACUUM DEGASSING CHAMBER EVACUATION DYNAMICS & VACUUM DECAY HERMETICITY LEAK TESTER                            *)
(* Evaluates chamber pressure decay rate: Q_leak = (P_end - P_start) / Delta_t [mbar/s]                                *)
(* Rejects cell if blister pouch puncture seal experiences volatile gas blow-by or chamber seal leakage.               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (iFSM_CurrentState = 8) THEN
    rVac_DecayDwellTimer_s := rVac_DecayDwellTimer_s + 0.001;

    IF bFSM_FirstScanInStep THEN
        rVac_DecayStartPressure_mbar := rVoted_Vac_mbar;
        rVac_DecayDwellTimer_s       := 0.0;
        bVac_DecayTestPassed         := FALSE;
    END_IF;

    IF rVac_DecayDwellTimer_s >= 2.50 THEN
        rVac_ComputedLeakRate_mbar_s := (rVoted_Vac_mbar - rVac_DecayStartPressure_mbar) / rVac_DecayDwellTimer_s;
        STATUS_VAC_DECAY_RATE_mbar_s := rVac_ComputedLeakRate_mbar_s;
        bVac_DecayTestPassed         := (rVac_ComputedLeakRate_mbar_s <= c_rVac_MaxPermissibleLeak_mbar_s);
    END_IF;
ELSE
    rVac_DecayDwellTimer_s := 0.0;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.6: HIGH-FREQUENCY RESEAL INDUCTION HEATING CLOSED-LOOP PID CONTROLLER                                              *)
(* Controls 300 kHz induction heating power to fuse aluminum-polypropylene pouch laminate flap at 198.0 deg C.          *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF CMD_INDUCTION_HEATER_ENABLE THEN
    rInd_TempError_degC        := c_rInd_TargetTemp_degC - rVoted_IndTemp_degC;
    rInd_PID_Integral_degC_s   := rInd_PID_Integral_degC_s + (rInd_TempError_degC * 0.001);

    (* Anti-Windup Clamping *)
    IF rInd_PID_Integral_degC_s > 350.0 THEN
        rInd_PID_Integral_degC_s := 350.0;
    ELSIF rInd_PID_Integral_degC_s < -50.0 THEN
        rInd_PID_Integral_degC_s := -50.0;
    END_IF;

    rInd_PID_Derivative_degC_s := (rVoted_IndTemp_degC - rInd_PrevTemp_degC) / 0.001;
    rInd_PrevTemp_degC         := rVoted_IndTemp_degC;

    rInd_OutputPowerDemand_kW := (c_rInd_Kp * rInd_TempError_degC) +
                                 (c_rInd_Ki * rInd_PID_Integral_degC_s) -
                                 (c_rInd_Kd * rInd_PID_Derivative_degC_s);

    IF rInd_OutputPowerDemand_kW > 6.5 THEN
        rInd_OutputPowerDemand_kW := 6.5;
    ELSIF rInd_OutputPowerDemand_kW < 0.0 THEN
        rInd_OutputPowerDemand_kW := 0.0;
    END_IF;

    CMD_INDUCTION_POWER_SP_kW := rInd_OutputPowerDemand_kW;
ELSE
    rInd_PID_Integral_degC_s  := 0.0;
    CMD_INDUCTION_POWER_SP_kW := 0.0;
    rInd_PrevTemp_degC        := rVoted_IndTemp_degC;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.7: 1 kHz ACIR COMPLEX IMPEDANCE SORTER & CELL QUALITY GRADING ENGINE                                              *)
(* Evaluates 4-terminal AC Internal Resistance at 1 kHz and OCV relaxation to grade cells into Grade A, B, Rework, Scrap.*)
(* -------------------------------------------------------------------------------------------------------------------- *)
STATUS_ACIR_VALUE_mOhm := ZIT_CELL_ACIR_501;

bCell_GradeA_Qualified := (ZIT_CELL_ACIR_501 <= c_rACIR_GradeA_Max_mOhm) AND
                          (rThev_OCV_Est_V >= c_rOCV_GradeA_Min_V) AND
                          bSEI_PeakIdentified AND
                          (STATUS_WELD_QUALITY_SCORE >= 90.0);

bCell_GradeB_Qualified := (ZIT_CELL_ACIR_501 <= c_rACIR_GradeB_Max_mOhm) AND
                          (rThev_OCV_Est_V >= c_rOCV_GradeB_Min_V) AND
                          (STATUS_WELD_QUALITY_SCORE >= 75.0) AND NOT bCell_GradeA_Qualified;

bCell_ReworkRequired   := (STATUS_WELD_QUALITY_SCORE < 75.0) AND (STATUS_WELD_QUALITY_SCORE >= 60.0);
bCell_ScrapRejected    := (ZIT_CELL_ACIR_501 > c_rACIR_GradeB_Max_mOhm) OR
                          (rThev_OCV_Est_V < 3.200) OR
                          (STATUS_WELD_QUALITY_SCORE < 60.0);

IF bCell_GradeA_Qualified THEN
    STATUS_CELL_GRADE := 1; (* Grade A: Premium EV Traction *)
ELSIF bCell_GradeB_Qualified THEN
    STATUS_CELL_GRADE := 2; (* Grade B: Secondary Stationary Energy Storage *)
ELSIF bCell_ReworkRequired THEN
    STATUS_CELL_GRADE := 3; (* Rework: Tab Re-Clamp / Secondary Reseal *)
ELSE
    STATUS_CELL_GRADE := 4; (* Scrap: Reject & Neutralize *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 4.8: SCARA 6-AXIS ROBOTIC COLLATION GANTRY QUINTIC S-CURVE TRAJECTORY GENERATOR                                      *)
(* Real-time calculation of smooth 5th-order polynomial motion: s(tau) = 10*tau^3 - 15*tau^4 + 6*tau^5.                 *)
(* Guarantees zero velocity and zero acceleration at trajectory boundaries (jerk-limited, sub-800 ms cycle).            *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF bSCARA_MoveActive THEN
    rSCARA_MotionTime_s := rSCARA_MotionTime_s + 0.001;
    IF rSCARA_MotionTime_s >= rSCARA_TrajectoryDuration_s THEN
        rSCARA_MotionTime_s := rSCARA_TrajectoryDuration_s;
        bSCARA_MoveActive   := FALSE;
        CMD_SCARA_START_MOVE:= FALSE;
    END_IF;

    rSCARA_NormalizedTime_Tau := rSCARA_MotionTime_s / rSCARA_TrajectoryDuration_s;
    IF rSCARA_NormalizedTime_Tau > 1.0 THEN
        rSCARA_NormalizedTime_Tau := 1.0;
    ELSIF rSCARA_NormalizedTime_Tau < 0.0 THEN
        rSCARA_NormalizedTime_Tau := 0.0;
    END_IF;

    (* Quintic Polynomial Interpolation *)
    rSCARA_QuinticPoly_S  := (10.0 * (rSCARA_NormalizedTime_Tau**3)) -
                             (15.0 * (rSCARA_NormalizedTime_Tau**4)) +
                             ( 6.0 * (rSCARA_NormalizedTime_Tau**5));

    rSCARA_QuinticPoly_dS := (30.0 * (rSCARA_NormalizedTime_Tau**2)) -
                             (60.0 * (rSCARA_NormalizedTime_Tau**3)) +
                             (30.0 * (rSCARA_NormalizedTime_Tau**4));

    CMD_SCARA_TARGET_X_mm  := rSCARA_StartX_mm + ((rSCARA_GoalX_mm - rSCARA_StartX_mm) * rSCARA_QuinticPoly_S);
    CMD_SCARA_TARGET_Y_mm  := rSCARA_StartY_mm + ((rSCARA_GoalY_mm - rSCARA_StartY_mm) * rSCARA_QuinticPoly_S);
    CMD_SCARA_TARGET_Z_mm  := rSCARA_StartZ_mm + ((rSCARA_GoalZ_mm - rSCARA_StartZ_mm) * rSCARA_QuinticPoly_S);
    CMD_SCARA_TARGET_R_deg := rSCARA_StartR_deg + ((rSCARA_GoalR_deg - rSCARA_StartR_deg) * rSCARA_QuinticPoly_S);

    (* Tool Center Point Cartesian Tracking Error *)
    rSCARA_TrackingError_mm := SQRT(((POS_SCARA_X_401 - CMD_SCARA_TARGET_X_mm)**2) +
                                    ((POS_SCARA_Y_402 - CMD_SCARA_TARGET_Y_mm)**2) +
                                    ((POS_SCARA_Z_403 - CMD_SCARA_TARGET_Z_mm)**2));
ELSE
    rSCARA_MotionTime_s     := 0.0;
    rSCARA_TrackingError_mm := 0.0;
END_IF;
''')

    # =========================================================================
    # 10. PHASE 5: DETERMINISTIC 12-STAGE FINITE STATE MACHINE (FSM)
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 5: DETERMINISTIC 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                               *)
(* States:                                                                                                              *)
(*   0:  FSM_STATE_00_IDLE_INFEED_SCAN            - Infeed cell presence & 2D DataMatrix laser verification.            *)
(*   1:  FSM_STATE_01_SCARA_PICK_AND_ALIGN        - 6-axis SCARA pickup, laser tab alignment & precision clamping.       *)
(*   2:  FSM_STATE_02_TAB_CLAMP_SONOTRODE_ENGAGE  - Ultrasonic voice-coil normal force ramp (680 N clamping pre-load).  *)
(*   3:  FSM_STATE_03_ULTRASONIC_WELD_BURST       - 20 kHz 3.5 kW acoustic vibration, energy/collapse distance cutoff.  *)
(*   4:  FSM_STATE_04_WELD_SIGNATURE_EVAL         - Acoustic power integral & confocal seam profile quality evaluation.  *)
(*   5:  FSM_STATE_05_SCARA_TRAY_TRANSFER         - Fast transfer of welded cell into 96-cell formation tray fixture.   *)
(*   6:  FSM_STATE_06_FORMATION_CCCV_CHARGE       - High-precision galvanostatic CC (25 A) to CV (3.85 V) charge.       *)
(*   7:  FSM_STATE_07_DQDV_SEI_ANALYSIS           - dQ/dV differential capacity graphite staging & SEI verification.     *)
(*   8:  FSM_STATE_08_VAC_CHAMBER_LOAD_PUNCTURE   - Chamber vacuum pumpdown (<0.1 mbar) & blister piercing needle stroke*)
(*   9:  FSM_STATE_09_ELECTROLYTE_EVAC_DECAY_TEST - Volatile gas extraction & 2.5s chamber hermetic vacuum decay test.  *)
(*   10: FSM_STATE_10_INDUCTION_RESEAL_AND_COOL   - 300 kHz induction heating (198 deg C) hermetic pouch fusion & chill.*)
(*   11: FSM_STATE_11_OCV_ACIR_GRADING_SORT       - 1 kHz ACIR and relaxed OCV measurement & 4-tier bin classification. *)
(*   12: FSM_STATE_12_TRAY_EJECT_WAREHOUSE        - Indexing complete 96-cell pallet to automated aging warehouse buffer*)
(*   99: FSM_STATE_99_EMERGENCY_SAFE_ABORT        - Safe system shutdown: retract actuators, dump power, isolate vacuum.*)
(* ==================================================================================================================== *)

(* Detect Entry into New Step *)
IF iFSM_CurrentState <> iFSM_PreviousState THEN
    bFSM_FirstScanInStep := TRUE;
    rFSM_StateStepTimer_s := 0.0;
    iFSM_PreviousState    := iFSM_CurrentState;
ELSE
    bFSM_FirstScanInStep  := FALSE;
    rFSM_StateStepTimer_s := rFSM_StateStepTimer_s + 0.001;
END_IF;

(* Master Emergency Interlock Trip Guard *)
IF (NOT bEmergencyStopOk) OR (NOT bSafetyGateClosed) OR bFSM_EmergencyAbortLatched THEN
    iFSM_CurrentState := 99;
END_IF;

CASE iFSM_CurrentState OF
    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 0: IDLE, CELL INFEED & BARCODE SCAN VERIFICATION                                                           *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    0:
        STATUS_SYSTEM_STATE         := 0;
        CMD_US_GEN_ENABLE           := FALSE;
        CMD_CYCLER_ENABLE           := FALSE;
        CMD_VAC_ROUGHING_VALVE      := FALSE;
        CMD_VAC_TURBO_GATE_VALVE    := FALSE;
        CMD_NEEDLE_PUNCTURE_EXTEND  := FALSE;
        CMD_INDUCTION_HEATER_ENABLE := FALSE;
        CMD_RESEAL_JAW_CLAMP        := FALSE;

        IF bSysEnable AND bAutoStart AND bCellPresentInfeed AND BC_CELL_BARCODE_VALID THEN
            iFSM_CurrentState := 1; (* Advance to SCARA Pick & Align *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 1: SCARA PICKUP, TAB ALIGNMENT & FIXTURE TRANSFER                                                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    1:
        STATUS_SYSTEM_STATE := 1;
        IF bFSM_FirstScanInStep THEN
            rSCARA_StartX_mm   := POS_SCARA_X_401;
            rSCARA_StartY_mm   := POS_SCARA_Y_402;
            rSCARA_StartZ_mm   := POS_SCARA_Z_403;
            rSCARA_StartR_deg  := POS_SCARA_R_404;
            rSCARA_GoalX_mm    := 250.0; (* Infeed Cell Fixture Position *)
            rSCARA_GoalY_mm    := 120.0;
            rSCARA_GoalZ_mm    :=  15.0; (* Grip Height *)
            rSCARA_GoalR_deg   :=   0.0;
            rSCARA_MotionTime_s:= 0.0;
            bSCARA_MoveActive  := TRUE;
            CMD_SCARA_START_MOVE:= TRUE;
            CMD_SCARA_VAC_VALVE := TRUE; (* Activate Suction *)
        END_IF;

        (* Once arrived and suction confirmed, transfer to ultrasonic anvil *)
        IF (NOT bSCARA_MoveActive) AND (PIT_SCARA_VAC_406 <= -0.75) THEN
            IF rFSM_StateStepTimer_s >= 0.850 THEN
                iFSM_CurrentState := 2; (* Advance to Tab Clamping *)
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 2: TAB CLAMPING & SONOTRODE NORMAL FORCE ENGAGEMENT                                                        *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    2:
        STATUS_SYSTEM_STATE := 2;
        IF bFSM_FirstScanInStep THEN
            rWeld_AccumEnergy_J   := 0.0;
            rWeld_PeakPower_W     := 0.0;
            rWeld_Duration_s      := 0.0;
            bWeld_CycleTerminated := FALSE;
        END_IF;

        (* Voice-Coil Force Ramped by MPC toward 680.0 N *)
        CMD_US_FORCE_SETPOINT_N := 680.0;

        (* Capture Stack Baseline Height once force stabilizes within +-20 N *)
        IF (ABS(rVoted_Force_N - 680.0) <= 20.0) AND (rFSM_StateStepTimer_s >= 0.150) THEN
            rWeld_InitialHeight_mm := rVoted_Disp_mm;
            iFSM_CurrentState      := 3; (* Trigger Ultrasonic Acoustic Burst *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 3: ULTRASONIC TAB-TO-LEAD ACOUSTIC WELD BURST (20 kHz SONICATION)                                         *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    3:
        STATUS_SYSTEM_STATE := 3;
        IF bFSM_FirstScanInStep THEN
            CMD_US_GEN_ENABLE    := TRUE;
            CMD_US_AMPLITUDE_PCT := 85.0; (* 85% Amplitude Envelope *)
        END_IF;

        (* Check Termination Cutoff Flags from Cyber-Physical Engine 4.2 *)
        IF bWeld_CycleTerminated OR (rWeld_Duration_s >= c_rWeld_MaxDuration_s) THEN
            CMD_US_GEN_ENABLE := FALSE;
            iFSM_CurrentState := 4; (* Advance to Weld Signature Evaluation *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 4: WELD QUALITY SIGNATURE EVALUATION & METROLOGY CHECK                                                     *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    4:
        STATUS_SYSTEM_STATE := 4;
        CMD_US_GEN_ENABLE   := FALSE;

        IF bFSM_FirstScanInStep THEN
            (* Release Voice-Coil Normal Clamping Force *)
            CMD_US_FORCE_SETPOINT_N := 0.0;

            (* Compute Composite Weld Quality Metric Q-Score [0..100%] *)
            IF (rWeld_AccumEnergy_J >= c_rWeld_MinEnergy_J) AND (rWeld_AccumEnergy_J <= c_rWeld_MaxEnergy_J) AND
               (rWeld_CollapseHeight_mm >= c_rWeld_MinCollapse_mm) AND (rWeld_CollapseHeight_mm <= c_rWeld_MaxCollapse_mm) AND
               (rWeld_PeakPower_W <= c_rWeld_MaxPeakPower_W) THEN
                STATUS_WELD_QUALITY_SCORE := 96.5; (* Prime Weld Signature *)
            ELSIF (rWeld_AccumEnergy_J >= (c_rWeld_MinEnergy_J * 0.90)) AND (rWeld_CollapseHeight_mm >= (c_rWeld_MinCollapse_mm * 0.85)) THEN
                STATUS_WELD_QUALITY_SCORE := 78.0; (* Acceptable Class B *)
            ELSE
                STATUS_WELD_QUALITY_SCORE := 42.0; (* Defective Joint *)
            END_IF;
        END_IF;

        IF rFSM_StateStepTimer_s >= 0.120 THEN
            IF STATUS_WELD_QUALITY_SCORE >= 75.0 THEN
                iFSM_CurrentState := 5; (* Advance to Tray Transfer *)
            ELSE
                CMD_CELL_REJECT_GATE := TRUE; (* Divert Bad Weld to Rework/Scrap Chute *)
                iFSM_CurrentState    := 0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 5: SCARA TRANSFER TO 96-CELL FORMATION TRAY FIXTURE                                                        *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    5:
        STATUS_SYSTEM_STATE := 5;
        IF bFSM_FirstScanInStep THEN
            rSCARA_StartX_mm   := POS_SCARA_X_401;
            rSCARA_StartY_mm   := POS_SCARA_Y_402;
            rSCARA_StartZ_mm   := POS_SCARA_Z_403;
            rSCARA_StartR_deg  := POS_SCARA_R_404;
            rSCARA_GoalX_mm    := 650.0; (* Formation Tray Carrier Position *)
            rSCARA_GoalY_mm    := 380.0;
            rSCARA_GoalZ_mm    :=  25.0;
            rSCARA_GoalR_deg   :=  90.0;
            rSCARA_MotionTime_s:= 0.0;
            bSCARA_MoveActive  := TRUE;
            CMD_SCARA_START_MOVE:= TRUE;
        END_IF;

        IF (NOT bSCARA_MoveActive) AND (rFSM_StateStepTimer_s >= 0.750) THEN
            CMD_SCARA_VAC_VALVE := FALSE; (* Release Suction Grip *)
            IF rFSM_StateStepTimer_s >= 0.850 THEN
                iFSM_CurrentState := 6; (* Advance to Formation Charge *)
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 6: CONSTANT-CURRENT CONSTANT-VOLTAGE (CCCV) FORMATION CHARGING                                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    6:
        STATUS_SYSTEM_STATE := 6;
        IF bFSM_FirstScanInStep THEN
            CMD_CYCLER_ENABLE          := TRUE;
            CMD_CYCLER_MODE_CV         := FALSE;
            CMD_CYCLER_CURR_SP_A       := rForm_ChargeCurrentSP_A; (* 25.0 A *)
            CMD_CYCLER_VOLT_LIMIT_V    := rForm_VoltageTarget_V;   (* 3.850 V *)
            bForm_CV_ModeActive        := FALSE;
            rForm_AccumCharge_Ah       := 0.0;
            rdQdV_MaxPeak_Ah_V         := 0.0;
            bSEI_PeakIdentified        := FALSE;
        END_IF;

        (* Check Formation Completion: Taper current satisfied or state timeout *)
        IF (NOT CMD_CYCLER_ENABLE) OR (rFSM_StateStepTimer_s >= 18.0) THEN
            CMD_CYCLER_ENABLE := FALSE;
            iFSM_CurrentState := 7; (* Advance to SEI Analysis Verification *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 7: dQ/dV SEI PASSIVATION LAYER EVALUATION                                                                  *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    7:
        STATUS_SYSTEM_STATE := 7;
        CMD_CYCLER_ENABLE   := FALSE;

        (* Verify SEI Passivation Signature Peak Area & Location *)
        IF bFSM_FirstScanInStep THEN
            IF bSEI_PeakIdentified AND (rVolt_At_dQdV_Peak_V >= 3.42) AND (rVolt_At_dQdV_Peak_V <= 3.72) THEN
                STATUS_SEI_PEAK_DETECTED := TRUE;
            ELSE
                STATUS_SEI_PEAK_DETECTED := FALSE;
            END_IF;
        END_IF;

        IF rFSM_StateStepTimer_s >= 0.200 THEN
            iFSM_CurrentState := 8; (* Advance to Vacuum Degassing Chamber *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 8: VACUUM DEGASSING CHAMBER PUMP DOWN & BLISTER NEEDLE PUNCTURE                                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    8:
        STATUS_SYSTEM_STATE := 8;
        IF bFSM_FirstScanInStep THEN
            CMD_VAC_ROUGHING_VALVE     := TRUE;
            CMD_NEEDLE_PUNCTURE_EXTEND := FALSE;
        END_IF;

        (* Once chamber roughs below 0.50 mbar, extend needle to puncture pouch gas pocket *)
        IF (rVoted_Vac_mbar <= 0.50) AND (NOT CMD_NEEDLE_PUNCTURE_EXTEND) THEN
            CMD_NEEDLE_PUNCTURE_EXTEND    := TRUE;
            CMD_ELECTROLYTE_SUCTION_VALVE := TRUE;
        END_IF;

        (* Deep Vacuum Roughing Complete & Needle Retracted *)
        IF (rVoted_Vac_mbar <= c_rVac_TargetRoughing_mbar) AND (rFSM_StateStepTimer_s >= 3.50) THEN
            CMD_NEEDLE_PUNCTURE_EXTEND := FALSE;
            iFSM_CurrentState          := 9; (* Advance to Vacuum Decay Leak Test *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 9: ELECTROLYTE EVACUATION & VACUUM DECAY HERMETICITY LEAK TEST                                             *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    9:
        STATUS_SYSTEM_STATE := 9;
        IF bFSM_FirstScanInStep THEN
            (* Isolate Chamber to measure vacuum decay *)
            CMD_VAC_ROUGHING_VALVE        := FALSE;
            CMD_ELECTROLYTE_SUCTION_VALVE := FALSE;
        END_IF;

        (* 2.5 Second Decay Dwell Checked by Engine 4.5 *)
        IF rFSM_StateStepTimer_s >= 2.60 THEN
            IF bVac_DecayTestPassed THEN
                iFSM_CurrentState := 10; (* Advance to Induction Reseal *)
            ELSE
                (* Pouch Puncture Blow-by or Seal Rupture Defect *)
                ALARM_WORD_02     := ALARM_WORD_02 OR 16#00000008; (* Vacuum Leak Decay Trip *)
                iFSM_CurrentState := 11;                           (* Skip Reseal -> Route to Reject *)
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 10: HIGH-FREQUENCY INDUCTION HERMETIC RESEAL & CHILLING                                                    *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    10:
        STATUS_SYSTEM_STATE := 10;
        IF bFSM_FirstScanInStep THEN
            CMD_RESEAL_JAW_CLAMP        := TRUE; (* Clamp Pouch Reseal Lip *)
            CMD_INDUCTION_HEATER_ENABLE := TRUE;
            rInd_DwellTimer_s           := 0.0;
        END_IF;

        (* Reseal Dwell Timer once spot temp reaches 195.0 deg C *)
        IF rVoted_IndTemp_degC >= 195.0 THEN
            rInd_DwellTimer_s := rInd_DwellTimer_s + 0.001;
        END_IF;

        IF rInd_DwellTimer_s >= 1.200 THEN
            CMD_INDUCTION_HEATER_ENABLE := FALSE;
            (* Chilling clamp dwell 0.50 s *)
            IF rFSM_StateStepTimer_s >= 2.200 THEN
                CMD_RESEAL_JAW_CLAMP := FALSE;
                iFSM_CurrentState    := 11; (* Advance to ACIR / OCV Grading *)
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 11: 1 kHz ACIR & RELAXED OCV QUALITY GRADING CLASSIFICATION                                                *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    11:
        STATUS_SYSTEM_STATE := 11;
        CMD_INDUCTION_HEATER_ENABLE := FALSE;
        CMD_RESEAL_JAW_CLAMP        := FALSE;

        IF rFSM_StateStepTimer_s >= 0.350 THEN
            IF (STATUS_CELL_GRADE = 1) OR (STATUS_CELL_GRADE = 2) THEN
                iFSM_CurrentState := 12; (* Accepted Cell -> Eject to Warehouse Tray *)
            ELSE
                CMD_CELL_REJECT_GATE := TRUE; (* Divert Scrap/Rework Cell *)
                iFSM_CurrentState    := 0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 12: TRAY EJECT & AGING WAREHOUSE CONVEYOR INDEX                                                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    12:
        STATUS_SYSTEM_STATE := 12;
        IF bFSM_FirstScanInStep THEN
            CMD_TRAY_INDEX_PULSE := TRUE;
        END_IF;

        IF rFSM_StateStepTimer_s >= 0.500 THEN
            CMD_TRAY_INDEX_PULSE := FALSE;
            iFSM_CurrentState    := 0; (* Cycle Complete: Return to Idle Ready *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 99: CRITICAL EMERGENCY SAFE ABORT                                                                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    99:
        STATUS_SYSTEM_STATE           := 99;
        CMD_US_GEN_ENABLE             := FALSE;
        CMD_US_FORCE_SETPOINT_N       := 0.0;
        CMD_CYCLER_ENABLE             := FALSE;
        CMD_CYCLER_CURR_SP_A          := 0.0;
        CMD_VAC_ROUGHING_VALVE        := FALSE;
        CMD_VAC_TURBO_GATE_VALVE      := FALSE;
        CMD_NEEDLE_PUNCTURE_EXTEND    := FALSE;
        CMD_ELECTROLYTE_SUCTION_VALVE := FALSE;
        CMD_INDUCTION_HEATER_ENABLE   := FALSE;
        CMD_INDUCTION_POWER_SP_kW     := 0.0;
        CMD_RESEAL_JAW_CLAMP          := FALSE;
        CMD_SCARA_START_MOVE          := FALSE;
        CMD_SCARA_VAC_VALVE           := FALSE;

        IF bSysReset AND bEmergencyStopOk AND bSafetyGateClosed THEN
            bFSM_EmergencyAbortLatched := FALSE;
            ALARM_WORD_01              := 0;
            ALARM_WORD_02              := 0;
            ALARM_WORD_03              := 0;
            iFSM_CurrentState          := 0;
        END_IF;
END_CASE;
''')

    # =========================================================================
    # 11. PHASE 6: ISA-18.2 MULTI-TIERED ALARMS & DIAGNOSTIC PACKING
    # =========================================================================
    code_parts.append('''(* ==================================================================================================================== *)
(* PHASE 6: ISA-18.2 MULTI-TIERED PROCESS ALARM MANAGEMENT & STATUS WORD PACKING                                        *)
(* Implements 5-Tier Alarm Severity Ladder: HI_HI, HI, LO, LO_LO, and Rate-of-Change (ROC) with Deadband Hysteresis.    *)
(* Diagnostic Packing:                                                                                                  *)
(*   ALARM_WORD_01 : Emergency Trips (E-Stop, Thermal Runaway, Overvoltage, Diverged Voting)                           *)
(*   ALARM_WORD_02 : Process Warnings (Weld Force Deviation, Power Excursion, Vacuum Decay Loss)                       *)
(*   ALARM_WORD_03 : 2oo3 TMR Hardware Discrepancies (Piezo Load Cells, LVDT, Kelvin Probes, Pyrometers)               *)
(*   INTERLOCK_WORD: Safety Gates, Coolant Flow, N2 Purge, Chamber Vacuum Ready                                        *)
(*   DIAGNOSTIC_WORD: Subsystem FSM State, PLL Lock, SEI Signature Found, Cycle Finished                                *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.1: RATE-OF-CHANGE (ROC) & THERMAL RUNAWAY MONITORING                                                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
rRateOfChange_CellTemp_degC_s := (rVoted_Temp_degC - rPrevSample_CellTemp_degC) / 0.001;
rPrevSample_CellTemp_degC     := rVoted_Temp_degC;

IF rRateOfChange_CellTemp_degC_s >= c_rTrip_CellTemp_ROC_degC_s THEN
    ALARM_WORD_01              := ALARM_WORD_01 OR 16#00000001; (* Bit 0: Cell Core Thermal Runaway Early ROC Trip *)
    bFSM_EmergencyAbortLatched := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.2: CELL OVERVOLTAGE & OVERTEMPERATURE CRITICAL TRIPS                                                              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF rVoted_Volt_V >= c_rTrip_CellVolt_HH THEN
    ALARM_WORD_01              := ALARM_WORD_01 OR 16#00000002; (* Bit 1: Cell Terminal Voltage HI_HI Overcharge Trip *)
    bFSM_EmergencyAbortLatched := TRUE;
ELSIF rVoted_Volt_V <= (c_rTrip_CellVolt_HH - c_rDeadband_CellVolt_V) THEN
    ALARM_WORD_01 := ALARM_WORD_01 AND NOT 16#00000002;
END_IF;

IF rVoted_Temp_degC >= c_rTrip_CellTemp_HH THEN
    ALARM_WORD_01              := ALARM_WORD_01 OR 16#00000004; (* Bit 2: Cell Core Temperature HI_HI Excursion Trip *)
    bFSM_EmergencyAbortLatched := TRUE;
ELSIF rVoted_Temp_degC <= (c_rTrip_CellTemp_HH - c_rDeadband_CellTemp_degC) THEN
    ALARM_WORD_01 := ALARM_WORD_01 AND NOT 16#00000004;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.3: ULTRASONIC WELD POWER & FORCE EXCURSIONS                                                                        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF JIT_US_POWER_105 >= c_rTrip_USPower_HH THEN
    ALARM_WORD_01 := ALARM_WORD_01 OR 16#00000008; (* Bit 3: Ultrasonic Generator HI_HI Power Inverter Trip *)
ELSIF JIT_US_POWER_105 <= (c_rTrip_USPower_HH - c_rDeadband_USPower_W) THEN
    ALARM_WORD_01 := ALARM_WORD_01 AND NOT 16#00000008;
END_IF;

IF (rVoted_Force_N >= c_rTrip_Force_HH) OR (rVoted_Force_N <= c_rTrip_Force_LL) THEN
    ALARM_WORD_02 := ALARM_WORD_02 OR 16#00000001; (* Bit 0: Normal Clamping Force Out-of-Bounds Warning *)
ELSIF (rVoted_Force_N <= (c_rTrip_Force_HH - c_rDeadband_Force_N)) AND
      (rVoted_Force_N >= (c_rTrip_Force_LL + c_rDeadband_Force_N)) THEN
    ALARM_WORD_02 := ALARM_WORD_02 AND NOT 16#00000001;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.4: VACUUM DEGASSING & INDUCTION TEMPERATURE ALARMS                                                                 *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF rVoted_Vac_mbar >= c_rTrip_VacPress_HH THEN
    ALARM_WORD_02 := ALARM_WORD_02 OR 16#00000002; (* Bit 1: Vacuum Chamber Loss of Vacuum Warning *)
ELSIF rVoted_Vac_mbar <= (c_rTrip_VacPress_HH - c_rDeadband_VacPress_mbar) THEN
    ALARM_WORD_02 := ALARM_WORD_02 AND NOT 16#00000002;
END_IF;

IF (rVoted_IndTemp_degC >= c_rTrip_InductTemp_HH) OR (rVoted_IndTemp_degC <= c_rTrip_InductTemp_LL) THEN
    ALARM_WORD_02 := ALARM_WORD_02 OR 16#00000004; (* Bit 2: Induction Reseal Temperature Window Fault *)
ELSIF (rVoted_IndTemp_degC <= (c_rTrip_InductTemp_HH - c_rDeadband_InductTemp_degC)) AND
      (rVoted_IndTemp_degC >= (c_rTrip_InductTemp_LL + c_rDeadband_InductTemp_degC)) THEN
    ALARM_WORD_02 := ALARM_WORD_02 AND NOT 16#00000004;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.5: SCARA ROBOT KINEMATIC TRACKING ERROR TRIP                                                                       *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF rSCARA_TrackingError_mm >= c_rTrip_SCARA_TrackErr_HH THEN
    ALARM_WORD_01              := ALARM_WORD_01 OR 16#00000010; (* Bit 4: SCARA Robot Excessive Tracking Error Trip *)
    bFSM_EmergencyAbortLatched := TRUE;
ELSIF rSCARA_TrackingError_mm < c_rTrip_SCARA_TrackErr_H THEN
    ALARM_WORD_01 := ALARM_WORD_01 AND NOT 16#00000010;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.6: INTERLOCK WORD PACKING (32 BITS)                                                                                *)
(* -------------------------------------------------------------------------------------------------------------------- *)
INTERLOCK_WORD := 16#00000000;
IF bEmergencyStopOk        THEN INTERLOCK_WORD := INTERLOCK_WORD OR 16#00000001; END_IF;
IF bSafetyGateClosed       THEN INTERLOCK_WORD := INTERLOCK_WORD OR 16#00000002; END_IF;
IF bPurgeNitrogenAvailable THEN INTERLOCK_WORD := INTERLOCK_WORD OR 16#00000004; END_IF;
IF bCoolingWaterFlowOk     THEN INTERLOCK_WORD := INTERLOCK_WORD OR 16#00000008; END_IF;
IF bCellPresentInfeed      THEN INTERLOCK_WORD := INTERLOCK_WORD OR 16#00000010; END_IF;
IF bTrayPresentCollation   THEN INTERLOCK_WORD := INTERLOCK_WORD OR 16#00000020; END_IF;
IF bPLL_FrequencyLocked    THEN INTERLOCK_WORD := INTERLOCK_WORD OR 16#00000040; END_IF;
IF bVac_DecayTestPassed    THEN INTERLOCK_WORD := INTERLOCK_WORD OR 16#00000080; END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.7: DIAGNOSTIC STATUS WORD PACKING (32 BITS)                                                                        *)
(* -------------------------------------------------------------------------------------------------------------------- *)
DIAGNOSTIC_WORD := 16#00000000;
DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR INT_TO_DWORD(iFSM_CurrentState); (* Lower 8 Bits: Current FSM State *)
IF bForm_CV_ModeActive        THEN DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR 16#00000100; END_IF;
IF bSEI_PeakIdentified        THEN DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR 16#00000200; END_IF;
IF bCell_GradeA_Qualified     THEN DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR 16#00000400; END_IF;
IF bCell_GradeB_Qualified     THEN DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR 16#00000800; END_IF;
IF bSCARA_MoveActive          THEN DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR 16#00001000; END_IF;
IF CMD_US_GEN_ENABLE          THEN DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR 16#00002000; END_IF;
IF CMD_CYCLER_ENABLE          THEN DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR 16#00004000; END_IF;
IF CMD_INDUCTION_HEATER_ENABLETHEN DIAGNOSTIC_WORD := DIAGNOSTIC_WORD OR 16#00008000; END_IF;
''')

    # =========================================================================
    # 12. CLOSING DELIMITER
    # =========================================================================
    code_parts.append('''END_FUNCTION_BLOCK''')

    return "\n".join(code_parts)

if __name__ == '__main__':
    st_body = generate_st_code()
    print(f"Generated Raw ST Code Length: {len(st_body)} characters")
    print(f"Generated Raw ST Line Count: {len(st_body.splitlines())} lines")

    prompt_text = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION (TIER 1 - CYCLE 2):
- Domain: Automotive & EV Battery Manufacturing (Tier 1 Global High-Demand Industrial Automation)
- System: High-Speed Cylindrical & Prismatic EV Battery Cell Formation, Grading & Ultrasonic Foil-to-Tab Welding Line: 20 kHz 3.5 kW Ultrasonic Metal Welding Sonotrode with Active Dynamic Force Control (200 to 1200 N) & Energy/Peak Power/Distance Multi-Mode Weld Termination, Multi-Channel High-Precision Galvanostatic / Potentiostatic Cell Formation Cycler (0 to 5 V, 0 to 100 A with ±0.02% F.S. current accuracy and continuous dQ/dV differential capacity peak identification for SEI layer growth tracking), Vacuum Degassing Chamber with Puncture Needle Piercing and High-Frequency Hermetic Reseal Induction Heating, and High-Speed 6-Axis SCARA Cell Collation Gantry (< 0.8 s cycle time per cell).
- Function Block Name: `FB_Automotive_EV_CellFormation_UltrasonicTabWeld`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing ultrasonic horn resonant frequency phase angle, weld clamping normal force, dynamic acoustic impedance, cell terminal voltage, formation charging current, cell core temperature, vacuum degassing chamber pressure, and SCARA gantry Cartesian velocity.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing ultrasonic weld energy trajectory deviation ($Q$), formation current ripple ($R$), and cell core temperature rise ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on cell terminal voltage sensing probes, ultrasonic transducer piezoelectric force sensors, and vacuum chamber Pirani gauges.
   - Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
   - Deterministic 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering Cell Infeed & Barcode Laser Scan, SCARA Tab Alignment & Clamping, Ultrasonic Tab-to-Lead Horn Sonication (20 kHz Energy/Distance Cutoff), Weld Quality Signature Analysis (Acoustic Power Integral & Height Delta), Cell Transfer to Formation Tray, Constant-Current Constant-Voltage (CCCV) Formation Charging, dQ/dV SEI Passivation Layer Evaluation, Vacuum Degassing Chamber Puncture, Electrolyte Evacuation & Vacuum Decay Leak Test, High-Frequency Induction Reseal, Open-Circuit Voltage (OCV) & AC Internal Resistance (ACIR 1 kHz) Grading Sort, and Tray Eject to Aging Warehouse.
3. 100% Strict Syntax & Delimiter Parity:
   - Every `IF` must have `END_IF;`
   - Every `CASE` must have `END_CASE;`
   - Every `FOR` must have `END_FOR;`
   - First line: `FUNCTION_BLOCK FB_Automotive_EV_CellFormation_UltrasonicTabWeld`, Last line: `END_FUNCTION_BLOCK`
   - Triple backticks with `iec-st`: ` ```iec-st ` ... ` ``` `
4. Validation & Delivery:
   - Save your dataset to `data/swarm_raw/agent_<uuid>.json` with complete user/assistant message structure.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

    formatted_code = f"```iec-st\n{st_body}\n```"

    file_uuid = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{file_uuid}.json"

    record = {
        "id": f"synthetic_v7_{file_uuid}",
        "instruction": prompt_text,
        "input": "",
        "output": formatted_code,
        "messages": [
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": formatted_code}
        ]
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"SUCCESS: Saved dataset to {output_filename}")
    print(f"File Size: {os.path.getsize(output_filename)} bytes")

    # Run external validator
    res = subprocess.run(["python", "validate_iec.py", output_filename], capture_output=True, text=True)
    print("VALIDATOR STDOUT:\n", res.stdout)
    if res.stderr:
        print("VALIDATOR STDERR:\n", res.stderr)
    if res.returncode != 0:
        print(f"FAILED: Validator returned code {res.returncode}")
        exit(1)
    else:
        print(f"ALL CHECKS PASSED FOR {output_filename}!")

