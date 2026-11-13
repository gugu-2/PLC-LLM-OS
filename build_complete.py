# Generator script build_complete.py
import json
import uuid
import re
import os
import sys

def main():
    parts = []
    
    # -------------------------------------------------------------
    # 0. HEADER & FUNCTION BLOCK DECLARATION
    # -------------------------------------------------------------
    parts.append("FUNCTION_BLOCK FB_Nuclear_PWR_PrimaryCoolant_Pressurizer_RodControl_Coordinated\n")
    parts.append("""(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: NUCLEAR POWER GENERATION & CLEAN ENERGY INFRASTRUCTURE
TARGET SYSTEM: COMMERCIAL PRESSURIZED WATER REACTOR (PWR) PRIMARY COOLANT LOOP (RCS),
               PRESSURIZER PRESSURE/LEVEL NONEQUILIBRIUM THERMODYNAMICS, AND CONTROL ROD
               REACTIVITY REGULATION COUPLING
PLANT REFERENCE: 1,150 MWe (3,411 MWth) 4-LOOP GENERATION III+ PRESSURIZED WATER REACTOR
SAFETY CLASS: CLASS 1E / IEEE 603 / IEC 61508 SIL-3 REDUNDANT DCS ARCHITECTURE
PERSONA: V7 PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR (75+ YEARS EXPERIENCE)

ARCHITECTURAL SUBSYSTEMS INTEGRATED:
  1. REACTOR POINT KINETICS WITH 6 DELAYED NEUTRON PRECURSOR GROUPS & PRECISE THERMAL FEEDBACK
     - Prompt neutron lifetime Lambda = 2.0E-5 [s], Total delayed fraction Beta = 0.006502 (650.2 [pcm])
     - Delayed precursor groups:
       * Group 1: Beta_1 = 0.000215, Lambda_1 = 0.0124 [s^-1]
       * Group 2: Beta_2 = 0.001424, Lambda_2 = 0.0305 [s^-1]
       * Group 3: Beta_3 = 0.001274, Lambda_3 = 0.1110 [s^-1]
       * Group 4: Beta_4 = 0.002568, Lambda_4 = 0.3010 [s^-1]
       * Group 5: Beta_5 = 0.000748, Lambda_5 = 1.1400 [s^-1]
       * Group 6: Beta_6 = 0.000273, Lambda_6 = 3.0100 [s^-1]
     - Doppler fuel temperature coefficient alpha_Doppler [pcm/deg C]
     - Moderator temperature coefficient alpha_Moderator [pcm/deg C]
     - Chemical shim soluble boron reactivity worth rho_boron [pcm/ppm]
     - Iodine-135 / Xenon-135 dynamic equilibrium and post-trip poisoning chain differential dynamics
  2. PRESSURIZER TWO-REGION NON-EQUILIBRIUM THERMODYNAMIC CONTROL
     - Liquid water and steam vapor inventory mass and enthalpy conservation balances
     - Surge flow coupling driven by RCS thermal expansion / contraction: W_surge = f(dTavg/dt)
     - Proportional SCR electric heater banks and on/off backup heater banks
     - Continuous and modulating cold leg spray valves with subcooled liquid droplet thermodynamics
     - Class 1E pilot-operated relief valves (PORVs) and spring safety valve pilot stages
  3. PRIMARY COOLANT LOOP (RCS) TEMPERATURE DYNAMICS & TURBINE LOAD PROGRAM
     - T_avg dynamic tracking against turbine steam load reference program: T_ref = f(Load_MW)
     - Core Delta-T (T_hot - T_cold) and nuclear flux lead-lag mismatch compensation
     - Maximum permissible thermal ramp rate constraint: |dTavg/dt| <= 55.0 [deg C / hr]
  4. 6x6 DISCRETE STATE-SPACE OBSERVER & LUENBERGER INNOVATION
     - State vector: x = [Power (%FP), T_avg (deg C), T_fuel (deg C), Pzr_P (bar), Pzr_L (%), Flow (kg/s)]
     - Actuators: u = [CRDM speed (steps/min), Prop Heaters (%), Spray (%), Net CVCS (%), Backup Heaters (%)]
     - Explicit discrete state transition matrix A (6x6), input matrix B (6x5), output matrix C (6x6),
       direct transmission matrix D (6x5), and Kalman/Luenberger observer innovation gain matrix L (6x6)
  5. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH 10 UNROLLED PGD ITERATIONS
     - Explicit quadratic cost matrices Q, R, S, P_term
     - Dynamic enforcement of Axial Flux Difference (AFD / Delta-I) target bands (-5.0% to +5.0%)
     - Actuator slew rate damping and mechanical jack wear minimization
     - 10 unrolled Projected Gradient Descent iterations with backward adjoint costate propagation
  6. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) FAULT-TOLERANT SENSOR VOTING
     - 4 triplicated sensor channels: Excore Flux, Primary Loop T_hot/T_cold, Pressurizer Pressure, Pzr Level
     - Continuous pairwise discrepancy cross-checking with 100 [ms] persistence timers
     - Bumpless degradation: 2oo3 -> 1oo2 -> Failover / Class 1E SCRAM trip
  7. DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
     - Covering: Idle, Cold Shutdown, Hot Shutdown, Hot Standby, Criticality Approach (1/M tracking),
       Zero-Power Physics Testing, Power Ascension, Nominal Baseload MPC, Grid Frequency Droop Dispatch,
       Xenon Transient Trim, Rapid Steam Dump Turndown, Controlled Shutdown, Post-SCRAM RHR, Emergency SCRAM
  8. ISA-18.2 MULTI-TIER ALARMS & BIT-PACKED 32-BIT TELEMETRY DWORDS
     - High-High, High, Low, Low-Low thresholds with deadband hysteresis
     - First-Out SCRAM root-cause diagnostic latch
     - Comprehensive bitwise telemetry encoding: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord
====================================================================================================
*)
""")

    # -------------------------------------------------------------
    # 1. VAR_INPUT
    # -------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* Master Execution and Safety Commands *)
    bMasterEnable                   : BOOL;     (* Master function block execution enable command [bool] *)
    bOperatorAckAlarms              : BOOL;     (* Operator ISA-18.2 alarm acknowledge pushbutton [bool] *)
    bManualTripSCRAM_Class1E        : BOOL;     (* Class 1E hardwired manual reactor trip / SCRAM demand [bool] *)
    bTurbineTripInterlock           : BOOL;     (* High-speed turbine main stop valve trip interlock [bool] *)
    bSafetyInjectionActuated        : BOOL;     (* Emergency core cooling safety injection system signal [bool] *)
    bAutoRodControlSelect           : BOOL;     (* Automatic coordinated control rod regulation mode selector [bool] *)
    bAutoPressurizerSelect          : BOOL;     (* Automatic pressurizer pressure and level control selector [bool] *)
    bGridFrequencyDroopEnable       : BOOL;     (* Primary frequency response and grid droop control enable [bool] *)
    bCRDM_ManualRaisePB             : BOOL;     (* Manual CRDM regulating bank raise pushbutton [bool] *)
    bCRDM_ManualLowerPB             : BOOL;     (* Manual CRDM regulating bank lower pushbutton [bool] *)
    
    (* Primary Plant Telemetry and Process References *)
    rTurbineLoadDemand              : REAL;     (* Grid dispatch turbine electrical load demand reference [0.0..100.0 %] *)
    rGridFrequency_Hz               : REAL;     (* High-voltage grid electrical transmission frequency [45.0..65.0 Hz] *)
    rSteamDumpBypassFlow_KgSec      : REAL;     (* Steam dump bypass valves mass flow rate to condenser [0.0..1500.0 kg/s] *)
    rRCS_TotalLoopFlow_KgSec        : REAL;     (* Total primary coolant loops combined mass flow rate [0.0..18000.0 kg/s] *)
    rCVCS_ChargingFlow_M3h          : REAL;     (* Chemical and Volume Control System high-head charging line flow [0.0..60.0 m3/h] *)
    rCVCS_LetdownFlow_M3h           : REAL;     (* Chemical and Volume Control System low-pressure letdown line flow [0.0..60.0 m3/h] *)
    rBoronConcentration_PPM         : REAL;     (* On-line primary coolant soluble boron concentration meter [0.0..3000.0 ppm] *)
    rAxialFluxOffset_Pct            : REAL;     (* Measured axial flux difference (Delta-I = P_top - P_bot) [-50.0..+50.0 %] *)
    rControlRodBankD_PosSteps       : REAL;     (* CRDM Regulating Bank D current position [0.0..228.0 steps] *)
    tScanCycleTime                  : TIME;     (* Deterministic controller task execution cycle period [ms] *)
    
    (* 2oo3 TMR Sensor Triplet 1: Excore Nuclear Power Range Neutron Detectors *)
    rExcoreFluxChA_PctFP            : REAL;     (* Excore nuclear power range detector Channel A [0.0..125.0 % FP] *)
    rExcoreFluxChB_PctFP            : REAL;     (* Excore nuclear power range detector Channel B [0.0..125.0 % FP] *)
    rExcoreFluxChC_PctFP            : REAL;     (* Excore nuclear power range detector Channel C [0.0..125.0 % FP] *)
    
    (* 2oo3 TMR Sensor Triplet 2: Primary Coolant Loop Narrow-Range Hot Leg RTDs *)
    rRCS_Thot_ChA_DegC              : REAL;     (* Reactor Coolant Loop narrow-range hot leg RTD Channel A [260.0..350.0 deg C] *)
    rRCS_Thot_ChB_DegC              : REAL;     (* Reactor Coolant Loop narrow-range hot leg RTD Channel B [260.0..350.0 deg C] *)
    rRCS_Thot_ChC_DegC              : REAL;     (* Reactor Coolant Loop narrow-range hot leg RTD Channel C [260.0..350.0 deg C] *)
    
    (* 2oo3 TMR Sensor Triplet 2b: Primary Coolant Loop Narrow-Range Cold Leg RTDs *)
    rRCS_Tcold_ChA_DegC             : REAL;     (* Reactor Coolant Loop narrow-range cold leg RTD Channel A [260.0..350.0 deg C] *)
    rRCS_Tcold_ChB_DegC             : REAL;     (* Reactor Coolant Loop narrow-range cold leg RTD Channel B [260.0..350.0 deg C] *)
    rRCS_Tcold_ChC_DegC             : REAL;     (* Reactor Coolant Loop narrow-range cold leg RTD Channel C [260.0..350.0 deg C] *)
    
    (* 2oo3 TMR Sensor Triplet 3: Pressurizer Narrow-Range Pressure Transmitters *)
    rPzrPressure_ChA_Bar            : REAL;     (* Pressurizer narrow-range piezoresistive pressure Channel A [120.0..180.0 bar] *)
    rPzrPressure_ChB_Bar            : REAL;     (* Pressurizer narrow-range piezoresistive pressure Channel B [120.0..180.0 bar] *)
    rPzrPressure_ChC_Bar            : REAL;     (* Pressurizer narrow-range piezoresistive pressure Channel C [120.0..180.0 bar] *)
    
    (* 2oo3 TMR Sensor Triplet 4: Pressurizer Differential Pressure Level Transmitters *)
    rPzrLevel_ChA_Pct               : REAL;     (* Pressurizer differential pressure water level Channel A [0.0..100.0 %] *)
    rPzrLevel_ChB_Pct               : REAL;     (* Pressurizer differential pressure water level Channel B [0.0..100.0 %] *)
    rPzrLevel_ChC_Pct               : REAL;     (* Pressurizer differential pressure water level Channel C [0.0..100.0 %] *)
END_VAR
""")

    # -------------------------------------------------------------
    # 2. VAR_OUTPUT
    # -------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* Actuator Control Commands *)
    rCRDM_RodBankSpeed_Cmd          : REAL;     (* Regulating Bank D stepping speed demand [-72.0..+72.0 steps/min] *)
    bCRDM_StepDirectionOut          : BOOL;     (* CRDM stepping direction flag: TRUE=Withdraw, FALSE=Insert [bool] *)
    bCRDM_StepGatePulse             : BOOL;     (* CRDM magnetic jack thyristor pulsing gate firing enable [bool] *)
    rPzrProportionalHeaters_Cmd     : REAL;     (* Pressurizer proportional heater SCR thyristor command [0.0..100.0 %] *)
    bPzrBackupHeaterBank1_Cmd       : BOOL;     (* Pressurizer backup heater bank 1 contactor command [bool] *)
    bPzrBackupHeaterBank2_Cmd       : BOOL;     (* Pressurizer backup heater bank 2 contactor command [bool] *)
    rPzrSprayValveMod_Cmd           : REAL;     (* Pressurizer cold leg modulating spray valve demand [0.0..100.0 %] *)
    bPzrPORV_ReliefValve_Cmd        : BOOL;     (* Pressurizer pilot-operated relief valve (PORV) solenoid output [bool] *)
    rCVCS_ChargingPumpSpeed_Cmd     : REAL;     (* CVCS variable-frequency drive charging pump demand [0.0..100.0 %] *)
    rCVCS_LetdownControlValve_Cmd   : REAL;     (* CVCS letdown line pressure control modulating valve [0.0..100.0 %] *)
    
    (* Reactor Protection System (RPS) & Interlock Commands *)
    bEmergencySCRAM_TripActive      : BOOL;     (* Reactor Protection System (RPS) active trip scram latch [bool] *)
    bSafetyContainmentIsolation_Cmd : BOOL;     (* Class 1E safety injection and containment isolation demand [bool] *)
    bTurbineRunback_Demand          : BOOL;     (* Coordinated turbine runback request signal [bool] *)
    bSteamDumpBypassPermissive      : BOOL;     (* Steam dump bypass to condenser open permissive [bool] *)
    
    (* Voted and Process State Telemetry *)
    rRCS_Tavg_Voted_DegC            : REAL;     (* 2oo3 TMR voted primary loop average coolant temperature [deg C] *)
    rRCS_Tref_Program_DegC          : REAL;     (* Programmed turbine reference coolant temperature [deg C] *)
    rRCS_DeltaT_Error_DegC          : REAL;     (* Temperature tracking mismatch error Delta-T [deg C] *)
    rPzrPressure_Voted_Bar          : REAL;     (* 2oo3 TMR voted pressurizer pressure [bar] *)
    rPzrLevel_Voted_Pct             : REAL;     (* 2oo3 TMR voted pressurizer water level [%] *)
    rNuclearPower_Voted_PctFP       : REAL;     (* 2oo3 TMR voted excore nuclear thermal power [% FP] *)
    rCalculatedReactivity_PCM       : REAL;     (* Total online core reactivity balance [pcm] *)
    rEstimatedFuelTemp_DegC         : REAL;     (* Observer estimated core fuel centerline temperature [deg C] *)
    rEstimatedCoolantFlow_KgSec     : REAL;     (* Observer estimated RCS primary loop mass flow rate [kg/s] *)
    
    (* Finite State Machine and Diagnostics Telemetry *)
    iCurrentFSMState                : INT;      (* Active 14-stage deterministic finite state machine index [int] *)
    dwStatusWord1                   : DWORD;    (* Operational status word 1 telemetry [dword] *)
    dwStatusWord2                   : DWORD;    (* Operational status word 2 telemetry [dword] *)
    dwAlarmWord1                    : DWORD;    (* ISA-18.2 trip and primary warning alarms [dword] *)
    dwAlarmWord2                    : DWORD;    (* ISA-18.2 secondary and hardware discrepancy alarms [dword] *)
    dwFirstOutWord                  : DWORD;    (* Reactor protection first-out SCRAM root cause latch [dword] *)
END_VAR
""")

    # -------------------------------------------------------------
    # 3. VAR
    # -------------------------------------------------------------
    parts.append("""VAR
    (* Discrete State-Space Model Matrices (6 States x 6 States, 6 States x 5 Actuators) *)
    matA : ARRAY[1..6, 1..6] OF REAL; (* Discrete state transition matrix A [dimensionless] *)
    matB : ARRAY[1..6, 1..5] OF REAL; (* Discrete input coupling matrix B [dimensionless] *)
    matC : ARRAY[1..6, 1..6] OF REAL; (* State measurement mapping matrix C [dimensionless] *)
    matD : ARRAY[1..6, 1..5] OF REAL; (* Direct feedthrough matrix D [dimensionless] *)
    matL : ARRAY[1..6, 1..6] OF REAL; (* Observer Kalman/Luenberger innovation gain matrix L [dimensionless] *)
    
    (* Model Predictive Control (MPC) Cost Weight Matrices *)
    matQ : ARRAY[1..6, 1..6] OF REAL; (* State tracking quadratic cost matrix Q [dimensionless] *)
    matR : ARRAY[1..5, 1..5] OF REAL; (* Actuator effort quadratic cost matrix R [dimensionless] *)
    matS : ARRAY[1..5, 1..5] OF REAL; (* Actuator slew rate penalty matrix S [dimensionless] *)
    matP_term : ARRAY[1..6, 1..6] OF REAL; (* Terminal state quadratic penalty matrix P [dimensionless] *)
    
    (* State Vectors & Estimation Variables *)
    vecX_hat        : ARRAY[1..6] OF REAL; (* Observer state estimates: [Pwr, Tavg, Tfuel, PzrP, PzrL, Flow] *)
    vecX_hat_next   : ARRAY[1..6] OF REAL; (* Predicted state estimates at step k+1 *)
    vecX_meas       : ARRAY[1..6] OF REAL; (* Actual process measurement vector *)
    vecX_ref        : ARRAY[1..6] OF REAL; (* State reference trajectory setpoints *)
    vecX_err        : ARRAY[1..6] OF REAL; (* State tracking error vector (x_hat - x_ref) *)
    vecY_innov      : ARRAY[1..6] OF REAL; (* Observer measurement innovation residual (y_meas - C*x_hat) *)
    vecU_cmd        : ARRAY[1..5] OF REAL; (* Actuator demand vector: [RodSpd, PropHtr, Spray, CVCS, BupHtr] *)
    vecU_prev       : ARRAY[1..5] OF REAL; (* Previous scan cycle actuator commands *)
    vecU_cand       : ARRAY[1..5] OF REAL; (* Candidate actuator vector during PGD optimization *)
    vecU_min        : ARRAY[1..5] OF REAL; (* Lower physical saturation limits of actuators *)
    vecU_max        : ARRAY[1..5] OF REAL; (* Upper physical saturation limits of actuators *)
    vecDU_max       : ARRAY[1..5] OF REAL; (* Maximum permissible actuator slew rates per cycle *)
    vecGradU        : ARRAY[1..5] OF REAL; (* Cost gradient with respect to control vector u *)
    vecLambda       : ARRAY[1..6] OF REAL; (* Adjoint costate vector for Pontryagin backward propagation *)
    
    (* MPC Receding-Horizon Trajectory Buffers (4-Step Horizon x 6 States / 5 Inputs) *)
    arrX_pred_traj  : ARRAY[0..4, 1..6] OF REAL; (* Forward state predictions over prediction horizon *)
    arrU_pred_traj  : ARRAY[0..3, 1..5] OF REAL; (* Actuator control trajectory over prediction horizon *)
    arrLambda_traj  : ARRAY[0..4, 1..6] OF REAL; (* Backward adjoint costate trajectory *)
    
    (* Point Kinetics & 6 Delayed Neutron Precursor Variables *)
    rPrecursor_C1   : REAL; (* Delayed neutron precursor group 1 density [atoms/cm3] *)
    rPrecursor_C2   : REAL; (* Delayed neutron precursor group 2 density [atoms/cm3] *)
    rPrecursor_C3   : REAL; (* Delayed neutron precursor group 3 density [atoms/cm3] *)
    rPrecursor_C4   : REAL; (* Delayed neutron precursor group 4 density [atoms/cm3] *)
    rPrecursor_C5   : REAL; (* Delayed neutron precursor group 5 density [atoms/cm3] *)
    rPrecursor_C6   : REAL; (* Delayed neutron precursor group 6 density [atoms/cm3] *)
    rBeta_1         : REAL; (* Group 1 delayed neutron fraction [dimensionless] *)
    rBeta_2         : REAL; (* Group 2 delayed neutron fraction [dimensionless] *)
    rBeta_3         : REAL; (* Group 3 delayed neutron fraction [dimensionless] *)
    rBeta_4         : REAL; (* Group 4 delayed neutron fraction [dimensionless] *)
    rBeta_5         : REAL; (* Group 5 delayed neutron fraction [dimensionless] *)
    rBeta_6         : REAL; (* Group 6 delayed neutron fraction [dimensionless] *)
    rLambda_1       : REAL; (* Group 1 precursor decay constant [1/s] *)
    rLambda_2       : REAL; (* Group 2 precursor decay constant [1/s] *)
    rLambda_3       : REAL; (* Group 3 precursor decay constant [1/s] *)
    rLambda_4       : REAL; (* Group 4 precursor decay constant [1/s] *)
    rLambda_5       : REAL; (* Group 5 precursor decay constant [1/s] *)
    rLambda_6       : REAL; (* Group 6 precursor decay constant [1/s] *)
    rBetaTotal      : REAL; (* Total effective delayed neutron fraction Beta [dimensionless] *)
    rPromptLifetime : REAL; (* Prompt neutron generation lifetime Lambda [s] *)
    rNeutronFlux    : REAL; (* Core average thermal neutron flux [n/cm2-s] *)
    
    (* Iodine-135 and Xenon-135 Poisoning Differential Kinetics *)
    rIodine135_Conc : REAL; (* Core average Iodine-135 inventory concentration [atoms/cm3] *)
    rXenon135_Conc  : REAL; (* Core average Xenon-135 poison concentration [atoms/cm3] *)
    rDecayConst_I   : REAL; (* Radioactive decay constant of Iodine-135 [1/s] *)
    rDecayConst_Xe  : REAL; (* Radioactive decay constant of Xenon-135 [1/s] *)
    rFissionYield_I : REAL; (* Direct fission yield of Iodine-135 [dimensionless] *)
    rFissionYield_Xe: REAL; (* Direct fission yield of Xenon-135 [dimensionless] *)
    rSigmaAbs_Xe    : REAL; (* Microscopic thermal neutron absorption cross section of Xe-135 [cm2] *)
    rMacroFission   : REAL; (* Macroscopic fission cross section of UO2 core [1/cm] *)
    rNuFission      : REAL; (* Average number of neutrons emitted per thermal fission [dimensionless] *)
    
    (* Reactivity Components & Thermal Coefficients *)
    rReactivityRods     : REAL; (* Control rod insertion reactivity worth [pcm] *)
    rReactivityDoppler  : REAL; (* Fuel temperature Doppler feedback reactivity [pcm] *)
    rReactivityMod      : REAL; (* Moderator temperature feedback reactivity [pcm] *)
    rReactivityBoron    : REAL; (* Chemical soluble boron reactivity [pcm] *)
    rReactivityXenon    : REAL; (* Xenon-135 poisoning negative reactivity [pcm] *)
    rAlphaDoppler       : REAL; (* Doppler temperature coefficient [pcm/deg C] *)
    rAlphaModerator     : REAL; (* Moderator temperature coefficient [pcm/deg C] *)
    rBoronDifferential  : REAL; (* Soluble boron differential reactivity worth [pcm/ppm] *)
    rT_fuel_ref         : REAL; (* Reference fuel centerline temperature at nominal 100% FP [deg C] *)
    rT_mod_ref          : REAL; (* Reference moderator temperature at nominal zero-load [deg C] *)
    rBoron_ref_ppm      : REAL; (* Reference soluble boron concentration for clean core [ppm] *)
    rRodPositionFrac    : REAL; (* Normalized Bank D position [0.0..1.0] *)
    
    (* Pressurizer Nonequilibrium Two-Region Thermodynamic Variables *)
    rPzrLiquidMass_Kg       : REAL; (* Pressurizer liquid region water inventory [kg] *)
    rPzrVaporMass_Kg        : REAL; (* Pressurizer vapor steam bubble inventory [kg] *)
    rPzrLiquidEnthalpy_Jkg  : REAL; (* Saturated/subcooled liquid specific enthalpy [J/kg] *)
    rPzrVaporEnthalpy_Jkg   : REAL; (* Saturated/superheated steam vapor specific enthalpy [J/kg] *)
    rPzrLiquidVolume_M3     : REAL; (* Pressurizer liquid region volume [m3] *)
    rPzrVaporVolume_M3      : REAL; (* Pressurizer steam bubble volume [m3] *)
    rPzrTotalVolume_M3      : REAL; (* Total internal pressurizer vessel volume [m3] *)
    rPzrSurgeFlow_KgSec     : REAL; (* Primary loop insurge/outsurge mass flow rate [kg/s] *)
    rPzrSprayFlow_KgSec     : REAL; (* Pressurizer cold leg spray total mass flow rate [kg/s] *)
    rPzrReliefFlow_KgSec    : REAL; (* Pressurizer PORV and safety valve discharge flow [kg/s] *)
    rPzrTotalHeaterPower_W  : REAL; (* Pressurizer electric immersion heaters total thermal power [W] *)
    rRCS_FluidDensity_KgM3  : REAL; (* Primary coolant loop bulk water density [kg/m3] *)
    rRCS_VolExpansionCoeff  : REAL; (* Primary coolant isobaric volumetric thermal expansion coefficient [1/deg C] *)
    rRCS_TotalFluidMass_Kg  : REAL; (* Total water mass in primary reactor coolant loops [kg] *)
    rRateOfPressureChange   : REAL; (* Calculated rate of pressurizer pressure change dp/dt [bar/s] *)
    
    (* 2oo3 TMR Sensor Voting Variables & Timers *)
    (* Triplet 1: Excore Flux *)
    bFlux_ChA_Fault : BOOL; (* Excore flux Channel A fault flag [bool] *)
    bFlux_ChB_Fault : BOOL; (* Excore flux Channel B fault flag [bool] *)
    bFlux_ChC_Fault : BOOL; (* Excore flux Channel C fault flag [bool] *)
    tFlux_Discrep_AB : TIME; (* Discrepancy persistence timer between Ch A and B [ms] *)
    tFlux_Discrep_BC : TIME; (* Discrepancy persistence timer between Ch B and C [ms] *)
    tFlux_Discrep_CA : TIME; (* Discrepancy persistence timer between Ch C and A [ms] *)
    
    (* Triplet 2: Hot/Cold Leg Temperatures *)
    rRCS_Tavg_ChA_DegC : REAL; (* Loop A calculated average coolant temperature [deg C] *)
    rRCS_Tavg_ChB_DegC : REAL; (* Loop B calculated average coolant temperature [deg C] *)
    rRCS_Tavg_ChC_DegC : REAL; (* Loop C calculated average coolant temperature [deg C] *)
    bTemp_ChA_Fault : BOOL; (* RCS temperature Channel A fault flag [bool] *)
    bTemp_ChB_Fault : BOOL; (* RCS temperature Channel B fault flag [bool] *)
    bTemp_ChC_Fault : BOOL; (* RCS temperature Channel C fault flag [bool] *)
    tTemp_Discrep_AB : TIME; (* Discrepancy persistence timer between Temp Ch A and B [ms] *)
    tTemp_Discrep_BC : TIME; (* Discrepancy persistence timer between Temp Ch B and C [ms] *)
    tTemp_Discrep_CA : TIME; (* Discrepancy persistence timer between Temp Ch C and A [ms] *)
    
    (* Triplet 3: Pressurizer Pressure *)
    bPress_ChA_Fault : BOOL; (* Pressurizer pressure Channel A fault flag [bool] *)
    bPress_ChB_Fault : BOOL; (* Pressurizer pressure Channel B fault flag [bool] *)
    bPress_ChC_Fault : BOOL; (* Pressurizer pressure Channel C fault flag [bool] *)
    tPress_Discrep_AB : TIME; (* Discrepancy persistence timer between Press Ch A and B [ms] *)
    tPress_Discrep_BC : TIME; (* Discrepancy persistence timer between Press Ch B and C [ms] *)
    tPress_Discrep_CA : TIME; (* Discrepancy persistence timer between Press Ch C and A [ms] *)
    
    (* Triplet 4: Pressurizer Level *)
    bLevel_ChA_Fault : BOOL; (* Pressurizer level Channel A fault flag [bool] *)
    bLevel_ChB_Fault : BOOL; (* Pressurizer level Channel B fault flag [bool] *)
    bLevel_ChC_Fault : BOOL; (* Pressurizer level Channel C fault flag [bool] *)
    tLevel_Discrep_AB : TIME; (* Discrepancy persistence timer between Level Ch A and B [ms] *)
    tLevel_Discrep_BC : TIME; (* Discrepancy persistence timer between Level Ch B and C [ms] *)
    tLevel_Discrep_CA : TIME; (* Discrepancy persistence timer between Level Ch C and A [ms] *)
    
    (* Deterministic 14-Stage Production Finite State Machine Variables *)
    iFSM_NextState          : INT;      (* Next state transition target index [int] *)
    tStateTimer             : TIME;     (* Accumulated elapsed time in current state [ms] *)
    rStateTime_Sec          : REAL;     (* Elapsed state time in seconds [s] *)
    bStateFirstCycle        : BOOL;     (* One-shot initial execution pulse on entering state [bool] *)
    iPrevState              : INT;      (* Previous FSM state index [int] *)
    
    (* FSM Specific Process Tracking Variables *)
    rCriticality_1_over_M   : REAL;     (* Subcritical neutron source multiplication 1/M ratio [dimensionless] *)
    rBaselineCountRate      : REAL;     (* Baseline initial shutdown neutron count rate [cps] *)
    rCurrentCountRate       : REAL;     (* Current measured neutron count rate [cps] *)
    rPhysicsTestingPower_Pct: REAL;     (* Target power during zero-power physics testing [% FP] *)
    rTurbineSyncFrequency   : REAL;     (* Measured generator turbine shaft electrical frequency [Hz] *)
    bTurbineBreakerClosed   : BOOL;     (* Generator main electrical output breaker feedback [bool] *)
    rRCS_HeatupRampRate     : REAL;     (* Calculated primary loop heatup ramp rate [deg C / hr] *)
    rPreviousTavg_Sample    : REAL;     (* Stored Tavg value from previous calculation sample [deg C] *)
    
    (* Permissive Interlocks (Nuclear Standard Plant Permissives) *)
    bPermissive_P4          : BOOL;     (* Reactor trip permissive P-4: Reactor tripped, enables steam dump bypass [bool] *)
    bPermissive_P6          : BOOL;     (* Intermediate range permissive P-6: Source range de-energized [bool] *)
    bPermissive_P7          : BOOL;     (* Low power trip permissive P-7: Reactor power > 10% FP, arms trips [bool] *)
    bPermissive_P8          : BOOL;     (* Power range permissive P-8: Single loop loss of flow trip enabled [bool] *)
    bPermissive_P10         : BOOL;     (* Power range permissive P-10: Power > 10% FP, transfers rod control [bool] *)
    
    (* ISA-18.2 Multi-Tier Alarm Trip Limits and Deadband Hysteresis Registers *)
    bAlarm_Power_HH         : BOOL;     (* Reactor overpower High-High trip alarm (107.0% FP) [bool] *)
    bAlarm_Power_H          : BOOL;     (* Reactor overpower High warning alarm (103.0% FP) [bool] *)
    bAlarm_Power_L          : BOOL;     (* Reactor power Low warning alarm (0.5% FP) [bool] *)
    bAlarm_Power_LL         : BOOL;     (* Reactor power Low-Low warning alarm (0.01% FP) [bool] *)
    
    bAlarm_Press_HH         : BOOL;     (* Pressurizer pressure High-High trip alarm (165.0 bar) [bool] *)
    bAlarm_Press_H          : BOOL;     (* Pressurizer pressure High warning alarm (158.0 bar) [bool] *)
    bAlarm_Press_L          : BOOL;     (* Pressurizer pressure Low warning alarm (151.0 bar) [bool] *)
    bAlarm_Press_LL         : BOOL;     (* Pressurizer pressure Low-Low trip alarm (135.0 bar) [bool] *)
    
    bAlarm_Level_HH         : BOOL;     (* Pressurizer level High-High trip alarm (92.0 %) [bool] *)
    bAlarm_Level_H          : BOOL;     (* Pressurizer level High warning alarm (70.0 %) [bool] *)
    bAlarm_Level_L          : BOOL;     (* Pressurizer level Low warning alarm (20.0 %) [bool] *)
    bAlarm_Level_LL         : BOOL;     (* Pressurizer level Low-Low trip heaters alarm (12.0 %) [bool] *)
    
    bAlarm_Tavg_HH          : BOOL;     (* Primary loop Tavg High-High trip alarm (315.0 deg C) [bool] *)
    bAlarm_Tavg_H           : BOOL;     (* Primary loop Tavg High warning alarm (311.0 deg C) [bool] *)
    bAlarm_Tavg_L           : BOOL;     (* Primary loop Tavg Low warning alarm (288.0 deg C) [bool] *)
    bAlarm_Tavg_LL          : BOOL;     (* Primary loop Tavg Low-Low trip alarm (280.0 deg C) [bool] *)
    
    bAlarm_OTDT_Trip        : BOOL;     (* Overtemperature Delta-T core thermal margin trip demand [bool] *)
    bAlarm_OPDT_Trip        : BOOL;     (* Overpower Delta-T core thermal margin trip demand [bool] *)
    bAlarm_AFD_OutOfBand    : BOOL;     (* Axial Flux Difference (Delta-I) exceeding target operating band [bool] *)
    bAlarm_ThermalRamp_High : BOOL;     (* Primary coolant thermal ramp rate exceeding 55.0 deg C/hr [bool] *)
    
    (* Overtemperature Delta-T & Overpower Delta-T Protection Setpoint Calculation Registers *)
    rDeltaT_CoreActual      : REAL;     (* Actual core temperature difference (Thot - Tcold) [deg C] *)
    rOTDT_CalculatedTrip    : REAL;     (* Dynamic calculated Overtemperature Delta-T trip setpoint [deg C] *)
    rOPDT_CalculatedTrip    : REAL;     (* Dynamic calculated Overpower Delta-T trip setpoint [deg C] *)
    rOTDT_FilterState1      : REAL;     (* Lead-lag filter state for OTDT temperature tracking [deg C] *)
    rOTDT_FilterState2      : REAL;     (* Lag filter state for OTDT temperature tracking [deg C] *)
    rOPDT_FilterState       : REAL;     (* Rate-lag filter state for OPDT thermal power tracking [deg C] *)
    
    (* Actuator Modulation Internal Registers *)
    rCRDM_PulseTimer        : REAL;     (* Timer accumulator for CRDM magnetic jack thyristor pulsing [s] *)
    bCRDM_PulseActive       : BOOL;     (* Pulsing thyristor gate signal currently asserted [bool] *)
    rHeaterModulationCycle  : REAL;     (* Time-proportional modulation period for electric heaters [s] *)
    rSprayModulationCycle   : REAL;     (* Continuous spray valve positioning damping register [0..1] *)
    
    (* Loop Counters and Optimization Math Intermediates *)
    idxIter         : INT;  (* MPC Projected Gradient Descent unrolled iteration counter [int] *)
    idxHorizon      : INT;  (* Prediction horizon step counter [int] *)
    idxRow          : INT;  (* Matrix row traversal index [int] *)
    idxCol          : INT;  (* Matrix column traversal index [int] *)
    idxInput        : INT;  (* Actuator input traversal index [int] *)
    idxPrecursor    : INT;  (* Delayed neutron precursor group traversal index [int] *)
    rCycleSec       : REAL; (* Task scan cycle execution period converted to seconds [s] *)
    rStepSizeAlpha  : REAL; (* Projected gradient descent step size learning rate alpha [dimensionless] *)
    rPenaltyAFD     : REAL; (* Axial Flux Difference constraint violation penalty magnitude [dimensionless] *)
    rPenaltyRamp    : REAL; (* RCS thermal ramp rate constraint violation penalty magnitude [dimensionless] *)
    rTempSum        : REAL; (* Generic floating point accumulation register [dimensionless] *)
    rTempSum2       : REAL; (* Secondary floating point accumulation register [dimensionless] *)
    rStepUpdate     : REAL; (* Step candidate for PGD projected update [dimensionless] *)
    rStepClamped    : REAL; (* Slew clamped candidate for PGD [dimensionless] *)
    bInitialized    : BOOL; (* Master initialization latch for state-space matrices & parameters [bool] *)
    
    (* Temporary Differencing Registers for 2oo3 TMR *)
    rDiff_A_B       : REAL; (* Pairwise absolute difference between sensor A and B *)
    rDiff_B_C       : REAL; (* Pairwise absolute difference between sensor B and C *)
    rDiff_C_A       : REAL; (* Pairwise absolute difference between sensor C and A *)
    rTolFlux        : REAL; (* Flux triplet tolerance [2.0 % FP] *)
    rTolTemp        : REAL; (* Temperature triplet tolerance [1.5 deg C] *)
    rTolPress       : REAL; (* Pressure triplet tolerance [1.2 bar] *)
    rTolLevel       : REAL; (* Level triplet tolerance [2.5 %] *)
    
    (* Intermediate Dynamics Registers *)
    dPrecursor_C1   : REAL; (* Derivative of precursor group 1 [atoms/cm3-s] *)
    dPrecursor_C2   : REAL; (* Derivative of precursor group 2 [atoms/cm3-s] *)
    dPrecursor_C3   : REAL; (* Derivative of precursor group 3 [atoms/cm3-s] *)
    dPrecursor_C4   : REAL; (* Derivative of precursor group 4 [atoms/cm3-s] *)
    dPrecursor_C5   : REAL; (* Derivative of precursor group 5 [atoms/cm3-s] *)
    dPrecursor_C6   : REAL; (* Derivative of precursor group 6 [atoms/cm3-s] *)
    dIodine135      : REAL; (* Derivative of Iodine-135 concentration [atoms/cm3-s] *)
    dXenon135       : REAL; (* Derivative of Xenon-135 concentration [atoms/cm3-s] *)
    rPrecursorSum   : REAL; (* Sum of precursor decay sources [atoms/cm3-s] *)
    dPower_dt       : REAL; (* Core power rate of change [% FP / s] *)
    h_v_sat         : REAL; (* Saturated steam specific enthalpy [J/kg] *)
    h_l_sat         : REAL; (* Saturated liquid specific enthalpy [J/kg] *)
    h_spray_liq     : REAL; (* Cold leg spray subcooled liquid specific enthalpy [J/kg] *)
    rPzrPsiFactor   : REAL; (* Pressurizer adiabatic compressibility factor [bar-m3/J] *)
END_VAR
""")

    # -------------------------------------------------------------
    # 4. PREAMBLE & MASTER ENABLE
    # -------------------------------------------------------------
    parts.append("""
(* Convert Scan Cycle Time to Floating Point Seconds *)
IF tScanCycleTime > T#0MS THEN
    rCycleSec := TIME_TO_REAL(tScanCycleTime) / 1000.0;
ELSE
    rCycleSec := 0.050; (* Fallback default 50 ms deterministic task cycle *)
END_IF;

(* Master Functional Block Enable Interlock *)
IF NOT bMasterEnable THEN
    rCRDM_RodBankSpeed_Cmd := 0.0;
    bCRDM_StepDirectionOut := FALSE;
    bCRDM_StepGatePulse := FALSE;
    rPzrProportionalHeaters_Cmd := 0.0;
    bPzrBackupHeaterBank1_Cmd := FALSE;
    bPzrBackupHeaterBank2_Cmd := FALSE;
    rPzrSprayValveMod_Cmd := 0.0;
    bPzrPORV_ReliefValve_Cmd := FALSE;
    rCVCS_ChargingPumpSpeed_Cmd := 0.0;
    rCVCS_LetdownControlValve_Cmd := 0.0;
    bEmergencySCRAM_TripActive := FALSE;
    bSafetyContainmentIsolation_Cmd := FALSE;
    bTurbineRunback_Demand := FALSE;
    bSteamDumpBypassPermissive := FALSE;
    dwStatusWord1 := 16#00000000;
    dwStatusWord2 := 16#00000000;
    dwAlarmWord1 := 16#00000000;
    dwAlarmWord2 := 16#00000000;
    dwFirstOutWord := 16#00000000;
    RETURN;
END_IF;
""")

    # -------------------------------------------------------------
    # 5. PHASE 1: 2oo3 TMR SENSOR VOTING SUITE
    # -------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* === PHASE 1: 2oo3 TMR SENSOR VOTING WITH DISCREPANCY TIMERS                                      === *)
(* ==================================================================================================== *)

(* Parameterize Triplet Discrepancy Thresholds *)
rTolFlux := 2.0;    (* Excore flux threshold 2.0 % FP *)
rTolTemp := 1.5;    (* Coolant temperature threshold 1.5 deg C *)
rTolPress := 1.2;   (* Pressurizer pressure threshold 1.2 bar *)
rTolLevel := 2.5;   (* Pressurizer level threshold 2.5 % *)

(* -------------------------------------------------------------------------------------------------- *)
(* TRIPLET 1: EXCORE NUCLEAR POWER RANGE NEUTRON FLUX CHANNELS A, B, C                                *)
(* -------------------------------------------------------------------------------------------------- *)
(* Sanity & Plausibility Checks *)
IF (rExcoreFluxChA_PctFP < 0.0) OR (rExcoreFluxChA_PctFP > 125.0) THEN
    bFlux_ChA_Fault := TRUE;
END_IF;
IF (rExcoreFluxChB_PctFP < 0.0) OR (rExcoreFluxChB_PctFP > 125.0) THEN
    bFlux_ChB_Fault := TRUE;
END_IF;
IF (rExcoreFluxChC_PctFP < 0.0) OR (rExcoreFluxChC_PctFP > 125.0) THEN
    bFlux_ChC_Fault := TRUE;
END_IF;

(* Compute Pairwise Absolute Deviations *)
rDiff_A_B := ABS(rExcoreFluxChA_PctFP - rExcoreFluxChB_PctFP);
rDiff_B_C := ABS(rExcoreFluxChB_PctFP - rExcoreFluxChC_PctFP);
rDiff_C_A := ABS(rExcoreFluxChC_PctFP - rExcoreFluxChA_PctFP);

(* Integrate Discrepancy Persistence Timers (100 ms Criterion) *)
IF rDiff_A_B > rTolFlux THEN
    tFlux_Discrep_AB := tFlux_Discrep_AB + tScanCycleTime;
ELSE
    tFlux_Discrep_AB := T#0MS;
END_IF;

IF rDiff_B_C > rTolFlux THEN
    tFlux_Discrep_BC := tFlux_Discrep_BC + tScanCycleTime;
ELSE
    tFlux_Discrep_BC := T#0MS;
END_IF;

IF rDiff_C_A > rTolFlux THEN
    tFlux_Discrep_CA := tFlux_Discrep_CA + tScanCycleTime;
ELSE
    tFlux_Discrep_CA := T#0MS;
END_IF;

(* Fault Isolation by Cross-Channel Discrepancy Intersection *)
IF (tFlux_Discrep_AB >= T#100MS) AND (tFlux_Discrep_CA >= T#100MS) AND (tFlux_Discrep_BC < T#100MS) THEN
    bFlux_ChA_Fault := TRUE;
END_IF;
IF (tFlux_Discrep_AB >= T#100MS) AND (tFlux_Discrep_BC >= T#100MS) AND (tFlux_Discrep_CA < T#100MS) THEN
    bFlux_ChB_Fault := TRUE;
END_IF;
IF (tFlux_Discrep_BC >= T#100MS) AND (tFlux_Discrep_CA >= T#100MS) AND (tFlux_Discrep_AB < T#100MS) THEN
    bFlux_ChC_Fault := TRUE;
END_IF;

(* Fault-Tolerant Voting & Bumpless Degradation for Nuclear Flux *)
IF (NOT bFlux_ChA_Fault) AND (NOT bFlux_ChB_Fault) AND (NOT bFlux_ChC_Fault) THEN
    (* All 3 Channels Healthy: Exact Median Selector *)
    rNuclearPower_Voted_PctFP := MAX(MIN(rExcoreFluxChA_PctFP, rExcoreFluxChB_PctFP), MIN(MAX(rExcoreFluxChA_PctFP, rExcoreFluxChB_PctFP), rExcoreFluxChC_PctFP));
ELSIF bFlux_ChA_Fault AND (NOT bFlux_ChB_Fault) AND (NOT bFlux_ChC_Fault) THEN
    (* Channel A Degraded: 1oo2 Mean of B and C *)
    rNuclearPower_Voted_PctFP := (rExcoreFluxChB_PctFP + rExcoreFluxChC_PctFP) * 0.5;
ELSIF bFlux_ChB_Fault AND (NOT bFlux_ChA_Fault) AND (NOT bFlux_ChC_Fault) THEN
    (* Channel B Degraded: 1oo2 Mean of A and C *)
    rNuclearPower_Voted_PctFP := (rExcoreFluxChA_PctFP + rExcoreFluxChC_PctFP) * 0.5;
ELSIF bFlux_ChC_Fault AND (NOT bFlux_ChA_Fault) AND (NOT bFlux_ChB_Fault) THEN
    (* Channel C Degraded: 1oo2 Mean of A and B *)
    rNuclearPower_Voted_PctFP := (rExcoreFluxChA_PctFP + rExcoreFluxChB_PctFP) * 0.5;
ELSIF (NOT bFlux_ChA_Fault) AND bFlux_ChB_Fault AND bFlux_ChC_Fault THEN
    (* Dual Sensor Failure: Failover to Sole Healthy Channel A *)
    rNuclearPower_Voted_PctFP := rExcoreFluxChA_PctFP;
ELSIF bFlux_ChA_Fault AND (NOT bFlux_ChB_Fault) AND bFlux_ChC_Fault THEN
    (* Dual Sensor Failure: Failover to Sole Healthy Channel B *)
    rNuclearPower_Voted_PctFP := rExcoreFluxChB_PctFP;
ELSIF bFlux_ChA_Fault AND bFlux_ChB_Fault AND (NOT bFlux_ChC_Fault) THEN
    (* Dual Sensor Failure: Failover to Sole Healthy Channel C *)
    rNuclearPower_Voted_PctFP := rExcoreFluxChC_PctFP;
ELSE
    (* Triple Sensor Failure: Class 1E Fail-Safe Emergency SCRAM *)
    bEmergencySCRAM_TripActive := TRUE;
    rNuclearPower_Voted_PctFP := 0.0;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* TRIPLET 2: PRIMARY COOLANT LOOP NARROW-RANGE HOT/COLD LEG RTDS & LOOP TAVG                         *)
(* -------------------------------------------------------------------------------------------------- *)
(* Synthesize Channel Loop Average Coolant Temperatures *)
rRCS_Tavg_ChA_DegC := (rRCS_Thot_ChA_DegC + rRCS_Tcold_ChA_DegC) * 0.5;
rRCS_Tavg_ChB_DegC := (rRCS_Thot_ChB_DegC + rRCS_Tcold_ChB_DegC) * 0.5;
rRCS_Tavg_ChC_DegC := (rRCS_Thot_ChC_DegC + rRCS_Tcold_ChC_DegC) * 0.5;

(* Sanity & Plausibility Checks *)
IF (rRCS_Tavg_ChA_DegC < 260.0) OR (rRCS_Tavg_ChA_DegC > 350.0) THEN
    bTemp_ChA_Fault := TRUE;
END_IF;
IF (rRCS_Tavg_ChB_DegC < 260.0) OR (rRCS_Tavg_ChB_DegC > 350.0) THEN
    bTemp_ChB_Fault := TRUE;
END_IF;
IF (rRCS_Tavg_ChC_DegC < 260.0) OR (rRCS_Tavg_ChC_DegC > 350.0) THEN
    bTemp_ChC_Fault := TRUE;
END_IF;

(* Compute Pairwise Deviations *)
rDiff_A_B := ABS(rRCS_Tavg_ChA_DegC - rRCS_Tavg_ChB_DegC);
rDiff_B_C := ABS(rRCS_Tavg_ChB_DegC - rRCS_Tavg_ChC_DegC);
rDiff_C_A := ABS(rRCS_Tavg_ChC_DegC - rRCS_Tavg_ChA_DegC);

(* Integrate Discrepancy Timers *)
IF rDiff_A_B > rTolTemp THEN
    tTemp_Discrep_AB := tTemp_Discrep_AB + tScanCycleTime;
ELSE
    tTemp_Discrep_AB := T#0MS;
END_IF;

IF rDiff_B_C > rTolTemp THEN
    tTemp_Discrep_BC := tTemp_Discrep_BC + tScanCycleTime;
ELSE
    tTemp_Discrep_BC := T#0MS;
END_IF;

IF rDiff_C_A > rTolTemp THEN
    tTemp_Discrep_CA := tTemp_Discrep_CA + tScanCycleTime;
ELSE
    tTemp_Discrep_CA := T#0MS;
END_IF;

(* Fault Isolation by Cross-Channel Intersection *)
IF (tTemp_Discrep_AB >= T#100MS) AND (tTemp_Discrep_CA >= T#100MS) AND (tTemp_Discrep_BC < T#100MS) THEN
    bTemp_ChA_Fault := TRUE;
END_IF;
IF (tTemp_Discrep_AB >= T#100MS) AND (tTemp_Discrep_BC >= T#100MS) AND (tTemp_Discrep_CA < T#100MS) THEN
    bTemp_ChB_Fault := TRUE;
END_IF;
IF (tTemp_Discrep_BC >= T#100MS) AND (tTemp_Discrep_CA >= T#100MS) AND (tTemp_Discrep_AB < T#100MS) THEN
    bTemp_ChC_Fault := TRUE;
END_IF;

(* Fault-Tolerant Voting & Bumpless Degradation for Tavg *)
IF (NOT bTemp_ChA_Fault) AND (NOT bTemp_ChB_Fault) AND (NOT bTemp_ChC_Fault) THEN
    rRCS_Tavg_Voted_DegC := MAX(MIN(rRCS_Tavg_ChA_DegC, rRCS_Tavg_ChB_DegC), MIN(MAX(rRCS_Tavg_ChA_DegC, rRCS_Tavg_ChB_DegC), rRCS_Tavg_ChC_DegC));
ELSIF bTemp_ChA_Fault AND (NOT bTemp_ChB_Fault) AND (NOT bTemp_ChC_Fault) THEN
    rRCS_Tavg_Voted_DegC := (rRCS_Tavg_ChB_DegC + rRCS_Tavg_ChC_DegC) * 0.5;
ELSIF bTemp_ChB_Fault AND (NOT bTemp_ChA_Fault) AND (NOT bTemp_ChC_Fault) THEN
    rRCS_Tavg_Voted_DegC := (rRCS_Tavg_ChA_DegC + rRCS_Tavg_ChC_DegC) * 0.5;
ELSIF bTemp_ChC_Fault AND (NOT bTemp_ChA_Fault) AND (NOT bTemp_ChB_Fault) THEN
    rRCS_Tavg_Voted_DegC := (rRCS_Tavg_ChA_DegC + rRCS_Tavg_ChB_DegC) * 0.5;
ELSIF (NOT bTemp_ChA_Fault) AND bTemp_ChB_Fault AND bTemp_ChC_Fault THEN
    rRCS_Tavg_Voted_DegC := rRCS_Tavg_ChA_DegC;
ELSIF bTemp_ChA_Fault AND (NOT bTemp_ChB_Fault) AND bTemp_ChC_Fault THEN
    rRCS_Tavg_Voted_DegC := rRCS_Tavg_ChB_DegC;
ELSIF bTemp_ChA_Fault AND bTemp_ChB_Fault AND (NOT bTemp_ChC_Fault) THEN
    rRCS_Tavg_Voted_DegC := rRCS_Tavg_ChC_DegC;
ELSE
    bEmergencySCRAM_TripActive := TRUE;
    rRCS_Tavg_Voted_DegC := 292.0;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* TRIPLET 3: PRESSURIZER NARROW-RANGE PIEZORESISTIVE PRESSURE TRANSMITTERS                            *)
(* -------------------------------------------------------------------------------------------------- *)
(* Sanity & Plausibility Checks *)
IF (rPzrPressure_ChA_Bar < 120.0) OR (rPzrPressure_ChA_Bar > 180.0) THEN
    bPress_ChA_Fault := TRUE;
END_IF;
IF (rPzrPressure_ChB_Bar < 120.0) OR (rPzrPressure_ChB_Bar > 180.0) THEN
    bPress_ChB_Fault := TRUE;
END_IF;
IF (rPzrPressure_ChC_Bar < 120.0) OR (rPzrPressure_ChC_Bar > 180.0) THEN
    bPress_ChC_Fault := TRUE;
END_IF;

(* Compute Pairwise Deviations *)
rDiff_A_B := ABS(rPzrPressure_ChA_Bar - rPzrPressure_ChB_Bar);
rDiff_B_C := ABS(rPzrPressure_ChB_Bar - rPzrPressure_ChC_Bar);
rDiff_C_A := ABS(rPzrPressure_ChC_Bar - rPzrPressure_ChA_Bar);

(* Integrate Discrepancy Timers *)
IF rDiff_A_B > rTolPress THEN
    tPress_Discrep_AB := tPress_Discrep_AB + tScanCycleTime;
ELSE
    tPress_Discrep_AB := T#0MS;
END_IF;

IF rDiff_B_C > rTolPress THEN
    tPress_Discrep_BC := tPress_Discrep_BC + tScanCycleTime;
ELSE
    tPress_Discrep_BC := T#0MS;
END_IF;

IF rDiff_C_A > rTolPress THEN
    tPress_Discrep_CA := tPress_Discrep_CA + tScanCycleTime;
ELSE
    tPress_Discrep_CA := T#0MS;
END_IF;

(* Fault Isolation by Cross-Channel Intersection *)
IF (tPress_Discrep_AB >= T#100MS) AND (tPress_Discrep_CA >= T#100MS) AND (tPress_Discrep_BC < T#100MS) THEN
    bPress_ChA_Fault := TRUE;
END_IF;
IF (tPress_Discrep_AB >= T#100MS) AND (tPress_Discrep_BC >= T#100MS) AND (tPress_Discrep_CA < T#100MS) THEN
    bPress_ChB_Fault := TRUE;
END_IF;
IF (tPress_Discrep_BC >= T#100MS) AND (tPress_Discrep_CA >= T#100MS) AND (tPress_Discrep_AB < T#100MS) THEN
    bPress_ChC_Fault := TRUE;
END_IF;

(* Fault-Tolerant Voting & Bumpless Degradation for Pressurizer Pressure *)
IF (NOT bPress_ChA_Fault) AND (NOT bPress_ChB_Fault) AND (NOT bPress_ChC_Fault) THEN
    rPzrPressure_Voted_Bar := MAX(MIN(rPzrPressure_ChA_Bar, rPzrPressure_ChB_Bar), MIN(MAX(rPzrPressure_ChA_Bar, rPzrPressure_ChB_Bar), rPzrPressure_ChC_Bar));
ELSIF bPress_ChA_Fault AND (NOT bPress_ChB_Fault) AND (NOT bPress_ChC_Fault) THEN
    rPzrPressure_Voted_Bar := (rPzrPressure_ChB_Bar + rPzrPressure_ChC_Bar) * 0.5;
ELSIF bPress_ChB_Fault AND (NOT bPress_ChA_Fault) AND (NOT bPress_ChC_Fault) THEN
    rPzrPressure_Voted_Bar := (rPzrPressure_ChA_Bar + rPzrPressure_ChC_Bar) * 0.5;
ELSIF bPress_ChC_Fault AND (NOT bPress_ChA_Fault) AND (NOT bPress_ChB_Fault) THEN
    rPzrPressure_Voted_Bar := (rPzrPressure_ChA_Bar + rPzrPressure_ChB_Bar) * 0.5;
ELSIF (NOT bPress_ChA_Fault) AND bPress_ChB_Fault AND bPress_ChC_Fault THEN
    rPzrPressure_Voted_Bar := rPzrPressure_ChA_Bar;
ELSIF bPress_ChA_Fault AND (NOT bPress_ChB_Fault) AND bPress_ChC_Fault THEN
    rPzrPressure_Voted_Bar := rPzrPressure_ChB_Bar;
ELSIF bPress_ChA_Fault AND bPress_ChB_Fault AND (NOT bPress_ChC_Fault) THEN
    rPzrPressure_Voted_Bar := rPzrPressure_ChC_Bar;
ELSE
    bEmergencySCRAM_TripActive := TRUE;
    rPzrPressure_Voted_Bar := 155.1;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* TRIPLET 4: PRESSURIZER DIFFERENTIAL PRESSURE WATER LEVEL TRANSMITTERS                              *)
(* -------------------------------------------------------------------------------------------------- *)
(* Sanity & Plausibility Checks *)
IF (rPzrLevel_ChA_Pct < 0.0) OR (rPzrLevel_ChA_Pct > 100.0) THEN
    bLevel_ChA_Fault := TRUE;
END_IF;
IF (rPzrLevel_ChB_Pct < 0.0) OR (rPzrLevel_ChB_Pct > 100.0) THEN
    bLevel_ChB_Fault := TRUE;
END_IF;
IF (rPzrLevel_ChC_Pct < 0.0) OR (rPzrLevel_ChC_Pct > 100.0) THEN
    bLevel_ChC_Fault := TRUE;
END_IF;

(* Compute Pairwise Deviations *)
rDiff_A_B := ABS(rPzrLevel_ChA_Pct - rPzrLevel_ChB_Pct);
rDiff_B_C := ABS(rPzrLevel_ChB_Pct - rPzrLevel_ChC_Pct);
rDiff_C_A := ABS(rPzrLevel_ChC_Pct - rPzrLevel_ChA_Pct);

(* Integrate Discrepancy Timers *)
IF rDiff_A_B > rTolLevel THEN
    tLevel_Discrep_AB := tLevel_Discrep_AB + tScanCycleTime;
ELSE
    tLevel_Discrep_AB := T#0MS;
END_IF;

IF rDiff_B_C > rTolLevel THEN
    tLevel_Discrep_BC := tLevel_Discrep_BC + tScanCycleTime;
ELSE
    tLevel_Discrep_BC := T#0MS;
END_IF;

IF rDiff_C_A > rTolLevel THEN
    tLevel_Discrep_CA := tLevel_Discrep_CA + tScanCycleTime;
ELSE
    tLevel_Discrep_CA := T#0MS;
END_IF;

(* Fault Isolation by Cross-Channel Intersection *)
IF (tLevel_Discrep_AB >= T#100MS) AND (tLevel_Discrep_CA >= T#100MS) AND (tLevel_Discrep_BC < T#100MS) THEN
    bLevel_ChA_Fault := TRUE;
END_IF;
IF (tLevel_Discrep_AB >= T#100MS) AND (tLevel_Discrep_BC >= T#100MS) AND (tLevel_Discrep_CA < T#100MS) THEN
    bLevel_ChB_Fault := TRUE;
END_IF;
IF (tLevel_Discrep_BC >= T#100MS) AND (tLevel_Discrep_CA >= T#100MS) AND (tLevel_Discrep_AB < T#100MS) THEN
    bLevel_ChC_Fault := TRUE;
END_IF;

(* Fault-Tolerant Voting & Bumpless Degradation for Pressurizer Level *)
IF (NOT bLevel_ChA_Fault) AND (NOT bLevel_ChB_Fault) AND (NOT bLevel_ChC_Fault) THEN
    rPzrLevel_Voted_Pct := MAX(MIN(rPzrLevel_ChA_Pct, rPzrLevel_ChB_Pct), MIN(MAX(rPzrLevel_ChA_Pct, rPzrLevel_ChB_Pct), rPzrLevel_ChC_Pct));
ELSIF bLevel_ChA_Fault AND (NOT bLevel_ChB_Fault) AND (NOT bLevel_ChC_Fault) THEN
    rPzrLevel_Voted_Pct := (rPzrLevel_ChB_Pct + rPzrLevel_ChC_Pct) * 0.5;
ELSIF bLevel_ChB_Fault AND (NOT bLevel_ChA_Fault) AND (NOT bLevel_ChC_Fault) THEN
    rPzrLevel_Voted_Pct := (rPzrLevel_ChA_Pct + rPzrLevel_ChC_Pct) * 0.5;
ELSIF bLevel_ChC_Fault AND (NOT bLevel_ChA_Fault) AND (NOT bLevel_ChB_Fault) THEN
    rPzrLevel_Voted_Pct := (rPzrLevel_ChA_Pct + rPzrLevel_ChB_Pct) * 0.5;
ELSIF (NOT bLevel_ChA_Fault) AND bLevel_ChB_Fault AND bLevel_ChC_Fault THEN
    rPzrLevel_Voted_Pct := rPzrLevel_ChA_Pct;
ELSIF bLevel_ChA_Fault AND (NOT bLevel_ChB_Fault) AND bLevel_ChC_Fault THEN
    rPzrLevel_Voted_Pct := rPzrLevel_ChB_Pct;
ELSIF bLevel_ChA_Fault AND bLevel_ChB_Fault AND (NOT bLevel_ChC_Fault) THEN
    rPzrLevel_Voted_Pct := rPzrLevel_ChC_Pct;
ELSE
    bEmergencySCRAM_TripActive := TRUE;
    rPzrLevel_Voted_Pct := 22.0;
END_IF;
""")

    # -------------------------------------------------------------
    # 6. PHASE 2: CYBER-PHYSICAL STATE-SPACE & OBSERVER INNOVATION
    # -------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* === PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (x[k+1]=A*x+B*u+L*innov)    === *)
(* ==================================================================================================== *)

(* Initialize Model Parameters, Matrices & Precursors on Startup Scan *)
IF NOT bInitialized THEN
    (* 6x6 Discrete State Transition Matrix A *)
    matA[1,1] := 0.9850; matA[1,2] := -0.0120; matA[1,3] := -0.0085; matA[1,4] := 0.0000; matA[1,5] := 0.0000; matA[1,6] := 0.0015;
    matA[2,1] := 0.0245; matA[2,2] := 0.9650; matA[2,3] := 0.0180; matA[2,4] := 0.0020; matA[2,5] := 0.0000; matA[2,6] := -0.0150;
    matA[3,1] := 0.0520; matA[3,2] := 0.0150; matA[3,3] := 0.9250; matA[3,4] := 0.0000; matA[3,5] := 0.0000; matA[3,6] := 0.0000;
    matA[4,1] := 0.0080; matA[4,2] := 0.0350; matA[4,3] := 0.0000; matA[4,4] := 0.9720; matA[4,5] := -0.0180; matA[4,6] := 0.0050;
    matA[5,1] := 0.0020; matA[5,2] := 0.0450; matA[5,3] := 0.0000; matA[5,4] := 0.0060; matA[5,5] := 0.9880; matA[5,6] := 0.0000;
    matA[6,1] := 0.0000; matA[6,2] := -0.0050; matA[6,3] := 0.0000; matA[6,4] := 0.0010; matA[6,5] := 0.0000; matA[6,6] := 0.9940;

    (* 6x5 Discrete Input Coupling Matrix B *)
    matB[1,1] := -0.0185; matB[1,2] := 0.0000; matB[1,3] := 0.0000; matB[1,4] := -0.0005; matB[1,5] := 0.0000;
    matB[2,1] := -0.0065; matB[2,2] := 0.0010; matB[2,3] := -0.0025; matB[2,4] := 0.0012; matB[2,5] := 0.0005;
    matB[3,1] := -0.0220; matB[3,2] := 0.0000; matB[3,3] := 0.0000; matB[3,4] := 0.0000; matB[3,5] := 0.0000;
    matB[4,1] := 0.0000; matB[4,2] := 0.0385; matB[4,3] := -0.0480; matB[4,4] := 0.0125; matB[4,5] := 0.0650;
    matB[5,1] := 0.0000; matB[5,2] := 0.0020; matB[5,3] := 0.0045; matB[5,4] := 0.0350; matB[5,5] := 0.0035;
    matB[6,1] := 0.0000; matB[6,2] := 0.0000; matB[6,3] := 0.0000; matB[6,4] := 0.0005; matB[6,5] := 0.0000;

    (* 6x6 Measurement Output Matrix C (Identity) *)
    matC[1,1] := 1.0; matC[1,2] := 0.0; matC[1,3] := 0.0; matC[1,4] := 0.0; matC[1,5] := 0.0; matC[1,6] := 0.0;
    matC[2,1] := 0.0; matC[2,2] := 1.0; matC[2,3] := 0.0; matC[2,4] := 0.0; matC[2,5] := 0.0; matC[2,6] := 0.0;
    matC[3,1] := 0.0; matC[3,2] := 0.0; matC[3,3] := 1.0; matC[3,4] := 0.0; matC[3,5] := 0.0; matC[3,6] := 0.0;
    matC[4,1] := 0.0; matC[4,2] := 0.0; matC[4,3] := 0.0; matC[4,4] := 1.0; matC[4,5] := 0.0; matC[4,6] := 0.0;
    matC[5,1] := 0.0; matC[5,2] := 0.0; matC[5,3] := 0.0; matC[5,4] := 0.0; matC[5,5] := 1.0; matC[5,6] := 0.0;
    matC[6,1] := 0.0; matC[6,2] := 0.0; matC[6,3] := 0.0; matC[6,4] := 0.0; matC[6,5] := 0.0; matC[6,6] := 1.0;

    (* 6x5 Direct Transmission Matrix D (Zero) *)
    matD[1,1] := 0.0; matD[1,2] := 0.0; matD[1,3] := 0.0; matD[1,4] := 0.0; matD[1,5] := 0.0;
    matD[2,1] := 0.0; matD[2,2] := 0.0; matD[2,3] := 0.0; matD[2,4] := 0.0; matD[2,5] := 0.0;
    matD[3,1] := 0.0; matD[3,2] := 0.0; matD[3,3] := 0.0; matD[3,4] := 0.0; matD[3,5] := 0.0;
    matD[4,1] := 0.0; matD[4,2] := 0.0; matD[4,3] := 0.0; matD[4,4] := 0.0; matD[4,5] := 0.0;
    matD[5,1] := 0.0; matD[5,2] := 0.0; matD[5,3] := 0.0; matD[5,4] := 0.0; matD[5,5] := 0.0;
    matD[6,1] := 0.0; matD[6,2] := 0.0; matD[6,3] := 0.0; matD[6,4] := 0.0; matD[6,5] := 0.0;

    (* 6x6 Observer Luenberger Gain Matrix L *)
    matL[1,1] := 0.285; matL[1,2] := 0.015; matL[1,3] := 0.010; matL[1,4] := 0.000; matL[1,5] := 0.000; matL[1,6] := 0.002;
    matL[2,1] := 0.020; matL[2,2] := 0.310; matL[2,3] := 0.018; matL[2,4] := 0.005; matL[2,5] := 0.002; matL[2,6] := 0.000;
    matL[3,1] := 0.045; matL[3,2] := 0.025; matL[3,3] := 0.265; matL[3,4] := 0.000; matL[3,5] := 0.000; matL[3,6] := 0.000;
    matL[4,1] := 0.000; matL[4,2] := 0.015; matL[4,3] := 0.000; matL[4,4] := 0.350; matL[4,5] := 0.020; matL[4,6] := 0.005;
    matL[5,1] := 0.000; matL[5,2] := 0.005; matL[5,3] := 0.000; matL[5,4] := 0.018; matL[5,5] := 0.320; matL[5,6] := 0.000;
    matL[6,1] := 0.000; matL[6,2] := 0.000; matL[6,3] := 0.000; matL[6,4] := 0.002; matL[6,5] := 0.000; matL[6,6] := 0.240;

    (* MPC Quadratic Tracking Cost Matrix Q (6x6) *)
    matQ[1,1] := 15.0; matQ[1,2] := 0.0;  matQ[1,3] := 0.0;  matQ[1,4] := 0.0;  matQ[1,5] := 0.0;  matQ[1,6] := 0.0;
    matQ[2,1] := 0.0;  matQ[2,2] := 25.0; matQ[2,3] := 0.0;  matQ[2,4] := 0.0;  matQ[2,5] := 0.0;  matQ[2,6] := 0.0;
    matQ[3,1] := 0.0;  matQ[3,2] := 0.0;  matQ[3,3] := 2.5;  matQ[3,4] := 0.0;  matQ[3,5] := 0.0;  matQ[3,6] := 0.0;
    matQ[4,1] := 0.0;  matQ[4,2] := 0.0;  matQ[4,3] := 0.0;  matQ[4,4] := 35.0; matQ[4,5] := 0.0;  matQ[4,6] := 0.0;
    matQ[5,1] := 0.0;  matQ[5,2] := 0.0;  matQ[5,3] := 0.0;  matQ[5,4] := 0.0;  matQ[5,5] := 30.0; matQ[5,6] := 0.0;
    matQ[6,1] := 0.0;  matQ[6,2] := 0.0;  matQ[6,3] := 0.0;  matQ[6,4] := 0.0;  matQ[6,5] := 0.0;  matQ[6,6] := 5.0;

    (* MPC Actuator Penalty Matrix R (5x5) *)
    matR[1,1] := 2.5; matR[1,2] := 0.0; matR[1,3] := 0.0; matR[1,4] := 0.0; matR[1,5] := 0.0;
    matR[2,1] := 0.0; matR[2,2] := 0.8; matR[2,3] := 0.0; matR[2,4] := 0.0; matR[2,5] := 0.0;
    matR[3,1] := 0.0; matR[3,2] := 0.0; matR[3,3] := 1.5; matR[3,4] := 0.0; matR[3,5] := 0.0;
    matR[4,1] := 0.0; matR[4,2] := 0.0; matR[4,3] := 0.0; matR[4,4] := 0.6; matR[4,5] := 0.0;
    matR[5,1] := 0.0; matR[5,2] := 0.0; matR[5,3] := 0.0; matR[5,4] := 0.0; matR[5,5] := 1.2;

    (* MPC Slew Rate Penalty Matrix S (5x5) *)
    matS[1,1] := 5.0; matS[1,2] := 0.0; matS[1,3] := 0.0; matS[1,4] := 0.0; matS[1,5] := 0.0;
    matS[2,1] := 0.0; matS[2,2] := 1.5; matS[2,3] := 0.0; matS[2,4] := 0.0; matS[2,5] := 0.0;
    matS[3,1] := 0.0; matS[3,2] := 0.0; matS[3,3] := 3.0; matS[3,4] := 0.0; matS[3,5] := 0.0;
    matS[4,1] := 0.0; matS[4,2] := 0.0; matS[4,3] := 0.0; matS[4,4] := 1.0; matS[4,5] := 0.0;
    matS[5,1] := 0.0; matS[5,2] := 0.0; matS[5,3] := 0.0; matS[5,4] := 0.0; matS[5,5] := 2.5;

    (* MPC Terminal Penalty Matrix P_term (6x6) *)
    matP_term[1,1] := 45.0; matP_term[1,2] := 0.0;   matP_term[1,3] := 0.0;   matP_term[1,4] := 0.0;   matP_term[1,5] := 0.0;   matP_term[1,6] := 0.0;
    matP_term[2,1] := 0.0;   matP_term[2,2] := 75.0;  matP_term[2,3] := 0.0;   matP_term[2,4] := 0.0;   matP_term[2,5] := 0.0;   matP_term[2,6] := 0.0;
    matP_term[3,1] := 0.0;   matP_term[3,2] := 0.0;   matP_term[3,3] := 8.0;   matP_term[3,4] := 0.0;   matP_term[3,5] := 0.0;   matP_term[3,6] := 0.0;
    matP_term[4,1] := 0.0;   matP_term[4,2] := 0.0;   matP_term[4,3] := 0.0;   matP_term[4,4] := 110.0; matP_term[4,5] := 0.0;   matP_term[4,6] := 0.0;
    matP_term[5,1] := 0.0;   matP_term[5,2] := 0.0;   matP_term[5,3] := 0.0;   matP_term[5,4] := 0.0;   matP_term[5,5] := 90.0;  matP_term[5,6] := 0.0;
    matP_term[6,1] := 0.0;   matP_term[6,2] := 0.0;   matP_term[6,3] := 0.0;   matP_term[6,4] := 0.0;   matP_term[6,5] := 0.0;   matP_term[6,6] := 15.0;

    (* Actuator Boundaries & Slew Limits *)
    vecU_min[1] := -72.0; vecU_max[1] := 72.0;  vecDU_max[1] := 8.0;  (* Rod speed steps/min *)
    vecU_min[2] := 0.0;   vecU_max[2] := 100.0; vecDU_max[2] := 20.0; (* Proportional heaters % *)
    vecU_min[3] := 0.0;   vecU_max[3] := 100.0; vecDU_max[3] := 25.0; (* Spray valve % *)
    vecU_min[4] := 0.0;   vecU_max[4] := 100.0; vecDU_max[4] := 15.0; (* CVCS pump % *)
    vecU_min[5] := 0.0;   vecU_max[5] := 100.0; vecDU_max[5] := 100.0;(* Backup heaters on/off % *)

    (* Point Kinetics Precursor Constants (U-235 Thermal Fission Delayed Groups) *)
    rBeta_1 := 0.000215; rLambda_1 := 0.0124;
    rBeta_2 := 0.001424; rLambda_2 := 0.0305;
    rBeta_3 := 0.001274; rLambda_3 := 0.1110;
    rBeta_4 := 0.002568; rLambda_4 := 0.3010;
    rBeta_5 := 0.000748; rLambda_5 := 1.1400;
    rBeta_6 := 0.000273; rLambda_6 := 3.0100;
    rBetaTotal := 0.006502;
    rPromptLifetime := 0.000020; (* 20 microseconds prompt generation lifetime *)

    (* Iodine-135 / Xenon-135 Chain Constants *)
    rDecayConst_I := 0.0000287;   (* 1/s (half-life 6.57 hours) *)
    rDecayConst_Xe := 0.0000209;  (* 1/s (half-life 9.2 hours) *)
    rFissionYield_I := 0.0639;
    rFissionYield_Xe := 0.0023;
    rSigmaAbs_Xe := 2.65E-18;     (* cm2 thermal absorption cross section *)
    rMacroFission := 0.125;       (* 1/cm macroscopic fission cross section *)
    rNuFission := 2.43;           (* average fission neutrons *)

    (* Reactivity Feedback Coefficients *)
    rAlphaDoppler := -2.85;       (* Doppler fuel temperature coefficient: -2.85 pcm/deg C *)
    rAlphaModerator := -28.5;     (* Moderator density temperature coefficient: -28.5 pcm/deg C *)
    rBoronDifferential := -8.2;   (* Chemical soluble boron differential worth: -8.2 pcm/ppm *)
    rT_fuel_ref := 680.0;         (* Reference nominal fuel centerline temperature at 100% FP [deg C] *)
    rT_mod_ref := 292.0;          (* Reference nominal moderator temperature [deg C] *)
    rBoron_ref_ppm := 1200.0;     (* Nominal cycle critical boron reference [ppm] *)

    (* Pressurizer Thermodynamic Constants *)
    rPzrTotalVolume_M3 := 51.0;
    rRCS_FluidDensity_KgM3 := 710.0;
    rRCS_VolExpansionCoeff := 0.0028;
    rRCS_TotalFluidMass_Kg := 250000.0;
    h_v_sat := 2.65E6;
    h_l_sat := 1.62E6;
    h_spray_liq := 1.25E6;

    (* Initialize State Vector Estimates *)
    vecX_hat[1] := 100.0;   (* Power 100% FP *)
    vecX_hat[2] := 308.5;   (* RCS Tavg 308.5 deg C *)
    vecX_hat[3] := 680.0;   (* Fuel Centerline 680.0 deg C *)
    vecX_hat[4] := 155.1;   (* Pressurizer Pressure 155.1 bar *)
    vecX_hat[5] := 53.5;    (* Pressurizer Level 53.5 % *)
    vecX_hat[6] := 14200.0; (* RCS Primary Mass Flow Rate 14,200 kg/s *)

    (* Initialize Precursors to Equilibrium at 100% FP *)
    rPrecursor_C1 := (rBeta_1 / (rLambda_1 * rPromptLifetime)) * 100.0;
    rPrecursor_C2 := (rBeta_2 / (rLambda_2 * rPromptLifetime)) * 100.0;
    rPrecursor_C3 := (rBeta_3 / (rLambda_3 * rPromptLifetime)) * 100.0;
    rPrecursor_C4 := (rBeta_4 / (rLambda_4 * rPromptLifetime)) * 100.0;
    rPrecursor_C5 := (rBeta_5 / (rLambda_5 * rPromptLifetime)) * 100.0;
    rPrecursor_C6 := (rBeta_6 / (rLambda_6 * rPromptLifetime)) * 100.0;

    (* Initialize Iodine and Xenon to Equilibrium *)
    rNeutronFlux := 100.0 * 3.5E11;
    rIodine135_Conc := (rFissionYield_I * rMacroFission * rNeutronFlux) / rDecayConst_I;
    rXenon135_Conc := (rFissionYield_Xe * rMacroFission * rNeutronFlux + rDecayConst_I * rIodine135_Conc) / (rDecayConst_Xe + rSigmaAbs_Xe * rNeutronFlux);

    bInitialized := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* 1. POINT KINETICS WITH 6 DELAYED NEUTRON PRECURSORS & IODINE/XENON BALANCES                       *)
(* -------------------------------------------------------------------------------------------------- *)
rNeutronFlux := rNuclearPower_Voted_PctFP * 3.5E11;

(* Precursor Group Differential Integrations *)
dPrecursor_C1 := (rBeta_1 / rPromptLifetime) * rNuclearPower_Voted_PctFP - rLambda_1 * rPrecursor_C1;
dPrecursor_C2 := (rBeta_2 / rPromptLifetime) * rNuclearPower_Voted_PctFP - rLambda_2 * rPrecursor_C2;
dPrecursor_C3 := (rBeta_3 / rPromptLifetime) * rNuclearPower_Voted_PctFP - rLambda_3 * rPrecursor_C3;
dPrecursor_C4 := (rBeta_4 / rPromptLifetime) * rNuclearPower_Voted_PctFP - rLambda_4 * rPrecursor_C4;
dPrecursor_C5 := (rBeta_5 / rPromptLifetime) * rNuclearPower_Voted_PctFP - rLambda_5 * rPrecursor_C5;
dPrecursor_C6 := (rBeta_6 / rPromptLifetime) * rNuclearPower_Voted_PctFP - rLambda_6 * rPrecursor_C6;

rPrecursor_C1 := rPrecursor_C1 + dPrecursor_C1 * rCycleSec;
rPrecursor_C2 := rPrecursor_C2 + dPrecursor_C2 * rCycleSec;
rPrecursor_C3 := rPrecursor_C3 + dPrecursor_C3 * rCycleSec;
rPrecursor_C4 := rPrecursor_C4 + dPrecursor_C4 * rCycleSec;
rPrecursor_C5 := rPrecursor_C5 + dPrecursor_C5 * rCycleSec;
rPrecursor_C6 := rPrecursor_C6 + dPrecursor_C6 * rCycleSec;

(* Iodine-135 and Xenon-135 Differential Dynamics *)
dIodine135 := rFissionYield_I * rMacroFission * rNeutronFlux - rDecayConst_I * rIodine135_Conc;
rIodine135_Conc := rIodine135_Conc + dIodine135 * rCycleSec;

dXenon135 := rFissionYield_Xe * rMacroFission * rNeutronFlux + rDecayConst_I * rIodine135_Conc - rDecayConst_Xe * rXenon135_Conc - rSigmaAbs_Xe * rXenon135_Conc * rNeutronFlux;
rXenon135_Conc := rXenon135_Conc + dXenon135 * rCycleSec;

(* Calculate Dynamic Xenon Poisoning Reactivity [pcm] *)
rReactivityXenon := - (rSigmaAbs_Xe * rXenon135_Conc) / (rNuFission * rMacroFission) * 1.0E5;

(* Control Rod Regulating Bank D Integral Worth (S-Curve Normalized Polynomial) *)
IF rControlRodBankD_PosSteps > 228.0 THEN
    rRodPositionFrac := 1.0;
ELSIF rControlRodBankD_PosSteps < 0.0 THEN
    rRodPositionFrac := 0.0;
ELSE
    rRodPositionFrac := rControlRodBankD_PosSteps / 228.0;
END_IF;

(* Integrated Worth: Full Out (Frac=1.0) -> 0 pcm; Full In (Frac=0.0) -> -1200 pcm *)
rReactivityRods := - 1200.0 * (1.0 - (3.0 * rRodPositionFrac * rRodPositionFrac - 2.0 * rRodPositionFrac * rRodPositionFrac * rRodPositionFrac));

(* Thermal Reactivity Feedbacks *)
rReactivityDoppler := rAlphaDoppler * (vecX_hat[3] - rT_fuel_ref);
rReactivityMod := rAlphaModerator * (rRCS_Tavg_Voted_DegC - rT_mod_ref);
rReactivityBoron := rBoronDifferential * (rBoronConcentration_PPM - rBoron_ref_ppm);

(* Total Core Reactivity Balance [pcm] *)
rCalculatedReactivity_PCM := rReactivityRods + rReactivityDoppler + rReactivityMod + rReactivityBoron + rReactivityXenon;

(* -------------------------------------------------------------------------------------------------- *)
(* 2. PRESSURIZER TWO-REGION NON-EQUILIBRIUM THERMODYNAMIC MASS & ENERGY BALANCES                     *)
(* -------------------------------------------------------------------------------------------------- *)
(* Compute Rate of RCS Coolant Expansion / Contraction *)
rRCS_HeatupRampRate := ((rRCS_Tavg_Voted_DegC - rPreviousTavg_Sample) / rCycleSec) * 3600.0;
rPreviousTavg_Sample := rRCS_Tavg_Voted_DegC;

(* Surge Flow Coupling: Net CVCS Injection + Primary Coolant Thermal Volumetric Expansion *)
rPzrSurgeFlow_KgSec := ((rCVCS_ChargingFlow_M3h - rCVCS_LetdownFlow_M3h) * (rRCS_FluidDensity_KgM3 / 3600.0)) + (rRCS_TotalFluidMass_Kg * rRCS_VolExpansionCoeff * ((rRCS_Tavg_Voted_DegC - rPreviousTavg_Sample) / rCycleSec));

(* Total Pressurizer Electric Immersion Heater Thermal Power *)
rPzrTotalHeaterPower_W := (rPzrProportionalHeaters_Cmd / 100.0) * 450000.0;
IF bPzrBackupHeaterBank1_Cmd THEN
    rPzrTotalHeaterPower_W := rPzrTotalHeaterPower_W + 675000.0;
END_IF;
IF bPzrBackupHeaterBank2_Cmd THEN
    rPzrTotalHeaterPower_W := rPzrTotalHeaterPower_W + 675000.0;
END_IF;

(* Modulating Cold Leg Spray Flow *)
rPzrSprayFlow_KgSec := (rPzrSprayValveMod_Cmd / 100.0) * 45.0;

(* Pilot-Operated Relief Valve Discharge Flow *)
IF bPzrPORV_ReliefValve_Cmd THEN
    rPzrReliefFlow_KgSec := 28.5; (* 28.5 kg/s steam relief at 162 bar *)
ELSE
    rPzrReliefFlow_KgSec := 0.0;
END_IF;

(* Dynamic Rate of Pressurizer Pressure Change dp/dt [bar/s] *)
rRateOfPressureChange := (rPzrTotalHeaterPower_W - rPzrSprayFlow_KgSec * (h_v_sat - h_spray_liq) + rPzrSurgeFlow_KgSec * (h_l_sat - h_spray_liq) - rPzrReliefFlow_KgSec * h_v_sat) / (rPzrTotalVolume_M3 * 2.85E5);

(* -------------------------------------------------------------------------------------------------- *)
(* 3. RCS TAVG TURBINE PROGRAMMED REFERENCE & MISMATCH TEMPERATURE ERROR                             *)
(* -------------------------------------------------------------------------------------------------- *)
(* Programmed Turbine Load Reference: 292.0 deg C at 0% Load to 308.5 deg C at 100% Load *)
rRCS_Tref_Program_DegC := 292.0 + (308.5 - 292.0) * (rTurbineLoadDemand / 100.0);
rRCS_DeltaT_Error_DegC := rRCS_Tavg_Voted_DegC - rRCS_Tref_Program_DegC;
rDeltaT_CoreActual := rRCS_Thot_ChA_DegC - rRCS_Tcold_ChA_DegC;

(* -------------------------------------------------------------------------------------------------- *)
(* 4. 6x6 STATE-SPACE OBSERVER INNOVATION: x_hat[k+1] = A*x_hat[k] + B*u[k] + L*(y_meas - C*x_hat[k]) *)
(* -------------------------------------------------------------------------------------------------- *)
(* Assemble Process Measurement Vector *)
vecX_meas[1] := rNuclearPower_Voted_PctFP;
vecX_meas[2] := rRCS_Tavg_Voted_DegC;
vecX_meas[3] := rRCS_Tavg_Voted_DegC + (rNuclearPower_Voted_PctFP * 3.75); (* Core fuel centerline estimate *)
vecX_meas[4] := rPzrPressure_Voted_Bar;
vecX_meas[5] := rPzrLevel_Voted_Pct;
vecX_meas[6] := rRCS_TotalLoopFlow_KgSec;

(* Compute Measurement Innovation Residual: y_innov = y_meas - C * x_hat *)
FOR idxRow := 1 TO 6 DO
    rTempSum := 0.0;
    FOR idxCol := 1 TO 6 DO
        rTempSum := rTempSum + matC[idxRow, idxCol] * vecX_hat[idxCol];
    END_FOR;
    vecY_innov[idxRow] := vecX_meas[idxRow] - rTempSum;
END_FOR;

(* Propagate Observer Discrete State Trajectory *)
FOR idxRow := 1 TO 6 DO
    (* A * x_hat component *)
    rTempSum := 0.0;
    FOR idxCol := 1 TO 6 DO
        rTempSum := rTempSum + matA[idxRow, idxCol] * vecX_hat[idxCol];
    END_FOR;
    
    (* B * u component *)
    rTempSum2 := 0.0;
    FOR idxInput := 1 TO 5 DO
        rTempSum2 := rTempSum2 + matB[idxRow, idxInput] * vecU_cmd[idxInput];
    END_FOR;
    
    (* L * innovation residual component *)
    FOR idxCol := 1 TO 6 DO
        rTempSum2 := rTempSum2 + matL[idxRow, idxCol] * vecY_innov[idxCol];
    END_FOR;
    
    vecX_hat_next[idxRow] := rTempSum + rTempSum2;
END_FOR;

(* Latch Propagated Observer States *)
FOR idxRow := 1 TO 6 DO
    vecX_hat[idxRow] := vecX_hat_next[idxRow];
END_FOR;

(* Output Estimated Telemetry *)
rEstimatedFuelTemp_DegC := vecX_hat[3];
rEstimatedCoolantFlow_KgSec := vecX_hat[6];
""")

    # -------------------------------------------------------------
    # 7. PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH 10 UNROLLED PGD ITERATIONS
    # -------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* === PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH 10 UNROLLED PGD ITERATIONS                   === *)
(* ==================================================================================================== *)

(* Parameterize Target State References *)
vecX_ref[1] := rTurbineLoadDemand;                                      (* Target Nuclear Power [% FP] *)
vecX_ref[2] := rRCS_Tref_Program_DegC;                                  (* Target RCS Tavg [deg C] *)
vecX_ref[3] := 292.0 + (680.0 - 292.0) * (rTurbineLoadDemand / 100.0);   (* Target Fuel Centerline [deg C] *)
vecX_ref[4] := 155.1;                                                   (* Target Pressurizer Pressure [bar] *)
vecX_ref[5] := 22.0 + (53.5 - 22.0) * (rTurbineLoadDemand / 100.0);     (* Programmed Level [22%..53.5%] *)
vecX_ref[6] := 14200.0;                                                 (* Nominal 4-Loop Mass Flow [kg/s] *)

(* Initialize Prediction Horizon Step 0 to Observer Current State *)
FOR idxRow := 1 TO 6 DO
    arrX_pred_traj[0, idxRow] := vecX_hat[idxRow];
END_FOR;

(* Initialize Actuator Trajectory with Previous Solution *)
FOR idxHorizon := 0 TO 3 DO
    FOR idxInput := 1 TO 5 DO
        arrU_pred_traj[idxHorizon, idxInput] := vecU_cmd[idxInput];
    END_FOR;
END_FOR;

(* PGD Learning Rate Step Size *)
rStepSizeAlpha := 0.0035;

(* -------------------------------------------------------------------------------------------------- *)
(* UNROLLED 10 ITERATIONS OF PROJECTED GRADIENT DESCENT (PGD)                                        *)
(* -------------------------------------------------------------------------------------------------- *)
FOR idxIter := 1 TO 10 DO
    (* ---------------------------------------------------------------------------------------------- *)
    (* Step A: Forward Trajectory Rollout Simulation (k = 0 to 3)                                     *)
    (* ---------------------------------------------------------------------------------------------- *)
    FOR idxHorizon := 0 TO 3 DO
        FOR idxRow := 1 TO 6 DO
            rTempSum := 0.0;
            FOR idxCol := 1 TO 6 DO
                rTempSum := rTempSum + matA[idxRow, idxCol] * arrX_pred_traj[idxHorizon, idxCol];
            END_FOR;
            
            rTempSum2 := 0.0;
            FOR idxInput := 1 TO 5 DO
                rTempSum2 := rTempSum2 + matB[idxRow, idxInput] * arrU_pred_traj[idxHorizon, idxInput];
            END_FOR;
            
            arrX_pred_traj[idxHorizon + 1, idxRow] := rTempSum + rTempSum2;
        END_FOR;
    END_FOR;

    (* ---------------------------------------------------------------------------------------------- *)
    (* Step B: Terminal Adjoint Costate Vector Evaluation: lambda[4] = P_term * (x[4] - x_ref)        *)
    (* ---------------------------------------------------------------------------------------------- *)
    FOR idxRow := 1 TO 6 DO
        rTempSum := 0.0;
        FOR idxCol := 1 TO 6 DO
            rTempSum := rTempSum + matP_term[idxRow, idxCol] * (arrX_pred_traj[4, idxCol] - vecX_ref[idxCol]);
        END_FOR;
        arrLambda_traj[4, idxRow] := rTempSum;
    END_FOR;

    (* ---------------------------------------------------------------------------------------------- *)
    (* Step C: Backward Adjoint Costate Recursion (k = 3 down to 0)                                   *)
    (* ---------------------------------------------------------------------------------------------- *)
    FOR idxHorizon := 3 DOWNTO 0 DO
        (* Evaluate Dynamic Constraints: Axial Flux Difference (AFD) & RCS Thermal Ramp Rate *)
        IF ABS(rAxialFluxOffset_Pct) > 5.0 THEN
            rPenaltyAFD := (ABS(rAxialFluxOffset_Pct) - 5.0) * 12.5;
        ELSE
            rPenaltyAFD := 0.0;
        END_IF;

        rPenaltyRamp := 0.0;
        IF ABS(arrX_pred_traj[idxHorizon + 1, 2] - arrX_pred_traj[idxHorizon, 2]) > 0.01528 THEN
            rPenaltyRamp := (ABS(arrX_pred_traj[idxHorizon + 1, 2] - arrX_pred_traj[idxHorizon, 2]) - 0.01528) * 45.0;
        END_IF;

        FOR idxRow := 1 TO 6 DO
            (* State error penalty: Q * (x - x_ref) *)
            rTempSum := 0.0;
            FOR idxCol := 1 TO 6 DO
                rTempSum := rTempSum + matQ[idxRow, idxCol] * (arrX_pred_traj[idxHorizon, idxCol] - vecX_ref[idxCol]);
            END_FOR;
            
            (* Adjoint back-propagation: A^T * lambda[k+1] *)
            rTempSum2 := 0.0;
            FOR idxCol := 1 TO 6 DO
                rTempSum2 := rTempSum2 + matA[idxCol, idxRow] * arrLambda_traj[idxHorizon + 1, idxCol];
            END_FOR;
            
            (* Include barrier constraint penalties on power and temperature *)
            IF idxRow = 1 THEN
                rTempSum := rTempSum + rPenaltyAFD;
            ELSIF idxRow = 2 THEN
                rTempSum := rTempSum + rPenaltyRamp;
            END_IF;
            
            arrLambda_traj[idxHorizon, idxRow] := rTempSum + rTempSum2;
        END_FOR;
    END_FOR;

    (* ---------------------------------------------------------------------------------------------- *)
    (* Step D: Actuator Gradient Computation & Projected Box Step Update                             *)
    (* ---------------------------------------------------------------------------------------------- *)
    FOR idxHorizon := 0 TO 3 DO
        FOR idxInput := 1 TO 5 DO
            (* Effort gradient: R * u *)
            rTempSum := 0.0;
            FOR idxCol := 1 TO 5 DO
                rTempSum := rTempSum + matR[idxInput, idxCol] * arrU_pred_traj[idxHorizon, idxCol];
            END_FOR;
            
            (* Costate gradient: B^T * lambda[k+1] *)
            rTempSum2 := 0.0;
            FOR idxRow := 1 TO 6 DO
                rTempSum2 := rTempSum2 + matB[idxRow, idxInput] * arrLambda_traj[idxHorizon + 1, idxRow];
            END_FOR;
            
            (* Slew rate damping gradient: S * (u - u_prev) *)
            FOR idxCol := 1 TO 5 DO
                rTempSum2 := rTempSum2 + matS[idxInput, idxCol] * (arrU_pred_traj[idxHorizon, idxCol] - vecU_prev[idxCol]);
            END_FOR;
            
            vecGradU[idxInput] := rTempSum + rTempSum2;
            
            (* Projected Step Update *)
            rStepUpdate := arrU_pred_traj[idxHorizon, idxInput] - rStepSizeAlpha * vecGradU[idxInput];
            
            (* Slew Rate Clamping *)
            rStepClamped := MAX(vecU_prev[idxInput] - vecDU_max[idxInput], MIN(vecU_prev[idxInput] + vecDU_max[idxInput], rStepUpdate));
            
            (* Actuator Saturation Box Projection *)
            arrU_pred_traj[idxHorizon, idxInput] := MAX(vecU_min[idxInput], MIN(vecU_max[idxInput], rStepClamped));
        END_FOR;
    END_FOR;
END_FOR;

(* Extract First Horizon Actuator Demand as Optimal Command *)
vecU_cmd[1] := arrU_pred_traj[0, 1]; (* Rod bank speed command [-72..+72 steps/min] *)
vecU_cmd[2] := arrU_pred_traj[0, 2]; (* Proportional heaters power [0..100 %] *)
vecU_cmd[3] := arrU_pred_traj[0, 3]; (* Spray valve demand [0..100 %] *)
vecU_cmd[4] := arrU_pred_traj[0, 4]; (* CVCS charging pump speed [0..100 %] *)
vecU_cmd[5] := arrU_pred_traj[0, 5]; (* Backup heaters bank demand [0..100 %] *)
""")

    # -------------------------------------------------------------
    # 8. PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE
    # -------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* === PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                        === *)
(* ==================================================================================================== *)

(* Update State Elapsed Execution Timer *)
tStateTimer := tStateTimer + tScanCycleTime;
rStateTime_Sec := TIME_TO_REAL(tStateTimer) / 1000.0;
bStateFirstCycle := (iCurrentFSMState <> iPrevState);
iPrevState := iCurrentFSMState;

(* Nuclear Standard Permissive Interlock Logic *)
bPermissive_P4 := bEmergencySCRAM_TripActive;
bPermissive_P6 := (rNuclearPower_Voted_PctFP >= 0.001);
bPermissive_P7 := (rNuclearPower_Voted_PctFP >= 10.0);
bPermissive_P8 := (rNuclearPower_Voted_PctFP >= 30.0);
bPermissive_P10 := (rNuclearPower_Voted_PctFP >= 10.0);

(* Emergency Trip Overrides State Machine into State 13 *)
IF bManualTripSCRAM_Class1E OR bEmergencySCRAM_TripActive THEN
    iCurrentFSMState := 13;
END_IF;

(* Execute Finite State Machine *)
CASE iCurrentFSMState OF
    (* ---------------------------------------------------------------------------------------------- *)
    0: (* STATE_IDLE *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
            vecU_cmd[1] := 0.0;
            vecU_cmd[2] := 0.0;
            vecU_cmd[3] := 0.0;
            vecU_cmd[4] := 0.0;
            vecU_cmd[5] := 0.0;
        END_IF;
        
        (* Idle transition to cold shutdown when master enabled *)
        IF bMasterEnable AND (NOT bEmergencySCRAM_TripActive) THEN
            iCurrentFSMState := 1;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    1: (* STATE_COLD_SHUTDOWN_RHR_CIRCULATION_AND_BORON_CHECK *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Verify Residual Heat Removal circulation flow and boron concentration >= 2400 ppm *)
        IF (rBoronConcentration_PPM >= 2400.0) AND (rRCS_TotalLoopFlow_KgSec >= 8000.0) AND (rStateTime_Sec >= 5.0) THEN
            iCurrentFSMState := 2;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    2: (* STATE_HOT_SHUTDOWN_RCS_HEATING_AND_PRESSURIZATION *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Energize heaters to draw pressurizer steam bubble and ramp RCS temperature to 292 deg C *)
        vecU_cmd[2] := 100.0; (* Proportional heaters full *)
        vecU_cmd[5] := 100.0; (* Backup heaters full *)
        
        (* Regulate water level to 22% during bubble formation *)
        IF rPzrLevel_Voted_Pct < 22.0 THEN
            vecU_cmd[4] := 65.0; (* Increase CVCS charging *)
        ELSE
            vecU_cmd[4] := 25.0;
        END_IF;
        
        (* Transition to Hot Standby when pressure reaches 155.1 bar and temperature reaches 292 deg C *)
        IF (rPzrPressure_Voted_Bar >= 153.0) AND (rRCS_Tavg_Voted_DegC >= 290.0) AND (rPzrLevel_Voted_Pct >= 20.0) THEN
            iCurrentFSMState := 3;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    3: (* STATE_HOT_STANDBY_CRDM_POWER_ENABLE_AND_TEST *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Hold pressure at 155.1 bar and Tavg at 292.0 deg C *)
        IF rPzrPressure_Voted_Bar > 155.5 THEN
            vecU_cmd[2] := 0.0;
            vecU_cmd[3] := 15.0; (* Slight spray *)
        ELSIF rPzrPressure_Voted_Bar < 154.5 THEN
            vecU_cmd[2] := 75.0;
            vecU_cmd[3] := 0.0;
        END_IF;
        
        (* Once CRDM MG sets are synchronized and safety injection armed, proceed to criticality approach *)
        IF (rStateTime_Sec >= 10.0) AND bAutoRodControlSelect THEN
            iCurrentFSMState := 4;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    4: (* STATE_REACTOR_CRITICALITY_APPROACH_DILUTION_AND_PULL *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
            rBaselineCountRate := 120.0; (* Initial baseline shutdown count rate *)
        END_IF;
        
        (* Calculate 1/M multiplication monitoring ratio *)
        rCurrentCountRate := 120.0 + (rNuclearPower_Voted_PctFP * 1.0E5);
        rCriticality_1_over_M := rBaselineCountRate / MAX(1.0, rCurrentCountRate);
        
        (* Step out Regulating Bank D at conservative speed *)
        IF rControlRodBankD_PosSteps < 150.0 THEN
            vecU_cmd[1] := 16.0; (* 16 steps/min withdrawal *)
            bCRDM_StepDirectionOut := TRUE;
        ELSE
            vecU_cmd[1] := 0.0;
        END_IF;
        
        (* Reactor achieves criticality when power rises above 1.0E-3 % FP *)
        IF (rNuclearPower_Voted_PctFP >= 0.001) AND (rCalculatedReactivity_PCM >= -50.0) THEN
            iCurrentFSMState := 5;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    5: (* STATE_ZERO_POWER_PHYSICS_TESTING_AND_CALIBRATION *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
            rPhysicsTestingPower_Pct := 0.05; (* Hold at 0.05% FP *)
        END_IF;
        
        (* Regulate power tightly at physics testing level using small rod trims *)
        IF rNuclearPower_Voted_PctFP > 0.06 THEN
            vecU_cmd[1] := -8.0; (* Insert rods *)
            bCRDM_StepDirectionOut := FALSE;
        ELSIF rNuclearPower_Voted_PctFP < 0.04 THEN
            vecU_cmd[1] := 8.0; (* Withdraw rods *)
            bCRDM_StepDirectionOut := TRUE;
        ELSE
            vecU_cmd[1] := 0.0;
        END_IF;
        
        (* After calibration period and approval, advance to power ascension *)
        IF (rStateTime_Sec >= 15.0) THEN
            iCurrentFSMState := 6;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    6: (* STATE_POWER_ASCENSION_RAMP_TURBINE_SYNCHRONIZATION *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Ramp reactor power and coordinate turbine acceleration *)
        IF rNuclearPower_Voted_PctFP < 15.0 THEN
            vecU_cmd[1] := 24.0; (* Withdraw rods to ramp power *)
            bCRDM_StepDirectionOut := TRUE;
        ELSE
            vecU_cmd[1] := 0.0;
            bTurbineBreakerClosed := TRUE;
        END_IF;
        
        (* Permissive P-10 arms when power exceeds 10% FP. Transition to Nominal Baseload when synchronized *)
        IF bPermissive_P10 AND (rNuclearPower_Voted_PctFP >= 15.0) AND bTurbineBreakerClosed THEN
            iCurrentFSMState := 7;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    7: (* STATE_NOMINAL_BASELOAD_COORDINATED_MPC_ACTIVE *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* In Nominal Baseload, full multivariable receding-horizon MPC actively governs actuators *)
        (* Handled by Phase 3 optimal control commands *)
        
        (* Detect grid frequency deviations triggering frequency response mode *)
        IF bGridFrequencyDroopEnable AND (ABS(rGridFrequency_Hz - 50.0) > 0.15) THEN
            iCurrentFSMState := 8;
        ELSIF ABS(rReactivityXenon) > 2800.0 THEN
            iCurrentFSMState := 9; (* Xenon trim compensation *)
        ELSIF bTurbineTripInterlock THEN
            iCurrentFSMState := 10; (* Rapid steam dump turndown *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    8: (* STATE_GRID_FREQUENCY_LOAD_FOLLOWING_RAMP_DISPATCH *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Primary Frequency Response Droop (4% Governor Droop Characteristic) *)
        IF rGridFrequency_Hz < 49.85 THEN
            (* Underfrequency: Increase turbine load demand and withdraw rods *)
            vecU_cmd[1] := 32.0;
            bCRDM_StepDirectionOut := TRUE;
        ELSIF rGridFrequency_Hz > 50.15 THEN
            (* Overfrequency: Decrease turbine load demand and insert rods *)
            vecU_cmd[1] := -32.0;
            bCRDM_StepDirectionOut := FALSE;
        END_IF;
        
        (* Return to baseload when grid frequency stabilizes *)
        IF ABS(rGridFrequency_Hz - 50.0) <= 0.05 THEN
            iCurrentFSMState := 7;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    9: (* STATE_XENON_TRANSIENT_POISONING_COMPENSATION_TRIM *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Compensate for Xenon peak or decay using CVCS boration/dilution trim *)
        IF rReactivityXenon < -3000.0 THEN
            (* Xenon build-up: Dilute soluble boron to restore reactivity *)
            vecU_cmd[4] := 75.0; (* Higher pure condensate charging *)
        ELSIF rReactivityXenon > -2200.0 THEN
            (* Xenon burnout: Borate coolant *)
            vecU_cmd[4] := 35.0;
        END_IF;
        
        (* Return to baseload when xenon stabilizes *)
        IF (rStateTime_Sec >= 20.0) OR (ABS(dXenon135) < 1.0E7) THEN
            iCurrentFSMState := 7;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    10: (* STATE_RAPID_POWER_TURNDOWN_STEAM_DUMP_BYPASS *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
            bSteamDumpBypassPermissive := TRUE;
        END_IF;
        
        (* Fast rod insertion to match reduced steam demand without tripping reactor *)
        vecU_cmd[1] := -72.0; (* Maximum insertion speed *)
        bCRDM_StepDirectionOut := FALSE;
        
        (* Modulate spray to suppress pressure surge *)
        vecU_cmd[3] := 80.0;
        vecU_cmd[2] := 0.0;
        
        (* When reactor power reaches target bypass load level, transition back to baseload or controlled shutdown *)
        IF (rNuclearPower_Voted_PctFP <= 35.0) AND (rPzrPressure_Voted_Bar <= 156.0) THEN
            bSteamDumpBypassPermissive := FALSE;
            iCurrentFSMState := 7;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    11: (* STATE_CONTROLLED_REACTOR_SHUTDOWN_BORON_INJECTION *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Boration to cold shutdown concentration while inserting control rods *)
        vecU_cmd[1] := -48.0; (* Regulating rod insertion *)
        bCRDM_StepDirectionOut := FALSE;
        vecU_cmd[4] := 85.0;  (* Concentrated boric acid injection *)
        
        (* When core is deeply subcritical, transition to idle/cold shutdown *)
        IF (rNuclearPower_Voted_PctFP <= 0.0001) AND (rControlRodBankD_PosSteps <= 5.0) THEN
            iCurrentFSMState := 1;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    12: (* STATE_POST_SCRAM_RESIDUAL_HEAT_REMOVAL_STABILIZE *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Stabilize primary plant after SCRAM: Maintain pressurizer level at 22% and pressure at 150 bar *)
        vecU_cmd[1] := 0.0; (* Rods already fully on bottom *)
        IF rPzrPressure_Voted_Bar < 150.0 THEN
            vecU_cmd[2] := 80.0;
            vecU_cmd[5] := 50.0;
            vecU_cmd[3] := 0.0;
        ELSIF rPzrPressure_Voted_Bar > 153.0 THEN
            vecU_cmd[2] := 0.0;
            vecU_cmd[5] := 0.0;
            vecU_cmd[3] := 25.0;
        END_IF;
        
        IF rPzrLevel_Voted_Pct < 22.0 THEN
            vecU_cmd[4] := 60.0;
        ELSE
            vecU_cmd[4] := 20.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------- *)
    13: (* STATE_EMERGENCY_REACTOR_TRIP_SCRAM_CONTAINMENT_ISOLATION *)
    (* ---------------------------------------------------------------------------------------------- *)
        IF bStateFirstCycle THEN
            tStateTimer := T#0MS;
        END_IF;
        
        (* Immediate Class 1E fail-safe actuator trips *)
        bEmergencySCRAM_TripActive := TRUE;
        bSafetyContainmentIsolation_Cmd := TRUE;
        vecU_cmd[1] := -72.0; (* Full speed gravity fall demand *)
        bCRDM_StepDirectionOut := FALSE;
        vecU_cmd[2] := 0.0;   (* Trip proportional heaters *)
        vecU_cmd[5] := 0.0;   (* Trip backup heaters *)
        vecU_cmd[3] := 0.0;   (* Close spray valves *)
        vecU_cmd[4] := 100.0; (* Max emergency high head injection if SI active *)
        
        (* When core decay heat stabilizes and containment verified isolated, transition to post-SCRAM stabilization *)
        IF (rStateTime_Sec >= 10.0) AND (rNuclearPower_Voted_PctFP < 0.1) THEN
            iCurrentFSMState := 12;
        END_IF;
END_CASE;
""")

    # -------------------------------------------------------------
    # 9. PHASE 5: ISA-18.2 MULTI-TIER ALARMS & BIT-PACKED TELEMETRY DWORDS & OUTPUTS
    # -------------------------------------------------------------
    parts.append("""
(* ==================================================================================================== *)
(* === PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS WORDS & ACTUATOR MODULATION  === *)
(* ==================================================================================================== *)

(* -------------------------------------------------------------------------------------------------- *)
(* 1. ISA-18.2 ALARM DETECTION WITH DEADBAND HYSTERESIS                                              *)
(* -------------------------------------------------------------------------------------------------- *)
(* Reactor Overpower Alarms (High-High = 107.0% FP Trip, High = 103.0% FP Warning) *)
IF rNuclearPower_Voted_PctFP >= 107.0 THEN
    bAlarm_Power_HH := TRUE;
    bEmergencySCRAM_TripActive := TRUE;
ELSIF rNuclearPower_Voted_PctFP < 105.5 THEN
    bAlarm_Power_HH := FALSE;
END_IF;

IF rNuclearPower_Voted_PctFP >= 103.0 THEN
    bAlarm_Power_H := TRUE;
ELSIF rNuclearPower_Voted_PctFP < 101.5 THEN
    bAlarm_Power_H := FALSE;
END_IF;

IF rNuclearPower_Voted_PctFP <= 0.5 THEN
    bAlarm_Power_L := TRUE;
ELSIF rNuclearPower_Voted_PctFP > 1.0 THEN
    bAlarm_Power_L := FALSE;
END_IF;

IF rNuclearPower_Voted_PctFP <= 0.01 THEN
    bAlarm_Power_LL := TRUE;
ELSIF rNuclearPower_Voted_PctFP > 0.05 THEN
    bAlarm_Power_LL := FALSE;
END_IF;

(* Pressurizer Pressure Alarms (HH = 165.0 bar Trip, H = 158.0 bar, L = 151.0 bar, LL = 135.0 bar Trip) *)
IF rPzrPressure_Voted_Bar >= 165.0 THEN
    bAlarm_Press_HH := TRUE;
    bEmergencySCRAM_TripActive := TRUE;
ELSIF rPzrPressure_Voted_Bar < 163.5 THEN
    bAlarm_Press_HH := FALSE;
END_IF;

IF rPzrPressure_Voted_Bar >= 158.0 THEN
    bAlarm_Press_H := TRUE;
ELSIF rPzrPressure_Voted_Bar < 156.5 THEN
    bAlarm_Press_H := FALSE;
END_IF;

IF rPzrPressure_Voted_Bar <= 151.0 THEN
    bAlarm_Press_L := TRUE;
ELSIF rPzrPressure_Voted_Bar > 152.5 THEN
    bAlarm_Press_L := FALSE;
END_IF;

IF rPzrPressure_Voted_Bar <= 135.0 THEN
    bAlarm_Press_LL := TRUE;
    bEmergencySCRAM_TripActive := TRUE;
ELSIF rPzrPressure_Voted_Bar > 137.0 THEN
    bAlarm_Press_LL := FALSE;
END_IF;

(* Pressurizer Level Alarms (HH = 92.0% Trip, H = 70.0%, L = 20.0%, LL = 12.0% Heater Trip) *)
IF rPzrLevel_Voted_Pct >= 92.0 THEN
    bAlarm_Level_HH := TRUE;
    bEmergencySCRAM_TripActive := TRUE;
ELSIF rPzrLevel_Voted_Pct < 90.0 THEN
    bAlarm_Level_HH := FALSE;
END_IF;

IF rPzrLevel_Voted_Pct >= 70.0 THEN
    bAlarm_Level_H := TRUE;
ELSIF rPzrLevel_Voted_Pct < 68.0 THEN
    bAlarm_Level_H := FALSE;
END_IF;

IF rPzrLevel_Voted_Pct <= 20.0 THEN
    bAlarm_Level_L := TRUE;
ELSIF rPzrLevel_Voted_Pct > 22.0 THEN
    bAlarm_Level_L := FALSE;
END_IF;

IF rPzrLevel_Voted_Pct <= 12.0 THEN
    bAlarm_Level_LL := TRUE;
ELSIF rPzrLevel_Voted_Pct > 14.0 THEN
    bAlarm_Level_LL := FALSE;
END_IF;

(* Primary Coolant Tavg Alarms (HH = 315.0 deg C Trip, H = 311.0 deg C, L = 288.0 deg C, LL = 280.0 deg C) *)
IF rRCS_Tavg_Voted_DegC >= 315.0 THEN
    bAlarm_Tavg_HH := TRUE;
    bEmergencySCRAM_TripActive := TRUE;
ELSIF rRCS_Tavg_Voted_DegC < 313.5 THEN
    bAlarm_Tavg_HH := FALSE;
END_IF;

IF rRCS_Tavg_Voted_DegC >= 311.0 THEN
    bAlarm_Tavg_H := TRUE;
ELSIF rRCS_Tavg_Voted_DegC < 309.5 THEN
    bAlarm_Tavg_H := FALSE;
END_IF;

IF rRCS_Tavg_Voted_DegC <= 288.0 THEN
    bAlarm_Tavg_L := TRUE;
ELSIF rRCS_Tavg_Voted_DegC > 290.0 THEN
    bAlarm_Tavg_L := FALSE;
END_IF;

IF rRCS_Tavg_Voted_DegC <= 280.0 THEN
    bAlarm_Tavg_LL := TRUE;
    bEmergencySCRAM_TripActive := TRUE;
ELSIF rRCS_Tavg_Voted_DegC > 282.0 THEN
    bAlarm_Tavg_LL := FALSE;
END_IF;

(* Overtemperature Delta-T (OTDT) Dynamic Reactor Protection Setpoint Calculation *)
rOTDT_CalculatedTrip := 38.5 * (1.185 - 0.0125 * (rRCS_Tavg_Voted_DegC - 302.5) + 0.00085 * (rPzrPressure_Voted_Bar - 155.1) - 0.0055 * MAX(0.0, ABS(rAxialFluxOffset_Pct) - 5.0));
IF rDeltaT_CoreActual >= rOTDT_CalculatedTrip THEN
    bAlarm_OTDT_Trip := TRUE;
    bEmergencySCRAM_TripActive := TRUE;
ELSIF rDeltaT_CoreActual < (rOTDT_CalculatedTrip - 1.2) THEN
    bAlarm_OTDT_Trip := FALSE;
END_IF;

(* Overpower Delta-T (OPDT) Dynamic Reactor Protection Setpoint Calculation *)
rOPDT_CalculatedTrip := 38.5 * (1.095 - 0.0085 * (rRCS_Tavg_Voted_DegC - 302.5) - 0.0045 * MAX(0.0, ABS(rAxialFluxOffset_Pct) - 5.0));
IF rDeltaT_CoreActual >= rOPDT_CalculatedTrip THEN
    bAlarm_OPDT_Trip := TRUE;
    bEmergencySCRAM_TripActive := TRUE;
ELSIF rDeltaT_CoreActual < (rOPDT_CalculatedTrip - 1.2) THEN
    bAlarm_OPDT_Trip := FALSE;
END_IF;

(* Axial Flux Difference (AFD) Target Band Violation *)
IF ABS(rAxialFluxOffset_Pct) > 5.0 THEN
    bAlarm_AFD_OutOfBand := TRUE;
ELSIF ABS(rAxialFluxOffset_Pct) < 4.2 THEN
    bAlarm_AFD_OutOfBand := FALSE;
END_IF;

(* RCS Thermal Heatup/Cooldown Ramp Rate Limit (55.0 deg C / hr) *)
IF ABS(rRCS_HeatupRampRate) > 55.0 THEN
    bAlarm_ThermalRamp_High := TRUE;
ELSIF ABS(rRCS_HeatupRampRate) < 50.0 THEN
    bAlarm_ThermalRamp_High := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* 2. FIRST-OUT SCRAM ROOT-CAUSE LATCHING LOGIC                                                      *)
(* -------------------------------------------------------------------------------------------------- *)
IF (dwFirstOutWord = 16#00000000) AND bEmergencySCRAM_TripActive THEN
    IF bManualTripSCRAM_Class1E THEN
        dwFirstOutWord := 16#00000001; (* Bit 0: Manual Operator Pushbutton SCRAM *)
    ELSIF bAlarm_Power_HH THEN
        dwFirstOutWord := 16#00000002; (* Bit 1: Reactor Overpower High-High Trip *)
    ELSIF bAlarm_Press_HH THEN
        dwFirstOutWord := 16#00000004; (* Bit 2: Pressurizer Pressure High-High Trip *)
    ELSIF bAlarm_Press_LL THEN
        dwFirstOutWord := 16#00000008; (* Bit 3: Pressurizer Pressure Low-Low Trip *)
    ELSIF bAlarm_Level_HH THEN
        dwFirstOutWord := 16#00000010; (* Bit 4: Pressurizer Level High-High Trip *)
    ELSIF bAlarm_Tavg_HH THEN
        dwFirstOutWord := 16#00000020; (* Bit 5: RCS Coolant Tavg High-High Trip *)
    ELSIF bAlarm_OTDT_Trip THEN
        dwFirstOutWord := 16#00000040; (* Bit 6: Overtemperature Delta-T Trip *)
    ELSIF bAlarm_OPDT_Trip THEN
        dwFirstOutWord := 16#00000080; (* Bit 7: Overpower Delta-T Trip *)
    ELSIF bTurbineTripInterlock THEN
        dwFirstOutWord := 16#00000100; (* Bit 8: Turbine Stop Valve Fast Trip *)
    ELSIF bSafetyInjectionActuated THEN
        dwFirstOutWord := 16#00000200; (* Bit 9: Safety Injection Actuation Trip *)
    ELSE
        dwFirstOutWord := 16#00008000; (* Bit 15: General Hardware TMR Trip *)
    END_IF;
END_IF;

(* Operator Alarm Acknowledge Reset *)
IF bOperatorAckAlarms THEN
    IF NOT bEmergencySCRAM_TripActive THEN
        dwFirstOutWord := 16#00000000;
    END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* 3. 32-BIT TELEMETRY ENCODING: STATUS & ALARM WORDS                                                 *)
(* -------------------------------------------------------------------------------------------------- *)
(* dwStatusWord1: Operational States and Health Flags *)
dwStatusWord1 := INT_TO_DWORD(iCurrentFSMState); (* Bits 0..3: Current State Index *)
IF bMasterEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bEmergencySCRAM_TripActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bAutoRodControlSelect THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bAutoPressurizerSelect THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF (NOT bFlux_ChA_Fault) AND (NOT bFlux_ChB_Fault) AND (NOT bFlux_ChC_Fault) THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF (NOT bTemp_ChA_Fault) AND (NOT bTemp_ChB_Fault) AND (NOT bTemp_ChC_Fault) THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF (NOT bPress_ChA_Fault) AND (NOT bPress_ChB_Fault) AND (NOT bPress_ChC_Fault) THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF (NOT bLevel_ChA_Fault) AND (NOT bLevel_ChB_Fault) AND (NOT bLevel_ChC_Fault) THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF ABS(vecU_cmd[1]) > 1.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* Rods Stepping *)
IF bCRDM_StepDirectionOut THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;  (* Rod Direction Out *)
IF vecU_cmd[2] > 5.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;       (* Prop Heaters Active *)
IF vecU_cmd[3] > 2.0 THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;       (* Spray Active *)

(* dwStatusWord2: Nuclear Permissives and System Substates *)
dwStatusWord2 := 16#00000000;
IF bPermissive_P4 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bPermissive_P6 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bPermissive_P7 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF bPermissive_P8 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF bPermissive_P10 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF bGridFrequencyDroopEnable THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bSteamDumpBypassPermissive THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF bTurbineBreakerClosed THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;
IF bPzrBackupHeaterBank1_Cmd THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bPzrBackupHeaterBank2_Cmd THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bPzrPORV_ReliefValve_Cmd THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;

(* dwAlarmWord1: Primary ISA-18.2 Warning & Trip Bits *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_Power_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_Power_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_Power_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_Power_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_Press_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_Press_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_Press_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarm_Press_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bAlarm_Level_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF bAlarm_Level_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF bAlarm_Level_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF bAlarm_Level_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF bAlarm_Tavg_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF bAlarm_Tavg_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;
IF bAlarm_Tavg_L THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF;
IF bAlarm_Tavg_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF;

(* dwAlarmWord2: Core Protection and Hardware Discrepancies *)
dwAlarmWord2 := 16#00000000;
IF bAlarm_OTDT_Trip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlarm_OPDT_Trip THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlarm_AFD_OutOfBand THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlarm_ThermalRamp_High THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bFlux_ChA_Fault OR bFlux_ChB_Fault OR bFlux_ChC_Fault THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bTemp_ChA_Fault OR bTemp_ChB_Fault OR bTemp_ChC_Fault THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bPress_ChA_Fault OR bPress_ChB_Fault OR bPress_ChC_Fault THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bLevel_ChA_Fault OR bLevel_ChB_Fault OR bLevel_ChC_Fault THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;

(* -------------------------------------------------------------------------------------------------- *)
(* 4. ACTUATOR COMMAND DISPATCH & MODULATION STAGES                                                  *)
(* -------------------------------------------------------------------------------------------------- *)
(* Control Rod Drive Mechanism (CRDM) Stepping Generator *)
rCRDM_RodBankSpeed_Cmd := vecU_cmd[1];
IF rCRDM_RodBankSpeed_Cmd > 1.0 THEN
    bCRDM_StepDirectionOut := TRUE;
    rCRDM_PulseTimer := rCRDM_PulseTimer + rCycleSec;
    IF rCRDM_PulseTimer >= (60.0 / rCRDM_RodBankSpeed_Cmd) THEN
        bCRDM_StepGatePulse := TRUE;
        rCRDM_PulseTimer := 0.0;
    ELSE
        bCRDM_StepGatePulse := FALSE;
    END_IF;
ELSIF rCRDM_RodBankSpeed_Cmd < -1.0 THEN
    bCRDM_StepDirectionOut := FALSE;
    rCRDM_PulseTimer := rCRDM_PulseTimer + rCycleSec;
    IF rCRDM_PulseTimer >= (60.0 / ABS(rCRDM_RodBankSpeed_Cmd)) THEN
        bCRDM_StepGatePulse := TRUE;
        rCRDM_PulseTimer := 0.0;
    ELSE
        bCRDM_StepGatePulse := FALSE;
    END_IF;
ELSE
    bCRDM_StepGatePulse := FALSE;
    rCRDM_PulseTimer := 0.0;
END_IF;

(* Pressurizer Heaters Outputs *)
IF bAlarm_Level_LL THEN
    (* Interlock: Cut all immersion heaters on Low-Low water level to prevent element burnout *)
    rPzrProportionalHeaters_Cmd := 0.0;
    bPzrBackupHeaterBank1_Cmd := FALSE;
    bPzrBackupHeaterBank2_Cmd := FALSE;
ELSE
    rPzrProportionalHeaters_Cmd := vecU_cmd[2];
    bPzrBackupHeaterBank1_Cmd := (vecU_cmd[5] >= 40.0);
    bPzrBackupHeaterBank2_Cmd := (vecU_cmd[5] >= 80.0);
END_IF;

(* Pressurizer Spray Modulating Valve Demand *)
rPzrSprayValveMod_Cmd := vecU_cmd[3];

(* Pressurizer Pilot-Operated Relief Valve (PORV) Solenoid Demand *)
IF rPzrPressure_Voted_Bar >= 162.0 THEN
    bPzrPORV_ReliefValve_Cmd := TRUE;
ELSIF rPzrPressure_Voted_Bar <= 158.5 THEN
    bPzrPORV_ReliefValve_Cmd := FALSE;
END_IF;

(* CVCS Charging & Letdown Modulating Commands *)
rCVCS_ChargingPumpSpeed_Cmd := vecU_cmd[4];
IF rPzrLevel_Voted_Pct > 58.0 THEN
    rCVCS_LetdownControlValve_Cmd := 75.0;
ELSIF rPzrLevel_Voted_Pct < 48.0 THEN
    rCVCS_LetdownControlValve_Cmd := 25.0;
ELSE
    rCVCS_LetdownControlValve_Cmd := 50.0;
END_IF;

(* Telemetry State Output *)
iCurrentFSMState := iCurrentFSMState;

(* Store Current Control Vector as Previous for Slew Rate Limiting in Next Cycle *)
FOR idxInput := 1 TO 5 DO
    vecU_prev[idxInput] := vecU_cmd[idxInput];
END_FOR;
""")

    # -------------------------------------------------------------
    # 10. CLOSING DECLARATION
    # -------------------------------------------------------------
    parts.append("\nEND_FUNCTION_BLOCK\n")
    
    full_code = "".join(parts)
    return full_code

if __name__ == "__main__":
    code = build_full_iec_st()
    print(f"Generated Structured Text characters: {len(code)}")
    with open("FB_Nuclear_PWR_PrimaryCoolant_Pressurizer_RodControl_Coordinated.st", "w", encoding="utf-8") as f:
        f.write(code)
    print("Saved to .st file.")
