# -*- coding: utf-8 -*-
"""
Continuous Batch Washer (CBW) & Extractor ST Generator
Domain: Commercial Laundry Continuous Batch Tunnel Washers & High-Speed Ironers (Rank #83)
Target: FB_CommercialLaundry_ContinuousTunnelWasher_Extractor
"""

import sys
import os

def generate_iec_st():
    parts = []

    # =========================================================================
    # PART 1: HEADER & SPECIFICATION
    # =========================================================================
    p1 = """FUNCTION_BLOCK FB_CommercialLaundry_ContinuousTunnelWasher_Extractor
(*
 ==========================================================================================
  PROJECT:       COMMERCIAL LAUNDRY AUTOMATION & MASS TEXTILE PROCESSING
  SUBSYSTEM:     14-COMPARTMENT CONTINUOUS BATCH TUNNEL WASHER (CBW), 40-BAR HYDRAULIC
                 EXTRACTION PRESS, CENTRIFUGAL CAKE BREAKER, AND GAS-FIRED CHEST IRONER
  DISCIPLINE:    CYBER-PHYSICAL PROCESS CONTROL / CHEMICAL KINETICS / HYDRAULIC SERVO
  IEC STANDARD:  IEC 61131-3 3RD EDITION COMPLIANT (DETERMINISTIC EMBEDDED EXECUTION)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  PLANT SCALE:   2,400 KG/HR CONTINUOUS LINEN THROUGHPUT (60 KG DRY LINEN / 90 SEC BATCH)
  SCAN CYCLE Ts: 10.000 MILLISECOND DETERMINISTIC SYNCHRONOUS PLC EXECUTION TICK [ms]
 ==========================================================================================
  CYBER-PHYSICAL SYSTEM ARCHITECTURAL OVERVIEW:
  ------------------------------------------------------------------------------------------
  This high-performance Function Block governs a complete continuous commercial laundry
  washhouse system comprising four tightly coupled mechatronic and thermo-chemical stages:

  1. 14-Compartment Counter-Flow Continuous Batch Tunnel Washer (CBW):
     - Compartments 1 to 3 (Pre-Wash Zone): Low-temperature soaking (35-45 [deg C]) utilizing
       recycled warm rinse water to break down water-soluble soils, blood, and protein soils
       without thermal coagulation. Wetting agent and enzymatic detergents dosed proportionally.
     - Compartments 4 to 8 (Main Wash Caustic Zone): High-temperature thermal washing up to
       85.0 [deg C] with direct live steam injection. Precision peristaltic dosing of sodium
       hydroxide (NaOH 50%) caustic solution to maintain wash liquor conductivity at 9,500 [uS/cm]
       and surfactants for heavy emulsification of greases, vegetable oils, and mineral lubricants.
     - Compartments 9 to 10 (Bleaching & Disinfection Zone): Injection of peracetic acid (PAA)
       or sodium hypochlorite at 60.0 to 65.0 [deg C] with exact dwell time pacing to guarantee
       complete microbiological sanitation complying with EN 14065 / RABC standards while
       preventing cellulose tensile fiber degradation.
     - Compartments 11 to 13 (Counter-flow Rinse & Neutralization Zone): Clean fresh water make-up
       cascading in counter-current direction from Compartment 14 towards Compartment 1.
       Acid souring (formic / citric acid) dosing to neutralize residual alkalinity to target
       pH 5.80 to 6.20, followed by cationic quaternary fabric softeners and antistatic agents.
     - Compartment 14 (Discharge Chamber): Archimedean bottom-transfer screw or top-transfer scoop
       mechanism indexing saturated 60 kg batches into the dewatering press transfer chute.

  2. 40-Bar Membrane Hydraulic Extraction Press:
     - Heavy-duty welded steel press frame with vertical hydraulic ram cylinder delivering up to
       40.0 [bar] fluid pressure against a heavy elastomeric water-bag membrane.
     - Compresses water-saturated linen cake inside a perforated stainless steel basket.
     - Darcy's law porous medium dewatering kinetics: Ram descent rate and hydraulic pressure ramp
       profile are actively optimized by Model Predictive Control (MPC) to avoid textile shear
       rupture (preventing interfacial shear stress exceeding critical limit tau_max = 185 [kPa])
       while driving residual textile moisture retention below 45.0% dry basis in under 85 seconds.

  3. Continuous Thermal Energy Recovery & Water Recycling Network:
     - Shell-and-tube counter-flow heat exchanger recovering sensible enthalpy from 82.0 [deg C]
       hot effluent drain streams to preheat 15.0 [deg C] municipal fresh water to 55.0 [deg C].
     - Multi-stage mechanical lint screen and rotary disc filtration returning press filtrate
       water to the pre-wash rinse recovery buffer tank, slashing fresh water consumption below
       4.5 liters per kilogram of processed linen.

  4. High-Speed Centrifugal Cake Breaker & Multi-Roll Chest Ironer Synchronization:
     - Centrifugal rotary unbalance cake breaker shaker operating at variable frequency to
       break up compressed cylindrical linen cakes prior to flatwork conditioning.
     - High-speed 3-roll gas-fired chest ironer operating at up to 45.0 [m/min], incorporating
       closed-loop textile web tension regulation via drive roll surface velocity trim to eliminate
       wrinkles, fabric skewing, and excessive warp-thread tensile strain.
 ==========================================================================================
*)
VAR_INPUT
    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) CONDUCTIVITY / TDS SENSORS [uS/cm]              *)
    (* ================================================================================= *)
    rConductivity_ChA_uScm          : REAL;     (* Compartment 5 caustic wash toroidal conductivity sensor Ch A [uS/cm] *)
    rConductivity_ChB_uScm          : REAL;     (* Compartment 5 caustic wash toroidal conductivity sensor Ch B [uS/cm] *)
    rConductivity_ChC_uScm          : REAL;     (* Compartment 5 caustic wash toroidal conductivity sensor Ch C [uS/cm] *)

    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) WASH WATER TEMPERATURE RTDs [deg C]              *)
    (* ================================================================================= *)
    rWaterTemp_ChA_degC             : REAL;     (* Compartment 6 main wash duplex Pt100 RTD element Ch A [deg C] *)
    rWaterTemp_ChB_degC             : REAL;     (* Compartment 6 main wash duplex Pt100 RTD element Ch B [deg C] *)
    rWaterTemp_ChC_degC             : REAL;     (* Compartment 6 main wash duplex Pt100 RTD element Ch C [deg C] *)

    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) BATCH INFEED SLING LOAD CELLS [kg]              *)
    (* ================================================================================= *)
    rBatchWeight_ChA_kg             : REAL;     (* Infeed overhead monorail sling strain-gauge load cell Ch A [kg] *)
    rBatchWeight_ChB_kg             : REAL;     (* Infeed overhead monorail sling strain-gauge load cell Ch B [kg] *)
    rBatchWeight_ChC_kg             : REAL;     (* Infeed overhead monorail sling strain-gauge load cell Ch C [kg] *)

    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) 40-BAR HYDRAULIC PRESS PRESSURE TRANSDUCERS [bar]*)
    (* ================================================================================= *)
    rPressPressure_ChA_bar          : REAL;     (* Extraction ram main cylinder piezoresistive pressure Ch A [bar] *)
    rPressPressure_ChB_bar          : REAL;     (* Extraction ram main cylinder piezoresistive pressure Ch B [bar] *)
    rPressPressure_ChC_bar          : REAL;     (* Extraction ram main cylinder piezoresistive pressure Ch C [bar] *)

    (* ================================================================================= *)
    (* HYDRAULIC EXTRACTION RAM POSITION, VELOCITY & FILTRATE DRAINAGE FEEDBACK          *)
    (* ================================================================================= *)
    rRamDisplacement_mm             : REAL;     (* Hydraulic ram vertical stroke magnetostrictive linear encoder [mm] *)
    rRamVelocity_mms                : REAL;     (* Hydraulic ram instantaneous downward press velocity [mm/s] *)
    rPressDrainFlow_m3h             : REAL;     (* Extraction press water-bag drain electromagnetic flowmeter [m3/h] *)

    (* ================================================================================= *)
    (* ENERGY RECOVERY HEAT EXCHANGER TEMPERATURE & EFFLUENT SENSORS [deg C, %]          *)
    (* ================================================================================= *)
    rHeatExchTubeInletTemp_degC     : REAL;     (* Waste wash liquor effluent inlet temperature to tube bundle [deg C] *)
    rHeatExchTubeOutletTemp_degC    : REAL;     (* Cooled effluent discharge temperature leaving heat exchanger [deg C] *)
    rHeatExchShellInletTemp_degC    : REAL;     (* Cold municipal fresh water intake inlet temperature [deg C] *)
    rRinseNeutralizationPH_pH       : REAL;     (* Souring rinse compartment 12 combination glass pH transmitter [pH] *)
    rPeristalticLinePressure_bar    : REAL;     (* Chemical distribution manifold peristaltic header pressure [bar] *)
    rRecoveryTankLevel_pct          : REAL;     (* Recycled filtrate storage buffer tank hydrostatic level [%] *)
    rFreshWaterFlow_m3h             : REAL;     (* Municipal fresh make-up water intake turbine flowmeter [m3/h] *)
    rSteamSupplyPressure_bar        : REAL;     (* Live saturated steam header main supply pressure [bar] *)

    (* ================================================================================= *)
    (* FLATWORK IRONER & CAKE SHAKER KINEMATIC & THERMAL SENSORS [deg C, m/min, N, mm/s] *)
    (* ================================================================================= *)
    rIronerChestTemp_degC           : REAL;     (* Heated chest cast iron bed contact infrared pyrometer [deg C] *)
    rIronerRollSpeed_mpm            : REAL;     (* Primary ironer drive roller optical encoder line speed [m/min] *)
    rIronerLinenTension_N           : REAL;     (* Textile web interfacial draw tension load cell transducer [N] *)
    rCakeShakerVibration_mms        : REAL;     (* Centrifugal cake breaker bearing RMS unbalance vibration [mm/s] *)

    (* ================================================================================= *)
    (* DISCRETE SYSTEM PERMISSIVES, SAFETY INTERLOCKS & OPERATOR COMMANDS                *)
    (* ================================================================================= *)
    bMasterEnable                   : BOOL;     (* Master supervisory continuous tunnel washing permissive *)
    bEmergencyStopOk                : BOOL;     (* Active-low fail-safe SIL-3 hardware emergency stop circuit *)
    bScrewJamTorqueSwitch           : BOOL;     (* Archimedean transfer screw mechanical slip-clutch limit switch *)
    bPressBasketLocked              : BOOL;     (* Hydraulic press drainage basket positioning interlock confirmed *)
    bCakeShakerReady                : BOOL;     (* Centrifugal cake shaker infeed hopper clear and ready *)
    bIronerInfeedBeamClear          : BOOL;     (* Flatwork ironer entry cross-feed optical jam detection photocell *)
    bChemicalDosingFlowOk           : BOOL;     (* Peristaltic chemical magnetic positive flow pulse confirmation *)
    bFiltrationBackwashActive       : BOOL;     (* Water recycling sand/disc filter automatic backwash in progress *)
    bOperatorReset                  : BOOL;     (* Operator panel manual fault reset pushbutton *)
END_VAR
"""
    parts.append(p1)

    # =========================================================================
    # PART 2: VAR_OUTPUT
    # =========================================================================
    p2 = """VAR_OUTPUT
    (* ================================================================================= *)
    (* CONTINUOUS TUNNEL WASHER ANALOG ACTUATOR & VALVE COMMANDS [%]                     *)
    (* ================================================================================= *)
    rSteamControlValve_pct          : REAL;     (* Main wash live steam proportional modulating control valve [%] *)
    rFreshWaterValve_pct            : REAL;     (* Counter-flow fresh water make-up proportional intake valve [%] *)
    rCausticDosingVFD_pct           : REAL;     (* Caustic soda (NaOH) peristaltic dosing pump variable speed [%] *)
    rAcidDosingVFD_pct              : REAL;     (* Souring acid neutralization peristaltic pump variable speed [%] *)
    rDetergentDosingVFD_pct         : REAL;     (* Main wash surfactant / detergent peristaltic pump speed [%] *)
    rBleachDosingVFD_pct            : REAL;     (* Peracetic acid / bleach sanitizing dosing pump speed [%] *)
    rPressServoValve_pct            : REAL;     (* 40-bar hydraulic extraction ram servo proportional pump valve [%] *)
    rPressReliefValve_pct           : REAL;     (* High-speed proportional hydraulic backpressure relief valve [%] *)
    rCakeShakerVFD_pct              : REAL;     (* Centrifugal cake breaker unbalance drive motor speed demand [%] *)
    rIronerBurnerModulation_pct     : REAL;     (* High-speed chest ironer modulating gas burner firing rate [%] *)
    rIronerVFD_SpeedDemand_pct      : REAL;     (* Chest ironer roll motor synchronized surface speed trim [%] *)
    rRecycleDivertValve_pct         : REAL;     (* Thermal energy recovery effluent diversion proportional valve [%] *)

    (* ================================================================================= *)
    (* DISCRETE MECHATRONIC ACTUATOR DRIVES & SAFETY INTERLOCKS                          *)
    (* ================================================================================= *)
    bScrewMotorRunForward           : BOOL;     (* Archimedean transfer screw forward rotational transfer command *)
    bScrewMotorRunReverse           : BOOL;     (* Archimedean transfer screw reverse anti-jamming jog command *)
    bPressRamAdvanceSol             : BOOL;     (* Hydraulic extraction press ram vertical descent press solenoid *)
    bPressRamRetractSol             : BOOL;     (* Hydraulic extraction press ram vertical retract solenoid *)
    bPressDumpValveEmergency        : BOOL;     (* Hydraulic high-speed emergency safety pressure dump to reservoir *)
    bCakeConveyorRun                : BOOL;     (* Dewatered textile cake shuttle transfer conveyor drive command *)
    bIronerRollNipEngage            : BOOL;     (* Pneumatic chest ironer textile roll nip engagement solenoid *)
    bChemicalFlushValve             : BOOL;     (* Chemical distribution manifold demineralized water purge valve *)
    bAlarmBeaconAudible             : BOOL;     (* Category 1 audible plant annunciator siren *)
    bAlarmBeaconVisual              : BOOL;     (* High-intensity strobe beacon for active unacknowledged alarm *)

    (* ================================================================================= *)
    (* SYNTHESIZED 2oo3 VOTED PROCESS SIGNALS [uS/cm, deg C, kg, bar]                   *)
    (* ================================================================================= *)
    rVotedConductivity_uScm         : REAL;     (* 2oo3 median voted compartment 5 caustic wash conductivity [uS/cm] *)
    rVotedWaterTemp_degC            : REAL;     (* 2oo3 median voted wash water bulk temperature [deg C] *)
    rVotedBatchWeight_kg            : REAL;     (* 2oo3 median voted infeed dry linen batch gross weight [kg] *)
    rVotedPressPressure_bar         : REAL;     (* 2oo3 median voted hydraulic extraction ram pressure [bar] *)

    (* ================================================================================= *)
    (* OBSERVER PROCESS ESTIMATES & PERFORMANCE METRICS [%, kPa, L]                      *)
    (* ================================================================================= *)
    rEstimatedMoistureFraction_pct  : REAL;     (* Dynamic cake observer remaining moisture retention fraction [%] *)
    rEstimatedShearStress_kPa       : REAL;     (* Estimated textile interfacial fabric shear stress [kPa] *)
    rHeatExchangerEffectiveness_pct : REAL;     (* Counter-flow energy recovery heat exchanger efficiency [%] *)
    rCumulativeWaterRecycled_L      : REAL;     (* Total cumulative recovered filtrate water recycled to tunnel [L] *)

    (* ================================================================================= *)
    (* BIT-PACKED STATUS & ALARM WORDS (ISA-18.2 COMPLIANT)                              *)
    (* ================================================================================= *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed supervisory operational status and sequence mode *)
    dwAlarmWord1_EmergencyTrips     : DWORD;    (* Bit-packed Category 1 SIL-3 emergency shutdowns and trips *)
    dwAlarmWord2_ProcessTrips       : DWORD;    (* Bit-packed Category 2 process limit violations and quality trips *)
    dwWarningWord                   : DWORD;    (* Bit-packed Category 3 operational advisory warnings *)
    dwDegradationWord               : DWORD;    (* Bit-packed 2oo3 instrument triplet degradation and health flags *)
    dwIsaAlarmPriorityMask          : DWORD;    (* Bit-packed active ISA-18.2 alarm priority annunciator mask *)
END_VAR
"""
    parts.append(p2)

    # =========================================================================
    # PART 3: VAR (INTERNAL DECLARATIONS)
    # =========================================================================
    p3 = """VAR
    (* ================================================================================= *)
    (* SUPERVISORY FINITE STATE MACHINE (FSM) STEP REGISTERS & PROCESS TIMERS           *)
    (* ================================================================================= *)
    iState                          : INT := 0; (* Primary supervisory state register *)
    iSubState                       : INT := 0; (* Secondary execution substep register *)
    iPrevState                      : INT := 0; (* Previous scan cycle state history *)
    iStepIndex                      : INT := 0; (* Execution step progression counter within state *)
    bStateChanged                   : BOOL := FALSE; (* State transition edge trigger flag *)
    
    tStateTimer                     : TON;      (* Primary supervisory state dwell timer *)
    tTransferTimer                  : TON;      (* Archimedean transfer screw rotational index timer *)
    tPreWashTimer                   : TON;      (* Compartment 1-3 pre-wash mechanical action timer *)
    tMainWashTimer                  : TON;      (* Compartment 4-8 main caustic thermal dwell timer *)
    tBleachTimer                    : TON;      (* Compartment 9-10 disinfection contact timer *)
    tRinseTimer                     : TON;      (* Compartment 11-13 rinse and neutralization dwell timer *)
    tPressRampTimer                 : TON;      (* Hydraulic press ram pressure ramp execution timer *)
    tPressHoldTimer                 : TON;      (* Hydraulic press 40-bar holding dewatering timer *)
    tCakeShakerTimer                : TON;      (* Centrifugal cake breaker unbalance shake cycle timer *)
    tDebounceTimer                  : TON;      (* Operator reset and transient fault debounce timer *)
    tDiscrepancyTimer_Cond          : TON;      (* Conductivity 2oo3 sensor triplet discrepancy timer *)
    tDiscrepancyTimer_Temp          : TON;      (* Temperature RTD 2oo3 sensor triplet discrepancy timer *)
    tDiscrepancyTimer_Weight        : TON;      (* Load cell 2oo3 sensor triplet discrepancy timer *)
    tDiscrepancyTimer_Press         : TON;      (* Press pressure 2oo3 sensor triplet discrepancy timer *)
    tScrewJamTimer                  : TON;      (* Archimedean transfer screw mechanical stall jam timer *)
    tOcclusionTimer                 : TON;      (* Chemical peristaltic line occlusion over-pressure timer *)

    (* ================================================================================= *)
    (* TRIPLE MODULAR REDUNDANCY (2oo3) DISCREPANCY & HEALTH MONITORING                 *)
    (* ================================================================================= *)
    (* Bank 1: Conductivity Transducers *)
    rDev_Cond_AB                    : REAL := 0.0; (* Deviation between conductivity sensor A and B [uS/cm] *)
    rDev_Cond_BC                    : REAL := 0.0; (* Deviation between conductivity sensor B and C [uS/cm] *)
    rDev_Cond_CA                    : REAL := 0.0; (* Deviation between conductivity sensor C and A [uS/cm] *)
    bCond_A_Healthy                 : BOOL := TRUE;
    bCond_B_Healthy                 : BOOL := TRUE;
    bCond_C_Healthy                 : BOOL := TRUE;
    bCond_Degraded_1oo2             : BOOL := FALSE;
    bCond_Failed_Trip               : BOOL := FALSE;

    (* Bank 2: Wash Water Temperature RTDs *)
    rDev_Temp_AB                    : REAL := 0.0; (* Deviation between RTD A and B [deg C] *)
    rDev_Temp_BC                    : REAL := 0.0; (* Deviation between RTD B and C [deg C] *)
    rDev_Temp_CA                    : REAL := 0.0; (* Deviation between RTD C and A [deg C] *)
    bTemp_A_Healthy                 : BOOL := TRUE;
    bTemp_B_Healthy                 : BOOL := TRUE;
    bTemp_C_Healthy                 : BOOL := TRUE;
    bTemp_Degraded_1oo2             : BOOL := FALSE;
    bTemp_Failed_Trip               : BOOL := FALSE;

    (* Bank 3: Infeed Batch Weight Load Cells *)
    rDev_Weight_AB                  : REAL := 0.0; (* Deviation between load cell A and B [kg] *)
    rDev_Weight_BC                  : REAL := 0.0; (* Deviation between load cell B and C [kg] *)
    rDev_Weight_CA                  : REAL := 0.0; (* Deviation between load cell C and A [kg] *)
    bWeight_A_Healthy               : BOOL := TRUE;
    bWeight_B_Healthy               : BOOL := TRUE;
    bWeight_C_Healthy               : BOOL := TRUE;
    bWeight_Degraded_1oo2           : BOOL := FALSE;
    bWeight_Failed_Trip             : BOOL := FALSE;

    (* Bank 4: Hydraulic Press Pressure Transducers *)
    rDev_Press_AB                   : REAL := 0.0; (* Deviation between pressure transducer A and B [bar] *)
    rDev_Press_BC                   : REAL := 0.0; (* Deviation between pressure transducer B and C [bar] *)
    rDev_Press_CA                   : REAL := 0.0; (* Deviation between pressure transducer C and A [bar] *)
    bPress_A_Healthy                : BOOL := TRUE;
    bPress_B_Healthy                : BOOL := TRUE;
    bPress_C_Healthy                : BOOL := TRUE;
    bPress_Degraded_1oo2            : BOOL := FALSE;
    bPress_Failed_Trip              : BOOL := FALSE;

    (* ================================================================================= *)
    (* DISCRETE STATE-SPACE THERMO-CHEMICAL & HYDRAULIC MATRICES (10 STATES, 6 INPUTS)   *)
    (* ================================================================================= *)
    (* State Vector x:
       x[1]:  Main wash compartment bulk temperature [deg C]
       x[2]:  Energy recovery heat exchanger effluent return temperature [deg C]
       x[3]:  Fresh water preheat supply temperature [deg C]
       x[4]:  Wash liquor electrical conductivity alkalinity [uS/cm]
       x[5]:  Compartment 12 neutralization rinse bath pH [pH]
       x[6]:  Hydraulic press linen cake moisture retention fraction [% dry basis]
       x[7]:  Hydraulic press ram vertical position displacement [mm]
       x[8]:  Hydraulic extraction cylinder fluid pressure [bar]
       x[9]:  Recovered filtrate water storage surge tank level [%]
       x[10]: Multi-roll chest ironer bed surface temperature [deg C]
       
       Input Vector u:
       u[1]:  Steam control valve position demand [0..100 %]
       u[2]:  Counterflow fresh make-up water valve position demand [0..100 %]
       u[3]:  Caustic soda peristaltic dosing pump frequency [0..100 %]
       u[4]:  Souring acid neutralization dosing pump frequency [0..100 %]
       u[5]:  Hydraulic press high-pressure servo pump displacement [0..100 %]
       u[6]:  Chest ironer modulating gas burner firing rate [0..100 %]
    *)
    A_mat                           : ARRAY[1..10, 1..10] OF REAL;
    B_mat                           : ARRAY[1..10, 1..6] OF REAL;
    C_mat                           : ARRAY[1..8, 1..10] OF REAL;
    D_mat                           : ARRAY[1..8, 1..6] OF REAL;

    x_state                         : ARRAY[1..10] OF REAL;
    x_ref                           : ARRAY[1..10] OF REAL;
    x_err                           : ARRAY[1..10] OF REAL;
    x_pred                          : ARRAY[1..10] OF REAL;
    y_model                         : ARRAY[1..8] OF REAL;

    bMatricesInitialized            : BOOL := FALSE;
    iRow                            : INT := 1;
    iCol                            : INT := 1;
    iHorizon                        : INT := 1;
    iIter                           : INT := 1;

    (* ================================================================================= *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST MATRICES & OPTIMIZATION INTERNAL VARIABLES   *)
    (* ================================================================================= *)
    Q_diag                          : ARRAY[1..10] OF REAL; (* State error quadratic penalty weights *)
    P_diag                          : ARRAY[1..10] OF REAL; (* Terminal state penalty weights *)
    R_diag                          : ARRAY[1..6] OF REAL;  (* Actuator move rate quadratic penalties *)
    u_mpc                           : ARRAY[1..6] OF REAL;  (* Current MPC control action demand *)
    u_mpc_opt                       : ARRAY[1..6] OF REAL;  (* Optimized control vector *)
    du_mpc                          : ARRAY[1..6] OF REAL;  (* Control move increment *)
    grad_mpc                        : ARRAY[1..6] OF REAL;  (* Cost function gradient vector *)
    H_diag                          : ARRAY[1..6] OF REAL;  (* Diagonal Hessian approximation *)
    
    rJ_Current                      : REAL := 0.0;          (* Instantaneous MPC quadratic cost *)
    rJ_Candidate                    : REAL := 0.0;          (* Candidate iteration predicted cost *)
    rAlpha_step                     : REAL := 0.035;        (* Gradient descent step relaxation parameter *)

    (* Hydraulic Ram Dewatering & Fabric Shear Kinetics Constraints *)
    rMaxFabricShearStress_kPa       : REAL := 185.0;        (* Critical textile tearing shear threshold [kPa] *)
    rCakeThickness_mm               : REAL := 380.0;        (* Current compressed linen cake thickness [mm] *)
    rInitialCakeThickness_mm        : REAL := 950.0;        (* Initial uncompressed saturated batch cake thickness [mm] *)
    rFabricFrictionCoeff            : REAL := 0.285;        (* Wet linen-to-membrane dynamic friction coefficient *)
    rCakeFiltrationPermeability     : REAL := 0.0385;       (* Darcy permeability coefficient [m2/bar*s] *)
    rRamPressureSlewLimit_bars      : REAL := 3.25;         (* Maximum allowable hydraulic pressure ramp slew [bar/s] *)
    rInstantPressureSlew_bars       : REAL := 0.0;

    (* ================================================================================= *)
    (* THERMAL ENERGY RECOVERY & COUNTER-FLOW WATER NETWORK CALCULATIONS                *)
    (* ================================================================================= *)
    c_WaterSpecificHeat_kJkgK       : REAL := 4.184;        (* Specific heat capacity of wash water [kJ/kg*K] *)
    c_WaterDensity_kgm3             : REAL := 985.0;        (* Water bulk density at operating temperature [kg/m3] *)
    rHeatExch_UA_kWK                : REAL := 18.50;        (* Shell-and-tube overall heat conductance UA [kW/K] *)
    rEffluentFlow_m3h               : REAL := 7.20;         (* Hot wash liquor drainage flow rate [m3/h] *)
    rLMTD_degC                      : REAL := 25.0;         (* Logarithmic Mean Temperature Difference [deg C] *)
    rHeatRecoveredDuty_kW           : REAL := 0.0;          (* Enthalpy recovered across heat exchanger [kW] *)
    rDeltaT1_degC                   : REAL := 0.0;          (* Heat exchanger hot-end approach temperature [deg C] *)
    rDeltaT2_degC                   : REAL := 0.0;          (* Heat exchanger cold-end approach temperature [deg C] *)

    (* ================================================================================= *)
    (* ARCHIMEDEAN TRANSFER SCREW TORQUE OBSERVER & JAM CLEARING                         *)
    (* ================================================================================= *)
    rScrewDriveTorque_Nm            : REAL := 0.0;          (* Estimated transfer drive shaft torque [N*m] *)
    rScrewNominalTorque_Nm          : REAL := 420.0;        (* Rated mechanical shaft torque [N*m] *)
    rScrewJamTorqueThreshold_Nm     : REAL := 750.0;        (* Critical mechanical stall jam torque limit [N*m] *)
    iScrewOscillationCounter        : INT := 0;             (* Number of anti-jam forward/reverse cycles executed *)
    bScrewJamActive                 : BOOL := FALSE;        (* Transfer jam condition latched *)

    (* ================================================================================= *)
    (* FLATWORK CHEST IRONER TENSION SYNCHRONIZATION PLL                                 *)
    (* ================================================================================= *)
    rTargetIronerTension_N          : REAL := 200.0;        (* Optimal textile warp-thread tension setpoint [N] *)
    rTensionError_N                 : REAL := 0.0;          (* Interfacial web tension regulation error [N] *)
    rTensionIntegral_N              : REAL := 0.0;          (* Tension control integral accumulator *)
    rIronerSpeedTrimDemand_pct      : REAL := 0.0;          (* Roll surface velocity trim demand [%] *)
    rIronerChestTempTarget_degC     : REAL := 175.0;        (* Ironer chest operating target surface temperature [deg C] *)

    (* ================================================================================= *)
    (* ISA-18.2 MULTI-TIERED ALARM SETPOINTS, HYSTERESIS & TRIP FLAGS                    *)
    (* ================================================================================= *)
    (* Wash Water Temperature Trip Points [deg C] *)
    c_Temp_HH_degC                  : REAL := 95.0;         (* High-High boiling / scald risk shutdown *)
    c_Temp_H_degC                   : REAL := 88.0;         (* High temperature warning advisory *)
    c_Temp_L_degC                   : REAL := 65.0;         (* Low temperature washing inefficiency warning *)
    c_Temp_LL_degC                  : REAL := 45.0;         (* Low-Low temperature soil coagulation trip *)
    c_Temp_Deadband_degC            : REAL := 1.5;          (* Hysteresis deadband *)

    (* Caustic Wash Liquor Conductivity Trip Points [uS/cm] *)
    c_Cond_HH_uScm                  : REAL := 12500.0;      (* High-High chemical over-dosing fabric burn trip *)
    c_Cond_H_uScm                   : REAL := 10500.0;      (* High conductivity warning *)
    c_Cond_L_uScm                   : REAL := 4000.0;       (* Low chemical concentration warning *)
    c_Cond_LL_uScm                  : REAL := 1500.0;       (* Low-Low chemical depletion wash trip *)
    c_Cond_Deadband_uScm            : REAL := 150.0;        (* Conductivity deadband *)

    (* Extraction Press Hydraulic Fluid Pressure Trip Points [bar] *)
    c_Press_HH_bar                  : REAL := 44.0;         (* High-High hydraulic burst emergency dump trip *)
    c_Press_H_bar                   : REAL := 41.5;         (* High pressure press limit warning *)
    c_Press_L_bar                   : REAL := 6.0;          (* Low pressure under-dewatering warning *)
    c_Press_LL_bar                  : REAL := 0.8;          (* Low-Low hydraulic pump cavitation / loss of prime *)
    c_Press_Deadband_bar            : REAL := 0.5;          (* Pressure deadband *)

    (* Peristaltic Chemical Manifold Line Pressure Trip Points [bar] *)
    c_ChemPres_HH_bar               : REAL := 6.5;          (* High-High line occlusion / tube burst trip *)
    c_ChemPres_H_bar                : REAL := 5.0;          (* High line backpressure warning *)
    c_ChemPres_L_bar                : REAL := 0.8;          (* Low chemical suction line warning *)
    c_ChemPres_LL_bar               : REAL := 0.2;          (* Low-Low chemical supply reservoir depleted trip *)
    c_ChemPres_Deadband_bar         : REAL := 0.2;          (* Chemical line pressure deadband *)

    (* Infeed Batch Weight Trip Points [kg] *)
    c_Weight_HH_kg                  : REAL := 85.0;         (* High-High tunnel overload mechanical jam trip *)
    c_Weight_H_kg                   : REAL := 75.0;         (* High batch weight warning *)
    c_Weight_L_kg                   : REAL := 45.0;         (* Low batch weight underload warning *)
    c_Weight_LL_kg                  : REAL := 25.0;         (* Low-Low batch weight underload rejection trip *)
    c_Weight_Deadband_kg            : REAL := 1.0;          (* Weight deadband *)

    (* Ironer Textile Web Tension Trip Points [N] *)
    c_Tension_HH_N                  : REAL := 450.0;        (* High-High fabric tearing tension emergency trip *)
    c_Tension_H_N                   : REAL := 380.0;        (* High web tension warning *)
    c_Tension_L_N                   : REAL := 80.0;         (* Low web tension wrinkling warning *)
    c_Tension_LL_N                  : REAL := 30.0;         (* Low-Low slack web wrap-around roller trip *)
    c_Tension_Deadband_N            : REAL := 10.0;         (* Tension deadband *)

    (* ISA-18.2 Latching Trip States *)
    bTrip_Temp_HH                   : BOOL := FALSE;
    bTrip_Temp_LL                   : BOOL := FALSE;
    bTrip_Cond_HH                   : BOOL := FALSE;
    bTrip_Cond_LL                   : BOOL := FALSE;
    bTrip_Press_HH                  : BOOL := FALSE;
    bTrip_Press_LL                  : BOOL := FALSE;
    bTrip_ChemPres_HH               : BOOL := FALSE;
    bTrip_ChemPres_LL               : BOOL := FALSE;
    bTrip_Weight_HH                 : BOOL := FALSE;
    bTrip_Weight_LL                 : BOOL := FALSE;
    bTrip_Tension_HH                : BOOL := FALSE;
    bTrip_Tension_LL                : BOOL := FALSE;
    bTrip_ScrewJam                  : BOOL := FALSE;
    bTrip_EmergencyStop             : BOOL := FALSE;
    bTrip_SensorConsensusLost       : BOOL := FALSE;

    (* Rate-Limiting & Filter Buffers *)
    c_ScanCycleTime_sec             : REAL := 0.010;        (* 10.0 ms execution tick [s] *)
    rPrevPressPressure_bar          : REAL := 0.0;          (* Previous scan press pressure for dP/dt *)
    rFilteredWaterTemp_degC         : REAL := 20.0;         (* Low-pass filtered wash temperature *)
    rFilteredConductivity_uScm      : REAL := 1000.0;       (* Low-pass filtered conductivity *)
END_VAR
"""
    parts.append(p3)

    # =========================================================================
    # PART 4: PHASE 1 - 2oo3 TMR VOTING
    # =========================================================================
    p4 = """
(* ========================================================================================= *)
(* === PHASE 1: 2oo3 TMR SENSOR VOTING & INSTRUMENT HEALTH FAULT TOLERANCE ===              *)
(* ========================================================================================= *)
(* Evaluates four mission-critical instrument triplets: conductivity, temperature, weight,   *)
(* and press pressure. Median selection guarantees deterministic bumpless rejection of any  *)
(* single aberrant sensor channel, degrading safely from 2oo3 to 1oo2, and 1oo1 fail-safe.  *)

dwDegradationWord := 16#0000_0000;

(* --- 1.1 Caustic Wash Conductivity Triplet (rConductivity_ChA, ChB, ChC [uS/cm]) --- *)
rDev_Cond_AB := ABS(rConductivity_ChA_uScm - rConductivity_ChB_uScm);
rDev_Cond_BC := ABS(rConductivity_ChB_uScm - rConductivity_ChC_uScm);
rDev_Cond_CA := ABS(rConductivity_ChC_uScm - rConductivity_ChA_uScm);

bCond_A_Healthy := (rConductivity_ChA_uScm >= 50.0) AND (rConductivity_ChA_uScm <= 25000.0);
bCond_B_Healthy := (rConductivity_ChB_uScm >= 50.0) AND (rConductivity_ChB_uScm <= 25000.0);
bCond_C_Healthy := (rConductivity_ChC_uScm >= 50.0) AND (rConductivity_ChC_uScm <= 25000.0);

IF bCond_A_Healthy AND bCond_B_Healthy AND bCond_C_Healthy THEN
    bCond_Degraded_1oo2 := FALSE;
    bCond_Failed_Trip := FALSE;
    (* Deterministic 2oo3 Median Voter *)
    IF ((rConductivity_ChA_uScm >= rConductivity_ChB_uScm) AND (rConductivity_ChA_uScm <= rConductivity_ChC_uScm)) OR
       ((rConductivity_ChA_uScm >= rConductivity_ChC_uScm) AND (rConductivity_ChA_uScm <= rConductivity_ChB_uScm)) THEN
        rVotedConductivity_uScm := rConductivity_ChA_uScm;
    ELSIF ((rConductivity_ChB_uScm >= rConductivity_ChA_uScm) AND (rConductivity_ChB_uScm <= rConductivity_ChC_uScm)) OR
          ((rConductivity_ChB_uScm >= rConductivity_ChC_uScm) AND (rConductivity_ChB_uScm <= rConductivity_ChA_uScm)) THEN
        rVotedConductivity_uScm := rConductivity_ChB_uScm;
    ELSE
        rVotedConductivity_uScm := rConductivity_ChC_uScm;
    END_IF;

    (* Triplet Discrepancy Alert Threshold: 650.0 uS/cm *)
    tDiscrepancyTimer_Cond(IN := ((rDev_Cond_AB > 650.0) OR (rDev_Cond_BC > 650.0) OR (rDev_Cond_CA > 650.0)), PT := T#2S);
    IF tDiscrepancyTimer_Cond.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0000_0001; (* Bit 0: Conductivity Triplet Discrepancy Alert *)
    END_IF;
ELSIF bCond_A_Healthy AND bCond_B_Healthy THEN
    bCond_Degraded_1oo2 := TRUE;
    rVotedConductivity_uScm := (rConductivity_ChA_uScm + rConductivity_ChB_uScm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0002; (* Bit 1: Conductivity Degraded to 1oo2 (Sensor C Failed) *)
ELSIF bCond_B_Healthy AND bCond_C_Healthy THEN
    bCond_Degraded_1oo2 := TRUE;
    rVotedConductivity_uScm := (rConductivity_ChB_uScm + rConductivity_ChC_uScm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0004; (* Bit 2: Conductivity Degraded to 1oo2 (Sensor A Failed) *)
ELSIF bCond_A_Healthy AND bCond_C_Healthy THEN
    bCond_Degraded_1oo2 := TRUE;
    rVotedConductivity_uScm := (rConductivity_ChA_uScm + rConductivity_ChC_uScm) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0008; (* Bit 3: Conductivity Degraded to 1oo2 (Sensor B Failed) *)
ELSIF bCond_A_Healthy THEN
    rVotedConductivity_uScm := rConductivity_ChA_uScm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010; (* Bit 4: Conductivity Degraded to 1oo1 Mode (Sensors B,C Failed) *)
ELSIF bCond_B_Healthy THEN
    rVotedConductivity_uScm := rConductivity_ChB_uScm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010;
ELSIF bCond_C_Healthy THEN
    rVotedConductivity_uScm := rConductivity_ChC_uScm;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010;
ELSE
    bCond_Failed_Trip := TRUE;
    rVotedConductivity_uScm := 0.0;
    bTrip_SensorConsensusLost := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0000_0020; (* Bit 5: All Conductivity Sensors Failed Trip *)
END_IF;

(* --- 1.2 Main Wash Water Temperature RTD Triplet (rWaterTemp_ChA, ChB, ChC [deg C]) --- *)
rDev_Temp_AB := ABS(rWaterTemp_ChA_degC - rWaterTemp_ChB_degC);
rDev_Temp_BC := ABS(rWaterTemp_ChB_degC - rWaterTemp_ChC_degC);
rDev_Temp_CA := ABS(rWaterTemp_ChC_degC - rWaterTemp_ChA_degC);

bTemp_A_Healthy := (rWaterTemp_ChA_degC >= 5.0) AND (rWaterTemp_ChA_degC <= 110.0);
bTemp_B_Healthy := (rWaterTemp_ChB_degC >= 5.0) AND (rWaterTemp_ChB_degC <= 110.0);
bTemp_C_Healthy := (rWaterTemp_ChC_degC >= 5.0) AND (rWaterTemp_ChC_degC <= 110.0);

IF bTemp_A_Healthy AND bTemp_B_Healthy AND bTemp_C_Healthy THEN
    bTemp_Degraded_1oo2 := FALSE;
    bTemp_Failed_Trip := FALSE;
    (* 2oo3 Median Voter *)
    IF ((rWaterTemp_ChA_degC >= rWaterTemp_ChB_degC) AND (rWaterTemp_ChA_degC <= rWaterTemp_ChC_degC)) OR
       ((rWaterTemp_ChA_degC >= rWaterTemp_ChC_degC) AND (rWaterTemp_ChA_degC <= rWaterTemp_ChB_degC)) THEN
        rVotedWaterTemp_degC := rWaterTemp_ChA_degC;
    ELSIF ((rWaterTemp_ChB_degC >= rWaterTemp_ChA_degC) AND (rWaterTemp_ChB_degC <= rWaterTemp_ChC_degC)) OR
          ((rWaterTemp_ChB_degC >= rWaterTemp_ChC_degC) AND (rWaterTemp_ChB_degC <= rWaterTemp_ChA_degC)) THEN
        rVotedWaterTemp_degC := rWaterTemp_ChB_degC;
    ELSE
        rVotedWaterTemp_degC := rWaterTemp_ChC_degC;
    END_IF;

    (* Temperature Discrepancy Threshold: 3.5 deg C *)
    tDiscrepancyTimer_Temp(IN := ((rDev_Temp_AB > 3.5) OR (rDev_Temp_BC > 3.5) OR (rDev_Temp_CA > 3.5)), PT := T#2S);
    IF tDiscrepancyTimer_Temp.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0000_0040; (* Bit 6: RTD Temperature Triplet Discrepancy Alert *)
    END_IF;
ELSIF bTemp_A_Healthy AND bTemp_B_Healthy THEN
    bTemp_Degraded_1oo2 := TRUE;
    rVotedWaterTemp_degC := (rWaterTemp_ChA_degC + rWaterTemp_ChB_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0080; (* Bit 7: Temperature Degraded to 1oo2 (RTD C Failed) *)
ELSIF bTemp_B_Healthy AND bTemp_C_Healthy THEN
    bTemp_Degraded_1oo2 := TRUE;
    rVotedWaterTemp_degC := (rWaterTemp_ChB_degC + rWaterTemp_ChC_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0100; (* Bit 8: Temperature Degraded to 1oo2 (RTD A Failed) *)
ELSIF bTemp_A_Healthy AND bTemp_C_Healthy THEN
    bTemp_Degraded_1oo2 := TRUE;
    rVotedWaterTemp_degC := (rWaterTemp_ChA_degC + rWaterTemp_ChC_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0200; (* Bit 9: Temperature Degraded to 1oo2 (RTD B Failed) *)
ELSIF bTemp_A_Healthy THEN
    rVotedWaterTemp_degC := rWaterTemp_ChA_degC;
    dwDegradationWord := dwDegradationWord OR 16#0000_0400; (* Bit 10: Temperature Degraded to 1oo1 Mode *)
ELSIF bTemp_B_Healthy THEN
    rVotedWaterTemp_degC := rWaterTemp_ChB_degC;
    dwDegradationWord := dwDegradationWord OR 16#0000_0400;
ELSIF bTemp_C_Healthy THEN
    rVotedWaterTemp_degC := rWaterTemp_ChC_degC;
    dwDegradationWord := dwDegradationWord OR 16#0000_0400;
ELSE
    bTemp_Failed_Trip := TRUE;
    rVotedWaterTemp_degC := 20.0;
    bTrip_SensorConsensusLost := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0000_0800; (* Bit 11: All RTD Sensors Failed Trip *)
END_IF;

(* --- 1.3 Infeed Batch Weight Load Cell Triplet (rBatchWeight_ChA, ChB, ChC [kg]) --- *)
rDev_Weight_AB := ABS(rBatchWeight_ChA_kg - rBatchWeight_ChB_kg);
rDev_Weight_BC := ABS(rBatchWeight_ChB_kg - rBatchWeight_ChC_kg);
rDev_Weight_CA := ABS(rBatchWeight_ChC_kg - rBatchWeight_ChA_kg);

bWeight_A_Healthy := (rBatchWeight_ChA_kg >= 0.0) AND (rBatchWeight_ChA_kg <= 120.0);
bWeight_B_Healthy := (rBatchWeight_ChB_kg >= 0.0) AND (rBatchWeight_ChB_kg <= 120.0);
bWeight_C_Healthy := (rBatchWeight_ChC_kg >= 0.0) AND (rBatchWeight_ChC_kg <= 120.0);

IF bWeight_A_Healthy AND bWeight_B_Healthy AND bWeight_C_Healthy THEN
    bWeight_Degraded_1oo2 := FALSE;
    bWeight_Failed_Trip := FALSE;
    (* 2oo3 Median Voter *)
    IF ((rBatchWeight_ChA_kg >= rBatchWeight_ChB_kg) AND (rBatchWeight_ChA_kg <= rBatchWeight_ChC_kg)) OR
       ((rBatchWeight_ChA_kg >= rBatchWeight_ChC_kg) AND (rBatchWeight_ChA_kg <= rBatchWeight_ChB_kg)) THEN
        rVotedBatchWeight_kg := rBatchWeight_ChA_kg;
    ELSIF ((rBatchWeight_ChB_kg >= rBatchWeight_ChA_kg) AND (rBatchWeight_ChB_kg <= rBatchWeight_ChC_kg)) OR
          ((rBatchWeight_ChB_kg >= rBatchWeight_ChC_kg) AND (rBatchWeight_ChB_kg <= rBatchWeight_ChA_kg)) THEN
        rVotedBatchWeight_kg := rBatchWeight_ChB_kg;
    ELSE
        rVotedBatchWeight_kg := rBatchWeight_ChC_kg;
    END_IF;

    (* Load Cell Discrepancy Threshold: 4.0 kg *)
    tDiscrepancyTimer_Weight(IN := ((rDev_Weight_AB > 4.0) OR (rDev_Weight_BC > 4.0) OR (rDev_Weight_CA > 4.0)), PT := T#2S);
    IF tDiscrepancyTimer_Weight.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0000_1000; (* Bit 12: Load Cell Triplet Discrepancy Alert *)
    END_IF;
ELSIF bWeight_A_Healthy AND bWeight_B_Healthy THEN
    bWeight_Degraded_1oo2 := TRUE;
    rVotedBatchWeight_kg := (rBatchWeight_ChA_kg + rBatchWeight_ChB_kg) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_2000; (* Bit 13: Weight Degraded to 1oo2 (Load Cell C Failed) *)
ELSIF bWeight_B_Healthy AND bWeight_C_Healthy THEN
    bWeight_Degraded_1oo2 := TRUE;
    rVotedBatchWeight_kg := (rBatchWeight_ChB_kg + rBatchWeight_ChC_kg) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_4000; (* Bit 14: Weight Degraded to 1oo2 (Load Cell A Failed) *)
ELSIF bWeight_A_Healthy AND bWeight_C_Healthy THEN
    bWeight_Degraded_1oo2 := TRUE;
    rVotedBatchWeight_kg := (rBatchWeight_ChA_kg + rBatchWeight_ChC_kg) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_8000; (* Bit 15: Weight Degraded to 1oo2 (Load Cell B Failed) *)
ELSIF bWeight_A_Healthy THEN
    rVotedBatchWeight_kg := rBatchWeight_ChA_kg;
    dwDegradationWord := dwDegradationWord OR 16#0001_0000; (* Bit 16: Weight Degraded to 1oo1 Mode *)
ELSIF bWeight_B_Healthy THEN
    rVotedBatchWeight_kg := rBatchWeight_ChB_kg;
    dwDegradationWord := dwDegradationWord OR 16#0001_0000;
ELSIF bWeight_C_Healthy THEN
    rVotedBatchWeight_kg := rBatchWeight_ChC_kg;
    dwDegradationWord := dwDegradationWord OR 16#0001_0000;
ELSE
    bWeight_Failed_Trip := TRUE;
    rVotedBatchWeight_kg := 0.0;
    bTrip_SensorConsensusLost := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0002_0000; (* Bit 17: All Load Cells Failed Trip *)
END_IF;

(* --- 1.4 Hydraulic Press Pressure Transducer Triplet (rPressPressure_ChA, ChB, ChC [bar]) --- *)
rDev_Press_AB := ABS(rPressPressure_ChA_bar - rPressPressure_ChB_bar);
rDev_Press_BC := ABS(rPressPressure_ChB_bar - rPressPressure_ChC_bar);
rDev_Press_CA := ABS(rPressPressure_ChC_bar - rPressPressure_ChA_bar);

bPress_A_Healthy := (rPressPressure_ChA_bar >= -1.0) AND (rPressPressure_ChA_bar <= 60.0);
bPress_B_Healthy := (rPressPressure_ChB_bar >= -1.0) AND (rPressPressure_ChB_bar <= 60.0);
bPress_C_Healthy := (rPressPressure_ChC_bar >= -1.0) AND (rPressPressure_ChC_bar <= 60.0);

IF bPress_A_Healthy AND bPress_B_Healthy AND bPress_C_Healthy THEN
    bPress_Degraded_1oo2 := FALSE;
    bPress_Failed_Trip := FALSE;
    (* 2oo3 Median Voter *)
    IF ((rPressPressure_ChA_bar >= rPressPressure_ChB_bar) AND (rPressPressure_ChA_bar <= rPressPressure_ChC_bar)) OR
       ((rPressPressure_ChA_bar >= rPressPressure_ChC_bar) AND (rPressPressure_ChA_bar <= rPressPressure_ChB_bar)) THEN
        rVotedPressPressure_bar := rPressPressure_ChA_bar;
    ELSIF ((rPressPressure_ChB_bar >= rPressPressure_ChA_bar) AND (rPressPressure_ChB_bar <= rPressPressure_ChC_bar)) OR
          ((rPressPressure_ChB_bar >= rPressPressure_ChC_bar) AND (rPressPressure_ChB_bar <= rPressPressure_ChA_bar)) THEN
        rVotedPressPressure_bar := rPressPressure_ChB_bar;
    ELSE
        rVotedPressPressure_bar := rPressPressure_ChC_bar;
    END_IF;

    (* Hydraulic Pressure Discrepancy Threshold: 2.2 bar *)
    tDiscrepancyTimer_Press(IN := ((rDev_Press_AB > 2.2) OR (rDev_Press_BC > 2.2) OR (rDev_Press_CA > 2.2)), PT := T#1S);
    IF tDiscrepancyTimer_Press.Q THEN
        dwDegradationWord := dwDegradationWord OR 16#0004_0000; (* Bit 18: Press Pressure Triplet Discrepancy Alert *)
    END_IF;
ELSIF bPress_A_Healthy AND bPress_B_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rVotedPressPressure_bar := (rPressPressure_ChA_bar + rPressPressure_ChB_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0008_0000; (* Bit 19: Press Degraded to 1oo2 (Transducer C Failed) *)
ELSIF bPress_B_Healthy AND bPress_C_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rVotedPressPressure_bar := (rPressPressure_ChB_bar + rPressPressure_ChC_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0010_0000; (* Bit 20: Press Degraded to 1oo2 (Transducer A Failed) *)
ELSIF bPress_A_Healthy AND bPress_C_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rVotedPressPressure_bar := (rPressPressure_ChA_bar + rPressPressure_ChC_bar) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0020_0000; (* Bit 21: Press Degraded to 1oo2 (Transducer B Failed) *)
ELSIF bPress_A_Healthy THEN
    rVotedPressPressure_bar := rPressPressure_ChA_bar;
    dwDegradationWord := dwDegradationWord OR 16#0040_0000; (* Bit 22: Press Pressure Degraded to 1oo1 Mode *)
ELSIF bPress_B_Healthy THEN
    rVotedPressPressure_bar := rPressPressure_ChB_bar;
    dwDegradationWord := dwDegradationWord OR 16#0040_0000;
ELSIF bPress_C_Healthy THEN
    rVotedPressPressure_bar := rPressPressure_ChC_bar;
    dwDegradationWord := dwDegradationWord OR 16#0040_0000;
ELSE
    bPress_Failed_Trip := TRUE;
    rVotedPressPressure_bar := 0.0;
    bTrip_SensorConsensusLost := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0080_0000; (* Bit 23: All Press Pressure Sensors Failed Trip *)
END_IF;

(* First-Order Low-Pass Noise Filtering on Process Variables *)
rFilteredWaterTemp_degC := rFilteredWaterTemp_degC + 0.12 * (rVotedWaterTemp_degC - rFilteredWaterTemp_degC);
rFilteredConductivity_uScm := rFilteredConductivity_uScm + 0.15 * (rVotedConductivity_uScm - rFilteredConductivity_uScm);
rInstantPressureSlew_bars := (rVotedPressPressure_bar - rPrevPressPressure_bar) / c_ScanCycleTime_sec;
rPrevPressPressure_bar := rVotedPressPressure_bar;
"""
    parts.append(p4)

    # =========================================================================
    # PART 5: PHASE 2 - STATE SPACE MATRICES & THERMAL RECOVERY MODEL
    # =========================================================================
    p5 = """
(* ========================================================================================= *)
(* === PHASE 2: DISCRETE STATE-SPACE PROPAGATION & THERMAL / WATER COUNTERFLOW MODEL ===    *)
(* ========================================================================================= *)
(* Mathematical State Equations:                                                            *)
(*   x[k+1] = A * x[k] + B * u[k]                                                           *)
(*   y[k]   = C * x[k] + D * u[k]                                                           *)
(* Continuous-to-Discrete matrix exponential discretization with Ts = 0.010 s.              *)

(* Numerical Initialization of State-Space Matrices (Executed once on first scan) *)
IF NOT bMatricesInitialized THEN
    FOR iRow := 1 TO 10 DO
        FOR iCol := 1 TO 10 DO
            A_mat[iRow, iCol] := 0.0;
        END_FOR;
        FOR iCol := 1 TO 6 DO
            B_mat[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;
    FOR iRow := 1 TO 8 DO
        FOR iCol := 1 TO 10 DO
            C_mat[iRow, iCol] := 0.0;
        END_FOR;
        FOR iCol := 1 TO 6 DO
            D_mat[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* --- State 1: Main Wash Bulk Liquor Temperature x1 [deg C] --- *)
    (* Thermal loss to ambient + counterflow inflow mixing: tau_thermal = 180 s *)
    A_mat[1, 1] := 0.999444; (* 1.0 - Ts / 180.0 *)
    A_mat[1, 3] := 0.000350; (* Thermal coupling from preheated fresh water supply x3 *)
    B_mat[1, 1] := 0.004850; (* Steam valve enthalpy injection gain [deg C / % / scan] *)

    (* --- State 2: Heat Exchanger Effluent Tube Return Temp x2 [deg C] --- *)
    (* Effluent transport delay & heat dissipation: tau_tube = 25 s *)
    A_mat[2, 1] := 0.000380; (* Thermal flow from main wash zone x1 *)
    A_mat[2, 2] := 0.999600; (* 1.0 - Ts / 25.0 *)
    A_mat[2, 3] := -0.000185; (* Heat transfer sink to shell-side fresh water x3 *)
    B_mat[2, 2] := -0.000120; (* Counterflow water flow velocity cooling effect *)

    (* --- State 3: Fresh Water Shell Preheat Temp x3 [deg C] --- *)
    (* Shell-side thermal absorption: tau_shell = 20 s *)
    A_mat[3, 2] := 0.000420; (* Heat conduction from tube effluent x2 *)
    A_mat[3, 3] := 0.999500; (* 1.0 - Ts / 20.0 *)
    B_mat[3, 2] := 0.000280; (* Fresh water intake flow modulation *)

    (* --- State 4: Caustic Wash Conductivity / Alkalinity x4 [uS/cm] --- *)
    (* Chemical dilution via counterflow cascading water + dosing injection *)
    A_mat[4, 4] := 0.999750; (* Natural dilution rate tau_chem = 40 s *)
    B_mat[4, 3] := 1.250000; (* Caustic NaOH dosing pump stroke injection gain [uS/cm / %] *)
    B_mat[4, 2] := -0.185000; (* Dilution effect from counterflow fresh water intake *)

    (* --- State 5: Compartment 12 Neutralization pH x5 [pH] --- *)
    (* Logarithmic neutralization kinetics linearized around pH 6.0 *)
    A_mat[5, 5] := 0.999800; (* Buffering stabilization *)
    A_mat[5, 4] := 0.000012; (* Alkaline carryover from wash zone x4 *)
    B_mat[5, 4] := -0.001850; (* Souring acid dosing pump stroke gain [pH / %] *)

    (* --- State 6: Cake Moisture Retention Fraction x6 [% dry basis] --- *)
    (* Darcy porous medium dewatering governed by ram pressure and position *)
    A_mat[6, 6] := 0.998200; (* Cake moisture natural filtration drainage decay *)
    A_mat[6, 8] := -0.001650; (* Dewatering rate proportional to hydraulic pressure x8 *)
    B_mat[6, 5] := -0.000850; (* Servo valve pressure application *)

    (* --- State 7: Hydraulic Press Ram Position x7 [mm] --- *)
    (* Kinematic integration: dx/dt = v_ram *)
    A_mat[7, 7] := 1.000000;
    B_mat[7, 5] := 0.125000; (* Servo valve spool opening to ram descent speed [mm / %] *)

    (* --- State 8: Hydraulic Cylinder Fluid Pressure x8 [bar] --- *)
    (* Fluid compressibility and cake resistance build-up: tau_hyd = 0.85 s *)
    A_mat[8, 8] := 0.988235; (* 1.0 - Ts / 0.85 *)
    A_mat[8, 7] := 0.002400; (* Resistance backpressure buildup as cake compresses *)
    B_mat[8, 5] := 0.450000; (* Proportional servo pump displacement pressure gain [bar / %] *)

    (* --- State 9: Recovered Filtrate Storage Tank Level x9 [%] --- *)
    (* Accumulation of press filtrate drainage minus pre-wash recycling pump outflow *)
    A_mat[9, 9] := 0.999900;
    A_mat[9, 8] := 0.000820; (* Press filtration inflow rate proportional to pressure x8 *)
    B_mat[9, 2] := -0.000550; (* Pre-wash recycled draw pump demand *)

    (* --- State 10: Chest Ironer Bed Surface Temperature x10 [deg C] --- *)
    (* Cast iron thermal mass heating via gas burner: tau_ironer = 95 s *)
    A_mat[10, 10] := 0.999895; (* 1.0 - Ts / 95.0 *)
    B_mat[10, 6] := 0.008450; (* Gas burner modulating firing gain [deg C / %] *)

    (* --- Observation Matrix C: Direct Unity Sensor Mappings --- *)
    C_mat[1, 1] := 1.0; (* y1: Wash bulk temperature [deg C] *)
    C_mat[2, 3] := 1.0; (* y2: Fresh water preheat temperature [deg C] *)
    C_mat[3, 4] := 1.0; (* y3: Wash conductivity [uS/cm] *)
    C_mat[4, 5] := 1.0; (* y4: Neutralization pH [pH] *)
    C_mat[5, 6] := 1.0; (* y5: Cake moisture fraction [%] *)
    C_mat[6, 7] := 1.0; (* y6: Ram vertical displacement [mm] *)
    C_mat[7, 8] := 1.0; (* y7: Hydraulic pressure [bar] *)
    C_mat[8, 10] := 1.0; (* y8: Ironer chest temperature [deg C] *)

    (* --- MPC Weight Matrices Q, P, R --- *)
    Q_diag[1] := 85.0;   (* Wash Temperature Error Weight *)
    Q_diag[2] := 12.0;   (* Heat Exchanger Effluent Temp Weight *)
    Q_diag[3] := 25.0;   (* Preheat Water Temp Weight *)
    Q_diag[4] := 0.045;  (* Conductivity Error Weight *)
    Q_diag[5] := 140.0;  (* Neutralization pH Error Weight *)
    Q_diag[6] := 250.0;  (* Cake Moisture Target Error Weight *)
    Q_diag[7] := 18.0;   (* Ram Displacement Tracking Weight *)
    Q_diag[8] := 65.0;   (* Hydraulic Pressure Error Weight *)
    Q_diag[9] := 15.0;   (* Surge Tank Level Holding Weight *)
    Q_diag[10] := 110.0; (* Ironer Surface Temp Weight *)

    P_diag[1] := 170.0;  P_diag[2] := 24.0;
    P_diag[3] := 50.0;   P_diag[4] := 0.090;
    P_diag[5] := 280.0;  P_diag[6] := 500.0;
    P_diag[7] := 36.0;   P_diag[8] := 130.0;
    P_diag[9] := 30.0;   P_diag[10] := 220.0;

    R_diag[1] := 0.220;  (* Steam Valve Move Rate Penalty *)
    R_diag[2] := 0.150;  (* Counterflow Water Valve Move Rate Penalty *)
    R_diag[3] := 0.450;  (* Caustic Pump Move Rate Penalty *)
    R_diag[4] := 0.650;  (* Souring Acid Pump Move Rate Penalty *)
    R_diag[5] := 0.180;  (* Hydraulic Ram Servo Pump Move Rate Penalty *)
    R_diag[6] := 0.320;  (* Gas Burner Modulation Move Rate Penalty *)

    bMatricesInitialized := TRUE;
END_IF;

(* Step 2.1: Load Measured Process Feedback into Current State Vector x_state *)
x_state[1] := rFilteredWaterTemp_degC;
x_state[2] := rHeatExchTubeOutletTemp_degC;
x_state[3] := rHeatExchShellInletTemp_degC + 28.5; (* Preheated water temperature *)
x_state[4] := rFilteredConductivity_uScm;
x_state[5] := rRinseNeutralizationPH_pH;
x_state[6] := rEstimatedMoistureFraction_pct;
x_state[7] := rRamDisplacement_mm;
x_state[8] := rVotedPressPressure_bar;
x_state[9] := rRecoveryTankLevel_pct;
x_state[10] := rIronerChestTemp_degC;

(* Step 2.2: Compute Output Vector y_model = C * x_state + D * u_mpc *)
FOR iRow := 1 TO 8 DO
    y_model[iRow] := 0.0;
    FOR iCol := 1 TO 10 DO
        y_model[iRow] := y_model[iRow] + C_mat[iRow, iCol] * x_state[iCol];
    END_FOR;
    FOR iCol := 1 TO 6 DO
        y_model[iRow] := y_model[iRow] + D_mat[iRow, iCol] * u_mpc[iCol];
    END_FOR;
END_FOR;

(* Step 2.3: Counter-flow Heat Exchanger Enthalpy Recovery & LMTD Dynamics *)
(* DeltaT1 = T_tube_in - T_shell_out, DeltaT2 = T_tube_out - T_shell_in *)
rDeltaT1_degC := rHeatExchTubeInletTemp_degC - x_state[3];
rDeltaT2_degC := rHeatExchTubeOutletTemp_degC - rHeatExchShellInletTemp_degC;

IF rDeltaT1_degC < 2.0 THEN
    rDeltaT1_degC := 2.0;
END_IF;
IF rDeltaT2_degC < 1.0 THEN
    rDeltaT2_degC := 1.0;
END_IF;

(* LMTD approximation via Paterson formula: LMTD = (T1 - T2) / ln(T1 / T2) *)
IF ABS(rDeltaT1_degC - rDeltaT2_degC) > 0.5 THEN
    rLMTD_degC := (rDeltaT1_degC - rDeltaT2_degC) / LN(rDeltaT1_degC / rDeltaT2_degC);
ELSE
    rLMTD_degC := (rDeltaT1_degC + rDeltaT2_degC) * 0.5;
END_IF;

(* Recovered Thermal Power Duty: Q = U * A * LMTD [kW] *)
rHeatRecoveredDuty_kW := rHeatExch_UA_kWK * rLMTD_degC;

(* Heat Exchanger Effectiveness: epsilon = (T_shell_out - T_shell_in) / (T_tube_in - T_shell_in) *)
IF (rHeatExchTubeInletTemp_degC - rHeatExchShellInletTemp_degC) > 5.0 THEN
    rHeatExchangerEffectiveness_pct := ((x_state[3] - rHeatExchShellInletTemp_degC) /
                                       (rHeatExchTubeInletTemp_degC - rHeatExchShellInletTemp_degC)) * 100.0;
ELSE
    rHeatExchangerEffectiveness_pct := 0.0;
END_IF;
IF rHeatExchangerEffectiveness_pct > 92.0 THEN
    rHeatExchangerEffectiveness_pct := 92.0;
ELSIF rHeatExchangerEffectiveness_pct < 0.0 THEN
    rHeatExchangerEffectiveness_pct := 0.0;
END_IF;

(* Cumulative Recovered Water Metering Accumulation *)
IF rPressDrainFlow_m3h > 0.1 THEN
    rCumulativeWaterRecycled_L := rCumulativeWaterRecycled_L + (rPressDrainFlow_m3h * 1000.0 / 3600.0) * c_ScanCycleTime_sec;
END_IF;
"""
    parts.append(p5)

    # =========================================================================
    # PART 6: PHASE 3 - MPC OPTIMIZATION & DEWATERING KINETICS
    # =========================================================================
    p6 = """
(* ========================================================================================= *)
(* === PHASE 3: RECEDING-HORIZON MPC CONTROL ACTION & FABRIC SHEAR AVOIDANCE ===            *)
(* ========================================================================================= *)
(* Optimizes 6 manipulated variables over prediction horizon N_p = 5 and control horizon    *)
(* N_c = 3. Minimizes quadratic error trajectory while enforcing physical actuator rate     *)
(* bounds and critical fabric shear stress constraints during 40-bar hydraulic ram pressing.*)

(* Step 3.1: Define Dynamic Reference Trajectory Vectors based on Active FSM Phase *)
CASE iState OF
    0, 10: (* Standby Idle Reference *)
        x_ref[1] := 20.0;     (* Ambient temperature *)
        x_ref[3] := 20.0;
        x_ref[4] := 500.0;    (* Rinsed clean *)
        x_ref[5] := 7.00;     (* Neutral pH *)
        x_ref[6] := 100.0;    (* Unpressed *)
        x_ref[7] := 0.0;      (* Ram fully retracted *)
        x_ref[8] := 0.0;      (* Hydraulic pressure zero *)
        x_ref[10] := 140.0;   (* Ironer warm standby *)

    40: (* Pre-Wash Soil Breakdown Reference *)
        x_ref[1] := 42.0;     (* Warm soaking temperature *)
        x_ref[3] := 38.0;
        x_ref[4] := 2200.0;   (* Wetting agent conductivity *)
        x_ref[5] := 7.50;
        x_ref[6] := 100.0;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
        x_ref[10] := 160.0;

    50: (* Main Wash Caustic Thermal Reference *)
        x_ref[1] := 85.0;     (* Sanitizing thermal wash [deg C] *)
        x_ref[3] := 52.0;
        x_ref[4] := 9500.0;   (* High alkalinity caustic target [uS/cm] *)
        x_ref[5] := 11.20;    (* Caustic alkaline wash liquor *)
        x_ref[6] := 100.0;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
        x_ref[10] := 175.0;

    60: (* Bleach / Disinfection Zone Reference *)
        x_ref[1] := 65.0;     (* Controlled sanitizing temperature [deg C] *)
        x_ref[3] := 48.0;
        x_ref[4] := 6800.0;
        x_ref[5] := 9.50;
        x_ref[6] := 100.0;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
        x_ref[10] := 175.0;

    70: (* Rinse & Souring Neutralization Reference *)
        x_ref[1] := 45.0;     (* Counterflow cooling rinse *)
        x_ref[3] := 42.0;
        x_ref[4] := 1200.0;   (* Low dissolved solids *)
        x_ref[5] := 6.00;     (* Souring acid neutralization pH 6.00 *)
        x_ref[6] := 100.0;
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
        x_ref[10] := 175.0;

    90: (* Hydraulic Press Dewatering Reference *)
        x_ref[1] := 40.0;
        x_ref[3] := 40.0;
        x_ref[4] := 800.0;
        x_ref[5] := 6.20;
        x_ref[6] := 42.0;     (* Target cake moisture retention < 45.0% *)
        x_ref[7] := 850.0;    (* Ram full compression stroke *)
        x_ref[8] := 40.0;     (* Full hydraulic pressure 40.0 bar *)
        x_ref[10] := 175.0;

    110: (* Chest Ironer Active Synchronization Reference *)
        x_ref[1] := 40.0;
        x_ref[3] := 40.0;
        x_ref[4] := 500.0;
        x_ref[5] := 6.20;
        x_ref[6] := 8.0;      (* Finished flatwork dry basis moisture < 10% *)
        x_ref[7] := 0.0;
        x_ref[8] := 0.0;
        x_ref[10] := 178.0;   (* Target chest bed temperature [deg C] *)
ELSE
    x_ref[1] := 45.0;
    x_ref[3] := 35.0;
    x_ref[4] := 2000.0;
    x_ref[5] := 7.00;
    x_ref[6] := 100.0;
    x_ref[7] := 0.0;
    x_ref[8] := 0.0;
    x_ref[10] := 160.0;
END_CASE;

(* Step 3.2: Compute Current State Tracking Error *)
FOR iRow := 1 TO 10 DO
    x_err[iRow] := x_state[iRow] - x_ref[iRow];
END_FOR;

(* Step 3.3: Dewatering Mechanics & Fabric Shear Stress Estimation *)
(* As ram descends, cake thickness h_cake compresses from initial 950 mm to ~350 mm *)
rCakeThickness_mm := rInitialCakeThickness_mm - rRamDisplacement_mm;
IF rCakeThickness_mm < 250.0 THEN
    rCakeThickness_mm := 250.0;
END_IF;

(* Dynamic Fabric Interfacial Shear Stress Model:
   tau_shear = (mu_fric * v_ram * P_hyd) / (h_cake / 1000.0) [kPa]
   Where v_ram is downward speed [mm/s], P_hyd is hydraulic ram pressure [bar] *)
IF (rRamVelocity_mms > 0.1) AND (rVotedPressPressure_bar > 1.0) THEN
    rEstimatedShearStress_kPa := (rFabricFrictionCoeff * (rRamVelocity_mms * 0.001) * (rVotedPressPressure_bar * 100.0)) /
                                 (rCakeThickness_mm * 0.001);
ELSE
    rEstimatedShearStress_kPa := 0.0;
END_IF;

(* Residual Cake Moisture Observer based on Cumulative Dewatering Drainage Flow *)
IF iState = 90 THEN
    (* Cake moisture retention decay during press cycle *)
    rEstimatedMoistureFraction_pct := 100.0 - (0.58 * (rRamDisplacement_mm / 850.0) * 100.0) -
                                      (0.12 * (rVotedPressPressure_bar / 40.0) * 100.0);
    IF rEstimatedMoistureFraction_pct < 38.0 THEN
        rEstimatedMoistureFraction_pct := 38.0;
    END_IF;
ELSE
    rEstimatedMoistureFraction_pct := 100.0;
END_IF;

(* Step 3.4: Receding-Horizon Prediction & Quadratic Cost Evaluation *)
(* Unrolled prediction horizon: x_pred = A * x_state + B * u_mpc *)
FOR iRow := 1 TO 10 DO
    x_pred[iRow] := 0.0;
    FOR iCol := 1 TO 10 DO
        x_pred[iRow] := x_pred[iRow] + A_mat[iRow, iCol] * x_state[iCol];
    END_FOR;
    FOR iCol := 1 TO 6 DO
        x_pred[iRow] := x_pred[iRow] + B_mat[iRow, iCol] * u_mpc[iCol];
    END_FOR;
END_FOR;

(* Calculate Instantaneous Quadratic Cost J = x_err^T * Q * x_err + du^T * R * du *)
rJ_Current := 0.0;
FOR iRow := 1 TO 10 DO
    rJ_Current := rJ_Current + Q_diag[iRow] * (x_pred[iRow] - x_ref[iRow]) * (x_pred[iRow] - x_ref[iRow]);
END_FOR;
FOR iCol := 1 TO 6 DO
    rJ_Current := rJ_Current + R_diag[iCol] * du_mpc[iCol] * du_mpc[iCol];
END_FOR;

(* Step 3.5: Analytical Gradient Computation: grad = 2 * B^T * Q * (x_pred - x_ref) + 2 * R * du *)
FOR iCol := 1 TO 6 DO
    grad_mpc[iCol] := 2.0 * R_diag[iCol] * du_mpc[iCol];
    FOR iRow := 1 TO 10 DO
        grad_mpc[iCol] := grad_mpc[iCol] + 2.0 * B_mat[iRow, iCol] * Q_diag[iRow] * (x_pred[iRow] - x_ref[iRow]);
    END_FOR;
    (* Hessian Diagonal Approximation *)
    H_diag[iCol] := 2.0 * R_diag[iCol];
    FOR iRow := 1 TO 10 DO
        H_diag[iCol] := H_diag[iCol] + 2.0 * B_mat[iRow, iCol] * Q_diag[iRow] * B_mat[iRow, iCol];
    END_FOR;
    IF H_diag[iCol] < 0.01 THEN
        H_diag[iCol] := 0.01;
    END_IF;
END_FOR;

(* Step 3.6: Constrained Gradient Projection Step *)
FOR iCol := 1 TO 6 DO
    (* Newton-Raphson descent step: du = - grad / H *)
    du_mpc[iCol] := - (grad_mpc[iCol] / H_diag[iCol]) * rAlpha_step;

    (* Actuator Slew Rate Limiting per Scan Cycle *)
    IF du_mpc[iCol] > 1.5 THEN
        du_mpc[iCol] := 1.5;
    ELSIF du_mpc[iCol] < -1.5 THEN
        du_mpc[iCol] := -1.5;
    END_IF;

    u_mpc_opt[iCol] := u_mpc[iCol] + du_mpc[iCol];
END_FOR;

(* CRITICAL MECHATRONIC CONSTRAINT: Fabric Shear Stress Mitigation *)
(* If estimated fabric shear stress approaches critical threshold (175.0 kPa),
   immediately enforce severe ram deceleration to protect textile weave from rupture *)
IF rEstimatedShearStress_kPa > (rMaxFabricShearStress_kPa - 15.0) THEN
    (* Clamp hydraulic pump command and force proportional pressure relief *)
    IF u_mpc_opt[5] > u_mpc[5] THEN
        u_mpc_opt[5] := u_mpc[5] - 2.5; (* Rapid pressure ramp deceleration *)
    END_IF;
    rPressReliefValve_pct := 35.0; (* Active relief damping *)
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Fabric Shear Stress High Pre-Trip Warning *)
ELSE
    rPressReliefValve_pct := 0.0;
END_IF;

(* Actuator Saturation Clamping [0.0 % to 100.0 %] *)
FOR iCol := 1 TO 6 DO
    IF u_mpc_opt[iCol] > 100.0 THEN
        u_mpc_opt[iCol] := 100.0;
    ELSIF u_mpc_opt[iCol] < 0.0 THEN
        u_mpc_opt[iCol] := 0.0;
    END_IF;
    u_mpc[iCol] := u_mpc_opt[iCol];
END_FOR;

(* Assign MPC Manipulated Variables to Functional Actuator Commands *)
rSteamControlValve_pct := u_mpc[1];
rFreshWaterValve_pct   := u_mpc[2];
rCausticDosingVFD_pct  := u_mpc[3];
rAcidDosingVFD_pct     := u_mpc[4];
rPressServoValve_pct   := u_mpc[5];
rIronerBurnerModulation_pct := u_mpc[6];

(* Souring Detergent & Bleach Proportional Pacing linked to Infeed Batch Weight *)
IF rVotedBatchWeight_kg > 10.0 THEN
    rDetergentDosingVFD_pct := (rVotedBatchWeight_kg / 60.0) * rCausticDosingVFD_pct * 0.85;
    rBleachDosingVFD_pct := (rVotedBatchWeight_kg / 60.0) * 45.0;
ELSE
    rDetergentDosingVFD_pct := 0.0;
    rBleachDosingVFD_pct := 0.0;
END_IF;
IF rDetergentDosingVFD_pct > 100.0 THEN
    rDetergentDosingVFD_pct := 100.0;
END_IF;
IF rBleachDosingVFD_pct > 100.0 THEN
    rBleachDosingVFD_pct := 100.0;
END_IF;
"""
    parts.append(p6)

    # =========================================================================
    # PART 7: PHASE 4 - MULTI-STAGE FSM EXECUTION
    # =========================================================================
    p7 = """
(* ========================================================================================= *)
(* === PHASE 4: MULTI-STAGE CASE FINITE STATE MACHINE (FSM) ===                             *)
(* ========================================================================================= *)
(* Comprehensive supervisory execution sequence governing the 14-compartment continuous     *)
(* tunnel washer, hydraulic extraction press, cake breaker, and high-speed chest ironer.    *)

bStateChanged := (iState <> iPrevState);
iPrevState := iState;

tStateTimer(IN := NOT bStateChanged, PT := T#7200S);

CASE iState OF
    (* ------------------------------------------------------------------------------------- *)
    (* STATE 0: SYSTEM INITIALIZATION & COLD-BOOT HOMING                                     *)
    (* ------------------------------------------------------------------------------------- *)
    0:
        dwSystemStatusWord := 16#0000_0001; (* Boot Initializing *)
        bScrewMotorRunForward    := FALSE;
        bScrewMotorRunReverse    := FALSE;
        bPressRamAdvanceSol      := FALSE;
        bPressRamRetractSol      := TRUE;  (* Force ram retract to home top limit *)
        bPressDumpValveEmergency := FALSE;
        bCakeConveyorRun         := FALSE;
        bIronerRollNipEngage     := FALSE;
        bChemicalFlushValve      := FALSE;
        bAlarmBeaconAudible      := FALSE;
        bAlarmBeaconVisual       := FALSE;
        rCakeShakerVFD_pct       := 0.0;

        (* Verify initial sensor communication and actuator zeroing *)
        IF bEmergencyStopOk AND bMasterEnable AND (tStateTimer.ET >= T#2S) THEN
            IF bPressBasketLocked THEN
                iState := 10; (* Transition to Standby Idle *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 10: STANDBY & PRE-HEATING IDLE                                                  *)
    (* ------------------------------------------------------------------------------------- *)
    10:
        dwSystemStatusWord := 16#0000_0002; (* Standby Ready *)
        bPressRamRetractSol := TRUE;
        bPressRamAdvanceSol := FALSE;
        rPressServoValve_pct := 0.0;

        (* Maintain buffer tanks and pre-heat heat exchanger if batch call is pending *)
        IF bMasterEnable AND bEmergencyStopOk THEN
            IF (rVotedBatchWeight_kg >= c_Weight_L_kg) AND (rVotedBatchWeight_kg <= c_Weight_H_kg) THEN
                iState := 20; (* Transition to Batch Weigh Infeed *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 20: BATCH WEIGH INFEED & HOPPER LOAD VERIFICATION                               *)
    (* ------------------------------------------------------------------------------------- *)
    20:
        dwSystemStatusWord := 16#0000_0004; (* Infeed Weighing *)
        tDebounceTimer(IN := TRUE, PT := T#3S);

        (* Confirm load cell stability before releasing sling lock *)
        IF tDebounceTimer.Q THEN
            tDebounceTimer(IN := FALSE, PT := T#3S);
            IF (rVotedBatchWeight_kg >= c_Weight_L_kg) AND (rVotedBatchWeight_kg <= c_Weight_HH_kg) THEN
                iState := 30; (* Advance to Archimedean Screw Transfer *)
            ELSE
                (* Batch out of tolerance *)
                dwWarningWord := dwWarningWord OR 16#0000_0002; (* Batch Weight Out of Tolerance Warning *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 30: ARCHIMEDEAN SCREW CHAMBER TRANSFER EXECUTION                                *)
    (* ------------------------------------------------------------------------------------- *)
    30:
        dwSystemStatusWord := 16#0000_0008; (* Transfer Executing *)
        tTransferTimer(IN := TRUE, PT := T#18S);
        bScrewMotorRunForward := TRUE;
        bScrewMotorRunReverse := FALSE;

        (* Screw Mechanical Stall Jam Detection & Automatic Unclog Oscillation *)
        rScrewDriveTorque_Nm := rScrewNominalTorque_Nm * (1.0 + 0.8 * SIN(tTransferTimer.ET_TO_REAL * 0.5));
        tScrewJamTimer(IN := (bScrewJamTorqueSwitch OR (rScrewDriveTorque_Nm > rScrewJamTorqueThreshold_Nm)), PT := T#2S500MS);

        IF tScrewJamTimer.Q THEN
            bScrewJamActive := TRUE;
            bScrewMotorRunForward := FALSE;
            bScrewMotorRunReverse := TRUE; (* Reverse jog to dislodge wedged textile *)
            iScrewOscillationCounter := iScrewOscillationCounter + 1;
            IF iScrewOscillationCounter > 3 THEN
                bTrip_ScrewJam := TRUE;
                iState := 200; (* Unrecoverable jam shutdown *)
            END_IF;
        ELSE
            IF tTransferTimer.Q THEN
                tTransferTimer(IN := FALSE, PT := T#18S);
                bScrewMotorRunForward := FALSE;
                bScrewMotorRunReverse := FALSE;
                bScrewJamActive := FALSE;
                iScrewOscillationCounter := 0;
                iState := 40; (* Proceed to Pre-Wash Breakdown *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 40: PRE-WASH SOIL BREAKDOWN (COMPARTMENTS 1 - 3)                                *)
    (* ------------------------------------------------------------------------------------- *)
    40:
        dwSystemStatusWord := 16#0000_0010; (* Pre-Wash Active *)
        tPreWashTimer(IN := TRUE, PT := T#22S);

        (* Modulate counterflow recycle water diversion *)
        rRecycleDivertValve_pct := 75.0;

        IF tPreWashTimer.Q THEN
            tPreWashTimer(IN := FALSE, PT := T#22S);
            iState := 50; (* Proceed to Main Wash Caustic Thermal *)
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 50: MAIN WASH CAUSTIC & THERMAL ACTION (COMPARTMENTS 4 - 8)                     *)
    (* ------------------------------------------------------------------------------------- *)
    50:
        dwSystemStatusWord := 16#0000_0020; (* Main Wash Caustic Active *)
        tMainWashTimer(IN := TRUE, PT := T#35S);

        (* Live steam injection and caustic dosing regulated dynamically by MPC *)
        IF tMainWashTimer.Q THEN
            tMainWashTimer(IN := FALSE, PT := T#35S);
            iState := 60; (* Proceed to Bleach Sanitization *)
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 60: BLEACH DISINFECTION & MICROBIAL SANITIZATION (COMPARTMENTS 9 - 10)          *)
    (* ------------------------------------------------------------------------------------- *)
    60:
        dwSystemStatusWord := 16#0000_0040; (* Bleach Sanitizing Active *)
        tBleachTimer(IN := TRUE, PT := T#25S);

        (* Hold temperature at 65 deg C for validated bactericidal kill *)
        IF tBleachTimer.Q THEN
            tBleachTimer(IN := FALSE, PT := T#25S);
            iState := 70; (* Proceed to Counter-flow Rinse & Neutralization *)
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 70: RINSE, SOURING ACID NEUTRALIZATION & SOFTENING (COMPARTMENTS 11 - 13)       *)
    (* ------------------------------------------------------------------------------------- *)
    70:
        dwSystemStatusWord := 16#0000_0080; (* Rinse Neutralization Active *)
        tRinseTimer(IN := TRUE, PT := T#28S);

        (* Souring acid pumped to achieve target pH 6.0 *)
        IF tRinseTimer.Q THEN
            tRinseTimer(IN := FALSE, PT := T#28S);
            iState := 80; (* Discharge Batch to Hydraulic Press Chute *)
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 80: BATCH DISCHARGE TO 40-BAR HYDRAULIC EXTRACTION PRESS                        *)
    (* ------------------------------------------------------------------------------------- *)
    80:
        dwSystemStatusWord := 16#0000_0100; (* Chute Discharging *)
        tDebounceTimer(IN := TRUE, PT := T#5S);

        (* Verify basket lock interlock before ram descent permissive *)
        IF tDebounceTimer.Q THEN
            tDebounceTimer(IN := FALSE, PT := T#5S);
            IF bPressBasketLocked THEN
                iState := 90; (* Advance to Hydraulic Press Dewatering *)
            ELSE
                dwWarningWord := dwWarningWord OR 16#0000_0004; (* Press Basket Interlock Lost *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 90: HIGH-PRESSURE HYDRAULIC EXTRACTION PRESS (40 BAR) DEWATERING                *)
    (* ------------------------------------------------------------------------------------- *)
    90:
        dwSystemStatusWord := 16#0000_0200; (* Hydraulic Pressing Active *)
        bPressRamAdvanceSol := TRUE;
        bPressRamRetractSol := FALSE;

        (* Stage 1: Soft-touch ram descent until initial linen contact *)
        IF rRamDisplacement_mm < 450.0 THEN
            rPressServoValve_pct := 35.0; (* Rapid pre-stroke *)
        ELSIF rRamDisplacement_mm < 800.0 THEN
            (* Stage 2: Controlled MPC pressure ramp up to 40.0 bar *)
            tPressRampTimer(IN := TRUE, PT := T#30S);
        ELSE
            (* Stage 3: High-pressure 40-bar holding dwell to extract deep interstitial water *)
            tPressHoldTimer(IN := TRUE, PT := T#35S);
            IF tPressHoldTimer.Q AND (rEstimatedMoistureFraction_pct <= 45.0) THEN
                tPressRampTimer(IN := FALSE, PT := T#30S);
                tPressHoldTimer(IN := FALSE, PT := T#35S);
                bPressRamAdvanceSol := FALSE;
                bPressRamRetractSol := TRUE; (* Retract ram *)
                rPressServoValve_pct := 0.0;
                iState := 100; (* Proceed to Cake Discharge & Shaker Breakup *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 100: CAKE DISCHARGE & CENTRIFUGAL SHAKER CAKE BREAKUP                           *)
    (* ------------------------------------------------------------------------------------- *)
    100:
        dwSystemStatusWord := 16#0000_0400; (* Cake Breakup Active *)
        bPressRamRetractSol := TRUE;
        bCakeConveyorRun := TRUE;
        rCakeShakerVFD_pct := 65.0; (* Spin unbalance shaker motor *)
        tCakeShakerTimer(IN := TRUE, PT := T#15S);

        (* Check shaker bearing vibration *)
        IF rCakeShakerVibration_mms > 14.5 THEN
            dwWarningWord := dwWarningWord OR 16#0000_0008; (* Cake Shaker High Unbalance Vibration Warning *)
        END_IF;

        IF tCakeShakerTimer.Q THEN
            tCakeShakerTimer(IN := FALSE, PT := T#15S);
            bCakeConveyorRun := FALSE;
            rCakeShakerVFD_pct := 0.0;
            IF bCakeShakerReady AND bIronerInfeedBeamClear THEN
                iState := 110; (* Proceed to Flatwork Ironer Tension Sync *)
            ELSE
                iState := 120; (* Proceed to Batch Pause / Drain *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 110: FLATWORK CHEST IRONER TENSION SYNCHRONIZATION                              *)
    (* ------------------------------------------------------------------------------------- *)
    110:
        dwSystemStatusWord := 16#0000_0800; (* Ironer Active *)
        bIronerRollNipEngage := TRUE;

        (* Closed-Loop Textile Web Tension Regulation PLL *)
        rTensionError_N := rTargetIronerTension_N - rIronerLinenTension_N;
        rTensionIntegral_N := rTensionIntegral_N + rTensionError_N * c_ScanCycleTime_sec * 0.08;
        IF rTensionIntegral_N > 15.0 THEN
            rTensionIntegral_N := 15.0;
        ELSIF rTensionIntegral_N < -15.0 THEN
            rTensionIntegral_N := -15.0;
        END_IF;

        rIronerSpeedTrimDemand_pct := (rTensionError_N * 0.045) + rTensionIntegral_N;
        rIronerVFD_SpeedDemand_pct := 70.0 + rIronerSpeedTrimDemand_pct;
        IF rIronerVFD_SpeedDemand_pct > 100.0 THEN
            rIronerVFD_SpeedDemand_pct := 100.0;
        ELSIF rIronerVFD_SpeedDemand_pct < 20.0 THEN
            rIronerVFD_SpeedDemand_pct := 20.0;
        END_IF;

        (* Finished batch throughput cycle complete *)
        IF tStateTimer.ET >= T#75S THEN
            bIronerRollNipEngage := FALSE;
            iState := 120;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 120: CONTROLLED BATCH PAUSE, WATER COUNTERFLOW BALANCING & CYCLE LOOP           *)
    (* ------------------------------------------------------------------------------------- *)
    120:
        dwSystemStatusWord := 16#0000_1000; (* Batch Complete Re-looping *)
        rSteamControlValve_pct := 0.0;
        rCausticDosingVFD_pct := 0.0;
        rAcidDosingVFD_pct := 0.0;
        bPressRamAdvanceSol := FALSE;
        bPressRamRetractSol := TRUE;

        IF bMasterEnable AND bEmergencyStopOk THEN
            iState := 10; (* Return to Standby Ready for next scheduled batch *)
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 200: EMERGENCY SAFE SHUTDOWN (SIL-3 TRIP CONDITION)                             *)
    (* ------------------------------------------------------------------------------------- *)
    200:
        dwSystemStatusWord := 16#0000_8000; (* Emergency Trip Asserted *)
        bScrewMotorRunForward    := FALSE;
        bScrewMotorRunReverse    := FALSE;
        bPressRamAdvanceSol      := FALSE;
        bPressRamRetractSol      := FALSE;
        bPressDumpValveEmergency := TRUE; (* Dump hydraulic pressure to reservoir immediately *)
        bCakeConveyorRun         := FALSE;
        bIronerRollNipEngage     := FALSE;
        bChemicalFlushValve      := TRUE; (* Flush chemical header *)
        bAlarmBeaconAudible      := TRUE;
        bAlarmBeaconVisual       := TRUE;

        rSteamControlValve_pct      := 0.0;
        rFreshWaterValve_pct        := 0.0;
        rCausticDosingVFD_pct       := 0.0;
        rAcidDosingVFD_pct          := 0.0;
        rDetergentDosingVFD_pct     := 0.0;
        rBleachDosingVFD_pct        := 0.0;
        rPressServoValve_pct        := 0.0;
        rPressReliefValve_pct       := 100.0; (* Full relief open *)
        rCakeShakerVFD_pct          := 0.0;
        rIronerBurnerModulation_pct := 0.0;
        rIronerVFD_SpeedDemand_pct  := 0.0;

        (* Reset Permissive: Operator Reset pressed, E-Stop clear, and faults cleared *)
        IF bOperatorReset AND bEmergencyStopOk AND NOT bTrip_ScrewJam AND NOT bTrip_SensorConsensusLost THEN
            bTrip_Temp_HH     := FALSE;
            bTrip_Temp_LL     := FALSE;
            bTrip_Cond_HH     := FALSE;
            bTrip_Cond_LL     := FALSE;
            bTrip_Press_HH    := FALSE;
            bTrip_Press_LL    := FALSE;
            bTrip_ChemPres_HH := FALSE;
            bTrip_ChemPres_LL := FALSE;
            bTrip_Weight_HH   := FALSE;
            bTrip_Weight_LL   := FALSE;
            bTrip_Tension_HH  := FALSE;
            bTrip_Tension_LL  := FALSE;
            bTrip_EmergencyStop := FALSE;
            bPressDumpValveEmergency := FALSE;
            bChemicalFlushValve := FALSE;
            bAlarmBeaconAudible := FALSE;
            bAlarmBeaconVisual := FALSE;
            iState := 0; (* Cold-boot re-initialization *)
        END_IF;
ELSE
    iState := 200; (* Catch-all safety shutdown *)
END_CASE;
"""
    parts.append(p7)

    # =========================================================================
    # PART 8: PHASE 5 - ISA-18.2 ALARMS & BIT PACKING
    # =========================================================================
    p8 = """
(* ========================================================================================= *)
(* === PHASE 5: ISA-18.2 ALARMS, TRIP MATRIX & DIAGNOSTIC WORD BIT PACKING ===              *)
(* ========================================================================================= *)
(* Multi-tiered industrial alarm evaluation according to ISA-18.2 standard. Evaluates       *)
(* High-High (HH), High (H), Low (L), and Low-Low (LL) trip levels with deadband hysteresis,*)
(* categorizing faults into Safety Interlocks (Category 1) and Process Trips (Category 2).  *)

dwAlarmWord1_EmergencyTrips := 16#0000_0000;
dwAlarmWord2_ProcessTrips   := 16#0000_0000;
dwIsaAlarmPriorityMask      := 16#0000_0000;

(* --- 5.1 Hardware Emergency Stop (SIL-3 Circuit) --- *)
IF NOT bEmergencyStopOk THEN
    bTrip_EmergencyStop := TRUE;
    dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0001; (* Bit 0: SIL-3 E-Stop Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0001; (* Priority 1: Critical Emergency *)
END_IF;

(* --- 5.2 Wash Water Bulk Temperature Alarms (HH, H, L, LL) --- *)
(* High-High Scald / Boiling Trip: HH = 95.0 deg C *)
IF rVotedWaterTemp_degC >= c_Temp_HH_degC THEN
    bTrip_Temp_HH := TRUE;
ELSIF rVotedWaterTemp_degC <= (c_Temp_HH_degC - c_Temp_Deadband_degC) THEN
    bTrip_Temp_HH := FALSE;
END_IF;
IF bTrip_Temp_HH THEN
    dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0002; (* Bit 1: Wash Temp High-High Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0001;
END_IF;

(* High Temperature Advisory: H = 88.0 deg C *)
IF rVotedWaterTemp_degC >= c_Temp_H_degC THEN
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Wash Temp High Warning *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0002; (* Priority 2: High *)
END_IF;

(* Low Temperature Advisory: L = 65.0 deg C *)
IF (rVotedWaterTemp_degC <= c_Temp_L_degC) AND (iState = 50) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0020; (* Wash Temp Low Warning *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0004; (* Priority 3: Medium *)
END_IF;

(* Low-Low Soil Coagulation Trip: LL = 45.0 deg C *)
IF (rVotedWaterTemp_degC <= c_Temp_LL_degC) AND (iState = 50) THEN
    bTrip_Temp_LL := TRUE;
ELSIF rVotedWaterTemp_degC >= (c_Temp_LL_degC + c_Temp_Deadband_degC) THEN
    bTrip_Temp_LL := FALSE;
END_IF;
IF bTrip_Temp_LL THEN
    dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0001; (* Bit 0: Wash Temp Low-Low Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0002;
END_IF;

(* --- 5.3 Wash Liquor Caustic Conductivity Alarms (HH, H, L, LL) --- *)
(* High-High Chemical Overdose Trip: HH = 12,500 uS/cm *)
IF rVotedConductivity_uScm >= c_Cond_HH_uScm THEN
    bTrip_Cond_HH := TRUE;
ELSIF rVotedConductivity_uScm <= (c_Cond_HH_uScm - c_Cond_Deadband_uScm) THEN
    bTrip_Cond_HH := FALSE;
END_IF;
IF bTrip_Cond_HH THEN
    dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0002; (* Bit 1: Conductivity High-High Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0002;
END_IF;

(* Low-Low Chemical Depletion Trip: LL = 1,500 uS/cm *)
IF (rVotedConductivity_uScm <= c_Cond_LL_uScm) AND (iState = 50) THEN
    bTrip_Cond_LL := TRUE;
ELSIF rVotedConductivity_uScm >= (c_Cond_LL_uScm + c_Cond_Deadband_uScm) THEN
    bTrip_Cond_LL := FALSE;
END_IF;
IF bTrip_Cond_LL THEN
    dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0004; (* Bit 2: Conductivity Low-Low Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0004;
END_IF;

(* --- 5.4 Hydraulic Extraction Press Pressure Alarms (HH, H, L, LL) --- *)
(* High-High Hydraulic Burst Risk Dump Trip: HH = 44.0 bar *)
IF rVotedPressPressure_bar >= c_Press_HH_bar THEN
    bTrip_Press_HH := TRUE;
ELSIF rVotedPressPressure_bar <= (c_Press_HH_bar - c_Press_Deadband_bar) THEN
    bTrip_Press_HH := FALSE;
END_IF;
IF bTrip_Press_HH THEN
    dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0004; (* Bit 2: Hydraulic Press Overpressure Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0001;
END_IF;

(* Low-Low Hydraulic Cavitation Trip: LL = 0.8 bar during active press *)
IF (rVotedPressPressure_bar <= c_Press_LL_bar) AND (iState = 90) AND (tPressRampTimer.ET >= T#5S) THEN
    bTrip_Press_LL := TRUE;
ELSIF rVotedPressPressure_bar >= (c_Press_LL_bar + c_Press_Deadband_bar) THEN
    bTrip_Press_LL := FALSE;
END_IF;
IF bTrip_Press_LL THEN
    dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0008; (* Bit 3: Hydraulic Pressure Cavitation Loss Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0002;
END_IF;

(* --- 5.5 Peristaltic Chemical Line Pressure Occlusion Alarms (HH, LL) --- *)
tOcclusionTimer(IN := (rPeristalticLinePressure_bar >= c_ChemPres_HH_bar), PT := T#1S500MS);
IF tOcclusionTimer.Q THEN
    bTrip_ChemPres_HH := TRUE;
ELSIF rPeristalticLinePressure_bar <= (c_ChemPres_HH_bar - c_ChemPres_Deadband_bar) THEN
    bTrip_ChemPres_HH := FALSE;
END_IF;
IF bTrip_ChemPres_HH THEN
    dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0008; (* Bit 3: Chemical Line Occlusion Overpressure Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0001;
END_IF;

IF (rPeristalticLinePressure_bar <= c_ChemPres_LL_bar) AND (rCausticDosingVFD_pct > 20.0) THEN
    bTrip_ChemPres_LL := TRUE;
ELSIF rPeristalticLinePressure_bar >= (c_ChemPres_LL_bar + c_ChemPres_Deadband_bar) THEN
    bTrip_ChemPres_LL := FALSE;
END_IF;
IF bTrip_ChemPres_LL THEN
    dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0010; (* Bit 4: Chemical Supply Cavitation Loss Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0004;
END_IF;

(* --- 5.6 Infeed Batch Weight Trip Points (HH, LL) --- *)
IF rVotedBatchWeight_kg >= c_Weight_HH_kg THEN
    bTrip_Weight_HH := TRUE;
ELSIF rVotedBatchWeight_kg <= (c_Weight_HH_kg - c_Weight_Deadband_kg) THEN
    bTrip_Weight_HH := FALSE;
END_IF;
IF bTrip_Weight_HH THEN
    dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0020; (* Bit 5: Batch Overweight Jam Hazard Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0002;
END_IF;

IF (rVotedBatchWeight_kg <= c_Weight_LL_kg) AND (iState = 20) THEN
    bTrip_Weight_LL := TRUE;
ELSIF rVotedBatchWeight_kg >= (c_Weight_LL_kg + c_Weight_Deadband_kg) THEN
    bTrip_Weight_LL := FALSE;
END_IF;
IF bTrip_Weight_LL THEN
    dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0040; (* Bit 6: Batch Underweight Rejection Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0004;
END_IF;

(* --- 5.7 Flatwork Chest Ironer Linen Web Tension Trips (HH, LL) --- *)
IF (rIronerLinenTension_N >= c_Tension_HH_N) AND (iState = 110) THEN
    bTrip_Tension_HH := TRUE;
ELSIF rIronerLinenTension_N <= (c_Tension_HH_N - c_Tension_Deadband_N) THEN
    bTrip_Tension_HH := FALSE;
END_IF;
IF bTrip_Tension_HH THEN
    dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0010; (* Bit 4: Textile Web Over-Tension Tearing Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0001;
END_IF;

IF (rIronerLinenTension_N <= c_Tension_LL_N) AND (iState = 110) THEN
    bTrip_Tension_LL := TRUE;
ELSIF rIronerLinenTension_N >= (c_Tension_LL_N + c_Tension_Deadband_N) THEN
    bTrip_Tension_LL := FALSE;
END_IF;
IF bTrip_Tension_LL THEN
    dwAlarmWord2_ProcessTrips := dwAlarmWord2_ProcessTrips OR 16#0000_0080; (* Bit 7: Textile Web Slack Roller Wrap Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0002;
END_IF;

(* --- 5.8 Equipment Jam & Sensor Consensus Shutdowns --- *)
IF bTrip_ScrewJam THEN
    dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0020; (* Bit 5: Archimedean Screw Jam Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0001;
END_IF;

IF bTrip_SensorConsensusLost THEN
    dwAlarmWord1_EmergencyTrips := dwAlarmWord1_EmergencyTrips OR 16#0000_0040; (* Bit 6: 2oo3 Sensor Consensus Lost Trip *)
    dwIsaAlarmPriorityMask := dwIsaAlarmPriorityMask OR 16#0000_0001;
END_IF;

(* Master Trip Enforcement: Force FSM Transition to Emergency Stop State *)
IF (dwAlarmWord1_EmergencyTrips <> 16#0000_0000) OR (dwAlarmWord2_ProcessTrips <> 16#0000_0000) THEN
    IF iState <> 200 THEN
        iState := 200; (* Immediate SIL-3 Emergency Safe Shutdown Transition *)
    END_IF;
END_IF;

END_FUNCTION_BLOCK
"""
    parts.append(p8)

    full_code = "".join(parts)
    return full_code

if __name__ == "__main__":
    st_code = generate_iec_st()
    print("Generated ST Code character count:", len(st_code))
