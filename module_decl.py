# module_decl.py
# Contains Header, VAR_INPUT, VAR_OUTPUT, VAR declarations

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
*)"""

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
END_VAR"""

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
END_VAR"""

def get_var():
    return """VAR
    (* ================================================================================================== *)
    (* DISCRETE CYBER-PHYSICAL STATE-SPACE MATRICES & VECTORS (12x12 A, 12x8 B, 8x12 C, 8x8 D)          *)
    (* States: 1=VCD, 2=NCD, 3=Glc, 4=Gln, 5=Lac, 6=Amm, 7=mAb, 8=DO, 9=pH, 10=Temp, 11=Vol, 12=R_f     *)
    (* Inputs: 1=O2_micro, 2=Air_micro, 3=CO2_macro, 4=Base_pump, 5=Feed, 6=Perm, 7=Bleed, 8=TCU_net   *)
    (* Outputs: 1=VCD, 2=Glc, 3=Lac, 4=mAb, 5=DO, 6=pH, 7=Temp, 8=Vol                                    *)
    (* ================================================================================================== *)
    arrA                            : ARRAY[1..12, 1..12] OF REAL;
    arrB                            : ARRAY[1..12, 1..8] OF REAL;
    arrC                            : ARRAY[1..8, 1..12] OF REAL;
    arrD                            : ARRAY[1..8, 1..8] OF REAL;
    arrX_State                      : ARRAY[1..12] OF REAL;  (* Active state estimate vector *)
    arrX_Next                       : ARRAY[1..12] OF REAL;  (* Discrete propagated state vector *)
    arrX_Pred                       : ARRAY[1..12] OF REAL;  (* Horizon trajectory predictor *)
    arrX_Horizon                    : ARRAY[1..5, 1..12] OF REAL; (* 5-step receding prediction horizon *)
    arrU_Actuators                  : ARRAY[1..8] OF REAL;   (* Actuator command vector *)
    arrU_Old                        : ARRAY[1..8] OF REAL;   (* Previous execution step actuators *)
    arrU_Delta                      : ARRAY[1..8] OF REAL;   (* Actuator slew rate vector *)
    arrU_Optimal                    : ARRAY[1..8] OF REAL;   (* Projected MPC optimizer solution *)
    arrY_Outputs                    : ARRAY[1..8] OF REAL;   (* Calculated model output vector *)
    arrSP                           : ARRAY[1..12] OF REAL;  (* State-space target trajectory *)
    arrQ_Weights                    : ARRAY[1..12] OF REAL;  (* Quadratic state deviation penalties *)
    arrR_Weights                    : ARRAY[1..8] OF REAL;   (* Quadratic actuator slew penalties *)
    arrP_Terminal                   : ARRAY[1..12] OF REAL;  (* Terminal horizon state penalties *)
    arrU_Min                        : ARRAY[1..8] OF REAL;   (* Physical minimum actuator saturations *)
    arrU_Max                        : ARRAY[1..8] OF REAL;   (* Physical maximum actuator saturations *)
    arrDeltaU_Max                   : ARRAY[1..8] OF REAL;   (* Maximum allowed actuator delta per cycle *)
    arrGradJ                        : ARRAY[1..8] OF REAL;   (* Projected cost gradient vector *)
    bMatricesInitialized            : BOOL := FALSE;         (* State-space matrix initialization flag *)

    (* ================================================================================================== *)
    (* BIOPHARMACEUTICAL CELL CULTURE & HYDRODYNAMIC PHYSICAL CONSTANTS                                  *)
    (* ================================================================================================== *)
    c_rPi                           : REAL := 3.141592653589793; (* Circle circumference constant [-] *)
    c_rBrothDensity_kg_m3           : REAL := 1025.0;            (* Mammalian cell culture broth density [kg/m^3] *)
    c_rBrothViscosity_Pa_s          : REAL := 0.00115;           (* Broth dynamic shear viscosity at 37 C [Pa*s] *)
    c_rImpellerDia_m                : REAL := 0.285;             (* Bottom magnetic drive pitched-blade impeller diameter [m] *)
    c_rImpellerNp                   : REAL := 1.65;              (* Turbulent impeller power number Np [-] *)
    c_rVesselInnerDia_m             : REAL := 0.760;             (* 500L SUB vessel cylindrical inner diameter [m] *)
    c_rVesselCrossSection_m2        : REAL := 0.45364;           (* 500L SUB horizontal cross-sectional area [m^2] *)
    c_rMolarGasVol_L_mol            : REAL := 22.414;            (* Standard molar volume of ideal gas [L/mol] *)
    c_rHenryConstO2_bar_L_mol       : REAL := 769.23;            (* Henry law solubility constant for oxygen at 37 C [bar*L/mol] *)
    c_rFilterFiberRadius_m          : REAL := 0.000375;          (* TFF hollow fiber inner lumen radius (0.75 mm ID) [m] *)
    c_rFilterFiberCount             : REAL := 2400.0;            (* Number of parallel hollow fibers in TFF cartridge [-] *)
    c_rFilterArea_m2                : REAL := 2.50;              (* TFF hollow fiber total effective membrane area [m^2] *)
    c_rCleanMembraneRes_1e11        : REAL := 1.85;              (* Virgin hydraulic membrane resistance [10^11 m^-1] *)

    (* ================================================================================================== *)
    (* MAMMALIAN CELL KINETIC PARAMETERS (CHO-DG44 MONOD / MICHAELIS-MENTEN BIO-MODEL)                  *)
    (* ================================================================================================== *)
    c_rMuMax_h_inv                  : REAL := 0.0380;            (* Maximum specific cellular growth rate [h^-1] *)
    c_rKsGlc_g_L                    : REAL := 0.250;             (* Monod substrate affinity constant for D-Glucose [g/L] *)
    c_rKsGln_mmol_L                 : REAL := 0.150;             (* Monod substrate affinity constant for L-Glutamine [mmol/L] *)
    c_rKiLac_g_L                    : REAL := 8.500;             (* Non-competitive metabolic inhibition constant for Lactate [g/L] *)
    c_rKiAmm_mmol_L                 : REAL := 4.200;             (* Non-competitive metabolic inhibition constant for Ammonia [mmol/L] *)
    c_rYxGlc_cells_g                : REAL := 1.250E8;           (* Biomass cell yield on D-Glucose [cells/g] *)
    c_rYxGln_cells_mmol             : REAL := 5.800E8;           (* Biomass cell yield on L-Glutamine [cells/mmol] *)
    c_rYlacGlc_g_g                  : REAL := 0.720;             (* Metabolic yield of Lactate per gram Glucose [g/g] *)
    c_rYammGln_mmol_mmol            : REAL := 0.450;             (* Metabolic yield of Ammonia per mmol Glutamine [mmol/mmol] *)
    c_rAlphaMAb                     : REAL := 0.0280;            (* Growth-associated mAb antibody productivity [g/(10^6 cells*h)] *)
    c_rBetaMAb                      : REAL := 0.00065;           (* Maintenance nongrowth-associated mAb productivity [g/(10^6 cells*h)] *)
    c_rKd0_h_inv                    : REAL := 0.00250;           (* Baseline specific cellular apoptosis/death rate [h^-1] *)
    c_rKdLac                        : REAL := 0.00085;           (* Toxic death rate acceleration coefficient by Lactate [L/(g*h)] *)
    c_rKdAmm                        : REAL := 0.00140;           (* Toxic death rate acceleration coefficient by Ammonia [L/(mmol*h)] *)
    c_rOptTemp_degC                 : REAL := 36.80;             (* Optimum metabolic culture temperature [deg C] *)
    c_rOptPH                        : REAL := 7.00;              (* Optimum enzymatic extracellular broth pH [pH units] *)
    c_rBaseNormality_M              : REAL := 1.00;              (* Sterile sodium bicarbonate dosing solution normality [mol/L] *)

    (* ================================================================================================== *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR INTERFACE & TIMERS                                     *)
    (* ================================================================================================== *)
    c_rTMR_DO_Tol_Pct               : REAL := 4.50;              (* Max allowable inter-channel optical DO divergence [% air sat] *)
    c_rTMR_PH_Tol_pH                : REAL := 0.150;             (* Max allowable inter-channel broth pH divergence [pH units] *)
    c_rTMR_Weight_Tol_kg            : REAL := 8.00;              (* Max allowable inter-channel load cell divergence [kg] *)
    c_rTMR_Press_Tol_mbar           : REAL := 25.00;             (* Max allowable inter-channel permeate pressure divergence [mbar] *)
    rVoted_DO_Pct                   : REAL := 45.0;              (* Reconciled 2oo3 median voted DO value [% air sat] *)
    rVoted_PH                       : REAL := 7.00;              (* Reconciled 2oo3 median voted broth pH [pH units] *)
    rVoted_Weight_kg                : REAL := 450.0;             (* Reconciled 2oo3 median voted skid gross weight [kg] *)
    rVoted_PermPress_mbar           : REAL := 120.0;             (* Reconciled 2oo3 median voted permeate pressure [mbar] *)
    bDO_Probe1_Degraded             : BOOL := FALSE;             (* DO probe 1 persistent discrepancy latch [bool] *)
    bDO_Probe2_Degraded             : BOOL := FALSE;             (* DO probe 2 persistent discrepancy latch [bool] *)
    bDO_Probe3_Degraded             : BOOL := FALSE;             (* DO probe 3 persistent discrepancy latch [bool] *)
    bDO_SystemFault                 : BOOL := FALSE;             (* 2oo3 DO triple failure critical alarm [bool] *)
    bPH_Probe1_Degraded             : BOOL := FALSE;             (* pH probe 1 persistent discrepancy latch [bool] *)
    bPH_Probe2_Degraded             : BOOL := FALSE;             (* pH probe 2 persistent discrepancy latch [bool] *)
    bPH_Probe3_Degraded             : BOOL := FALSE;             (* pH probe 3 persistent discrepancy latch [bool] *)
    bPH_SystemFault                 : BOOL := FALSE;             (* 2oo3 pH triple failure critical alarm [bool] *)
    bWeight_Cell1_Degraded          : BOOL := FALSE;             (* Load cell 1 persistent discrepancy latch [bool] *)
    bWeight_Cell2_Degraded          : BOOL := FALSE;             (* Load cell 2 persistent discrepancy latch [bool] *)
    bWeight_Cell3_Degraded          : BOOL := FALSE;             (* Load cell 3 persistent discrepancy latch [bool] *)
    bWeight_SystemFault             : BOOL := FALSE;             (* 2oo3 weight triple failure critical alarm [bool] *)
    bPerm_Trans1_Degraded           : BOOL := FALSE;             (* Permeate sensor 1 persistent discrepancy latch [bool] *)
    bPerm_Trans2_Degraded           : BOOL := FALSE;             (* Permeate sensor 2 persistent discrepancy latch [bool] *)
    bPerm_Trans3_Degraded           : BOOL := FALSE;             (* Permeate sensor 3 persistent discrepancy latch [bool] *)
    bPerm_SystemFault               : BOOL := FALSE;             (* 2oo3 permeate pressure critical failure alarm [bool] *)
    tTimer_DO_Discrep1              : TON;                       (* Discrepancy debounce timer DO channel 1 *)
    tTimer_DO_Discrep2              : TON;                       (* Discrepancy debounce timer DO channel 2 *)
    tTimer_DO_Discrep3              : TON;                       (* Discrepancy debounce timer DO channel 3 *)
    tTimer_PH_Discrep1              : TON;                       (* Discrepancy debounce timer pH channel 1 *)
    tTimer_PH_Discrep2              : TON;                       (* Discrepancy debounce timer pH channel 2 *)
    tTimer_PH_Discrep3              : TON;                       (* Discrepancy debounce timer pH channel 3 *)
    tTimer_Weight_Discrep1          : TON;                       (* Discrepancy debounce timer weight channel 1 *)
    tTimer_Weight_Discrep2          : TON;                       (* Discrepancy debounce timer weight channel 2 *)
    tTimer_Weight_Discrep3          : TON;                       (* Discrepancy debounce timer weight channel 3 *)
    tTimer_Perm_Discrep1            : TON;                       (* Discrepancy debounce timer permeate press channel 1 *)
    tTimer_Perm_Discrep2            : TON;                       (* Discrepancy debounce timer permeate press channel 2 *)
    tTimer_Perm_Discrep3            : TON;                       (* Discrepancy debounce timer permeate press channel 3 *)

    (* ================================================================================================== *)
    (* OFF-GAS ANALYSIS & METABOLIC BALANCING INTERNAL VARIABLES                                         *)
    (* ================================================================================================== *)
    rTotalInletGas_sLpm             : REAL := 5.00;              (* Sum of all active sparger gas flows [sL/min] *)
    rMolarInletGas_mol_h            : REAL := 13.38;             (* Inlet gas total molar delivery rate [mol/h] *)
    rFraction_O2_In                 : REAL := 0.2095;            (* Weighted mole fraction O2 in sparged inlet gas [-] *)
    rFraction_CO2_In                : REAL := 0.0004;            (* Weighted mole fraction CO2 in sparged inlet gas [-] *)
    rFraction_N2_In                 : REAL := 0.7901;            (* Weighted mole fraction N2 in sparged inlet gas [-] *)
    rFraction_O2_Out                : REAL := 0.1820;            (* Normalized dry off-gas O2 mole fraction [-] *)
    rFraction_CO2_Out               : REAL := 0.0345;            (* Normalized dry off-gas CO2 mole fraction [-] *)
    rFraction_N2_Out                : REAL := 0.7835;            (* Normalized dry off-gas N2 mole fraction [-] *)
    rInertGasRatio                  : REAL := 1.0084;            (* N2 inert balance correction factor [-] *)
    rSpecific_qO2_pmol_cell_d       : REAL := 0.220;             (* Specific cellular oxygen uptake rate [pmol/(cell*day)] *)
    rSpecific_qCO2_pmol_cell_d      : REAL := 0.245;             (* Specific cellular CO2 evolution rate [pmol/(cell*day)] *)

    (* ================================================================================================== *)
    (* HYDRODYNAMICS & TFF MEMBRANE HYDRAULIC INTERNAL VARIABLES                                         *)
    (* ================================================================================================== *)
    rRevPerSec                      : REAL := 2.00;              (* Agitator rotational frequency [rev/s] *)
    rAgitatorPower_W                : REAL := 24.5;              (* Shaft net power dissipated into broth liquid [W] *)
    rKinematicVisc_m2_s             : REAL := 1.122E-6;          (* Kinematic fluid broth viscosity [m^2/s] *)
    rTurbulentDissipation_W_kg      : REAL := 0.0544;            (* Local energy dissipation per unit mass [W/kg] *)
    rReynoldsNum                    : REAL := 145000.0;          (* Impeller turbulent Reynolds number [-] *)
    rSuperficialGasVel_m_s          : REAL := 0.000184;          (* Bioreactor superficial sparge gas velocity [m/s] *)
    rPermeateFlow_m3_s              : REAL := 0.0000104;         (* Permeate volumetric flow rate [m^3/s] *)
    rPermeateFlux_LMH               : REAL := 15.00;             (* Permeate area-specific flux [L/(m^2*h)] *)
    rRetentateCircFlow_Lph          : REAL := 320.0;             (* TFF recirculation cross-flow delivery pump [L/h] *)
    rRetentateCircFlow_m3_s         : REAL := 0.0000889;         (* TFF recirculation cross-flow delivery pump [m^3/s] *)
    rLumenAreaTotal_m2              : REAL := 0.001060;          (* Total cross-sectional area of hollow fibers [m^2] *)
    rRetentateVelocity_m_s          : REAL := 0.0838;            (* Crossflow linear fluid velocity inside fiber lumen [m/s] *)

    (* ================================================================================================== *)
    (* CELLULAR METABOLIC KINETIC INTERMEDIATE ACCUMULATORS                                              *)
    (* ================================================================================================== *)
    rMu_Gross                       : REAL := 0.0350;            (* Uninhibited gross specific growth rate [h^-1] *)
    rMu_Net                         : REAL := 0.0320;            (* Net cellular growth rate (mu - kd) [h^-1] *)
    rKd_Total                       : REAL := 0.0030;            (* Toxic metabolite accelerated death rate [h^-1] *)
    rFactor_Temp                    : REAL := 1.00;              (* Arrhenius-Gaussian temperature kinetic scaling [-] *)
    rFactor_PH                      : REAL := 1.00;              (* Enzymatic Gaussian pH kinetic scaling [-] *)
    rMonod_Glc                      : REAL := 0.950;             (* Glucose Monod saturation fraction [-] *)
    rMonod_Gln                      : REAL := 0.920;             (* Glutamine Monod saturation fraction [-] *)
    rInhib_Lac                      : REAL := 0.880;             (* Lactate non-competitive inhibition fraction [-] *)
    rInhib_Amm                      : REAL := 0.910;             (* Ammonia non-competitive inhibition fraction [-] *)
    rRate_qGlc                      : REAL := 0.000280;          (* Specific glucose consumption rate [g/(10^6 cells*h)] *)
    rRate_qGln                      : REAL := 0.000058;          (* Specific glutamine consumption rate [mmol/(10^6 cells*h)] *)
    rRate_qLac                      : REAL := 0.000201;          (* Specific lactate secretion rate [g/(10^6 cells*h)] *)
    rRate_qAmm                      : REAL := 0.000026;          (* Specific ammonia secretion rate [mmol/(10^6 cells*h)] *)
    rRate_qp                        : REAL := 0.001630;          (* Specific mAb antibody production rate [g/(10^6 cells*h)] *)
    rPerfusionDilution_h_inv        : REAL := 0.04167;           (* Perfusion feed dilution rate D_feed [h^-1] *)
    rPermeateDilution_h_inv         : REAL := 0.03889;           (* Clarified harvest permeate dilution rate D_perm [h^-1] *)
    rBleedDilution_h_inv            : REAL := 0.00278;           (* Automated biomass cell bleed dilution rate D_bleed [h^-1] *)

    (* ================================================================================================== *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL OPTIMIZER VARIABLES                                     *)
    (* ================================================================================================== *)
    idx_i                           : INT := 1;                  (* Loop index i *)
    idx_j                           : INT := 1;                  (* Loop index j *)
    idx_k                           : INT := 1;                  (* Loop index k *)
    idx_step                        : INT := 1;                  (* Prediction horizon step index *)
    idx_iter                        : INT := 1;                  (* Projected gradient descent iteration counter *)
    rAlphaStep                      : REAL := 0.0125;            (* Gradient descent learning rate parameter [-] *)
    rCostJ                          : REAL := 0.0;               (* Quadratic cost performance index accumulator *)
    rPredStateSum                   : REAL := 0.0;               (* Inner product temporary scalar accumulator *)

    (* ================================================================================================== *)
    (* ASYMMETRIC pH, TEMPERATURE & DISSOLVED OXYGEN PID REGULATORS                                       *)
    (* ================================================================================================== *)
    rErr_pH                         : REAL := 0.0;               (* Broth pH tracking error [pH units] *)
    rInteg_pH                       : REAL := 0.0;               (* Broth pH anti-windup discrete integral accumulator *)
    rDeriv_pH                       : REAL := 0.0;               (* Broth pH rate-of-change filtered derivative *)
    rErr_pH_Old                     : REAL := 0.0;               (* Broth pH previous step error register *)
    rPID_pH_Out                     : REAL := 0.0;               (* Split-range dual pH controller output [-1.0 to +1.0] *)
    rErr_Temp                       : REAL := 0.0;               (* Broth temperature tracking error [deg C] *)
    rInteg_Temp                     : REAL := 0.0;               (* Broth temperature anti-windup discrete integral *)
    rDeriv_Temp                     : REAL := 0.0;               (* Broth temperature rate-of-change derivative *)
    rErr_Temp_Old                   : REAL := 0.0;               (* Broth temperature previous step error register *)
    rPID_Temp_Out                   : REAL := 0.0;               (* Split-range dual TCU heating/cooling output [-1.0 to +1.0] *)
    rErr_DO                         : REAL := 0.0;               (* Dissolved oxygen tracking error [% air sat] *)
    rInteg_DO                       : REAL := 0.0;               (* Dissolved oxygen anti-windup discrete integral *)
    rDeriv_DO                       : REAL := 0.0;               (* Dissolved oxygen filtered derivative *)
    rErr_DO_Old                     : REAL := 0.0;               (* Dissolved oxygen previous step error register *)
    rPID_DO_Out                     : REAL := 0.0;               (* Master oxygen demand cascade output [0.0 to 1.0] *)

    (* ================================================================================================== *)
    (* FINITE STATE MACHINE (FSM) TIMERS, FLAGS & ACCUMULATORS                                           *)
    (* ================================================================================================== *)
    tStateTimer                     : TON;                       (* Active state elapsed dwell timer *)
    tLeakHoldTimer                  : TON;                       (* Single-use bag pressure decay qualification timer *)
    tBackflushCycleTimer            : TON;                       (* TFF automated reverse backflush pacing timer *)
    tBackflushPulseTimer            : TON;                       (* TFF automated reverse pulse duration timer *)
    tAntifoamLockoutTimer           : TON;                       (* Antifoam chemical shot interlock pause timer *)
    tAntifoamShotTimer              : TON;                       (* Antifoam injection pulse duration timer *)
    tInoculationTimer               : TON;                       (* Seed train aseptic inoculation transfer timer *)
    tNeutralizationTimer            : TON;                       (* In-line biowaste caustic neutralization flush timer *)
    rBagLeakStartPress_mbar         : REAL := 0.0;               (* Initial pressure recorded at start of leak test [mbar] *)
    rBagLeakDecay_mbar              : REAL := 0.0;               (* Evaluated pressure drop across hold duration [mbar] *)
    bBackflushActive                : BOOL := FALSE;             (* Membrane reverse backflush active status flag [bool] *)
    bAntifoamActive                 : BOOL := FALSE;             (* Antifoam dosing stroke active status flag [bool] *)
    bInoculationComplete            : BOOL := FALSE;             (* Seed train cell transfer complete confirmation [bool] *)
    rCumulativeHarvest_kg           : REAL := 0.0;               (* Cumulative mAb permeate collected in current tote [kg] *)
    rPerfusionRamp_VVD              : REAL := 0.20;              (* Dynamic ramp-up perfusion rate setpoint [d^-1] *)
    rChemostatBleedSetpoint_Lph     : REAL := 0.0;               (* Reconciled chemostat biomass bleed flow rate [L/h] *)

    (* ================================================================================================== *)
    (* ISA-18.2 MULTI-TIERED ALARMS: DEBOUNCE TIMERS, HYSTERESIS & STATUS BITS                           *)
    (* ================================================================================================== *)
    c_rDO_HH_Limit                  : REAL := 90.0;              (* Dissolved oxygen critical high limit [% air sat] *)
    c_rDO_H_Limit                   : REAL := 70.0;              (* Dissolved oxygen warning high limit [% air sat] *)
    c_rDO_L_Limit                   : REAL := 30.0;              (* Dissolved oxygen warning low limit [% air sat] *)
    c_rDO_LL_Limit                  : REAL := 15.0;              (* Dissolved oxygen critical low limit [% air sat] *)
    c_rDO_Deadband                  : REAL := 2.0;               (* Dissolved oxygen alarm deadband hysteresis [% air sat] *)
    c_rPH_HH_Limit                  : REAL := 7.45;              (* Broth pH critical alkaline excursion limit [pH units] *)
    c_rPH_H_Limit                   : REAL := 7.20;              (* Broth pH warning alkaline limit [pH units] *)
    c_rPH_L_Limit                   : REAL := 6.85;              (* Broth pH warning acid limit [pH units] *)
    c_rPH_LL_Limit                  : REAL := 6.60;              (* Broth pH critical acid excursion limit [pH units] *)
    c_rPH_Deadband                  : REAL := 0.05;              (* Broth pH alarm deadband hysteresis [pH units] *)
    c_rTemp_HH_Limit                : REAL := 38.5;              (* Broth temperature critical heat limit [deg C] *)
    c_rTemp_H_Limit                 : REAL := 37.5;              (* Broth temperature warning heat limit [deg C] *)
    c_rTemp_L_Limit                 : REAL := 36.2;              (* Broth temperature warning cold limit [deg C] *)
    c_rTemp_LL_Limit                : REAL := 35.0;              (* Broth temperature critical cold limit [deg C] *)
    c_rTemp_Deadband                : REAL := 0.20;              (* Broth temperature deadband hysteresis [deg C] *)
    c_rPress_Bag_HH_Limit           : REAL := 65.0;              (* Headspace pressure burst disk rupture limit [mbar] *)
    c_rPress_Bag_H_Limit            : REAL := 45.0;              (* Headspace pressure warning inflation limit [mbar] *)
    c_rPress_Bag_Deadband           : REAL := 5.0;               (* Headspace pressure alarm deadband [mbar] *)
    c_rTMP_HH_Limit                 : REAL := 550.0;             (* TFF transmembrane pressure irreversible fouling [mbar] *)
    c_rTMP_H_Limit                  : REAL := 420.0;             (* TFF transmembrane pressure backflush trigger [mbar] *)
    c_rTMP_Deadband                 : REAL := 20.0;              (* TFF transmembrane pressure alarm deadband [mbar] *)
    c_rWeight_HH_Limit              : REAL := 530.0;             (* Skid weight critical overflow limit [kg] *)
    c_rWeight_H_Limit               : REAL := 510.0;             (* Skid weight high warning limit [kg] *)
    c_rWeight_L_Limit               : REAL := 350.0;             (* Skid weight low warning limit [kg] *)
    c_rWeight_LL_Limit              : REAL := 100.0;             (* Skid weight empty kettle critical limit [kg] *)
    c_rWeight_Deadband              : REAL := 5.0;               (* Skid weight alarm deadband hysteresis [kg] *)
    tAlarmDebounce_DO_LL            : TON;                       (* Debounce timer for DO LL alarm *)
    tAlarmDebounce_DO_HH            : TON;                       (* Debounce timer for DO HH alarm *)
    tAlarmDebounce_PH_LL            : TON;                       (* Debounce timer for pH LL alarm *)
    tAlarmDebounce_PH_HH            : TON;                       (* Debounce timer for pH HH alarm *)
    tAlarmDebounce_Temp_LL          : TON;                       (* Debounce timer for Temp LL alarm *)
    tAlarmDebounce_Temp_HH          : TON;                       (* Debounce timer for Temp HH alarm *)
    tAlarmDebounce_Press_HH         : TON;                       (* Debounce timer for Bag Pressure HH alarm *)
    tAlarmDebounce_TMP_HH           : TON;                       (* Debounce timer for TFF TMP HH alarm *)
    tAlarmDebounce_Weight_HH        : TON;                       (* Debounce timer for Weight HH alarm *)
    tAlarmDebounce_FoamPersistent   : TON;                       (* Debounce timer for foaming runaway alarm *)
    tAlarmDebounce_AgitatorDecouple : TON;                       (* Debounce timer for mag-lev coupling fault *)
END_VAR"""
