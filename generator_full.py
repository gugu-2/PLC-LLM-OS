# Complete python generator for FB_Biopharma_PerfusionBioreactor_ATF_OffGas
import os
import sys
import json
import uuid

def generate_iec_block():
    lines = []
    
    # -------------------------------------------------------------------------
    # HEADER & SYSTEM SPECIFICATION
    # -------------------------------------------------------------------------
    lines.append("""FUNCTION_BLOCK FB_Biopharma_PerfusionBioreactor_ATF_OffGas
(*
========================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL BIOPHARMACEUTICAL CONTINUOUS PROCESSING DIVISION
TARGET SYSTEM: COMMERCIAL 25,000-L MAMMALIAN CELL MONOCLONAL ANTIBODY BIOREACTOR & ATF PERFUSION SKID
========================================================================================================
SYSTEM ARCHITECTURE SPECIFICATION:
  - Bioreactor Core: 25,000-L gross volume (20,000-L nominal working broth volume) 316L electropolished
    stainless steel vessel (Ra < 0.38 um), dual elephant-ear axial low-shear impellers, bottom-mounted
    magnetic drive coupling with sterile double mechanical condensate-flushed barrier seal.
  - Alternating Tangential Flow (ATF) Perfusion Retention Skid: ATF-10 system featuring 0.2 um polyethersulfone
    (PES) hollow-fiber membrane modules (11.5 m2 filtration area per module, multi-housing array), pneumatic
    reciprocating diaphragm displacement creating high-frequency bi-directional tangential broth shear across
    membrane lumen, minimizing cellular cake formation and shear-induced cell lysis (LDH < 120 U/L).
  - Dynamic Transmembrane Pressure (TMP) & Antifouling Backpulse: Continuous monitoring of feed, retentate,
    and permeate differential pressures. Integrated high-pressure reverse permeate sterile backpulse cycle
    (4.5 bar, 1.5 s burst) triggered on fouling cake resistance thresholds to restore transmembrane flux.
  - 4-Gas Mass Flow Cascade Sparging: Micro-sparging array (15 um porous sintered stainless steel frit)
    delivering pure Oxygen (O2) and Carbon Dioxide (CO2) for micro-bubble gas transfer efficiency; macro-sparging
    ring (1.5 mm drilled orifices) delivering sterile Process Air and Nitrogen (N2) for bulk volumetric gas
    balance and dissolved CO2 stripping without shear-induced cell damage.
  - Respirometric Off-Gas Mass Spectrometer Analysis: Triple-sample capillary quad mass spectrometer
    continuously quantifying exhaust gas mole fractions of O2, CO2, Ar, and N2. Real-time respirometric
    kinetics computation: Oxygen Uptake Rate (OUR), Carbon Dioxide Evolution Rate (CER), and Respiratory
    Quotient (RQ = CER / OUR) to detect metabolic shifts between glycolysis and oxidative phosphorylation.
  - In-Line Laser Raman Spectroscopy & Chemometrics: 785 nm stabilized excitation laser immersion sapphire
    probe with multivariate Partial Least Squares (PLS) chemometric models predicting real-time Viable Cell
    Density (VCD > 90 x 10^6 cells/mL), Glucose substrate concentration, and Lactate metabolite accumulation.
  - Cyber-Physical Mathematical Core:
    * 8-State discrete state-space formulation at Ts = 10 ms: x[k+1] = A*x[k] + B*u[k].
    * Receding-Horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional (Q, R, S, P)
      and Projected Gradient Descent (PGD) optimizer subject to hard actuator limits and dynamic slew constraints.
    * 2oo3 Triple Modular Redundancy (TMR) voting across 5 critical sensor channels with discrepancy timers.
    * 14-Stage deterministic production Finite State Machine (FSM) covering CIP, SIP (F0 >= 30), media fill,
      inoculation, exponential batch, perfusion cut-in, steady-state chemostat, backpulse, bleed, and biokill.
    * ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate-of-Change) with 32-bit status word telemetry.
========================================================================================================
*)
VAR_INPUT
    (* Master Execution & Safety Permissives *)
    bEnable : BOOL; (* [bool] Master Function Block Execution Enable *)
    bAcknowledgeAlarms : BOOL; (* [bool] Global Alarm Acknowledgment & Trip Reset *)
    bStartProduction : BOOL; (* [bool] Operator Production Campaign Start Command *)
    bEmergencyStop : BOOL; (* [bool] Emergency Stop Hardwired Safety Interlock (Normally Closed) *)
    bManualBackpulseTrigger : BOOL; (* [bool] Manual Operator ATF Membrane Backpulse Command *)
    bCIP_SupplyPermissive : BOOL; (* [bool] Central Clean-In-Place Skid Ready & Permissive *)
    bSIP_SteamPermissive : BOOL; (* [bool] Saturated Pure Steam Utility Supply Header Permissive [bar] *)
    bHarvestPermissive : BOOL; (* [bool] Downstream Purification Chromatography Capture Permissive *)
    bBleedPermissive : BOOL; (* [bool] Waste Biomass Thermal Neutralization Line Permissive *)

    (* 2oo3 TMR Broth Temperature Sensor Array [deg C] *)
    rTemp_Broth_A : REAL; (* [deg C] Broth Bulk Temperature RTD Pt100 Channel A *)
    rTemp_Broth_B : REAL; (* [deg C] Broth Bulk Temperature RTD Pt100 Channel B *)
    rTemp_Broth_C : REAL; (* [deg C] Broth Bulk Temperature RTD Pt100 Channel C *)
    rTemp_Jacket_Inlet : REAL; (* [deg C] Thermoregulation Jacket Recirculation Supply Temperature *)

    (* 2oo3 TMR Dissolved Oxygen Optical Sensor Array [% air sat] *)
    rDO_Probe_A : REAL; (* [% air sat] Dissolved Oxygen Luminescence Sensor Channel A *)
    rDO_Probe_B : REAL; (* [% air sat] Dissolved Oxygen Luminescence Sensor Channel B *)
    rDO_Probe_C : REAL; (* [% air sat] Dissolved Oxygen Luminescence Sensor Channel C *)

    (* 2oo3 TMR Culture Broth pH Sensor Array [pH] *)
    rPH_Sensor_A : REAL; (* [pH] Culture Broth Pressurized Gel Electrode Channel A *)
    rPH_Sensor_B : REAL; (* [pH] Culture Broth Pressurized Gel Electrode Channel B *)
    rPH_Sensor_C : REAL; (* [pH] Culture Broth Pressurized Gel Electrode Channel C *)

    (* 2oo3 TMR ATF Filtration Pressure Transmitter Array [bar] *)
    rPressure_ATF_Feed_A : REAL; (* [bar] ATF Hollow-Fiber Inlet Feed Pressure Sensor Channel A *)
    rPressure_ATF_Feed_B : REAL; (* [bar] ATF Hollow-Fiber Inlet Feed Pressure Sensor Channel B *)
    rPressure_ATF_Feed_C : REAL; (* [bar] ATF Hollow-Fiber Inlet Feed Pressure Sensor Channel C *)
    rPressure_ATF_Retentate : REAL; (* [bar] ATF Hollow-Fiber Retentate Return Pressure Transmitter *)
    rPressure_ATF_Permeate : REAL; (* [bar] ATF Hollow-Fiber Permeate Filtrate Line Pressure Transmitter *)
    rPressure_Headspace : REAL; (* [bar] Bioreactor Headspace Static Sterile Pressure Transmitter *)

    (* 2oo3 TMR Respirometric Off-Gas Mass Spectrometer Analyzers [% vol] *)
    rOffGas_O2_A : REAL; (* [% vol] Exhaust Gas Mass Spectrometer O2 Mole Fraction Channel A *)
    rOffGas_O2_B : REAL; (* [% vol] Exhaust Gas Mass Spectrometer O2 Mole Fraction Channel B *)
    rOffGas_O2_C : REAL; (* [% vol] Exhaust Gas Mass Spectrometer O2 Mole Fraction Channel C *)
    rOffGas_CO2_A : REAL; (* [% vol] Exhaust Gas Mass Spectrometer CO2 Mole Fraction Channel A *)
    rOffGas_CO2_B : REAL; (* [% vol] Exhaust Gas Mass Spectrometer CO2 Mole Fraction Channel B *)
    rOffGas_CO2_C : REAL; (* [% vol] Exhaust Gas Mass Spectrometer CO2 Mole Fraction Channel C *)

    (* Gas Supply Header & Inlet Blending Composition *)
    rInletGas_O2_Pct : REAL; (* [% vol] Blended Inlet Sparging Gas O2 Mole Fraction *)
    rInletGas_CO2_Pct : REAL; (* [% vol] Blended Inlet Sparging Gas CO2 Mole Fraction *)
    rTotalInletGasFlow_NLmin : REAL; (* [NL/min] Total Header Inlet Sparging Gas Mass Flow *)

    (* In-Line Laser Raman Spectroscopy Chemometric Feedbacks *)
    rRaman_VCD_Raw : REAL; (* [10^6 cells/mL] In-Line Laser Raman Viable Cell Density Feedback *)
    rRaman_Glucose_Raw : REAL; (* [g/L] In-Line Laser Raman Glucose Substrate Feedback *)
    rRaman_Lactate_Raw : REAL; (* [g/L] In-Line Laser Raman Lactate Toxic Metabolite Feedback *)
    rRaman_Titer_Raw : REAL; (* [g/L] In-Line Laser Raman Monoclonal Antibody Product Titer *)
    bRaman_SignalValid : BOOL; (* [bool] In-Line Raman Spectrometer Spectral Quality Permissive *)

    (* Mechanical, Utility & Physical Measurements *)
    rVesselWeight_kg : REAL; (* [kg] Bioreactor Total Gross Mass Load Cell Sum *)
    rAgitatorSpeed_Feedback : REAL; (* [rpm] Agitator Servomotor Encoder Speed Feedback *)
    rSteamHeaderPressure_bar : REAL; (* [bar] Clean Utility Pure Steam Supply Header Pressure *)
    rGlycolSupplyTemp_degC : REAL; (* [deg C] Chilled Glycol Header Supply Temperature *)
    rWFI_Conductivity_uScm : REAL; (* [uS/cm] Water-For-Injection Rinse Final Conductivity *)
END_VAR
VAR_OUTPUT
    (* Continuous Actuator Manipulated Value Commands *)
    rCmd_JacketControl_Pct : REAL; (* [%] Thermoregulation Jacket Valve (-100.0% Full Chilled Glycol to +100.0% Full Steam) *)
    rCmd_SpargerO2_Flow : REAL; (* [NL/min] Pure O2 Micro-Sparger Mass Flow Controller Flow Setpoint *)
    rCmd_SpargerCO2_Flow : REAL; (* [NL/min] CO2 Acid Micro-Sparger Mass Flow Controller Flow Setpoint *)
    rCmd_SpargerAir_Flow : REAL; (* [NL/min] Sterile Process Air Macro-Sparger MFC Flow Setpoint *)
    rCmd_SpargerN2_Flow : REAL; (* [NL/min] Nitrogen Headspace Blanket / Stripping MFC Setpoint *)
    rCmd_BasePump_Flow : REAL; (* [mL/min] Alkaline Neutralization Base Titration Peristaltic Pump Setpoint *)
    rCmd_NutrientFeed_Flow : REAL; (* [L/h] Concentrated Nutrient Feed Medium Peristaltic Pump Rate *)
    rCmd_ATF_CycleRate : REAL; (* [cpm] ATF Reciprocating Diaphragm Displacement Frequency *)
    rCmd_PermeateHarvest_Flow : REAL; (* [L/h] Continuous Perfusion Permeate Harvest Extraction Pump Rate *)
    rCmd_BleedPump_Flow : REAL; (* [L/h] Automated Excess Cell Biomass Bleed Pump Rate *)
    rCmd_AgitatorSpeed_RPM : REAL; (* [rpm] Dual Elephant-Ear Impeller Speed Setpoint *)

    (* Discrete Valve & Actuator State Commands *)
    bCmd_BackpulseValve_Open : BOOL; (* [bool] High-Pressure Sterile Permeate Backpulse Diaphragm Valve Command *)
    bCmd_CIP_SupplyValve : BOOL; (* [bool] CIP Supply Header Block Valve Command *)
    bCmd_SIP_PureSteamValve : BOOL; (* [bool] SIP Saturated Pure Steam Inlet Valve Command *)
    bCmd_SIP_CondensateDrainValve : BOOL; (* [bool] SIP Vessel Bottom Condensate Drain Trap Bypass Valve *)
    bCmd_SterileVentValve : BOOL; (* [bool] Bioreactor Headspace Sterile Exhaust Vent Valve *)

    (* Voted & Validated Process Variables *)
    rVal_Voted_Temp : REAL; (* [deg C] 2oo3 TMR Voted Broth Bulk Temperature *)
    rVal_Voted_DO : REAL; (* [% air sat] 2oo3 TMR Voted Dissolved Oxygen Percentage *)
    rVal_Voted_PH : REAL; (* [pH] 2oo3 TMR Voted Culture Broth pH *)
    rVal_Calculated_TMP : REAL; (* [bar] ATF Hollow-Fiber Membrane Transmembrane Pressure *)
    rVal_Calculated_OUR : REAL; (* [mmol/L/h] Respirometric Oxygen Uptake Rate *)
    rVal_Calculated_CER : REAL; (* [mmol/L/h] Respirometric Carbon Dioxide Evolution Rate *)
    rVal_Calculated_RQ : REAL; (* [-] Calculated Respiratory Quotient (CER / OUR) *)
    rVal_Estimated_VCD : REAL; (* [10^6 cells/mL] Cyber-Physical Observer Estimated Viable Cell Density *)
    rVal_Estimated_Glucose : REAL; (* [g/L] Cyber-Physical Observer Estimated Glucose Concentration *)
    rVal_Estimated_Lactate : REAL; (* [g/L] Cyber-Physical Observer Estimated Lactate Accumulation *)
    rVal_Accumulated_F0 : REAL; (* [min] Integrated Thermal SIP Lethality F0 Value *)
    rVal_PerfusionRate_VVD : REAL; (* [vessel vol/day] Normalized Volumetric Perfusion Exchange Rate *)

    (* Process Execution Status & Bit-Packed Diagnostics *)
    iActiveState : INT; (* [-] Current Operational Finite State Machine State Index (0..14) *)
    wAlarmWord_Critical_HH : DWORD; (* [-] Bit-Packed ISA-18.2 Critical Emergency Shutdown Alarms *)
    wAlarmWord_Warning_H : DWORD; (* [-] Bit-Packed ISA-18.2 Process Operational Warnings *)
    wSensorHealthStatusWord : DWORD; (* [-] Bit-Packed 2oo3 TMR Sensor Channel Diagnostic Fault Status *)
    wAutomationStatusWord : DWORD; (* [-] Bit-Packed Process Automation & Interlock Permissive Status *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR BLOCK (Internal state, matrices, TMR variables, MPC weights, FSM, Alarms)
    # -------------------------------------------------------------------------
    lines.append("""VAR
    (* Execution Scan Timing Constant *)
    rScanTime : REAL := 0.010; (* [s] Periodic Cyclic Task Scan Interval (10 ms) *)

    (* Cyber-Physical State Vectors (8 States: 1:Temp, 2:DO, 3:pH, 4:VCD, 5:Glc, 6:Lac, 7:TMP, 8:CER) *)
    rState_x : ARRAY[1..8] OF REAL; (* Internal Estimated State Vector x[k] *)
    rState_x_pred : ARRAY[1..8] OF REAL; (* One-Cycle Ahead Predicted State Vector x[k+1] *)
    rState_x_hat : ARRAY[1..8] OF REAL; (* Observer Corrected State Vector x_hat[k] *)
    rState_x_ref : ARRAY[1..8] OF REAL; (* Closed-Loop Setpoint Reference Trajectory Vector *)
    rInnov_y : ARRAY[1..8] OF REAL; (* Observer Innovation Residual Vector y_meas - y_pred *)

    (* Actuator Manipulated Vectors (8 Actuators: 1:Jacket, 2:O2, 3:CO2, 4:Air, 5:Base, 6:Feed, 7:ATF, 8:Perm) *)
    rControl_u : ARRAY[1..8] OF REAL; (* Current Optimal Control Command Vector u[k] *)
    rControl_u_prev : ARRAY[1..8] OF REAL; (* Previous Cycle Actuator Vector u[k-1] *)
    rControl_u_target : ARRAY[1..8] OF REAL; (* Desired Actuator Operating Equilibrium Vector *)
    rDelta_u : ARRAY[1..8] OF REAL; (* Actuator Slew Rate Vector Delta_u[k] *)
    rU_cand : ARRAY[1..8] OF REAL; (* MPC Candidate Control Vector in Optimization Loop *)
    rGrad_J : ARRAY[1..8] OF REAL; (* Cost Functional Gradient Vector dJ/du *)

    (* Actuator Physical Saturation & Slew Limits *)
    rU_Min : ARRAY[1..8] OF REAL; (* Lower Box Bound on Manipulated Actuators *)
    rU_Max : ARRAY[1..8] OF REAL; (* Upper Box Bound on Manipulated Actuators *)
    rDeltaU_Max : ARRAY[1..8] OF REAL; (* Maximum Allowable Actuator Slew Rate Per Scan Cycle *)

    (* Discrete State-Space System Matrices (Ts = 10 ms) *)
    rMatA : ARRAY[1..8, 1..8] OF REAL; (* 8x8 State Dynamics Transition Matrix A_d *)
    rMatB : ARRAY[1..8, 1..8] OF REAL; (* 8x8 Input Coupling Matrix B_d *)
    rMatC : ARRAY[1..8, 1..8] OF REAL; (* 8x8 Output Measurement Matrix C_d *)
    rMatL : ARRAY[1..8, 1..8] OF REAL; (* 8x8 Luenberger Observer / EKF Gain Matrix L *)

    (* Model Predictive Control (MPC) Penalty Matrices *)
    rMatQ : ARRAY[1..8] OF REAL; (* State Tracking Error Diagonal Weighting Matrix Q *)
    rMatR : ARRAY[1..8] OF REAL; (* Actuator Effort Penalty Diagonal Weighting Matrix R *)
    rMatS : ARRAY[1..8] OF REAL; (* Actuator Slew Rate Penalty Diagonal Weighting Matrix S *)
    rMatP : ARRAY[1..8] OF REAL; (* Terminal State Cost Diagonal Weighting Matrix P *)

    (* MPC Trajectory Prediction Buffer (5-Step Prediction Horizon Np = 5) *)
    rPred_Traj : ARRAY[1..5, 1..8] OF REAL; (* Multi-Step Forward Predicted State Trajectory *)

    (* 2oo3 TMR Voting Variables: Broth Temperature RTD Pt100 *)
    rMedian_Temp : REAL;
    rDiff_Temp_A : REAL;
    rDiff_Temp_B : REAL;
    rDiff_Temp_C : REAL;
    rTimer_Temp_A : REAL := 0.0;
    rTimer_Temp_B : REAL := 0.0;
    rTimer_Temp_C : REAL := 0.0;
    bFault_Temp_A : BOOL := FALSE;
    bFault_Temp_B : BOOL := FALSE;
    bFault_Temp_C : BOOL := FALSE;
    rVoted_Temp_Raw : REAL;
    rVoted_Temp_LastGood : REAL := 37.0;
    iHealthy_Temp : INT;

    (* 2oo3 TMR Voting Variables: Dissolved Oxygen Optical Luminescence *)
    rMedian_DO : REAL;
    rDiff_DO_A : REAL;
    rDiff_DO_B : REAL;
    rDiff_DO_C : REAL;
    rTimer_DO_A : REAL := 0.0;
    rTimer_DO_B : REAL := 0.0;
    rTimer_DO_C : REAL := 0.0;
    bFault_DO_A : BOOL := FALSE;
    bFault_DO_B : BOOL := FALSE;
    bFault_DO_C : BOOL := FALSE;
    rVoted_DO_Raw : REAL;
    rVoted_DO_LastGood : REAL := 50.0;
    iHealthy_DO : INT;

    (* 2oo3 TMR Voting Variables: Culture Broth pH Pressurized Gel *)
    rMedian_PH : REAL;
    rDiff_PH_A : REAL;
    rDiff_PH_B : REAL;
    rDiff_PH_C : REAL;
    rTimer_PH_A : REAL := 0.0;
    rTimer_PH_B : REAL := 0.0;
    rTimer_PH_C : REAL := 0.0;
    bFault_PH_A : BOOL := FALSE;
    bFault_PH_B : BOOL := FALSE;
    bFault_PH_C : BOOL := FALSE;
    rVoted_PH_Raw : REAL;
    rVoted_PH_LastGood : REAL := 7.05;
    iHealthy_PH : INT;

    (* 2oo3 TMR Voting Variables: ATF Hollow-Fiber Inlet Feed Pressure *)
    rMedian_FeedPress : REAL;
    rDiff_FeedPress_A : REAL;
    rDiff_FeedPress_B : REAL;
    rDiff_FeedPress_C : REAL;
    rTimer_FeedPress_A : REAL := 0.0;
    rTimer_FeedPress_B : REAL := 0.0;
    rTimer_FeedPress_C : REAL := 0.0;
    bFault_FeedPress_A : BOOL := FALSE;
    bFault_FeedPress_B : BOOL := FALSE;
    bFault_FeedPress_C : BOOL := FALSE;
    rVoted_FeedPress_Raw : REAL;
    rVoted_FeedPress_LastGood : REAL := 0.45;
    iHealthy_FeedPress : INT;

    (* 2oo3 TMR Voting Variables: Off-Gas Exhaust Mass Spectrometer *)
    rMedian_OffGas_O2 : REAL;
    rDiff_OffGas_O2_A : REAL;
    rDiff_OffGas_O2_B : REAL;
    rDiff_OffGas_O2_C : REAL;
    rTimer_OffGas_O2_A : REAL := 0.0;
    rTimer_OffGas_O2_B : REAL := 0.0;
    rTimer_OffGas_O2_C : REAL := 0.0;
    bFault_OffGas_O2_A : BOOL := FALSE;
    bFault_OffGas_O2_B : BOOL := FALSE;
    bFault_OffGas_O2_C : BOOL := FALSE;
    rVoted_OffGas_O2_Raw : REAL;
    rVoted_OffGas_O2_LastGood : REAL := 18.5;

    rMedian_OffGas_CO2 : REAL;
    rDiff_OffGas_CO2_A : REAL;
    rDiff_OffGas_CO2_B : REAL;
    rDiff_OffGas_CO2_C : REAL;
    rTimer_OffGas_CO2_A : REAL := 0.0;
    rTimer_OffGas_CO2_B : REAL := 0.0;
    rTimer_OffGas_CO2_C : REAL := 0.0;
    bFault_OffGas_CO2_A : BOOL := FALSE;
    bFault_OffGas_CO2_B : BOOL := FALSE;
    bFault_OffGas_CO2_C : BOOL := FALSE;
    rVoted_OffGas_CO2_Raw : REAL;
    rVoted_OffGas_CO2_LastGood : REAL := 4.2;

    (* 2oo3 Discrepancy Limits & Debounce Trip Thresholds *)
    rLimit_Discrepancy_Temp : REAL := 0.60; (* [deg C] Discrepancy Tolerance for Temperature Channels *)
    rLimit_Discrepancy_DO : REAL := 6.50; (* [% air sat] Discrepancy Tolerance for DO Probes *)
    rLimit_Discrepancy_PH : REAL := 0.18; (* [pH] Discrepancy Tolerance for pH Electrodes *)
    rLimit_Discrepancy_FeedPress : REAL := 0.12; (* [bar] Discrepancy Tolerance for ATF Feed PT *)
    rLimit_Discrepancy_OffGas : REAL := 0.40; (* [% vol] Discrepancy Tolerance for Mass Spec Analyzers *)
    rTime_Discrepancy_Trip : REAL := 2.50; (* [s] Sustained Discrepancy Duration to Latch Channel Fault *)

    (* Low-Pass Filter Smoothing Coefficients *)
    rFilterAlpha_Temp : REAL := 0.08;
    rFilterAlpha_DO : REAL := 0.12;
    rFilterAlpha_PH : REAL := 0.10;
    rFilterAlpha_TMP : REAL := 0.15;
    rFilterAlpha_CER : REAL := 0.05;

    (* Respirometric Off-Gas Intermediates *)
    rDryInlet_O2_Fract : REAL;
    rDryInlet_CO2_Fract : REAL;
    rDryExhaust_O2_Fract : REAL;
    rDryExhaust_CO2_Fract : REAL;
    rInertRatio : REAL;
    rMolarGasVolume : REAL := 22.414; (* [NL/mol] Standard Molar Gas Volume *)

    (* Biophysical & Monod Kinetic Parameters *)
    rMu_Max : REAL := 0.045; (* [1/h] Maximum Specific Cell Growth Rate *)
    rKs_Glucose : REAL := 0.35; (* [g/L] Monod Half-Velocity Glucose Affinity Constant *)
    rKi_Lactate : REAL := 4.20; (* [g/L] Non-Competitive Lactate Inhibition Constant *)
    rYield_X_S : REAL := 2.10e8; (* [cells/g] Biomass Yield per Gram of Glucose *)
    rYield_L_S : REAL := 0.82; (* [g/g] Lactate Yield per Gram of Glucose *)
    rMaint_Glucose : REAL := 0.018; (* [g/g/h] Specific Cellular Maintenance Energy *)
    rSpec_OUR : REAL := 0.285; (* [pmol/cell/day] Cellular Specific Oxygen Uptake *)
    rSpec_CER : REAL := 0.315; (* [pmol/cell/day] Cellular Specific Carbon Dioxide Evolution *)
    rMembraneArea_m2 : REAL := 11.5; (* [m2] ATF Hollow-Fiber Membrane Total Filtration Area *)
    rCleanMembraneResist : REAL := 1.25e11; (* [1/m] Intrinsic Clean Membrane Hydraulic Resistance *)
    rSpecificCakeResist : REAL := 2.80e12; (* [m/kg] Specific Cake Layer Deposition Resistance *)
    rViscosity_Pa_s : REAL := 0.0012; (* [Pa*s] Mammalian Cell Broth Dynamic Viscosity *)

    (* Finite State Machine Operational Registers *)
    eState : INT := 0; (* Active FSM State Variable (0..14) *)
    ePrevState : INT := 0; (* Previous Scan Cycle FSM State *)
    rStateTimer_sec : REAL := 0.0; (* Elapsed Time in Current FSM Operational Stage *)
    iCIP_SubStep : INT := 0; (* Clean-In-Place Internal Sub-Phase Index (0..5) *)
    rCIP_StepTimer_sec : REAL := 0.0; (* CIP Sub-Phase Elapsed Timer *)
    rSIP_HoldTimer_sec : REAL := 0.0; (* Thermal Sterilization High Temperature Dwell Timer *)
    rLethalityRate_L : REAL := 0.0; (* Instantaneous Lethality Rate L = 10^((T-121.1)/10) *)
    rBackpulse_CycleTimer_sec : REAL := 0.0; (* Inter-Backpulse Cumulative Period Timer *)
    rBackpulse_PulseDuration_sec : REAL := 0.0; (* High-Pressure Backpulse Injection Burst Timer *)
    bBackpulseActive : BOOL := FALSE; (* High-Pressure Backpulse Valve Open State Flag *)
    bBackpulseRequired : BOOL := FALSE; (* Antifouling Backpulse Demand Latch *)

    (* Cumulative Volumetric Accounting Registers *)
    rAccumulated_Permeate_Vol_L : REAL := 0.0; (* Total Harvest Permeate Volume Extracted [L] *)
    rAccumulated_Feed_Vol_L : REAL := 0.0; (* Total Concentrated Nutrient Feed Delivered [L] *)
    rAccumulated_Bleed_Vol_L : REAL := 0.0; (* Total Excess Cell Biomass Volume Purged [L] *)
    rVesselBrothVolume_L : REAL := 20000.0; (* Dynamic Vessel Liquid Broth Inventory [L] *)
    rNominalVolume_L : REAL := 20000.0; (* Nominal Vessel Working Setpoint Volume [L] *)

    (* ISA-18.2 Alarm Trip Points & Deadbands *)
    rLimit_Temp_HH : REAL := 40.50; (* [deg C] Critical Broth High-High Temperature Trip *)
    rLimit_Temp_H : REAL := 37.80; (* [deg C] Broth High Temperature Warning *)
    rLimit_Temp_L : REAL := 36.20; (* [deg C] Broth Low Temperature Warning *)
    rLimit_Temp_LL : REAL := 34.00; (* [deg C] Broth Low-Low Temperature Trip *)
    rLimit_Temp_Deadband : REAL := 0.25; (* [deg C] Temperature Alarm Clearance Hysteresis *)

    rLimit_DO_HH : REAL := 85.00; (* [% air sat] Hyperoxia High-High DO Trip *)
    rLimit_DO_H : REAL := 65.00; (* [% air sat] High DO Warning *)
    rLimit_DO_L : REAL := 25.00; (* [% air sat] Hypoxia Low DO Warning *)
    rLimit_DO_LL : REAL := 12.00; (* [% air sat] Severe Anoxia Low-Low DO Trip *)
    rLimit_DO_Deadband : REAL := 2.50; (* [% air sat] DO Alarm Clearance Hysteresis *)

    rLimit_PH_HH : REAL := 7.45; (* [pH] Alkaline Stress High-High pH Trip *)
    rLimit_PH_H : REAL := 7.25; (* [pH] High pH Warning *)
    rLimit_PH_L : REAL := 6.85; (* [pH] Low pH Acid Warning *)
    rLimit_PH_LL : REAL := 6.65; (* [pH] Severe Acidosis Low-Low pH Trip *)
    rLimit_PH_Deadband : REAL := 0.05; (* [pH] pH Alarm Clearance Hysteresis *)

    rLimit_TMP_HH : REAL := 0.85; (* [bar] Critical Membrane High-High Rupture TMP *)
    rLimit_TMP_H : REAL := 0.52; (* [bar] High Fouling TMP Warning (Backpulse Trigger) *)
    rLimit_TMP_Deadband : REAL := 0.04; (* [bar] TMP Alarm Clearance Hysteresis *)

    rLimit_Headspace_HH : REAL := 1.85; (* [bar] Overpressure Safety Rupture Trip *)
    rLimit_Headspace_H : REAL := 1.25; (* [bar] Headspace High Pressure Warning *)
    rLimit_Headspace_L : REAL := 0.08; (* [bar] Headspace Low Pressure (Loss of Sterile Barrier) *)
    rLimit_Headspace_Deadband : REAL := 0.03; (* [bar] Headspace Pressure Hysteresis *)

    rLimit_Glucose_L : REAL := 1.20; (* [g/L] Starvation Risk Low Glucose Warning *)
    rLimit_Glucose_LL : REAL := 0.40; (* [g/L] Critical Cell Starvation Trip *)
    rLimit_Lactate_H : REAL := 3.20; (* [g/L] Cytotoxic Lactate Accumulation Warning *)
    rLimit_Lactate_HH : REAL := 4.80; (* [g/L] Severe Metabolite Toxicity Trip *)
    rLimit_RQ_H : REAL := 1.35; (* [-] Respiratory Quotient Anaerobic Shift Warning *)

    (* Rate-of-Change (ROC) Derivative Monitoring *)
    rPrev_TMP : REAL := 0.20;
    rPrev_DO : REAL := 50.0;
    rPrev_HeadspacePressure : REAL := 0.35;
    rRate_TMP_bar_s : REAL := 0.0;
    rRate_DO_pct_s : REAL := 0.0;
    rRate_Pressure_bar_s : REAL := 0.0;
    rLimit_ROC_TMP_Trip : REAL := 0.045; (* [bar/s] Maximum Permissible TMP Rate of Rise *)
    rLimit_ROC_DO_Trip : REAL := -2.50; (* [%/s] Sudden Oxygen Collapse Rate *)
    rLimit_ROC_Pressure_Trip : REAL := 0.15; (* [bar/s] Rapid Vessel Pressurization Rate *)

    (* Latched Alarm Condition Booleans *)
    bAlarm_Temp_HH : BOOL := FALSE;
    bAlarm_Temp_H : BOOL := FALSE;
    bAlarm_Temp_L : BOOL := FALSE;
    bAlarm_Temp_LL : BOOL := FALSE;
    bAlarm_DO_HH : BOOL := FALSE;
    bAlarm_DO_H : BOOL := FALSE;
    bAlarm_DO_L : BOOL := FALSE;
    bAlarm_DO_LL : BOOL := FALSE;
    bAlarm_PH_HH : BOOL := FALSE;
    bAlarm_PH_H : BOOL := FALSE;
    bAlarm_PH_L : BOOL := FALSE;
    bAlarm_PH_LL : BOOL := FALSE;
    bAlarm_TMP_HH : BOOL := FALSE;
    bAlarm_TMP_H : BOOL := FALSE;
    bAlarm_Headspace_HH : BOOL := FALSE;
    bAlarm_Headspace_H : BOOL := FALSE;
    bAlarm_Headspace_L : BOOL := FALSE;
    bAlarm_Glucose_L : BOOL := FALSE;
    bAlarm_Glucose_LL : BOOL := FALSE;
    bAlarm_Lactate_H : BOOL := FALSE;
    bAlarm_Lactate_HH : BOOL := FALSE;
    bAlarm_RQ_H : BOOL := FALSE;
    bAlarm_ROC_TMP : BOOL := FALSE;
    bAlarm_ROC_DO : BOOL := FALSE;
    bAlarm_ROC_Pressure : BOOL := FALSE;
    bAlarm_VesselWeight_LL : BOOL := FALSE;
    bAlarm_AgitatorSpeed_Dev : BOOL := FALSE;
    bAlarm_AllTempSensorsFailed : BOOL := FALSE;
    bAlarm_AllDOSensorsFailed : BOOL := FALSE;
    bAlarm_AllPHSensorsFailed : BOOL := FALSE;
    bAlarm_AllFeedPressFailed : BOOL := FALSE;
    bAlarm_AllOffGasFailed : BOOL := FALSE;

    (* Loop Counters & Scratchpad Variables *)
    i : INT;
    j : INT;
    k : INT;
    p : INT;
    m : INT;
    iter : INT;
    rTemp_Sum : REAL;
    rTemp_Diff : REAL;
    rSensitivity : REAL;
    rAlpha_PGD : REAL := 0.015; (* Step Size for Projected Gradient Descent *)
    rBiomassNetGrowthRate : REAL;
    rSpecGlcConsumption : REAL;
    rSpecLacProduction : REAL;
    rPermeateFlux_LMH : REAL;
    rCurrentTMP_Pa : REAL;
    rCakeResistance_m : REAL;
    bInitialScanDone : BOOL := FALSE;
END_VAR
""")

    # -------------------------------------------------------------------------
    # PHASE 1: 2oo3 TMR SENSOR VOTING WITH DISCREPANCY TIMERS
    # -------------------------------------------------------------------------
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH SUSTAINED DISCREPANCY TIMERS       *)
(* ==================================================================================================== *)
IF NOT bEnable THEN
    (* Set Safe Zero Commands and Bypass Processing When Block Is Disabled *)
    rCmd_JacketControl_Pct := 0.0;
    rCmd_SpargerO2_Flow := 0.0;
    rCmd_SpargerCO2_Flow := 0.0;
    rCmd_SpargerAir_Flow := 0.0;
    rCmd_SpargerN2_Flow := 0.0;
    rCmd_BasePump_Flow := 0.0;
    rCmd_NutrientFeed_Flow := 0.0;
    rCmd_ATF_CycleRate := 0.0;
    rCmd_PermeateHarvest_Flow := 0.0;
    rCmd_BleedPump_Flow := 0.0;
    rCmd_AgitatorSpeed_RPM := 0.0;
    bCmd_BackpulseValve_Open := FALSE;
    bCmd_CIP_SupplyValve := FALSE;
    bCmd_SIP_PureSteamValve := FALSE;
    bCmd_SIP_CondensateDrainValve := FALSE;
    bCmd_SterileVentValve := TRUE; (* Open Vent to Prevent Vacuum Ingress *)
    wAlarmWord_Critical_HH := 16#00000000;
    wAlarmWord_Warning_H := 16#00000000;
    wSensorHealthStatusWord := 16#00000000;
    wAutomationStatusWord := 16#00000000;
    RETURN;
END_IF;

(* 1.1: 2oo3 TMR BROTH BULK TEMPERATURE RTD Pt100 VOTING *)
IF (rTemp_Broth_A >= rTemp_Broth_B AND rTemp_Broth_A <= rTemp_Broth_C) OR (rTemp_Broth_A <= rTemp_Broth_B AND rTemp_Broth_A >= rTemp_Broth_C) THEN
    rMedian_Temp := rTemp_Broth_A;
ELSIF (rTemp_Broth_B >= rTemp_Broth_A AND rTemp_Broth_B <= rTemp_Broth_C) OR (rTemp_Broth_B <= rTemp_Broth_A AND rTemp_Broth_B >= rTemp_Broth_C) THEN
    rMedian_Temp := rTemp_Broth_B;
ELSE
    rMedian_Temp := rTemp_Broth_C;
END_IF;

rDiff_Temp_A := ABS(rTemp_Broth_A - rMedian_Temp);
rDiff_Temp_B := ABS(rTemp_Broth_B - rMedian_Temp);
rDiff_Temp_C := ABS(rTemp_Broth_C - rMedian_Temp);

(* Channel A Discrepancy Debounce Timer *)
IF rDiff_Temp_A > rLimit_Discrepancy_Temp THEN
    rTimer_Temp_A := rTimer_Temp_A + rScanTime;
    IF rTimer_Temp_A >= rTime_Discrepancy_Trip THEN
        bFault_Temp_A := TRUE;
    END_IF;
ELSE
    rTimer_Temp_A := MAX(0.0, rTimer_Temp_A - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN
        bFault_Temp_A := FALSE;
    END_IF;
END_IF;

(* Channel B Discrepancy Debounce Timer *)
IF rDiff_Temp_B > rLimit_Discrepancy_Temp THEN
    rTimer_Temp_B := rTimer_Temp_B + rScanTime;
    IF rTimer_Temp_B >= rTime_Discrepancy_Trip THEN
        bFault_Temp_B := TRUE;
    END_IF;
ELSE
    rTimer_Temp_B := MAX(0.0, rTimer_Temp_B - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN
        bFault_Temp_B := FALSE;
    END_IF;
END_IF;

(* Channel C Discrepancy Debounce Timer *)
IF rDiff_Temp_C > rLimit_Discrepancy_Temp THEN
    rTimer_Temp_C := rTimer_Temp_C + rScanTime;
    IF rTimer_Temp_C >= rTime_Discrepancy_Trip THEN
        bFault_Temp_C := TRUE;
    END_IF;
ELSE
    rTimer_Temp_C := MAX(0.0, rTimer_Temp_C - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN
        bFault_Temp_C := FALSE;
    END_IF;
END_IF;

(* Degraded Mode Arithmetic Synthesis *)
iHealthy_Temp := 0;
IF NOT bFault_Temp_A THEN iHealthy_Temp := iHealthy_Temp + 1; END_IF;
IF NOT bFault_Temp_B THEN iHealthy_Temp := iHealthy_Temp + 1; END_IF;
IF NOT bFault_Temp_C THEN iHealthy_Temp := iHealthy_Temp + 1; END_IF;

IF iHealthy_Temp = 3 THEN
    rVoted_Temp_Raw := (rTemp_Broth_A + rTemp_Broth_B + rTemp_Broth_C) / 3.0;
    bAlarm_AllTempSensorsFailed := FALSE;
ELSIF iHealthy_Temp = 2 THEN
    bAlarm_AllTempSensorsFailed := FALSE;
    IF bFault_Temp_A THEN
        rVoted_Temp_Raw := (rTemp_Broth_B + rTemp_Broth_C) / 2.0;
    ELSIF bFault_Temp_B THEN
        rVoted_Temp_Raw := (rTemp_Broth_A + rTemp_Broth_C) / 2.0;
    ELSE
        rVoted_Temp_Raw := (rTemp_Broth_A + rTemp_Broth_B) / 2.0;
    END_IF;
ELSIF iHealthy_Temp = 1 THEN
    bAlarm_AllTempSensorsFailed := FALSE;
    IF NOT bFault_Temp_A THEN
        rVoted_Temp_Raw := rTemp_Broth_A;
    ELSIF NOT bFault_Temp_B THEN
        rVoted_Temp_Raw := rTemp_Broth_B;
    ELSE
        rVoted_Temp_Raw := rTemp_Broth_C;
    END_IF;
ELSE
    bAlarm_AllTempSensorsFailed := TRUE;
    rVoted_Temp_Raw := rVoted_Temp_LastGood;
END_IF;

rVoted_Temp_LastGood := rVoted_Temp_Raw;
rVal_Voted_Temp := rVal_Voted_Temp + (rFilterAlpha_Temp * (rVoted_Temp_Raw - rVal_Voted_Temp));

(* 1.2: 2oo3 TMR DISSOLVED OXYGEN OPTICAL LUMINESCENCE PROBES *)
IF (rDO_Probe_A >= rDO_Probe_B AND rDO_Probe_A <= rDO_Probe_C) OR (rDO_Probe_A <= rDO_Probe_B AND rDO_Probe_A >= rDO_Probe_C) THEN
    rMedian_DO := rDO_Probe_A;
ELSIF (rDO_Probe_B >= rDO_Probe_A AND rDO_Probe_B <= rDO_Probe_C) OR (rDO_Probe_B <= rDO_Probe_A AND rDO_Probe_B >= rDO_Probe_C) THEN
    rMedian_DO := rDO_Probe_B;
ELSE
    rMedian_DO := rDO_Probe_C;
END_IF;

rDiff_DO_A := ABS(rDO_Probe_A - rMedian_DO);
rDiff_DO_B := ABS(rDO_Probe_B - rMedian_DO);
rDiff_DO_C := ABS(rDO_Probe_C - rMedian_DO);

IF rDiff_DO_A > rLimit_Discrepancy_DO THEN
    rTimer_DO_A := rTimer_DO_A + rScanTime;
    IF rTimer_DO_A >= rTime_Discrepancy_Trip THEN bFault_DO_A := TRUE; END_IF;
ELSE
    rTimer_DO_A := MAX(0.0, rTimer_DO_A - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_DO_A := FALSE; END_IF;
END_IF;

IF rDiff_DO_B > rLimit_Discrepancy_DO THEN
    rTimer_DO_B := rTimer_DO_B + rScanTime;
    IF rTimer_DO_B >= rTime_Discrepancy_Trip THEN bFault_DO_B := TRUE; END_IF;
ELSE
    rTimer_DO_B := MAX(0.0, rTimer_DO_B - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_DO_B := FALSE; END_IF;
END_IF;

IF rDiff_DO_C > rLimit_Discrepancy_DO THEN
    rTimer_DO_C := rTimer_DO_C + rScanTime;
    IF rTimer_DO_C >= rTime_Discrepancy_Trip THEN bFault_DO_C := TRUE; END_IF;
ELSE
    rTimer_DO_C := MAX(0.0, rTimer_DO_C - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_DO_C := FALSE; END_IF;
END_IF;

iHealthy_DO := 0;
IF NOT bFault_DO_A THEN iHealthy_DO := iHealthy_DO + 1; END_IF;
IF NOT bFault_DO_B THEN iHealthy_DO := iHealthy_DO + 1; END_IF;
IF NOT bFault_DO_C THEN iHealthy_DO := iHealthy_DO + 1; END_IF;

IF iHealthy_DO = 3 THEN
    rVoted_DO_Raw := (rDO_Probe_A + rDO_Probe_B + rDO_Probe_C) / 3.0;
    bAlarm_AllDOSensorsFailed := FALSE;
ELSIF iHealthy_DO = 2 THEN
    bAlarm_AllDOSensorsFailed := FALSE;
    IF bFault_DO_A THEN
        rVoted_DO_Raw := (rDO_Probe_B + rDO_Probe_C) / 2.0;
    ELSIF bFault_DO_B THEN
        rVoted_DO_Raw := (rDO_Probe_A + rDO_Probe_C) / 2.0;
    ELSE
        rVoted_DO_Raw := (rDO_Probe_A + rDO_Probe_B) / 2.0;
    END_IF;
ELSIF iHealthy_DO = 1 THEN
    bAlarm_AllDOSensorsFailed := FALSE;
    IF NOT bFault_DO_A THEN
        rVoted_DO_Raw := rDO_Probe_A;
    ELSIF NOT bFault_DO_B THEN
        rVoted_DO_Raw := rDO_Probe_B;
    ELSE
        rVoted_DO_Raw := rDO_Probe_C;
    END_IF;
ELSE
    bAlarm_AllDOSensorsFailed := TRUE;
    rVoted_DO_Raw := rVoted_DO_LastGood;
END_IF;

rVoted_DO_LastGood := rVoted_DO_Raw;
rVal_Voted_DO := rVal_Voted_DO + (rFilterAlpha_DO * (rVoted_DO_Raw - rVal_Voted_DO));

(* 1.3: 2oo3 TMR CULTURE BROTH pH PRESSURIZED GEL ELECTRODES *)
IF (rPH_Sensor_A >= rPH_Sensor_B AND rPH_Sensor_A <= rPH_Sensor_C) OR (rPH_Sensor_A <= rPH_Sensor_B AND rPH_Sensor_A >= rPH_Sensor_C) THEN
    rMedian_PH := rPH_Sensor_A;
ELSIF (rPH_Sensor_B >= rPH_Sensor_A AND rPH_Sensor_B <= rPH_Sensor_C) OR (rPH_Sensor_B <= rPH_Sensor_A AND rPH_Sensor_B >= rPH_Sensor_C) THEN
    rMedian_PH := rPH_Sensor_B;
ELSE
    rMedian_PH := rPH_Sensor_C;
END_IF;

rDiff_PH_A := ABS(rPH_Sensor_A - rMedian_PH);
rDiff_PH_B := ABS(rPH_Sensor_B - rMedian_PH);
rDiff_PH_C := ABS(rPH_Sensor_C - rMedian_PH);

IF rDiff_PH_A > rLimit_Discrepancy_PH THEN
    rTimer_PH_A := rTimer_PH_A + rScanTime;
    IF rTimer_PH_A >= rTime_Discrepancy_Trip THEN bFault_PH_A := TRUE; END_IF;
ELSE
    rTimer_PH_A := MAX(0.0, rTimer_PH_A - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_PH_A := FALSE; END_IF;
END_IF;

IF rDiff_PH_B > rLimit_Discrepancy_PH THEN
    rTimer_PH_B := rTimer_PH_B + rScanTime;
    IF rTimer_PH_B >= rTime_Discrepancy_Trip THEN bFault_PH_B := TRUE; END_IF;
ELSE
    rTimer_PH_B := MAX(0.0, rTimer_PH_B - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_PH_B := FALSE; END_IF;
END_IF;

IF rDiff_PH_C > rLimit_Discrepancy_PH THEN
    rTimer_PH_C := rTimer_PH_C + rScanTime;
    IF rTimer_PH_C >= rTime_Discrepancy_Trip THEN bFault_PH_C := TRUE; END_IF;
ELSE
    rTimer_PH_C := MAX(0.0, rTimer_PH_C - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_PH_C := FALSE; END_IF;
END_IF;

iHealthy_PH := 0;
IF NOT bFault_PH_A THEN iHealthy_PH := iHealthy_PH + 1; END_IF;
IF NOT bFault_PH_B THEN iHealthy_PH := iHealthy_PH + 1; END_IF;
IF NOT bFault_PH_C THEN iHealthy_PH := iHealthy_PH + 1; END_IF;

IF iHealthy_PH = 3 THEN
    rVoted_PH_Raw := (rPH_Sensor_A + rPH_Sensor_B + rPH_Sensor_C) / 3.0;
    bAlarm_AllPHSensorsFailed := FALSE;
ELSIF iHealthy_PH = 2 THEN
    bAlarm_AllPHSensorsFailed := FALSE;
    IF bFault_PH_A THEN
        rVoted_PH_Raw := (rPH_Sensor_B + rPH_Sensor_C) / 2.0;
    ELSIF bFault_PH_B THEN
        rVoted_PH_Raw := (rPH_Sensor_A + rPH_Sensor_C) / 2.0;
    ELSE
        rVoted_PH_Raw := (rPH_Sensor_A + rPH_Sensor_B) / 2.0;
    END_IF;
ELSIF iHealthy_PH = 1 THEN
    bAlarm_AllPHSensorsFailed := FALSE;
    IF NOT bFault_PH_A THEN
        rVoted_PH_Raw := rPH_Sensor_A;
    ELSIF NOT bFault_PH_B THEN
        rVoted_PH_Raw := rPH_Sensor_B;
    ELSE
        rVoted_PH_Raw := rPH_Sensor_C;
    END_IF;
ELSE
    bAlarm_AllPHSensorsFailed := TRUE;
    rVoted_PH_Raw := rVoted_PH_LastGood;
END_IF;

rVoted_PH_LastGood := rVoted_PH_Raw;
rVal_Voted_PH := rVal_Voted_PH + (rFilterAlpha_PH * (rVoted_PH_Raw - rVal_Voted_PH));

(* 1.4: 2oo3 TMR ATF HOLLOW-FIBER INLET FEED PRESSURE TRANSMITTERS *)
IF (rPressure_ATF_Feed_A >= rPressure_ATF_Feed_B AND rPressure_ATF_Feed_A <= rPressure_ATF_Feed_C) OR (rPressure_ATF_Feed_A <= rPressure_ATF_Feed_B AND rPressure_ATF_Feed_A >= rPressure_ATF_Feed_C) THEN
    rMedian_FeedPress := rPressure_ATF_Feed_A;
ELSIF (rPressure_ATF_Feed_B >= rPressure_ATF_Feed_A AND rPressure_ATF_Feed_B <= rPressure_ATF_Feed_C) OR (rPressure_ATF_Feed_B <= rPressure_ATF_Feed_A AND rPressure_ATF_Feed_B >= rPressure_ATF_Feed_C) THEN
    rMedian_FeedPress := rPressure_ATF_Feed_B;
ELSE
    rMedian_FeedPress := rPressure_ATF_Feed_C;
END_IF;

rDiff_FeedPress_A := ABS(rPressure_ATF_Feed_A - rMedian_FeedPress);
rDiff_FeedPress_B := ABS(rPressure_ATF_Feed_B - rMedian_FeedPress);
rDiff_FeedPress_C := ABS(rPressure_ATF_Feed_C - rMedian_FeedPress);

IF rDiff_FeedPress_A > rLimit_Discrepancy_FeedPress THEN
    rTimer_FeedPress_A := rTimer_FeedPress_A + rScanTime;
    IF rTimer_FeedPress_A >= rTime_Discrepancy_Trip THEN bFault_FeedPress_A := TRUE; END_IF;
ELSE
    rTimer_FeedPress_A := MAX(0.0, rTimer_FeedPress_A - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_FeedPress_A := FALSE; END_IF;
END_IF;

IF rDiff_FeedPress_B > rLimit_Discrepancy_FeedPress THEN
    rTimer_FeedPress_B := rTimer_FeedPress_B + rScanTime;
    IF rTimer_FeedPress_B >= rTime_Discrepancy_Trip THEN bFault_FeedPress_B := TRUE; END_IF;
ELSE
    rTimer_FeedPress_B := MAX(0.0, rTimer_FeedPress_B - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_FeedPress_B := FALSE; END_IF;
END_IF;

IF rDiff_FeedPress_C > rLimit_Discrepancy_FeedPress THEN
    rTimer_FeedPress_C := rTimer_FeedPress_C + rScanTime;
    IF rTimer_FeedPress_C >= rTime_Discrepancy_Trip THEN bFault_FeedPress_C := TRUE; END_IF;
ELSE
    rTimer_FeedPress_C := MAX(0.0, rTimer_FeedPress_C - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_FeedPress_C := FALSE; END_IF;
END_IF;

iHealthy_FeedPress := 0;
IF NOT bFault_FeedPress_A THEN iHealthy_FeedPress := iHealthy_FeedPress + 1; END_IF;
IF NOT bFault_FeedPress_B THEN iHealthy_FeedPress := iHealthy_FeedPress + 1; END_IF;
IF NOT bFault_FeedPress_C THEN iHealthy_FeedPress := iHealthy_FeedPress + 1; END_IF;

IF iHealthy_FeedPress = 3 THEN
    rVoted_FeedPress_Raw := (rPressure_ATF_Feed_A + rPressure_ATF_Feed_B + rPressure_ATF_Feed_C) / 3.0;
    bAlarm_AllFeedPressFailed := FALSE;
ELSIF iHealthy_FeedPress = 2 THEN
    bAlarm_AllFeedPressFailed := FALSE;
    IF bFault_FeedPress_A THEN
        rVoted_FeedPress_Raw := (rPressure_ATF_Feed_B + rPressure_ATF_Feed_C) / 2.0;
    ELSIF bFault_FeedPress_B THEN
        rVoted_FeedPress_Raw := (rPressure_ATF_Feed_A + rPressure_ATF_Feed_C) / 2.0;
    ELSE
        rVoted_FeedPress_Raw := (rPressure_ATF_Feed_A + rPressure_ATF_Feed_B) / 2.0;
    END_IF;
ELSIF iHealthy_FeedPress = 1 THEN
    bAlarm_AllFeedPressFailed := FALSE;
    IF NOT bFault_FeedPress_A THEN
        rVoted_FeedPress_Raw := rPressure_ATF_Feed_A;
    ELSIF NOT bFault_FeedPress_B THEN
        rVoted_FeedPress_Raw := rPressure_ATF_Feed_B;
    ELSE
        rVoted_FeedPress_Raw := rPressure_ATF_Feed_C;
    END_IF;
ELSE
    bAlarm_AllFeedPressFailed := TRUE;
    rVoted_FeedPress_Raw := rVoted_FeedPress_LastGood;
END_IF;

rVoted_FeedPress_LastGood := rVoted_FeedPress_Raw;

(* First-Principles Transmembrane Pressure Calculation: TMP = ((P_Feed + P_Retentate)/2) - P_Permeate *)
rTemp_Sum := ((rVoted_FeedPress_Raw + rPressure_ATF_Retentate) * 0.5) - rPressure_ATF_Permeate;
rVal_Calculated_TMP := rVal_Calculated_TMP + (rFilterAlpha_TMP * (rTemp_Sum - rVal_Calculated_TMP));

(* 1.5: 2oo3 TMR OFF-GAS MASS SPECTROMETER (O2 & CO2 MOLE FRACTIONS) *)
IF (rOffGas_O2_A >= rOffGas_O2_B AND rOffGas_O2_A <= rOffGas_O2_C) OR (rOffGas_O2_A <= rOffGas_O2_B AND rOffGas_O2_A >= rOffGas_O2_C) THEN
    rMedian_OffGas_O2 := rOffGas_O2_A;
ELSIF (rOffGas_O2_B >= rOffGas_O2_A AND rOffGas_O2_B <= rOffGas_O2_C) OR (rOffGas_O2_B <= rOffGas_O2_A AND rOffGas_O2_B >= rOffGas_O2_C) THEN
    rMedian_OffGas_O2 := rOffGas_O2_B;
ELSE
    rMedian_OffGas_O2 := rOffGas_O2_C;
END_IF;

rDiff_OffGas_O2_A := ABS(rOffGas_O2_A - rMedian_OffGas_O2);
rDiff_OffGas_O2_B := ABS(rOffGas_O2_B - rMedian_OffGas_O2);
rDiff_OffGas_O2_C := ABS(rOffGas_O2_C - rMedian_OffGas_O2);

IF rDiff_OffGas_O2_A > rLimit_Discrepancy_OffGas THEN
    rTimer_OffGas_O2_A := rTimer_OffGas_O2_A + rScanTime;
    IF rTimer_OffGas_O2_A >= rTime_Discrepancy_Trip THEN bFault_OffGas_O2_A := TRUE; END_IF;
ELSE
    rTimer_OffGas_O2_A := MAX(0.0, rTimer_OffGas_O2_A - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_OffGas_O2_A := FALSE; END_IF;
END_IF;

IF rDiff_OffGas_O2_B > rLimit_Discrepancy_OffGas THEN
    rTimer_OffGas_O2_B := rTimer_OffGas_O2_B + rScanTime;
    IF rTimer_OffGas_O2_B >= rTime_Discrepancy_Trip THEN bFault_OffGas_O2_B := TRUE; END_IF;
ELSE
    rTimer_OffGas_O2_B := MAX(0.0, rTimer_OffGas_O2_B - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_OffGas_O2_B := FALSE; END_IF;
END_IF;

IF rDiff_OffGas_O2_C > rLimit_Discrepancy_OffGas THEN
    rTimer_OffGas_O2_C := rTimer_OffGas_O2_C + rScanTime;
    IF rTimer_OffGas_O2_C >= rTime_Discrepancy_Trip THEN bFault_OffGas_O2_C := TRUE; END_IF;
ELSE
    rTimer_OffGas_O2_C := MAX(0.0, rTimer_OffGas_O2_C - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_OffGas_O2_C := FALSE; END_IF;
END_IF;

IF NOT bFault_OffGas_O2_A AND NOT bFault_OffGas_O2_B AND NOT bFault_OffGas_O2_C THEN
    rVoted_OffGas_O2_Raw := (rOffGas_O2_A + rOffGas_O2_B + rOffGas_O2_C) / 3.0;
ELSIF NOT bFault_OffGas_O2_A AND NOT bFault_OffGas_O2_B THEN
    rVoted_OffGas_O2_Raw := (rOffGas_O2_A + rOffGas_O2_B) / 2.0;
ELSIF NOT bFault_OffGas_O2_A AND NOT bFault_OffGas_O2_C THEN
    rVoted_OffGas_O2_Raw := (rOffGas_O2_A + rOffGas_O2_C) / 2.0;
ELSIF NOT bFault_OffGas_O2_B AND NOT bFault_OffGas_O2_C THEN
    rVoted_OffGas_O2_Raw := (rOffGas_O2_B + rOffGas_O2_C) / 2.0;
ELSIF NOT bFault_OffGas_O2_A THEN
    rVoted_OffGas_O2_Raw := rOffGas_O2_A;
ELSIF NOT bFault_OffGas_O2_B THEN
    rVoted_OffGas_O2_Raw := rOffGas_O2_B;
ELSIF NOT bFault_OffGas_O2_C THEN
    rVoted_OffGas_O2_Raw := rOffGas_O2_C;
ELSE
    rVoted_OffGas_O2_Raw := rVoted_OffGas_O2_LastGood;
END_IF;
rVoted_OffGas_O2_LastGood := rVoted_OffGas_O2_Raw;

(* Off-Gas CO2 Median & Voting *)
IF (rOffGas_CO2_A >= rOffGas_CO2_B AND rOffGas_CO2_A <= rOffGas_CO2_C) OR (rOffGas_CO2_A <= rOffGas_CO2_B AND rOffGas_CO2_A >= rOffGas_CO2_C) THEN
    rMedian_OffGas_CO2 := rOffGas_CO2_A;
ELSIF (rOffGas_CO2_B >= rOffGas_CO2_A AND rOffGas_CO2_B <= rOffGas_CO2_C) OR (rOffGas_CO2_B <= rOffGas_CO2_A AND rOffGas_CO2_B >= rOffGas_CO2_C) THEN
    rMedian_OffGas_CO2 := rOffGas_CO2_B;
ELSE
    rMedian_OffGas_CO2 := rOffGas_CO2_C;
END_IF;

rDiff_OffGas_CO2_A := ABS(rOffGas_CO2_A - rMedian_OffGas_CO2);
rDiff_OffGas_CO2_B := ABS(rOffGas_CO2_B - rMedian_OffGas_CO2);
rDiff_OffGas_CO2_C := ABS(rOffGas_CO2_C - rMedian_OffGas_CO2);

IF rDiff_OffGas_CO2_A > rLimit_Discrepancy_OffGas THEN
    rTimer_OffGas_CO2_A := rTimer_OffGas_CO2_A + rScanTime;
    IF rTimer_OffGas_CO2_A >= rTime_Discrepancy_Trip THEN bFault_OffGas_CO2_A := TRUE; END_IF;
ELSE
    rTimer_OffGas_CO2_A := MAX(0.0, rTimer_OffGas_CO2_A - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_OffGas_CO2_A := FALSE; END_IF;
END_IF;

IF rDiff_OffGas_CO2_B > rLimit_Discrepancy_OffGas THEN
    rTimer_OffGas_CO2_B := rTimer_OffGas_CO2_B + rScanTime;
    IF rTimer_OffGas_CO2_B >= rTime_Discrepancy_Trip THEN bFault_OffGas_CO2_B := TRUE; END_IF;
ELSE
    rTimer_OffGas_CO2_B := MAX(0.0, rTimer_OffGas_CO2_B - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_OffGas_CO2_B := FALSE; END_IF;
END_IF;

IF rDiff_OffGas_CO2_C > rLimit_Discrepancy_OffGas THEN
    rTimer_OffGas_CO2_C := rTimer_OffGas_CO2_C + rScanTime;
    IF rTimer_OffGas_CO2_C >= rTime_Discrepancy_Trip THEN bFault_OffGas_CO2_C := TRUE; END_IF;
ELSE
    rTimer_OffGas_CO2_C := MAX(0.0, rTimer_OffGas_CO2_C - (rScanTime * 2.0));
    IF bAcknowledgeAlarms THEN bFault_OffGas_CO2_C := FALSE; END_IF;
END_IF;

IF NOT bFault_OffGas_CO2_A AND NOT bFault_OffGas_CO2_B AND NOT bFault_OffGas_CO2_C THEN
    rVoted_OffGas_CO2_Raw := (rOffGas_CO2_A + rOffGas_CO2_B + rOffGas_CO2_C) / 3.0;
ELSIF NOT bFault_OffGas_CO2_A AND NOT bFault_OffGas_CO2_B THEN
    rVoted_OffGas_CO2_Raw := (rOffGas_CO2_A + rOffGas_CO2_B) / 2.0;
ELSIF NOT bFault_OffGas_CO2_A AND NOT bFault_OffGas_CO2_C THEN
    rVoted_OffGas_CO2_Raw := (rOffGas_CO2_A + rOffGas_CO2_C) / 2.0;
ELSIF NOT bFault_OffGas_CO2_B AND NOT bFault_OffGas_CO2_C THEN
    rVoted_OffGas_CO2_Raw := (rOffGas_CO2_B + rOffGas_CO2_C) / 2.0;
ELSIF NOT bFault_OffGas_CO2_A THEN
    rVoted_OffGas_CO2_Raw := rOffGas_CO2_A;
ELSIF NOT bFault_OffGas_CO2_B THEN
    rVoted_OffGas_CO2_Raw := rOffGas_CO2_B;
ELSIF NOT bFault_OffGas_CO2_C THEN
    rVoted_OffGas_CO2_Raw := rOffGas_CO2_C;
ELSE
    rVoted_OffGas_CO2_Raw := rVoted_OffGas_CO2_LastGood;
END_IF;
rVoted_OffGas_CO2_LastGood := rVoted_OffGas_CO2_Raw;
""")

    # -------------------------------------------------------------------------
    # PHASE 2: RESPIROMETRY, RAMAN OBSERVER & FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE
    # -------------------------------------------------------------------------
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 2: RESPIROMETRIC KINETICS, RAMAN OBSERVER & 8-STATE DISCRETE STATE-SPACE FORMULATION           *)
(* ==================================================================================================== *)

(* 2.1: FIRST-PRINCIPLES RESPIROMETRIC OFF-GAS KINETICS (HALDANE INERT BALANCE FORMULATION) *)
(* Conversion to Dry Mole Fractions *)
rDryInlet_O2_Fract := rInletGas_O2_Pct * 0.01;
rDryInlet_CO2_Fract := rInletGas_CO2_Pct * 0.01;
rDryExhaust_O2_Fract := rVoted_OffGas_O2_Raw * 0.01;
rDryExhaust_CO2_Fract := rVoted_OffGas_CO2_Raw * 0.01;

(* Respirometric Inert Gas Ratio (Nitrogen/Argon Balance) *)
rInertRatio := (1.0 - rDryInlet_O2_Fract - rDryInlet_CO2_Fract) / MAX(0.001, (1.0 - rDryExhaust_O2_Fract - rDryExhaust_CO2_Fract));

(* Oxygen Uptake Rate (OUR) in [mmol/L/h] *)
(* OUR = (F_in / (V_L * V_m)) * (y_O2_in - y_O2_out * InertRatio) * 60.0 * 1000.0 *)
rTemp_Diff := rDryInlet_O2_Fract - (rDryExhaust_O2_Fract * rInertRatio);
rVal_Calculated_OUR := (rTotalInletGasFlow_NLmin / (MAX(100.0, rVesselBrothVolume_L) * rMolarGasVolume)) * rTemp_Diff * 60000.0;
rVal_Calculated_OUR := MAX(0.0, rVal_Calculated_OUR);

(* Carbon Dioxide Evolution Rate (CER) in [mmol/L/h] *)
(* CER = (F_in / (V_L * V_m)) * (y_CO2_out * InertRatio - y_CO2_in) * 60.0 * 1000.0 *)
rTemp_Diff := (rDryExhaust_CO2_Fract * rInertRatio) - rDryInlet_CO2_Fract;
rTemp_Sum := (rTotalInletGasFlow_NLmin / (MAX(100.0, rVesselBrothVolume_L) * rMolarGasVolume)) * rTemp_Diff * 60000.0;
rVal_Calculated_CER := rVal_Calculated_CER + (rFilterAlpha_CER * (rTemp_Sum - rVal_Calculated_CER));
rVal_Calculated_CER := MAX(0.0, rVal_Calculated_CER);

(* Respiratory Quotient (RQ = CER / OUR) *)
IF rVal_Calculated_OUR > 0.10 THEN
    rVal_Calculated_RQ := rVal_Calculated_CER / rVal_Calculated_OUR;
ELSE
    rVal_Calculated_RQ := 1.00;
END_IF;

(* 2.2: IN-LINE LASER RAMAN CHEMOMETRICS FUSION & LUENBERGER OBSERVER UPDATE *)
(* State Vector Definitions:
   x[1] = Broth Bulk Temperature [deg C]
   x[2] = Dissolved Oxygen Saturation [% air sat]
   x[3] = Culture Broth pH [pH]
   x[4] = Viable Cell Density (VCD) [10^6 cells/mL]
   x[5] = Glucose Substrate Concentration [g/L]
   x[6] = Lactate Metabolite Accumulation [g/L]
   x[7] = ATF Hollow-Fiber Transmembrane Pressure (TMP) [bar]
   x[8] = Off-Gas Carbon Dioxide Evolution Rate (CER) [mmol/L/h]
*)

(* Measurement Residual Innovation Vector Calculation *)
rInnov_y[1] := rVal_Voted_Temp - rState_x[1];
rInnov_y[2] := rVal_Voted_DO - rState_x[2];
rInnov_y[3] := rVal_Voted_PH - rState_x[3];

IF bRaman_SignalValid THEN
    rInnov_y[4] := rRaman_VCD_Raw - rState_x[4];
    rInnov_y[5] := rRaman_Glucose_Raw - rState_x[5];
    rInnov_y[6] := rRaman_Lactate_Raw - rState_x[6];
ELSE
    (* Fall back to purely kinematically predicted biomass and metabolites when Raman beam is gated *)
    rInnov_y[4] := 0.0;
    rInnov_y[5] := 0.0;
    rInnov_y[6] := 0.0;
END_IF;

rInnov_y[7] := rVal_Calculated_TMP - rState_x[7];
rInnov_y[8] := rVal_Calculated_CER - rState_x[8];

(* Luenberger Observer Matrix Correction: x_hat[k] = x[k] + L * (y[k] - C*x[k]) *)
FOR i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (rMatL[i, j] * rInnov_y[j]);
    END_FOR;
    rState_x_hat[i] := rState_x[i] + rTemp_Sum;
END_FOR;

(* Output Validated Estimated Observer Values *)
rVal_Estimated_VCD := MAX(0.0, rState_x_hat[4]);
rVal_Estimated_Glucose := MAX(0.0, rState_x_hat[5]);
rVal_Estimated_Lactate := MAX(0.0, rState_x_hat[6]);

(* 2.3: DISCRETE STATE-SPACE MATRIX INITIALIZATION (8x8 Formulation at Ts = 10 ms) *)
IF NOT bInitialScanDone THEN
    (* Row 1: Temperature Dynamics (Dissipative Heat Transfer & Jacket Thermal Coupling) *)
    rMatA[1, 1] := 0.9985;  rMatA[1, 2] := 0.0;     rMatA[1, 3] := 0.0;     rMatA[1, 4] := 0.00015;
    rMatA[1, 5] := 0.0;     rMatA[1, 6] := 0.0;     rMatA[1, 7] := 0.0;     rMatA[1, 8] := 0.0;

    (* Row 2: Dissolved Oxygen Dynamics (Gas Liquid Mass Transfer kla & Cellular Respiration) *)
    rMatA[2, 1] := -0.005;  rMatA[2, 2] := 0.9850;  rMatA[2, 3] := 0.0;     rMatA[2, 4] := -0.00185;
    rMatA[2, 5] := 0.0;     rMatA[2, 6] := 0.0;     rMatA[2, 7] := 0.0;     rMatA[2, 8] := -0.0022;

    (* Row 3: Broth pH Dynamics (Liquid Bicarbonate Chemistry & Carbonic Acid Equilibrium) *)
    rMatA[3, 1] := 0.0;     rMatA[3, 2] := 0.0;     rMatA[3, 3] := 0.9920;  rMatA[3, 4] := -0.00008;
    rMatA[3, 5] := 0.0;     rMatA[3, 6] := -0.0012; rMatA[3, 7] := 0.0;     rMatA[3, 8] := -0.00045;

    (* Row 4: Viable Cell Density (Biomass Growth & Exponential Kinetics) *)
    rMatA[4, 1] := 0.0001;  rMatA[4, 2] := 0.0002;  rMatA[4, 3] := 0.0001;  rMatA[4, 4] := 1.00012;
    rMatA[4, 5] := 0.00085; rMatA[4, 6] := -0.0004; rMatA[4, 7] := 0.0;     rMatA[4, 8] := 0.0;

    (* Row 5: Glucose Substrate (Monod Uptake Consumption & Maintenance Depletion) *)
    rMatA[5, 1] := 0.0;     rMatA[5, 2] := 0.0;     rMatA[5, 3] := 0.0;     rMatA[5, 4] := -0.00055;
    rMatA[5, 5] := 0.9975;  rMatA[5, 6] := 0.0;     rMatA[5, 7] := 0.0;     rMatA[5, 8] := 0.0;

    (* Row 6: Lactate Metabolite (Glycolytic Secretion & Secondary Re-Oxidation) *)
    rMatA[6, 1] := 0.0;     rMatA[6, 2] := 0.0;     rMatA[6, 3] := 0.0;     rMatA[6, 4] := 0.00042;
    rMatA[6, 5] := 0.00015; rMatA[6, 6] := 0.9980;  rMatA[6, 7] := 0.0;     rMatA[6, 8] := 0.0;

    (* Row 7: Transmembrane Pressure TMP (Hollow-Fiber Cake Deposition & Hydraulic Permeability) *)
    rMatA[7, 1] := 0.0;     rMatA[7, 2] := 0.0;     rMatA[7, 3] := 0.0;     rMatA[7, 4] := 0.00008;
    rMatA[7, 5] := 0.0;     rMatA[7, 6] := 0.0;     rMatA[7, 7] := 0.9995;  rMatA[7, 8] := 0.0;

    (* Row 8: Off-Gas Carbon Dioxide Evolution Rate (Cellular Respiration & Decarboxylation) *)
    rMatA[8, 1] := 0.001;   rMatA[8, 2] := 0.005;   rMatA[8, 3] := 0.0;     rMatA[8, 4] := 0.0035;
    rMatA[8, 5] := 0.0022;  rMatA[8, 6] := 0.0;     rMatA[8, 7] := 0.0;     rMatA[8, 8] := 0.9820;

    (* Input Coupling Matrix B_d (Actuators 1:Jacket, 2:O2, 3:CO2, 4:Air, 5:Base, 6:Feed, 7:ATF, 8:Perm) *)
    (* Col 1: Jacket Valve Cmd (-100% cool to +100% heat) *)
    rMatB[1, 1] := 0.0045;  rMatB[2, 1] := 0.0;     rMatB[3, 1] := 0.0;     rMatB[4, 1] := 0.0;
    rMatB[5, 1] := 0.0;     rMatB[6, 1] := 0.0;     rMatB[7, 1] := 0.0;     rMatB[8, 1] := 0.0;

    (* Col 2: Pure Oxygen Micro-Sparger MFC (NL/min) *)
    rMatB[1, 2] := 0.0;     rMatB[2, 2] := 0.0850;  rMatB[3, 2] := 0.0;     rMatB[4, 2] := 0.0;
    rMatB[5, 2] := 0.0;     rMatB[6, 2] := 0.0;     rMatB[7, 2] := 0.0;     rMatB[8, 2] := 0.0012;

    (* Col 3: Carbon Dioxide Micro-Sparger MFC (NL/min) *)
    rMatB[1, 3] := 0.0;     rMatB[2, 3] := -0.008;  rMatB[3, 3] := -0.0125; rMatB[4, 3] := 0.0;
    rMatB[5, 3] := 0.0;     rMatB[6, 3] := 0.0;     rMatB[7, 3] := 0.0;     rMatB[8, 3] := 0.0450;

    (* Col 4: Sterile Process Air Macro-Sparger MFC (NL/min) *)
    rMatB[1, 4] := 0.0;     rMatB[2, 4] := 0.0220;  rMatB[3, 4] := 0.0035;  rMatB[4, 4] := 0.0;
    rMatB[5, 4] := 0.0;     rMatB[6, 4] := 0.0;     rMatB[7, 4] := 0.0;     rMatB[8, 4] := 0.0150;

    (* Col 5: Alkaline Neutralization Base Titration Pump (mL/min) *)
    rMatB[1, 5] := 0.0;     rMatB[2, 5] := 0.0;     rMatB[3, 5] := 0.0185;  rMatB[4, 5] := 0.0;
    rMatB[5, 5] := 0.0;     rMatB[6, 5] := 0.0;     rMatB[7, 5] := 0.0;     rMatB[8, 5] := 0.0;

    (* Col 6: Concentrated Nutrient Feed Pump (L/h) *)
    rMatB[1, 6] := 0.0;     rMatB[2, 6] := 0.0;     rMatB[3, 6] := 0.0;     rMatB[4, 6] := 0.0001;
    rMatB[5, 6] := 0.0245;  rMatB[6, 6] := 0.0020;  rMatB[7, 6] := 0.0;     rMatB[8, 6] := 0.0;

    (* Col 7: ATF Reciprocating Diaphragm Frequency (cpm) *)
    rMatB[1, 7] := 0.0;     rMatB[2, 7] := 0.0;     rMatB[3, 7] := 0.0;     rMatB[4, 7] := -0.00005;
    rMatB[5, 7] := 0.0;     rMatB[6, 7] := 0.0;     rMatB[7, 7] := -0.0015; rMatB[8, 7] := 0.0;

    (* Col 8: Perfusion Permeate Harvest Extraction Pump (L/h) *)
    rMatB[1, 8] := 0.0;     rMatB[2, 8] := 0.0;     rMatB[3, 8] := 0.0;     rMatB[4, 8] := -0.00008;
    rMatB[5, 8] := -0.0035; rMatB[6, 8] := -0.0042; rMatB[7, 8] := 0.0028;  rMatB[8, 8] := 0.0;

    (* Observer Diagonal Gain Matrix L *)
    rMatL[1, 1] := 0.12;  rMatL[2, 2] := 0.18;  rMatL[3, 3] := 0.15;  rMatL[4, 4] := 0.08;
    rMatL[5, 5] := 0.09;  rMatL[6, 6] := 0.07;  rMatL[7, 7] := 0.20;  rMatL[8, 8] := 0.14;

    (* MPC Quadratic Penalty Weights (Q, R, S, P) *)
    rMatQ[1] := 15.0;  rMatQ[2] := 8.0;   rMatQ[3] := 25.0;  rMatQ[4] := 2.0;
    rMatQ[5] := 12.0;  rMatQ[6] := 6.0;   rMatQ[7] := 35.0;  rMatQ[8] := 4.0;

    rMatR[1] := 0.50;  rMatR[2] := 0.25;  rMatR[3] := 0.30;  rMatR[4] := 0.10;
    rMatR[5] := 0.40;  rMatR[6] := 0.80;  rMatR[7] := 0.15;  rMatR[8] := 0.60;

    rMatS[1] := 1.20;  rMatS[2] := 0.50;  rMatS[3] := 0.60;  rMatS[4] := 0.20;
    rMatS[5] := 0.90;  rMatS[6] := 1.50;  rMatS[7] := 0.40;  rMatS[8] := 1.10;

    rMatP[1] := 30.0;  rMatP[2] := 18.0;  rMatP[3] := 50.0;  rMatP[4] := 5.0;
    rMatP[5] := 25.0;  rMatP[6] := 12.0;  rMatP[7] := 75.0;  rMatP[8] := 8.0;

    (* Physical Actuator Box Saturation Limits *)
    rU_Min[1] := -100.0; rU_Max[1] := 100.0; (* Jacket Valve [%] *)
    rU_Min[2] := 0.0;    rU_Max[2] := 150.0; (* Pure O2 MFC [NL/min] *)
    rU_Min[3] := 0.0;    rU_Max[3] := 50.0;  (* Pure CO2 MFC [NL/min] *)
    rU_Min[4] := 0.0;    rU_Max[4] := 350.0; (* Process Air MFC [NL/min] *)
    rU_Min[5] := 0.0;    rU_Max[5] := 200.0; (* Base Neutralization [mL/min] *)
    rU_Min[6] := 0.0;    rU_Max[6] := 150.0; (* Nutrient Feed Pump [L/h] *)
    rU_Min[7] := 5.0;    rU_Max[7] := 55.0;  (* ATF Reciprocation [cpm] *)
    rU_Min[8] := 0.0;    rU_Max[8] := 250.0; (* Permeate Harvest Pump [L/h] *)

    (* Actuator Slew Rate Constraints (Per 10 ms Cycle) *)
    rDeltaU_Max[1] := 1.50;  (* Jacket Valve Max 150%/s *)
    rDeltaU_Max[2] := 2.00;  (* O2 MFC Max 200 NL/min/s *)
    rDeltaU_Max[3] := 1.00;  (* CO2 MFC Max 100 NL/min/s *)
    rDeltaU_Max[4] := 4.00;  (* Air MFC Max 400 NL/min/s *)
    rDeltaU_Max[5] := 2.50;  (* Base Pump Max 250 mL/min/s *)
    rDeltaU_Max[6] := 1.80;  (* Feed Pump Max 180 L/h/s *)
    rDeltaU_Max[7] := 0.50;  (* ATF Rate Max 50 cpm/s *)
    rDeltaU_Max[8] := 2.20;  (* Permeate Pump Max 220 L/h/s *)

    (* Initialize State Vector to Ambient Standby *)
    rState_x[1] := 37.0;
    rState_x[2] := 50.0;
    rState_x[3] := 7.05;
    rState_x[4] := 0.0;
    rState_x[5] := 4.0;
    rState_x[6] := 0.2;
    rState_x[7] := 0.15;
    rState_x[8] := 0.0;

    bInitialScanDone := TRUE;
END_IF;

(* 2.4: DISCRETE STATE PROPAGATION WITH FIRST-PRINCIPLES NON-LINEAR COUPLING *)
(* Monod Specific Cell Growth Rate with Temperature Arrhenius Factor & Substrate Kinetics *)
rBiomassNetGrowthRate := rMu_Max * (rState_x_hat[5] / (rKs_Glucose + rState_x_hat[5]))
                         * (rKi_Lactate / (rKi_Lactate + rState_x_hat[6]))
                         * EXP(-1.0 * EXPT((rState_x_hat[1] - 37.0) / 3.5, 2.0));

(* Metabolic Specific Rates *)
rSpecGlcConsumption := (rBiomassNetGrowthRate / rYield_X_S) + rMaint_Glucose;
rSpecLacProduction := rYield_L_S * rSpecGlcConsumption;

(* Transmembrane Permeate Flux J in LMH (L / m2 / h) *)
rPermeateFlux_LMH := rControl_u[8] / rMembraneArea_m2;

(* Hydraulic Clean Membrane & Cake Resistance Formulation *)
rCurrentTMP_Pa := rState_x_hat[7] * 100000.0; (* Convert bar to Pascals *)
rCakeResistance_m := rCleanMembraneResist + (rSpecificCakeResist * rState_x_hat[4] * 1.0e6 * (rPermeateFlux_LMH / 100.0));

(* Explicit 8-State Linear State-Space Propagation: x_pred = A*x_hat + B*u *)
FOR i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (rMatA[i, j] * rState_x_hat[j]);
    END_FOR;
    FOR m := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (rMatB[i, m] * rControl_u[m]);
    END_FOR;
    rState_x_pred[i] := rTemp_Sum;
END_FOR;

(* Apply Non-Linear Dynamic Biochemical Injections *)
(* Non-linear growth addition to VCD *)
rState_x_pred[4] := rState_x_pred[4] + (rBiomassNetGrowthRate * rState_x_hat[4] * (rScanTime / 3600.0));

(* Non-linear glucose consumption *)
rState_x_pred[5] := rState_x_pred[5] - (rSpecGlcConsumption * rState_x_hat[4] * 1.0e-3 * (rScanTime / 3600.0));

(* Non-linear lactate synthesis *)
rState_x_pred[6] := rState_x_pred[6] + (rSpecLacProduction * rState_x_hat[4] * 1.0e-3 * (rScanTime / 3600.0));

(* Antifouling backpulse dynamic hydraulic relief *)
IF bCmd_BackpulseValve_Open THEN
    rState_x_pred[7] := MAX(0.08, rState_x_pred[7] - 0.015);
END_IF;

(* State Vector Latched Update for Subsequent Execution Cycle *)
FOR i := 1 TO 8 DO
    rState_x[i] := rState_x_pred[i];
END_FOR;
""")

    # -------------------------------------------------------------------------
    # PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS
    # -------------------------------------------------------------------------
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)       *)
(* ==================================================================================================== *)

(* 3.1: DYNAMIC SETPOINT REFERENCE TRAJECTORY GENERATION ACCORDING TO FSM OPERATIONAL STAGE *)
CASE eState OF
    0: (* OFFLINE_STANDBY *)
        rState_x_ref[1] := 22.0; (* Ambient Cold Vessel *)
        rState_x_ref[2] := 0.0;
        rState_x_ref[3] := 7.00;
        rState_x_ref[4] := 0.0;
        rState_x_ref[5] := 0.0;
        rState_x_ref[6] := 0.0;
        rState_x_ref[7] := 0.05;
        rState_x_ref[8] := 0.0;

    1: (* CIP_CLEAN_IN_PLACE *)
        rState_x_ref[1] := 75.0; (* Hot Caustic Wash Temp *)
        rState_x_ref[2] := 0.0;
        rState_x_ref[3] := 12.5; (* High Alkaline Cleaning pH *)
        rState_x_ref[4] := 0.0;
        rState_x_ref[5] := 0.0;
        rState_x_ref[6] := 0.0;
        rState_x_ref[7] := 0.10;
        rState_x_ref[8] := 0.0;

    2: (* SIP_THERMAL_STERILIZATION *)
        rState_x_ref[1] := 121.5; (* Pure Steam Sterilization Hold *)
        rState_x_ref[2] := 0.0;
        rState_x_ref[3] := 7.00;
        rState_x_ref[4] := 0.0;
        rState_x_ref[5] := 0.0;
        rState_x_ref[6] := 0.0;
        rState_x_ref[7] := 0.15;
        rState_x_ref[8] := 0.0;

    3: (* POST_SIP_ASEPTIC_COOLDOWN *)
        rState_x_ref[1] := 37.0; (* Controlled Thermal Cooldown *)
        rState_x_ref[2] := 0.0;
        rState_x_ref[3] := 7.00;
        rState_x_ref[4] := 0.0;
        rState_x_ref[5] := 0.0;
        rState_x_ref[6] := 0.0;
        rState_x_ref[7] := 0.10;
        rState_x_ref[8] := 0.0;

    4: (* STERILE_MEDIA_BATCH_FILL *)
        rState_x_ref[1] := 37.0;
        rState_x_ref[2] := 50.0; (* Equilibrated DO Setpoint *)
        rState_x_ref[3] := 7.05; (* Media Homeostatic pH *)
        rState_x_ref[4] := 0.0;
        rState_x_ref[5] := 4.50; (* Initial Basal Glucose *)
        rState_x_ref[6] := 0.10;
        rState_x_ref[7] := 0.12;
        rState_x_ref[8] := 0.0;

    5: (* INOCULATION_SEED_TRANSFER *)
        rState_x_ref[1] := 37.0;
        rState_x_ref[2] := 45.0;
        rState_x_ref[3] := 7.05;
        rState_x_ref[4] := 4.50; (* Inoculum Target Density *)
        rState_x_ref[5] := 4.20;
        rState_x_ref[6] := 0.25;
        rState_x_ref[7] := 0.15;
        rState_x_ref[8] := 1.20;

    6: (* BATCH_EXPONENTIAL_GROWTH *)
        rState_x_ref[1] := 37.0;
        rState_x_ref[2] := 40.0;
        rState_x_ref[3] := 7.00;
        rState_x_ref[4] := 25.0; (* Exponential Density Build *)
        rState_x_ref[5] := 3.20;
        rState_x_ref[6] := 0.85;
        rState_x_ref[7] := 0.20;
        rState_x_ref[8] := 8.50;

    7: (* FED_BATCH_TRANSITION *)
        rState_x_ref[1] := 36.8; (* Mild Temperature Shift to Enhance Cell Viability *)
        rState_x_ref[2] := 40.0;
        rState_x_ref[3] := 6.98;
        rState_x_ref[4] := 45.0;
        rState_x_ref[5] := 3.50;
        rState_x_ref[6] := 1.20;
        rState_x_ref[7] := 0.25;
        rState_x_ref[8] := 14.0;

    8: (* PERFUSION_CUT_IN_RAMP *)
        rState_x_ref[1] := 36.8;
        rState_x_ref[2] := 40.0;
        rState_x_ref[3] := 6.95;
        rState_x_ref[4] := 70.0;
        rState_x_ref[5] := 3.00;
        rState_x_ref[6] := 1.45;
        rState_x_ref[7] := 0.32;
        rState_x_ref[8] := 22.0;

    9: (* STEADY_STATE_HIGH_DENSITY *)
        rState_x_ref[1] := 36.8; (* Homeostatic Temperature *)
        rState_x_ref[2] := 40.0; (* Strict DO Control *)
        rState_x_ref[3] := 6.95; (* Physiological pH Target *)
        rState_x_ref[4] := 95.0; (* Ultra-High Viable Cell Density Target: 95 million cells/mL *)
        rState_x_ref[5] := 2.80; (* Monod Controlled Glucose *)
        rState_x_ref[6] := 1.65; (* Non-Inhibitory Lactate Ceiling *)
        rState_x_ref[7] := 0.38; (* Controlled Transmembrane Pressure *)
        rState_x_ref[8] := 28.5; (* High Respiratory Activity CER *)

    10: (* MEMBRANE_BACKPULSE_ANTIFOULING *)
        rState_x_ref[1] := 36.8;
        rState_x_ref[2] := 40.0;
        rState_x_ref[3] := 6.95;
        rState_x_ref[4] := 95.0;
        rState_x_ref[5] := 2.80;
        rState_x_ref[6] := 1.65;
        rState_x_ref[7] := 0.18; (* Depressurized Target TMP *)
        rState_x_ref[8] := 28.5;

    11: (* BLEED_CELL_DENSITY_STABILIZATION *)
        rState_x_ref[1] := 36.8;
        rState_x_ref[2] := 40.0;
        rState_x_ref[3] := 6.95;
        rState_x_ref[4] := 92.0; (* Trimming Excess Biomass *)
        rState_x_ref[5] := 2.80;
        rState_x_ref[6] := 1.60;
        rState_x_ref[7] := 0.35;
        rState_x_ref[8] := 27.0;

    12: (* FINAL_HARVEST_CONCENTRATION *)
        rState_x_ref[1] := 35.0; (* Chilling Broth to Arrest Lysis *)
        rState_x_ref[2] := 30.0;
        rState_x_ref[3] := 6.90;
        rState_x_ref[4] := 110.0; (* Concentrated Cell Paste *)
        rState_x_ref[5] := 1.00;
        rState_x_ref[6] := 2.50;
        rState_x_ref[7] := 0.55;
        rState_x_ref[8] := 15.0;

    13: (* BIOKILL_THERMAL_DEACTIVATION *)
        rState_x_ref[1] := 85.0; (* Thermal Biokill Inactivation Hold *)
        rState_x_ref[2] := 0.0;
        rState_x_ref[3] := 7.00;
        rState_x_ref[4] := 0.0;
        rState_x_ref[5] := 0.0;
        rState_x_ref[6] := 0.0;
        rState_x_ref[7] := 0.10;
        rState_x_ref[8] := 0.0;

    14: (* EMERGENCY_VENT_SAFE_STOP *)
        rState_x_ref[1] := 20.0; (* Quench Cooling *)
        rState_x_ref[2] := 0.0;
        rState_x_ref[3] := 7.00;
        rState_x_ref[4] := 0.0;
        rState_x_ref[5] := 0.0;
        rState_x_ref[6] := 0.0;
        rState_x_ref[7] := 0.05;
        rState_x_ref[8] := 0.0;
ELSE
    (* Fallback Default Setpoints *)
    rState_x_ref[1] := 37.0;
    rState_x_ref[2] := 40.0;
    rState_x_ref[3] := 7.00;
    rState_x_ref[4] := 50.0;
    rState_x_ref[5] := 3.00;
    rState_x_ref[6] := 1.50;
    rState_x_ref[7] := 0.30;
    rState_x_ref[8] := 15.0;
END_CASE;

(* 3.2: MULTI-STEP FORWARD TRAJECTORY PREDICTION (Np = 5 Steps) *)
(* Prediction Step 1 *)
FOR i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (rMatA[i, j] * rState_x_hat[j]);
    END_FOR;
    FOR m := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (rMatB[i, m] * rControl_u[m]);
    END_FOR;
    rPred_Traj[1, i] := rTemp_Sum;
END_FOR;

(* Prediction Steps 2 to 5 *)
FOR p := 2 TO 5 DO
    FOR i := 1 TO 8 DO
        rTemp_Sum := 0.0;
        FOR j := 1 TO 8 DO
            rTemp_Sum := rTemp_Sum + (rMatA[i, j] * rPred_Traj[p - 1, j]);
        END_FOR;
        FOR m := 1 TO 8 DO
            rTemp_Sum := rTemp_Sum + (rMatB[i, m] * rControl_u[m]);
        END_FOR;
        rPred_Traj[p, i] := rTemp_Sum;
    END_FOR;
END_FOR;

(* 3.3: PROJECTED GRADIENT DESCENT (PGD) ITERATIVE OPTIMIZER *)
(* Initialize Candidate Actuator Vector with Current State *)
FOR m := 1 TO 8 DO
    rU_cand[m] := rControl_u[m];
END_FOR;

(* Perform 8 PGD Optimization Iterations Per Scan Cycle *)
FOR iter := 1 TO 8 DO
    (* Calculate Gradient dJ/du for Each Manipulated Actuator *)
    FOR m := 1 TO 8 DO
        (* Term 1: Actuator Effort Penalty Gradient: 2 * R_m * (u_m - u_target_m) *)
        rGrad_J[m] := 2.0 * rMatR[m] * (rU_cand[m] - rControl_u_target[m]);

        (* Term 2: Actuator Slew Rate Penalty Gradient: 2 * S_m * (u_m - u_prev_m) *)
        rGrad_J[m] := rGrad_J[m] + (2.0 * rMatS[m] * (rU_cand[m] - rControl_u_prev[m]));

        (* Term 3: Forward Tracking Error Sensitivity Accumulation across Prediction Horizon *)
        FOR p := 1 TO 5 DO
            FOR i := 1 TO 8 DO
                (* Sensitivity Approximation: d(x_p_i)/du_m ~ B[i, m] *)
                rSensitivity := rMatB[i, m];
                rTemp_Diff := rPred_Traj[p, i] - rState_x_ref[i];

                IF p < 5 THEN
                    rGrad_J[m] := rGrad_J[m] + (2.0 * rMatQ[i] * rTemp_Diff * rSensitivity);
                ELSE
                    (* Terminal Cost Penalty Weighting P at Horizon Boundary *)
                    rGrad_J[m] := rGrad_J[m] + (2.0 * rMatP[i] * rTemp_Diff * rSensitivity);
                END_IF;
            END_FOR;
        END_FOR;

        (* Projected Gradient Descent Update Step *)
        rU_cand[m] := rU_cand[m] - (rAlpha_PGD * rGrad_J[m]);

        (* Apply Dynamic Slew Rate Clamping *)
        rTemp_Diff := rU_cand[m] - rControl_u_prev[m];
        IF rTemp_Diff > rDeltaU_Max[m] THEN
            rU_cand[m] := rControl_u_prev[m] + rDeltaU_Max[m];
        ELSIF rTemp_Diff < -rDeltaU_Max[m] THEN
            rU_cand[m] := rControl_u_prev[m] - rDeltaU_Max[m];
        END_IF;

        (* Apply Hard Physical Actuator Saturation Box Limits *)
        IF rU_cand[m] > rU_Max[m] THEN
            rU_cand[m] := rU_Max[m];
        ELSIF rU_cand[m] < rU_Min[m] THEN
            rU_cand[m] := rU_Min[m];
        END_IF;
    END_FOR;
END_FOR;

(* Latch Solved Optimal Actuator Vector *)
FOR m := 1 TO 8 DO
    rControl_u_prev[m] := rControl_u[m];
    rControl_u[m] := rU_cand[m];
    rDelta_u[m] := rControl_u[m] - rControl_u_prev[m];
END_FOR;

(* 3.4: PHYSICAL ACTUATOR OUTPUT MAPPING & MULTI-GAS DECOUPLING *)
(* Actuator 1: Jacket Thermoregulation Split-Range Heating / Cooling *)
rCmd_JacketControl_Pct := rControl_u[1];

(* Actuator 2: Micro-Sparger Oxygen Flow Rate *)
rCmd_SpargerO2_Flow := rControl_u[2];

(* Actuator 3: Micro-Sparger Carbon Dioxide Acid Flow Rate *)
rCmd_SpargerCO2_Flow := rControl_u[3];

(* Actuator 4: Macro-Sparger Sterile Process Air Stripping Flow Rate *)
rCmd_SpargerAir_Flow := rControl_u[4];

(* Headspace N2 Blanket Pressure Regulation *)
IF rPressure_Headspace < 0.15 THEN
    rCmd_SpargerN2_Flow := 15.0; (* Deliver Sterile N2 to Maintain Positive Sterile Barrier *)
ELSIF rPressure_Headspace > 0.45 THEN
    rCmd_SpargerN2_Flow := 0.0;
ELSE
    rCmd_SpargerN2_Flow := 5.0;
END_IF;

(* Actuator 5: Alkaline Neutralization Base Titration Peristaltic Pump *)
rCmd_BasePump_Flow := rControl_u[5];

(* Actuator 6: Concentrated Nutrient Feed Pump *)
rCmd_NutrientFeed_Flow := rControl_u[6];

(* Actuator 7: ATF Reciprocating Diaphragm Displacement Frequency *)
rCmd_ATF_CycleRate := rControl_u[7];

(* Actuator 8: Perfusion Permeate Harvest Extraction Pump *)
rCmd_PermeateHarvest_Flow := rControl_u[8];

(* Dynamic Impeller Speed Command Based on Agitation Reynolds & Shear Thresholds *)
CASE eState OF
    0..3:
        rCmd_AgitatorSpeed_RPM := 0.0;
    4:
        rCmd_AgitatorSpeed_RPM := 35.0; (* Media Homogenization *)
    5:
        rCmd_AgitatorSpeed_RPM := 45.0; (* Inoculum Dispersion *)
    6..7:
        rCmd_AgitatorSpeed_RPM := 55.0; (* Cell Growth Mixing *)
    8..11:
        rCmd_AgitatorSpeed_RPM := 65.0; (* High Density Oxygen Transfer (P/V < 80 W/m3) *)
    12:
        rCmd_AgitatorSpeed_RPM := 40.0; (* Low Shear Concentration *)
    13:
        rCmd_AgitatorSpeed_RPM := 75.0; (* Thermal Biokill Bulk Mixing *)
    14:
        rCmd_AgitatorSpeed_RPM := 0.0;
ELSE
    rCmd_AgitatorSpeed_RPM := 45.0;
END_CASE;

(* Normalized Perfusion Volumetric Exchange Rate (VVD: Vessel Volumes per Day) *)
rVal_PerfusionRate_VVD := (rCmd_PermeateHarvest_Flow * 24.0) / MAX(100.0, rVesselBrothVolume_L);
""")

    # -------------------------------------------------------------------------
    # PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                                *)
(* ==================================================================================================== *)

(* State Transition Timer Update *)
IF eState = ePrevState THEN
    rStateTimer_sec := rStateTimer_sec + rScanTime;
ELSE
    rStateTimer_sec := 0.0;
    ePrevState := eState;
END_IF;

iActiveState := eState;

(* Primary Finite State Machine Dispatcher *)
CASE eState OF
    0: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 0: OFFLINE_STANDBY (Vessel Depressurized, Dry, Ambient Verification)                   *)
       (* ----------------------------------------------------------------------------------------- *)
        rCmd_JacketControl_Pct := 0.0;
        rCmd_SpargerO2_Flow := 0.0;
        rCmd_SpargerCO2_Flow := 0.0;
        rCmd_SpargerAir_Flow := 0.0;
        rCmd_SpargerN2_Flow := 0.0;
        rCmd_BasePump_Flow := 0.0;
        rCmd_NutrientFeed_Flow := 0.0;
        rCmd_ATF_CycleRate := 0.0;
        rCmd_PermeateHarvest_Flow := 0.0;
        rCmd_BleedPump_Flow := 0.0;
        bCmd_BackpulseValve_Open := FALSE;
        bCmd_CIP_SupplyValve := FALSE;
        bCmd_SIP_PureSteamValve := FALSE;
        bCmd_SIP_CondensateDrainValve := FALSE;
        bCmd_SterileVentValve := TRUE;

        (* Advance to CIP when Start Permissive and Safety Interlocks are Satisfied *)
        IF bStartProduction AND bEmergencyStop AND bCIP_SupplyPermissive THEN
            eState := 1; (* Transition to Clean-In-Place *)
            rStateTimer_sec := 0.0;
            iCIP_SubStep := 0;
            rCIP_StepTimer_sec := 0.0;
        END_IF;

    1: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 1: CIP_CLEAN_IN_PLACE (5-Phase Alkaline / Acid / WFI Cleaning Validation)             *)
       (* ----------------------------------------------------------------------------------------- *)
        bCmd_CIP_SupplyValve := TRUE;
        bCmd_SIP_PureSteamValve := FALSE;
        bCmd_SterileVentValve := TRUE;
        rCIP_StepTimer_sec := rCIP_StepTimer_sec + rScanTime;

        CASE iCIP_SubStep OF
            0: (* Phase 1: Initial Ambient Water-For-Injection (WFI) Pre-Rinse (600 s) *)
                rCmd_JacketControl_Pct := 0.0;
                rCmd_AgitatorSpeed_RPM := 50.0;
                IF rCIP_StepTimer_sec >= 600.0 THEN
                    iCIP_SubStep := 1;
                    rCIP_StepTimer_sec := 0.0;
                END_IF;

            1: (* Phase 2: Hot Alkaline Caustic Flush (2.0% NaOH @ 75 deg C, 2,400 s) *)
                rCmd_JacketControl_Pct := 65.0; (* Steam Heating to 75 deg C *)
                rCmd_AgitatorSpeed_RPM := 65.0;
                IF rVal_Voted_Temp >= 73.0 AND rCIP_StepTimer_sec >= 2400.0 THEN
                    iCIP_SubStep := 2;
                    rCIP_StepTimer_sec := 0.0;
                END_IF;

            2: (* Phase 3: Intermediate Ambient WFI Rinse (900 s) *)
                rCmd_JacketControl_Pct := 0.0;
                rCmd_AgitatorSpeed_RPM := 50.0;
                IF rCIP_StepTimer_sec >= 900.0 THEN
                    iCIP_SubStep := 3;
                    rCIP_StepTimer_sec := 0.0;
                END_IF;

            3: (* Phase 4: Dilute Phosphoric Acid Rinse (1.0% H3PO4 @ 65 deg C, 1,800 s) *)
                rCmd_JacketControl_Pct := 45.0;
                rCmd_AgitatorSpeed_RPM := 55.0;
                IF rVal_Voted_Temp >= 63.0 AND rCIP_StepTimer_sec >= 1800.0 THEN
                    iCIP_SubStep := 4;
                    rCIP_StepTimer_sec := 0.0;
                END_IF;

            4: (* Phase 5: Final WFI Flush & Conductivity Verification (< 1.3 uS/cm) *)
                rCmd_JacketControl_Pct := 0.0;
                rCmd_AgitatorSpeed_RPM := 60.0;
                IF rWFI_Conductivity_uScm < 1.30 AND rCIP_StepTimer_sec >= 900.0 THEN
                    iCIP_SubStep := 5;
                    rCIP_StepTimer_sec := 0.0;
                END_IF;

            5: (* Complete CIP Hold *)
                bCmd_CIP_SupplyValve := FALSE;
                IF bSIP_SteamPermissive THEN
                    eState := 2; (* Advance to SIP Thermal Sterilization *)
                    rStateTimer_sec := 0.0;
                    rSIP_HoldTimer_sec := 0.0;
                    rVal_Accumulated_F0 := 0.0;
                END_IF;
        END_CASE;

    2: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 2: SIP_THERMAL_STERILIZATION (Saturated Pure Steam 121.5 deg C, F0 >= 30.0 min)       *)
       (* ----------------------------------------------------------------------------------------- *)
        bCmd_CIP_SupplyValve := FALSE;
        bCmd_SIP_PureSteamValve := TRUE;
        bCmd_SIP_CondensateDrainValve := TRUE; (* Active Trap Drainage *)
        bCmd_SterileVentValve := FALSE; (* Closed to Accumulate Chamber Pressure *)
        rCmd_AgitatorSpeed_RPM := 25.0;

        (* Saturated Steam Injection & Chamber Pressurization *)
        IF rVal_Voted_Temp < 121.5 THEN
            rCmd_JacketControl_Pct := 100.0; (* Full Heating *)
        ELSE
            rCmd_JacketControl_Pct := 25.0; (* Modulated Holding *)
        END_IF;

        (* Cumulative Thermal Lethality Integration: F0 = Integral(10^((T - 121.1) / 10) * dt) *)
        IF rVal_Voted_Temp >= 115.0 THEN
            rLethalityRate_L := EXPT(10.0, (rVal_Voted_Temp - 121.1) / 10.0);
            rVal_Accumulated_F0 := rVal_Accumulated_F0 + (rLethalityRate_L * (rScanTime / 60.0));
            rSIP_HoldTimer_sec := rSIP_HoldTimer_sec + rScanTime;
        END_IF;

        (* Sterility Validation Criteria: F0 >= 30.0 min AND Dwell Duration >= 2,400 s (40 min) *)
        IF rVal_Accumulated_F0 >= 30.0 AND rSIP_HoldTimer_sec >= 2400.0 THEN
            eState := 3; (* Transition to Post-SIP Aseptic Cooldown *)
            rStateTimer_sec := 0.0;
            bCmd_SIP_PureSteamValve := FALSE;
            bCmd_SIP_CondensateDrainValve := FALSE;
        END_IF;

    3: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 3: POST_SIP_ASEPTIC_COOLDOWN (Sterile Gas Blanket +0.35 bar, Chilled Ramp to 37.0 C)   *)
       (* ----------------------------------------------------------------------------------------- *)
        bCmd_SIP_PureSteamValve := FALSE;
        bCmd_SIP_CondensateDrainValve := FALSE;
        bCmd_SterileVentValve := FALSE;

        (* Maintain Positive Sterile Overpressure Barrier with Sterile Air / N2 *)
        IF rPressure_Headspace < 0.35 THEN
            rCmd_SpargerAir_Flow := 50.0;
        ELSE
            rCmd_SpargerAir_Flow := 10.0;
        END_IF;

        (* Chilled Glycol Jacket Cooling Ramp (-1.5 deg C / min) *)
        IF rVal_Voted_Temp > 37.2 THEN
            rCmd_JacketControl_Pct := -85.0; (* Chilled Glycol Recirculation *)
            rCmd_AgitatorSpeed_RPM := 35.0;
        ELSE
            rCmd_JacketControl_Pct := 0.0;
            rCmd_AgitatorSpeed_RPM := 35.0;
            IF rPressure_Headspace >= 0.25 AND rPressure_Headspace <= 0.45 THEN
                eState := 4; (* Transition to Sterile Media Batch Fill *)
                rStateTimer_sec := 0.0;
            END_IF;
        END_IF;

    4: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 4: STERILE_MEDIA_BATCH_FILL (Basal Media Aseptic Charge 15,000 L, DO / pH Equilibrate)*)
       (* ----------------------------------------------------------------------------------------- *)
        bCmd_SterileVentValve := FALSE;
        rCmd_AgitatorSpeed_RPM := 40.0;

        (* Liquid Media Transfer Progression *)
        IF rVesselBrothVolume_L < 15000.0 THEN
            rVesselBrothVolume_L := rVesselBrothVolume_L + (50.0 * rScanTime); (* Media Inflow *)
        END_IF;

        (* Micro-sparge Process Air to Calibrate Optical Probes to 100% Saturation Reference *)
        IF rStateTimer_sec < 600.0 THEN
            rCmd_SpargerAir_Flow := 120.0;
            rCmd_SpargerO2_Flow := 0.0;
            rCmd_SpargerCO2_Flow := 0.0;
        ELSE
            (* De-oxygenate to Homeostatic 50.0% Setpoint using N2 Sparging *)
            IF rVal_Voted_DO > 52.0 THEN
                rCmd_SpargerN2_Flow := 85.0;
                rCmd_SpargerAir_Flow := 0.0;
            ELSE
                rCmd_SpargerN2_Flow := 10.0;
            END_IF;
        END_IF;

        (* Media Transfer Complete and Temperature/pH Equilibrated *)
        IF rVesselBrothVolume_L >= 14950.0 AND rVal_Voted_Temp >= 36.8 AND rVal_Voted_Temp <= 37.2 AND rVal_Voted_PH >= 7.00 AND rVal_Voted_PH <= 7.10 AND rStateTimer_sec >= 1200.0 THEN
            eState := 5; (* Advance to Inoculation Seed Transfer *)
            rStateTimer_sec := 0.0;
        END_IF;

    5: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 5: INOCULATION_SEED_TRANSFER (Aseptic Inoculum 2,500 L from N-1 Seed Bioreactor)      *)
       (* ----------------------------------------------------------------------------------------- *)
        rCmd_AgitatorSpeed_RPM := 45.0;

        (* Seed Inoculum Transfer Progression *)
        IF rVesselBrothVolume_L < 17500.0 THEN
            rVesselBrothVolume_L := rVesselBrothVolume_L + (35.0 * rScanTime);
        END_IF;

        (* Verify Initial Seed Viable Cell Density (Target 3.5 to 5.0 million cells/mL) *)
        IF rVesselBrothVolume_L >= 17450.0 AND rStateTimer_sec >= 600.0 THEN
            eState := 6; (* Advance to Closed Batch Exponential Growth *)
            rStateTimer_sec := 0.0;
        END_IF;

    6: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 6: BATCH_EXPONENTIAL_GROWTH (Closed Batch Culture, VCD Ramp to 20-30 x 10^6 cells/mL)  *)
       (* ----------------------------------------------------------------------------------------- *)
        rCmd_AgitatorSpeed_RPM := 55.0;
        rCmd_PermeateHarvest_Flow := 0.0;
        rCmd_NutrientFeed_Flow := 0.0;
        rCmd_ATF_CycleRate := 0.0;

        (* Advance to Fed-Batch when Substrate Depletes or Viable Biomass Crosses 22 million cells/mL *)
        IF (rVal_Estimated_Glucose < 2.50 OR rVal_Estimated_VCD >= 22.0) AND rStateTimer_sec >= 3600.0 THEN
            eState := 7; (* Transition to Fed-Batch Transition *)
            rStateTimer_sec := 0.0;
        END_IF;

    7: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 7: FED_BATCH_TRANSITION (Nutrient Priming, Glucose Regulation, ATF Loop Wet-Out)     *)
       (* ----------------------------------------------------------------------------------------- *)
        rCmd_AgitatorSpeed_RPM := 60.0;

        (* Glucose Bolus Feed Regulation *)
        IF rVal_Estimated_Glucose < 3.20 THEN
            rCmd_NutrientFeed_Flow := 45.0; (* L/h *)
        ELSE
            rCmd_NutrientFeed_Flow := 15.0;
        END_IF;

        (* ATF Loop Slow Broth Recirculation Priming (5 cpm) to Eliminate Air Bubbles *)
        rCmd_ATF_CycleRate := 8.0;
        rCmd_PermeateHarvest_Flow := 0.0;

        (* Advance to Perfusion Cut-In when VCD Crosses 40 million cells/mL *)
        IF rVal_Estimated_VCD >= 40.0 AND rStateTimer_sec >= 1800.0 THEN
            eState := 8; (* Advance to Perfusion Cut-In Ramp *)
            rStateTimer_sec := 0.0;
        END_IF;

    8: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 8: PERFUSION_CUT_IN_RAMP (ATF Start 15 cpm, Permeate Ramp 0.2 to 1.0 VVD)             *)
       (* ----------------------------------------------------------------------------------------- *)
        rCmd_AgitatorSpeed_RPM := 65.0;
        rCmd_ATF_CycleRate := 18.0;

        (* Perfusion Ramp Rate: Increment Permeate Flow Towards 1.0 VVD (approx 833 L/h) *)
        IF rCmd_PermeateHarvest_Flow < 450.0 THEN
            rCmd_PermeateHarvest_Flow := rCmd_PermeateHarvest_Flow + (0.50 * rScanTime);
        END_IF;

        (* Coordinate Nutrient Media Feed with Harvest Extraction and Load Cell Level *)
        rCmd_NutrientFeed_Flow := rCmd_PermeateHarvest_Flow * 1.02;

        (* Accumulate Volumes *)
        rAccumulated_Permeate_Vol_L := rAccumulated_Permeate_Vol_L + (rCmd_PermeateHarvest_Flow * (rScanTime / 3600.0));
        rAccumulated_Feed_Vol_L := rAccumulated_Feed_Vol_L + (rCmd_NutrientFeed_Flow * (rScanTime / 3600.0));

        (* Transition to Steady-State Perfusion Chemostat when VCD >= 80 million cells/mL *)
        IF rVal_Estimated_VCD >= 80.0 AND rCmd_PermeateHarvest_Flow >= 400.0 THEN
            eState := 9; (* Advance to Steady-State High Density Perfusion *)
            rStateTimer_sec := 0.0;
        END_IF;

    9: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 9: STEADY_STATE_HIGH_DENSITY (Continuous Chemostat, VCD > 90 x 10^6 cells/mL)         *)
       (* ----------------------------------------------------------------------------------------- *)
        rCmd_AgitatorSpeed_RPM := 65.0;
        rCmd_ATF_CycleRate := 28.0;

        (* Steady Volumetric Perfusion Exchange: 1.50 to 2.00 VVD (1,250 to 1,660 L/h) *)
        IF rHarvestPermissive THEN
            rCmd_PermeateHarvest_Flow := 1250.0; (* L/h *)
        ELSE
            rCmd_PermeateHarvest_Flow := 200.0; (* Throttled Recirculation Bypass *)
        END_IF;

        rCmd_NutrientFeed_Flow := rCmd_PermeateHarvest_Flow;

        (* Accumulate Volumetric Production Records *)
        rAccumulated_Permeate_Vol_L := rAccumulated_Permeate_Vol_L + (rCmd_PermeateHarvest_Flow * (rScanTime / 3600.0));
        rAccumulated_Feed_Vol_L := rAccumulated_Feed_Vol_L + (rCmd_NutrientFeed_Flow * (rScanTime / 3600.0));

        (* Antifouling Backpulse Evaluation: Periodic Timer (every 900 s) OR High TMP (> 0.50 bar) *)
        rBackpulse_CycleTimer_sec := rBackpulse_CycleTimer_sec + rScanTime;
        IF (rBackpulse_CycleTimer_sec >= 900.0 OR rVal_Calculated_TMP >= 0.50 OR bManualBackpulseTrigger) THEN
            eState := 10; (* Branch to Membrane Backpulse Antifouling *)
            rStateTimer_sec := 0.0;
            rBackpulse_CycleTimer_sec := 0.0;
            bBackpulseActive := TRUE;
            rBackpulse_PulseDuration_sec := 0.0;
        ELSIF rVal_Estimated_VCD >= 102.0 AND bBleedPermissive THEN
            eState := 11; (* Branch to Automated Biomass Bleed *)
            rStateTimer_sec := 0.0;
        END_IF;

    10: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 10: MEMBRANE_BACKPULSE_ANTIFOULING (High-Pressure Sterile Reverse Permeate Pulse)     *)
        (* ----------------------------------------------------------------------------------------- *)
        (* Momentarily Halt Permeate Extraction Pump to Eliminate Forward Transmembrane Flux *)
        rCmd_PermeateHarvest_Flow := 0.0;
        rCmd_ATF_CycleRate := 38.0; (* Elevated Reciprocating Shear to Flush Detached Cake *)

        (* Execute 1.5-Second High-Pressure Sterile Filtrate Reverse Burst *)
        rBackpulse_PulseDuration_sec := rBackpulse_PulseDuration_sec + rScanTime;
        IF rBackpulse_PulseDuration_sec < 1.50 THEN
            bCmd_BackpulseValve_Open := TRUE;
        ELSE
            bCmd_BackpulseValve_Open := FALSE;
            (* Allow 10.0 Seconds for Cake Re-suspension and Shear Clearing *)
            IF rBackpulse_PulseDuration_sec >= 11.50 THEN
                bBackpulseActive := FALSE;
                eState := 9; (* Return to Steady-State Perfusion *)
                rStateTimer_sec := 0.0;
            END_IF;
        END_IF;

    11: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 11: BLEED_CELL_DENSITY_STABILIZATION (Biomass Bleed to Purge Dead / Senescent Cells)  *)
        (* ----------------------------------------------------------------------------------------- *)
        rCmd_AgitatorSpeed_RPM := 65.0;
        rCmd_ATF_CycleRate := 28.0;

        (* Engage Automated Cell Bleed Peristaltic Pump (45.0 L/h) *)
        rCmd_BleedPump_Flow := 45.0;
        rAccumulated_Bleed_Vol_L := rAccumulated_Bleed_Vol_L + (rCmd_BleedPump_Flow * (rScanTime / 3600.0));

        (* Maintain Steady Harvest Permeate *)
        rCmd_PermeateHarvest_Flow := 1250.0;
        rCmd_NutrientFeed_Flow := rCmd_PermeateHarvest_Flow + rCmd_BleedPump_Flow;

        (* Once Viable Cell Density Returns to Target Equilibrium (92 million cells/mL), Return *)
        IF rVal_Estimated_VCD <= 93.0 OR NOT bBleedPermissive THEN
            rCmd_BleedPump_Flow := 0.0;
            eState := 9; (* Return to Steady-State Chemostat *)
            rStateTimer_sec := 0.0;
        END_IF;

    12: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 12: FINAL_HARVEST_CONCENTRATION (Campaign Termination, Maximal Permeate Capture)      *)
        (* ----------------------------------------------------------------------------------------- *)
        rCmd_NutrientFeed_Flow := 0.0; (* Cut Fresh Media Feed *)
        rCmd_AgitatorSpeed_RPM := 40.0;
        rCmd_ATF_CycleRate := 22.0;

        (* Continue Permeate Extraction to Drain Broth to Residual Minimum (3,000 L) *)
        IF rVesselBrothVolume_L > 3000.0 THEN
            rCmd_PermeateHarvest_Flow := 650.0;
            rVesselBrothVolume_L := rVesselBrothVolume_L - (rCmd_PermeateHarvest_Flow * (rScanTime / 3600.0));
        ELSE
            rCmd_PermeateHarvest_Flow := 0.0;
            eState := 13; (* Advance to Thermal Biokill Inactivation *)
            rStateTimer_sec := 0.0;
        END_IF;

    13: (* ----------------------------------------------------------------------------------------- *)
       (* STATE 13: BIOKILL_THERMAL_DEACTIVATION (Residual Broth Inactivation @ 85 deg C for 60 min)   *)
       (* ----------------------------------------------------------------------------------------- *)
        rCmd_PermeateHarvest_Flow := 0.0;
        rCmd_NutrientFeed_Flow := 0.0;
        rCmd_BleedPump_Flow := 0.0;
        rCmd_ATF_CycleRate := 0.0;
        rCmd_SpargerO2_Flow := 0.0;
        rCmd_SpargerCO2_Flow := 0.0;
        rCmd_SpargerAir_Flow := 0.0;
        bCmd_SterileVentValve := TRUE;
        rCmd_AgitatorSpeed_RPM := 70.0;

        (* Pure Steam Jacket Heating to 85.0 deg C *)
        IF rVal_Voted_Temp < 85.0 THEN
            rCmd_JacketControl_Pct := 100.0;
        ELSE
            rCmd_JacketControl_Pct := 20.0; (* Thermal Maintenance *)
        END_IF;

        (* Hold at 85.0 deg C for 3,600 s (60 min) to Confirm 100% Thermal Inactivation *)
        IF rVal_Voted_Temp >= 84.5 AND rStateTimer_sec >= 3600.0 THEN
            eState := 0; (* Cycle Complete: Return to Standby *)
            rStateTimer_sec := 0.0;
        END_IF;

    14: (* ----------------------------------------------------------------------------------------- *)
        (* STATE 14: EMERGENCY_VENT_SAFE_STOP (Emergency Trip, Full Fluid Isolation, Sterile Hold)      *)
        (* ----------------------------------------------------------------------------------------- *)
        rCmd_JacketControl_Pct := -50.0; (* Arrest Cell Metabolism via Rapid Quench *)
        rCmd_SpargerO2_Flow := 0.0;
        rCmd_SpargerCO2_Flow := 0.0;
        rCmd_SpargerAir_Flow := 0.0;
        rCmd_SpargerN2_Flow := 0.0;
        rCmd_BasePump_Flow := 0.0;
        rCmd_NutrientFeed_Flow := 0.0;
        rCmd_ATF_CycleRate := 0.0;
        rCmd_PermeateHarvest_Flow := 0.0;
        rCmd_BleedPump_Flow := 0.0;
        rCmd_AgitatorSpeed_RPM := 0.0;
        bCmd_BackpulseValve_Open := FALSE;
        bCmd_CIP_SupplyValve := FALSE;
        bCmd_SIP_PureSteamValve := FALSE;
        bCmd_SIP_CondensateDrainValve := FALSE;
        bCmd_SterileVentValve := TRUE; (* Open Vent to Prevent Vacuum Collapse *)

        (* Operator Reset Permissive *)
        IF bAcknowledgeAlarms AND bEmergencyStop AND NOT bAlarm_Temp_HH AND NOT bAlarm_Headspace_HH AND NOT bAlarm_TMP_HH THEN
            eState := 0; (* Safe Reset to Standby *)
            rStateTimer_sec := 0.0;
        END_IF;
ELSE
    eState := 14; (* Safe Catch-All Fault State *)
END_CASE;
""")

    # -------------------------------------------------------------------------
    # PHASE 5: ISA-18.2 MULTI-TIER ALARMS & BIT-PACKED STATUS WORDS
    # -------------------------------------------------------------------------
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIERED ALARMS, DERIVATIVE TRIP MONITORS & STATUS WORD PACKING                *)
(* ==================================================================================================== *)

(* 5.1: RATE-OF-CHANGE (ROC) DERIVATIVE TRACKING *)
rRate_TMP_bar_s := (rVal_Calculated_TMP - rPrev_TMP) / rScanTime;
rRate_DO_pct_s := (rVal_Voted_DO - rPrev_DO) / rScanTime;
rRate_Pressure_bar_s := (rPressure_Headspace - rPrev_HeadspacePressure) / rScanTime;

rPrev_TMP := rVal_Calculated_TMP;
rPrev_DO := rVal_Voted_DO;
rPrev_HeadspacePressure := rPressure_Headspace;

IF rRate_TMP_bar_s > rLimit_ROC_TMP_Trip THEN
    bAlarm_ROC_TMP := TRUE;
ELSIF bAcknowledgeAlarms THEN
    bAlarm_ROC_TMP := FALSE;
END_IF;

IF rRate_DO_pct_s < rLimit_ROC_DO_Trip THEN
    bAlarm_ROC_DO := TRUE;
ELSIF bAcknowledgeAlarms THEN
    bAlarm_ROC_DO := FALSE;
END_IF;

IF rRate_Pressure_bar_s > rLimit_ROC_Pressure_Trip THEN
    bAlarm_ROC_Pressure := TRUE;
ELSIF bAcknowledgeAlarms THEN
    bAlarm_ROC_Pressure := FALSE;
END_IF;

(* 5.2: TEMPERATURE THRESHOLD MONITORING WITH HYSTERESIS DEADBAND *)
IF rVal_Voted_Temp >= rLimit_Temp_HH THEN
    bAlarm_Temp_HH := TRUE;
ELSIF rVal_Voted_Temp < (rLimit_Temp_HH - rLimit_Temp_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_Temp_HH := FALSE;
END_IF;

IF rVal_Voted_Temp >= rLimit_Temp_H THEN
    bAlarm_Temp_H := TRUE;
ELSIF rVal_Voted_Temp < (rLimit_Temp_H - rLimit_Temp_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_Temp_H := FALSE;
END_IF;

IF rVal_Voted_Temp <= rLimit_Temp_LL THEN
    bAlarm_Temp_LL := TRUE;
ELSIF rVal_Voted_Temp > (rLimit_Temp_LL + rLimit_Temp_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_Temp_LL := FALSE;
END_IF;

IF rVal_Voted_Temp <= rLimit_Temp_L THEN
    bAlarm_Temp_L := TRUE;
ELSIF rVal_Voted_Temp > (rLimit_Temp_L + rLimit_Temp_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_Temp_L := FALSE;
END_IF;

(* 5.3: DISSOLVED OXYGEN THRESHOLD MONITORING *)
IF rVal_Voted_DO >= rLimit_DO_HH THEN
    bAlarm_DO_HH := TRUE;
ELSIF rVal_Voted_DO < (rLimit_DO_HH - rLimit_DO_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_DO_HH := FALSE;
END_IF;

IF rVal_Voted_DO >= rLimit_DO_H THEN
    bAlarm_DO_H := TRUE;
ELSIF rVal_Voted_DO < (rLimit_DO_H - rLimit_DO_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_DO_H := FALSE;
END_IF;

IF rVal_Voted_DO <= rLimit_DO_LL THEN
    bAlarm_DO_LL := TRUE;
ELSIF rVal_Voted_DO > (rLimit_DO_LL + rLimit_DO_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_DO_LL := FALSE;
END_IF;

IF rVal_Voted_DO <= rLimit_DO_L THEN
    bAlarm_DO_L := TRUE;
ELSIF rVal_Voted_DO > (rLimit_DO_L + rLimit_DO_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_DO_L := FALSE;
END_IF;

(* 5.4: CULTURE BROTH pH THRESHOLD MONITORING *)
IF rVal_Voted_PH >= rLimit_PH_HH THEN
    bAlarm_PH_HH := TRUE;
ELSIF rVal_Voted_PH < (rLimit_PH_HH - rLimit_PH_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_PH_HH := FALSE;
END_IF;

IF rVal_Voted_PH >= rLimit_PH_H THEN
    bAlarm_PH_H := TRUE;
ELSIF rVal_Voted_PH < (rLimit_PH_H - rLimit_PH_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_PH_H := FALSE;
END_IF;

IF rVal_Voted_PH <= rLimit_PH_LL THEN
    bAlarm_PH_LL := TRUE;
ELSIF rVal_Voted_PH > (rLimit_PH_LL + rLimit_PH_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_PH_LL := FALSE;
END_IF;

IF rVal_Voted_PH <= rLimit_PH_L THEN
    bAlarm_PH_L := TRUE;
ELSIF rVal_Voted_PH > (rLimit_PH_L + rLimit_PH_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_PH_L := FALSE;
END_IF;

(* 5.5: TRANSMEMBRANE PRESSURE (TMP) & HEADSPACE PRESSURE MONITORING *)
IF rVal_Calculated_TMP >= rLimit_TMP_HH THEN
    bAlarm_TMP_HH := TRUE;
ELSIF rVal_Calculated_TMP < (rLimit_TMP_HH - rLimit_TMP_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_TMP_HH := FALSE;
END_IF;

IF rVal_Calculated_TMP >= rLimit_TMP_H THEN
    bAlarm_TMP_H := TRUE;
ELSIF rVal_Calculated_TMP < (rLimit_TMP_H - rLimit_TMP_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_TMP_H := FALSE;
END_IF;

IF rPressure_Headspace >= rLimit_Headspace_HH THEN
    bAlarm_Headspace_HH := TRUE;
ELSIF rPressure_Headspace < (rLimit_Headspace_HH - rLimit_Headspace_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_Headspace_HH := FALSE;
END_IF;

IF rPressure_Headspace >= rLimit_Headspace_H THEN
    bAlarm_Headspace_H := TRUE;
ELSIF rPressure_Headspace < (rLimit_Headspace_H - rLimit_Headspace_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_Headspace_H := FALSE;
END_IF;

IF rPressure_Headspace <= rLimit_Headspace_L AND eState >= 4 AND eState <= 12 THEN
    bAlarm_Headspace_L := TRUE;
ELSIF rPressure_Headspace > (rLimit_Headspace_L + rLimit_Headspace_Deadband) AND bAcknowledgeAlarms THEN
    bAlarm_Headspace_L := FALSE;
END_IF;

(* 5.6: METABOLITE & RESPIROMETRIC ALARMS *)
IF rVal_Estimated_Glucose <= rLimit_Glucose_LL AND eState >= 6 AND eState <= 11 THEN
    bAlarm_Glucose_LL := TRUE;
ELSIF rVal_Estimated_Glucose > (rLimit_Glucose_LL + 0.20) AND bAcknowledgeAlarms THEN
    bAlarm_Glucose_LL := FALSE;
END_IF;

IF rVal_Estimated_Glucose <= rLimit_Glucose_L AND eState >= 6 AND eState <= 11 THEN
    bAlarm_Glucose_L := TRUE;
ELSIF rVal_Estimated_Glucose > (rLimit_Glucose_L + 0.25) AND bAcknowledgeAlarms THEN
    bAlarm_Glucose_L := FALSE;
END_IF;

IF rVal_Estimated_Lactate >= rLimit_Lactate_HH THEN
    bAlarm_Lactate_HH := TRUE;
ELSIF rVal_Estimated_Lactate < (rLimit_Lactate_HH - 0.30) AND bAcknowledgeAlarms THEN
    bAlarm_Lactate_HH := FALSE;
END_IF;

IF rVal_Estimated_Lactate >= rLimit_Lactate_H THEN
    bAlarm_Lactate_H := TRUE;
ELSIF rVal_Estimated_Lactate < (rLimit_Lactate_H - 0.20) AND bAcknowledgeAlarms THEN
    bAlarm_Lactate_H := FALSE;
END_IF;

IF rVal_Calculated_RQ >= rLimit_RQ_H THEN
    bAlarm_RQ_H := TRUE;
ELSIF rVal_Calculated_RQ < (rLimit_RQ_H - 0.08) AND bAcknowledgeAlarms THEN
    bAlarm_RQ_H := FALSE;
END_IF;

(* Critical Emergency Safe Stop Interlock Assertion *)
IF bAlarm_Temp_HH OR bAlarm_Headspace_HH OR bAlarm_TMP_HH OR bAlarm_AllTempSensorsFailed OR bAlarm_AllDOSensorsFailed OR bAlarm_AllPHSensorsFailed OR NOT bEmergencyStop THEN
    eState := 14; (* Immediately Command Emergency Vent Safe Stop *)
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.7: BIT-PACKED ISA-18.2 CRITICAL EMERGENCY ALARMS (wAlarmWord_Critical_HH)                           *)
(* ---------------------------------------------------------------------------------------------------- *)
wAlarmWord_Critical_HH := 16#00000000;
IF bAlarm_Temp_HH              THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000001; END_IF;
IF bAlarm_DO_HH                THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000002; END_IF;
IF bAlarm_PH_HH                THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000004; END_IF;
IF bAlarm_TMP_HH               THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000008; END_IF;
IF bAlarm_Headspace_HH         THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000010; END_IF;
IF bAlarm_Glucose_LL           THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000020; END_IF;
IF bAlarm_Lactate_HH           THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000040; END_IF;
IF bAlarm_AllTempSensorsFailed THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000080; END_IF;
IF bAlarm_AllDOSensorsFailed   THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000100; END_IF;
IF bAlarm_AllPHSensorsFailed   THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000200; END_IF;
IF bAlarm_AllFeedPressFailed   THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000400; END_IF;
IF bAlarm_ROC_Pressure         THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00000800; END_IF;
IF bAlarm_ROC_TMP              THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00001000; END_IF;
IF NOT bEmergencyStop          THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00002000; END_IF;
IF rVesselWeight_kg < 2500.0 AND eState >= 4 THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00004000; END_IF;
IF eState = 14                 THEN wAlarmWord_Critical_HH := wAlarmWord_Critical_HH OR 16#00008000; END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.8: BIT-PACKED ISA-18.2 OPERATIONAL WARNING ALARMS (wAlarmWord_Warning_H)                           *)
(* ---------------------------------------------------------------------------------------------------- *)
wAlarmWord_Warning_H := 16#00000000;
IF bAlarm_Temp_H           THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000001; END_IF;
IF bAlarm_Temp_L           THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000002; END_IF;
IF bAlarm_DO_H             THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000004; END_IF;
IF bAlarm_DO_L             THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000008; END_IF;
IF bAlarm_PH_H             THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000010; END_IF;
IF bAlarm_PH_L             THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000020; END_IF;
IF bAlarm_TMP_H            THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000040; END_IF;
IF bAlarm_Headspace_H      THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000080; END_IF;
IF bAlarm_Headspace_L      THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000100; END_IF;
IF bAlarm_Glucose_L        THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000200; END_IF;
IF bAlarm_Lactate_H        THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000400; END_IF;
IF bAlarm_RQ_H             THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00000800; END_IF;
IF bAlarm_ROC_DO           THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00001000; END_IF;
IF NOT bRaman_SignalValid  THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00002000; END_IF;
IF bBackpulseActive        THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00004000; END_IF;
IF rWFI_Conductivity_uScm > 1.30 AND eState = 1 THEN wAlarmWord_Warning_H := wAlarmWord_Warning_H OR 16#00008000; END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.9: BIT-PACKED 2oo3 TMR SENSOR CHANNEL HEALTH STATUS WORD (wSensorHealthStatusWord)                 *)
(* ---------------------------------------------------------------------------------------------------- *)
wSensorHealthStatusWord := 16#00000000;
IF bFault_Temp_A          THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000001; END_IF;
IF bFault_Temp_B          THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000002; END_IF;
IF bFault_Temp_C          THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000004; END_IF;
IF bFault_DO_A            THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000008; END_IF;
IF bFault_DO_B            THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000010; END_IF;
IF bFault_DO_C            THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000020; END_IF;
IF bFault_PH_A            THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000040; END_IF;
IF bFault_PH_B            THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000080; END_IF;
IF bFault_PH_C            THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000100; END_IF;
IF bFault_FeedPress_A     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000200; END_IF;
IF bFault_FeedPress_B     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000400; END_IF;
IF bFault_FeedPress_C     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00000800; END_IF;
IF bFault_OffGas_O2_A     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00001000; END_IF;
IF bFault_OffGas_O2_B     THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00002000; END_IF;
IF bFault_OffGas_CO2_A    THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00004000; END_IF;
IF bFault_OffGas_CO2_B    THEN wSensorHealthStatusWord := wSensorHealthStatusWord OR 16#00008000; END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 5.10: BIT-PACKED PROCESS AUTOMATION & INTERLOCK PERMISSIVE STATUS (wAutomationStatusWord)             *)
(* ---------------------------------------------------------------------------------------------------- *)
wAutomationStatusWord := 16#00000000;
IF eState = 0                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000001; END_IF; (* Standby *)
IF eState = 1                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000002; END_IF; (* CIP *)
IF eState = 2                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000004; END_IF; (* SIP *)
IF eState = 3                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000008; END_IF; (* Cooldown *)
IF eState = 4                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000010; END_IF; (* Media Fill *)
IF eState = 5                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000020; END_IF; (* Inoculation *)
IF eState = 6                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000040; END_IF; (* Batch Growth *)
IF eState = 7                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000080; END_IF; (* Fed-Batch *)
IF eState = 8                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000100; END_IF; (* Perfusion Ramp *)
IF eState = 9                  THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000200; END_IF; (* Steady Chemostat *)
IF eState = 10                 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000400; END_IF; (* Backpulse *)
IF eState = 11                 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00000800; END_IF; (* Cell Bleed *)
IF eState = 12                 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00001000; END_IF; (* Final Harvest *)
IF eState = 13                 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00002000; END_IF; (* Biokill *)
IF eState = 14                 THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00004000; END_IF; (* Emergency Stop *)
IF bHarvestPermissive          THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00008000; END_IF;
IF bBleedPermissive            THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00010000; END_IF;
IF bCIP_SupplyPermissive       THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00020000; END_IF;
IF bSIP_SteamPermissive        THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00040000; END_IF;
IF bStartProduction            THEN wAutomationStatusWord := wAutomationStatusWord OR 16#00080000; END_IF;

END_FUNCTION_BLOCK
""")

    return "".join(lines)

if __name__ == "__main__":
    code = generate_iec_block()
    print(f"Total lines: {len(code.splitlines())}")
    print(f"Total chars: {len(code)}")
