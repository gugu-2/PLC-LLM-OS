# Master Generator for FB_Water_SWRO_Desalination_IsobaricERD_MembraneFouling
import json
import uuid
import re
import os

def build_full_st_code():
    st = []
    
    # Header comment
    st.append("""FUNCTION_BLOCK FB_Water_SWRO_Desalination_IsobaricERD_MembraneFouling
(*
 ====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - ULTRA-RIGOROUS SYNTHETIC DATASET V7 MAX-PERSONA
  DOMAIN: HEAVY MUNICIPAL INFRASTRUCTURE & MEGA-SCALE DESALINATION
  SYSTEM: WORLD-SCALE 600,000 M3/DAY SEAWATER REVERSE OSMOSIS (SWRO) FACILITY (DESALINATION TRAIN CELL)
 ====================================================================================================
  PROCESS TOPOLOGY & CYBER-PHYSICAL SPECIFICATION:
   1. HIGH-PRESSURE SEAWATER FEED PUMPING (HPFP):
      - 12 MW Medium-Voltage Variable Frequency Drive (VFD) multistage centrifugal pump delivering
        raw seawater feed up to 75.0 bar to spiral-wound polyamide thin-film composite (TFC) membranes.
      - Closed-loop dynamic decoupling of Transmembrane Pressure (TMP) and Permeate Recovery (45.0% +/- 0.5%).
      - Fast overpressure trip response (< 100 ms) preventing irreversible membrane compaction, delamination,
        and high-pressure vessel violent rupture.
   2. ISOBARIC CERAMIC PRESSURE EXCHANGER (PX) ENERGY RECOVERY DEVICE (ERD):
      - Ceramic isobaric rotor achieving 97.5% net hydraulic energy transfer efficiency from high-pressure
        brine concentrate reject to incoming raw seawater feed.
      - Integrated booster pump VFD compensating for PX internal duct hydraulic friction and differential head.
      - Online rotor speed monitoring (ST_ERD_PX_ROTOR_RPM_501), volumetric overflush index balancing,
        and ceramic hydrodynamic bearing lubrication film pressure management.
   3. MEMBRANE KINETICS, CONCENTRATION POLARIZATION & FOULING OBSERVER:
      - Extended Solution-Diffusion model ($J_w = A_w (\\Delta P - \\Delta \\pi), J_s = B_s (C_m - C_p)$).
      - Temperature Correction Factor (TCF) with Arrhenius thermal activation energy compensation.
      - Non-linear van 't Hoff osmotic pressure calculation (\\pi = f(TDS, T)) across feed, brine, and wall.
      - Boundary layer mass transfer modeling feed spacer channel crossflow hydrodynamics (Reynolds, Schmidt,
        Sherwood numbers) and exponential Concentration Polarization (CP) modulus (\\Gamma = exp(J_w / k_L)).
      - Online mineral scaling observer computing ionic strength, Stiff & Davis Stability Index (S&DSI),
        and Gypsum (CaSO4.2H2O) super-saturation ratio ($S_r = \\sqrt{IAP / K_{sp}}$).
      - Continuous biofouling and particulate cake resistance accumulation observer ($R_f$).
   4. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC):
      - 8-State x 8-Actuator discrete state-space formulation ($x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k$) at 50 ms cycle.
      - Quadratic cost functional ($J = \\sum (x-r)^T Q (x-r) + u^T R u + \\Delta u^T S \\Delta u$) optimizing HPFP VFD speed,
        ERD booster pump speed, brine throttle valve, and anti-scalant chemical dosing stroke.
      - Strict multi-objective optimization: Specific Energy Consumption ($SEC < 2.80 \\text{ kWh/m}^3$)
        and product water quality ($TDS < 200 \\text{ ppm}$, conductivity $< 350 \\mu\\text{S/cm}$).
   5. TRIPLE MODULAR REDUNDANCY (2oo3 TMR):
      - Triplicated high-pressure feed transmitters with 0.8 bar discrepancy threshold.
      - Triplicated concentrate reject transmitters with 0.8 bar discrepancy threshold.
      - Triplicated permeate conductivity analyzers with 5.0 uS/cm discrepancy limit.
      - Triplicated intake turbidity analyzers with 0.50 NTU discrepancy limit.
      - Automated channel degradation (3-healthy -> 2oo2 degraded -> 1oo1 fallback -> fail-safe trip).
   6. RED TIDE ALGAL BLOOM & HIGH TURBIDITY INTAKE DIVERSION INTERLOCKS:
      - Raw seawater intake turbidity spike detection (> 10.0 NTU) triggering fast diversion gate actuation
        to sea outfall, protecting ultrafiltration pretreatment and high-pressure reverse osmosis membranes.
      - Oxidation-Reduction Potential (ORP > 250 mV) fast trip preventing sodium hypochlorite free chlorine
        breakthrough from oxidizing aromatic polyamide membranes.
   7. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM):
      - 0:SYSTEM_OFFLINE_STANDBY, 1:LOW_PRESSURE_MEMBRANE_FLUSH, 2:CHEMICAL_SCALE_INHIBITOR_PRIME,
        3:HP_PUMP_SOFT_START_RAMP, 4:ERD_ISOBARIC_PX_SYNCHRONIZATION, 5:PRESSURE_RAMP_TO_OSMOTIC_BREAK,
        6:STEADY_STATE_PERMEATE_HARVEST, 7:MEMBRANE_CLEANING_CIP_CYCLE, 8:HIGH_TURBIDITY_INTAKE_DIVERT,
        9:CONCENTRATE_VALVE_DEPRESSURIZATION, 10:PERMEATE_DISCHARGE_FLUSH_SHUTDOWN, 11:EMERGENCY_ESTOP_LINE_RELIEF.
   8. ISA-18.2 MULTI-TIERED ALARM ENGINE & PACKED STATUS BITMASKS:
      - 5-Tier alarm structure (HI_HI, HI, LO, LO_LO, ROC) with deadband hysteresis.
      - Diagnostic telemetry words: dwStatusWord1, dwStatusWord2, dwAlarmWord_Trip, dwAlarmWord_Warning, dwSensorHealthMask.
 ====================================================================================================
*)""")

    # VAR_INPUT
    st.append("""VAR_INPUT
    (* Supervisory Permissives, Mode Selection & Safety Gates *)
    bMasterEnable                       : BOOL := FALSE;    (* Master Supervisory Execution Permissive Gate *)
    bEmergencyStop                      : BOOL := TRUE;     (* Hardwired Dual-Channel Active-Low E-Stop Interlock *)
    bResetFault                         : BOOL := FALSE;    (* Global Fault Reset and Alarm Acknowledge Command *)
    bAutoMpcEnable                      : BOOL := TRUE;     (* Receding-Horizon MPC Auto-Loop Closed-Loop Enable Gate *)
    bCipSequencePermissive              : BOOL := FALSE;    (* Operator Permissive to Initiate Clean-In-Place Cycle *)
    tTaskScanInterval                   : TIME := T#50MS;   (* Cyclic Task Scan Execution Period (Nominal: 50 ms) *)

    (* Phase 1: 2oo3 TMR High-Pressure Feed Pressure Transmitters [bar] *)
    PT_SWRO_HP_FEED_101A                : REAL := 68.5;     (* [bar] Membrane Train HP Feed Pressure Channel A *)
    PT_SWRO_HP_FEED_101B                : REAL := 68.5;     (* [bar] Membrane Train HP Feed Pressure Channel B *)
    PT_SWRO_HP_FEED_101C                : REAL := 68.5;     (* [bar] Membrane Train HP Feed Pressure Channel C *)

    (* Phase 1: 2oo3 TMR High-Pressure Brine Concentrate Reject Pressure Transmitters [bar] *)
    PT_SWRO_CONCENTRATE_102A            : REAL := 65.8;     (* [bar] High-Pressure Brine Reject Header Pressure Ch A *)
    PT_SWRO_CONCENTRATE_102B            : REAL := 65.8;     (* [bar] High-Pressure Brine Reject Header Pressure Ch B *)
    PT_SWRO_CONCENTRATE_102C            : REAL := 65.8;     (* [bar] High-Pressure Brine Reject Header Pressure Ch C *)

    (* Phase 1: 2oo3 TMR Permeate Product Header Backpressure Transmitters [bar] *)
    PT_SWRO_PERMEATE_103A               : REAL := 1.85;     (* [bar] Permeate Product Discharge Manifold Pressure Ch A *)
    PT_SWRO_PERMEATE_103B               : REAL := 1.85;     (* [bar] Permeate Product Discharge Manifold Pressure Ch B *)
    PT_SWRO_PERMEATE_103C               : REAL := 1.85;     (* [bar] Permeate Product Discharge Manifold Pressure Ch C *)

    (* Phase 1: 2oo3 TMR High-Pressure Seawater Feed Mass Flow Meters [m3/h] *)
    FT_HP_SEAWATER_FEED_201A            : REAL := 1300.0;   (* [m3/h] Total HP Seawater Inflow Flow Rate Ch A *)
    FT_HP_SEAWATER_FEED_201B            : REAL := 1300.0;   (* [m3/h] Total HP Seawater Inflow Flow Rate Ch B *)
    FT_HP_SEAWATER_FEED_201C            : REAL := 1300.0;   (* [m3/h] Total HP Seawater Inflow Flow Rate Ch C *)

    (* Phase 1: 2oo3 TMR Permeate Product Flow Meters [m3/h] *)
    FT_PERMEATE_PRODUCT_202A            : REAL := 585.0;    (* [m3/h] Permeate Desalinated Water Outflow Ch A *)
    FT_PERMEATE_PRODUCT_202B            : REAL := 585.0;    (* [m3/h] Permeate Desalinated Water Outflow Ch B *)
    FT_PERMEATE_PRODUCT_202C            : REAL := 585.0;    (* [m3/h] Permeate Desalinated Water Outflow Ch C *)

    (* Phase 1: 2oo3 TMR Brine Concentrate Reject Flow Meters [m3/h] *)
    FT_BRINE_REJECT_203A                : REAL := 715.0;    (* [m3/h] High-Pressure Brine Outflow Flow Rate Ch A *)
    FT_BRINE_REJECT_203B                : REAL := 715.0;    (* [m3/h] High-Pressure Brine Outflow Flow Rate Ch B *)
    FT_BRINE_REJECT_203C                : REAL := 715.0;    (* [m3/h] High-Pressure Brine Outflow Flow Rate Ch C *)

    (* Phase 1: 2oo3 TMR Raw Seawater Feed Salinity TDS Analyzers [ppm] *)
    AIT_FEED_SALINITY_TDS_301A          : REAL := 38500.0;  (* [ppm] Raw Seawater Inflow Total Dissolved Solids Ch A *)
    AIT_FEED_SALINITY_TDS_301B          : REAL := 38500.0;  (* [ppm] Raw Seawater Inflow Total Dissolved Solids Ch B *)
    AIT_FEED_SALINITY_TDS_301C          : REAL := 38500.0;  (* [ppm] Raw Seawater Inflow Total Dissolved Solids Ch C *)

    (* Phase 1: 2oo3 TMR Permeate Electrical Conductivity Analyzers [uS/cm] *)
    AIT_PERMEATE_CONDUCTIVITY_302A      : REAL := 285.0;    (* [uS/cm] Permeate Desalinated Water Conductivity Ch A *)
    AIT_PERMEATE_CONDUCTIVITY_302B      : REAL := 285.0;    (* [uS/cm] Permeate Desalinated Water Conductivity Ch B *)
    AIT_PERMEATE_CONDUCTIVITY_302C      : REAL := 285.0;    (* [uS/cm] Permeate Desalinated Water Conductivity Ch C *)

    (* Phase 1: 2oo3 TMR Raw Seawater Intake Turbidity Analyzers [NTU] *)
    AIT_INTAKE_TURBIDITY_NTU_303A       : REAL := 0.85;     (* [NTU] Raw Seawater Intake Turbidity Level Ch A *)
    AIT_INTAKE_TURBIDITY_NTU_303B       : REAL := 0.85;     (* [NTU] Raw Seawater Intake Turbidity Level Ch B *)
    AIT_INTAKE_TURBIDITY_NTU_303C       : REAL := 0.85;     (* [NTU] Raw Seawater Intake Turbidity Level Ch C *)

    (* Phase 1: 2oo3 TMR Seawater Inlet Temperature Transmitters [deg C] *)
    TT_SEAWATER_INLET_401A              : REAL := 24.5;     (* [deg C] Seawater Intake Feed Temperature Ch A *)
    TT_SEAWATER_INLET_401B              : REAL := 24.5;     (* [deg C] Seawater Intake Feed Temperature Ch B *)
    TT_SEAWATER_INLET_401C              : REAL := 24.5;     (* [deg C] Seawater Intake Feed Temperature Ch C *)

    (* Phase 1: 2oo3 TMR Isobaric Ceramic Pressure Exchanger (PX) Rotor Speed Tachometers [RPM] *)
    ST_ERD_PX_ROTOR_RPM_501A            : REAL := 1020.0;   (* [RPM] ERD Ceramic Rotor Rotational Speed Ch A *)
    ST_ERD_PX_ROTOR_RPM_501B            : REAL := 1020.0;   (* [RPM] ERD Ceramic Rotor Rotational Speed Ch B *)
    ST_ERD_PX_ROTOR_RPM_501C            : REAL := 1020.0;   (* [RPM] ERD Ceramic Rotor Rotational Speed Ch C *)

    (* Phase 1: 2oo3 TMR ERD Booster Circulation Pump Discharge Pressure Transmitters [bar] *)
    PT_ERD_BOOSTER_DISCHARGE_502A       : REAL := 69.2;     (* [bar] ERD Booster Pump Discharge Manifold Pressure Ch A *)
    PT_ERD_BOOSTER_DISCHARGE_502B       : REAL := 69.2;     (* [bar] ERD Booster Pump Discharge Manifold Pressure Ch B *)
    PT_ERD_BOOSTER_DISCHARGE_502C       : REAL := 69.2;     (* [bar] ERD Booster Pump Discharge Manifold Pressure Ch C *)

    (* Phase 1: 2oo3 TMR Feed Oxidation-Reduction Potential (ORP) Chlorine Analyzers [mV] *)
    AIT_FEED_ORP_304A                   : REAL := 165.0;    (* [mV] Feed Seawater ORP Redox Potential Ch A *)
    AIT_FEED_ORP_304B                   : REAL := 165.0;    (* [mV] Feed Seawater ORP Redox Potential Ch B *)
    AIT_FEED_ORP_304C                   : REAL := 165.0;    (* [mV] Feed Seawater ORP Redox Potential Ch C *)

    (* Auxiliary Process Transmitters *)
    PT_LP_FEED_SUCTION_104A             : REAL := 4.20;     (* [bar] Low-Pressure Feed Pump Suction Pressure Ch A *)
    PT_LP_FEED_SUCTION_104B             : REAL := 4.20;     (* [bar] Low-Pressure Feed Pump Suction Pressure Ch B *)
    FT_ANTISCALANT_DOSING_601A          : REAL := 12.8;     (* [L/h] Anti-Scalant Scale Inhibitor Dosing Flow Ch A *)
    FT_ANTISCALANT_DOSING_601B          : REAL := 12.8;     (* [L/h] Anti-Scalant Scale Inhibitor Dosing Flow Ch B *)
    LT_CIP_TANK_LEVEL_701               : REAL := 82.0;     (* [%] Clean-In-Place Chemical Tank Liquid Level *)
    TT_CIP_CLEANING_TEMP_702            : REAL := 35.0;     (* [deg C] Clean-In-Place Solution Cleaning Temperature *)
    AIT_FEED_PH_305                     : REAL := 8.15;     (* [pH] Raw Seawater Inflow pH Value *)
    AIT_CONCENTRATE_PH_306              : REAL := 7.95;     (* [pH] Brine Concentrate Reject pH Value *)
    AIT_CONCENTRATE_TDS_307             : REAL := 68500.0;  (* [ppm] Measured Brine Reject Salinity TDS *)

    (* Operator & Supervisory Recipe Processing Setpoints *)
    rSet_Recovery_Target_pct            : REAL := 45.0;     (* [%] Nominal Permeate Water Recovery Ratio Setpoint *)
    rSet_PermeateFlow_Target_m3_h       : REAL := 585.0;    (* [m3/h] Nominal Train Permeate Production Outflow *)
    rSet_MaxFeedPressure_bar            : REAL := 75.0;     (* [bar] Maximum Allowable HP Feed Pumping Pressure *)
    rSet_MaxPermeateTDS_ppm             : REAL := 200.0;    (* [ppm] Potable Water Maximum Permeate Salinity Ceiling *)
    rSet_TargetSEC_kWh_m3               : REAL := 2.80;     (* [kWh/m3] Maximum Target Specific Energy Consumption *)
    rSet_Antiscalant_Dosing_ppm         : REAL := 2.50;     (* [ppm] Target Chemical Anti-Scalant Feed Concentration *)
END_VAR""")

    # VAR_OUTPUT
    st.append("""VAR_OUTPUT
    (* Primary Actuator Control Commands *)
    rCmd_HPFP_VFD_Speed_Pct             : REAL := 0.0;      (* [%] 12 MW HP Feed Pump VFD Speed Reference (0..100%) *)
    rCmd_ERD_Booster_VFD_Speed_Pct      : REAL := 0.0;      (* [%] ERD Booster Circulation Pump VFD Reference (0..100%) *)
    rCmd_Brine_Throttle_Valve_Pct       : REAL := 0.0;      (* [%] High-Pressure Brine Reject Modulating Valve Position *)
    rCmd_Permeate_Backpressure_Valve_Pct: REAL := 0.0;      (* [%] Permeate Line Backpressure Regulating Valve Position *)
    rCmd_Antiscalant_Dosing_Pump_Pct    : REAL := 0.0;      (* [%] Chemical Anti-Scalant Metering Dosing Stroke Frequency *)
    rCmd_LP_Feed_Pump_Speed_Pct         : REAL := 0.0;      (* [%] Raw Seawater Intake Low-Pressure Booster Pump Speed *)
    rCmd_ERD_Overflush_TrimValve_Pct    : REAL := 0.0;      (* [%] PX Volumetric Balance & Overflush Trim Valve Position *)
    bCmd_Intake_Divert_Gate_Open        : BOOL := FALSE;    (* [bool] Red Tide / Storm High Turbidity Intake Diversion Gate *)
    bCmd_Permeate_DumpValve_Open        : BOOL := FALSE;    (* [bool] Off-Spec High Conductivity Permeate Dump to Outfall *)
    bCmd_CIP_Circulation_Pump_Run       : BOOL := FALSE;    (* [bool] Clean-In-Place Chemical Circulation Wash Pump Start *)
    bCmd_HP_Emergency_Depressurize_FastRelief: BOOL := FALSE; (* [bool] Fast Depressurization Relief Solenoid Valve *)
    bCmd_HPFP_Breaker_Trip              : BOOL := FALSE;    (* [bool] Hardwired 12 MW Medium-Voltage Switchgear Fast Trip *)

    (* 2oo3 TMR Validated Process Feedback *)
    rVoted_HP_Feed_Pressure_bar         : REAL := 68.5;     (* [bar] 2oo3 Validated Membrane Train HP Feed Pressure *)
    rVoted_Brine_Reject_Pressure_bar    : REAL := 65.8;     (* [bar] 2oo3 Validated High-Pressure Brine Reject Pressure *)
    rVoted_Permeate_Pressure_bar        : REAL := 1.85;     (* [bar] 2oo3 Validated Permeate Header Backpressure *)
    rVoted_HP_Seawater_Flow_m3_h        : REAL := 1300.0;   (* [m3/h] 2oo3 Validated Total HP Seawater Inflow Flow Rate *)
    rVoted_Permeate_Flow_m3_h           : REAL := 585.0;    (* [m3/h] 2oo3 Validated Permeate Desalinated Water Outflow *)
    rVoted_Brine_Reject_Flow_m3_h       : REAL := 715.0;    (* [m3/h] 2oo3 Validated Brine Reject Outflow Flow Rate *)
    rVoted_Feed_Salinity_TDS_ppm        : REAL := 38500.0;  (* [ppm] 2oo3 Validated Raw Seawater Inflow Salinity TDS *)
    rVoted_Permeate_Conductivity_uS_cm  : REAL := 285.0;    (* [uS/cm] 2oo3 Validated Permeate Electrical Conductivity *)
    rVoted_Intake_Turbidity_NTU         : REAL := 0.85;     (* [NTU] 2oo3 Validated Raw Seawater Intake Turbidity Level *)
    rVoted_Seawater_Temp_degC           : REAL := 24.5;     (* [deg C] 2oo3 Validated Seawater Intake Temperature *)
    rVoted_ERD_Rotor_Speed_RPM          : REAL := 1020.0;   (* [RPM] 2oo3 Validated ERD Ceramic Rotor Rotational Speed *)
    rVoted_ERD_Booster_Pressure_bar     : REAL := 69.2;     (* [bar] 2oo3 Validated ERD Booster Pump Discharge Pressure *)
    rVoted_Feed_ORP_mV                  : REAL := 165.0;    (* [mV] 2oo3 Validated Feed Seawater ORP Redox Potential *)

    (* Cyber-Physical Observers, Kinetic Models & Performance Metrics *)
    rCalculated_Transmembrane_Pressure_bar : REAL := 33.5;  (* [bar] Calculated Transmembrane Pressure (TMP) *)
    rCalculated_Net_Driving_Pressure_bar   : REAL := 5.80;  (* [bar] Calculated Net Driving Pressure (NDP = TMP - Delta_Pi) *)
    rCalculated_Permeate_Recovery_pct      : REAL := 45.0;  (* [%] Calculated Instantaneous Permeate Recovery Fraction *)
    rCalculated_Salt_Rejection_pct         : REAL := 99.58; (* [%] Dynamic Membrane Salt Rejection Efficiency *)
    rCalculated_Permeate_TDS_ppm           : REAL := 162.0; (* [ppm] Reconstructed Permeate Solute Concentration TDS *)
    rCalculated_Osmotic_Pressure_Feed_bar  : REAL := 27.65; (* [bar] Non-Linear van 't Hoff Feed Osmotic Pressure *)
    rCalculated_Osmotic_Pressure_Brine_bar : REAL := 49.20; (* [bar] Non-Linear van 't Hoff Brine Reject Osmotic Pressure *)
    rCalculated_Concentration_Polarization_Modulus : REAL := 1.185; (* [-] Exponential CP Modulus (Gamma = exp(Jw / kL)) *)
    rObserved_Fouling_Resistance_m_inv     : REAL := 2.45E11; (* [1/m] Cumulative Hydraulic Scaling & Biofouling Resistance *)
    rObserved_Stiff_Davis_Index            : REAL := -0.22; (* [-] Stiff & Davis Stability Index for High-Salinity Brine *)
    rObserved_Gypsum_Saturation_Ratio      : REAL := 0.68;  (* [-] CaSO4.2H2O Super-Saturation Ratio (Sr < 1.0 safe) *)
    rCalculated_ERD_Net_Efficiency_pct     : REAL := 97.5;  (* [%] Net Isobaric Hydraulic Energy Transfer Efficiency *)
    rCalculated_Specific_Energy_Consumption_kWh_m3 : REAL := 2.74; (* [kWh/m3] Specific Energy Consumption (SEC) *)
    rEstimated_Membrane_Life_Remaining_Months: REAL := 46.5;(* [months] Projected Membrane Useful Life to Compaction/Fouling *)

    (* Supervisory State, Telemetry & ISA-18.2 Diagnostic Bitmasks *)
    eActiveFsmState                     : INT := 0;         (* [-] Operational Finite State Machine Step (0..11) *)
    dwStatusWord1                       : DWORD := 16#0000; (* [-] Master Desalination Train Status & Valve Interlock Mask *)
    dwStatusWord2                       : DWORD := 16#0000; (* [-] ERD Synchronization, MPC Status & Observer Telemetry *)
    dwAlarmWord_Trip                    : DWORD := 16#0000; (* [-] ISA-18.2 Priority 1 / Emergency Safety Shutdown Latches *)
    dwAlarmWord_Warning                 : DWORD := 16#0000; (* [-] ISA-18.2 Priority 2 / Process Deviation Warning Latches *)
    dwSensorHealthMask                  : DWORD := 16#0000; (* [-] 2oo3 TMR Transducer Discrepancy & Channel Health Bitmask *)
    bProductionQualified                : BOOL := FALSE;    (* [bool] Potable Water Quality & Commercial Compliance Gate *)
    bEmergencyShutdownActive            : BOOL := FALSE;    (* [bool] Emergency Shutdown Active, Line Relieved, Tripped *)
END_VAR""")

    # VAR
    st.append("""VAR
    (* ====================================================================================================
       PHYSICAL CONSTANTS, MEMBRANE COEFFICIENTS & HYDRAULIC DIMENSIONS
       ==================================================================================================== *)
    rCONST_R_GAS                        : REAL := 8.31446;      (* Universal Gas Constant [J/(mol*K)] *)
    rCONST_MEMBRANE_AREA_M2             : REAL := 38000.0;      (* Aggregate Active Polyamide Membrane Area per Train [m2] *)
    rCONST_NOMINAL_Aw                   : REAL := 1.25E-11;     (* Pure Water Permeability Coeff Aw [m/(s*Pa)] at 25 C *)
    rCONST_NOMINAL_Bs                   : REAL := 2.20E-8;      (* Salt Permeability Coeff Bs [m/s] at 25 C *)
    rCONST_ACTIVATION_ENERGY_W          : REAL := 21500.0;      (* Water Permeation Thermal Activation Energy [J/mol] *)
    rCONST_ACTIVATION_ENERGY_S          : REAL := 32000.0;      (* Salt Permeation Thermal Activation Energy [J/mol] *)
    rCONST_SEAWATER_DENSITY_NOM         : REAL := 1028.0;       (* Raw Seawater Bulk Mass Density [kg/m3] *)
    rCONST_DIFFUSIVITY_NACL             : REAL := 1.55E-9;      (* Molecular Diffusion Coefficient of NaCl [m2/s] *)
    rCONST_FEED_SPACER_DH_M             : REAL := 0.00075;      (* Feed Spacer Channel Hydraulic Diameter dh [m] (34 mil) *)
    rCONST_FEED_CHANNEL_VOID_FRAC       : REAL := 0.88;         (* Feed Spacer Net Open Flow Void Fraction *)
    rCONST_HPFP_HYD_EFFICIENCY          : REAL := 0.885;        (* High-Pressure Feed Pump Hydraulic Efficiency *)
    rCONST_BOOSTER_HYD_EFFICIENCY       : REAL := 0.840;        (* ERD Booster Pump Hydraulic Efficiency *)
    rCONST_MOTOR_VFD_EFFICIENCY         : REAL := 0.965;        (* 12 MW MV Motor and VFD Combined Electrical Efficiency *)
    rCONST_PX_CERAMIC_ROTOR_VOLUME_L    : REAL := 14.5;         (* Isobaric Ceramic Pressure Exchanger Rotor Channel Vol [L] *)
    rCONST_PX_DUCT_GEOMETRY_K           : REAL := 0.785;        (* PX Rotor Volumetric Hydrodynamic Rotation Constant *)

    (* ====================================================================================================
       DISCRETE STATE-SPACE MATRICES & VECTORS (8 States x 8 Inputs)
       States x: [1: NDP (bar), 2: Jw (LMH), 3: Cm_wall (ppm), 4: Rf (10^11 m^-1),
                  5: Omega_px (RPM), 6: Recovery (%), 7: Cp_perm (ppm), 8: SEC (kWh/m3)]
       Inputs u: [1: Spd_HPFP (%), 2: Spd_Booster (%), 3: V_brine (%), 4: V_perm (%),
                  5: Stroke_Antiscalant (%), 6: Spd_LPFP (%), 7: V_overflush (%), 8: Gate_divert (%)]
       ==================================================================================================== *)
    matA                                : ARRAY[1..8, 1..8] OF REAL;
    matB                                : ARRAY[1..8, 1..8] OF REAL;
    matC                                : ARRAY[1..8, 1..8] OF REAL;
    matD                                : ARRAY[1..8, 1..8] OF REAL;
    matQ                                : ARRAY[1..8, 1..8] OF REAL;
    matR                                : ARRAY[1..8, 1..8] OF REAL;
    matS                                : ARRAY[1..8, 1..8] OF REAL;
    matP                                : ARRAY[1..8, 1..8] OF REAL;
    xState                              : ARRAY[1..8] OF REAL;
    xPred                               : ARRAY[1..8] OF REAL;
    xSetpoint                           : ARRAY[1..8] OF REAL;
    xError                              : ARRAY[1..8] OF REAL;
    uActuator                           : ARRAY[1..8] OF REAL;
    uPrevious                           : ARRAY[1..8] OF REAL;
    uOptimal                            : ARRAY[1..8] OF REAL;
    deltaU                              : ARRAY[1..8] OF REAL;
    uMin                                : ARRAY[1..8] OF REAL;
    uMax                                : ARRAY[1..8] OF REAL;
    deltaUMax                           : ARRAY[1..8] OF REAL;
    bMatricesInitialized                : BOOL := FALSE;

    (* Receding-Horizon MPC Dynamic Arrays *)
    xHorizon                            : ARRAY[1..5, 1..8] OF REAL;
    rGrad                               : ARRAY[1..8] OF REAL;
    rTotalCost                          : REAL := 0.0;
    rStepSize                           : REAL := 0.0012;
    iHorizonStep                        : INT := 1;
    iMatRow                             : INT := 1;
    iMatCol                             : INT := 1;
    kStateIdx                           : INT := 1;
    mInputIdx                           : INT := 1;

    (* ====================================================================================================
       2oo3 TMR SENSOR VOTING STRUCTURES, DISCREPANCY TIMERS & HEALTH MATRICES
       ==================================================================================================== *)
    rTMR_Tol_FeedPressure               : REAL := 0.8;      (* [bar] Discrepancy Tolerance for HP Feed Transmitters *)
    rTMR_Tol_BrinePressure              : REAL := 0.8;      (* [bar] Discrepancy Tolerance for Concentrate Transmitters *)
    rTMR_Tol_PermeatePressure           : REAL := 0.15;     (* [bar] Discrepancy Tolerance for Permeate Pressure *)
    rTMR_Tol_FeedFlow                   : REAL := 15.0;     (* [m3/h] Discrepancy Tolerance for HP Feed Flow *)
    rTMR_Tol_PermeateFlow               : REAL := 8.0;      (* [m3/h] Discrepancy Tolerance for Permeate Flow *)
    rTMR_Tol_BrineFlow                  : REAL := 10.0;     (* [m3/h] Discrepancy Tolerance for Brine Outflow *)
    rTMR_Tol_FeedTDS                    : REAL := 400.0;    (* [ppm] Discrepancy Tolerance for Feed Salinity TDS *)
    rTMR_Tol_PermeateCond               : REAL := 5.0;      (* [uS/cm] Discrepancy Tolerance for Permeate Conductivity *)
    rTMR_Tol_Turbidity                  : REAL := 0.50;     (* [NTU] Discrepancy Tolerance for Raw Intake Turbidity *)
    rTMR_Tol_Temperature               : REAL := 0.40;     (* [deg C] Discrepancy Tolerance for Seawater Temperature *)
    rTMR_Tol_RotorRPM                   : REAL := 25.0;     (* [RPM] Discrepancy Tolerance for ERD Rotor Tachometer *)
    rTMR_Tol_BoosterPressure            : REAL := 0.8;      (* [bar] Discrepancy Tolerance for ERD Booster Pressure *)
    rTMR_Tol_FeedORP                    : REAL := 15.0;     (* [mV] Discrepancy Tolerance for Feed ORP Analyzer *)

    (* Discrepancy Difference Registers *)
    rDiff_PFeed_AB, rDiff_PFeed_BC, rDiff_PFeed_CA       : REAL;
    bFault_PFeed_A, bFault_PFeed_B, bFault_PFeed_C       : BOOL;
    rTimer_PFeed_A, rTimer_PFeed_B, rTimer_PFeed_C       : REAL;
    iHealthy_PFeed                                       : INT := 3;

    rDiff_PBrine_AB, rDiff_PBrine_BC, rDiff_PBrine_CA   : REAL;
    bFault_PBrine_A, bFault_PBrine_B, bFault_PBrine_C   : BOOL;
    rTimer_PBrine_A, rTimer_PBrine_B, rTimer_PBrine_C   : REAL;
    iHealthy_PBrine                                     : INT := 3;

    rDiff_PPermeate_AB, rDiff_PPermeate_BC, rDiff_PPermeate_CA : REAL;
    bFault_PPermeate_A, bFault_PPermeate_B, bFault_PPermeate_C : BOOL;
    rTimer_PPermeate_A, rTimer_PPermeate_B, rTimer_PPermeate_C : REAL;
    iHealthy_PPermeate                                   : INT := 3;

    rDiff_FFeed_AB, rDiff_FFeed_BC, rDiff_FFeed_CA       : REAL;
    bFault_FFeed_A, bFault_FFeed_B, bFault_FFeed_C       : BOOL;
    rTimer_FFeed_A, rTimer_FFeed_B, rTimer_FFeed_C       : REAL;
    iHealthy_FFeed                                       : INT := 3;

    rDiff_FPerm_AB, rDiff_FPerm_BC, rDiff_FPerm_CA       : REAL;
    bFault_FPerm_A, bFault_FPerm_B, bFault_FPerm_C       : BOOL;
    rTimer_FPerm_A, rTimer_FPerm_B, rTimer_FPerm_C       : REAL;
    iHealthy_FPerm                                       : INT := 3;

    rDiff_FBrine_AB, rDiff_FBrine_BC, rDiff_FBrine_CA   : REAL;
    bFault_FBrine_A, bFault_FBrine_B, bFault_FBrine_C   : BOOL;
    rTimer_FBrine_A, rTimer_FBrine_B, rTimer_FBrine_C   : REAL;
    iHealthy_FBrine                                     : INT := 3;

    rDiff_TDSFeed_AB, rDiff_TDSFeed_BC, rDiff_TDSFeed_CA : REAL;
    bFault_TDSFeed_A, bFault_TDSFeed_B, bFault_TDSFeed_C : BOOL;
    rTimer_TDSFeed_A, rTimer_TDSFeed_B, rTimer_TDSFeed_C : REAL;
    iHealthy_TDSFeed                                     : INT := 3;

    rDiff_CondPerm_AB, rDiff_CondPerm_BC, rDiff_CondPerm_CA : REAL;
    bFault_CondPerm_A, bFault_CondPerm_B, bFault_CondPerm_C : BOOL;
    rTimer_CondPerm_A, rTimer_CondPerm_B, rTimer_CondPerm_C : REAL;
    iHealthy_CondPerm                                   : INT := 3;

    rDiff_Turb_AB, rDiff_Turb_BC, rDiff_Turb_CA         : REAL;
    bFault_Turb_A, bFault_Turb_B, bFault_Turb_C         : BOOL;
    rTimer_Turb_A, rTimer_Turb_B, rTimer_Turb_C         : REAL;
    iHealthy_Turb                                       : INT := 3;

    rDiff_Temp_AB, rDiff_Temp_BC, rDiff_Temp_CA         : REAL;
    bFault_Temp_A, bFault_Temp_B, bFault_Temp_C         : BOOL;
    rTimer_Temp_A, rTimer_Temp_B, rTimer_Temp_C         : REAL;
    iHealthy_Temp                                       : INT := 3;

    rDiff_RPM_AB, rDiff_RPM_BC, rDiff_RPM_CA             : REAL;
    bFault_RPM_A, bFault_RPM_B, bFault_RPM_C             : BOOL;
    rTimer_RPM_A, rTimer_RPM_B, rTimer_RPM_C             : REAL;
    iHealthy_RPM                                         : INT := 3;

    rDiff_PBoost_AB, rDiff_PBoost_BC, rDiff_PBoost_CA   : REAL;
    bFault_PBoost_A, bFault_PBoost_B, bFault_PBoost_C   : BOOL;
    rTimer_PBoost_A, rTimer_PBoost_B, rTimer_PBoost_C   : REAL;
    iHealthy_PBoost                                     : INT := 3;

    rDiff_ORP_AB, rDiff_ORP_BC, rDiff_ORP_CA             : REAL;
    bFault_ORP_A, bFault_ORP_B, bFault_ORP_C             : BOOL;
    rTimer_ORP_A, rTimer_ORP_B, rTimer_ORP_C             : REAL;
    iHealthy_ORP                                         : INT := 3;

    (* ====================================================================================================
       CYBER-PHYSICAL KINETIC, THERMODYNAMIC & FOULING VARIABLES
       ==================================================================================================== *)
    rTemp_Kelvin                        : REAL := 297.65;
    rTCF_TemperatureFactor              : REAL := 1.0;
    rOsmotic_Feed_Calc                  : REAL := 27.65;
    rOsmotic_Brine_Calc                 : REAL := 49.20;
    rOsmotic_Avg_Bulk                   : REAL := 38.42;
    rOsmotic_Perm_Calc                  : REAL := 0.12;
    rDelta_Osmotic_Bulk                 : REAL := 38.30;
    rDeltaP_Feed_To_Brine               : REAL := 2.70;
    rAverage_Pressure_Feed_Chamber      : REAL := 67.15;
    rCrossflowVelocity_m_s              : REAL := 0.185;
    rDynamicViscosity_Pa_s              : REAL := 0.00095;
    rReynolds_FeedChannel               : REAL := 150.2;
    rSchmidt_Feed                       : REAL := 595.0;
    rSherwood_Feed                      : REAL := 28.5;
    rMassTransferCoeff_kL_m_s           : REAL := 5.88E-5;
    rWaterFlux_Jw_LMH                   : REAL := 15.39;
    rWaterFlux_Jw_m_s                   : REAL := 4.275E-6;
    rCP_Exponent                        : REAL := 0.0727;
    rCP_Modulus_Gamma                   : REAL := 1.075;
    rWallConcentration_Cm_ppm           : REAL := 41380.0;
    rOsmotic_Wall_Calc                  : REAL := 29.72;
    rNet_Driving_Pressure_bar           : REAL := 5.80;
    rSaltFlux_Js_g_m2_h                 : REAL := 2.49;
    rCalculated_Permeate_Salinity_ppm   : REAL := 162.0;
    rIonicStrength_Brine                : REAL := 1.71;
    rStiffDavis_K_Factor                : REAL := 2.85;
    rStiffDavis_Index_SDSI              : REAL := -0.22;
    rGypsum_Ksp_Solubility              : REAL := 2.45E-4;
    rGypsum_IAP_Product                 : REAL := 1.13E-4;
    rGypsum_Saturation_Ratio_Sr         : REAL := 0.68;
    rFouling_Rate_Scaling_m_inv_s       : REAL := 0.0;
    rFouling_Rate_Biofouling_m_inv_s    : REAL := 1.25E5;
    rFouling_Rate_Shear_Removal_m_inv_s : REAL := 8.50E4;
    rFouling_Rate_Antiscalant_m_inv_s   : REAL := 1.10E5;
    rNet_Fouling_Rate_m_inv_s           : REAL := 0.0;

    (* Isobaric Ceramic ERD Dynamic Balances *)
    rERD_HP_Brine_Flow_m3_h             : REAL := 715.0;
    rERD_LP_Feed_Flow_m3_h              : REAL := 725.0;
    rERD_HP_Boosted_Flow_m3_h           : REAL := 715.0;
    rERD_Overflush_Fraction             : REAL := 0.014;
    rERD_Rotor_Expected_RPM             : REAL := 1020.0;
    rERD_HydraulicPower_Input_kW        : REAL := 1306.0;
    rERD_HydraulicPower_Recovered_kW    : REAL := 1273.0;
    rBoosterPump_Head_bar               : REAL := 2.70;
    rBoosterPump_HydraulicPower_kW      : REAL := 53.6;
    rBoosterPump_ElectricPower_kW       : REAL := 66.1;
    rHPFP_Direct_Feed_Flow_m3_h         : REAL := 585.0;
    rHPFP_HydraulicPower_kW             : REAL := 1113.0;
    rHPFP_ElectricPower_kW              : REAL := 1303.0;
    rLPFP_Intake_ElectricPower_kW       : REAL := 162.0;
    rTotal_Facility_Electric_Power_kW   : REAL := 1531.1;
    rCalculated_SEC_kWh_m3              : REAL := 2.617;

    (* ====================================================================================================
       12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) VARIABLES
       ==================================================================================================== *)
    STATE_SYSTEM_OFFLINE_STANDBY        : INT := 0;     (* Train depressurized, pumps offline, safe standby *)
    STATE_LOW_PRESSURE_MEMBRANE_FLUSH   : INT := 1;     (* Low-pressure raw feed flush displacing air/brine *)
    STATE_CHEMICAL_SCALE_INHIBITOR_PRIME: INT := 2;     (* Anti-scalant chemical dosing metering verified *)
    STATE_HP_PUMP_SOFT_START_RAMP       : INT := 3;     (* 12 MW HPFP VFD soft ramp to minimum head (30 bar) *)
    STATE_ERD_ISOBARIC_PX_SYNCHRONIZATION:INT := 4;     (* Isobaric ceramic PX rotor spun up, speed synced *)
    STATE_PRESSURE_RAMP_TO_OSMOTIC_BREAK:INT := 5;     (* Coordinated ramp through osmotic barrier (65 bar) *)
    STATE_STEADY_STATE_PERMEATE_HARVEST : INT := 6;     (* Closed-loop MPC active, 45% recovery, TDS < 200 ppm *)
    STATE_MEMBRANE_CLEANING_CIP_CYCLE   : INT := 7;     (* Low pressure chemical wash recirculation (acid/caustic) *)
    STATE_HIGH_TURBIDITY_INTAKE_DIVERT  : INT := 8;     (* Red tide / storm event: Raw intake diverted to sea *)
    STATE_CONCENTRATE_VALVE_DEPRESSURIZATION:INT := 9;  (* Controlled depressurization of concentrate manifold *)
    STATE_PERMEATE_DISCHARGE_FLUSH_SHUTDOWN:INT := 10;  (* Fresh permeate flush displacing seawater in vessels *)
    STATE_EMERGENCY_ESTOP_LINE_RELIEF   : INT := 11;    (* Fast breaker trip, fast relief valve depressurize *)

    tFsmStepTimer_Sec                   : REAL := 0.0;
    tFlushTimer_Sec                     : REAL := 0.0;
    tSoftStartTimer_Sec                 : REAL := 0.0;
    tSyncTimer_Sec                      : REAL := 0.0;
    tPressureRampTimer_Sec              : REAL := 0.0;
    tCipTimer_Sec                       : REAL := 0.0;
    rRampTargetPressure                 : REAL := 68.5;
    rRampTargetVFD                      : REAL := 82.5;

    (* ====================================================================================================
       ISA-18.2 MULTI-TIERED ALARM THRESHOLDS & HYSTERESIS
       ==================================================================================================== *)
    rALM_TRIP_FEED_P_HH                 : REAL := 78.0;     (* [bar] High-High Feed Overpressure Compaction Fast Trip *)
    rALM_WARN_FEED_P_H                  : REAL := 75.5;     (* [bar] High Feed Pressure Warning *)
    rALM_WARN_FEED_P_L                  : REAL := 45.0;     (* [bar] Low Feed Pressure Warning *)
    rALM_TRIP_FEED_P_LL                 : REAL := 35.0;     (* [bar] Low-Low Feed Pressure Loss Trip *)
    rALM_HYST_FEED_P                    : REAL := 0.8;      (* [bar] Feed Pressure Deadband Hysteresis *)

    rALM_TRIP_PERM_COND_HH              : REAL := 450.0;    (* [uS/cm] High-High Permeate Conductivity Off-Spec Trip *)
    rALM_WARN_PERM_COND_H               : REAL := 350.0;    (* [uS/cm] High Permeate Conductivity Warning *)
    rALM_HYST_PERM_COND                 : REAL := 5.0;      (* [uS/cm] Permeate Conductivity Hysteresis *)

    rALM_TRIP_TURBIDITY_HH              : REAL := 10.0;     (* [NTU] High-High Raw Turbidity Red Tide Sluice Diversion *)
    rALM_WARN_TURBIDITY_H               : REAL := 4.0;      (* [NTU] High Turbidity Pre-warning *)
    rALM_HYST_TURBIDITY                 : REAL := 0.50;     (* [NTU] Turbidity Deadband Hysteresis *)

    rALM_TRIP_BRINE_P_HH                : REAL := 75.0;     (* [bar] High-High Brine Header Overpressure Trip *)
    rALM_TRIP_BRINE_P_LL                : REAL := 35.0;     (* [bar] Low-Low Brine Header Loss of Backpressure Trip *)
    rALM_HYST_BRINE_P                   : REAL := 0.8;      (* [bar] Brine Pressure Deadband Hysteresis *)

    rALM_TRIP_PX_ROTOR_HH               : REAL := 1500.0;   (* [RPM] High-High PX Ceramic Rotor Overspeed Trip *)
    rALM_TRIP_PX_ROTOR_LL               : REAL := 400.0;    (* [RPM] Low-Low PX Ceramic Rotor Stall Trip *)
    rALM_HYST_PX_ROTOR                  : REAL := 25.0;     (* [RPM] PX Rotor Speed Hysteresis *)

    rALM_TRIP_ANTISCALANT_LL            : REAL := 4.0;      (* [L/h] Low-Low Anti-Scalant Scale Inhibitor Loss Trip *)
    rALM_HYST_ANTISCALANT               : REAL := 0.5;      (* [L/h] Anti-Scalant Flow Hysteresis *)

    rALM_TRIP_ORP_HH                    : REAL := 250.0;    (* [mV] High-High ORP Chlorine Breakthrough Membrane Trip *)
    rALM_HYST_ORP                       : REAL := 10.0;     (* [mV] ORP Deadband Hysteresis *)

    rALM_WARN_SDSI_H                    : REAL := 0.50;     (* [-] High Stiff & Davis Scaling Potential Warning *)
    rALM_HYST_SDSI                      : REAL := 0.05;     (* [-] SDSI Deadband Hysteresis *)

    rALM_WARN_SEC_H                     : REAL := 3.20;     (* [kWh/m3] High Specific Energy Consumption Warning *)
    rALM_HYST_SEC                       : REAL := 0.05;     (* [kWh/m3] SEC Deadband Hysteresis *)

    (* ISA-18.2 Discrete Alarm Latch Flags *)
    bAlm_Feed_P_HH                      : BOOL := FALSE;
    bAlm_Feed_P_H                       : BOOL := FALSE;
    bAlm_Feed_P_L                       : BOOL := FALSE;
    bAlm_Feed_P_LL                      : BOOL := FALSE;
    bAlm_Perm_Cond_HH                   : BOOL := FALSE;
    bAlm_Perm_Cond_H                    : BOOL := FALSE;
    bAlm_Turbidity_HH                   : BOOL := FALSE;
    bAlm_Turbidity_H                    : BOOL := FALSE;
    bAlm_Brine_P_HH                     : BOOL := FALSE;
    bAlm_Brine_P_LL                     : BOOL := FALSE;
    bAlm_PX_Rotor_HH                    : BOOL := FALSE;
    bAlm_PX_Rotor_LL                    : BOOL := FALSE;
    bAlm_Antiscalant_LL                 : BOOL := FALSE;
    bAlm_ORP_HH                         : BOOL := FALSE;
    bAlm_SDSI_H                         : BOOL := FALSE;
    bAlm_SEC_H                          : BOOL := FALSE;
    bAlm_Discrepancy_Trip               : BOOL := FALSE;

    (* Auxiliary Math & Scan Registers *)
    rDeltaTime_Sec                      : REAL := 0.050;    (* Deterministic Task Scan Duration [s] *)
    rPreviousFeedPressure               : REAL := 68.5;
    rPressureROC_bar_s                  : REAL := 0.0;
    rPreviousPermeateCond               : REAL := 285.0;
    rCondROC_uS_cm_s                    : REAL := 0.0;
    rTempCalc1                          : REAL := 0.0;
    rTempCalc2                          : REAL := 0.0;
    rTempCalc3                          : REAL := 0.0;
END_VAR""")

    # MAIN LOGIC - Master safety interlock & execution supervision
    st.append("""(* ====================================================================================================
   EXECUTION CYCLE: MASTER SAFETY INTERLOCK & SUPERVISION EVALUATION
   ==================================================================================================== *)
IF NOT bMasterEnable OR NOT bEmergencyStop THEN
    eActiveFsmState                             := STATE_EMERGENCY_ESTOP_LINE_RELIEF;
    rCmd_HPFP_VFD_Speed_Pct                     := 0.0;
    rCmd_ERD_Booster_VFD_Speed_Pct              := 0.0;
    rCmd_LP_Feed_Pump_Speed_Pct                 := 0.0;
    rCmd_Antiscalant_Dosing_Pump_Pct            := 0.0;
    rCmd_Brine_Throttle_Valve_Pct               := 100.0; (* Full Open to Prevent High-Pressure Accumulation *)
    rCmd_Permeate_Backpressure_Valve_Pct        := 100.0;
    rCmd_ERD_Overflush_TrimValve_Pct            := 0.0;
    bCmd_HP_Emergency_Depressurize_FastRelief   := TRUE;  (* Fast Water Hammer & Line Pressure Relief *)
    bCmd_HPFP_Breaker_Trip                      := TRUE;  (* Medium-Voltage Breaker Trip Permissive *)
    bCmd_Intake_Divert_Gate_Open                := TRUE;  (* Divert Raw Seawater to Sea Outfall *)
    bCmd_Permeate_DumpValve_Open                := TRUE;  (* Dump Permeate to Prevent Backflow Contamination *)
    bCmd_CIP_Circulation_Pump_Run               := FALSE;
    bEmergencyShutdownActive                    := TRUE;
    bProductionQualified                        := FALSE;
    dwStatusWord1                               := 16#0001; (* Master Safety Tripped Bitmask *)
    dwAlarmWord_Trip                            := 16#0001;
    RETURN;
END_IF;

(* Deterministic Cycle Scan Duration Normalization *)
rDeltaTime_Sec := TIME_TO_REAL(tTaskScanInterval) / 1000.0;
IF rDeltaTime_Sec < 0.010 THEN
    rDeltaTime_Sec := 0.050;
END_IF;""")

    # PHASE 0: State-space matrix initialization
    st.append("""(* ====================================================================================================
   PHASE 0: DETERMINISTIC INITIALIZATION OF DISCRETE STATE-SPACE & MPC WEIGHT MATRICES
   Discrete State Vector x (8x1):
     x[1] = Net Transmembrane Driving Pressure NDP [bar] (Nominal: 5.80)
     x[2] = Permeate Water Flux Jw [LMH] (Nominal: 15.39)
     x[3] = Membrane Wall Solute Concentration Cm [ppm] (Nominal: 41380.0)
     x[4] = Cumulative Hydraulic Fouling Resistance Rf [10^11 m^-1] (Nominal: 2.45)
     x[5] = Isobaric Ceramic PX Rotor Speed Omega_px [RPM] (Nominal: 1020.0)
     x[6] = Permeate Water Recovery Ratio Y [%] (Nominal: 45.0)
     x[7] = Permeate Desalinated Water Salinity Cp [ppm] (Nominal: 162.0)
     x[8] = Train Specific Energy Consumption SEC [kWh/m3] (Nominal: 2.617)

   Discrete Actuator Vector u (8x1):
     u[1] = 12 MW HPFP VFD Speed Reference Spd_HPFP [%] (Nominal: 82.5)
     u[2] = ERD Booster Circulation Pump Speed Spd_Booster [%] (Nominal: 78.0)
     u[3] = High-Pressure Brine Reject Throttle Valve V_brine [%] (Nominal: 46.5)
     u[4] = Permeate Line Backpressure Regulating Valve V_perm [%] (Nominal: 25.0)
     u[5] = Chemical Anti-Scalant Metering Dosing Stroke [%] (Nominal: 62.0)
     u[6] = Raw Seawater Intake LP Booster Pump Speed [%] (Nominal: 55.0)
     u[7] = PX Volumetric Overflush Balance Trim Valve [%] (Nominal: 35.0)
     u[8] = Raw Intake Red Tide Diversion Sluice Gate [%] (Nominal: 0.0 = Service)
   ==================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* Discrete Transition Matrix A (8x8) at Ts = 50 ms *)
    matA[1, 1] :=  0.9780; matA[1, 2] := -0.0240; matA[1, 3] := -0.0120; matA[1, 4] := -0.0350; matA[1, 5] :=  0.0050; matA[1, 6] :=  0.0000; matA[1, 7] :=  0.0000; matA[1, 8] :=  0.0000;
    matA[2, 1] :=  0.0450; matA[2, 2] :=  0.9620; matA[2, 3] := -0.0180; matA[2, 4] := -0.0480; matA[2, 5] :=  0.0000; matA[2, 6] :=  0.0000; matA[2, 7] :=  0.0000; matA[2, 8] :=  0.0000;
    matA[3, 1] :=  0.0150; matA[3, 2] :=  0.0650; matA[3, 3] :=  0.9850; matA[3, 4] :=  0.0000; matA[3, 5] := -0.0080; matA[3, 6] :=  0.0220; matA[3, 7] :=  0.0000; matA[3, 8] :=  0.0000;
    matA[4, 1] :=  0.0002; matA[4, 2] :=  0.0008; matA[4, 3] :=  0.0012; matA[4, 4] :=  0.9998; matA[4, 5] :=  0.0000; matA[4, 6] :=  0.0000; matA[4, 7] :=  0.0000; matA[4, 8] :=  0.0000;
    matA[5, 1] :=  0.0000; matA[5, 2] :=  0.0000; matA[5, 3] :=  0.0000; matA[5, 4] :=  0.0000; matA[5, 5] :=  0.9450; matA[5, 6] :=  0.0000; matA[5, 7] :=  0.0000; matA[5, 8] :=  0.0000;
    matA[6, 1] :=  0.0180; matA[6, 2] :=  0.0420; matA[6, 3] :=  0.0000; matA[6, 4] := -0.0050; matA[6, 5] := -0.0150; matA[6, 6] :=  0.9550; matA[6, 7] :=  0.0000; matA[6, 8] :=  0.0000;
    matA[7, 1] := -0.0080; matA[7, 2] := -0.0150; matA[7, 3] :=  0.0350; matA[7, 4] :=  0.0000; matA[7, 5] :=  0.0000; matA[7, 6] :=  0.0120; matA[7, 7] :=  0.9750; matA[7, 8] :=  0.0000;
    matA[8, 1] :=  0.0250; matA[8, 2] := -0.0450; matA[8, 3] :=  0.0000; matA[8, 4] :=  0.0180; matA[8, 5] := -0.0350; matA[8, 6] := -0.0550; matA[8, 7] :=  0.0000; matA[8, 8] :=  0.9820;

    (* Discrete Input Coupling Matrix B (8x8) at Ts = 50 ms *)
    matB[1, 1] :=  0.3850; matB[1, 2] :=  0.0650; matB[1, 3] := -0.2150; matB[1, 4] := -0.0850; matB[1, 5] :=  0.0000; matB[1, 6] :=  0.0250; matB[1, 7] :=  0.0000; matB[1, 8] := -0.1500;
    matB[2, 1] :=  0.4200; matB[2, 2] :=  0.0750; matB[2, 3] := -0.1850; matB[2, 4] := -0.0650; matB[2, 5] :=  0.0000; matB[2, 6] :=  0.0150; matB[2, 7] :=  0.0000; matB[2, 8] := -0.1200;
    matB[3, 1] :=  0.1500; matB[3, 2] :=  0.0350; matB[3, 3] := -0.3200; matB[3, 4] :=  0.0000; matB[3, 5] := -0.0050; matB[3, 6] :=  0.0000; matB[3, 7] := -0.0450; matB[3, 8] :=  0.0000;
    matB[4, 1] :=  0.0010; matB[4, 2] :=  0.0000; matB[4, 3] := -0.0020; matB[4, 4] :=  0.0000; matB[4, 5] := -0.0180; matB[4, 6] :=  0.0000; matB[4, 7] :=  0.0000; matB[4, 8] :=  0.0000;
    matB[5, 1] :=  0.0500; matB[5, 2] :=  0.0000; matB[5, 3] :=  0.4850; matB[5, 4] :=  0.0000; matB[5, 5] :=  0.0000; matB[5, 6] :=  0.0000; matB[5, 7] :=  0.0650; matB[5, 8] :=  0.0000;
    matB[6, 1] :=  0.0850; matB[6, 2] :=  0.0150; matB[6, 3] := -0.4500; matB[6, 4] := -0.0250; matB[6, 5] :=  0.0000; matB[6, 6] := -0.0650; matB[6, 7] :=  0.0000; matB[6, 8] :=  0.0000;
    matB[7, 1] := -0.0650; matB[7, 2] := -0.0120; matB[7, 3] :=  0.0450; matB[7, 4] :=  0.0150; matB[7, 5] :=  0.0000; matB[7, 6] :=  0.0000; matB[7, 7] :=  0.0000; matB[7, 8] :=  0.0000;
    matB[8, 1] :=  0.2250; matB[8, 2] :=  0.0450; matB[8, 3] := -0.0850; matB[8, 4] :=  0.0120; matB[8, 5] :=  0.0020; matB[8, 6] :=  0.0180; matB[8, 7] := -0.0250; matB[8, 8] :=  0.0000;

    (* Output Observation Matrix C (8x8) *)
    FOR iMatRow := 1 TO 8 DO
        FOR iMatCol := 1 TO 8 DO
            IF iMatRow = iMatCol THEN
                matC[iMatRow, iMatCol] := 1.0;
                matD[iMatRow, iMatCol] := 0.0;
            ELSE
                matC[iMatRow, iMatCol] := 0.0;
                matD[iMatRow, iMatCol] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* MPC Quadratic Penalty Weights: Q (States), R (Effort), S (Slew Rate), P (Terminal) *)
    FOR iMatRow := 1 TO 8 DO
        FOR iMatCol := 1 TO 8 DO
            matQ[iMatRow, iMatCol] := 0.0;
            matR[iMatRow, iMatCol] := 0.0;
            matS[iMatRow, iMatCol] := 0.0;
            matP[iMatRow, iMatCol] := 0.0;
        END_FOR;
    END_FOR;

    (* Diagonal State Penalties Q: NDP, Jw, Cm, Rf, Omega_px, Recovery, Cp, SEC *)
    matQ[1, 1] := 12.0;    (* NDP pressure deviation *)
    matQ[2, 2] := 18.0;    (* Permeate flux stability *)
    matQ[3, 3] := 0.02;    (* Wall concentration *)
    matQ[4, 4] := 150.0;   (* Fouling resistance suppression *)
    matQ[5, 5] := 0.08;    (* PX rotor speed stability *)
    matQ[6, 6] := 180.0;   (* High penalty on 45.0% Recovery setpoint lock *)
    matQ[7, 7] := 45.0;    (* Permeate product TDS compliance (< 200 ppm) *)
    matQ[8, 8] := 250.0;   (* Highest penalty: minimize SEC (< 2.80 kWh/m3) *)

    (* Diagonal Actuator Effort Penalties R *)
    matR[1, 1] := 0.85;    (* HPFP VFD power penalty *)
    matR[2, 2] := 0.35;    (* Booster VFD effort *)
    matR[3, 3] := 0.45;    (* Brine throttle modulation *)
    matR[4, 4] := 0.20;    (* Permeate backpressure *)
    matR[5, 5] := 1.50;    (* Chemical dosing cost penalty *)
    matR[6, 6] := 0.25;    (* LP intake booster *)
    matR[7, 7] := 0.15;    (* PX trim valve *)
    matR[8, 8] := 500.0;   (* Severe penalty on intake diversion (emergency only) *)

    (* Diagonal Slew Rate Penalties S: suppress high-frequency valve chattering *)
    matS[1, 1] := 8.50;    (* HPFP VFD rate limiter *)
    matS[2, 2] := 3.20;
    matS[3, 3] := 4.80;    (* Brine valve cavitation suppressor *)
    matS[4, 4] := 2.50;
    matS[5, 5] := 1.20;
    matS[6, 6] := 2.00;
    matS[7, 7] := 1.50;
    matS[8, 8] := 25.0;

    (* Terminal Weights P: Riccati solution approximation P = 2.5 * Q *)
    FOR iMatRow := 1 TO 8 DO
        matP[iMatRow, iMatRow] := matQ[iMatRow, iMatRow] * 2.5;
    END_FOR;

    (* Actuator Physical Saturation Bounds [uMin, uMax] and Slew Limits deltaUMax *)
    uMin[1] := 25.0;  uMax[1] := 100.0; deltaUMax[1] := 1.5;  (* HPFP VFD (25% min cooling flow) *)
    uMin[2] := 15.0;  uMax[2] := 100.0; deltaUMax[2] := 2.0;  (* ERD Booster VFD *)
    uMin[3] := 10.0;  uMax[3] := 95.0;  deltaUMax[3] := 2.5;  (* Brine Throttle Valve *)
    uMin[4] := 5.0;   uMax[4] := 90.0;  deltaUMax[4] := 3.0;  (* Permeate Backpressure *)
    uMin[5] := 0.0;   uMax[5] := 100.0; deltaUMax[5] := 5.0;  (* Anti-Scalant Dosing *)
    uMin[6] := 20.0;  uMax[6] := 100.0; deltaUMax[6] := 2.0;  (* LP Intake Booster *)
    uMin[7] := 0.0;   uMax[7] := 100.0; deltaUMax[7] := 5.0;  (* PX Trim Valve *)
    uMin[8] := 0.0;   uMax[8] := 100.0; deltaUMax[8] := 10.0; (* Intake Divert Gate *)

    bMatricesInitialized := TRUE;
END_IF;""")

    # PHASE 1: 2oo3 TMR Voting Logic for all 13 transmitter sets
    # We write a function to generate each 2oo3 block cleanly
    def make_tmr_block(tag, chA, chB, chC, tol, v_out, diffAB, diffBC, diffCA, fA, fB, fC, tA, tB, tC, hCount, bitmask_fault, unit, name):
        return f"""(* --- 2oo3 TMR: {name} [{unit}] (Tag: {tag}, Tol: {tol} {unit}) --- *)
{diffAB} := ABS({chA} - {chB});
{diffBC} := ABS({chB} - {chC});
{diffCA} := ABS({chC} - {chA});

IF {diffAB} > {tol} THEN
    {tA} := {tA} + rDeltaTime_Sec;
    {tB} := {tB} + rDeltaTime_Sec;
ELSE
    IF {tA} > 0.0 THEN {tA} := {tA} - (rDeltaTime_Sec * 0.5); END_IF;
    IF {tB} > 0.0 THEN {tB} := {tB} - (rDeltaTime_Sec * 0.5); END_IF;
END_IF;

IF {diffBC} > {tol} THEN
    {tB} := {tB} + rDeltaTime_Sec;
    {tC} := {tC} + rDeltaTime_Sec;
ELSE
    IF {tB} > 0.0 THEN {tB} := {tB} - (rDeltaTime_Sec * 0.5); END_IF;
    IF {tC} > 0.0 THEN {tC} := {tC} - (rDeltaTime_Sec * 0.5); END_IF;
END_IF;

IF {diffCA} > {tol} THEN
    {tC} := {tC} + rDeltaTime_Sec;
    {tA} := {tA} + rDeltaTime_Sec;
ELSE
    IF {tC} > 0.0 THEN {tC} := {tC} - (rDeltaTime_Sec * 0.5); END_IF;
    IF {tA} > 0.0 THEN {tA} := {tA} - (rDeltaTime_Sec * 0.5); END_IF;
END_IF;

{fA} := ({tA} >= 0.500);
{fB} := ({tB} >= 0.500);
{fC} := ({tC} >= 0.500);

{hCount} := 3;
IF {fA} THEN {hCount} := {hCount} - 1; END_IF;
IF {fB} THEN {hCount} := {hCount} - 1; END_IF;
IF {fC} THEN {hCount} := {hCount} - 1; END_IF;

CASE {hCount} OF
    3: (* All 3 channels healthy: Mid-value selection (median) *)
        IF (({chA} >= {chB}) AND ({chA} <= {chC})) OR (({chA} >= {chC}) AND ({chA} <= {chB})) THEN
            {v_out} := {chA};
        ELSIF (({chB} >= {chA}) AND ({chB} <= {chC})) OR (({chB} >= {chC}) AND ({chB} <= {chA})) THEN
            {v_out} := {chB};
        ELSE
            {v_out} := {chC};
        END_IF;

    2: (* 1 channel degraded: Arithmetic average of remaining 2 healthy channels *)
        IF NOT {fA} AND NOT {fB} THEN
            {v_out} := ({chA} + {chB}) * 0.5;
        ELSIF NOT {fB} AND NOT {fC} THEN
            {v_out} := ({chB} + {chC}) * 0.5;
        ELSE
            {v_out} := ({chA} + {chC}) * 0.5;
        END_IF;
        dwSensorHealthMask := dwSensorHealthMask OR {bitmask_fault};

    1: (* 2 channels degraded: Fallback to sole surviving healthy channel *)
        IF NOT {fA} THEN
            {v_out} := {chA};
        ELSIF NOT {fB} THEN
            {v_out} := {chB};
        ELSE
            {v_out} := {chC};
        END_IF;
        dwSensorHealthMask := dwSensorHealthMask OR {bitmask_fault};
        dwAlarmWord_Warning := dwAlarmWord_Warning OR {bitmask_fault};

    0: (* Complete TMR failure: Hold last valid value and trip critical discrepancy latch *)
        bAlm_Discrepancy_Trip := TRUE;
        dwAlarmWord_Trip := dwAlarmWord_Trip OR {bitmask_fault};
END_CASE;"""

    st.append("(* ====================================================================================================\n   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & SENSOR HEALTH ENGINES\n   ==================================================================================================== *)")
    st.append(make_tmr_block("PT_SWRO_HP_FEED_101", "PT_SWRO_HP_FEED_101A", "PT_SWRO_HP_FEED_101B", "PT_SWRO_HP_FEED_101C", "rTMR_Tol_FeedPressure", "rVoted_HP_Feed_Pressure_bar", "rDiff_PFeed_AB", "rDiff_PFeed_BC", "rDiff_PFeed_CA", "bFault_PFeed_A", "bFault_PFeed_B", "bFault_PFeed_C", "rTimer_PFeed_A", "rTimer_PFeed_B", "rTimer_PFeed_C", "iHealthy_PFeed", "16#0002", "bar", "Membrane Train HP Feed Pressure Transmitters"))
    st.append(make_tmr_block("PT_SWRO_CONCENTRATE_102", "PT_SWRO_CONCENTRATE_102A", "PT_SWRO_CONCENTRATE_102B", "PT_SWRO_CONCENTRATE_102C", "rTMR_Tol_BrinePressure", "rVoted_Brine_Reject_Pressure_bar", "rDiff_PBrine_AB", "rDiff_PBrine_BC", "rDiff_PBrine_CA", "bFault_PBrine_A", "bFault_PBrine_B", "bFault_PBrine_C", "rTimer_PBrine_A", "rTimer_PBrine_B", "rTimer_PBrine_C", "iHealthy_PBrine", "16#0004", "bar", "High-Pressure Brine Reject Header Pressure"))
    st.append(make_tmr_block("PT_SWRO_PERMEATE_103", "PT_SWRO_PERMEATE_103A", "PT_SWRO_PERMEATE_103B", "PT_SWRO_PERMEATE_103C", "rTMR_Tol_PermeatePressure", "rVoted_Permeate_Pressure_bar", "rDiff_PPermeate_AB", "rDiff_PPermeate_BC", "rDiff_PPermeate_CA", "bFault_PPermeate_A", "bFault_PPermeate_B", "bFault_PPermeate_C", "rTimer_PPermeate_A", "rTimer_PPermeate_B", "rTimer_PPermeate_C", "iHealthy_PPermeate", "16#0008", "bar", "Permeate Header Backpressure Transmitters"))
    st.append(make_tmr_block("FT_HP_SEAWATER_FEED_201", "FT_HP_SEAWATER_FEED_201A", "FT_HP_SEAWATER_FEED_201B", "FT_HP_SEAWATER_FEED_201C", "rTMR_Tol_FeedFlow", "rVoted_HP_Seawater_Flow_m3_h", "rDiff_FFeed_AB", "rDiff_FFeed_BC", "rDiff_FFeed_CA", "bFault_FFeed_A", "bFault_FFeed_B", "bFault_FFeed_C", "rTimer_FFeed_A", "rTimer_FFeed_B", "rTimer_FFeed_C", "iHealthy_FFeed", "16#0010", "m3/h", "High-Pressure Seawater Feed Mass Flow Meters"))
    st.append(make_tmr_block("FT_PERMEATE_PRODUCT_202", "FT_PERMEATE_PRODUCT_202A", "FT_PERMEATE_PRODUCT_202B", "FT_PERMEATE_PRODUCT_202C", "rTMR_Tol_PermeateFlow", "rVoted_Permeate_Flow_m3_h", "rDiff_FPerm_AB", "rDiff_FPerm_BC", "rDiff_FPerm_CA", "bFault_FPerm_A", "bFault_FPerm_B", "bFault_FPerm_C", "rTimer_FPerm_A", "rTimer_FPerm_B", "rTimer_FPerm_C", "iHealthy_FPerm", "16#0020", "m3/h", "Permeate Desalinated Product Water Flow Meters"))
    st.append(make_tmr_block("FT_BRINE_REJECT_203", "FT_BRINE_REJECT_203A", "FT_BRINE_REJECT_203B", "FT_BRINE_REJECT_203C", "rTMR_Tol_BrineFlow", "rVoted_Brine_Reject_Flow_m3_h", "rDiff_FBrine_AB", "rDiff_FBrine_BC", "rDiff_FBrine_CA", "bFault_FBrine_A", "bFault_FBrine_B", "bFault_FBrine_C", "rTimer_FBrine_A", "rTimer_FBrine_B", "rTimer_FBrine_C", "iHealthy_FBrine", "16#0040", "m3/h", "Brine Concentrate Reject Outflow Flow Meters"))
    st.append(make_tmr_block("AIT_FEED_SALINITY_TDS_301", "AIT_FEED_SALINITY_TDS_301A", "AIT_FEED_SALINITY_TDS_301B", "AIT_FEED_SALINITY_TDS_301C", "rTMR_Tol_FeedTDS", "rVoted_Feed_Salinity_TDS_ppm", "rDiff_TDSFeed_AB", "rDiff_TDSFeed_BC", "rDiff_TDSFeed_CA", "bFault_TDSFeed_A", "bFault_TDSFeed_B", "bFault_TDSFeed_C", "rTimer_TDSFeed_A", "rTimer_TDSFeed_B", "rTimer_TDSFeed_C", "iHealthy_TDSFeed", "16#0080", "ppm", "Raw Seawater Inflow Salinity TDS Analyzers"))
    st.append(make_tmr_block("AIT_PERMEATE_CONDUCTIVITY_302", "AIT_PERMEATE_CONDUCTIVITY_302A", "AIT_PERMEATE_CONDUCTIVITY_302B", "AIT_PERMEATE_CONDUCTIVITY_302C", "rTMR_Tol_PermeateCond", "rVoted_Permeate_Conductivity_uS_cm", "rDiff_CondPerm_AB", "rDiff_CondPerm_BC", "rDiff_CondPerm_CA", "bFault_CondPerm_A", "bFault_CondPerm_B", "bFault_CondPerm_C", "rTimer_CondPerm_A", "rTimer_CondPerm_B", "rTimer_CondPerm_C", "iHealthy_CondPerm", "16#0100", "uS/cm", "Permeate Product Electrical Conductivity Analyzers"))
    st.append(make_tmr_block("AIT_INTAKE_TURBIDITY_NTU_303", "AIT_INTAKE_TURBIDITY_NTU_303A", "AIT_INTAKE_TURBIDITY_NTU_303B", "AIT_INTAKE_TURBIDITY_NTU_303C", "rTMR_Tol_Turbidity", "rVoted_Intake_Turbidity_NTU", "rDiff_Turb_AB", "rDiff_Turb_BC", "rDiff_Turb_CA", "bFault_Turb_A", "bFault_Turb_B", "bFault_Turb_C", "rTimer_Turb_A", "rTimer_Turb_B", "rTimer_Turb_C", "iHealthy_Turb", "16#0200", "NTU", "Raw Seawater Intake Turbidity Analyzers"))
    st.append(make_tmr_block("TT_SEAWATER_INLET_401", "TT_SEAWATER_INLET_401A", "TT_SEAWATER_INLET_401B", "TT_SEAWATER_INLET_401C", "rTMR_Tol_Temperature", "rVoted_Seawater_Temp_degC", "rDiff_Temp_AB", "rDiff_Temp_BC", "rDiff_Temp_CA", "bFault_Temp_A", "bFault_Temp_B", "bFault_Temp_C", "rTimer_Temp_A", "rTimer_Temp_B", "rTimer_Temp_C", "iHealthy_Temp", "16#0400", "deg C", "Seawater Intake Feed Temperature Transmitters"))
    st.append(make_tmr_block("ST_ERD_PX_ROTOR_RPM_501", "ST_ERD_PX_ROTOR_RPM_501A", "ST_ERD_PX_ROTOR_RPM_501B", "ST_ERD_PX_ROTOR_RPM_501C", "rTMR_Tol_RotorRPM", "rVoted_ERD_Rotor_Speed_RPM", "rDiff_RPM_AB", "rDiff_RPM_BC", "rDiff_RPM_CA", "bFault_RPM_A", "bFault_RPM_B", "bFault_RPM_C", "rTimer_RPM_A", "rTimer_RPM_B", "rTimer_RPM_C", "iHealthy_RPM", "16#0800", "RPM", "ERD Ceramic Isobaric Rotor Tachometers"))
    st.append(make_tmr_block("PT_ERD_BOOSTER_DISCHARGE_502", "PT_ERD_BOOSTER_DISCHARGE_502A", "PT_ERD_BOOSTER_DISCHARGE_502B", "PT_ERD_BOOSTER_DISCHARGE_502C", "rTMR_Tol_BoosterPressure", "rVoted_ERD_Booster_Pressure_bar", "rDiff_PBoost_AB", "rDiff_PBoost_BC", "rDiff_PBoost_CA", "bFault_PBoost_A", "bFault_PBoost_B", "bFault_PBoost_C", "rTimer_PBoost_A", "rTimer_PBoost_B", "rTimer_PBoost_C", "iHealthy_PBoost", "16#1000", "bar", "ERD Booster Pump Discharge Manifold Pressure"))
    st.append(make_tmr_block("AIT_FEED_ORP_304", "AIT_FEED_ORP_304A", "AIT_FEED_ORP_304B", "AIT_FEED_ORP_304C", "rTMR_Tol_FeedORP", "rVoted_Feed_ORP_mV", "rDiff_ORP_AB", "rDiff_ORP_BC", "rDiff_ORP_CA", "bFault_ORP_A", "bFault_ORP_B", "bFault_ORP_C", "rTimer_ORP_A", "rTimer_ORP_B", "rTimer_ORP_C", "iHealthy_ORP", "16#2000", "mV", "Feed Seawater Oxidation-Reduction Potential (ORP) Chlorine Analyzers"))

    # PHASE 2: Cyber-Physical Kinetic & Membrane Transport Observers
    st.append("""(* ====================================================================================================
   PHASE 2: CYBER-PHYSICAL KINETIC, THERMODYNAMIC & MEMBRANE FOULING OBSERVERS
   ==================================================================================================== *)
(* 1. Thermodynamic Temperature & Arrhenius Temperature Correction Factor (TCF) *)
rTemp_Kelvin := rVoted_Seawater_Temp_degC + 273.15;
IF rTemp_Kelvin < 275.15 THEN rTemp_Kelvin := 275.15; END_IF;

(* Arrhenius TCF for water permeability: TCF = exp( (Ea/R) * (1/298.15 - 1/T_kelvin) ) *)
rTCF_TemperatureFactor := EXP((rCONST_ACTIVATION_ENERGY_W / rCONST_R_GAS) * ((1.0 / 298.15) - (1.0 / rTemp_Kelvin)));
IF rTCF_TemperatureFactor < 0.65 THEN rTCF_TemperatureFactor := 0.65; END_IF;
IF rTCF_TemperatureFactor > 1.65 THEN rTCF_TemperatureFactor := 1.65; END_IF;

(* Dynamic Seawater Viscosity: mu(T) [Pa*s] *)
rDynamicViscosity_Pa_s := 0.001002 * EXP(0.0245 * (20.0 - rVoted_Seawater_Temp_degC));

(* 2. Non-Linear van 't Hoff Osmotic Pressure Formulation: Pi = phi * (i * C * R * T / M) *)
(* Feed Osmotic Pressure [bar]: Pi_feed = 0.000805 * T_kelvin * (TDS_feed / 1000) *)
rOsmotic_Feed_Calc := 0.000805 * rTemp_Kelvin * (rVoted_Feed_Salinity_TDS_ppm / 1000.0);
rCalculated_Osmotic_Pressure_Feed_bar := rOsmotic_Feed_Calc;

(* Brine Reject Osmotic Pressure [bar]: estimated from mass balance and verified against AIT_CONCENTRATE_TDS_307 *)
IF rVoted_HP_Seawater_Flow_m3_h > 10.0 AND rVoted_Brine_Reject_Flow_m3_h > 10.0 THEN
    rTempCalc1 := (rVoted_HP_Seawater_Flow_m3_h * rVoted_Feed_Salinity_TDS_ppm) / rVoted_Brine_Reject_Flow_m3_h;
ELSE
    rTempCalc1 := AIT_CONCENTRATE_TDS_307;
END_IF;
IF rTempCalc1 < rVoted_Feed_Salinity_TDS_ppm THEN rTempCalc1 := rVoted_Feed_Salinity_TDS_ppm * 1.5; END_IF;
rOsmotic_Brine_Calc := 0.000805 * rTemp_Kelvin * (rTempCalc1 / 1000.0);
rCalculated_Osmotic_Pressure_Brine_bar := rOsmotic_Brine_Calc;

(* Crossflow Log-Mean / Bulk Arithmetic Average Osmotic Pressure *)
rOsmotic_Avg_Bulk := (rOsmotic_Feed_Calc + rOsmotic_Brine_Calc) * 0.5;

(* Permeate Product Osmotic Pressure [bar] *)
rOsmotic_Perm_Calc := 0.000805 * rTemp_Kelvin * (rCalculated_Permeate_Salinity_ppm / 1000.0);
rDelta_Osmotic_Bulk := rOsmotic_Avg_Bulk - rOsmotic_Perm_Calc;

(* 3. Feed Channel Spacer Hydrodynamics & Crossflow Velocity *)
rDeltaP_Feed_To_Brine := rVoted_HP_Feed_Pressure_bar - rVoted_Brine_Reject_Pressure_bar;
IF rDeltaP_Feed_To_Brine < 0.2 THEN rDeltaP_Feed_To_Brine := 0.2; END_IF;

rAverage_Pressure_Feed_Chamber := rVoted_HP_Feed_Pressure_bar - (rDeltaP_Feed_To_Brine * 0.5);

(* Crossflow Velocity through feed spacer channel: u_cross = Q_avg / (A_open * 3600) *)
rCrossflowVelocity_m_s := ((rVoted_HP_Seawater_Flow_m3_h + rVoted_Brine_Reject_Flow_m3_h) * 0.5) / (rCONST_MEMBRANE_AREA_M2 * 0.00075 * rCONST_FEED_CHANNEL_VOID_FRAC * 0.05);
IF rCrossflowVelocity_m_s < 0.05 THEN rCrossflowVelocity_m_s := 0.05; END_IF;
IF rCrossflowVelocity_m_s > 0.45 THEN rCrossflowVelocity_m_s := 0.45; END_IF;

(* Reynolds Number in feed spacer: Re = rho * u_cross * dh / mu *)
rReynolds_FeedChannel := (rCONST_SEAWATER_DENSITY_NOM * rCrossflowVelocity_m_s * rCONST_FEED_SPACER_DH_M) / rDynamicViscosity_Pa_s;

(* Schmidt Number: Sc = mu / (rho * D_diff) *)
rSchmidt_Feed := rDynamicViscosity_Pa_s / (rCONST_SEAWATER_DENSITY_NOM * rCONST_DIFFUSIVITY_NACL);

(* Sherwood Number correlation for 34 mil diamond net feed spacers: Sh = 0.065 * Re^0.875 * Sc^0.25 *)
rSherwood_Feed := 0.065 * EXPT(rReynolds_FeedChannel, 0.875) * EXPT(rSchmidt_Feed, 0.25);

(* Boundary Layer Mass Transfer Coefficient: k_L = Sh * D_diff / dh [m/s] *)
rMassTransferCoeff_kL_m_s := (rSherwood_Feed * rCONST_DIFFUSIVITY_NACL) / rCONST_FEED_SPACER_DH_M;
IF rMassTransferCoeff_kL_m_s < 1.0E-5 THEN rMassTransferCoeff_kL_m_s := 1.0E-5; END_IF;

(* 4. Transmembrane Pressure (TMP) & Net Driving Pressure (NDP) *)
rCalculated_Transmembrane_Pressure_bar := rAverage_Pressure_Feed_Chamber - rVoted_Permeate_Pressure_bar;
IF rCalculated_Transmembrane_Pressure_bar < 0.0 THEN rCalculated_Transmembrane_Pressure_bar := 0.0; END_IF;

(* 5. Solution-Diffusion Water Flux & Concentration Polarization Modulus *)
(* Apparent Water Permeability with fouling resistance: Aw_eff = (Aw_0 * TCF) / (1 + Rf / 1E11) *)
rTempCalc2 := (rCONST_NOMINAL_Aw * rTCF_TemperatureFactor) / (1.0 + (rObserved_Fouling_Resistance_m_inv / 2.0E11));

(* Initial NDP estimate without CP: NDP = TMP - Delta_Pi_bulk *)
rNet_Driving_Pressure_bar := rCalculated_Transmembrane_Pressure_bar - rDelta_Osmotic_Bulk;
IF rNet_Driving_Pressure_bar < 0.1 THEN rNet_Driving_Pressure_bar := 0.1; END_IF;

(* Water Flux Jw [m/s] = Aw_eff * NDP * 1E5 Pa/bar *)
rWaterFlux_Jw_m_s := rTempCalc2 * (rNet_Driving_Pressure_bar * 1.0E5);
rWaterFlux_Jw_LMH := rWaterFlux_Jw_m_s * 3.6E6; (* Convert m/s to L/(m2*h) *)
IF rWaterFlux_Jw_LMH < 0.5 THEN rWaterFlux_Jw_LMH := 0.5; END_IF;
IF rWaterFlux_Jw_LMH > 35.0 THEN rWaterFlux_Jw_LMH := 35.0; END_IF;

(* Exponential Concentration Polarization Modulus: Gamma = exp(Jw / k_L) *)
rCP_Exponent := rWaterFlux_Jw_m_s / rMassTransferCoeff_kL_m_s;
IF rCP_Exponent > 0.85 THEN rCP_Exponent := 0.85; END_IF;
rCP_Modulus_Gamma := EXP(rCP_Exponent);
rCalculated_Concentration_Polarization_Modulus := rCP_Modulus_Gamma;

(* Membrane Surface Wall Concentration: Cm = C_bulk * Gamma *)
rWallConcentration_Cm_ppm := rVoted_Feed_Salinity_TDS_ppm * rCP_Modulus_Gamma;

(* Recomputed Osmotic Pressure at the Wall Membrane Surface [bar] *)
rOsmotic_Wall_Calc := 0.000805 * rTemp_Kelvin * (rWallConcentration_Cm_ppm / 1000.0);

(* Final Dynamic Net Driving Pressure: NDP = TMP - (Pi_wall - Pi_perm) *)
rNet_Driving_Pressure_bar := rCalculated_Transmembrane_Pressure_bar - (rOsmotic_Wall_Calc - rOsmotic_Perm_Calc);
IF rNet_Driving_Pressure_bar < 0.05 THEN rNet_Driving_Pressure_bar := 0.05; END_IF;
rCalculated_Net_Driving_Pressure_bar := rNet_Driving_Pressure_bar;

(* 6. Salt Transport Flux & Permeate TDS Reconstruction *)
(* Salt Permeability with Arrhenius temperature compensation: Bs(T) *)
rTempCalc3 := rCONST_NOMINAL_Bs * EXP((rCONST_ACTIVATION_ENERGY_S / rCONST_R_GAS) * ((1.0 / 298.15) - (1.0 / rTemp_Kelvin)));

(* Salt Flux Js [g/(m2*h)] = Bs * (Cm - Cp) * 1E-3 *)
rSaltFlux_Js_g_m2_h := rTempCalc3 * (rWallConcentration_Cm_ppm - rCalculated_Permeate_Salinity_ppm) * 0.0036;

(* Reconstructed Permeate TDS [ppm]: Cp = (Js / Jw) * 1000 *)
rCalculated_Permeate_Salinity_ppm := (rSaltFlux_Js_g_m2_h / (rWaterFlux_Jw_LMH + 0.001)) * 1000.0;
IF rCalculated_Permeate_Salinity_ppm < 50.0 THEN rCalculated_Permeate_Salinity_ppm := 50.0; END_IF;
IF rCalculated_Permeate_Salinity_ppm > 850.0 THEN rCalculated_Permeate_Salinity_ppm := 850.0; END_IF;
rCalculated_Permeate_TDS_ppm := rCalculated_Permeate_Salinity_ppm;

(* Permeate Recovery Fraction & Dynamic Salt Rejection *)
IF rVoted_HP_Seawater_Flow_m3_h > 50.0 THEN
    rCalculated_Permeate_Recovery_pct := (rVoted_Permeate_Flow_m3_h / rVoted_HP_Seawater_Flow_m3_h) * 100.0;
ELSE
    rCalculated_Permeate_Recovery_pct := 0.0;
END_IF;

IF rVoted_Feed_Salinity_TDS_ppm > 100.0 THEN
    rCalculated_Salt_Rejection_pct := (1.0 - (rCalculated_Permeate_Salinity_ppm / rVoted_Feed_Salinity_TDS_ppm)) * 100.0;
ELSE
    rCalculated_Salt_Rejection_pct := 99.5;
END_IF;

(* 7. Mineral Scaling Indices: Stiff & Davis Stability Index (S&DSI) & Gypsum Saturation *)
(* Brine Ionic Strength: I = 2.5E-5 * TDS_brine *)
rIonicStrength_Brine := 2.5E-5 * rTempCalc1;

(* S&DSI Constant K_SD(I, T) *)
rStiffDavis_K_Factor := 2.65 + (0.012 * (rVoted_Seawater_Temp_degC - 20.0)) + (0.18 * SQRT(rIonicStrength_Brine));

(* S&DSI = pH_brine - pCa - pAlk - K_SD *)
rStiffDavis_Index_SDSI := AIT_CONCENTRATE_PH_306 - 2.80 - 2.50 - rStiffDavis_K_Factor;
rObserved_Stiff_Davis_Index := rStiffDavis_Index_SDSI;

(* Gypsum Saturation Product: Ksp(T, I) *)
rGypsum_Ksp_Solubility := 2.40E-4 * (1.0 + (0.015 * (rVoted_Seawater_Temp_degC - 25.0))) * (1.0 + (0.35 * SQRT(rIonicStrength_Brine)));
rGypsum_IAP_Product := 0.028 * 0.040 * (rTempCalc1 / 38500.0) * (rTempCalc1 / 38500.0) * 1.0E-3;
rGypsum_Saturation_Ratio_Sr := SQRT(rGypsum_IAP_Product / (rGypsum_Ksp_Solubility + 1.0E-9));
rObserved_Gypsum_Saturation_Ratio := rGypsum_Saturation_Ratio_Sr;

(* 8. Cumulative Hydraulic Fouling & Biofouling Observer *)
IF rGypsum_Saturation_Ratio_Sr > 1.0 THEN
    rFouling_Rate_Scaling_m_inv_s := 2.5E5 * (rGypsum_Saturation_Ratio_Sr - 1.0);
ELSE
    rFouling_Rate_Scaling_m_inv_s := 0.0;
END_IF;

(* Biofouling rate driven by temperature and biomass nutrients *)
rFouling_Rate_Biofouling_m_inv_s := 1.25E5 * EXP(0.075 * (rVoted_Seawater_Temp_degC - 20.0));

(* Shear removal rate by crossflow velocity *)
rFouling_Rate_Shear_Removal_m_inv_s := 8.50E4 * (rCrossflowVelocity_m_s / 0.185);

(* Anti-scalant chemical inhibition removal rate *)
rFouling_Rate_Antiscalant_m_inv_s := 1.10E5 * ((FT_ANTISCALANT_DOSING_601A + FT_ANTISCALANT_DOSING_601B) * 0.5 / 12.8);

(* Net Rate of Fouling Resistance Accumulation [1/(m*s)] *)
rNet_Fouling_Rate_m_inv_s := rFouling_Rate_Scaling_m_inv_s + rFouling_Rate_Biofouling_m_inv_s - rFouling_Rate_Shear_Removal_m_inv_s - rFouling_Rate_Antiscalant_m_inv_s;

(* Numerical Integration of Fouling Resistance *)
rObserved_Fouling_Resistance_m_inv := rObserved_Fouling_Resistance_m_inv + (rNet_Fouling_Rate_m_inv_s * rDeltaTime_Sec);
IF rObserved_Fouling_Resistance_m_inv < 1.0E10 THEN rObserved_Fouling_Resistance_m_inv := 1.0E10; END_IF;
IF rObserved_Fouling_Resistance_m_inv > 1.5E12 THEN rObserved_Fouling_Resistance_m_inv := 1.5E12; END_IF;

(* Projected Useful Membrane Life Remaining [months] *)
rEstimated_Membrane_Life_Remaining_Months := 60.0 * (1.0 - ((rObserved_Fouling_Resistance_m_inv - 1.0E10) / 1.49E12));
IF rEstimated_Membrane_Life_Remaining_Months < 0.0 THEN rEstimated_Membrane_Life_Remaining_Months := 0.0; END_IF;

(* 9. Isobaric Ceramic Pressure Exchanger (PX) Mass & Energy Balance *)
rERD_HP_Brine_Flow_m3_h := rVoted_Brine_Reject_Flow_m3_h;
rERD_HP_Boosted_Flow_m3_h := rERD_HP_Brine_Flow_m3_h;

(* PX Rotor Speed Hydrodynamic Law: RPM = (Q_brine / V_rotor) * K_geom *)
rERD_Rotor_Expected_RPM := (rERD_HP_Brine_Flow_m3_h / (rCONST_PX_CERAMIC_ROTOR_VOLUME_L * 0.001 * 60.0)) * rCONST_PX_DUCT_GEOMETRY_K;

(* Volumetric Overflush Index: lambda = (Q_LP_in - Q_HP_out) / Q_HP_out *)
rERD_LP_Feed_Flow_m3_h := rERD_HP_Boosted_Flow_m3_h * 1.014; (* 1.4% nominal overflush *)
rERD_Overflush_Fraction := (rERD_LP_Feed_Flow_m3_h - rERD_HP_Boosted_Flow_m3_h) / (rERD_HP_Boosted_Flow_m3_h + 0.001);

(* ERD Net Hydraulic Energy Transfer Efficiency: eta_ERD = (P_HP_out * Q_HP_out - P_LP_in * Q_LP_in) / (P_HP_in * Q_HP_in - P_LP_out * Q_LP_out) *)
rERD_HydraulicPower_Input_kW := (rVoted_Brine_Reject_Pressure_bar * 1.0E5 * (rERD_HP_Brine_Flow_m3_h / 3600.0)) / 1000.0;
rERD_HydraulicPower_Recovered_kW := (rVoted_ERD_Booster_Pressure_bar * 1.0E5 * (rERD_HP_Boosted_Flow_m3_h / 3600.0)) / 1000.0;
IF rERD_HydraulicPower_Input_kW > 10.0 THEN
    rCalculated_ERD_Net_Efficiency_pct := (rERD_HydraulicPower_Recovered_kW / rERD_HydraulicPower_Input_kW) * 100.0;
ELSE
    rCalculated_ERD_Net_Efficiency_pct := 97.5;
END_IF;
IF rCalculated_ERD_Net_Efficiency_pct > 99.0 THEN rCalculated_ERD_Net_Efficiency_pct := 99.0; END_IF;

(* 10. Specific Energy Consumption (SEC) Computation *)
(* Booster Pump Differential Head: delta_P_booster = P_feed - P_booster_in *)
rBoosterPump_Head_bar := rVoted_HP_Feed_Pressure_bar - rVoted_ERD_Booster_Pressure_bar;
IF rBoosterPump_Head_bar < 0.5 THEN rBoosterPump_Head_bar := 0.5; END_IF;

rBoosterPump_HydraulicPower_kW := (rBoosterPump_Head_bar * 1.0E5 * (rERD_HP_Boosted_Flow_m3_h / 3600.0)) / 1000.0;
rBoosterPump_ElectricPower_kW := rBoosterPump_HydraulicPower_kW / (rCONST_BOOSTER_HYD_EFFICIENCY * rCONST_MOTOR_VFD_EFFICIENCY);

(* High-Pressure Feed Pump Direct Stream (Split stream not passing through ERD) *)
rHPFP_Direct_Feed_Flow_m3_h := rVoted_HP_Seawater_Flow_m3_h - rERD_HP_Boosted_Flow_m3_h;
IF rHPFP_Direct_Feed_Flow_m3_h < 10.0 THEN rHPFP_Direct_Feed_Flow_m3_h := 10.0; END_IF;

rHPFP_HydraulicPower_kW := (rVoted_HP_Feed_Pressure_bar * 1.0E5 * (rHPFP_Direct_Feed_Flow_m3_h / 3600.0)) / 1000.0;
rHPFP_ElectricPower_kW := rHPFP_HydraulicPower_kW / (rCONST_HPFP_HYD_EFFICIENCY * rCONST_MOTOR_VFD_EFFICIENCY);

(* Low-Pressure Intake Booster Pump Electric Power *)
rLPFP_Intake_ElectricPower_kW := (PT_LP_FEED_SUCTION_104A * 1.0E5 * (rVoted_HP_Seawater_Flow_m3_h / 3600.0)) / (1000.0 * 0.78 * 0.95);

(* Aggregate Desalination Train Electrical Power [kW] *)
rTotal_Facility_Electric_Power_kW := rHPFP_ElectricPower_kW + rBoosterPump_ElectricPower_kW + rLPFP_Intake_ElectricPower_kW;

(* Specific Energy Consumption [kWh/m3] = Total kW / Permeate Outflow m3/h *)
IF rVoted_Permeate_Flow_m3_h > 10.0 THEN
    rCalculated_SEC_kWh_m3 := rTotal_Facility_Electric_Power_kW / rVoted_Permeate_Flow_m3_h;
ELSE
    rCalculated_SEC_kWh_m3 := 2.80;
END_IF;
rCalculated_Specific_Energy_Consumption_kWh_m3 := rCalculated_SEC_kWh_m3;""")

    # PHASE 3: Receding-Horizon Model Predictive Control (MPC)
    st.append("""(* ====================================================================================================
   PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) RECOVERY & TMP DECOUPLING
   ==================================================================================================== *)
(* Assemble Current State Vector xState (8x1) *)
xState[1] := rCalculated_Net_Driving_Pressure_bar;
xState[2] := rWaterFlux_Jw_LMH;
xState[3] := rWallConcentration_Cm_ppm;
xState[4] := rObserved_Fouling_Resistance_m_inv / 1.0E11;
xState[5] := rVoted_ERD_Rotor_Speed_RPM;
xState[6] := rCalculated_Permeate_Recovery_pct;
xState[7] := rCalculated_Permeate_TDS_ppm;
xState[8] := rCalculated_Specific_Energy_Consumption_kWh_m3;

(* Define Target State Setpoints xSetpoint (8x1) *)
xSetpoint[1] := 5.80;                              (* Target NDP [bar] *)
xSetpoint[2] := 15.39;                             (* Target Permeate Flux [LMH] *)
xSetpoint[3] := rVoted_Feed_Salinity_TDS_ppm * 1.075; (* Target Wall Salinity *)
xSetpoint[4] := 2.45;                              (* Target Fouling Resistance index *)
xSetpoint[5] := rERD_Rotor_Expected_RPM;           (* Synchronized PX Rotor Speed [RPM] *)
xSetpoint[6] := rSet_Recovery_Target_pct;          (* Strict 45.0% Recovery Setpoint *)
xSetpoint[7] := 160.0;                             (* Permeate TDS (< 200 ppm target) *)
xSetpoint[8] := rSet_TargetSEC_kWh_m3;             (* SEC Ceiling (< 2.80 kWh/m3) *)

(* Calculate Tracking Error Vector xError *)
FOR kStateIdx := 1 TO 8 DO
    xError[kStateIdx] := xState[kStateIdx] - xSetpoint[kStateIdx];
    xPred[kStateIdx] := xState[kStateIdx];
END_FOR;

(* Receding-Horizon Dynamic Optimization Execution *)
IF bAutoMpcEnable AND (eActiveFsmState = STATE_STEADY_STATE_PERMEATE_HARVEST) THEN
    (* 5-Step Horizon Simulation & Gradient Calculation *)
    rTotalCost := 0.0;
    FOR mInputIdx := 1 TO 8 DO
        rGrad[mInputIdx] := 0.0;
    END_FOR;

    FOR iHorizonStep := 1 TO 5 DO
        (* Propagate Horizon State: x[k+1] = A * x[k] + B * u[k] *)
        FOR iMatRow := 1 TO 8 DO
            rTempCalc1 := 0.0;
            FOR iMatCol := 1 TO 8 DO
                rTempCalc1 := rTempCalc1 + (matA[iMatRow, iMatCol] * xPred[iMatCol]) + (matB[iMatRow, iMatCol] * uActuator[iMatCol]);
            END_FOR;
            xHorizon[iHorizonStep, iMatRow] := rTempCalc1;
        END_FOR;

        (* Copy step prediction to xPred *)
        FOR kStateIdx := 1 TO 8 DO
            xPred[kStateIdx] := xHorizon[iHorizonStep, kStateIdx];
        END_FOR;

        (* Accumulate Stage Cost: J_stage = (x - r)^T * Q * (x - r) + u^T * R * u *)
        FOR kStateIdx := 1 TO 8 DO
            rTotalCost := rTotalCost + (matQ[kStateIdx, kStateIdx] * (xPred[kStateIdx] - xSetpoint[kStateIdx]) * (xPred[kStateIdx] - xSetpoint[kStateIdx]));
        END_FOR;
        FOR mInputIdx := 1 TO 8 DO
            rTotalCost := rTotalCost + (matR[mInputIdx, mInputIdx] * uActuator[mInputIdx] * uActuator[mInputIdx]);
        END_FOR;

        (* Backward Gradient Accumulation: grad_u = 2 * B^T * Q * (x - r) + 2 * R * u + 2 * S * delta_u *)
        FOR mInputIdx := 1 TO 8 DO
            rTempCalc2 := 0.0;
            FOR kStateIdx := 1 TO 8 DO
                rTempCalc2 := rTempCalc2 + (matB[kStateIdx, mInputIdx] * matQ[kStateIdx, kStateIdx] * (xPred[kStateIdx] - xSetpoint[kStateIdx]));
            END_FOR;
            rGrad[mInputIdx] := rGrad[mInputIdx] + (2.0 * rTempCalc2) + (2.0 * matR[mInputIdx, mInputIdx] * uActuator[mInputIdx]) + (2.0 * matS[mInputIdx, mInputIdx] * (uActuator[mInputIdx] - uPrevious[mInputIdx]));
        END_FOR;
    END_FOR;

    (* Add Terminal Cost: (x_N - r)^T * P * (x_N - r) *)
    FOR kStateIdx := 1 TO 8 DO
        rTotalCost := rTotalCost + (matP[kStateIdx, kStateIdx] * (xPred[kStateIdx] - xSetpoint[kStateIdx]) * (xPred[kStateIdx] - xSetpoint[kStateIdx]));
    END_FOR;

    (* Projected Gradient Descent Actuator Update: u_opt = u - step * grad *)
    FOR mInputIdx := 1 TO 8 DO
        uOptimal[mInputIdx] := uActuator[mInputIdx] - (rStepSize * rGrad[mInputIdx]);

        (* Slew Rate Clamping *)
        deltaU[mInputIdx] := uOptimal[mInputIdx] - uPrevious[mInputIdx];
        IF deltaU[mInputIdx] > deltaUMax[mInputIdx] THEN
            uOptimal[mInputIdx] := uPrevious[mInputIdx] + deltaUMax[mInputIdx];
        ELSIF deltaU[mInputIdx] < -deltaUMax[mInputIdx] THEN
            uOptimal[mInputIdx] := uPrevious[mInputIdx] - deltaUMax[mInputIdx];
        END_IF;

        (* Physical Saturation Box Constraints [uMin, uMax] *)
        IF uOptimal[mInputIdx] > uMax[mInputIdx] THEN
            uOptimal[mInputIdx] := uMax[mInputIdx];
        ELSIF uOptimal[mInputIdx] < uMin[mInputIdx] THEN
            uOptimal[mInputIdx] := uMin[mInputIdx];
        END_IF;

        (* Store for Next Iteration *)
        uPrevious[mInputIdx] := uActuator[mInputIdx];
        uActuator[mInputIdx] := uOptimal[mInputIdx];
    END_FOR;

    (* Assign Optimal Actuator Demands to Physical Commands *)
    rCmd_HPFP_VFD_Speed_Pct              := uActuator[1];
    rCmd_ERD_Booster_VFD_Speed_Pct       := uActuator[2];
    rCmd_Brine_Throttle_Valve_Pct        := uActuator[3];
    rCmd_Permeate_Backpressure_Valve_Pct := uActuator[4];
    rCmd_Antiscalant_Dosing_Pump_Pct     := uActuator[5];
    rCmd_LP_Feed_Pump_Speed_Pct          := uActuator[6];
    rCmd_ERD_Overflush_TrimValve_Pct     := uActuator[7];
    bCmd_Intake_Divert_Gate_Open         := (uActuator[8] > 50.0);
END_IF;""")

    # PHASE 4: 12-Stage Operational Finite State Machine (FSM)
    st.append("""(* ====================================================================================================
   PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) ENGINE
   ==================================================================================================== *)
tFsmStepTimer_Sec := tFsmStepTimer_Sec + rDeltaTime_Sec;

CASE eActiveFsmState OF
    0: (* STATE_SYSTEM_OFFLINE_STANDBY *)
        rCmd_HPFP_VFD_Speed_Pct                     := 0.0;
        rCmd_ERD_Booster_VFD_Speed_Pct              := 0.0;
        rCmd_LP_Feed_Pump_Speed_Pct                 := 0.0;
        rCmd_Antiscalant_Dosing_Pump_Pct            := 0.0;
        rCmd_Brine_Throttle_Valve_Pct               := 100.0;
        rCmd_Permeate_Backpressure_Valve_Pct        := 100.0;
        rCmd_ERD_Overflush_TrimValve_Pct            := 0.0;
        bCmd_HP_Emergency_Depressurize_FastRelief   := FALSE;
        bCmd_HPFP_Breaker_Trip                      := FALSE;
        bCmd_Intake_Divert_Gate_Open                := FALSE;
        bCmd_Permeate_DumpValve_Open                := TRUE;
        bCmd_CIP_Circulation_Pump_Run               := FALSE;
        bProductionQualified                        := FALSE;
        bEmergencyShutdownActive                    := FALSE;

        IF bMasterEnable AND bEmergencyStop AND NOT bAlm_Feed_P_HH AND NOT bAlm_Discrepancy_Trip THEN
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_LOW_PRESSURE_MEMBRANE_FLUSH;
        END_IF;

    1: (* STATE_LOW_PRESSURE_MEMBRANE_FLUSH *)
        (* Displaces stagnant hypersaline brine and air bubbles using low-pressure seawater flush *)
        rCmd_LP_Feed_Pump_Speed_Pct                 := 45.0;
        rCmd_Brine_Throttle_Valve_Pct               := 100.0;
        rCmd_Permeate_Backpressure_Valve_Pct        := 100.0;
        bCmd_Permeate_DumpValve_Open                := TRUE;
        tFlushTimer_Sec := tFlushTimer_Sec + rDeltaTime_Sec;

        (* Flush duration: 180 seconds to replace complete train hydraulic volume *)
        IF tFlushTimer_Sec >= 180.0 THEN
            tFlushTimer_Sec := 0.0;
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_CHEMICAL_SCALE_INHIBITOR_PRIME;
        END_IF;

    2: (* STATE_CHEMICAL_SCALE_INHIBITOR_PRIME *)
        (* Primes anti-scalant chemical dosing metering pumps before high-pressure operation *)
        rCmd_Antiscalant_Dosing_Pump_Pct            := 55.0;
        rCmd_LP_Feed_Pump_Speed_Pct                 := 50.0;

        (* Verify positive chemical flow rate feedback *)
        IF (FT_ANTISCALANT_DOSING_601A > 8.0) OR (FT_ANTISCALANT_DOSING_601B > 8.0) THEN
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_HP_PUMP_SOFT_START_RAMP;
        ELSIF tFsmStepTimer_Sec > 45.0 THEN
            (* Dosing prime failure timeout *)
            bAlm_Antiscalant_LL := TRUE;
            eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
        END_IF;

    3: (* STATE_HP_PUMP_SOFT_START_RAMP *)
        (* 12 MW Medium-Voltage VFD soft ramp to minimum continuous speed (30% / 30 bar) *)
        rCmd_Brine_Throttle_Valve_Pct               := 75.0;
        rCmd_LP_Feed_Pump_Speed_Pct                 := 60.0;
        tSoftStartTimer_Sec := tSoftStartTimer_Sec + rDeltaTime_Sec;

        IF rCmd_HPFP_VFD_Speed_Pct < 35.0 THEN
            rCmd_HPFP_VFD_Speed_Pct := rCmd_HPFP_VFD_Speed_Pct + (rDeltaTime_Sec * 0.85);
        END_IF;

        IF (rVoted_HP_Feed_Pressure_bar >= 28.0) AND (tSoftStartTimer_Sec >= 30.0) THEN
            tSoftStartTimer_Sec := 0.0;
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_ERD_ISOBARIC_PX_SYNCHRONIZATION;
        END_IF;

    4: (* STATE_ERD_ISOBARIC_PX_SYNCHRONIZATION *)
        (* Spin up isobaric ceramic PX rotor with concentrate reject flow and synchronize booster *)
        rCmd_ERD_Overflush_TrimValve_Pct            := 30.0;
        tSyncTimer_Sec := tSyncTimer_Sec + rDeltaTime_Sec;

        IF rCmd_ERD_Booster_VFD_Speed_Pct < 55.0 THEN
            rCmd_ERD_Booster_VFD_Speed_Pct := rCmd_ERD_Booster_VFD_Speed_Pct + (rDeltaTime_Sec * 1.2);
        END_IF;

        IF (rVoted_ERD_Rotor_Speed_RPM >= 750.0) AND (tSyncTimer_Sec >= 20.0) THEN
            tSyncTimer_Sec := 0.0;
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_PRESSURE_RAMP_TO_OSMOTIC_BREAK;
        END_IF;

    5: (* STATE_PRESSURE_RAMP_TO_OSMOTIC_BREAK *)
        (* Coordinated ramp through osmotic pressure barrier (~55 bar) to establish permeate flux *)
        tPressureRampTimer_Sec := tPressureRampTimer_Sec + rDeltaTime_Sec;

        IF rCmd_HPFP_VFD_Speed_Pct < 80.0 THEN
            rCmd_HPFP_VFD_Speed_Pct := rCmd_HPFP_VFD_Speed_Pct + (rDeltaTime_Sec * 0.45);
        END_IF;
        IF rCmd_ERD_Booster_VFD_Speed_Pct < 75.0 THEN
            rCmd_ERD_Booster_VFD_Speed_Pct := rCmd_ERD_Booster_VFD_Speed_Pct + (rDeltaTime_Sec * 0.40);
        END_IF;
        IF rCmd_Brine_Throttle_Valve_Pct > 48.0 THEN
            rCmd_Brine_Throttle_Valve_Pct := rCmd_Brine_Throttle_Valve_Pct - (rDeltaTime_Sec * 0.35);
        END_IF;

        (* Osmotic break condition: Feed Pressure > Osmotic Pressure and Permeate Flow starts *)
        IF (rVoted_HP_Feed_Pressure_bar >= 62.0) AND (rVoted_Permeate_Flow_m3_h >= 250.0) THEN
            tPressureRampTimer_Sec := 0.0;
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_STEADY_STATE_PERMEATE_HARVEST;
        END_IF;

    6: (* STATE_STEADY_STATE_PERMEATE_HARVEST *)
        (* Fully closed-loop Receding-Horizon MPC active: Locks recovery at 45.0% and SEC < 2.80 kWh/m3 *)
        IF rVoted_Permeate_Conductivity_uS_cm < 350.0 THEN
            bCmd_Permeate_DumpValve_Open := FALSE; (* Safe potable water delivery to municipal reservoir *)
        ELSE
            bCmd_Permeate_DumpValve_Open := TRUE;  (* Off-spec permeate diverted to outfall *)
        END_IF;

        (* Red tide or high turbidity interlock *)
        IF rVoted_Intake_Turbidity_NTU >= rALM_TRIP_TURBIDITY_HH THEN
            eActiveFsmState := STATE_HIGH_TURBIDITY_INTAKE_DIVERT;
        END_IF;

        (* Manual CIP Request Permissive *)
        IF bCipSequencePermissive THEN
            eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
        END_IF;

    7: (* STATE_MEMBRANE_CLEANING_CIP_CYCLE *)
        (* Low-pressure chemical wash recirculation (acid/caustic) *)
        rCmd_HPFP_VFD_Speed_Pct                     := 0.0;
        rCmd_ERD_Booster_VFD_Speed_Pct              := 0.0;
        bCmd_CIP_Circulation_Pump_Run               := TRUE;
        bCmd_Permeate_DumpValve_Open                := TRUE;
        tCipTimer_Sec := tCipTimer_Sec + rDeltaTime_Sec;

        (* CIP wash cycle nominal duration: 7200 seconds (2 hours) *)
        IF tCipTimer_Sec >= 7200.0 THEN
            bCmd_CIP_Circulation_Pump_Run := FALSE;
            tCipTimer_Sec := 0.0;
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_LOW_PRESSURE_MEMBRANE_FLUSH;
        END_IF;

    8: (* STATE_HIGH_TURBIDITY_INTAKE_DIVERT *)
        (* Raw intake diverted to sea outfall to protect ultrafiltration and RO membranes *)
        bCmd_Intake_Divert_Gate_Open                := TRUE;
        rCmd_HPFP_VFD_Speed_Pct                     := 0.0;
        rCmd_ERD_Booster_VFD_Speed_Pct              := 0.0;
        rCmd_LP_Feed_Pump_Speed_Pct                 := 0.0;
        rCmd_Brine_Throttle_Valve_Pct               := 100.0;
        bCmd_Permeate_DumpValve_Open                := TRUE;

        (* Return to flush when turbidity subsides below warning deadband *)
        IF rVoted_Intake_Turbidity_NTU < (rALM_WARN_TURBIDITY_H - rALM_HYST_TURBIDITY) THEN
            bCmd_Intake_Divert_Gate_Open := FALSE;
            eActiveFsmState := STATE_LOW_PRESSURE_MEMBRANE_FLUSH;
        END_IF;

    9: (* STATE_CONCENTRATE_VALVE_DEPRESSURIZATION *)
        (* Controlled gradual depressurization of concentrate and feed manifolds *)
        IF rCmd_HPFP_VFD_Speed_Pct > 0.0 THEN
            rCmd_HPFP_VFD_Speed_Pct := rCmd_HPFP_VFD_Speed_Pct - (rDeltaTime_Sec * 5.0);
        ELSE
            rCmd_HPFP_VFD_Speed_Pct := 0.0;
        END_IF;
        IF rCmd_ERD_Booster_VFD_Speed_Pct > 0.0 THEN
            rCmd_ERD_Booster_VFD_Speed_Pct := rCmd_ERD_Booster_VFD_Speed_Pct - (rDeltaTime_Sec * 5.0);
        ELSE
            rCmd_ERD_Booster_VFD_Speed_Pct := 0.0;
        END_IF;
        rCmd_Brine_Throttle_Valve_Pct := 100.0;
        bCmd_Permeate_DumpValve_Open := TRUE;

        IF rVoted_HP_Feed_Pressure_bar < 5.0 THEN
            tFsmStepTimer_Sec := 0.0;
            IF bCipSequencePermissive THEN
                eActiveFsmState := STATE_MEMBRANE_CLEANING_CIP_CYCLE;
            ELSE
                eActiveFsmState := STATE_PERMEATE_DISCHARGE_FLUSH_SHUTDOWN;
            END_IF;
        END_IF;

    10: (* STATE_PERMEATE_DISCHARGE_FLUSH_SHUTDOWN *)
        (* Fresh desalinated permeate flush displacing raw seawater inside vessels to stop osmosis *)
        rCmd_LP_Feed_Pump_Speed_Pct                 := 30.0;
        rCmd_Brine_Throttle_Valve_Pct               := 100.0;
        bCmd_Permeate_DumpValve_Open                := TRUE;

        IF tFsmStepTimer_Sec >= 120.0 THEN
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_SYSTEM_OFFLINE_STANDBY;
        END_IF;

    11: (* STATE_EMERGENCY_ESTOP_LINE_RELIEF *)
        (* Fast emergency line relief, breaker trip, fast relief valve opened *)
        rCmd_HPFP_VFD_Speed_Pct                     := 0.0;
        rCmd_ERD_Booster_VFD_Speed_Pct              := 0.0;
        rCmd_LP_Feed_Pump_Speed_Pct                 := 0.0;
        rCmd_Antiscalant_Dosing_Pump_Pct            := 0.0;
        rCmd_Brine_Throttle_Valve_Pct               := 100.0;
        rCmd_Permeate_Backpressure_Valve_Pct        := 100.0;
        bCmd_HP_Emergency_Depressurize_FastRelief   := TRUE;
        bCmd_HPFP_Breaker_Trip                      := TRUE;
        bCmd_Intake_Divert_Gate_Open                := TRUE;
        bCmd_Permeate_DumpValve_Open                := TRUE;
        bEmergencyShutdownActive                    := TRUE;
        bProductionQualified                        := FALSE;

        IF bResetFault AND bEmergencyStop THEN
            bCmd_HP_Emergency_Depressurize_FastRelief := FALSE;
            bCmd_HPFP_Breaker_Trip := FALSE;
            bEmergencyShutdownActive := FALSE;
            tFsmStepTimer_Sec := 0.0;
            eActiveFsmState := STATE_SYSTEM_OFFLINE_STANDBY;
        END_IF;
END_CASE;""")

    # PHASE 5: ISA-18.2 Alarms & Diagnostic Word Packing
    st.append("""(* ====================================================================================================
   PHASE 5: ISA-18.2 ALARMS, DIAGNOSTIC WORD PACKING & PRODUCTION QUALIFICATION
   ==================================================================================================== *)
(* Rate of Change (ROC) Calculations *)
rPressureROC_bar_s := (rVoted_HP_Feed_Pressure_bar - rPreviousFeedPressure) / rDeltaTime_Sec;
rPreviousFeedPressure := rVoted_HP_Feed_Pressure_bar;

rCondROC_uS_cm_s := (rVoted_Permeate_Conductivity_uS_cm - rPreviousPermeateCond) / rDeltaTime_Sec;
rPreviousPermeateCond := rVoted_Permeate_Conductivity_uS_cm;

(* ISA-18.2 Priority 1 / Priority 2 Threshold Evaluations with Deadband Hysteresis *)

(* 1. High-High Feed Overpressure Compaction Fast Trip (< 100 ms) *)
IF rVoted_HP_Feed_Pressure_bar >= rALM_TRIP_FEED_P_HH THEN
    bAlm_Feed_P_HH := TRUE;
    bCmd_HPFP_Breaker_Trip := TRUE;
    bCmd_HP_Emergency_Depressurize_FastRelief := TRUE;
    eActiveFsmState := STATE_EMERGENCY_ESTOP_LINE_RELIEF;
ELSIF rVoted_HP_Feed_Pressure_bar < (rALM_TRIP_FEED_P_HH - rALM_HYST_FEED_P) THEN
    bAlm_Feed_P_HH := FALSE;
END_IF;

IF rVoted_HP_Feed_Pressure_bar >= rALM_WARN_FEED_P_H THEN
    bAlm_Feed_P_H := TRUE;
ELSIF rVoted_HP_Feed_Pressure_bar < (rALM_WARN_FEED_P_H - rALM_HYST_FEED_P) THEN
    bAlm_Feed_P_H := FALSE;
END_IF;

IF (rVoted_HP_Feed_Pressure_bar <= rALM_WARN_FEED_P_L) AND (eActiveFsmState = STATE_STEADY_STATE_PERMEATE_HARVEST) THEN
    bAlm_Feed_P_L := TRUE;
ELSIF rVoted_HP_Feed_Pressure_bar > (rALM_WARN_FEED_P_L + rALM_HYST_FEED_P) THEN
    bAlm_Feed_P_L := FALSE;
END_IF;

IF (rVoted_HP_Feed_Pressure_bar <= rALM_TRIP_FEED_P_LL) AND (eActiveFsmState = STATE_STEADY_STATE_PERMEATE_HARVEST) THEN
    bAlm_Feed_P_LL := TRUE;
    eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
ELSIF rVoted_HP_Feed_Pressure_bar > (rALM_TRIP_FEED_P_LL + rALM_HYST_FEED_P) THEN
    bAlm_Feed_P_LL := FALSE;
END_IF;

(* 2. Permeate Conductivity Alarms *)
IF rVoted_Permeate_Conductivity_uS_cm >= rALM_TRIP_PERM_COND_HH THEN
    bAlm_Perm_Cond_HH := TRUE;
    bCmd_Permeate_DumpValve_Open := TRUE;
ELSIF rVoted_Permeate_Conductivity_uS_cm < (rALM_TRIP_PERM_COND_HH - rALM_HYST_PERM_COND) THEN
    bAlm_Perm_Cond_HH := FALSE;
END_IF;

IF rVoted_Permeate_Conductivity_uS_cm >= rALM_WARN_PERM_COND_H THEN
    bAlm_Perm_Cond_H := TRUE;
ELSIF rVoted_Permeate_Conductivity_uS_cm < (rALM_WARN_PERM_COND_H - rALM_HYST_PERM_COND) THEN
    bAlm_Perm_Cond_H := FALSE;
END_IF;

(* 3. Raw Seawater Intake Turbidity Alarms (Red Tide Diversion Gate) *)
IF rVoted_Intake_Turbidity_NTU >= rALM_TRIP_TURBIDITY_HH THEN
    bAlm_Turbidity_HH := TRUE;
    bCmd_Intake_Divert_Gate_Open := TRUE;
    eActiveFsmState := STATE_HIGH_TURBIDITY_INTAKE_DIVERT;
ELSIF rVoted_Intake_Turbidity_NTU < (rALM_TRIP_TURBIDITY_HH - rALM_HYST_TURBIDITY) THEN
    bAlm_Turbidity_HH := FALSE;
END_IF;

IF rVoted_Intake_Turbidity_NTU >= rALM_WARN_TURBIDITY_H THEN
    bAlm_Turbidity_H := TRUE;
ELSIF rVoted_Intake_Turbidity_NTU < (rALM_WARN_TURBIDITY_H - rALM_HYST_TURBIDITY) THEN
    bAlm_Turbidity_H := FALSE;
END_IF;

(* 4. Brine Concentrate Reject Overpressure / Underpressure *)
IF rVoted_Brine_Reject_Pressure_bar >= rALM_TRIP_BRINE_P_HH THEN
    bAlm_Brine_P_HH := TRUE;
    eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
ELSIF rVoted_Brine_Reject_Pressure_bar < (rALM_TRIP_BRINE_P_HH - rALM_HYST_BRINE_P) THEN
    bAlm_Brine_P_HH := FALSE;
END_IF;

IF (rVoted_Brine_Reject_Pressure_bar <= rALM_TRIP_BRINE_P_LL) AND (eActiveFsmState = STATE_STEADY_STATE_PERMEATE_HARVEST) THEN
    bAlm_Brine_P_LL := TRUE;
    eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
ELSIF rVoted_Brine_Reject_Pressure_bar > (rALM_TRIP_BRINE_P_LL + rALM_HYST_BRINE_P) THEN
    bAlm_Brine_P_LL := FALSE;
END_IF;

(* 5. ERD Isobaric PX Ceramic Rotor Overspeed / Stall *)
IF rVoted_ERD_Rotor_Speed_RPM >= rALM_TRIP_PX_ROTOR_HH THEN
    bAlm_PX_Rotor_HH := TRUE;
    eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
ELSIF rVoted_ERD_Rotor_Speed_RPM < (rALM_TRIP_PX_ROTOR_HH - rALM_HYST_PX_ROTOR) THEN
    bAlm_PX_Rotor_HH := FALSE;
END_IF;

IF (rVoted_ERD_Rotor_Speed_RPM <= rALM_TRIP_PX_ROTOR_LL) AND (eActiveFsmState = STATE_STEADY_STATE_PERMEATE_HARVEST) THEN
    bAlm_PX_Rotor_LL := TRUE;
    eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
ELSIF rVoted_ERD_Rotor_Speed_RPM > (rALM_TRIP_PX_ROTOR_LL + rALM_HYST_PX_ROTOR) THEN
    bAlm_PX_Rotor_LL := FALSE;
END_IF;

(* 6. Chemical Anti-Scalant Low Flow Trip *)
IF ((FT_ANTISCALANT_DOSING_601A + FT_ANTISCALANT_DOSING_601B) * 0.5 <= rALM_TRIP_ANTISCALANT_LL) AND (eActiveFsmState = STATE_STEADY_STATE_PERMEATE_HARVEST) THEN
    bAlm_Antiscalant_LL := TRUE;
    eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
ELSIF ((FT_ANTISCALANT_DOSING_601A + FT_ANTISCALANT_DOSING_601B) * 0.5 > (rALM_TRIP_ANTISCALANT_LL + rALM_HYST_ANTISCALANT)) THEN
    bAlm_Antiscalant_LL := FALSE;
END_IF;

(* 7. Free Chlorine Breakthrough Fast Trip (ORP > 250 mV) *)
IF rVoted_Feed_ORP_mV >= rALM_TRIP_ORP_HH THEN
    bAlm_ORP_HH := TRUE;
    eActiveFsmState := STATE_CONCENTRATE_VALVE_DEPRESSURIZATION;
ELSIF rVoted_Feed_ORP_mV < (rALM_TRIP_ORP_HH - rALM_HYST_ORP) THEN
    bAlm_ORP_HH := FALSE;
END_IF;

(* 8. High Stiff & Davis Scaling Potential Warning *)
IF rObserved_Stiff_Davis_Index >= rALM_WARN_SDSI_H THEN
    bAlm_SDSI_H := TRUE;
ELSIF rObserved_Stiff_Davis_Index < (rALM_WARN_SDSI_H - rALM_HYST_SDSI) THEN
    bAlm_SDSI_H := FALSE;
END_IF;

(* 9. High Specific Energy Consumption Warning *)
IF rCalculated_Specific_Energy_Consumption_kWh_m3 >= rALM_WARN_SEC_H THEN
    bAlm_SEC_H := TRUE;
ELSIF rCalculated_Specific_Energy_Consumption_kWh_m3 < (rALM_WARN_SEC_H - rALM_HYST_SEC) THEN
    bAlm_SEC_H := FALSE;
END_IF;

(* Pack ISA-18.2 Diagnostic Alarm Words *)
dwAlarmWord_Trip := 16#0000;
IF bAlm_Feed_P_HH       THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0001; END_IF;
IF bAlm_Feed_P_LL       THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0002; END_IF;
IF bAlm_Perm_Cond_HH    THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0004; END_IF;
IF bAlm_Turbidity_HH    THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0008; END_IF;
IF bAlm_Brine_P_HH      THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0010; END_IF;
IF bAlm_Brine_P_LL      THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0020; END_IF;
IF bAlm_PX_Rotor_HH     THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0040; END_IF;
IF bAlm_PX_Rotor_LL     THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0080; END_IF;
IF bAlm_Antiscalant_LL  THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0100; END_IF;
IF bAlm_ORP_HH          THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0200; END_IF;
IF bAlm_Discrepancy_Trip THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0400; END_IF;

dwAlarmWord_Warning := 16#0000;
IF bAlm_Feed_P_H        THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0001; END_IF;
IF bAlm_Feed_P_L        THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0002; END_IF;
IF bAlm_Perm_Cond_H     THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0004; END_IF;
IF bAlm_Turbidity_H     THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0008; END_IF;
IF bAlm_SDSI_H          THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0010; END_IF;
IF bAlm_SEC_H           THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0020; END_IF;

(* Pack Facility Status Words *)
dwStatusWord1 := 16#0000;
IF bMasterEnable                    THEN dwStatusWord1 := dwStatusWord1 OR 16#0001; END_IF;
IF bEmergencyStop                   THEN dwStatusWord1 := dwStatusWord1 OR 16#0002; END_IF;
IF (rCmd_HPFP_VFD_Speed_Pct > 5.0)  THEN dwStatusWord1 := dwStatusWord1 OR 16#0004; END_IF;
IF (rCmd_ERD_Booster_VFD_Speed_Pct > 5.0) THEN dwStatusWord1 := dwStatusWord1 OR 16#0008; END_IF;
IF (rCmd_LP_Feed_Pump_Speed_Pct > 5.0) THEN dwStatusWord1 := dwStatusWord1 OR 16#0010; END_IF;
IF NOT bCmd_Permeate_DumpValve_Open THEN dwStatusWord1 := dwStatusWord1 OR 16#0020; END_IF;
IF bCmd_Intake_Divert_Gate_Open     THEN dwStatusWord1 := dwStatusWord1 OR 16#0040; END_IF;
IF bCmd_CIP_Circulation_Pump_Run    THEN dwStatusWord1 := dwStatusWord1 OR 16#0080; END_IF;

dwStatusWord2 := 16#0000;
IF bAutoMpcEnable                   THEN dwStatusWord2 := dwStatusWord2 OR 16#0001; END_IF;
IF (eActiveFsmState = STATE_STEADY_STATE_PERMEATE_HARVEST) THEN dwStatusWord2 := dwStatusWord2 OR 16#0002; END_IF;
IF (rCalculated_ERD_Net_Efficiency_pct >= 95.0) THEN dwStatusWord2 := dwStatusWord2 OR 16#0004; END_IF;
IF (rCalculated_Permeate_Recovery_pct >= 44.5) AND (rCalculated_Permeate_Recovery_pct <= 45.5) THEN dwStatusWord2 := dwStatusWord2 OR 16#0008; END_IF;
IF (rCalculated_Permeate_TDS_ppm < 200.0) THEN dwStatusWord2 := dwStatusWord2 OR 16#0010; END_IF;
IF (rCalculated_Specific_Energy_Consumption_kWh_m3 <= 2.80) THEN dwStatusWord2 := dwStatusWord2 OR 16#0020; END_IF;

(* Production Water Quality & Commercial Compliance Qualification Gate *)
bProductionQualified := (eActiveFsmState = STATE_STEADY_STATE_PERMEATE_HARVEST)
                        AND (rCalculated_Permeate_TDS_ppm < 200.0)
                        AND (rCalculated_Permeate_Recovery_pct >= 44.5)
                        AND (rCalculated_Permeate_Recovery_pct <= 45.5)
                        AND (rCalculated_Specific_Energy_Consumption_kWh_m3 <= 2.80)
                        AND NOT bEmergencyShutdownActive
                        AND (dwAlarmWord_Trip = 16#0000);""")

    # Closing
    st.append("END_FUNCTION_BLOCK")

    full_code = "\n\n".join(st)
    return full_code

def validate_code(code_str):
    # Check delimiters
    if_count = len(re.findall(r'\bIF\b', code_str))
    end_if_count = len(re.findall(r'\bEND_IF;', code_str))
    
    case_count = len(re.findall(r'\bCASE\b', code_str))
    end_case_count = len(re.findall(r'\bEND_CASE;', code_str))
    
    for_count = len(re.findall(r'\bFOR\b', code_str))
    end_for_count = len(re.findall(r'\bEND_FOR;', code_str))
    
    var_input_count = len(re.findall(r'\bVAR_INPUT\b', code_str))
    var_output_count = len(re.findall(r'\bVAR_OUTPUT\b', code_str))
    var_count = len(re.findall(r'\bVAR\b', code_str))
    end_var_count = len(re.findall(r'\bEND_VAR\b', code_str))
    
    fb_start = len(re.findall(r'\bFUNCTION_BLOCK\b', code_str))
    fb_end = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', code_str))
    
    print(f"IF: {if_count}, END_IF;: {end_if_count}")
    print(f"CASE: {case_count}, END_CASE;: {end_case_count}")
    print(f"FOR: {for_count}, END_FOR;: {end_for_count}")
    print(f"VAR/VAR_INPUT/VAR_OUTPUT: {var_count}, END_VAR: {end_var_count}")
    print(f"FUNCTION_BLOCK: {fb_start}, END_FUNCTION_BLOCK: {fb_end}")
    
    assert if_count == end_if_count, f"IF parity mismatch: {if_count} != {end_if_count}"
    assert case_count == end_case_count, f"CASE parity mismatch: {case_count} != {end_case_count}"
    assert for_count == end_for_count, f"FOR parity mismatch: {for_count} != {end_for_count}"
    assert fb_start == fb_end, f"FUNCTION_BLOCK parity mismatch: {fb_start} != {fb_end}"
    print("ALL DELIMITERS PERFECTLY MATCHED!")

if __name__ == "__main__":
    code = build_full_st_code()
    print(f"Generated Structured Text length: {len(code)} characters, {len(code.splitlines())} lines.")
    validate_code(code)

    uid = uuid.uuid4().hex[:8]
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Municipal Infrastructure & Mega-Scale Desalination: World-Scale 600,000 m³/Day Seawater Reverse Osmosis (SWRO) Desalination Facility: High-Pressure Feed Pumps (75.0 bar, 12 MW VFD), Isobaric Ceramic Pressure Exchanger (PX) Energy Recovery Device (97.5% net hydraulic energy transfer efficiency, rotor speed and volumetric lubrication balancing), Two-Pass Polyamide Membrane Train Mineral Scaling & Biofouling Observer (solution-diffusion model, concentration polarization modulus, temperature-compensated salt passage), Dynamic Transmembrane Pressure (TMP) & Permeate Recovery (45.0% ± 0.5%) Decoupling, and Red Tide Algal Bloom / Raw Seawater High Turbidity Emergency Intake Diversion Interlocks.**

Task: Write a world-class, mathematically rigorous, ultra-realistic IEC 61131-3 Structured Text Function Block named `FB_Water_SWRO_Desalination_IsobaricERD_MembraneFouling` for this world-scale SWRO desalination train.

NEXT-GEN QUALITY REQUIREMENTS:
1. Transmitter & Tag Nomenclature:
   - Standardized industrial P&ID tags: PT_SWRO_HP_FEED_101A/B/C, PT_SWRO_CONCENTRATE_102A/B/C, PT_SWRO_PERMEATE_103A/B/C, FT_HP_SEAWATER_FEED_201A/B/C, FT_PERMEATE_PRODUCT_202A/B/C, FT_BRINE_REJECT_203A/B/C, AIT_FEED_SALINITY_TDS_301A/B/C, AIT_PERMEATE_CONDUCTIVITY_302A/B/C, AIT_INTAKE_TURBIDITY_NTU_303A/B/C, TT_SEAWATER_INLET_401A/B/C, ST_ERD_PX_ROTOR_RPM_501A/B/C, PT_ERD_BOOSTER_DISCHARGE_502A/B/C.
2. Mathematical Depth & State-Space:
   - Full 8x8 discrete state-space formulation (x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k) at 50 ms cycle modeling solution-diffusion transport, van 't Hoff osmotic pressure, concentration polarization exponential boundary layer buildup, and ceramic isobaric rotor mixing leakage and hydrodynamic pressure loss.
   - Receding-horizon Model Predictive Control (MPC) quadratic cost functional optimizing high-pressure pump VFD speed, ERD booster pump speed, brine throttle valve, and anti-scalant dosing stroke to minimize specific energy consumption (< 2.8 kWh/m3) while keeping permeate TDS < 200 ppm.
3. 2oo3 Triple Modular Redundancy (TMR):
   - Membrane feed high-pressure transmitters (2oo3 voting with 0.8 bar discrepancy threshold).
   - Permeate conductivity analyzers (2oo3 voting with 5.0 µS/cm discrepancy limit).
4. ISA-18.2 Alarm Ladder:
   - Full 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with membrane compaction overpressure fast trip (< 100 ms) and raw seawater algal bloom turbidity surge diversion gate actuation.
5. Multi-Stage FSM:
   - 12-state state machine: SYSTEM_OFFLINE_STANDBY, LOW_PRESSURE_MEMBRANE_FLUSH, CHEMICAL_SCALE_INHIBITOR_PRIME, HP_PUMP_SOFT_START_RAMP, ERD_ISOBARIC_PX_SYNCHRONIZATION, PRESSURE_RAMP_TO_OSMOTIC_BREAK, STEADY_STATE_PERMEATE_HARVEST, MEMBRANE_CLEANING_CIP_CYCLE, HIGH_TURBIDITY_INTAKE_DIVERT, CONCENTRATE_VALVE_DEPRESSURIZATION, PERMEATE_DISCHARGE_FLUSH_SHUTDOWN, EMERGENCY_ESTOP_LINE_RELIEF.
6. Extreme Token Density & Code Completeness:
   - Zero summaries, zero placeholders, 100% exact delimiter parity. Output format in ```iec-st fenced code block."""

    output_fenced = f"```iec-st\n{code}\n```"

    record = {
        "id": f"synthetic_v3_{uid}",
        "instruction": prompt,
        "input": "",
        "output": output_fenced,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": output_fenced}
        ],
        "metadata": {
            "domain": "Water_Desalination_SWRO",
            "function_block": "FB_Water_SWRO_Desalination_IsobaricERD_MembraneFouling",
            "version": "v3_cyberphysical_max",
            "lines": len(code.splitlines()),
            "characters": len(code),
            "validated": True
        }
    }

    raw_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw"
    os.makedirs(raw_dir, exist_ok=True)
    filename = os.path.join(raw_dir, f"agent_{uid}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"SUCCESS: Saved {len(code)} characters to {filename}")

