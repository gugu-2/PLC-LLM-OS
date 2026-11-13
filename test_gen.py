# Generator script to write the complete IEC 61131-3 dataset for Nuclear PWR Coordinated Control
import json
import uuid
import re
import os
import sys

def build_full_iec_st():
    lines = []
    
    # First line
    lines.append("FUNCTION_BLOCK FB_Nuclear_PWR_PrimaryCoolant_Pressurizer_RodControl_Coordinated")
    
    # Engineering Documentation Header
    lines.append("""(*
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
*)""")

    # VAR_INPUT
    lines.append("""VAR_INPUT
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
END_VAR""")

    # VAR_OUTPUT
    lines.append("""VAR_OUTPUT
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
END_VAR""")

    # VAR Block
    lines.append("""VAR
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
END_VAR""")

    # Execution Preamble
    lines.append("""
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
END_IF;""")

    # Phase 1: 2oo3 TMR Voting Suite
    lines.append("""
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
END_IF;""")

    return "\n".join(lines)

print("Phase 1 complete.")
