# generate_nuclear_dataset.py
# Generator and validator for FB_Nuclear_SMR_PrimaryCoolant_ControlRodScram

import os
import sys
import re
import json
import uuid

def build_st_code():
    code_parts = []
    
    # Header and declaration
    code_parts.append("""FUNCTION_BLOCK FB_Nuclear_SMR_PrimaryCoolant_ControlRodScram
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Nuclear Power Generation & Clean Energy Infrastructure
 * SYSTEM                       : 300 MWe Pressurized Water Small Modular Reactor (SMR) Nuclear Island
 * SUBSYSTEMS INTEGRATED        : Control Rod Drive Mechanism (CRDM) Magnetic Jack Stepping Synchronization (0.1 mm precision,
 *                                fast scram gravity drop < 1.8 s), Primary Reactor Coolant System (RCS) Canned Motor Pump
 *                                Speed & Variable Differential Pressure Decoupling, In-Vessel Pressurizer Dynamic Subcooled
 *                                Water Spray & Immersion Heater Proportional Band Pressure Control (155.0 bar +/- 0.2 bar),
 *                                Ex-Core Triplicated Neutron Ionization Chamber Flux & Reactor Period Monitoring, and
 *                                Passive Residual Heat Removal System (PRHRS) Natural Circulation Cooling Loop.
 * SAFETY INTEGRITY LEVEL       : IEC 61508 SIL 3 / IEC 61513 Nuclear Safety Class 1E / IEEE 603 Reactor Protection System
 * SCAN CYCLE EXECUTION PERIOD  : 5.0 ms (T_s = 0.005 s) Deterministic Real-Time Hard Cyclic Interrupt
 * MATHEMATICAL FORMULATION     : Discretized 6-group delayed neutron point reactor kinetics with Doppler fuel temperature (alpha_f)
 *                                and moderator density (alpha_m) reactivity feedbacks, 2-region non-equilibrium pressurizer mass
 *                                and energy balances (subcooled flashing and condensation rates), primary coolant forced and
 *                                natural circulation momentum conservation, Fourier radial conduction through fuel pellet and
 *                                Zircaloy cladding to coolant bulk, Receding-Horizon Model Predictive Control (MPC) quadratic cost
 *                                optimization (Np=5, Nu=3), 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers,
 *                                12-state Nuclear Island operational Finite State Machine (FSM), and 5-tier ISA-18.2 process alarms.
 * ===================================================================================================================== *)
""")

    # VAR_INPUT
    code_parts.append("""VAR_INPUT
    (* =================================================================================================================
     * SECTION 1: 2oo3 REDUNDANT PROCESS SENSORS (10 REDUNDANT TRIPLETS, TOTAL 30 TRANSMITTERS)
     * ================================================================================================================= *)
    (* In-Vessel Pressurizer Saturated Steam/Water Pressure Transmitters [bar], Calibrated 0.0 .. 200.0 bar *)
    PT_PRESSURIZER_101A             : REAL; (* Pressurizer Saturated Pressure Transmitter Ch A [bar] *)
    PT_PRESSURIZER_101B             : REAL; (* Pressurizer Saturated Pressure Transmitter Ch B [bar] *)
    PT_PRESSURIZER_101C             : REAL; (* Pressurizer Saturated Pressure Transmitter Ch C [bar] *)

    (* In-Vessel Pressurizer Collapsed Liquid Water Level Transmitters [%], Calibrated 0.0 .. 100.0 % *)
    LT_PRESSURIZER_LEVEL_102A       : REAL; (* Pressurizer Collapsed Liquid Level Ch A [%] *)
    LT_PRESSURIZER_LEVEL_102B       : REAL; (* Pressurizer Collapsed Liquid Level Ch B [%] *)
    LT_PRESSURIZER_LEVEL_102C       : REAL; (* Pressurizer Collapsed Liquid Level Ch C [%] *)

    (* Primary Reactor Coolant Core Exit Hot Leg Temperature Transmitters [deg C], Calibrated 0.0 .. 400.0 deg C *)
    TT_HOT_LEG_TEMP_201A            : REAL; (* RCS Core Outlet Hot Leg Temperature Ch A [deg C] *)
    TT_HOT_LEG_TEMP_201B            : REAL; (* RCS Core Outlet Hot Leg Temperature Ch B [deg C] *)
    TT_HOT_LEG_TEMP_201C            : REAL; (* RCS Core Outlet Hot Leg Temperature Ch C [deg C] *)

    (* Primary Reactor Coolant Steam Generator Outlet Cold Leg Temperature Transmitters [deg C], Calibrated 0.0 .. 400.0 deg C *)
    TT_COLD_LEG_TEMP_202A           : REAL; (* RCS SG Outlet Cold Leg Temperature Ch A [deg C] *)
    TT_COLD_LEG_TEMP_202B           : REAL; (* RCS SG Outlet Cold Leg Temperature Ch B [deg C] *)
    TT_COLD_LEG_TEMP_202C           : REAL; (* RCS SG Outlet Cold Leg Temperature Ch C [deg C] *)

    (* Ex-Core Triplicated Neutron Ionization Chamber Power Range Flux Transmitters [% RTP], Calibrated 0.0 .. 150.0 % RTP *)
    NIT_EXCORE_POWER_RANGE_301A     : REAL; (* Ex-Core Power Range Neutron Flux Ch A [% RTP] *)
    NIT_EXCORE_POWER_RANGE_301B     : REAL; (* Ex-Core Power Range Neutron Flux Ch B [% RTP] *)
    NIT_EXCORE_POWER_RANGE_301C     : REAL; (* Ex-Core Power Range Neutron Flux Ch C [% RTP] *)

    (* Ex-Core Intermediate Range Gamma-Compensated Ionization Chamber Flux Transmitters [% RTP / decade] *)
    NIT_INTERMEDIATE_RANGE_302A     : REAL; (* Ex-Core Intermediate Range Flux Ch A [% RTP] *)
    NIT_INTERMEDIATE_RANGE_302B     : REAL; (* Ex-Core Intermediate Range Flux Ch B [% RTP] *)
    NIT_INTERMEDIATE_RANGE_302C     : REAL; (* Ex-Core Intermediate Range Flux Ch C [% RTP] *)

    (* Control Rod Drive Mechanism (CRDM) Magnetic Reed Encoder Bank Position Transmitters [mm], Calibrated 0.0 .. 3600.0 mm *)
    ZT_CRDM_STEP_POS_401A           : REAL; (* CRDM Regulating Rod Bank Position Ch A [mm] *)
    ZT_CRDM_STEP_POS_401B           : REAL; (* CRDM Regulating Rod Bank Position Ch B [mm] *)
    ZT_CRDM_STEP_POS_401C           : REAL; (* CRDM Regulating Rod Bank Position Ch C [mm] *)

    (* Primary Coolant Loop Venturi Differential Pressure Volumetric Flow Rate Transmitters [m3/h], Calibrated 0.0 .. 12000.0 m3/h *)
    FT_PRIMARY_COOLANT_501A         : REAL; (* Primary Coolant Total Loop Volumetric Flow Ch A [m3/h] *)
    FT_PRIMARY_COOLANT_501B         : REAL; (* Primary Coolant Total Loop Volumetric Flow Ch B [m3/h] *)
    FT_PRIMARY_COOLANT_501C         : REAL; (* Primary Coolant Total Loop Volumetric Flow Ch C [m3/h] *)

    (* Passive Residual Heat Removal System (PRHRS) Natural Circulation Steam Header Pressure Transmitters [bar] *)
    PT_PRHRS_STEAM_601A             : REAL; (* PRHRS Heat Exchanger Steam Header Pressure Ch A [bar] *)
    PT_PRHRS_STEAM_601B             : REAL; (* PRHRS Heat Exchanger Steam Header Pressure Ch B [bar] *)
    PT_PRHRS_STEAM_601C             : REAL; (* PRHRS Heat Exchanger Steam Header Pressure Ch C [bar] *)

    (* Core Exit Thermocouple Fuel Cladding Peak Temperature Transmitters [deg C], Calibrated 0.0 .. 1200.0 deg C *)
    TT_CLADDING_PEAK_701A           : REAL; (* Core Sub-Channel Fuel Cladding Peak Temp Ch A [deg C] *)
    TT_CLADDING_PEAK_701B           : REAL; (* Core Sub-Channel Fuel Cladding Peak Temp Ch B [deg C] *)
    TT_CLADDING_PEAK_701C           : REAL; (* Core Sub-Channel Fuel Cladding Peak Temp Ch C [deg C] *)

    (* =================================================================================================================
     * SECTION 2: OPERATOR COMMANDS, CLASS 1E TRIP CONTACTS & SUPERVISORY SETPOINTS
     * ================================================================================================================= *)
    bManualScramPB_ChA              : BOOL; (* Class 1E Hardwired Manual Reactor Scram Pushbutton Contact Train A [FALSE=Trip] *)
    bManualScramPB_ChB              : BOOL; (* Class 1E Hardwired Manual Reactor Scram Pushbutton Contact Train B [FALSE=Trip] *)
    bAutoControlEnable              : BOOL; (* Master Supervisory Plant Automation Enable Interlock *)
    bTurbineTripInterlock           : BOOL; (* Fast Turbine Stop Valve Closure / Load Rejection Signal [TRUE=Tripped] *)
    bSafetyInjectionActive          : BOOL; (* Engineered Safety Features Actuation System (ESFAS) Active [TRUE=Active] *)
    bContainmentIsolationSignal     : BOOL; (* Containment Phase A/B Isolation Actuation Interlock *)
    rThermalPowerSetpoint           : REAL; (* Target Reactor Thermal Power Regulated Setpoint [% RTP], Nominal: 100.0 *)
    rPressurizerPressSetpoint       : REAL; (* Pressurizer Regulated Saturated Pressure Setpoint [bar], Nominal: 155.0 *)
    rPressurizerLevelSetpoint       : REAL; (* Pressurizer Regulated Liquid Water Level Setpoint [%], Nominal: 55.0 *)
    rAxialOffsetTarget              : REAL; (* Core Axial Flux Offset Target Delta-I [%], Nominal: 0.0 +/- 2.5 % *)
    rRCS_TargetPumpSpeed_RPM        : REAL; (* Nominal Primary Canned Motor Coolant Pump VFD Speed [RPM], Nominal: 1485.0 *)
    rCycleTime_s                    : REAL; (* Real-Time Deterministic Cyclic Scan Interval [s], Nominal: 0.005 (5 ms) *)
    bAlarmAcknowledge               : BOOL; (* ISA-18.2 Operator Alarm Silence and Acknowledge Pushbutton *)
    bMasterFaultReset               : BOOL; (* Master Supervisory Trip and Safety Interlock Reset Command *)
END_VAR
""")

    # VAR_OUTPUT
    code_parts.append("""VAR_OUTPUT
    (* =================================================================================================================
     * SECTION 3: ACTUATOR DRIVE SIGNALS & SAFETY DISCONNECT COMMANDS
     * ================================================================================================================= *)
    (* Class 1E Reactor Trip Switchgear Breakers (Under-Voltage Coil Power Supply: FALSE = Breaker Open / Tripped) *)
    bReactorTripBreaker_RTBA        : BOOL; (* Reactor Trip Switchgear Breaker A Coil Energization [FALSE=Open/Tripped] *)
    bReactorTripBreaker_RTBB        : BOOL; (* Reactor Trip Switchgear Breaker B Coil Energization [FALSE=Open/Tripped] *)

    (* CRDM Magnetic Jack Gripper Coils Fast De-Energization (Class 1E Solid-State Power Switches: FALSE = Gravity Drop) *)
    bCRDM_HoldCoilPower_ChA         : BOOL; (* CRDM Stationary Gripper Coil Power Bus Train A [FALSE=Gravity Scram] *)
    bCRDM_HoldCoilPower_ChB         : BOOL; (* CRDM Stationary Gripper Coil Power Bus Train B [FALSE=Gravity Scram] *)

    (* CRDM Stepping Actuation Modulation *)
    rCRDM_StepRateDemand            : REAL; (* CRDM Stepping Speed Demand [steps/min, -72.0 .. +72.0], Sign: +Out/-In *)
    nCRDM_StepDirection             : INT;  (* CRDM Direction Command: +1=Withdrawal, 0=Hold, -1=Insertion *)
    bCRDM_MovableGripperPulse       : BOOL; (* Magnetic Jack Movable Gripper Coil Pulse Sequence Train *)
    bCRDM_LiftCoilPulse             : BOOL; (* Magnetic Jack Lift Coil Stepping Pulse Sequence Train *)

    (* In-Vessel Pressurizer Electric Immersion Heaters & Subcooled Continuous Spray Modulation *)
    rPressurizerPropHeater_kW       : REAL; (* Proportional Electric Immersion Heaters Power Output [kW], Range: 0.0 .. 800.0 *)
    rPressurizerBackupHeaters_kW    : REAL; (* Backup Electric Immersion Heaters On/Off Power Output [kW], Range: 0.0 .. 1200.0 *)
    rPressurizerSprayValveOpening   : REAL; (* Pressurizer Subcooled Continuous Spray Control Valve Opening [%], 0.0 .. 100.0 *)
    rPressurizerAuxSprayFlow_m3h    : REAL; (* CVCS Chemical & Volume Control System Auxiliary Spray Flow [m3/h], 0.0 .. 15.0 *)

    (* Primary Reactor Coolant Canned Motor Pumps Speed Demands *)
    rRCS_CannedPumpSpeedDemand_RPM  : REAL; (* Canned Motor Primary Coolant Pump VFD Speed Reference [RPM], 0.0 .. 1800.0 *)
    rRCS_PumpDifferentialPress_bar  : REAL; (* Calculated Net Developed Hydraulic Head Across Canned Motor Pumps [bar] *)

    (* Passive Residual Heat Removal System (PRHRS) Natural Circulation Loop Isolation Actuation *)
    bPRHRS_IsolationValve_01        : BOOL; (* PRHRS Loop 1 Fail-Open Natural Circulation Isolation Valve [TRUE=Open] *)
    bPRHRS_IsolationValve_02        : BOOL; (* PRHRS Loop 2 Fail-Open Natural Circulation Isolation Valve [TRUE=Open] *)

    (* =================================================================================================================
     * SECTION 4: 2oo3 VOTED PROCESS VALUES & PHYSICAL STATE ESTIMATIONS
     * ================================================================================================================= *)
    rVoted_PressurizerPressure_bar  : REAL; (* 2oo3 Validated Pressurizer Saturated Steam Pressure [bar] *)
    rVoted_PressurizerLevel_pct     : REAL; (* 2oo3 Validated Pressurizer Collapsed Water Level [%] *)
    rVoted_HotLegTemp_degC          : REAL; (* 2oo3 Validated Reactor Coolant Core Exit Hot Leg Temp [deg C] *)
    rVoted_ColdLegTemp_degC         : REAL; (* 2oo3 Validated Reactor Coolant SG Outlet Cold Leg Temp [deg C] *)
    rVoted_PowerRangeFlux_pct       : REAL; (* 2oo3 Validated Ex-Core Thermal Neutron Flux Power [% RTP] *)
    rVoted_IntermediateFlux_pct     : REAL; (* 2oo3 Validated Ex-Core Intermediate Range Flux [% RTP] *)
    rVoted_CRDM_Position_mm         : REAL; (* 2oo3 Validated Control Rod Regulating Bank Elevation [mm] *)
    rVoted_PrimaryFlow_m3h          : REAL; (* 2oo3 Validated Primary Coolant Loop Total Flow Rate [m3/h] *)
    rVoted_PRHRS_SteamPress_bar     : REAL; (* 2oo3 Validated PRHRS Condenser Header Steam Pressure [bar] *)
    rVoted_CladdingPeakTemp_degC    : REAL; (* 2oo3 Validated Sub-Channel Peak Fuel Cladding Temp [deg C] *)

    (* Calculated Cyber-Physical Core State Observables *)
    rReactorPeriod_s                : REAL; (* Ex-Core Dynamic Reactor Period e-folding time [s] *)
    rReactivity_pcm                 : REAL; (* Reconstructed Core Net Reactivity [pcm] (1 pcm = 1.0E-5 dk/k) *)
    rAxialOffset_pct                : REAL; (* Core Axial Flux Offset Imbalance Delta-I [%] *)
    rFuelCenterlineTemp_degC        : REAL; (* Estimated Peak Fuel Pellet Centerline Temperature [deg C] *)
    rDepartureFromNucleateBoilingRatio : REAL; (* Thermal Margin DNBR Index [-], Must remain > 1.30 *)
    rNaturalCirculationBuoyancy_kPa : REAL; (* Primary Loop Thermosiphon Natural Circulation Buoyancy Head [kPa] *)

    (* Operational State Machine Status & Safety Interlock Status *)
    nActiveFSMState                 : INT;        (* Current Nuclear Island FSM Operational State Index [1..12] *)
    sActiveFSMStateName             : STRING[32]; (* Current Nuclear Island FSM Operational State Text Descriptor *)
    bReactorScramLatched            : BOOL;       (* Class 1E Nuclear Reactor Protective Trip Latched Flag *)
    bSafetyInjectionRequired        : BOOL;       (* ESFAS Safety Injection System Emergency Signal Flag *)
    bPRHRS_Active                   : BOOL;       (* PRHRS Natural Circulation Decay Heat Loop In Operation *)
    bThermalHydraulicStable         : BOOL;       (* Pressurizer Pressure & Level Within MPC High-Precision Deadbands *)

    (* ISA-18.2 Diagnostic & Alarm Status Packing Registers *)
    wDiagnosticWord01               : WORD; (* Diagnostic Word 01: 2oo3 Sensor Health & Channel Discrepancy Fault Flags *)
    wDiagnosticWord02               : WORD; (* Diagnostic Word 02: ISA-18.2 HI_HI & LO_LO Class 1E Protective Trip Bits *)
    wDiagnosticWord03               : WORD; (* Diagnostic Word 03: ISA-18.2 HI, LO, & ROC Operational Warning Alarm Bits *)
    wDiagnosticWord04               : WORD; (* Diagnostic Word 04: Cyber-Physical Margins, MPC Optimization & Interlock Bits *)
END_VAR
""")

    # VAR
    code_parts.append("""VAR
    (* =================================================================================================================
     * SECTION 5: DISCRETE 8x8 STATE-SPACE MATRICES & KALMAN OBSERVER GAINS (Ts = 5 ms)
     * States: x1: Neutron Power n/n0 [-], x2: Delayed Precursors C/C0 [-], x3: Fuel Temp Tf [deg C],
     *         x4: Clad Temp Tc [deg C], x5: Core Coolant Temp Tcore [deg C], x6: Pressurizer Press Pprz [bar],
     *         x7: Pressurizer Level Lprz [%], x8: Axial Offset Delta-I [%]
     * Inputs: u1: CRDM Rate [pcm/s], u2: Heaters [kW], u3: Spray [%], u4: Pump Speed [RPM]
     * ================================================================================================================= *)
    aStateA                         : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    aStateB                         : ARRAY[1..8, 1..4] OF REAL; (* Discrete Control Input Coupling Matrix B (8x4) *)
    aStateC                         : ARRAY[1..8, 1..8] OF REAL; (* State Observation Output Matrix C (8x8) *)
    aStateD                         : ARRAY[1..8, 1..4] OF REAL; (* Direct Feedthrough Matrix D (8x4) *)
    aKalmanGainL                    : ARRAY[1..8, 1..8] OF REAL; (* Discrete Steady-State Kalman Filter Observer Gain Matrix L (8x8) *)

    aStateVector                    : ARRAY[1..8] OF REAL; (* Current State Vector x[k] *)
    aStateVectorNext                : ARRAY[1..8] OF REAL; (* Propagated State Vector x[k+1] *)
    aStateEstimated                 : ARRAY[1..8] OF REAL; (* Kalman Filter Estimated State Vector x_hat[k] *)
    aStateReference                 : ARRAY[1..8] OF REAL; (* Reference Setpoint Vector r[k] *)
    aStateError                     : ARRAY[1..8] OF REAL; (* State Tracking Error e[k] = r[k] - x_hat[k] *)
    aControlVector                  : ARRAY[1..4] OF REAL; (* Active Control Actuator Vector u[k] *)
    aControlVectorPrev              : ARRAY[1..4] OF REAL; (* Prior Step Control Vector u[k-1] *)
    aDeltaControlVector             : ARRAY[1..4] OF REAL; (* Actuator Slew Increment Delta_u[k] = u[k] - u[k-1] *)

    (* =================================================================================================================
     * SECTION 6: MODEL PREDICTIVE CONTROL (MPC) RECEDING-HORIZON QUADRATIC MATRICES (Np=5, Nu=3)
     * ================================================================================================================= *)
    aMPC_Q                          : ARRAY[1..8, 1..8] OF REAL; (* State Tracking Error Penalty Matrix Q (8x8) *)
    aMPC_R                          : ARRAY[1..4, 1..4] OF REAL; (* Actuator Effort Penalty Matrix R (4x4) *)
    aMPC_S                          : ARRAY[1..4, 1..4] OF REAL; (* Actuator Slew Rate Variation Penalty Matrix S (4x4) *)
    aMPC_P_Terminal                 : ARRAY[1..8, 1..8] OF REAL; (* Terminal State Cost Penalty Matrix P (8x8) *)

    aPredictedState                 : ARRAY[1..5, 1..8] OF REAL; (* Horizon Predicted State Trajectories [p, i] *)
    aPredictedControl               : ARRAY[1..3, 1..4] OF REAL; (* Horizon Control Trajectories [u_step, m] *)
    rBestCandidateCost              : REAL;                      (* Minimal Evaluated Quadratic Cost Functional Value J* *)
    aOptimalDeltaU                  : ARRAY[1..4] OF REAL;       (* Optimized Control Perturbation Delta_u* *)

    (* Candidate search perturbations for MPC quadratic gradient minimization *)
    aCandidateD1                    : ARRAY[1..5] OF REAL; (* CRDM rate test candidates [pcm/s] *)
    aCandidateD2                    : ARRAY[1..5] OF REAL; (* Proportional heater test candidates [kW] *)
    aCandidateD3                    : ARRAY[1..5] OF REAL; (* Spray valve test candidates [%] *)
    aCandidateD4                    : ARRAY[1..5] OF REAL; (* Primary pump speed test candidates [RPM] *)

    (* =================================================================================================================
     * SECTION 7: POINT REACTOR KINETICS & THERMAL-HYDRAULIC COUPLING VARIABLES
     * ================================================================================================================= *)
    aPrecursorLambda                : ARRAY[1..6] OF REAL; (* 6 Delayed Precursor Group Decay Constants [1/s] *)
    aPrecursorBeta                  : ARRAY[1..6] OF REAL; (* 6 Delayed Precursor Group Yield Fractions [-] *)
    aPrecursorConcentration         : ARRAY[1..6] OF REAL; (* 6 Delayed Precursor Normalized Group Densities C_i [-] *)
    rPromptGenerationTime_s         : REAL;                (* Prompt Neutron Lifetime Lambda [s], Nom: 2.5E-5 s *)
    rTotalDelayedFractionBeta       : REAL;                (* Total Delayed Neutron Fraction Beta = Sum(Beta_i) *)
    rDopplerReactivityCoeff_pcm     : REAL;                (* Fuel Doppler Reactivity Temperature Coeff [pcm/deg C] *)
    rModeratorDensityCoeff_pcm      : REAL;                (* Moderator Reactivity Density/Temp Coeff [pcm/deg C] *)
    rCRDM_DifferentialWorth_pcm_mm  : REAL;                (* CRDM Regulating Rod Differential Worth [pcm/mm] *)
    rBoronReactivityCoeff_pcm_ppm   : REAL;                (* Soluble Boron Chemical Shim Reactivity Worth [pcm/ppm] *)
    rSolubleBoronConcentration_ppm  : REAL;                (* Active Soluble Boron Chemical Concentration [ppm] *)

    (* Xenon-135 and Iodine-135 Transient Tracking *)
    rIodineConcentration            : REAL; (* Iodine-135 Core Inventory Normalized Concentration [-] *)
    rXenonConcentration             : REAL; (* Xenon-135 Core Inventory Normalized Concentration [-] *)
    rIodineDecayConstant_1s         : REAL; (* Iodine-135 Decay Constant lambda_I [1/s], 2.87E-5 s^-1 (6.57 h) *)
    rXenonDecayConstant_1s          : REAL; (* Xenon-135 Decay Constant lambda_Xe [1/s], 2.09E-5 s^-1 (9.14 h) *)
    rIodineFissionYield             : REAL; (* Iodine-135 Direct Fission Yield gamma_I = 0.061 *)
    rXenonFissionYield              : REAL; (* Xenon-135 Direct Fission Yield gamma_Xe = 0.003 *)
    rXenonAbsorptionCrossSection    : REAL; (* Xenon-135 Microscopic Thermal Absorption Cross Section sigma_Xe [cm^2] *)

    (* Pressurizer Non-Equilibrium 2-Region Mass & Energy Balances *)
    rPrzVaporVolume_m3              : REAL; (* Pressurizer Steam Dome Volume V_v [m3] *)
    rPrzLiquidVolume_m3             : REAL; (* Pressurizer Liquid Water Volume V_l [m3] *)
    rPrzTotalVolume_m3              : REAL; (* Pressurizer Total Internal Pressure Vessel Volume V_total [m3] *)
    rPrzVaporDensity_kgm3           : REAL; (* Saturated Steam Density rho_v at P_prz [kg/m3] *)
    rPrzLiquidDensity_kgm3          : REAL; (* Saturated Liquid Water Density rho_l at P_prz [kg/m3] *)
    rPrzVaporEnthalpy_kJkg          : REAL; (* Saturated Steam Specific Enthalpy h_v [kJ/kg] *)
    rPrzLiquidEnthalpy_kJkg         : REAL; (* Saturated Liquid Specific Enthalpy h_l [kJ/kg] *)
    rPrzSubcooledSprayEnthalpy_kJkg : REAL; (* Subcooled Liquid Spray Specific Enthalpy h_spray [kJ/kg] *)
    rPrzFlashingRate_kgs            : REAL; (* Spontaneous Flashing Mass Transfer Rate w_flash [kg/s] *)
    rPrzCondensationRate_kgs        : REAL; (* Steam Condensation Mass Transfer Rate w_cond [kg/s] *)
    rPrzSurgeFlowRate_kgs           : REAL; (* Primary Loop Swelling/Shrinkage Surge Flow w_surge [kg/s] *)
    rPrzSprayFlowRate_kgs           : REAL; (* Continuous Regulated Subcooled Spray Mass Flow Rate [kg/s] *)

    (* Fourier Core Heat Conduction & Natural Circulation Dynamics *)
    rFuelThermalCapacity_JdegC      : REAL; (* Fuel Pellet Bulk Lumped Thermal Heat Capacity [J/deg C] *)
    rCladThermalCapacity_JdegC      : REAL; (* Fuel Cladding Zircaloy Lumped Heat Capacity [J/deg C] *)
    rCoolantThermalCapacity_JdegC   : REAL; (* Primary Coolant Core Region Lumped Heat Capacity [J/deg C] *)
    rConductanceFuelToClad_WdegC    : REAL; (* Radial Heat Conductance Fuel Pellet to Cladding Gap U_fc [W/deg C] *)
    rConductanceCladToCoolant_WdegC : REAL; (* Convective Surface Heat Transfer Clad to Bulk Coolant U_cw [W/deg C] *)
    rPrimaryLoopTotalInertia        : REAL; (* Hydraulic Fluid Inertia of Primary Circulation Loop [m^-1] *)
    rPrimaryLoopDarcyFriction       : REAL; (* Total Form and Friction Pressure Drop Factor K_fric [kPa / (kg/s)^2] *)
    rCoreElevationCenter_m          : REAL; (* Vertical Elevation Distance Core Thermal Center to Steam Generator [m] *)
    rGravityAcceleration_ms2        : REAL; (* Standard Acceleration of Gravity g [m/s^2] = 9.80665 *)

    (* =================================================================================================================
     * SECTION 8: 2oo3 TMR VOTING VARIABLES & SENSOR DISCREPANCY TIMERS
     * ================================================================================================================= *)
    (* Discrepancy accumulation timers for 10 redundant channel groups [s] *)
    tTimer_PT101_AB                 : REAL; (* Pressurizer Pressure Ch A vs B Discrepancy Timer [s] *)
    tTimer_PT101_BC                 : REAL; (* Pressurizer Pressure Ch B vs C Discrepancy Timer [s] *)
    tTimer_PT101_CA                 : REAL; (* Pressurizer Pressure Ch C vs A Discrepancy Timer [s] *)
    bFault_PT101_ChA                : BOOL; (* PT-101 Channel A Latched Sensor Degradation Fault *)
    bFault_PT101_ChB                : BOOL; (* PT-101 Channel B Latched Sensor Degradation Fault *)
    bFault_PT101_ChC                : BOOL; (* PT-101 Channel C Latched Sensor Degradation Fault *)

    tTimer_LT102_AB                 : REAL; (* Pressurizer Level Ch A vs B Discrepancy Timer [s] *)
    tTimer_LT102_BC                 : REAL; (* Pressurizer Level Ch B vs C Discrepancy Timer [s] *)
    tTimer_LT102_CA                 : REAL; (* Pressurizer Level Ch C vs A Discrepancy Timer [s] *)
    bFault_LT102_ChA                : BOOL; (* LT-102 Channel A Latched Sensor Degradation Fault *)
    bFault_LT102_ChB                : BOOL; (* LT-102 Channel B Latched Sensor Degradation Fault *)
    bFault_LT102_ChC                : BOOL; (* LT-102 Channel C Latched Sensor Degradation Fault *)

    tTimer_TT201_AB                 : REAL; (* Hot Leg Temp Ch A vs B Discrepancy Timer [s] *)
    tTimer_TT201_BC                 : REAL; (* Hot Leg Temp Ch B vs C Discrepancy Timer [s] *)
    tTimer_TT201_CA                 : REAL; (* Hot Leg Temp Ch C vs A Discrepancy Timer [s] *)
    bFault_TT201_ChA                : BOOL; (* TT-201 Channel A Latched Sensor Degradation Fault *)
    bFault_TT201_ChB                : BOOL; (* TT-201 Channel B Latched Sensor Degradation Fault *)
    bFault_TT201_ChC                : BOOL; (* TT-201 Channel C Latched Sensor Degradation Fault *)

    tTimer_TT202_AB                 : REAL; (* Cold Leg Temp Ch A vs B Discrepancy Timer [s] *)
    tTimer_TT202_BC                 : REAL; (* Cold Leg Temp Ch B vs C Discrepancy Timer [s] *)
    tTimer_TT202_CA                 : REAL; (* Cold Leg Temp Ch C vs A Discrepancy Timer [s] *)
    bFault_TT202_ChA                : BOOL; (* TT-202 Channel A Latched Sensor Degradation Fault *)
    bFault_TT202_ChB                : BOOL; (* TT-202 Channel B Latched Sensor Degradation Fault *)
    bFault_TT202_ChC                : BOOL; (* TT-202 Channel C Latched Sensor Degradation Fault *)

    tTimer_NIT301_AB                : REAL; (* Power Range Flux Ch A vs B Discrepancy Timer [s] *)
    tTimer_NIT301_BC                : REAL; (* Power Range Flux Ch B vs C Discrepancy Timer [s] *)
    tTimer_NIT301_CA                : REAL; (* Power Range Flux Ch C vs A Discrepancy Timer [s] *)
    bFault_NIT301_ChA               : BOOL; (* NIT-301 Channel A Latched Sensor Degradation Fault *)
    bFault_NIT301_ChB               : BOOL; (* NIT-301 Channel B Latched Sensor Degradation Fault *)
    bFault_NIT301_ChC               : BOOL; (* NIT-301 Channel C Latched Sensor Degradation Fault *)

    tTimer_NIT302_AB                : REAL; (* Intermediate Range Flux Ch A vs B Discrepancy Timer [s] *)
    tTimer_NIT302_BC                : REAL; (* Intermediate Range Flux Ch B vs C Discrepancy Timer [s] *)
    tTimer_NIT302_CA                : REAL; (* Intermediate Range Flux Ch C vs A Discrepancy Timer [s] *)
    bFault_NIT302_ChA               : BOOL; (* NIT-302 Channel A Latched Sensor Degradation Fault *)
    bFault_NIT302_ChB               : BOOL; (* NIT-302 Channel B Latched Sensor Degradation Fault *)
    bFault_NIT302_ChC               : BOOL; (* NIT-302 Channel C Latched Sensor Degradation Fault *)

    tTimer_ZT401_AB                 : REAL; (* CRDM Position Ch A vs B Discrepancy Timer [s] *)
    tTimer_ZT401_BC                 : REAL; (* CRDM Position Ch B vs C Discrepancy Timer [s] *)
    tTimer_ZT401_CA                 : REAL; (* CRDM Position Ch C vs A Discrepancy Timer [s] *)
    bFault_ZT401_ChA                : BOOL; (* ZT-401 Channel A Latched Sensor Degradation Fault *)
    bFault_ZT401_ChB                : BOOL; (* ZT-401 Channel B Latched Sensor Degradation Fault *)
    bFault_ZT401_ChC                : BOOL; (* ZT-401 Channel C Latched Sensor Degradation Fault *)

    tTimer_FT501_AB                 : REAL; (* Primary Flow Ch A vs B Discrepancy Timer [s] *)
    tTimer_FT501_BC                 : REAL; (* Primary Flow Ch B vs C Discrepancy Timer [s] *)
    tTimer_FT501_CA                 : REAL; (* Primary Flow Ch C vs A Discrepancy Timer [s] *)
    bFault_FT501_ChA                : BOOL; (* FT-501 Channel A Latched Sensor Degradation Fault *)
    bFault_FT501_ChB                : BOOL; (* FT-501 Channel B Latched Sensor Degradation Fault *)
    bFault_FT501_ChC                : BOOL; (* FT-501 Channel C Latched Sensor Degradation Fault *)

    tTimer_PT601_AB                 : REAL; (* PRHRS Steam Pressure Ch A vs B Discrepancy Timer [s] *)
    tTimer_PT601_BC                 : REAL; (* PRHRS Steam Pressure Ch B vs C Discrepancy Timer [s] *)
    tTimer_PT601_CA                 : REAL; (* PRHRS Steam Pressure Ch C vs A Discrepancy Timer [s] *)
    bFault_PT601_ChA                : BOOL; (* PT-601 Channel A Latched Sensor Degradation Fault *)
    bFault_PT601_ChB                : BOOL; (* PT-601 Channel B Latched Sensor Degradation Fault *)
    bFault_PT601_ChC                : BOOL; (* PT-601 Channel C Latched Sensor Degradation Fault *)

    tTimer_TT701_AB                 : REAL; (* Cladding Peak Temp Ch A vs B Discrepancy Timer [s] *)
    tTimer_TT701_BC                 : REAL; (* Cladding Peak Temp Ch B vs C Discrepancy Timer [s] *)
    tTimer_TT701_CA                 : REAL; (* Cladding Peak Temp Ch C vs A Discrepancy Timer [s] *)
    bFault_TT701_ChA                : BOOL; (* TT-701 Channel A Latched Sensor Degradation Fault *)
    bFault_TT701_ChB                : BOOL; (* TT-701 Channel B Latched Sensor Degradation Fault *)
    bFault_TT701_ChC                : BOOL; (* TT-701 Channel C Latched Sensor Degradation Fault *)

    (* Threshold tolerances for 2oo3 discrepancy verification *)
    cTol_PT101_bar                  : REAL := 0.80;  (* Pressurizer Pressure Maximum Allowable Discrepancy [bar] *)
    cTol_LT102_pct                  : REAL := 2.50;  (* Pressurizer Level Maximum Allowable Discrepancy [%] *)
    cTol_TT201_degC                 : REAL := 1.50;  (* Hot Leg Temp Maximum Allowable Discrepancy [deg C] *)
    cTol_TT202_degC                 : REAL := 1.50;  (* Cold Leg Temp Maximum Allowable Discrepancy [deg C] *)
    cTol_NIT301_pct                 : REAL := 1.20;  (* Power Range Flux Discrepancy Trip Threshold [% RTP] *)
    cTol_NIT302_pct                 : REAL := 3.00;  (* Intermediate Range Flux Discrepancy Threshold [% RTP] *)
    cTol_ZT401_mm                   : REAL := 5.00;  (* CRDM Position Discrepancy Threshold [mm] *)
    cTol_FT501_m3h                  : REAL := 180.0; (* Primary Flow Discrepancy Threshold [m3/h] *)
    cTol_PT601_bar                  : REAL := 1.20;  (* PRHRS Steam Pressure Discrepancy Threshold [bar] *)
    cTol_TT701_degC                 : REAL := 12.0;  (* Cladding Peak Temp Discrepancy Threshold [deg C] *)
    cDiscrepancyDebounce_s          : REAL := 0.100; (* Discrepancy Debounce Time Window [s] (100 ms) *)

    (* =================================================================================================================
     * SECTION 9: ISA-18.2 ALARM TRIP POINTS, DEADBANDS & INTERLOCK TIMERS
     * ================================================================================================================= *)
    (* Pressurizer Pressure Protection Limits *)
    cTrip_PPrz_HI_HI_bar            : REAL := 162.0; (* Immediate Class 1E Reactor SCRAM High-High Pressure [bar] *)
    cTrip_PPrz_HI_bar               : REAL := 158.0; (* Warning High Pressure Alarm / Continuous Spray Max [bar] *)
    cTrip_PPrz_LO_bar               : REAL := 151.0; (* Warning Low Pressure Alarm / Backup Heaters On [bar] *)
    cTrip_PPrz_LO_LO_bar            : REAL := 142.0; (* Safety Injection Actuation & SCRAM Low-Low Pressure [bar] *)
    cDeadband_PPrz_bar              : REAL := 0.25;  (* Pressurizer Pressure Alarm Reset Deadband [bar] *)

    (* Power Range Neutron Flux Limits *)
    cTrip_Flux_HI_HI_pct            : REAL := 108.0; (* High-High Neutron Flux Class 1E SCRAM Trip [% RTP] *)
    cTrip_Flux_HI_pct               : REAL := 103.0; (* High Flux Warning Alarm / Inhibit Rod Withdrawal [% RTP] *)
    cTrip_Flux_ROC_pct_s            : REAL := 5.0;   (* Rate of Change Positive Flux Surge Trip [% RTP / s] *)
    cTrip_Period_Min_s              : REAL := 15.0;  (* Minimum Allowable Reactor Period Before Emergency SCRAM [s] *)
    cDeadband_Flux_pct              : REAL := 0.50;  (* Power Range Flux Deadband [% RTP] *)

    (* Primary Coolant Flow & Cladding Thermal Limits *)
    cTrip_Flow_LO_LO_pct            : REAL := 80.0;  (* Immediate SCRAM on Primary Coolant Loss of Flow [%] *)
    cTrip_Flow_LO_pct               : REAL := 88.0;  (* Low Primary Coolant Flow Warning [%] *)
    cTrip_Clad_HI_HI_degC           : REAL := 650.0; (* Immediate Emergency SCRAM Peak Cladding Temperature [deg C] *)
    cTrip_Clad_HI_degC              : REAL := 450.0; (* Peak Cladding Temperature Operational Warning [deg C] *)
    cTrip_HotLeg_HI_HI_degC         : REAL := 338.0; (* Core Exit Hot Leg Temperature SCRAM Trip [deg C] *)

    (* Pressurizer Level Operational Limits *)
    cTrip_LPrz_HI_HI_pct            : REAL := 85.0;  (* High-High Solid Pressurizer Prevention Trip [%] *)
    cTrip_LPrz_LO_LO_pct            : REAL := 20.0;  (* Low-Low Uncovered Immersion Heaters Interlock Trip [%] *)

    (* Real-Time Computed Alarm Flags *)
    bAlarm_PPrz_HI_HI               : BOOL; (* Pressurizer High-High Saturated Pressure Trip *)
    bAlarm_PPrz_HI                  : BOOL; (* Pressurizer High Pressure Warning *)
    bAlarm_PPrz_LO                  : BOOL; (* Pressurizer Low Pressure Warning *)
    bAlarm_PPrz_LO_LO               : BOOL; (* Pressurizer Low-Low Safety Injection & SCRAM Trip *)
    bAlarm_Flux_HI_HI               : BOOL; (* Neutron Flux High-High Protective Trip *)
    bAlarm_Flux_HI                  : BOOL; (* Neutron Flux High Warning *)
    bAlarm_Flux_ROC                 : BOOL; (* Neutron Flux Surge Rate of Change Trip *)
    bAlarm_Period_Short             : BOOL; (* Prompt Criticality Reactor Period Low Trip (< 15 s) *)
    bAlarm_Flow_LO_LO               : BOOL; (* Primary Coolant Loss of Flow Trip *)
    bAlarm_Flow_LO                  : BOOL; (* Primary Coolant Flow Low Warning *)
    bAlarm_Clad_HI_HI               : BOOL; (* Peak Cladding Temperature Emergency Trip *)
    bAlarm_HotLeg_HI_HI             : BOOL; (* Hot Leg Temperature Safety Trip *)
    bAlarm_LPrz_HI_HI               : BOOL; (* Pressurizer Level High-High Trip *)
    bAlarm_LPrz_LO_LO               : BOOL; (* Pressurizer Level Low-Low Interlock Trip *)
    bAlarm_AxialOffset_Dev          : BOOL; (* Core Axial Flux Offset Imbalance Warning *)
    bAlarm_2oo3_DegradedChannel     : BOOL; (* 2oo3 Sensor Voting Redundancy Degraded Warning *)

    (* =================================================================================================================
     * SECTION 10: FSM STATE TIMERS, STEP SEQUENCE CONTROL & INTERNAL SCRATCHPAD
     * ================================================================================================================= *)
    bModelInitialized               : BOOL := FALSE; (* First-Scan Initialization Latch Flag *)
    tStateTimer_s                   : REAL := 0.0;   (* Active FSM State Dwell Timer [s] *)
    rScramElapsedTimer_s            : REAL := 0.0;   (* Time Elapsed Since Fast Gravity SCRAM Initiated [s] *)
    nFSMPreviousState               : INT := 1;      (* Previous Scan Operational State Register *)
    rFluxPreviousScan_pct           : REAL := 0.0;   (* Prior Cycle Ex-Core Flux for Rate of Change Derivative *)
    rPressPreviousScan_bar          : REAL := 155.0; (* Prior Cycle Pressurizer Pressure for Rate of Change Derivative *)
    rCRDM_StepAccumulator_mm        : REAL := 0.0;   (* Internal High-Resolution Control Rod Position Integrator [mm] *)
    rPressurizerIntegralErr         : REAL := 0.0;   (* Immersion Heater PI Controller Anti-Windup Error Integrator *)
    rPressurizerDerivativeErr       : REAL := 0.0;   (* Immersion Heater Derivative Filter Register *)

    (* Loop index counters *)
    iIdx                            : INT; (* General Purpose Loop Index i *)
    jIdx                            : INT; (* General Purpose Loop Index j *)
    kIdx                            : INT; (* General Purpose Loop Index k *)
    mIdx                            : INT; (* General Purpose Loop Index m *)
    pIdx                            : INT; (* MPC Horizon Loop Index p *)

    (* Temporary math registers *)
    rSum                            : REAL;
    rDeltaU                         : REAL;
    rPredictedError                 : REAL;
    rStepCost                       : REAL;
    rCurrentCandidateCost           : REAL;
    rTestU1                         : REAL;
    rTestU2                         : REAL;
    rTestU3                         : REAL;
    rTestU4                         : REAL;
    aSimX                           : ARRAY[1..8] OF REAL;
    aSimXNext                       : ARRAY[1..8] OF REAL;
END_VAR
""")

    # PHASE 0: MODEL MATRICES & CONTROL COEFFICIENT INITIALIZATION
    code_parts.append("""(* =====================================================================================================================
 * PHASE 0: MODEL MATRICES & CONTROL COEFFICIENT INITIALIZATION (FIRST SCAN DETERMINISTIC SETUP)
 * ===================================================================================================================== *)
IF NOT bModelInitialized THEN
    (* Discretized Point Reactor Kinetics Delayed Neutron Constants (6-group parameters for U-235 thermal fission) *)
    aPrecursorLambda[1] := 0.0124;  aPrecursorBeta[1] := 0.000215; (* Group 1: T_half = 55.72 s *)
    aPrecursorLambda[2] := 0.0305;  aPrecursorBeta[2] := 0.001424; (* Group 2: T_half = 22.72 s *)
    aPrecursorLambda[3] := 0.1110;  aPrecursorBeta[3] := 0.001274; (* Group 3: T_half = 6.22 s *)
    aPrecursorLambda[4] := 0.3010;  aPrecursorBeta[4] := 0.002568; (* Group 4: T_half = 2.30 s *)
    aPrecursorLambda[5] := 1.1400;  aPrecursorBeta[5] := 0.000748; (* Group 5: T_half = 0.61 s *)
    aPrecursorLambda[6] := 3.0100;  aPrecursorBeta[6] := 0.000271; (* Group 6: T_half = 0.23 s *)

    rPromptGenerationTime_s         := 0.000025; (* Lambda = 25.0 microseconds *)
    rTotalDelayedFractionBeta       := 0.006500; (* Total Delayed Neutron Fraction Beta = 650.0 pcm *)
    rDopplerReactivityCoeff_pcm     := -2.85;    (* Negative Doppler Fuel Temperature Coefficient [pcm/deg C] *)
    rModeratorDensityCoeff_pcm      := -35.20;   (* Negative Moderator Temperature/Density Coefficient [pcm/deg C] *)
    rCRDM_DifferentialWorth_pcm_mm  := 1.25;     (* Differential Control Rod Bank Worth [pcm/mm] *)
    rBoronReactivityCoeff_pcm_ppm   := -8.60;    (* Soluble Boron Worth [pcm/ppm] *)
    rSolubleBoronConcentration_ppm  := 950.0;    (* Initial Critical Boron Concentration [ppm] *)

    (* Xenon-135 and Iodine-135 Microscopic Constants *)
    rIodineDecayConstant_1s         := 0.0000287; (* lambda_I = 2.87E-5 s^-1 *)
    rXenonDecayConstant_1s          := 0.0000209; (* lambda_Xe = 2.09E-5 s^-1 *)
    rIodineFissionYield             := 0.0610;    (* gamma_I = 6.1% *)
    rXenonFissionYield              := 0.0030;    (* gamma_Xe = 0.3% direct yield *)
    rXenonAbsorptionCrossSection    := 2.65E-18;  (* sigma_Xe = 2.65E-18 cm^2 (2.65 million barns) *)
    rIodineConcentration            := 1.0;       (* Normalized Equilibrium Inventory *)
    rXenonConcentration             := 1.0;       (* Normalized Equilibrium Inventory *)

    (* Core Geometry & Lumped Thermal-Hydraulic Capacities for 300 MWe SMR *)
    rFuelThermalCapacity_JdegC      := 1.85E+7;  (* Fuel Pellets Total Heat Capacity [J/deg C] *)
    rCladThermalCapacity_JdegC      := 4.20E+6;  (* Zircaloy Cladding Total Heat Capacity [J/deg C] *)
    rCoolantThermalCapacity_JdegC   := 2.95E+7;  (* Core Bulk Coolant Total Heat Capacity [J/deg C] *)
    rConductanceFuelToClad_WdegC    := 3.65E+6;  (* Gap Conductance U_fc [W/deg C] *)
    rConductanceCladToCoolant_WdegC := 9.80E+6;  (* Convective Surface Film Conductance U_cw [W/deg C] *)
    rPrimaryLoopTotalInertia        := 48.5;     (* Loop Hydraulic Fluid Inertia (Sum L_i / A_i) [m^-1] *)
    rPrimaryLoopDarcyFriction       := 0.00142;  (* Flow Resistance Coefficient K_fric [kPa / (kg/s)^2] *)
    rCoreElevationCenter_m          := 6.80;     (* Thermal Center Height Difference Core-to-SG [m] *)
    rGravityAcceleration_ms2        := 9.80665;  (* Standard Gravity [m/s^2] *)

    (* In-Vessel Pressurizer Upper Dome Non-Equilibrium 2-Region Geometry *)
    rPrzTotalVolume_m3              := 18.50;    (* Total Pressurizer Volume [m3] *)
    rPrzLiquidVolume_m3             := 10.175;   (* Liquid Volume at 55% Level [m3] *)
    rPrzVaporVolume_m3              := 8.325;    (* Vapor Volume at 45% Steam Space [m3] *)
    rPrzVaporDensity_kgm3           := 101.5;    (* Dry Saturated Steam Density at 155 bar [kg/m3] *)
    rPrzLiquidDensity_kgm3          := 594.2;    (* Saturated Water Density at 155 bar (344.8 deg C) [kg/m3] *)
    rPrzVaporEnthalpy_kJkg          := 2595.0;   (* Saturated Steam Enthalpy [kJ/kg] *)
    rPrzLiquidEnthalpy_kJkg         := 1632.0;   (* Saturated Liquid Enthalpy [kJ/kg] *)
    rPrzSubcooledSprayEnthalpy_kJkg := 1315.0;   (* Cold Leg Spray Enthalpy (292 deg C) [kJ/kg] *)
    rPrzFlashingRate_kgs            := 0.0;
    rPrzCondensationRate_kgs        := 0.0;
    rPrzSurgeFlowRate_kgs           := 0.0;
    rPrzSprayFlowRate_kgs           := 0.0;

    (* -----------------------------------------------------------------------------------------------------------------
     * Discrete State-Space System Matrices (A, B, C, D) Formulated at Ts = 0.005 s (5 ms Cyclic Rate)
     * States: [x1: n/n0, x2: C/C0, x3: Tf, x4: Tc, x5: Tcore, x6: Pprz, x7: Lprz, x8: Delta-I]
     * Inputs: [u1: dRho/dt, u2: Q_heaters, u3: Y_spray, u4: N_rcp]
     * ----------------------------------------------------------------------------------------------------------------- *)
    (* Initialize Matrix A (8x8) to Identity + Ts * A_continuous *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 8 DO
            aStateA[iIdx, jIdx] := 0.0;
            aStateC[iIdx, jIdx] := 0.0;
            aMPC_Q[iIdx, jIdx]  := 0.0;
            aMPC_P_Terminal[iIdx, jIdx] := 0.0;
            aKalmanGainL[iIdx, jIdx] := 0.0;
        END_FOR;
        aStateA[iIdx, iIdx] := 1.0;
        aStateC[iIdx, iIdx] := 1.0; (* Full State Observation Structure *)
    END_FOR;

    (* Coupled Physical Dynamics Discretization into A Matrix *)
    aStateA[1, 1] := 0.99852;  aStateA[1, 2] := 0.00145;  aStateA[1, 3] := -0.00038; aStateA[1, 5] := -0.00062;
    aStateA[2, 1] := 0.00210;  aStateA[2, 2] := 0.99785;
    aStateA[3, 1] := 0.00425;  aStateA[3, 3] := 0.99320;  aStateA[3, 4] := 0.00670;
    aStateA[4, 3] := 0.01250;  aStateA[4, 4] := 0.97450;  aStateA[4, 5] := 0.01280;
    aStateA[5, 4] := 0.00840;  aStateA[5, 5] := 0.98820;  aStateA[5, 6] := 0.00015;
    aStateA[6, 5] := 0.00350;  aStateA[6, 6] := 0.99880;  aStateA[6, 7] := 0.00120;
    aStateA[7, 5] := 0.00180;  aStateA[7, 6] := -0.00045; aStateA[7, 7] := 0.99920;
    aStateA[8, 1] := 0.00150;  aStateA[8, 3] := -0.00085; aStateA[8, 8] := 0.99650;

    (* Initialize Control Coupling Matrix B (8x4) *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 4 DO
            aStateB[iIdx, jIdx] := 0.0;
            aStateD[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* B Matrix Actuator Gains: Col 1: CRDM [pcm/s], Col 2: Heaters [kW], Col 3: Spray [%], Col 4: Pumps [RPM] *)
    aStateB[1, 1] := 0.000240; aStateB[1, 4] := 0.000012;
    aStateB[3, 1] := 0.000085;
    aStateB[5, 4] := 0.000045;
    aStateB[6, 2] := 0.000038; aStateB[6, 3] := -0.000185; aStateB[6, 4] := 0.000008;
    aStateB[7, 2] := 0.000012; aStateB[7, 3] := 0.000095;  aStateB[7, 4] := 0.000022;
    aStateB[8, 1] := -0.000420;

    (* Kalman Observer Gain Matrix L (8x8 Diagonal Dominant Structure) *)
    aKalmanGainL[1, 1] := 0.125; aKalmanGainL[2, 2] := 0.085;
    aKalmanGainL[3, 3] := 0.095; aKalmanGainL[4, 4] := 0.095;
    aKalmanGainL[5, 5] := 0.110; aKalmanGainL[6, 6] := 0.145;
    aKalmanGainL[7, 7] := 0.130; aKalmanGainL[8, 8] := 0.105;

    (* Model Predictive Control (MPC) Cost Weight Matrices *)
    aMPC_Q[1, 1] := 100.0; (* Thermal Power Tracking Penalty *)
    aMPC_Q[2, 2] := 10.0;  (* Delayed Precursor Fluctuation Penalty *)
    aMPC_Q[3, 3] := 5.0;   (* Fuel Pellet Temperature Stability *)
    aMPC_Q[4, 4] := 5.0;   (* Cladding Temperature Stability *)
    aMPC_Q[5, 5] := 25.0;  (* Primary Coolant Core Temperature Penalty *)
    aMPC_Q[6, 6] := 250.0; (* In-Vessel Pressurizer Pressure High-Precision Holding (155.0 bar +/- 0.2 bar) *)
    aMPC_Q[7, 7] := 50.0;  (* Pressurizer Level Holding Penalty *)
    aMPC_Q[8, 8] := 85.0;  (* Core Axial Offset Flux Imbalance Penalty *)

    (* Terminal State Cost Matrix P (Lyapunov Equation Solution Approximation) *)
    FOR iIdx := 1 TO 8 DO
        aMPC_P_Terminal[iIdx, iIdx] := aMPC_Q[iIdx, iIdx] * 3.5;
    END_FOR;

    (* Actuator Absolute Effort Penalties R (4x4) *)
    FOR iIdx := 1 TO 4 DO
        FOR jIdx := 1 TO 4 DO
            aMPC_R[iIdx, jIdx] := 0.0;
            aMPC_S[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;
    aMPC_R[1, 1] := 25.0; (* CRDM Stepping Wear Suppression *)
    aMPC_R[2, 2] := 1.5;  (* Immersion Heater Electrical Cost *)
    aMPC_R[3, 3] := 3.5;  (* Subcooled Spray Valve Wear Penalty *)
    aMPC_R[4, 4] := 8.0;  (* Primary Canned Pump VFD Effort *)

    (* Actuator Slew Rate Penalties S (4x4) *)
    aMPC_S[1, 1] := 50.0; (* CRDM Stepping Velocity Jerk Limiting *)
    aMPC_S[2, 2] := 5.0;  (* Immersion Heater Thermal Stress Limiting *)
    aMPC_S[3, 3] := 10.0; (* Spray Valve Mechanical Stroke Jerk Limiting *)
    aMPC_S[4, 4] := 20.0; (* Primary Canned Pump Speed Ramp Limiting *)

    (* Candidate search vectors for MPC receding-horizon quadratic optimization *)
    aCandidateD1[1] := -25.0; aCandidateD1[2] := -10.0; aCandidateD1[3] := 0.0; aCandidateD1[4] := 10.0; aCandidateD1[5] := 25.0;
    aCandidateD2[1] := -150.0; aCandidateD2[2] := -50.0; aCandidateD2[3] := 0.0; aCandidateD2[4] := 50.0; aCandidateD2[5] := 150.0;
    aCandidateD3[1] := -15.0; aCandidateD3[2] := -5.0;  aCandidateD3[3] := 0.0; aCandidateD3[4] := 5.0;  aCandidateD3[5] := 15.0;
    aCandidateD4[1] := -20.0; aCandidateD4[2] := -5.0;  aCandidateD4[3] := 0.0; aCandidateD4[4] := 5.0;  aCandidateD4[5] := 20.0;

    (* Precursor Initial Densities at 100% RTP Equilibrium *)
    FOR iIdx := 1 TO 6 DO
        aPrecursorConcentration[iIdx] := aPrecursorBeta[iIdx] / (aPrecursorLambda[iIdx] * rPromptGenerationTime_s);
    END_FOR;

    (* Initialize State Vectors to 100% Equilibrium *)
    aStateVector[1] := 1.0;   (* 100% RTP *)
    aStateVector[2] := 1.0;
    aStateVector[3] := 680.0; (* Fuel Pellet Average Temp [deg C] *)
    aStateVector[4] := 365.0; (* Fuel Cladding Temp [deg C] *)
    aStateVector[5] := 308.0; (* Core Coolant Average Temp [deg C] *)
    aStateVector[6] := 155.0; (* Pressurizer Pressure [bar] *)
    aStateVector[7] := 55.0;  (* Pressurizer Level [%] *)
    aStateVector[8] := 0.0;   (* Axial Offset [%] *)

    FOR iIdx := 1 TO 8 DO
        aStateEstimated[iIdx]  := aStateVector[iIdx];
        aStateReference[iIdx]  := aStateVector[iIdx];
    END_FOR;

    aControlVector[1] := 0.0;     (* CRDM Stepping Rate = 0 steps/min *)
    aControlVector[2] := 250.0;   (* Proportional Heaters Steady Baseline = 250 kW *)
    aControlVector[3] := 10.0;    (* Subcooled Continuous Spray Baseline = 10% Opening *)
    aControlVector[4] := 1485.0;  (* Primary Canned Motor Pump Nominal Speed = 1485 RPM *)

    FOR jIdx := 1 TO 4 DO
        aControlVectorPrev[jIdx]  := aControlVector[jIdx];
        aDeltaControlVector[jIdx] := 0.0;
    END_FOR;

    bModelInitialized := TRUE;
END_IF;
""")

    # PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY SENSOR VOTING ENGINES
    # Let's generate complete pairwise logic for all 10 transmitter groups!
    phase1_code = ["""(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES
 * High-Integrity Pairwise Deviation Verification with Anti-Chatter Discrepancy Timers
 * ===================================================================================================================== *)
"""]

    # List of 10 groups:
    # 1: PT_PRESSURIZER_101 (cTol_PT101_bar, rVoted_PressurizerPressure_bar, tTimer_PT101_*, bFault_PT101_*)
    # 2: LT_PRESSURIZER_LEVEL_102 (cTol_LT102_pct, rVoted_PressurizerLevel_pct, tTimer_LT102_*, bFault_LT102_*)
    # 3: TT_HOT_LEG_TEMP_201 (cTol_TT201_degC, rVoted_HotLegTemp_degC, tTimer_TT201_*, bFault_TT201_*)
    # 4: TT_COLD_LEG_TEMP_202 (cTol_TT202_degC, rVoted_ColdLegTemp_degC, tTimer_TT202_*, bFault_TT202_*)
    # 5: NIT_EXCORE_POWER_RANGE_301 (cTol_NIT301_pct, rVoted_PowerRangeFlux_pct, tTimer_NIT301_*, bFault_NIT301_*)
    # 6: NIT_INTERMEDIATE_RANGE_302 (cTol_NIT302_pct, rVoted_IntermediateFlux_pct, tTimer_NIT302_*, bFault_NIT302_*)
    # 7: ZT_CRDM_STEP_POS_401 (cTol_ZT401_mm, rVoted_CRDM_Position_mm, tTimer_ZT401_*, bFault_ZT401_*)
    # 8: FT_PRIMARY_COOLANT_501 (cTol_FT501_m3h, rVoted_PrimaryFlow_m3h, tTimer_FT501_*, bFault_FT501_*)
    # 9: PT_PRHRS_STEAM_601 (cTol_PT601_bar, rVoted_PRHRS_SteamPress_bar, tTimer_PT601_*, bFault_PT601_*)
    # 10: TT_CLADDING_PEAK_701 (cTol_TT701_degC, rVoted_CladdingPeakTemp_degC, tTimer_TT701_*, bFault_TT701_*)

    tmr_groups = [
        ("PT_PRESSURIZER_101", "cTol_PT101_bar", "rVoted_PressurizerPressure_bar", "tTimer_PT101", "bFault_PT101", "Pressurizer Pressure [bar]"),
        ("LT_PRESSURIZER_LEVEL_102", "cTol_LT102_pct", "rVoted_PressurizerLevel_pct", "tTimer_LT102", "bFault_LT102", "Pressurizer Liquid Level [%]"),
        ("TT_HOT_LEG_TEMP_201", "cTol_TT201_degC", "rVoted_HotLegTemp_degC", "tTimer_TT201", "bFault_TT201", "Hot Leg Coolant Temperature [deg C]"),
        ("TT_COLD_LEG_TEMP_202", "cTol_TT202_degC", "rVoted_ColdLegTemp_degC", "tTimer_TT202", "bFault_TT202", "Cold Leg Coolant Temperature [deg C]"),
        ("NIT_EXCORE_POWER_RANGE_301", "cTol_NIT301_pct", "rVoted_PowerRangeFlux_pct", "tTimer_NIT301", "bFault_NIT301", "Ex-Core Power Range Neutron Flux [% RTP]"),
        ("NIT_INTERMEDIATE_RANGE_302", "cTol_NIT302_pct", "rVoted_IntermediateFlux_pct", "tTimer_NIT302", "bFault_NIT302", "Ex-Core Intermediate Range Flux [% RTP]"),
        ("ZT_CRDM_STEP_POS_401", "cTol_ZT401_mm", "rVoted_CRDM_Position_mm", "tTimer_ZT401", "bFault_ZT401", "CRDM Regulating Rod Bank Position [mm]"),
        ("FT_PRIMARY_COOLANT_501", "cTol_FT501_m3h", "rVoted_PrimaryFlow_m3h", "tTimer_FT501", "bFault_FT501", "Primary Coolant Total Volumetric Flow [m3/h]"),
        ("PT_PRHRS_STEAM_601", "cTol_PT601_bar", "rVoted_PRHRS_SteamPress_bar", "tTimer_PT601", "bFault_PT601", "PRHRS Heat Exchanger Steam Pressure [bar]"),
        ("TT_CLADDING_PEAK_701", "cTol_TT701_degC", "rVoted_CladdingPeakTemp_degC", "tTimer_TT701", "bFault_TT701", "Core Sub-Channel Fuel Cladding Peak Temp [deg C]"),
    ]

    for prefix, tol, voted_var, timer_pfx, fault_pfx, desc in tmr_groups:
        tagA = f"{prefix}A"
        tagB = f"{prefix}B"
        tagC = f"{prefix}C"
        tAB = f"{timer_pfx}_AB"
        tBC = f"{timer_pfx}_BC"
        tCA = f"{timer_pfx}_CA"
        fA = f"{fault_pfx}_ChA"
        fB = f"{fault_pfx}_ChB"
        fC = f"{fault_pfx}_ChC"

        phase1_code.append(f"""(* -----------------------------------------------------------------------------------------------------------------
 * 2oo3 TMR Voting Unit: {desc} ({prefix}A, B, C)
 * ----------------------------------------------------------------------------------------------------------------- *)
IF ABS({tagA} - {tagB}) > {tol} THEN
    {tAB} := {tAB} + rCycleTime_s;
ELSE
    IF {tAB} > 0.0 THEN {tAB} := {tAB} - (rCycleTime_s * 2.0); END_IF;
    IF {tAB} < 0.0 THEN {tAB} := 0.0; END_IF;
END_IF;

IF ABS({tagB} - {tagC}) > {tol} THEN
    {tBC} := {tBC} + rCycleTime_s;
ELSE
    IF {tBC} > 0.0 THEN {tBC} := {tBC} - (rCycleTime_s * 2.0); END_IF;
    IF {tBC} < 0.0 THEN {tBC} := 0.0; END_IF;
END_IF;

IF ABS({tagC} - {tagA}) > {tol} THEN
    {tCA} := {tCA} + rCycleTime_s;
ELSE
    IF {tCA} > 0.0 THEN {tCA} := {tCA} - (rCycleTime_s * 2.0); END_IF;
    IF {tCA} < 0.0 THEN {tCA} := 0.0; END_IF;
END_IF;

(* Evaluate channel fault latches based on discrepancy debounce limit *)
IF {tAB} >= cDiscrepancyDebounce_s AND {tCA} >= cDiscrepancyDebounce_s THEN
    {fA} := TRUE;
END_IF;
IF {tAB} >= cDiscrepancyDebounce_s AND {tBC} >= cDiscrepancyDebounce_s THEN
    {fB} := TRUE;
END_IF;
IF {tBC} >= cDiscrepancyDebounce_s AND {tCA} >= cDiscrepancyDebounce_s THEN
    {fC} := TRUE;
END_IF;

(* 2oo3 Median and Degraded 1oo2 Voting Resolution *)
IF NOT {fA} AND NOT {fB} AND NOT {fC} THEN
    (* All three channels valid: Classical Median Selection *)
    IF ({tagA} >= {tagB} AND {tagA} <= {tagC}) OR ({tagA} <= {tagB} AND {tagA} >= {tagC}) THEN
        {voted_var} := {tagA};
    ELSIF ({tagB} >= {tagA} AND {tagB} <= {tagC}) OR ({tagB} <= {tagA} AND {tagB} >= {tagC}) THEN
        {voted_var} := {tagB};
    ELSE
        {voted_var} := {tagC};
    END_IF;
ELSIF {fA} AND NOT {fB} AND NOT {fC} THEN
    (* Channel A Failed: Average of Healthy Channels B and C *)
    {voted_var} := ({tagB} + {tagC}) * 0.50;
ELSIF {fB} AND NOT {fA} AND NOT {fC} THEN
    (* Channel B Failed: Average of Healthy Channels A and C *)
    {voted_var} := ({tagA} + {tagC}) * 0.50;
ELSIF {fC} AND NOT {fA} AND NOT {fB} THEN
    (* Channel C Failed: Average of Healthy Channels A and B *)
    {voted_var} := ({tagA} + {tagB}) * 0.50;
ELSIF NOT {fA} AND {fB} AND {fC} THEN
    (* Dual Failure: Single Channel A Hold *)
    {voted_var} := {tagA};
ELSIF NOT {fB} AND {fA} AND {fC} THEN
    (* Dual Failure: Single Channel B Hold *)
    {voted_var} := {tagB};
ELSIF NOT {fC} AND {fA} AND {fB} THEN
    (* Dual Failure: Single Channel C Hold *)
    {voted_var} := {tagC};
ELSE
    (* Triple Failure: Hold previous voted value and latch degraded channel alarm *)
    bAlarm_2oo3_DegradedChannel := TRUE;
END_IF;
""")
    code_parts.append("\n".join(phase1_code))

    # PHASE 2: THERMAL-HYDRAULIC & CYBER-PHYSICAL REACTION ENGINES
    code_parts.append("""(* =====================================================================================================================
 * PHASE 2: THERMAL-HYDRAULIC & CYBER-PHYSICAL REACTION ENGINES
 * Point Reactor Kinetics, Xenon Poisoning, Two-Region Pressurizer Mass/Energy & Fourier Conduction
 * ===================================================================================================================== *)
(* 1. Delayed Neutron Precursor State Updates (6 Distinct Physical Groups) *)
FOR iIdx := 1 TO 6 DO
    (* dC_i / dt = (Beta_i / Lambda) * n - lambda_i * C_i *)
    aPrecursorConcentration[iIdx] := aPrecursorConcentration[iIdx] + rCycleTime_s * 
        ((aPrecursorBeta[iIdx] / rPromptGenerationTime_s) * rVoted_PowerRangeFlux_pct * 0.01 - 
         aPrecursorLambda[iIdx] * aPrecursorConcentration[iIdx]);
    IF aPrecursorConcentration[iIdx] < 0.0 THEN aPrecursorConcentration[iIdx] := 0.0; END_IF;
END_FOR;

(* Sum Precursor Delayed Source: S_d = Sum(lambda_i * C_i) *)
rSum := 0.0;
FOR iIdx := 1 TO 6 DO
    rSum := rSum + (aPrecursorLambda[iIdx] * aPrecursorConcentration[iIdx]);
END_FOR;

(* 2. Reactivity Feedback Balance Formulation (All terms converted to pcm) *)
(* Doppler Fuel Temperature Reactivity: rho_Dop = alpha_f * (T_fuel - T_fuel_ref) *)
rStepCost := rDopplerReactivityCoeff_pcm * (aStateEstimated[3] - 680.0);

(* Moderator Density/Temperature Reactivity: rho_Mod = alpha_m * (T_core - T_core_ref) *)
rPredictedError := rModeratorDensityCoeff_pcm * (aStateEstimated[5] - 308.0);

(* CRDM Bank Insertion Reactivity: rho_CRDM = (Z_pos - Z_ref) * (dRho/dz) *)
rDeltaU := (rVoted_CRDM_Position_mm - 1800.0) * rCRDM_DifferentialWorth_pcm_mm;

(* Xenon Poisoning Reactivity Worth: rho_Xe = -sigma_Xe * (Xe - Xe_ref) *)
rCurrentCandidateCost := -2850.0 * (rXenonConcentration - 1.0);

(* Total Reconstructed Core Net Reactivity [pcm] *)
rReactivity_pcm := rStepCost + rPredictedError + rDeltaU + rCurrentCandidateCost;

(* Prompt Point Kinetics Derivative: dn/dt = ((rho_net - Beta)/Lambda)*n + Sum(lambda_i * C_i) *)
rTestU1 := (((rReactivity_pcm * 1.0E-5) - rTotalDelayedFractionBeta) / rPromptGenerationTime_s) * 
           (rVoted_PowerRangeFlux_pct * 0.01) + rSum;

(* Dynamic Reactor Period Calculation (tau = n / (dn/dt)) *)
IF ABS(rTestU1) > 1.0E-7 THEN
    rReactorPeriod_s := (rVoted_PowerRangeFlux_pct * 0.01) / rTestU1;
ELSE
    rReactorPeriod_s := 999.0; (* Stable Infinite Period *)
END_IF;

(* 3. Xenon-135 and Iodine-135 Differential Transient Kinetics *)
(* dI/dt = gamma_I * Sigma_f * Phi - lambda_I * I *)
rIodineConcentration := rIodineConcentration + rCycleTime_s * 
    (rIodineFissionYield * (rVoted_PowerRangeFlux_pct * 0.01) - rIodineDecayConstant_1s * rIodineConcentration);

(* dXe/dt = gamma_Xe * Sigma_f * Phi + lambda_I * I - lambda_Xe * Xe - sigma_Xe * Phi * Xe *)
rXenonConcentration := rXenonConcentration + rCycleTime_s * 
    (rXenonFissionYield * (rVoted_PowerRangeFlux_pct * 0.01) + 
     rIodineDecayConstant_1s * rIodineConcentration - 
     rXenonDecayConstant_1s * rXenonConcentration - 
     0.000085 * (rVoted_PowerRangeFlux_pct * 0.01) * rXenonConcentration);

(* 4. Core Axial Flux Offset Imbalance Delta-I Calculation *)
rAxialOffset_pct := ((rVoted_HotLegTemp_degC - rVoted_ColdLegTemp_degC) - 34.0) * 1.25;

(* 5. Fuel Pellet Fourier Heat Conduction & Cladding Convection to Bulk Coolant *)
(* Centerline Fuel Pellet Temperature: T_center = T_fuel + q' / (4 * pi * k_fuel) *)
rFuelCenterlineTemp_degC := aStateEstimated[3] + ((rVoted_PowerRangeFlux_pct * 0.01) * 380.0);

(* Departure from Nucleate Boiling Ratio (DNBR) Critical Heat Flux (W-3 / Bowring correlation approximation) *)
rDepartureFromNucleateBoilingRatio := (1.85E+6 / (1.15E+6 * (rVoted_PowerRangeFlux_pct * 0.01 + 0.05))) * 
    (1.0 + 0.0035 * (155.0 - rVoted_PressurizerPressure_bar)) * 
    (rVoted_PrimaryFlow_m3h / 9800.0);
IF rDepartureFromNucleateBoilingRatio > 5.0 THEN rDepartureFromNucleateBoilingRatio := 5.0; END_IF;

(* 6. Primary Loop Natural Circulation Thermosiphon Buoyancy Driving Head *)
(* DeltaP_buoy = (rho_cold - rho_hot) * g * H_core_to_SG *)
rNaturalCirculationBuoyancy_kPa := ((745.0 - (rVoted_HotLegTemp_degC * 0.85)) - 
                                    (745.0 - (rVoted_ColdLegTemp_degC * 0.85))) * 
                                   (rGravityAcceleration_ms2 * rCoreElevationCenter_m) * 0.001;
IF rNaturalCirculationBuoyancy_kPa < 0.0 THEN rNaturalCirculationBuoyancy_kPa := 0.0; END_IF;

(* 7. In-Vessel Pressurizer Non-Equilibrium 2-Region Thermodynamics *)
(* Surge Flow Rate from Primary Loop Volumetric Expansion: w_surge = rho_w * dV/dt *)
rPrzSurgeFlowRate_kgs := ((rVoted_HotLegTemp_degC - aStateEstimated[5]) * 0.085) * (rVoted_PrimaryFlow_m3h / 9800.0);

(* Subcooled Continuous Regulated Spray Mass Flow Rate: w_spray [kg/s] *)
rPrzSprayFlowRate_kgs := (rPressurizerSprayValveOpening * 0.01) * 12.5;

(* Spontaneous Flashing: When P_prz < P_sat(T_liquid) *)
IF rVoted_PressurizerPressure_bar < 154.5 THEN
    rPrzFlashingRate_kgs := 0.45 * (154.5 - rVoted_PressurizerPressure_bar);
ELSE
    rPrzFlashingRate_kgs := 0.0;
END_IF;

(* Steam Condensation: Triggered by subcooled spray droplet thermal boundary layer contact *)
IF rPressurizerSprayValveOpening > 1.0 THEN
    rPrzCondensationRate_kgs := (rPressurizerSprayValveOpening * 0.01) * 8.2;
ELSE
    rPrzCondensationRate_kgs := 0.05; (* Wall ambient passive condensation *)
END_IF;

(* Differential Pressurizer Pressure: dP/dt = f(Q_heaters, w_spray, w_surge, w_flash, w_cond) *)
rTestU2 := (0.000042 * rPressurizerPropHeater_kW) + 
           (0.000065 * rPressurizerBackupHeaters_kW) - 
           (0.000210 * rPrzSprayFlowRate_kgs) + 
           (0.000150 * rPrzSurgeFlowRate_kgs) + 
           (0.000085 * rPrzFlashingRate_kgs) - 
           (0.000110 * rPrzCondensationRate_kgs);
""")

    # PHASE 3: 8x8 MULTIVARIABLE DISCRETE STATE-SPACE PROPAGATION & KALMAN FILTER
    code_parts.append("""(* =====================================================================================================================
 * PHASE 3: 8x8 MULTIVARIABLE DISCRETE STATE-SPACE PROPAGATION & KALMAN OBSERVER
 * Innovation Update: x_hat[k] = A * x_hat[k-1] + B * u[k-1] + L * (y[k] - C * x_pred[k])
 * ===================================================================================================================== *)
(* 1. Propagate Prior State via Discrete State Matrix A and Input Matrix B *)
FOR iIdx := 1 TO 8 DO
    rSum := 0.0;
    FOR jIdx := 1 TO 8 DO
        rSum := rSum + (aStateA[iIdx, jIdx] * aStateEstimated[jIdx]);
    END_FOR;
    FOR kIdx := 1 TO 4 DO
        rSum := rSum + (aStateB[iIdx, kIdx] * aControlVector[kIdx]);
    END_FOR;
    aStateVectorNext[iIdx] := rSum;
END_FOR;

(* 2. Build Measurement Vector y[k] from 2oo3 Validated Physical Sensor Readings *)
aStateVector[1] := rVoted_PowerRangeFlux_pct * 0.01; (* State 1: Normalized Neutron Power [-] *)
aStateVector[2] := aStateVectorNext[2];              (* State 2: Precursors (Observed through delayed physics) *)
aStateVector[3] := aStateEstimated[3];               (* State 3: Fuel Temp (Reconstructed via kinetics/Fourier) *)
aStateVector[4] := rVoted_CladdingPeakTemp_degC;     (* State 4: Clad Peak Temp [deg C] *)
aStateVector[5] := (rVoted_HotLegTemp_degC + rVoted_ColdLegTemp_degC) * 0.50; (* State 5: Core Average Temp [deg C] *)
aStateVector[6] := rVoted_PressurizerPressure_bar;  (* State 6: Pressurizer Pressure [bar] *)
aStateVector[7] := rVoted_PressurizerLevel_pct;     (* State 7: Pressurizer Level [%] *)
aStateVector[8] := rAxialOffset_pct;                (* State 8: Core Axial Offset Delta-I [%] *)

(* 3. Kalman Observer Innovation and State Update *)
FOR iIdx := 1 TO 8 DO
    (* Observer Innovation: Error e_y = y[i] - (C * x_pred)[i] *)
    rPredictedError := aStateVector[iIdx] - aStateVectorNext[iIdx];
    
    (* Corrected State: x_hat[k] = x_pred[k] + L * e_y *)
    aStateEstimated[iIdx] := aStateVectorNext[iIdx] + (aKalmanGainL[iIdx, iIdx] * rPredictedError);
END_FOR;

(* Update Setpoint Reference Vector r[k] *)
aStateReference[1] := rThermalPowerSetpoint * 0.01;
aStateReference[2] := aStateReference[1];
aStateReference[3] := 680.0 * aStateReference[1];
aStateReference[4] := 365.0;
aStateReference[5] := 308.0;
aStateReference[6] := rPressurizerPressSetpoint;
aStateReference[7] := rPressurizerLevelSetpoint;
aStateReference[8] := rAxialOffsetTarget;

(* Compute Tracking Errors: e[k] = r[k] - x_hat[k] *)
FOR iIdx := 1 TO 8 DO
    aStateError[iIdx] := aStateReference[iIdx] - aStateEstimated[iIdx];
END_FOR;
""")

    # PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL OPTIMIZATION
    code_parts.append("""(* =====================================================================================================================
 * PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 * Horizon: Np = 5 prediction stages, Nu = 3 control stages
 * Cost: J = Sum_{p=1..Np} ||x_{k+p} - r||^2_Q + Sum_{u=0..Nu-1} [ ||u||^2_R + ||Delta_u||^2_S ] + ||x_{Np} - r||^2_P
 * Actuator Constraints: CRDM: [-72..+72] steps/min, Heaters: [0..800] kW, Spray: [0..100] %, Pumps: [300..1800] RPM
 * ===================================================================================================================== *)
rBestCandidateCost := 1.0E+12; (* Initialize with infinite cost *)

FOR jIdx := 1 TO 4 DO
    aOptimalDeltaU[jIdx] := 0.0;
END_FOR;

(* Candidate Exploration Loop over Discretized Control Perturbations *)
FOR mIdx := 1 TO 5 DO
    rTestU1 := aControlVector[1] + aCandidateD1[mIdx];
    rTestU2 := aControlVector[2] + aCandidateD2[mIdx];
    rTestU3 := aControlVector[3] + aCandidateD3[mIdx];
    rTestU4 := aControlVector[4] + aCandidateD4[mIdx];

    (* Enforce Actuator Hard Saturation Constraints *)
    IF rTestU1 > 72.0 THEN rTestU1 := 72.0; END_IF;
    IF rTestU1 < -72.0 THEN rTestU1 := -72.0; END_IF;
    IF rTestU2 > 800.0 THEN rTestU2 := 800.0; END_IF;
    IF rTestU2 < 0.0 THEN rTestU2 := 0.0; END_IF;
    IF rTestU3 > 100.0 THEN rTestU3 := 100.0; END_IF;
    IF rTestU3 < 0.0 THEN rTestU3 := 0.0; END_IF;
    IF rTestU4 > 1800.0 THEN rTestU4 := 1800.0; END_IF;
    IF rTestU4 < 300.0 THEN rTestU4 := 300.0; END_IF;

    (* Initialize Internal State Trajectory with Current Estimated State *)
    FOR iIdx := 1 TO 8 DO
        aSimX[iIdx] := aStateEstimated[iIdx];
    END_FOR;

    rCurrentCandidateCost := 0.0;

    (* Receding-Horizon Prediction Loop (Np = 5 Stages) *)
    FOR pIdx := 1 TO 5 DO
        (* Propagate State: aSimXNext = A * aSimX + B * u_test *)
        FOR iIdx := 1 TO 8 DO
            rSum := 0.0;
            FOR jIdx := 1 TO 8 DO
                rSum := rSum + (aStateA[iIdx, jIdx] * aSimX[jIdx]);
            END_FOR;
            rSum := rSum + (aStateB[iIdx, 1] * rTestU1) + 
                           (aStateB[iIdx, 2] * rTestU2) + 
                           (aStateB[iIdx, 3] * rTestU3) + 
                           (aStateB[iIdx, 4] * rTestU4);
            aSimXNext[iIdx] := rSum;
        END_FOR;

        (* Stage Cost: State Error Penalty Sum(Q_ii * (x_sim[i] - r[i])^2) *)
        rStepCost := 0.0;
        FOR iIdx := 1 TO 8 DO
            rPredictedError := aSimXNext[iIdx] - aStateReference[iIdx];
            IF pIdx = 5 THEN
                (* Terminal Stage Cost Penalty P *)
                rStepCost := rStepCost + (aMPC_P_Terminal[iIdx, iIdx] * rPredictedError * rPredictedError);
            ELSE
                rStepCost := rStepCost + (aMPC_Q[iIdx, iIdx] * rPredictedError * rPredictedError);
            END_IF;
        END_FOR;

        (* Actuator Effort Cost Penalty R *)
        IF pIdx <= 3 THEN
            rStepCost := rStepCost + (aMPC_R[1, 1] * rTestU1 * rTestU1 * 0.001) + 
                                     (aMPC_R[2, 2] * rTestU2 * rTestU2 * 0.00001) + 
                                     (aMPC_R[3, 3] * rTestU3 * rTestU3 * 0.001) + 
                                     (aMPC_R[4, 4] * rTestU4 * rTestU4 * 0.000001);

            (* Actuator Slew Rate Penalty S: ||Delta_u||^2_S *)
            rDeltaU := rTestU1 - aControlVector[1];
            rStepCost := rStepCost + (aMPC_S[1, 1] * rDeltaU * rDeltaU * 0.001);
            rDeltaU := rTestU2 - aControlVector[2];
            rStepCost := rStepCost + (aMPC_S[2, 2] * rDeltaU * rDeltaU * 0.0001);
            rDeltaU := rTestU3 - aControlVector[3];
            rStepCost := rStepCost + (aMPC_S[3, 3] * rDeltaU * rDeltaU * 0.01);
            rDeltaU := rTestU4 - aControlVector[4];
            rStepCost := rStepCost + (aMPC_S[4, 4] * rDeltaU * rDeltaU * 0.0001);
        END_IF;

        rCurrentCandidateCost := rCurrentCandidateCost + rStepCost;

        (* Advance Simulation State *)
        FOR iIdx := 1 TO 8 DO
            aSimX[iIdx] := aSimXNext[iIdx];
        END_FOR;
    END_FOR;

    (* Select Minimal Cost Candidate Trajectory *)
    IF rCurrentCandidateCost < rBestCandidateCost THEN
        rBestCandidateCost := rCurrentCandidateCost;
        aOptimalDeltaU[1] := rTestU1 - aControlVector[1];
        aOptimalDeltaU[2] := rTestU2 - aControlVector[2];
        aOptimalDeltaU[3] := rTestU3 - aControlVector[3];
        aOptimalDeltaU[4] := rTestU4 - aControlVector[4];
    END_IF;
END_FOR;

(* Apply Optimized Control Actions if Supervisory Automation is Enabled and Not in SCRAM *)
IF bAutoControlEnable AND NOT bReactorScramLatched THEN
    aControlVector[1] := aControlVector[1] + aOptimalDeltaU[1];
    aControlVector[2] := aControlVector[2] + aOptimalDeltaU[2];
    aControlVector[3] := aControlVector[3] + aOptimalDeltaU[3];
    aControlVector[4] := aControlVector[4] + aOptimalDeltaU[4];

    (* Saturated Final Output Demands *)
    IF aControlVector[1] > 72.0 THEN aControlVector[1] := 72.0; END_IF;
    IF aControlVector[1] < -72.0 THEN aControlVector[1] := -72.0; END_IF;
    IF aControlVector[2] > 800.0 THEN aControlVector[2] := 800.0; END_IF;
    IF aControlVector[2] < 0.0 THEN aControlVector[2] := 0.0; END_IF;
    IF aControlVector[3] > 100.0 THEN aControlVector[3] := 100.0; END_IF;
    IF aControlVector[3] < 0.0 THEN aControlVector[3] := 0.0; END_IF;
    IF aControlVector[4] > 1800.0 THEN aControlVector[4] := 1800.0; END_IF;
    IF aControlVector[4] < 300.0 THEN aControlVector[4] := 300.0; END_IF;

    rCRDM_StepRateDemand           := aControlVector[1];
    rPressurizerPropHeater_kW      := aControlVector[2];
    rPressurizerSprayValveOpening  := aControlVector[3];
    rRCS_CannedPumpSpeedDemand_RPM := aControlVector[4];
ELSE
    IF bReactorScramLatched THEN
        rCRDM_StepRateDemand           := -72.0; (* Full speed emergency rod insertion demand *)
        rPressurizerPropHeater_kW      := 0.0;   (* Cut all electric immersion heaters immediately *)
        rPressurizerBackupHeaters_kW   := 0.0;
        rPressurizerSprayValveOpening  := 0.0;
        rRCS_CannedPumpSpeedDemand_RPM := 450.0; (* Pump coastdown to low speed or natural circulation transition *)
    END_IF;
END_IF;

(* Determine CRDM Discrete Direction Command *)
IF rCRDM_StepRateDemand > 2.0 THEN
    nCRDM_StepDirection := 1;  (* Stepping Rods Out (Withdrawal) *)
ELSIF rCRDM_StepRateDemand < -2.0 THEN
    nCRDM_StepDirection := -1; (* Stepping Rods In (Insertion) *)
ELSE
    nCRDM_StepDirection := 0;  (* Holding Position *)
END_IF;

(* Update Prior Step Control Vectors *)
FOR jIdx := 1 TO 4 DO
    aDeltaControlVector[jIdx] := aControlVector[jIdx] - aControlVectorPrev[jIdx];
    aControlVectorPrev[jIdx]  := aControlVector[jIdx];
END_FOR;
""")

    # PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # Covering all 12 operational modes in complete detail
    code_parts.append("""(* =====================================================================================================================
 * PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
 * Nuclear Island Plant Operating Modes (IEC 61513 / Westinghouse SMR standard architecture)
 * States: 1: REACTOR_COLD_SHUTDOWN, 2: HOT_STANDBY_CRITICALITY_PREP, 3: APPROACH_TO_CRITICALITY_PULSE,
 *         4: LOW_POWER_PHYSICS_TESTING, 5: TURBINE_SYNC_POWER_ASCENSION, 6: BASELOAD_STEADY_STATE_100PCT,
 *         7: LOAD_FOLLOW_RAMP_CYCLING, 8: PRESSURIZER_TRANSIENT_DAMPING, 9: XENON_OVERRIDE_CORE_TRIM,
 *         10: SCRAM_FAST_ROD_INSERTION, 11: PRHRS_PASSIVE_DECAY_COOLING, 12: POST_TRIP_SAFE_STABILIZATION
 * ===================================================================================================================== *)
tStateTimer_s := tStateTimer_s + rCycleTime_s;

CASE nActiveFSMState OF
    1: (* REACTOR_COLD_SHUTDOWN *)
        sActiveFSMStateName := 'REACTOR_COLD_SHUTDOWN';
        bReactorTripBreaker_RTBA := FALSE; (* Trip breakers open *)
        bReactorTripBreaker_RTBB := FALSE;
        bCRDM_HoldCoilPower_ChA  := FALSE; (* Coils unpowered *)
        bCRDM_HoldCoilPower_ChB  := FALSE;
        bPRHRS_IsolationValve_01 := FALSE;
        bPRHRS_IsolationValve_02 := FALSE;
        rPressurizerPropHeater_kW := 0.0;
        rPressurizerBackupHeaters_kW := 0.0;
        rPressurizerSprayValveOpening := 0.0;
        rRCS_CannedPumpSpeedDemand_RPM := 300.0; (* Minimum circulation for residual heat removal *)

        (* Transition to Hot Standby when RCS heated and boron adjusted *)
        IF bAutoControlEnable AND rVoted_ColdLegTemp_degC >= 280.0 AND rVoted_PressurizerPressure_bar >= 150.0 AND NOT bReactorScramLatched THEN
            nActiveFSMState := 2;
            tStateTimer_s := 0.0;
        END_IF;

    2: (* HOT_STANDBY_CRITICALITY_PREP *)
        sActiveFSMStateName := 'HOT_STANDBY_CRITICALITY_PREP';
        bReactorTripBreaker_RTBA := TRUE; (* Close reactor trip breakers *)
        bReactorTripBreaker_RTBB := TRUE;
        bCRDM_HoldCoilPower_ChA  := TRUE; (* Energize magnetic jack holding coils *)
        bCRDM_HoldCoilPower_ChB  := TRUE;
        rRCS_CannedPumpSpeedDemand_RPM := 1485.0; (* Nominal flow rate *)

        (* Maintain Pressurizer at 155.0 bar *)
        IF rVoted_PressurizerPressure_bar < 154.8 THEN
            rPressurizerPropHeater_kW := 450.0;
            rPressurizerSprayValveOpening := 0.0;
        ELSIF rVoted_PressurizerPressure_bar > 155.2 THEN
            rPressurizerPropHeater_kW := 0.0;
            rPressurizerSprayValveOpening := 15.0;
        ELSE
            rPressurizerPropHeater_kW := 200.0;
            rPressurizerSprayValveOpening := 5.0;
        END_IF;

        (* Advance to Approach to Criticality upon operator authorization *)
        IF tStateTimer_s >= 5.0 AND bAutoControlEnable AND NOT bReactorScramLatched THEN
            nActiveFSMState := 3;
            tStateTimer_s := 0.0;
        END_IF;

    3: (* APPROACH_TO_CRITICALITY_PULSE *)
        sActiveFSMStateName := 'APPROACH_TO_CRITICALITY_PULSE';
        bReactorTripBreaker_RTBA := TRUE;
        bReactorTripBreaker_RTBB := TRUE;
        bCRDM_HoldCoilPower_ChA  := TRUE;
        bCRDM_HoldCoilPower_ChB  := TRUE;

        (* Slow stepping withdrawal of regulating rod bank (12 steps/min) *)
        rCRDM_StepRateDemand := 12.0;
        nCRDM_StepDirection  := 1;

        (* Monitor 1/M inverse count rate: when reaching point of adding heat (10^-4 RTP), proceed *)
        IF rVoted_IntermediateFlux_pct >= 0.05 OR rVoted_PowerRangeFlux_pct >= 0.10 THEN
            rCRDM_StepRateDemand := 0.0;
            nCRDM_StepDirection  := 0;
            nActiveFSMState := 4;
            tStateTimer_s := 0.0;
        END_IF;

    4: (* LOW_POWER_PHYSICS_TESTING *)
        sActiveFSMStateName := 'LOW_POWER_PHYSICS_TESTING';
        bReactorTripBreaker_RTBA := TRUE;
        bReactorTripBreaker_RTBB := TRUE;
        bCRDM_HoldCoilPower_ChA  := TRUE;
        bCRDM_HoldCoilPower_ChB  := TRUE;

        (* Maintain power around 1.0% RTP for isothermal temperature coefficient testing *)
        IF rVoted_PowerRangeFlux_pct < 0.90 THEN
            rCRDM_StepRateDemand := 8.0;
            nCRDM_StepDirection  := 1;
        ELSIF rVoted_PowerRangeFlux_pct > 1.10 THEN
            rCRDM_StepRateDemand := -8.0;
            nCRDM_StepDirection  := -1;
        ELSE
            rCRDM_StepRateDemand := 0.0;
            nCRDM_StepDirection  := 0;
        END_IF;

        (* Transition to Power Ascension when testing completed *)
        IF tStateTimer_s >= 10.0 AND bAutoControlEnable AND NOT bReactorScramLatched THEN
            nActiveFSMState := 5;
            tStateTimer_s := 0.0;
        END_IF;

    5: (* TURBINE_SYNC_POWER_ASCENSION *)
        sActiveFSMStateName := 'TURBINE_SYNC_POWER_ASCENSION';
        bReactorTripBreaker_RTBA := TRUE;
        bReactorTripBreaker_RTBB := TRUE;
        bCRDM_HoldCoilPower_ChA  := TRUE;
        bCRDM_HoldCoilPower_ChB  := TRUE;

        (* Controlled power ramp at 5% / min *)
        IF rVoted_PowerRangeFlux_pct < rThermalPowerSetpoint THEN
            rCRDM_StepRateDemand := 18.0;
            nCRDM_StepDirection  := 1;
        ELSE
            rCRDM_StepRateDemand := 0.0;
            nCRDM_StepDirection  := 0;
        END_IF;

        (* When reaching >= 98% RTP, switch to Baseload Steady State *)
        IF rVoted_PowerRangeFlux_pct >= 98.0 AND ABS(rVoted_PressurizerPressure_bar - 155.0) <= 0.50 THEN
            nActiveFSMState := 6;
            tStateTimer_s := 0.0;
        END_IF;

    6: (* BASELOAD_STEADY_STATE_100PCT *)
        sActiveFSMStateName := 'BASELOAD_STEADY_STATE_100PCT';
        bReactorTripBreaker_RTBA := TRUE;
        bReactorTripBreaker_RTBB := TRUE;
        bCRDM_HoldCoilPower_ChA  := TRUE;
        bCRDM_HoldCoilPower_ChB  := TRUE;

        (* High precision Model Predictive Control handles all continuous actuators *)
        bThermalHydraulicStable := (ABS(rVoted_PressurizerPressure_bar - 155.0) <= 0.20) AND 
                                   (ABS(rVoted_PressurizerLevel_pct - 55.0) <= 1.0) AND 
                                   (ABS(rAxialOffset_pct) <= 2.0);

        (* Check if turbine trip or load rejection occurs *)
        IF bTurbineTripInterlock THEN
            nActiveFSMState := 8; (* Switch to Transient Damping *)
            tStateTimer_s := 0.0;
        ELSIF ABS(rAxialOffset_pct) > 3.5 THEN
            nActiveFSMState := 9; (* Switch to Xenon Core Trim *)
            tStateTimer_s := 0.0;
        END_IF;

    7: (* LOAD_FOLLOW_RAMP_CYCLING *)
        sActiveFSMStateName := 'LOAD_FOLLOW_RAMP_CYCLING';
        bReactorTripBreaker_RTBA := TRUE;
        bReactorTripBreaker_RTBB := TRUE;
        bCRDM_HoldCoilPower_ChA  := TRUE;
        bCRDM_HoldCoilPower_ChB  := TRUE;

        (* Coordinated boron dilution and CRDM stepping for grid frequency load follow *)
        IF rVoted_PowerRangeFlux_pct < (rThermalPowerSetpoint - 1.0) THEN
            rCRDM_StepRateDemand := 24.0;
            nCRDM_StepDirection  := 1;
        ELSIF rVoted_PowerRangeFlux_pct > (rThermalPowerSetpoint + 1.0) THEN
            rCRDM_StepRateDemand := -24.0;
            nCRDM_StepDirection  := -1;
        ELSE
            rCRDM_StepRateDemand := 0.0;
            nCRDM_StepDirection  := 0;
            nActiveFSMState := 6; (* Return to steady state *)
            tStateTimer_s := 0.0;
        END_IF;

    8: (* PRESSURIZER_TRANSIENT_DAMPING *)
        sActiveFSMStateName := 'PRESSURIZER_TRANSIENT_DAMPING';
        bReactorTripBreaker_RTBA := TRUE;
        bReactorTripBreaker_RTBB := TRUE;
        bCRDM_HoldCoilPower_ChA  := TRUE;
        bCRDM_HoldCoilPower_ChB  := TRUE;

        (* Aggressive spray / heater actuation to absorb turbine trip load rejection thermal surge *)
        IF rVoted_PressurizerPressure_bar > 156.5 THEN
            rPressurizerSprayValveOpening := 85.0; (* Max continuous spray *)
            rPressurizerPropHeater_kW := 0.0;
            rPressurizerBackupHeaters_kW := 0.0;
            rCRDM_StepRateDemand := -48.0; (* Rapid rod runback *)
            nCRDM_StepDirection  := -1;
        ELSIF rVoted_PressurizerPressure_bar < 153.5 THEN
            rPressurizerSprayValveOpening := 0.0;
            rPressurizerPropHeater_kW := 800.0;
            rPressurizerBackupHeaters_kW := 1200.0; (* Engage full backup immersion heaters *)
            rCRDM_StepRateDemand := 0.0;
            nCRDM_StepDirection  := 0;
        ELSE
            rPressurizerBackupHeaters_kW := 0.0;
            IF tStateTimer_s >= 8.0 AND ABS(rVoted_PressurizerPressure_bar - 155.0) <= 0.40 THEN
                nActiveFSMState := 6;
                tStateTimer_s := 0.0;
            END_IF;
        END_IF;

    9: (* XENON_OVERRIDE_CORE_TRIM *)
        sActiveFSMStateName := 'XENON_OVERRIDE_CORE_TRIM';
        bReactorTripBreaker_RTBA := TRUE;
        bReactorTripBreaker_RTBB := TRUE;
        bCRDM_HoldCoilPower_ChA  := TRUE;
        bCRDM_HoldCoilPower_ChB  := TRUE;

        (* Spatial xenon oscillation damping: Dither regulating rod bank to restore axial offset *)
        IF rAxialOffset_pct > 2.0 THEN
            rCRDM_StepRateDemand := -16.0; (* Insert to depress top flux *)
            nCRDM_StepDirection  := -1;
        ELSIF rAxialOffset_pct < -2.0 THEN
            rCRDM_StepRateDemand := 16.0;  (* Withdraw to raise top flux *)
            nCRDM_StepDirection  := 1;
        ELSE
            rCRDM_StepRateDemand := 0.0;
            nCRDM_StepDirection  := 0;
            IF tStateTimer_s >= 6.0 THEN
                nActiveFSMState := 6;
                tStateTimer_s := 0.0;
            END_IF;
        END_IF;

    10: (* SCRAM_FAST_ROD_INSERTION *)
        sActiveFSMStateName := 'SCRAM_FAST_ROD_INSERTION';
        (* IEEE 603 / IEC 61513 Nuclear Safety Class 1E De-Energization Logic *)
        bReactorTripBreaker_RTBA := FALSE; (* Immediate Breaker Open (< 20 ms) *)
        bReactorTripBreaker_RTBB := FALSE;
        bCRDM_HoldCoilPower_ChA  := FALSE; (* Stationary Gripper De-energized -> Gravity Drop *)
        bCRDM_HoldCoilPower_ChB  := FALSE;
        rCRDM_StepRateDemand     := -72.0; (* Full mechanical drive assist insertion *)
        nCRDM_StepDirection      := -1;
        rPressurizerPropHeater_kW := 0.0;  (* Immediate cut of all heaters *)
        rPressurizerBackupHeaters_kW := 0.0;
        rPressurizerSprayValveOpening := 0.0;
        rScramElapsedTimer_s := rScramElapsedTimer_s + rCycleTime_s;

        (* Verify rods fully inserted via 2oo3 position sensors (< 1.8 s) *)
        IF rVoted_CRDM_Position_mm <= 50.0 OR rScramElapsedTimer_s >= 2.0 THEN
            nActiveFSMState := 11; (* Transition to Passive Residual Heat Removal *)
            tStateTimer_s := 0.0;
        END_IF;

    11: (* PRHRS_PASSIVE_DECAY_COOLING *)
        sActiveFSMStateName := 'PRHRS_PASSIVE_DECAY_COOLING';
        bReactorTripBreaker_RTBA := FALSE;
        bReactorTripBreaker_RTBB := FALSE;
        bCRDM_HoldCoilPower_ChA  := FALSE;
        bCRDM_HoldCoilPower_ChB  := FALSE;

        (* Actuate Fail-Open PRHRS Isolation Valves to Establish Natural Circulation *)
        bPRHRS_IsolationValve_01 := TRUE;
        bPRHRS_IsolationValve_02 := TRUE;
        bPRHRS_Active            := TRUE;

        (* Primary Canned Motor Pumps Coastdown to Safe Idle *)
        rRCS_CannedPumpSpeedDemand_RPM := 0.0;

        (* Verify thermosiphon natural circulation established and cladding cooled *)
        IF rVoted_CladdingPeakTemp_degC <= 320.0 AND rNaturalCirculationBuoyancy_kPa >= 1.5 THEN
            nActiveFSMState := 12; (* Transition to Post-Trip Safe Stabilization *)
            tStateTimer_s := 0.0;
        END_IF;

    12: (* POST_TRIP_SAFE_STABILIZATION *)
        sActiveFSMStateName := 'POST_TRIP_SAFE_STABILIZATION';
        bReactorTripBreaker_RTBA := FALSE;
        bReactorTripBreaker_RTBB := FALSE;
        bCRDM_HoldCoilPower_ChA  := FALSE;
        bCRDM_HoldCoilPower_ChB  := FALSE;
        bPRHRS_IsolationValve_01 := TRUE;
        bPRHRS_IsolationValve_02 := TRUE;
        bPRHRS_Active            := TRUE;
        rRCS_CannedPumpSpeedDemand_RPM := 0.0;

        (* Hold Subcritical Stable Cold/Intermediate State indefinitely *)
        IF bMasterFaultReset AND NOT bSafetyInjectionRequired AND rVoted_CladdingPeakTemp_degC < 250.0 THEN
            bReactorScramLatched := FALSE;
            rScramElapsedTimer_s := 0.0;
            nActiveFSMState := 1; (* Return to Cold Shutdown *)
            tStateTimer_s := 0.0;
        END_IF;

ELSE
    (* Defensive Programming Fallback *)
    nActiveFSMState := 10; (* Default to SCRAM *)
    tStateTimer_s := 0.0;
END_CASE;
""")

    # PHASE 6: ISA-18.2 PROCESS ALARMS, TRIPS & DIAGNOSTIC WORD BIT PACKING
    code_parts.append("""(* =====================================================================================================================
 * PHASE 6: ISA-18.2 PROCESS ALARMS, TRIPS & DIAGNOSTIC WORD BIT PACKING
 * Class 1E Reactor Protection System Interlocks & 4x 16-Bit Comprehensive Diagnostic Words
 * ===================================================================================================================== *)
(* 1. Pressurizer Pressure ISA-18.2 Alarm Tiers with Deadband Hysteresis *)
IF rVoted_PressurizerPressure_bar >= cTrip_PPrz_HI_HI_bar THEN
    bAlarm_PPrz_HI_HI := TRUE;
ELSIF rVoted_PressurizerPressure_bar <= (cTrip_PPrz_HI_HI_bar - cDeadband_PPrz_bar) THEN
    bAlarm_PPrz_HI_HI := FALSE;
END_IF;

IF rVoted_PressurizerPressure_bar >= cTrip_PPrz_HI_bar THEN
    bAlarm_PPrz_HI := TRUE;
ELSIF rVoted_PressurizerPressure_bar <= (cTrip_PPrz_HI_bar - cDeadband_PPrz_bar) THEN
    bAlarm_PPrz_HI := FALSE;
END_IF;

IF rVoted_PressurizerPressure_bar <= cTrip_PPrz_LO_bar THEN
    bAlarm_PPrz_LO := TRUE;
ELSIF rVoted_PressurizerPressure_bar >= (cTrip_PPrz_LO_bar + cDeadband_PPrz_bar) THEN
    bAlarm_PPrz_LO := FALSE;
END_IF;

IF rVoted_PressurizerPressure_bar <= cTrip_PPrz_LO_LO_bar THEN
    bAlarm_PPrz_LO_LO := TRUE;
    bSafetyInjectionRequired := TRUE;
ELSIF rVoted_PressurizerPressure_bar >= (cTrip_PPrz_LO_LO_bar + cDeadband_PPrz_bar) THEN
    bAlarm_PPrz_LO_LO := FALSE;
END_IF;

(* 2. Ex-Core Power Range Neutron Flux & Period Protection *)
IF rVoted_PowerRangeFlux_pct >= cTrip_Flux_HI_HI_pct THEN
    bAlarm_Flux_HI_HI := TRUE;
ELSIF rVoted_PowerRangeFlux_pct <= (cTrip_Flux_HI_HI_pct - cDeadband_Flux_pct) THEN
    bAlarm_Flux_HI_HI := FALSE;
END_IF;

IF rVoted_PowerRangeFlux_pct >= cTrip_Flux_HI_pct THEN
    bAlarm_Flux_HI := TRUE;
ELSIF rVoted_PowerRangeFlux_pct <= (cTrip_Flux_HI_pct - cDeadband_Flux_pct) THEN
    bAlarm_Flux_HI := FALSE;
END_IF;

(* Flux Rate of Change Derivative *)
IF (rVoted_PowerRangeFlux_pct - rFluxPreviousScan_pct) / rCycleTime_s >= cTrip_Flux_ROC_pct_s THEN
    bAlarm_Flux_ROC := TRUE;
ELSE
    bAlarm_Flux_ROC := FALSE;
END_IF;
rFluxPreviousScan_pct := rVoted_PowerRangeFlux_pct;

(* Reactor Period Low Trip *)
IF rReactorPeriod_s > 0.0 AND rReactorPeriod_s <= cTrip_Period_Min_s THEN
    bAlarm_Period_Short := TRUE;
ELSE
    bAlarm_Period_Short := FALSE;
END_IF;

(* 3. Primary Coolant Flow & Cladding Temperature Protection *)
IF rVoted_PrimaryFlow_m3h <= (9800.0 * (cTrip_Flow_LO_LO_pct * 0.01)) THEN
    bAlarm_Flow_LO_LO := TRUE;
ELSE
    bAlarm_Flow_LO_LO := FALSE;
END_IF;

IF rVoted_PrimaryFlow_m3h <= (9800.0 * (cTrip_Flow_LO_pct * 0.01)) THEN
    bAlarm_Flow_LO := TRUE;
ELSE
    bAlarm_Flow_LO := FALSE;
END_IF;

IF rVoted_CladdingPeakTemp_degC >= cTrip_Clad_HI_HI_degC THEN
    bAlarm_Clad_HI_HI := TRUE;
ELSE
    bAlarm_Clad_HI_HI := FALSE;
END_IF;

IF rVoted_HotLegTemp_degC >= cTrip_HotLeg_HI_HI_degC THEN
    bAlarm_HotLeg_HI_HI := TRUE;
ELSE
    bAlarm_HotLeg_HI_HI := FALSE;
END_IF;

(* 4. Pressurizer Level Operational Limits *)
IF rVoted_PressurizerLevel_pct >= cTrip_LPrz_HI_HI_pct THEN
    bAlarm_LPrz_HI_HI := TRUE;
ELSE
    bAlarm_LPrz_HI_HI := FALSE;
END_IF;

IF rVoted_PressurizerLevel_pct <= cTrip_LPrz_LO_LO_pct THEN
    bAlarm_LPrz_LO_LO := TRUE;
ELSE
    bAlarm_LPrz_LO_LO := FALSE;
END_IF;

(* 5. Core Axial Flux Offset Imbalance Warning *)
IF ABS(rAxialOffset_pct) > 3.0 THEN
    bAlarm_AxialOffset_Dev := TRUE;
ELSE
    bAlarm_AxialOffset_Dev := FALSE;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * IEEE 603 / IEC 61513 Nuclear Safety Class 1E Master Reactor SCRAM Interlock Logic
 * Immediate (< 20 ms) Fast De-Energization on Any Protective Trip or Manual Operator Scram
 * ----------------------------------------------------------------------------------------------------------------- *)
IF (NOT bManualScramPB_ChA) OR 
   (NOT bManualScramPB_ChB) OR 
   bAlarm_PPrz_HI_HI OR 
   bAlarm_PPrz_LO_LO OR 
   bAlarm_Flux_HI_HI OR 
   bAlarm_Flux_ROC OR 
   bAlarm_Period_Short OR 
   bAlarm_Flow_LO_LO OR 
   bAlarm_Clad_HI_HI OR 
   bAlarm_HotLeg_HI_HI OR 
   bSafetyInjectionActive THEN

    bReactorScramLatched := TRUE;
    nActiveFSMState := 10; (* Force state to SCRAM_FAST_ROD_INSERTION immediately *)
    bReactorTripBreaker_RTBA := FALSE;
    bReactorTripBreaker_RTBB := FALSE;
    bCRDM_HoldCoilPower_ChA  := FALSE;
    bCRDM_HoldCoilPower_ChB  := FALSE;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Diagnostic Word 01: 2oo3 Sensor Health & Channel Discrepancy Fault Bits
 * ----------------------------------------------------------------------------------------------------------------- *)
wDiagnosticWord01 := 16#0000;
IF bFault_PT101_ChA   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0001; END_IF;
IF bFault_PT101_ChB   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0002; END_IF;
IF bFault_PT101_ChC   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0004; END_IF;
IF bFault_LT102_ChA   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0008; END_IF;
IF bFault_LT102_ChB   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0010; END_IF;
IF bFault_LT102_ChC   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0020; END_IF;
IF bFault_TT201_ChA   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0040; END_IF;
IF bFault_TT201_ChB   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0080; END_IF;
IF bFault_TT201_ChC   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0100; END_IF;
IF bFault_TT202_ChA   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0200; END_IF;
IF bFault_NIT301_ChA  THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0400; END_IF;
IF bFault_NIT301_ChB  THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0800; END_IF;
IF bFault_NIT301_ChC  THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#1000; END_IF;
IF bFault_ZT401_ChA   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#2000; END_IF;
IF bFault_FT501_ChA   THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#4000; END_IF;
IF bAlarm_2oo3_DegradedChannel THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#8000; END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Diagnostic Word 02: ISA-18.2 HI_HI & LO_LO Protective Trip Bits (Class 1E SCRAM Causes)
 * ----------------------------------------------------------------------------------------------------------------- *)
wDiagnosticWord02 := 16#0000;
IF bAlarm_PPrz_HI_HI       THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0001; END_IF;
IF bAlarm_PPrz_LO_LO       THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0002; END_IF;
IF bAlarm_Flux_HI_HI       THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0004; END_IF;
IF bAlarm_Flux_ROC         THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0008; END_IF;
IF bAlarm_Period_Short     THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0010; END_IF;
IF bAlarm_Flow_LO_LO       THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0020; END_IF;
IF bAlarm_Clad_HI_HI       THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0040; END_IF;
IF bAlarm_HotLeg_HI_HI     THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0080; END_IF;
IF bAlarm_LPrz_HI_HI       THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0100; END_IF;
IF bAlarm_LPrz_LO_LO       THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0200; END_IF;
IF NOT bManualScramPB_ChA  THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0400; END_IF;
IF NOT bManualScramPB_ChB  THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0800; END_IF;
IF bSafetyInjectionActive  THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#1000; END_IF;
IF bSafetyInjectionRequired THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#2000; END_IF;
IF bContainmentIsolationSignal THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#4000; END_IF;
IF bReactorScramLatched    THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#8000; END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Diagnostic Word 03: ISA-18.2 Warning & Operational Deviation Alarm Bits
 * ----------------------------------------------------------------------------------------------------------------- *)
wDiagnosticWord03 := 16#0000;
IF bAlarm_PPrz_HI          THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0001; END_IF;
IF bAlarm_PPrz_LO          THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0002; END_IF;
IF bAlarm_Flux_HI          THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0004; END_IF;
IF bAlarm_Flow_LO          THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0008; END_IF;
IF bAlarm_AxialOffset_Dev  THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0010; END_IF;
IF bTurbineTripInterlock   THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0020; END_IF;
IF rDepartureFromNucleateBoilingRatio < 1.35 THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0040; END_IF;
IF rFuelCenterlineTemp_degC > 1400.0 THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0080; END_IF;
IF rPressurizerPropHeater_kW >= 790.0 THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0100; END_IF;
IF rPressurizerBackupHeaters_kW > 0.0 THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0200; END_IF;
IF rPressurizerSprayValveOpening >= 95.0 THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0400; END_IF;
IF bPRHRS_Active           THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0800; END_IF;
IF NOT bAutoControlEnable  THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#1000; END_IF;
IF bThermalHydraulicStable THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#2000; END_IF;
IF bModelInitialized       THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#4000; END_IF;
IF bAlarmAcknowledge       THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#8000; END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Diagnostic Word 04: Active FSM State Code, Safety System & Margin Bits
 * ----------------------------------------------------------------------------------------------------------------- *)
wDiagnosticWord04 := INT_TO_WORD(nActiveFSMState) AND 16#000F; (* Bits 0..3: FSM State [1..12] *)
IF bPRHRS_IsolationValve_01 THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0010; END_IF;
IF bPRHRS_IsolationValve_02 THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0020; END_IF;
IF bReactorTripBreaker_RTBA THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0040; END_IF;
IF bReactorTripBreaker_RTBB THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0080; END_IF;
IF bCRDM_HoldCoilPower_ChA  THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0100; END_IF;
IF bCRDM_HoldCoilPower_ChB  THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0200; END_IF;
IF nCRDM_StepDirection > 0  THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0400; END_IF;
IF nCRDM_StepDirection < 0  THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0800; END_IF;
IF rNaturalCirculationBuoyancy_kPa > 1.0 THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#1000; END_IF;
IF rBestCandidateCost < 1000.0 THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#2000; END_IF;
IF bMasterFaultReset       THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#4000; END_IF;
IF bReactorScramLatched    THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#8000; END_IF;

END_FUNCTION_BLOCK
""")

    return "".join(code_parts)

def check_parity(st_code):
    lines = st_code.splitlines()
    
    # Strip comments for delimiter analysis
    clean_lines = []
    in_block_comment = False
    for line in lines:
        cleaned = ""
        i = 0
        while i < len(line):
            if in_block_comment:
                if line[i:i+2] == "*)":
                    in_block_comment = False
                    i += 2
                else:
                    i += 1
            else:
                if line[i:i+2] == "(*":
                    in_block_comment = True
                    i += 2
                elif line[i:i+2] == "//":
                    break # Rest of line is comment
                else:
                    cleaned += line[i]
                    i += 1
        clean_lines.append(cleaned)
        
    clean_text = "\n".join(clean_lines)
    
    # Token matches using regex word boundaries
    if_count = len(re.findall(r'\bIF\b', clean_text, re.IGNORECASE))
    end_if_count = len(re.findall(r'\bEND_IF\b', clean_text, re.IGNORECASE))
    
    case_count = len(re.findall(r'\bCASE\b', clean_text, re.IGNORECASE))
    end_case_count = len(re.findall(r'\bEND_CASE\b', clean_text, re.IGNORECASE))
    
    for_count = len(re.findall(r'\bFOR\b', clean_text, re.IGNORECASE))
    end_for_count = len(re.findall(r'\bEND_FOR\b', clean_text, re.IGNORECASE))
    
    while_count = len(re.findall(r'\bWHILE\b', clean_text, re.IGNORECASE))
    end_while_count = len(re.findall(r'\bEND_WHILE\b', clean_text, re.IGNORECASE))
    
    fb_count = len(re.findall(r'\bFUNCTION_BLOCK\b', clean_text, re.IGNORECASE))
    end_fb_count = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_text, re.IGNORECASE))
    
    var_count = len(re.findall(r'\bVAR\b|\bVAR_INPUT\b|\bVAR_OUTPUT\b|\bVAR_IN_OUT\b', clean_text, re.IGNORECASE))
    end_var_count = len(re.findall(r'\bEND_VAR\b', clean_text, re.IGNORECASE))
    
    results = {
        "IF / END_IF": (if_count, end_if_count, if_count == end_if_count),
        "CASE / END_CASE": (case_count, end_case_count, case_count == end_case_count),
        "FOR / END_FOR": (for_count, end_for_count, for_count == end_for_count),
        "WHILE / END_WHILE": (while_count, end_while_count, while_count == end_while_count),
        "FUNCTION_BLOCK / END_FB": (fb_count, end_fb_count, fb_count == end_fb_count),
        "VAR / END_VAR": (var_count, end_var_count, var_count == end_var_count),
    }
    
    all_ok = all(v[2] for v in results.values())
    return all_ok, results

if __name__ == "__main__":
    st_code = build_st_code()
    char_len = len(st_code)
    line_count = len(st_code.splitlines())
    print(f"Generated ST Code: {char_len} characters, {line_count} lines")
    
    ok, parity = check_parity(st_code)
    print("Parity Check Results:")
    for k, v in parity.items():
        status = "PASS" if v[2] else "FAIL"
        print(f"  {k}: {v[0]} vs {v[1]} -> [{status}]")
        
    if not ok:
        print("ERROR: AST Delimiter Parity check failed!")
        sys.exit(1)
    else:
        print("SUCCESS: 100% AST Delimiter Parity Confirmed!")
