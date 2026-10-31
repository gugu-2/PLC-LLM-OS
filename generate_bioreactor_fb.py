# generate_bioreactor_fb.py
# Generates FB_Biotech_SingleUse_PerfusionBioreactor_500L

import json
import os
import subprocess

def get_header():
    return """FUNCTION_BLOCK FB_Biotech_SingleUse_PerfusionBioreactor_500L
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL BIOPHARMACEUTICALS & LIFE SCIENCES - ADVANCED THERAPY MEDICINAL PRODUCTS (ATMP)
500-LITER SINGLE-USE CONTINUOUS PERFUSION BIOREACTOR (SUB) WITH TANGENTIAL FLOW FILTRATION (TFF)
========================================================================================================================
ARCHITECTURE OVERVIEW:
  This production-grade Function Block implements complete multi-variable cyber-physical control for an industrial
  500-liter Single-Use Bioreactor (SUB) engineered for continuous high-density mammalian (CHO-DG44 / CHO-K1) cell
  culture producing recombinant therapeutic monoclonal antibodies (mAbs). The block couples mechanical, thermodynamic,
  fluid hydrodynamic, chemical buffering, and cellular metabolic systems into a deterministic PLC execution loop.

KEY ENGINEERING PRINCIPLES IMPLEMENTED:
  1. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR INTEGRITY:
     - Optical dissolved oxygen (DO) probes with pairwise discrepancy detection, degradation, and mid-value voting.
     - Redundant optical/electrochemical pH transmitters with dynamic drift detection and automated bumpless degradation.
     - Triplicate shear-beam load cell weight transmitters reconciling gross broth mass and liquid inventory.
     - Triplicate sanitary diaphragm-isolated pressure transducers monitoring TFF hollow-fiber permeate pressure.
  2. 4-GAS MASS FLOW CONTROLLER (MFC) DYNAMIC BLENDING MANIFOLD:
     - Pure Oxygen (O2), Clean Dry Compressed Air, Carbon Dioxide (CO2), and High-Purity Nitrogen (N2).
     - Micro-sparger (sintered porous frit 20-50 um pore diameter) for ultra-efficient, low-shear bubble dissolution.
     - Drilled-hole macro-sparger (1.5 mm diameter orifices) for bulk CO2 stripping and headspace blanket purging.
     - Real-time respiratory gas blending: decouples oxygenation (OTR) from dissolved carbon dioxide (pCO2) stripping.
  3. DUAL-RANGE ASYMMETRIC pH REGULATION:
     - Acidifying branch: High-frequency pulse-width modulated (PWM) CO2 gas sparging through macro-sparger.
     - Alkalizing branch: Variable-speed peristaltic pump dispensing sterile 1.0 M sodium bicarbonate (NaHCO3).
     - Asymmetric anti-windup deadbands to eliminate cyclic chemical hunting and prevent osmolality runaway (>380 mOsm/kg).
  4. TANGENTIAL FLOW FILTRATION (TFF) CELL RETENTION & CHEMOSTAT BLEED PACING:
     - 0.2 um polyethersulfone (PES) hollow-fiber membrane module providing 100% mammalian cell retention.
     - Continuous Transmembrane Pressure (TMP = (P_feed + P_retentate)/2 - P_permeate) calculation.
     - Automated high-frequency reverse backflush pulse pacing to disrupt laminar cake polarization.
     - Hollow-fiber lumen wall shear rate strictly regulated below 2000 s^-1 to eliminate cell shear necrosis.
     - Continuous automated cell bleed pump pacing to maintain steady-state Viable Cell Density (VCD > 80 x 10^6 cells/mL).
  5. OFF-GAS METABOLIC SPECTROMETRY & RESPIRATORY QUOTIENT (RQ):
     - Real-time molar gas balances via paramagnetic O2 and non-dispersive infrared (NDIR) CO2 off-gas analyzers.
     - Inert gas (N2) balancing to cancel out barometric pressure variations and headspace water vapor dilution.
     - Real-time Oxygen Uptake Rate (OUR [mmol/(L*h)]) and Carbon Dioxide Evolution Rate (CER [mmol/(L*h)]).
     - Respiratory Quotient calculation (RQ = CER / OUR) to detect metabolic shifts (glycolysis vs. Krebs TCA cycle).
  6. DISCRETE CYBER-PHYSICAL STATE-SPACE MODEL (12x12 A, 12x8 B, 8x12 C):
     - 12 Dynamic States: VCD, Non-viable Cell Density, Glucose, Glutamine, Lactate, Ammonia, mAb Titre, DO, pH, Temp, Vol, R_f.
     - Coupled Monod and Michaelis-Menten multi-substrate limitation with dual product inhibition kinetics.
     - Volumetric oxygen transfer coefficient (kLa) empirical correlation with specific power input (P/V) and gas superficial velocity.
  7. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC):
     - Quadratic cost function penalizing state tracking errors (Q) and actuator move rates (R).
     - Prediction horizon Np = 5 steps, control horizon Nc = 3 steps.
     - Projected gradient descent solver computing constrained actuator commands within physical pump/MFC bounds.
  8. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM):
     - From pre-use single-use bag integrity leak hold test to continuous perfusion harvest and CIP line decontamination.
  9. ISA-18.2 MULTI-TIERED ALARM MANAGEMENT & PACKED DIAGNOSTIC DWORDS:
     - Multi-level trip thresholds (HH, H, L, LL) with deadband hysteresis and qualification debounce filters.
========================================================================================================================
*)
"""

def get_var_input():
    return """VAR_INPUT
    (* Master Automation & Safety Interlocks *)
    bEnableSystem                   : BOOL := FALSE;        (* Master bioreactor automation sequence enable [bool] *)
    bEmergencyStopOk                : BOOL := TRUE;         (* Hardwired fail-safe dual-channel safety circuit status [bool] *)
    bSterileBarrierOk               : BOOL := TRUE;         (* Single-use bag sterile connection boundary sensor [bool] *)

    (* 2oo3 TMR Triple Dissolved Oxygen Optical Probes *)
    rDO_Probe1_Pct                  : REAL := 45.0;         (* Dissolved Oxygen optical probe 1 primary sensor [% air sat] *)
    rDO_Probe2_Pct                  : REAL := 45.0;         (* Dissolved Oxygen optical probe 2 secondary sensor [% air sat] *)
    rDO_Probe3_Pct                  : REAL := 45.0;         (* Dissolved Oxygen optical probe 3 tertiary sensor [% air sat] *)

    (* 2oo3 TMR Triple pH Combined Optical/Electrochemical Transmitters *)
    rPH_Probe1_pH                   : REAL := 7.00;         (* Broth pH combined optical/electrochemical transmitter 1 [pH units] *)
    rPH_Probe2_pH                   : REAL := 7.00;         (* Broth pH combined optical/electrochemical transmitter 2 [pH units] *)
    rPH_Probe3_pH                   : REAL := 7.00;         (* Broth pH combined optical/electrochemical transmitter 3 [pH units] *)

    (* 2oo3 TMR Triple Vessel Weight Load Cell Transmitters *)
    rVesselWeight1_kg               : REAL := 450.0;        (* Skid support shear-beam load cell weight transmitter 1 [kg] *)
    rVesselWeight2_kg               : REAL := 450.0;        (* Skid support shear-beam load cell weight transmitter 2 [kg] *)
    rVesselWeight3_kg               : REAL := 450.0;        (* Skid support shear-beam load cell weight transmitter 3 [kg] *)

    (* 2oo3 TMR Triple Hollow-Fiber Permeate Pressure Transducers *)
    rPermeatePress1_mbar            : REAL := 120.0;        (* Hollow-fiber membrane permeate line pressure sensor 1 [mbar] *)
    rPermeatePress2_mbar            : REAL := 120.0;        (* Hollow-fiber membrane permeate line pressure sensor 2 [mbar] *)
    rPermeatePress3_mbar            : REAL := 120.0;        (* Hollow-fiber membrane permeate line pressure sensor 3 [mbar] *)

    (* Hydraulic & Membrane Pressures *)
    rFeedPress_mbar                 : REAL := 380.0;        (* TFF cell retention module feed pressure transducer [mbar] *)
    rRetentatePress_mbar            : REAL := 290.0;        (* TFF cell retention module retentate pressure transducer [mbar] *)
    rVesselInternalPress_mbar       : REAL := 25.0;         (* Single-use bag headspace internal pressure transmitter [mbar] *)

    (* Thermal Control Sensors *)
    rBrothTemp_degC                 : REAL := 36.8;         (* Vessel thermal well resistance temperature detector PT100 [deg C] *)
    rJacketTemp_degC                : REAL := 37.1;         (* Jacketed thermal fluid circulating loop temperature [deg C] *)

    (* Drive & Agitation Feedback *)
    rAgitatorSpeedFeedback_rpm      : REAL := 120.0;        (* Bottom magnetic levitation impeller optical tachometer [rpm] *)
    rAgitatorCurrent_A              : REAL := 1.85;         (* Mag-lev drive synchronous motor phase current [A] *)

    (* Level & Biochemical Analyzers *)
    bFoamDetectHeadspace            : BOOL := FALSE;        (* Sanitary high-level optical/conductive foam detection probe [bool] *)
    rOffGas_O2_Pct                  : REAL := 18.2;         (* Off-gas paramagnetic analyzer dry oxygen fraction [%] *)
    rOffGas_CO2_Pct                 : REAL := 3.45;         (* Off-gas NDIR analyzer dry carbon dioxide fraction [%] *)
    rBiomassPermittivity_pF_cm      : REAL := 42.5;         (* High-frequency RF impedance biomass sensor [pF/cm] *)

    (* Auxiliary Reagent & Buffer Scales *)
    rHarvestScaleWeight_kg          : REAL := 85.0;         (* Permeate harvest sterile collection tote scale [kg] *)
    rMediaSupplyScaleWeight_kg      : REAL := 620.0;        (* Fresh perfusion media nutrient feed tank scale [kg] *)
    rBaseSupplyScaleWeight_kg       : REAL := 45.0;         (* Sodium bicarbonate buffer chemical reagent scale [kg] *)
    rAntifoamSupplyScale_kg         : REAL := 12.0;         (* Sterile silicone antifoam chemical reservoir scale [kg] *)

    (* Environmental & Execution Cycle *)
    rAmbientPress_mbar              : REAL := 1013.25;      (* Cleanroom suite atmospheric barometric pressure [mbar] *)
    rAmbientTemp_degC               : REAL := 21.5;         (* Cleanroom suite ambient air temperature [deg C] *)
    tTaskCycleTime_s                : REAL := 0.100;        (* Deterministic execution cycle delta time [s] *)

    (* Recipe Operating Setpoints *)
    rSet_DO_Pct                     : REAL := 45.0;         (* Dissolved oxygen operating setpoint [% air sat] *)
    rSet_PH                         : REAL := 7.00;         (* Broth pH operating setpoint [pH units] *)
    rSet_Temperature_degC           : REAL := 36.80;        (* Broth temperature operating setpoint [deg C] *)
    rSet_WorkingVolume_L            : REAL := 450.0;        (* Target working broth liquid volume [L] *)
    rSet_VCD_Target_1e6             : REAL := 85.0;         (* Viable cell density steady-state target [10^6 cells/mL] *)
    rSet_CSPR_Target_pL_cell_d      : REAL := 30.0;         (* Cell-specific perfusion rate target [pL/cell/day] *)
    rSet_MaxPerfusionRate_VVD       : REAL := 2.50;         (* Maximum allowable perfusion rate [d^-1] *)
    rSet_AgitatorBaseSpeed_rpm      : REAL := 120.0;        (* Nominal magnetic impeller rotational speed setpoint [rpm] *)
    rSet_TMP_AlarmThreshold_mbar    : REAL := 420.0;        (* Transmembrane pressure high trip threshold [mbar] *)
    rSet_BackflushInterval_s        : REAL := 900.0;        (* TFF automated reverse backflush pacing period [s] *)
    rSet_BackflushDuration_s        : REAL := 15.0;         (* TFF reverse backflush pulse execution duration [s] *)

    (* Operator & Sequence Commands *)
    bCmd_AcknowledgeAlarms          : BOOL := FALSE;        (* Operator ISA-18.2 alarm acknowledge command [bool] *)
    bCmd_ManualOverrideEnable       : BOOL := FALSE;        (* Engineering manual maintenance actuator override [bool] *)
    bCmd_ForceBackflushNow          : BOOL := FALSE;        (* Manual trigger for immediate TFF membrane backflush [bool] *)
    bCmd_AdvanceFSM_Phase           : BOOL := FALSE;        (* Manual engineering phase transition permissive trigger [bool] *)
    bCmd_AbortRun                   : BOOL := FALSE;        (* Emergency batch abort command [bool] *)
END_VAR
"""

def get_var_output():
    return """VAR_OUTPUT
    (* Mass Flow Controller Commands *)
    rCmd_MFC_O2_Micro_sLpm          : REAL := 0.0;          (* Micro-sparger pure O2 mass flow controller command [sL/min] *)
    rCmd_MFC_Air_Micro_sLpm         : REAL := 0.0;          (* Micro-sparger compressed air mass flow controller command [sL/min] *)
    rCmd_MFC_Air_Macro_sLpm         : REAL := 0.0;          (* Macro-sparger compressed air stripping flow command [sL/min] *)
    rCmd_MFC_CO2_Macro_sLpm         : REAL := 0.0;          (* Macro-sparger CO2 acidifying/stripping flow command [sL/min] *)
    rCmd_MFC_N2_Macro_sLpm          : REAL := 0.0;          (* Macro-sparger N2 deoxygenation mass flow command [sL/min] *)

    (* Agitation & Thermal Actuator Commands *)
    rCmd_AgitatorSpeed_rpm          : REAL := 0.0;          (* Bottom magnetic levitation drive speed setpoint [rpm] *)
    rCmd_TCU_HeatingPower_kW        : REAL := 0.0;          (* Jacketed thermal blanket electric heater SCR output [kW] *)
    rCmd_TCU_CoolingValve_Pct       : REAL := 0.0;          (* Jacketed cooling loop proportional servo valve [0-100%] [%] *)

    (* Bioprocess Pump Commands *)
    rCmd_PerfusionFeedPump_Lph      : REAL := 0.0;          (* Fresh nutrient media perfusion feed pump rate [L/h] *)
    rCmd_PermeateHarvestPump_Lph    : REAL := 0.0;          (* TFF hollow-fiber clarified permeate harvest rate [L/h] *)
    rCmd_CellBleedPump_Lph          : REAL := 0.0;          (* Biomass chemostat continuous cell bleed pump rate [L/h] *)
    rCmd_BasePeristalticPump_mLph   : REAL := 0.0;          (* Sodium bicarbonate chemical buffer dosing pump [mL/h] *)

    (* Sanitary Discrete Actuators *)
    bCmd_AntifoamDosePulse          : BOOL := FALSE;        (* Sterile antifoam injection solenoid pulse command [bool] *)
    bCmd_TFF_BackflushValve         : BOOL := FALSE;        (* TFF reverse pulse high-speed pinch valve actuator [bool] *)
    bCmd_HarvestDivertValve         : BOOL := FALSE;        (* Dual-bag harvest collection switching valve [bool] *)
    bCmd_WasteNeutralizeValve       : BOOL := FALSE;        (* In-line biowaste kill-tank caustic flush valve [bool] *)

    (* Reconciled Process State & Analytical Variables *)
    rCalc_VesselVolume_L            : REAL := 0.0;          (* 2oo3 load cell reconciled broth volume [L] *)
    rCalc_VCD_Estimated             : REAL := 0.0;          (* Metabolic/impedance observer estimated viable cell density [10^6 cells/mL] *)
    rCalc_OUR_mmol_L_h              : REAL := 0.0;          (* Real-time metabolic Oxygen Uptake Rate [mmol/(L*h)] *)
    rCalc_CER_mmol_L_h              : REAL := 0.0;          (* Real-time metabolic Carbon Dioxide Evolution Rate [mmol/(L*h)] *)
    rCalc_RQ                        : REAL := 1.0;          (* Respiratory Quotient CER/OUR [dimensionless] *)
    rCalc_CSPR_pL_cell_d            : REAL := 0.0;          (* Cell-Specific Perfusion Rate [pL/cell/day] *)
    rCalc_TMP_mbar                  : REAL := 0.0;          (* Tangential Flow Filtration Transmembrane Pressure [mbar] *)
    rCalc_MembraneResistance_1e11   : REAL := 0.0;          (* Hollow-fiber membrane fouling hydraulic resistance [10^11 m^-1] *)
    rCalc_ShearRate_s_inv           : REAL := 0.0;          (* Hollow-fiber lumen wall shear rate [1/s] *)
    rCalc_PowerPerVolume_W_m3       : REAL := 0.0;          (* Specific agitator power dissipation P/V [W/m3] *)
    rCalc_kLa_h_inv                 : REAL := 0.0;          (* Volumetric oxygen mass transfer coefficient kLa [1/h] *)
    rCalc_TipSpeed_m_s              : REAL := 0.0;          (* Bottom magnetic impeller outer tip speed [m/s] *)
    rCalc_KolmogorovScale_um        : REAL := 0.0;          (* Turbulent eddy Kolmogorov length microscale [um] *)

    (* Sequence State & Diagnostics *)
    iActiveFSMState                 : INT := 1;             (* 12-stage operational state machine active state index [enum] *)
    dwAlarmWord_1                   : DWORD := 16#00000000; (* ISA-18.2 Process excursions and critical safety trips bitfield *)
    dwAlarmWord_2                   : DWORD := 16#00000000; (* TMR sensor discrepancies and hardware fail flags bitfield *)
    dwStatusWord_1                  : DWORD := 16#00000000; (* System operation modes and subsystem ready flags bitfield *)
    dwStatusWord_2                  : DWORD := 16#00000000; (* Metabolic, filtration, and bioprocess quality metrics bitfield *)
    bSystemHealthy                  : BOOL := TRUE;         (* Comprehensive health status indicator [bool] *)
    bCriticalAlarmSummary           : BOOL := FALSE;        (* Master emergency stop / process abort demand flag [bool] *)
END_VAR
"""

print("Header, VAR_INPUT, VAR_OUTPUT defined.")
