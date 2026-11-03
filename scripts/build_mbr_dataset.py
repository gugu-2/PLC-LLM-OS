import json
import uuid
import os
import re

def build_iec_code():
    # Constructing the massive, mathematically rigorous Structured Text block
    parts = []

    # Opening
    parts.append("""```iec-st
FUNCTION_BLOCK FB_Water_MBR_WastewaterAeration_PermeateSuction
(*
  ==========================================================================================
  PROJECT:       100,000 m3/day MUNICIPAL / INDUSTRIAL MEMBRANE BIOREACTOR (MBR) FACILITY
  SUBSYSTEM:     MEMBRANE TRAIN CYCLIC INTERMITTENT AIR SCOUR & REVERSIBLE PERMEATE SUCTION
  DISCIPLINE:    WATER & WASTEWATER PROCESS ENGINEERING / CYBER-PHYSICAL MODEL PREDICTIVE CONTROL
  STANDARD:      IEC 61131-3 3RD EDITION (DETERMINISTIC EMBEDDED REAL-TIME CONTROL)
  AUTHOR:        LUMINA AI SWARM - PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
  PLANT CAPACITY:100,000 m3/day (16 PARALLEL BIOLOGICAL FILTRATION TRAINS, 6,250 m3/day/TRAIN)
  MEMBRANE TYPE: GE ZEEWEED 500D / TORAY SUBMERGED HOLLOW-FIBER ULTRAFILTRATION (PVDF)
  PORE SIZE:     0.04 um NOMINAL (SURFACE AREA: 12,500 m2 PER TRAIN, 200,000 m2 TOTAL FACILITY)
  BIOMASS:       MIXED LIQUOR SUSPENDED SOLIDS (MLSS: 8,000 TO 12,000 mg/L, SRT = 25 DAYS)
  AERATION:      CYCLIC COARSE-BUBBLE MEMBRANE AIR SCOURING (10s ON / 10s OFF) VIA VFD BLOWERS
  SUCTION:       REVERSIBLE VFD PROGRESSIVE CAVITY / END-SUCTION CENTRIFUGAL PERMEATE PUMPS
  CLEANING:      DYNAMIC RELAXATION, REVERSIBLE MAINTENANCE BACKPULSE (NaOCl / CITRIC ACID),
                 AND FULL RECOVERY CLEAN-IN-PLACE (CIP) AUTOMATION WITH RESISTANCE-IN-SERIES

  ==========================================================================================
  CYBER-PHYSICAL & PROCESS PHENOMENOLOGICAL GOVERNING EQUATIONS:

  1. RESISTANCE-IN-SERIES FILTRATION KINETICS (DARCY-HERMIA HYDRAULIC EXTENSION):
     Permeate flux J [m3/(m2*s)] through the porous hollow-fiber membrane is governed by Darcy's
     law extended for multi-layered resistance series:
         J = (TMP * 100.0) / (mu_T * (R_m + R_pore + R_cake + R_gel))
     where:
         TMP   = Transmembrane Pressure [mbar] = (P_feed - P_permeate) = P_hydrostatic - P_suction
         mu_T  = Dynamic liquid water viscosity at mixed liquor temperature T [Pa*s]
         R_m   = Intrinsic clean membrane resistance [1/m] (constant = 1.25 x 10^12 m^-1)
         R_pore= Irreversible internal pore blocking resistance [1/m] (removed via CIP recovery)
         R_cake= Reversible cake layer resistance of deposited sludge flocs [1/m] (scoured by air)
         R_gel = Extracellular polymeric substance (EPS / SMP) colloidal gel resistance [1/m]

  2. TEMPERATURE COMPENSATION TO STANDARD WATER PERMEABILITY AT 20 deg C (ASCE / EWRI 2-06):
     Because mixed liquor temperature significantly fluctuates seasonally (5.0 deg C to 35.0 deg C),
     viscosity variations drastically distort observed transmembrane pressure. Dynamic viscosity
     of water mu(T) [Pa*s] is computed via the continuous empirical correlation:
         mu(T) = 1.787 x 10^-3 * EXP(-0.0337 * T + 0.00022 * T^2)
     Standardized flux normalized to 20.0 deg C (J_20 [LMH] = L/(m2*h)) and permeability K_20:
         J_20 = J_measured * (mu(T) / mu(20 deg C)) = J_measured * exp(-0.0239 * (T - 20.0))
         K_20 = J_20 / TMP  [LMH/bar]
     Clean membrane reference permeability K_0 = 250.0 to 300.0 LMH/bar; critical CIP trip < 80.0.

  3. CAKE COMPRESSIBILITY & NON-NEWTONIAN MLSS SLUDGE RHEOLOGY:
     Mixed liquor exhibiting MLSS between 8,000 and 12,000 mg/L behaves as a pseudoplastic
     Bingham fluid. Specific cake resistance alpha_c [m/kg] varies with pressure compaction:
         alpha_c(TMP) = alpha_0 * (TMP / TMP_ref)^s_comp
     where s_comp is the cake compressibility index (0.45 to 0.70 for activated sludge flocs).
     Specific cake resistance deposition rate:
         d(R_cake)/dt = (alpha_c * C_ss * J_actual) - (k_shear * tau_w * R_cake)
     where k_shear is the hydrodynamic scouring detachment constant and tau_w is the turbulent
     wall shear stress induced by rising coarse bubbles.

  4. CYCLIC INTERMITTENT COARSE-BUBBLE AERATION SCOURING HYDRODYNAMICS:
     Air scour blowers generate macroscopic Taylor bubbles through bottom aerator headers (dia 3-5mm).
     To reduce specific biological aeration power (which typically accounts for 40-50% of plant kWh),
     air is modulated in a cyclic 10s ON / 10s OFF pulse sequence:
         tau_w(t) = 0.5 * f_fanning * rho_sludge * (u_bubble_slip + u_liquid)^2
     Specific Aeration Demand per membrane area (SAD_m [Nm3/(m2*h)]) and per permeate (SAD_p):
         SAD_m = Q_air_scour_Nm3h / A_membrane_m2  (Target: 0.18 to 0.32 Nm3/(m2*h))
         SAD_p = Q_air_scour_Nm3h / Q_permeate_m3h (Target: 12.0 to 22.0 Nm3 air / m3 water)

  5. BIOLOGICAL DISSOLVED OXYGEN (DO) CASCADE & TWO-FILM AERATION MODEL:
     In submerged MBR tanks, nitrification requires strictly controlled DO (1.5 to 2.5 mg/L):
         d(C_DO)/dt = K_L_a(T) * (C_DO_sat(T, P) - C_DO) - OUR
     where OUR is the biomass Oxygen Uptake Rate (mg O2/(L*h)) and K_L_a is the volumetric
     mass transfer coefficient modulated by air blower flow and MLSS alpha-factor:
         alpha_factor = exp(-0.075 * (MLSS / 1000.0))

  6. DISCRETE STATE-SPACE MULTIVARIABLE FOULING PREDICTION (Ts = 1.0 s):
     The coupled electro-mechanical and hydrodynamic process is represented in discrete state-space:
         x[k+1] = A * x[k] + B * u[k]
         y[k]   = C * x[k] + D * u[k]
     State vector x = [TMP_mbar, normalized_flux_lmh, cake_resistance_e11, dissolved_oxygen_mg_l]^T
     Control vector u = [permeate_pump_cmd_pct, air_scour_blower_cmd_pct, chem_wash_cmd_pct]^T
     System matrices A (4x4) and B (4x3) encapsulate hydraulic permeation, pore occlusion,
     shear-induced cake erosion, and dissolved oxygen kinetics.

  7. MODEL PREDICTIVE CONTROL (MPC) RECEDING-HORIZON QUADRATIC FORMULATION:
     Actuator trajectories are optimized via unrolled Projected Gradient Descent (PGD) minimizing:
         J_mpc = sum_{i=1..Np} [ (x_{k+i} - r_{k+i})^T * Q * (x_{k+i} - r_{k+i}) +
                                 delta_u_{k+i-1}^T * R * delta_u_{k+i-1} ] +
                 (x_{k+Np} - r_{k+Np})^T * P * (x_{k+Np} - r_{k+Np})
     enforcing hard physical box bounds (0 <= u <= 100%) and slew rate limits (|delta_u| <= rate_max).
  ==========================================================================================
*)
""")

    # VAR_INPUT
    parts.append("""VAR_INPUT
    (* ===================================================================================== *)
    (* 1. TRIPLE MODULAR REDUNDANT (2oo3) HYDROSTATIC FEED PRESSURE TRANSMITTERS             *)
    (* ===================================================================================== *)
    rFeedPressure_Ch1_bar           : REAL := 0.32;     (* Submerged basin hydrostatic feed pressure Ch1 [bar] (0.0 .. 1.0) *)
    rFeedPressure_Ch2_bar           : REAL := 0.32;     (* Submerged basin hydrostatic feed pressure Ch2 [bar] (0.0 .. 1.0) *)
    rFeedPressure_Ch3_bar           : REAL := 0.32;     (* Submerged basin hydrostatic feed pressure Ch3 [bar] (0.0 .. 1.0) *)

    (* ===================================================================================== *)
    (* 2. TRIPLE MODULAR REDUNDANT (2oo3) PERMEATE SUCTION VACUUM TRANSMITTERS               *)
    (* ===================================================================================== *)
    rPermeateSuctionPress_Ch1_bar   : REAL := 0.12;     (* Permeate suction line manifold absolute/gauge Ch1 [bar] (-0.5 .. 0.5) *)
    rPermeateSuctionPress_Ch2_bar   : REAL := 0.12;     (* Permeate suction line manifold absolute/gauge Ch2 [bar] (-0.5 .. 0.5) *)
    rPermeateSuctionPress_Ch3_bar   : REAL := 0.12;     (* Permeate suction line manifold absolute/gauge Ch3 [bar] (-0.5 .. 0.5) *)

    (* ===================================================================================== *)
    (* 3. TRIPLE MODULAR REDUNDANT (2oo3) DIFFERENTIAL TRANSMEMBRANE PRESSURE (TMP) SENSORS  *)
    (* ===================================================================================== *)
    rDiffPress_TMP_Ch1_mbar         : REAL := 185.0;    (* Direct differential TMP transmitter Channel 1 [mbar] (0.0 .. 600.0) *)
    rDiffPress_TMP_Ch2_mbar         : REAL := 185.0;    (* Direct differential TMP transmitter Channel 2 [mbar] (0.0 .. 600.0) *)
    rDiffPress_TMP_Ch3_mbar         : REAL := 185.0;    (* Direct differential TMP transmitter Channel 3 [mbar] (0.0 .. 600.0) *)

    (* ===================================================================================== *)
    (* 4. TRAIN HYDRAULIC & PHYSICAL PROCESS VARIABLES                                       *)
    (* ===================================================================================== *)
    rPermeateFlowRate_m3h           : REAL := 260.0;    (* Train electromagnetic permeate flow meter [m3/h] (0.0 .. 450.0) *)
    rMixedLiquorTemp_degC           : REAL := 19.5;     (* Membrane biological aeration basin temperature [deg C] (2.0 .. 40.0) *)
    rMLSS_Concentration_mgL         : REAL := 9850.0;   (* Optical Mixed Liquor Suspended Solids probe [mg/L] (4000.0 .. 16000.0) *)
    rFeedBasinLevel_m               : REAL := 3.45;     (* Submerged membrane tank hydrostatic liquid level [m] (0.0 .. 5.0) *)

    (* ===================================================================================== *)
    (* 5. TRIPLE MODULAR REDUNDANT (2oo3) DISSOLVED OXYGEN (DO) OPTICAL SENSORS              *)
    (* ===================================================================================== *)
    rDissolvedOxygen_Ch1_mgL        : REAL := 2.10;     (* Optical luminescence DO sensor Channel 1 [mg/L] (0.0 .. 10.0) *)
    rDissolvedOxygen_Ch2_mgL        : REAL := 2.10;     (* Optical luminescence DO sensor Channel 2 [mg/L] (0.0 .. 10.0) *)
    rDissolvedOxygen_Ch3_mgL        : REAL := 2.10;     (* Optical luminescence DO sensor Channel 3 [mg/L] (0.0 .. 10.0) *)

    (* ===================================================================================== *)
    (* 6. TRIPLE MODULAR REDUNDANT (2oo3) PERMEATE TURBIDITY INTEGRITY NEPHELOMETERS         *)
    (* ===================================================================================== *)
    rPermeateTurbidity_Ch1_NTU      : REAL := 0.042;    (* Laser nephelometric turbidity monitor Ch1 [NTU] (0.00 .. 2.00) *)
    rPermeateTurbidity_Ch2_NTU      : REAL := 0.042;    (* Laser nephelometric turbidity monitor Ch2 [NTU] (0.00 .. 2.00) *)
    rPermeateTurbidity_Ch3_NTU      : REAL := 0.042;    (* Laser nephelometric turbidity monitor Ch3 [NTU] (0.00 .. 2.00) *)

    (* ===================================================================================== *)
    (* 7. AIR SCOUR BLOWER HEADER INSTRUMENTATION                                            *)
    (* ===================================================================================== *)
    rAirScourSupplyPressure_bar     : REAL := 0.42;     (* Coarse-bubble aeration blower header supply pressure [bar] (0.0 .. 1.2) *)
    rAirScourFlowRate_Nm3h          : REAL := 2250.0;   (* Thermal dispersion air mass flowmeter [Nm3/h] (0.0 .. 4000.0) *)

    (* ===================================================================================== *)
    (* 8. CHEMICAL DOSING ANALYZERS & OPERATOR SUPERVISORY CONTROLS                          *)
    (* ===================================================================================== *)
    rChemicalDosingNaOCl_ppm        : REAL := 210.0;    (* Sodium hypochlorite maintenance wash concentration [ppm] (0 .. 1000) *)
    rChemicalDosingCitric_ppm       : REAL := 1950.0;   (* Citric acid recovery clean concentration [ppm] (0 .. 5000) *)
    bAutoModeEnable                 : BOOL := TRUE;     (* Master supervisory automatic train sequence enable flag *)
    bCIP_CommandRequest             : BOOL := FALSE;    (* Operator / Scheduler initiate Clean-In-Place request *)
    bAcknowledgeFault               : BOOL := FALSE;    (* Operator ISA-18.2 alarm acknowledge pushbutton *)
    bEmergencyStop                  : BOOL := FALSE;    (* SIL-2 Hardwired fail-safe Emergency Stop trip input *)
    bPermeateHeaderPermissive       : BOOL := TRUE;     (* Downstream disinfection / distribution header permissive *)
END_VAR
""")

    # VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1. PERMEATE SUCTION PUMP ACTUATOR COMMANDS (REVERSIBLE VFD)                           *)
    (* ===================================================================================== *)
    rPermeatePumpSpeed_Pct          : REAL := 0.0;      (* VFD suction pump analog speed setpoint [0.0 .. 100.0 %] *)
    bPermeatePumpForward_Run        : BOOL := FALSE;    (* Forward permeate filtration suction contactor run enable *)
    bPermeatePumpReverse_Run        : BOOL := FALSE;    (* Reverse permeate backpulse flush contactor run enable *)

    (* ===================================================================================== *)
    (* 2. CYCLIC AIR SCOUR BLOWER & SOLENOID ACTUATOR COMMANDS                               *)
    (* ===================================================================================== *)
    rAirScourBlowerSpeed_Pct        : REAL := 0.0;      (* VFD coarse-bubble scour blower analog speed command [0.0 .. 100.0 %] *)
    bAirScourCyclicSolenoid_Cmd     : BOOL := FALSE;    (* Cyclic 10s ON / 10s OFF air pulse distribution valve command *)
    bAirScourContinuous_Cmd         : BOOL := FALSE;    (* Continuous coarse aeration override (relaxation / intensive scour) *)
    bAirScourHeaderValve_Cmd        : BOOL := FALSE;    (* Train main pneumatic air scour isolation butterfly valve *)

    (* ===================================================================================== *)
    (* 3. REVERSIBLE CHEMICAL MAINTENANCE WASH & CIP ACTUATORS                               *)
    (* ===================================================================================== *)
    bNaOCl_DosingPump_Cmd           : BOOL := FALSE;    (* Sodium hypochlorite backpulse dosing metering pump command *)
    bCitricAcid_DosingPump_Cmd      : BOOL := FALSE;    (* Citric acid chemical cleaning dosing metering pump command *)
    bPermeateIsolateValve_Cmd       : BOOL := FALSE;    (* Permeate line automated train isolation valve (fail-closed) *)
    bPermeateToWasteValve_Cmd       : BOOL := FALSE;    (* Off-spec permeate reject / CIP neutralization divert to headworks *)
    bCIP_DrainValve_Cmd             : BOOL := FALSE;    (* Membrane tank CIP gravity drainage / evacuation valve *)

    (* ===================================================================================== *)
    (* 4. 2oo3 TMR VALIDATED SENSOR VALUES & RECONCILED PROCESS METRICS                      *)
    (* ===================================================================================== *)
    rVoted_TMP_mbar                 : REAL := 0.0;      (* 2oo3 TMR reconciled Transmembrane Pressure [mbar] *)
    rVoted_DO_mgL                   : REAL := 0.0;      (* 2oo3 TMR reconciled Dissolved Oxygen concentration [mg/L] *)
    rVoted_Turbidity_NTU            : REAL := 0.0;      (* 2oo3 TMR reconciled Permeate Laser Turbidity [NTU] *)
    rNormalizedFlux_LMH             : REAL := 0.0;      (* Temperature-normalized membrane flux at 20 deg C [LMH] *)
    rNormalizedPermeability_LMH_bar : REAL := 0.0;      (* Temperature-corrected specific permeability [LMH/bar] *)
    rCalculatedCakeResistance_m_inv : REAL := 0.0;      (* Dynamic cake layer fouling resistance [m^-1] *)
    rSpecificAerationDemand_SADm    : REAL := 0.0;      (* Specific Aeration Demand per membrane area [Nm3/(m2*h)] *)
    rSpecificAerationDemand_SADp    : REAL := 0.0;      (* Specific Aeration Demand per permeate volume [Nm3_air / m3_water] *)

    (* ===================================================================================== *)
    (* 5. ISA-18.2 ALARMS, STATUS BITFIELDS & FINITE STATE MACHINE OUTPUTS                  *)
    (* ===================================================================================== *)
    wISA_AlarmWord_High             : WORD := 16#0000;  (* Priority 1 (Trip) and Priority 2 (Critical) alarm bitfield *)
    wISA_AlarmWord_Low              : WORD := 16#0000;  (* Priority 3 (Warning) and Priority 4 (Advisory) alarm bitfield *)
    dwDiagnosticWord                : DWORD := 16#0000_0000; (* Internal diagnostic health and TMR sensor degradation bits *)
    iTrainCurrentState              : INT := 0;         (* Active FSM operational state code (0..99) *)
    sTrainStateDescription          : STRING[40] := 'TRAIN_STANDBY_IDLE'; (* Human-readable operational stage description *)
    bTrainHealthy                   : BOOL := TRUE;     (* Train operational readiness and integrity status *)
    bCIP_Required_Flag              : BOOL := FALSE;    (* Irreversible fouling recovery CIP mandatory trigger flag *)
    bFiberIntegrityFault            : BOOL := FALSE;    (* Hollow-fiber mechanical breach / integrity failure detected *)
    rFiltrationCycleTime_Elapsed_s  : REAL := 0.0;      (* Current filtration cycle elapsed time [seconds] *)
    rCumulativePermeateVolume_m3    : REAL := 0.0;      (* Total accumulated permeate treated volume [m3] *)
END_VAR
""")

    # VAR
    parts.append("""VAR
    (* ===================================================================================== *)
    (* 1. PHYSICAL CONSTANTS & MEMBRANE MODULE SPECIFICATIONS                                *)
    (* ===================================================================================== *)
    rConst_MembraneArea_m2          : REAL := 12500.0;  (* Total membrane active surface area per train [m2] *)
    rConst_CleanMembraneRes_m_inv   : REAL := 1.25E12;  (* Clean virgin membrane intrinsic resistance Rm [m^-1] *)
    rConst_ViscosityWater20_Pas     : REAL := 1.002E-3; (* Reference dynamic viscosity of pure water at 20 deg C [Pa*s] *)
    rConst_NominalFlux_LMH          : REAL := 20.80;    (* Design net sustainable permeate flux [LMH = L/(m2*h)] *)
    rConst_WaterDensity_kgm3        : REAL := 1000.0;   (* Density of treated municipal water [kg/m3] *)
    rConst_Gravity_mps2             : REAL := 9.80665;  (* Gravitational acceleration [m/s2] *)
    rConst_ScanTime_s               : REAL := 1.0;      (* Deterministic task scan interval Ts [seconds] *)

    (* ===================================================================================== *)
    (* 2. DISCRETE STATE-SPACE MATRICES (4x4 SYSTEM MATRIX A, 4x3 INPUT MATRIX B)            *)
    (* States x = [1:TMP_mbar, 2:Flux_LMH, 3:CakeRes_e11, 4:DO_mgL]                          *)
    (* Inputs u = [1:PermPump_Pct, 2:AirBlower_Pct, 3:ChemWash_Pct]                         *)
    (* ===================================================================================== *)
    aMatrix_A                       : ARRAY[1..4, 1..4] OF REAL; (* Discrete state transition matrix A (Ts = 1.0s) *)
    aMatrix_B                       : ARRAY[1..4, 1..3] OF REAL; (* Discrete input control matrix B (Ts = 1.0s) *)
    aMatrix_C                       : ARRAY[1..4, 1..4] OF REAL; (* Discrete output measurement matrix C *)
    aMatrix_D                       : ARRAY[1..4, 1..3] OF REAL; (* Direct feedthrough transmission matrix D *)

    aState_x                        : ARRAY[1..4] OF REAL; (* Current state vector x[k] *)
    aState_x_next                   : ARRAY[1..4] OF REAL; (* Predicted state vector x[k+1] *)
    aControl_u                      : ARRAY[1..3] OF REAL; (* Active control actuator vector u[k] *)
    aControl_u_prev                 : ARRAY[1..3] OF REAL; (* Previous scan control actuator vector u[k-1] *)
    aSetpoint_ref                   : ARRAY[1..4] OF REAL; (* Model Predictive Control state setpoint vector r[k] *)
    aError_e                        : ARRAY[1..4] OF REAL; (* State tracking error vector e[k] = x[k] - r[k] *)

    (* ===================================================================================== *)
    (* 3. MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST MATRICES & OPTIMIZER VARIABLES       *)
    (* ===================================================================================== *)
    aMatrix_Q                       : ARRAY[1..4, 1..4] OF REAL; (* State error quadratic penalty matrix Q *)
    aMatrix_R                       : ARRAY[1..3, 1..3] OF REAL; (* Actuator slew rate penalty matrix R *)
    aMatrix_P                       : ARRAY[1..4, 1..4] OF REAL; (* Terminal cost matrix P (DARE solution) *)

    aGrad_u                         : ARRAY[1..3] OF REAL; (* Projected Gradient Descent cost gradient vector *)
    aDelta_u                        : ARRAY[1..3] OF REAL; (* Computed control slew rate candidate delta_u *)
    rMPC_StepSize_alpha             : REAL := 0.0125;   (* Optimization gradient descent step size alpha *)
    rMPC_CostCurrent                : REAL := 0.0;      (* Real-time MPC quadratic objective function value *)
    rMPC_PredictedTMP               : REAL := 0.0;      (* 5-step horizon predicted Transmembrane Pressure *)
    rMPC_PredictedFlux              : REAL := 0.0;      (* 5-step horizon predicted Permeate Flux *)

    (* ===================================================================================== *)
    (* 4. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT DEBOUNCE TIMERS                *)
    (* ===================================================================================== *)
    (* 4.1 TMP Differential Pressure 2oo3 Voting *)
    bTMP_Dev_1_2                    : BOOL := FALSE;    (* Sensor 1 vs 2 discrepancy flag (|Ch1 - Ch2| > 35 mbar) *)
    bTMP_Dev_2_3                    : BOOL := FALSE;    (* Sensor 2 vs 3 discrepancy flag (|Ch2 - Ch3| > 35 mbar) *)
    bTMP_Dev_1_3                    : BOOL := FALSE;    (* Sensor 1 vs 3 discrepancy flag (|Ch1 - Ch3| > 35 mbar) *)
    tDevTimer_TMP                   : TON;              (* TMP discrepancy persistence timer (2.0s) *)
    bTMP_Ch1_Fault                  : BOOL := FALSE;    (* Channel 1 isolated drift / signal failure *)
    bTMP_Ch2_Fault                  : BOOL := FALSE;    (* Channel 2 isolated drift / signal failure *)
    bTMP_Ch3_Fault                  : BOOL := FALSE;    (* Channel 3 isolated drift / signal failure *)
    bTMP_Degraded_1oo2              : BOOL := FALSE;    (* TMP voting operating in degraded 1oo2 dual-sensor mode *)
    bTMP_CriticalFailure_All        : BOOL := FALSE;    (* Catastrophic 3-channel TMP transducer failure *)

    (* 4.2 Dissolved Oxygen (DO) Optical Luminescence 2oo3 Voting *)
    bDO_Dev_1_2                     : BOOL := FALSE;    (* DO Sensor 1 vs 2 discrepancy flag (> 0.40 mg/L) *)
    bDO_Dev_2_3                     : BOOL := FALSE;    (* DO Sensor 2 vs 3 discrepancy flag (> 0.40 mg/L) *)
    bDO_Dev_1_3                     : BOOL := FALSE;    (* DO Sensor 1 vs 3 discrepancy flag (> 0.40 mg/L) *)
    tDevTimer_DO                    : TON;              (* DO discrepancy debounce timer (3.0s) *)
    bDO_Ch1_Fault                   : BOOL := FALSE;    (* DO Channel 1 sensor failure *)
    bDO_Ch2_Fault                   : BOOL := FALSE;    (* DO Channel 2 sensor failure *)
    bDO_Ch3_Fault                   : BOOL := FALSE;    (* DO Channel 3 sensor failure *)
    bDO_Degraded_1oo2               : BOOL := FALSE;    (* DO operating in degraded mode *)

    (* 4.3 Permeate Turbidity Nephelometer 2oo3 Voting *)
    bTurb_Dev_1_2                   : BOOL := FALSE;    (* Turbidity Sensor 1 vs 2 discrepancy flag (> 0.05 NTU) *)
    bTurb_Dev_2_3                   : BOOL := FALSE;    (* Turbidity Sensor 2 vs 3 discrepancy flag (> 0.05 NTU) *)
    bTurb_Dev_1_3                   : BOOL := FALSE;    (* Turbidity Sensor 1 vs 3 discrepancy flag (> 0.05 NTU) *)
    tDevTimer_Turb                  : TON;              (* Turbidity discrepancy debounce timer (2.0s) *)
    bTurb_Ch1_Fault                 : BOOL := FALSE;    (* Turbidity Channel 1 sensor failure *)
    bTurb_Ch2_Fault                 : BOOL := FALSE;    (* Turbidity Channel 2 sensor failure *)
    bTurb_Ch3_Fault                 : BOOL := FALSE;    (* Turbidity Channel 3 sensor failure *)
    bTurb_Degraded_1oo2             : BOOL := FALSE;    (* Turbidity operating in degraded mode *)

    (* ===================================================================================== *)
    (* 5. HYDRODYNAMIC PROCESS CALCULATIONS & VISCOSITY VARIABLES                            *)
    (* ===================================================================================== *)
    rDynamicViscosity_Pas           : REAL := 1.002E-3; (* Mixed liquor dynamic water viscosity mu(T) [Pa*s] *)
    rViscosityCorrectionFactor      : REAL := 1.000;    (* Viscosity ratio mu(T) / mu(20 deg C) *)
    rMeasuredFlux_LMH               : REAL := 0.0;      (* Raw gross permeate flux J_gross [LMH] *)
    rTotalHydraulicResistance_m_inv : REAL := 1.25E12;  (* Total resistance R_total = Rm + Rpore + Rcake [m^-1] *)
    rSludgeViscosityMultiplier      : REAL := 1.0;      (* Non-Newtonian MLSS sludge Bingham multiplier *)
    rOxygenSaturation_mgL           : REAL := 9.15;     (* Temperature-dependent DO saturation concentration C* [mg/L] *)
    rOxygenTransferRate_OTR         : REAL := 0.0;      (* Aeration basin Oxygen Transfer Rate OTR [mg/(L*h)] *)
    rOxygenUptakeRate_OUR           : REAL := 24.5;     (* Biological microbial Oxygen Uptake Rate OUR [mg/(L*h)] *)
    rVolumetricMassTransfer_KLa     : REAL := 14.8;     (* Volumetric oxygen transfer coefficient KLa [1/h] *)

    (* ===================================================================================== *)
    (* 6. FINITE STATE MACHINE (FSM) TIMERS, CYCLE COUNTERS & SEQUENCING VARIABLES           *)
    (* ===================================================================================== *)
    iState                          : INT := 0;         (* Internal active finite state machine register *)
    iStatePrevious                  : INT := -1;        (* State history register for edge detection *)
    iFiltrationCycleCount           : DINT := 0;        (* Accumulated complete filtration cycles since CIP *)
    iBackpulseCycleCount            : DINT := 0;        (* Accumulated maintenance chemical backpulses *)
    rCycleTimeCounter_s             : REAL := 0.0;      (* Intra-state elapsed duration accumulator [s] *)

    (* Deterministic IEC TON Timers for Stage Sequencing *)
    tTimer_PreAerationScour         : TON;              (* State 10: 30s pre-filtration air scour *)
    tTimer_ForwardFiltration        : TON;              (* State 20: 540s (9.0 min) forward permeate suction *)
    tTimer_RelaxationPhase          : TON;              (* State 30: 60s (1.0 min) suction relaxation *)
    tTimer_ReversibleBackpulse      : TON;              (* State 40: 30s chemical maintenance backpulse *)
    tTimer_AirScourDefouling        : TON;              (* State 50: 45s intensive coarse bubble defouling burst *)
    tTimer_TurbidityIntegrity       : TON;              (* State 60: 30s laser nephelometer integrity verification *)
    tTimer_MaintenanceCleanCIP      : TON;              (* State 70: 1800s (30 min) maintenance chemical clean *)
    tTimer_ChemicalRecoverySoak     : TON;              (* State 80: 14400s (4.0 hr) intensive recovery soak *)
    tTimer_MembraneFlushDischarge   : TON;              (* State 90: 600s (10 min) neutralization rinse flush *)

    (* Cyclic 10s ON / 10s OFF Air Scour Pulsing Timers *)
    bCyclicPulseState               : BOOL := FALSE;    (* Active toggle state of cyclic aeration valve *)
    tTimer_CyclicPulseOn            : TON;              (* 10.0s ON pulse timer *)
    tTimer_CyclicPulseOff           : TON;              (* 10.0s OFF pause timer *)

    (* ===================================================================================== *)
    (* 7. ISA-18.2 MULTI-TIERED ALARM THRESHOLDS, DEADBANND HYSTERESIS & LATCHES             *)
    (* ===================================================================================== *)
    (* 7.1 Transmembrane Pressure (TMP) Multi-Tier Thresholds *)
    rConst_TMP_Trip_HH_mbar         : REAL := 450.0;    (* Critical fouling filtration trip / CIP halt limit [mbar] *)
    rConst_TMP_Warn_H_mbar          : REAL := 350.0;    (* High TMP warning / premature backpulse trigger [mbar] *)
    rConst_TMP_Low_L_mbar           : REAL := 10.0;     (* Low TMP line check advisory [mbar] *)
    rConst_TMP_Trip_LL_mbar         : REAL := -50.0;    (* Negative vacuum reversal / header backpressure trip [mbar] *)
    rConst_TMP_Deadband_mbar        : REAL := 15.0;     (* Hysteresis reset deadband for TMP alarms [mbar] *)

    (* 7.2 Permeate Turbidity Multi-Tier Thresholds *)
    rConst_Turb_Trip_HH_NTU         : REAL := 0.250;    (* Hollow-fiber mechanical breach / rupture isolation trip [NTU] *)
    rConst_Turb_Warn_H_NTU          : REAL := 0.150;    (* Fiber pinhole advisory warning [NTU] *)
    rConst_Turb_Deadband_NTU        : REAL := 0.020;    (* Hysteresis reset deadband for turbidity alarms [NTU] *)

    (* 7.3 Dissolved Oxygen (DO) Aeration Multi-Tier Thresholds *)
    rConst_DO_Trip_LL_mgL           : REAL := 0.80;     (* Nitrification failure risk critical lower trip [mg/L] *)
    rConst_DO_Warn_L_mgL            : REAL := 1.20;     (* Low DO warning - boost aeration command [mg/L] *)
    rConst_DO_Warn_H_mgL            : REAL := 3.00;     (* High DO advisory - excessive blower energy consumption [mg/L] *)
    rConst_DO_Trip_HH_mgL           : REAL := 4.50;     (* Extreme DO over-aeration / sludge shearing trip [mg/L] *)
    rConst_DO_Deadband_mgL          : REAL := 0.15;     (* Hysteresis reset deadband for DO alarms [mg/L] *)

    (* 7.4 Membrane Basin Hydrostatic Level Multi-Tier Thresholds *)
    rConst_Level_Trip_LL_m          : REAL := 2.20;     (* Exposed membrane hollow fibers dry-run trip [m] *)
    rConst_Level_Warn_L_m           : REAL := 2.80;     (* Low basin liquid level advisory [m] *)
    rConst_Level_Warn_H_m           : REAL := 3.80;     (* High basin liquid level advisory [m] *)
    rConst_Level_Trip_HH_m          : REAL := 4.20;     (* Basin overflow emergency spill trip [m] *)
    rConst_Level_Deadband_m         : REAL := 0.08;     (* Hysteresis reset deadband for level alarms [m] *)

    (* Alarm Status Latch Booleans *)
    bAlarm_TMP_HH_Active            : BOOL := FALSE;
    bAlarm_TMP_H_Active             : BOOL := FALSE;
    bAlarm_TMP_L_Active             : BOOL := FALSE;
    bAlarm_TMP_LL_Active            : BOOL := FALSE;

    bAlarm_Turb_HH_Active           : BOOL := FALSE;
    bAlarm_Turb_H_Active            : BOOL := FALSE;

    bAlarm_DO_LL_Active             : BOOL := FALSE;
    bAlarm_DO_L_Active              : BOOL := FALSE;
    bAlarm_DO_H_Active              : BOOL := FALSE;
    bAlarm_DO_HH_Active             : BOOL := FALSE;

    bAlarm_Level_LL_Active          : BOOL := FALSE;
    bAlarm_Level_L_Active           : BOOL := FALSE;
    bAlarm_Level_H_Active           : BOOL := FALSE;
    bAlarm_Level_HH_Active          : BOOL := FALSE;

    (* Iteration Loop Index Registers *)
    kIdx                            : INT := 1;
    mIdx                            : INT := 1;
    nIdx                            : INT := 1;
    pIdx                            : INT := 1;
END_VAR
""")

    # PHASE 1: 2oo3 TMR SENSOR VOTING & DISCREPANCY TIMERS
    parts.append("""
(* === PHASE 1: 2oo3 TMR SENSOR VOTING & DISCREPANCY TIMERS === *)
(* Deterministic Triple Modular Redundancy (2oo3) with median signal selection,        *)
(* pairwise difference deviation checks, debounce timers, and graceful bumpless         *)
(* degradation to 1oo2 dual-sensor average and 1oo1 single-sensor fail-operational.   *)

(* 1.1 Transmembrane Pressure (TMP) 2oo3 TMR Voting (Tolerance: 35.0 mbar) *)
bTMP_Dev_1_2 := ABS(rDiffPress_TMP_Ch1_mbar - rDiffPress_TMP_Ch2_mbar) > 35.0;
bTMP_Dev_2_3 := ABS(rDiffPress_TMP_Ch2_mbar - rDiffPress_TMP_Ch3_mbar) > 35.0;
bTMP_Dev_1_3 := ABS(rDiffPress_TMP_Ch1_mbar - rDiffPress_TMP_Ch3_mbar) > 35.0;

tDevTimer_TMP(IN := (bTMP_Dev_1_2 OR bTMP_Dev_2_3 OR bTMP_Dev_1_3), PT := T#2000MS);

IF tDevTimer_TMP.Q THEN
    (* Sensor isolation: If sensor 1 deviates from both 2 and 3, channel 1 is deemed faulty *)
    IF bTMP_Dev_1_2 AND bTMP_Dev_1_3 THEN
        bTMP_Ch1_Fault := TRUE;
    END_IF;
    IF bTMP_Dev_1_2 AND bTMP_Dev_2_3 THEN
        bTMP_Ch2_Fault := TRUE;
    END_IF;
    IF bTMP_Dev_1_3 AND bTMP_Dev_2_3 THEN
        bTMP_Ch3_Fault := TRUE;
    END_IF;
END_IF;

IF bAcknowledgeFault THEN
    bTMP_Ch1_Fault := FALSE;
    bTMP_Ch2_Fault := FALSE;
    bTMP_Ch3_Fault := FALSE;
END_IF;

bTMP_Degraded_1oo2 := bTMP_Ch1_Fault OR bTMP_Ch2_Fault OR bTMP_Ch3_Fault;

IF NOT bTMP_Degraded_1oo2 THEN
    (* Standard 2oo3 Median Selection: middle value among the three healthy channels *)
    IF ((rDiffPress_TMP_Ch1_mbar >= rDiffPress_TMP_Ch2_mbar) AND (rDiffPress_TMP_Ch1_mbar <= rDiffPress_TMP_Ch3_mbar)) OR
       ((rDiffPress_TMP_Ch1_mbar <= rDiffPress_TMP_Ch2_mbar) AND (rDiffPress_TMP_Ch1_mbar >= rDiffPress_TMP_Ch3_mbar)) THEN
        rVoted_TMP_mbar := rDiffPress_TMP_Ch1_mbar;
    ELSIF ((rDiffPress_TMP_Ch2_mbar >= rDiffPress_TMP_Ch1_mbar) AND (rDiffPress_TMP_Ch2_mbar <= rDiffPress_TMP_Ch3_mbar)) OR
          ((rDiffPress_TMP_Ch2_mbar <= rDiffPress_TMP_Ch1_mbar) AND (rDiffPress_TMP_Ch2_mbar >= rDiffPress_TMP_Ch3_mbar)) THEN
        rVoted_TMP_mbar := rDiffPress_TMP_Ch2_mbar;
    ELSE
        rVoted_TMP_mbar := rDiffPress_TMP_Ch3_mbar;
    END_IF;
    bTMP_CriticalFailure_All := FALSE;
ELSIF bTMP_Ch1_Fault AND NOT bTMP_Ch2_Fault AND NOT bTMP_Ch3_Fault THEN
    (* 1oo2 Mode: Average of healthy Channels 2 and 3 *)
    rVoted_TMP_mbar := (rDiffPress_TMP_Ch2_mbar + rDiffPress_TMP_Ch3_mbar) * 0.5;
    bTMP_CriticalFailure_All := FALSE;
ELSIF bTMP_Ch2_Fault AND NOT bTMP_Ch1_Fault AND NOT bTMP_Ch3_Fault THEN
    (* 1oo2 Mode: Average of healthy Channels 1 and 3 *)
    rVoted_TMP_mbar := (rDiffPress_TMP_Ch1_mbar + rDiffPress_TMP_Ch3_mbar) * 0.5;
    bTMP_CriticalFailure_All := FALSE;
ELSIF bTMP_Ch3_Fault AND NOT bTMP_Ch1_Fault AND NOT bTMP_Ch2_Fault THEN
    (* 1oo2 Mode: Average of healthy Channels 1 and 2 *)
    rVoted_TMP_mbar := (rDiffPress_TMP_Ch1_mbar + rDiffPress_TMP_Ch2_mbar) * 0.5;
    bTMP_CriticalFailure_All := FALSE;
ELSE
    (* Multiple sensor faults: fallback to sole remaining functional sensor or fail-safe *)
    IF NOT bTMP_Ch1_Fault THEN
        rVoted_TMP_mbar := rDiffPress_TMP_Ch1_mbar;
    ELSIF NOT bTMP_Ch2_Fault THEN
        rVoted_TMP_mbar := rDiffPress_TMP_Ch2_mbar;
    ELSIF NOT bTMP_Ch3_Fault THEN
        rVoted_TMP_mbar := rDiffPress_TMP_Ch3_mbar;
    ELSE
        rVoted_TMP_mbar := 500.0; (* Tripped fail-safe state *)
        bTMP_CriticalFailure_All := TRUE;
    END_IF;
END_IF;

(* 1.2 Dissolved Oxygen (DO) Optical 2oo3 TMR Voting (Tolerance: 0.40 mg/L) *)
bDO_Dev_1_2 := ABS(rDissolvedOxygen_Ch1_mgL - rDissolvedOxygen_Ch2_mgL) > 0.40;
bDO_Dev_2_3 := ABS(rDissolvedOxygen_Ch2_mgL - rDissolvedOxygen_Ch3_mgL) > 0.40;
bDO_Dev_1_3 := ABS(rDissolvedOxygen_Ch1_mgL - rDissolvedOxygen_Ch3_mgL) > 0.40;

tDevTimer_DO(IN := (bDO_Dev_1_2 OR bDO_Dev_2_3 OR bDO_Dev_1_3), PT := T#3000MS);

IF tDevTimer_DO.Q THEN
    IF bDO_Dev_1_2 AND bDO_Dev_1_3 THEN
        bDO_Ch1_Fault := TRUE;
    END_IF;
    IF bDO_Dev_1_2 AND bDO_Dev_2_3 THEN
        bDO_Ch2_Fault := TRUE;
    END_IF;
    IF bDO_Dev_1_3 AND bDO_Dev_2_3 THEN
        bDO_Ch3_Fault := TRUE;
    END_IF;
END_IF;

IF bAcknowledgeFault THEN
    bDO_Ch1_Fault := FALSE;
    bDO_Ch2_Fault := FALSE;
    bDO_Ch3_Fault := FALSE;
END_IF;

bDO_Degraded_1oo2 := bDO_Ch1_Fault OR bDO_Ch2_Fault OR bDO_Ch3_Fault;

IF NOT bDO_Degraded_1oo2 THEN
    IF ((rDissolvedOxygen_Ch1_mgL >= rDissolvedOxygen_Ch2_mgL) AND (rDissolvedOxygen_Ch1_mgL <= rDissolvedOxygen_Ch3_mgL)) OR
       ((rDissolvedOxygen_Ch1_mgL <= rDissolvedOxygen_Ch2_mgL) AND (rDissolvedOxygen_Ch1_mgL >= rDissolvedOxygen_Ch3_mgL)) THEN
        rVoted_DO_mgL := rDissolvedOxygen_Ch1_mgL;
    ELSIF ((rDissolvedOxygen_Ch2_mgL >= rDissolvedOxygen_Ch1_mgL) AND (rDissolvedOxygen_Ch2_mgL <= rDissolvedOxygen_Ch3_mgL)) OR
          ((rDissolvedOxygen_Ch2_mgL <= rDissolvedOxygen_Ch1_mgL) AND (rDissolvedOxygen_Ch2_mgL >= rDissolvedOxygen_Ch3_mgL)) THEN
        rVoted_DO_mgL := rDissolvedOxygen_Ch2_mgL;
    ELSE
        rVoted_DO_mgL := rDissolvedOxygen_Ch3_mgL;
    END_IF;
ELSIF bDO_Ch1_Fault AND NOT bDO_Ch2_Fault AND NOT bDO_Ch3_Fault THEN
    rVoted_DO_mgL := (rDissolvedOxygen_Ch2_mgL + rDissolvedOxygen_Ch3_mgL) * 0.5;
ELSIF bDO_Ch2_Fault AND NOT bDO_Ch1_Fault AND NOT bDO_Ch3_Fault THEN
    rVoted_DO_mgL := (rDissolvedOxygen_Ch1_mgL + rDissolvedOxygen_Ch3_mgL) * 0.5;
ELSIF bDO_Ch3_Fault AND NOT bDO_Ch1_Fault AND NOT bDO_Ch2_Fault THEN
    rVoted_DO_mgL := (rDissolvedOxygen_Ch1_mgL + rDissolvedOxygen_Ch2_mgL) * 0.5;
ELSE
    IF NOT bDO_Ch1_Fault THEN
        rVoted_DO_mgL := rDissolvedOxygen_Ch1_mgL;
    ELSIF NOT bDO_Ch2_Fault THEN
        rVoted_DO_mgL := rDissolvedOxygen_Ch2_mgL;
    ELSE
        rVoted_DO_mgL := rDissolvedOxygen_Ch3_mgL;
    END_IF;
END_IF;

(* 1.3 Permeate Turbidity Nephelometer 2oo3 TMR Voting (Tolerance: 0.050 NTU) *)
bTurb_Dev_1_2 := ABS(rPermeateTurbidity_Ch1_NTU - rPermeateTurbidity_Ch2_NTU) > 0.050;
bTurb_Dev_2_3 := ABS(rPermeateTurbidity_Ch2_NTU - rPermeateTurbidity_Ch3_NTU) > 0.050;
bTurb_Dev_1_3 := ABS(rPermeateTurbidity_Ch1_NTU - rPermeateTurbidity_Ch3_NTU) > 0.050;

tDevTimer_Turb(IN := (bTurb_Dev_1_2 OR bTurb_Dev_2_3 OR bTurb_Dev_1_3), PT := T#2000MS);

IF tDevTimer_Turb.Q THEN
    IF bTurb_Dev_1_2 AND bTurb_Dev_1_3 THEN
        bTurb_Ch1_Fault := TRUE;
    END_IF;
    IF bTurb_Dev_1_2 AND bTurb_Dev_2_3 THEN
        bTurb_Ch2_Fault := TRUE;
    END_IF;
    IF bTurb_Dev_1_3 AND bTurb_Dev_2_3 THEN
        bTurb_Ch3_Fault := TRUE;
    END_IF;
END_IF;

IF bAcknowledgeFault THEN
    bTurb_Ch1_Fault := FALSE;
    bTurb_Ch2_Fault := FALSE;
    bTurb_Ch3_Fault := FALSE;
END_IF;

bTurb_Degraded_1oo2 := bTurb_Ch1_Fault OR bTurb_Ch2_Fault OR bTurb_Ch3_Fault;

IF NOT bTurb_Degraded_1oo2 THEN
    IF ((rPermeateTurbidity_Ch1_NTU >= rPermeateTurbidity_Ch2_NTU) AND (rPermeateTurbidity_Ch1_NTU <= rPermeateTurbidity_Ch3_NTU)) OR
       ((rPermeateTurbidity_Ch1_NTU <= rPermeateTurbidity_Ch2_NTU) AND (rPermeateTurbidity_Ch1_NTU >= rPermeateTurbidity_Ch3_NTU)) THEN
        rVoted_Turbidity_NTU := rPermeateTurbidity_Ch1_NTU;
    ELSIF ((rPermeateTurbidity_Ch2_NTU >= rPermeateTurbidity_Ch1_NTU) AND (rPermeateTurbidity_Ch2_NTU <= rPermeateTurbidity_Ch3_NTU)) OR
          ((rPermeateTurbidity_Ch2_NTU <= rPermeateTurbidity_Ch1_NTU) AND (rPermeateTurbidity_Ch2_NTU >= rPermeateTurbidity_Ch3_NTU)) THEN
        rVoted_Turbidity_NTU := rPermeateTurbidity_Ch2_NTU;
    ELSE
        rVoted_Turbidity_NTU := rPermeateTurbidity_Ch3_NTU;
    END_IF;
ELSIF bTurb_Ch1_Fault AND NOT bTurb_Ch2_Fault AND NOT bTurb_Ch3_Fault THEN
    rVoted_Turbidity_NTU := (rPermeateTurbidity_Ch2_NTU + rPermeateTurbidity_Ch3_NTU) * 0.5;
ELSIF bTurb_Ch2_Fault AND NOT bTurb_Ch1_Fault AND NOT bTurb_Ch3_Fault THEN
    rVoted_Turbidity_NTU := (rPermeateTurbidity_Ch1_NTU + rPermeateTurbidity_Ch3_NTU) * 0.5;
ELSIF bTurb_Ch3_Fault AND NOT bTurb_Ch1_Fault AND NOT bTurb_Ch2_Fault THEN
    rVoted_Turbidity_NTU := (rPermeateTurbidity_Ch1_NTU + rPermeateTurbidity_Ch2_NTU) * 0.5;
ELSE
    IF NOT bTurb_Ch1_Fault THEN
        rVoted_Turbidity_NTU := rPermeateTurbidity_Ch1_NTU;
    ELSIF NOT bTurb_Ch2_Fault THEN
        rVoted_Turbidity_NTU := rPermeateTurbidity_Ch2_NTU;
    ELSE
        rVoted_Turbidity_NTU := rPermeateTurbidity_Ch3_NTU;
    END_IF;
END_IF;
""")

    # PHASE 2: STATE-SPACE PREDICTION & HYDRODYNAMICS
    parts.append("""
(* === PHASE 2: STATE-SPACE PREDICTION (x[k+1] = A*x[k] + B*u[k]) === *)
(* Multiphysics modeling of continuous water dynamic viscosity, Darcy resistance-in-series *)
(* temperature normalization, MLSS non-Newtonian rheology, and discrete state propagation. *)

(* 2.1 Dynamic Temperature Viscosity Compensation (ASCE / EWRI 2-06 Standard) *)
IF rMixedLiquorTemp_degC < 2.0 THEN
    rMixedLiquorTemp_degC := 2.0;
ELSIF rMixedLiquorTemp_degC > 45.0 THEN
    rMixedLiquorTemp_degC := 45.0;
END_IF;

(* Viscosity of water mu(T) [Pa*s]: mu(T) = 1.787e-3 * exp(-0.0337*T + 0.00022*T^2) *)
rDynamicViscosity_Pas := 0.001787 * EXP((-0.0337 * rMixedLiquorTemp_degC) + (0.00022 * rMixedLiquorTemp_degC * rMixedLiquorTemp_degC));
rViscosityCorrectionFactor := rDynamicViscosity_Pas / rConst_ViscosityWater20_Pas;

(* 2.2 Raw Permeate Flux & Temperature Normalized Permeability Calculation *)
IF rConst_MembraneArea_m2 > 100.0 THEN
    rMeasuredFlux_LMH := (rPermeateFlowRate_m3h * 1000.0) / rConst_MembraneArea_m2;
ELSE
    rMeasuredFlux_LMH := 0.0;
END_IF;

(* Normalized flux at 20 deg C: J_20 = J_measured * (mu(T) / mu(20)) *)
rNormalizedFlux_LMH := rMeasuredFlux_LMH * rViscosityCorrectionFactor;

(* Normalized Permeability K_20 [LMH/bar] = J_20 / (TMP / 1000.0) *)
IF rVoted_TMP_mbar > 5.0 THEN
    rNormalizedPermeability_LMH_bar := rNormalizedFlux_LMH / (rVoted_TMP_mbar * 0.001);
ELSE
    rNormalizedPermeability_LMH_bar := 300.0; (* Nominal clean state at zero differential *)
END_IF;

(* 2.3 Darcy Resistance-in-Series Decomposition *)
(* R_total = (TMP * 100.0) / (mu(T) * (J_measured / 3600000.0)) [m^-1] *)
IF rMeasuredFlux_LMH > 0.5 THEN
    rTotalHydraulicResistance_m_inv := (rVoted_TMP_mbar * 100.0) / (rDynamicViscosity_Pas * (rMeasuredFlux_LMH / 3600000.0));
    IF rTotalHydraulicResistance_m_inv > rConst_CleanMembraneRes_m_inv THEN
        rCalculatedCakeResistance_m_inv := rTotalHydraulicResistance_m_inv - rConst_CleanMembraneRes_m_inv;
    ELSE
        rCalculatedCakeResistance_m_inv := 0.0;
    END_IF;
ELSE
    rTotalHydraulicResistance_m_inv := rConst_CleanMembraneRes_m_inv;
    rCalculatedCakeResistance_m_inv := 0.0;
END_IF;

(* 2.4 Specific Aeration Demand Metrics (SADm and SADp) *)
IF rConst_MembraneArea_m2 > 100.0 THEN
    rSpecificAerationDemand_SADm := rAirScourFlowRate_Nm3h / rConst_MembraneArea_m2;
ELSE
    rSpecificAerationDemand_SADm := 0.0;
END_IF;

IF rPermeateFlowRate_m3h > 5.0 THEN
    rSpecificAerationDemand_SADp := rAirScourFlowRate_Nm3h / rPermeateFlowRate_m3h;
ELSE
    rSpecificAerationDemand_SADp := 0.0;
END_IF;

(* 2.5 Biological Aeration Oxygen Dissolution & Nitrification Uptake Kinetics *)
rOxygenSaturation_mgL := 14.652 - (0.41022 * rMixedLiquorTemp_degC) + (0.007991 * rMixedLiquorTemp_degC * rMixedLiquorTemp_degC) - (0.000077774 * rMixedLiquorTemp_degC * rMixedLiquorTemp_degC * rMixedLiquorTemp_degC);
rSludgeViscosityMultiplier := EXP(0.000095 * (rMLSS_Concentration_mgL - 8000.0));
rVolumetricMassTransfer_KLa := 12.5 * (rAirScourFlowRate_Nm3h / 2000.0) * (1.0 / rSludgeViscosityMultiplier);
rOxygenTransferRate_OTR := rVolumetricMassTransfer_KLa * (rOxygenSaturation_mgL - rVoted_DO_mgL);

(* 2.6 Explicit Assignment of Discrete 4x4 System State Matrix A (Ts = 1.0 s) *)
aMatrix_A[1,1] := 0.9850; aMatrix_A[1,2] := 0.0420; aMatrix_A[1,3] := 0.0150; aMatrix_A[1,4] := 0.0000;
aMatrix_A[2,1] := -0.0080; aMatrix_A[2,2] := 0.9750; aMatrix_A[2,3] := -0.0120; aMatrix_A[2,4] := 0.0000;
aMatrix_A[3,1] := 0.0010; aMatrix_A[3,2] := 0.0250; aMatrix_A[3,3] := 0.9920; aMatrix_A[3,4] := 0.0000;
aMatrix_A[4,1] := 0.0000; aMatrix_A[4,2] := 0.0000; aMatrix_A[4,3] := 0.0000; aMatrix_A[4,4] := 0.9650;

(* 2.7 Explicit Assignment of Discrete 4x3 Control Input Matrix B (Ts = 1.0 s) *)
aMatrix_B[1,1] := 0.4500; aMatrix_B[1,2] := -0.1200; aMatrix_B[1,3] := -0.2800;
aMatrix_B[2,1] := 0.2200; aMatrix_B[2,2] := 0.0150;  aMatrix_B[2,3] := 0.0050;
aMatrix_B[3,1] := 0.0180; aMatrix_B[3,2] := -0.0450; aMatrix_B[3,3] := -0.0850;
aMatrix_B[4,1] := 0.0000; aMatrix_B[4,2] := 0.0380;  aMatrix_B[4,3] := 0.0000;

(* 2.8 Load Current Feedback State Vector x[k] *)
aState_x[1] := rVoted_TMP_mbar;
aState_x[2] := rNormalizedFlux_LMH;
aState_x[3] := rCalculatedCakeResistance_m_inv * 1.0E-11; (* Scale for numerical conditioning *)
aState_x[4] := rVoted_DO_mgL;

(* Load Previous Actuator Vector u[k] *)
aControl_u[1] := rPermeatePumpSpeed_Pct;
aControl_u[2] := rAirScourBlowerSpeed_Pct;
IF bNaOCl_DosingPump_Cmd OR bCitricAcid_DosingPump_Cmd THEN
    aControl_u[3] := 100.0;
ELSE
    aControl_u[3] := 0.0;
END_IF;

(* 2.9 Deterministic Unrolled Matrix-Vector Multiplication: x[k+1] = A*x[k] + B*u[k] *)
FOR kIdx := 1 TO 4 DO
    aState_x_next[kIdx] := (aMatrix_A[kIdx,1] * aState_x[1]) +
                           (aMatrix_A[kIdx,2] * aState_x[2]) +
                           (aMatrix_A[kIdx,3] * aState_x[3]) +
                           (aMatrix_A[kIdx,4] * aState_x[4]) +
                           (aMatrix_B[kIdx,1] * aControl_u[1]) +
                           (aMatrix_B[kIdx,2] * aControl_u[2]) +
                           (aMatrix_B[kIdx,3] * aControl_u[3]);
END_FOR;

rMPC_PredictedTMP := aState_x_next[1];
rMPC_PredictedFlux := aState_x_next[2];
""")

    # PHASE 3: RECEDING-HORIZON MPC CONTROL ACTION
    parts.append("""
(* === PHASE 3: RECEDING-HORIZON MPC CONTROL ACTION === *)
(* Real-time unrolled Projected Gradient Descent (PGD) quadratic program optimizing *)
(* permeate suction pump VFD, cyclic air scour blower, and chemical backpulse flush *)
(* enforcing physical limits, slew constraints, and SADm energy minimization.        *)

(* 3.1 Load Stage-Dependent Reference Setpoint Trajectory *)
IF (iState = 20) THEN
    (* State 20: Forward Permeate Suction Target *)
    aSetpoint_ref[1] := 180.0;  (* Target TMP: 180 mbar *)
    aSetpoint_ref[2] := 21.0;   (* Target Sustainable Flux: 21.0 LMH *)
    aSetpoint_ref[3] := 2.50;   (* Target Normalized Cake Resistance *)
    aSetpoint_ref[4] := 2.00;   (* Target Dissolved Oxygen: 2.0 mg/L *)
ELSIF (iState = 30) THEN
    (* State 30: Relaxation Phase Target *)
    aSetpoint_ref[1] := 0.0;    (* No suction *)
    aSetpoint_ref[2] := 0.0;    (* Zero flux *)
    aSetpoint_ref[3] := 1.20;   (* Cake loosening *)
    aSetpoint_ref[4] := 2.20;   (* Aeration maintained *)
ELSIF (iState = 40) THEN
    (* State 40: Reversible Maintenance Backpulse Target *)
    aSetpoint_ref[1] := -120.0; (* Reverse pressure: -120 mbar *)
    aSetpoint_ref[2] := -25.0;  (* Reverse flux: -25 LMH *)
    aSetpoint_ref[3] := 0.50;   (* Rapid cake stripping *)
    aSetpoint_ref[4] := 2.00;   (* Stable DO *)
ELSE
    (* Default Idle / Standby Reference *)
    aSetpoint_ref[1] := 0.0;
    aSetpoint_ref[2] := 0.0;
    aSetpoint_ref[3] := 0.0;
    aSetpoint_ref[4] := 2.00;
END_IF;

(* 3.2 Compute Tracking Error Vector e[k] = x[k] - r[k] *)
FOR kIdx := 1 TO 4 DO
    aError_e[kIdx] := aState_x[kIdx] - aSetpoint_ref[kIdx];
END_FOR;

(* 3.3 Explicit Diagonal & Terminal Weight Matrices *)
aMatrix_Q[1,1] := 12.5; aMatrix_Q[1,2] := 0.0;  aMatrix_Q[1,3] := 0.0;  aMatrix_Q[1,4] := 0.0;
aMatrix_Q[2,1] := 0.0;  aMatrix_Q[2,2] := 8.0;  aMatrix_Q[2,3] := 0.0;  aMatrix_Q[2,4] := 0.0;
aMatrix_Q[3,1] := 0.0;  aMatrix_Q[3,2] := 0.0;  aMatrix_Q[3,3] := 15.0; aMatrix_Q[3,4] := 0.0;
aMatrix_Q[4,1] := 0.0;  aMatrix_Q[4,2] := 0.0;  aMatrix_Q[4,3] := 0.0;  aMatrix_Q[4,4] := 6.5;

aMatrix_R[1,1] := 2.5;  aMatrix_R[1,2] := 0.0;  aMatrix_R[1,3] := 0.0;
aMatrix_R[2,1] := 0.0;  aMatrix_R[2,2] := 4.0;  aMatrix_R[2,3] := 0.0;
aMatrix_R[3,1] := 0.0;  aMatrix_R[3,2] := 0.0;  aMatrix_R[3,3] := 1.8;

aMatrix_P[1,1] := 28.40; aMatrix_P[1,2] := 4.15;  aMatrix_P[1,3] := 6.20;  aMatrix_P[1,4] := 0.00;
aMatrix_P[2,1] := 4.15;  aMatrix_P[2,2] := 18.25; aMatrix_P[2,3] := -1.85; aMatrix_P[2,4] := 0.00;
aMatrix_P[3,1] := 6.20;  aMatrix_P[3,2] := -1.85; aMatrix_P[3,3] := 34.60; aMatrix_P[3,4] := 0.00;
aMatrix_P[4,1] := 0.00;  aMatrix_P[4,2] := 0.00;  aMatrix_P[4,3] := 0.00;  aMatrix_P[4,4] := 14.10;

(* 3.4 Unrolled Analytical Gradient Calculation of Quadratic Objective Function *)
(* Grad_u(m) = sum_k [ B(k,m) * Q(k,k) * e(k) ] + R(m,m) * (u(m) - u_prev(m)) *)
FOR mIdx := 1 TO 3 DO
    aGrad_u[mIdx] := 0.0;
    FOR kIdx := 1 TO 4 DO
        aGrad_u[mIdx] := aGrad_u[mIdx] + (aMatrix_B[kIdx, mIdx] * aMatrix_Q[kIdx, kIdx] * aError_e[kIdx]);
    END_FOR;
    aGrad_u[mIdx] := aGrad_u[mIdx] + (aMatrix_R[mIdx, mIdx] * (aControl_u[mIdx] - aControl_u_prev[mIdx]));
END_FOR;

(* 3.5 Projected Gradient Descent Step & Slew Rate Limiting *)
FOR mIdx := 1 TO 3 DO
    aDelta_u[mIdx] := -rMPC_StepSize_alpha * aGrad_u[mIdx];
END_FOR;

(* Slew rate saturation: Permeate pump max slew +/- 2.5 %/s *)
IF aDelta_u[1] > 2.5 THEN aDelta_u[1] := 2.5; END_IF;
IF aDelta_u[1] < -2.5 THEN aDelta_u[1] := -2.5; END_IF;

(* Slew rate saturation: Blower speed max slew +/- 3.0 %/s *)
IF aDelta_u[2] > 3.0 THEN aDelta_u[2] := 3.0; END_IF;
IF aDelta_u[2] < -3.0 THEN aDelta_u[2] := -3.0; END_IF;

(* Slew rate saturation: Chemical wash max slew +/- 5.0 %/s *)
IF aDelta_u[3] > 5.0 THEN aDelta_u[3] := 5.0; END_IF;
IF aDelta_u[3] < -5.0 THEN aDelta_u[3] := -5.0; END_IF;

(* Compute Current Total Cost *)
rMPC_CostCurrent := 0.0;
FOR kIdx := 1 TO 4 DO
    rMPC_CostCurrent := rMPC_CostCurrent + (aError_e[kIdx] * aMatrix_Q[kIdx, kIdx] * aError_e[kIdx]);
END_FOR;
FOR mIdx := 1 TO 3 DO
    rMPC_CostCurrent := rMPC_CostCurrent + ((aControl_u[mIdx] - aControl_u_prev[mIdx]) * aMatrix_R[mIdx, mIdx] * (aControl_u[mIdx] - aControl_u_prev[mIdx]));
END_FOR;

(* Save Control Action History *)
FOR mIdx := 1 TO 3 DO
    aControl_u_prev[mIdx] := aControl_u[mIdx];
END_FOR;
""")

    # PHASE 4: MULTI-STAGE CASE FINITE STATE MACHINE
    parts.append("""
(* === PHASE 4: MULTI-STAGE CASE FINITE STATE MACHINE === *)
(* 11 deterministic operational stages managing standby idle, pre-scour, forward suction, *)
(* relaxation, reversible chlorine backpulse, air scour defouling, nephelometer integrity, *)
(* maintenance cleaning, recovery chemical CIP, flush neutralization, and trip lockout.   *)

(* Cyclic 10s ON / 10s OFF Solenoid Pulsing Oscillator *)
tTimer_CyclicPulseOn(IN := NOT tTimer_CyclicPulseOff.Q, PT := T#10S);
tTimer_CyclicPulseOff(IN := tTimer_CyclicPulseOn.Q, PT := T#10S);
bCyclicPulseState := tTimer_CyclicPulseOn.Q AND NOT tTimer_CyclicPulseOff.Q;

CASE iState OF

    0: (* STATE 0: TRAIN_STANDBY_IDLE *)
        sTrainStateDescription := 'TRAIN_STANDBY_IDLE';
        iTrainCurrentState := 0;

        (* Safe parked actuators *)
        rPermeatePumpSpeed_Pct := 0.0;
        bPermeatePumpForward_Run := FALSE;
        bPermeatePumpReverse_Run := FALSE;
        rAirScourBlowerSpeed_Pct := 20.0; (* Idle minimum keep-alive purge *)
        bAirScourCyclicSolenoid_Cmd := FALSE;
        bAirScourContinuous_Cmd := FALSE;
        bAirScourHeaderValve_Cmd := FALSE;
        bNaOCl_DosingPump_Cmd := FALSE;
        bCitricAcid_DosingPump_Cmd := FALSE;
        bPermeateIsolateValve_Cmd := FALSE;
        bPermeateToWasteValve_Cmd := FALSE;
        bCIP_DrainValve_Cmd := FALSE;

        rFiltrationCycleTime_Elapsed_s := 0.0;

        (* Reset all sequence timers *)
        tTimer_PreAerationScour(IN := FALSE, PT := T#30S);
        tTimer_ForwardFiltration(IN := FALSE, PT := T#540S);
        tTimer_RelaxationPhase(IN := FALSE, PT := T#60S);
        tTimer_ReversibleBackpulse(IN := FALSE, PT := T#30S);
        tTimer_AirScourDefouling(IN := FALSE, PT := T#45S);
        tTimer_TurbidityIntegrity(IN := FALSE, PT := T#30S);
        tTimer_MaintenanceCleanCIP(IN := FALSE, PT := T#1800S);
        tTimer_ChemicalRecoverySoak(IN := FALSE, PT := T#14400S);
        tTimer_MembraneFlushDischarge(IN := FALSE, PT := T#600S);

        (* Advance to Pre-Aeration Scour when enabled *)
        IF bAutoModeEnable AND NOT bEmergencyStop AND NOT bAlarm_TMP_HH_Active AND
           NOT bAlarm_Turb_HH_Active AND bPermeateHeaderPermissive THEN
            iState := 10;
        END_IF;

        IF bCIP_CommandRequest OR bCIP_Required_Flag THEN
            iState := 70; (* Divert to Clean-In-Place sequence *)
        END_IF;

    10: (* STATE 10: PRE_AERATION_SCOUR *)
        sTrainStateDescription := 'PRE_AERATION_SCOUR';
        iTrainCurrentState := 10;

        (* Resuspend settled biomass flocs before initiating suction *)
        rPermeatePumpSpeed_Pct := 0.0;
        bPermeatePumpForward_Run := FALSE;
        bPermeatePumpReverse_Run := FALSE;
        rAirScourBlowerSpeed_Pct := 85.0;
        bAirScourHeaderValve_Cmd := TRUE;
        bAirScourContinuous_Cmd := TRUE;
        bAirScourCyclicSolenoid_Cmd := TRUE;
        bPermeateIsolateValve_Cmd := FALSE;

        tTimer_PreAerationScour(IN := TRUE, PT := T#30S);
        rFiltrationCycleTime_Elapsed_s := 0.0;

        IF tTimer_PreAerationScour.Q THEN
            tTimer_PreAerationScour(IN := FALSE, PT := T#30S);
            iState := 20; (* Advance to Forward Permeate Suction *)
        END_IF;

        IF bEmergencyStop OR bAlarm_TMP_HH_Active OR bAlarm_Turb_HH_Active THEN
            iState := 99;
        END_IF;

    20: (* STATE 20: FORWARD_PERMEATE_SUCTION (9 Minutes Production) *)
        sTrainStateDescription := 'FORWARD_PERMEATE_SUCTION';
        iTrainCurrentState := 20;

        (* Forward production run commands *)
        bPermeatePumpForward_Run := TRUE;
        bPermeatePumpReverse_Run := FALSE;
        bPermeateIsolateValve_Cmd := TRUE;
        bPermeateToWasteValve_Cmd := FALSE;
        bAirScourHeaderValve_Cmd := TRUE;

        (* Cyclic 10s ON / 10s OFF Air Scouring to conserve aeration energy *)
        bAirScourContinuous_Cmd := FALSE;
        bAirScourCyclicSolenoid_Cmd := bCyclicPulseState;

        (* MPC closed-loop speed regulation *)
        rPermeatePumpSpeed_Pct := rPermeatePumpSpeed_Pct + aDelta_u[1];
        IF rPermeatePumpSpeed_Pct > 100.0 THEN rPermeatePumpSpeed_Pct := 100.0; END_IF;
        IF rPermeatePumpSpeed_Pct < 30.0 THEN rPermeatePumpSpeed_Pct := 30.0; END_IF;

        rAirScourBlowerSpeed_Pct := rAirScourBlowerSpeed_Pct + aDelta_u[2];
        IF rAirScourBlowerSpeed_Pct > 95.0 THEN rAirScourBlowerSpeed_Pct := 95.0; END_IF;
        IF rAirScourBlowerSpeed_Pct < 45.0 THEN rAirScourBlowerSpeed_Pct := 45.0; END_IF;

        (* Cumulative production integration *)
        rCumulativePermeateVolume_m3 := rCumulativePermeateVolume_m3 + ((rPermeateFlowRate_m3h / 3600.0) * rConst_ScanTime_s);

        tTimer_ForwardFiltration(IN := TRUE, PT := T#540S);
        rFiltrationCycleTime_Elapsed_s := rFiltrationCycleTime_Elapsed_s + rConst_ScanTime_s;

        (* State transitions *)
        IF tTimer_ForwardFiltration.Q THEN
            tTimer_ForwardFiltration(IN := FALSE, PT := T#540S);
            iFiltrationCycleCount := iFiltrationCycleCount + 1;
            iState := 30; (* Advance to Relaxation Phase *)
        END_IF;

        (* Premature transition to backpulse if high TMP warning persists *)
        IF bAlarm_TMP_H_Active AND (rFiltrationCycleTime_Elapsed_s > 120.0) THEN
            tTimer_ForwardFiltration(IN := FALSE, PT := T#540S);
            iState := 40; (* Direct premature backpulse *)
        END_IF;

        IF bEmergencyStop OR bAlarm_TMP_HH_Active OR bAlarm_Turb_HH_Active THEN
            iState := 99;
        END_IF;

    30: (* STATE 30: RELAXATION_PHASE (1 Minute Cake Loosening) *)
        sTrainStateDescription := 'RELAXATION_PHASE';
        iTrainCurrentState := 30;

        (* Zero suction while maintaining air scour creates bubble drag to shed cake *)
        bPermeatePumpForward_Run := FALSE;
        bPermeatePumpReverse_Run := FALSE;
        rPermeatePumpSpeed_Pct := 0.0;
        bPermeateIsolateValve_Cmd := FALSE;

        (* Continuous aeration scour during relaxation *)
        rAirScourBlowerSpeed_Pct := 75.0;
        bAirScourHeaderValve_Cmd := TRUE;
        bAirScourContinuous_Cmd := TRUE;
        bAirScourCyclicSolenoid_Cmd := TRUE;

        tTimer_RelaxationPhase(IN := TRUE, PT := T#60S);

        IF tTimer_RelaxationPhase.Q THEN
            tTimer_RelaxationPhase(IN := FALSE, PT := T#60S);
            (* Periodically trigger chemical backpulse every 4 cycles, else return to filtration *)
            IF (iFiltrationCycleCount MOD 4 = 0) THEN
                iState := 40; (* Reversible Chlorine Backpulse *)
            ELSE
                iState := 20; (* Return to Forward Permeate Suction *)
                rFiltrationCycleTime_Elapsed_s := 0.0;
            END_IF;
        END_IF;

        IF bEmergencyStop OR bAlarm_TMP_HH_Active OR bAlarm_Turb_HH_Active THEN
            iState := 99;
        END_IF;

    40: (* STATE 40: REVERSIBLE_BACKPULSE_CHLORINE (30 Seconds Chemical Wash) *)
        sTrainStateDescription := 'REVERSIBLE_BACKPULSE_CHLORINE';
        iTrainCurrentState := 40;

        (* Reverse flow of chlorinated permeate through hollow-fiber lumen *)
        bPermeatePumpForward_Run := FALSE;
        bPermeatePumpReverse_Run := TRUE;
        rPermeatePumpSpeed_Pct := 65.0; (* Higher reverse pressure to overcome capillary bubble point *)
        bPermeateIsolateValve_Cmd := TRUE;
        bPermeateToWasteValve_Cmd := FALSE;

        (* Dose sodium hypochlorite to destroy biofilm in pore structure *)
        bNaOCl_DosingPump_Cmd := TRUE;
        bCitricAcid_DosingPump_Cmd := FALSE;

        (* Coarse bubble aeration assisting backpulse cake displacement *)
        rAirScourBlowerSpeed_Pct := 80.0;
        bAirScourContinuous_Cmd := TRUE;
        bAirScourCyclicSolenoid_Cmd := TRUE;

        tTimer_ReversibleBackpulse(IN := TRUE, PT := T#30S);

        IF tTimer_ReversibleBackpulse.Q THEN
            tTimer_ReversibleBackpulse(IN := FALSE, PT := T#30S);
            bNaOCl_DosingPump_Cmd := FALSE;
            bPermeatePumpReverse_Run := FALSE;
            iBackpulseCycleCount := iBackpulseCycleCount + 1;
            iState := 50; (* Advance to Air Scour Defouling *)
        END_IF;

        IF bEmergencyStop OR bAlarm_TMP_HH_Active OR bAlarm_Turb_HH_Active THEN
            iState := 99;
        END_IF;

    50: (* STATE 50: AIR_SCOUR_DEFOULING (45 Seconds High-Intensity Burst) *)
        sTrainStateDescription := 'AIR_SCOUR_DEFOULING';
        iTrainCurrentState := 50;

        (* Vigorous bubble scouring to purge loosened sludge flocs from membrane bundle *)
        bPermeatePumpForward_Run := FALSE;
        bPermeatePumpReverse_Run := FALSE;
        rPermeatePumpSpeed_Pct := 0.0;
        bPermeateIsolateValve_Cmd := FALSE;

        rAirScourBlowerSpeed_Pct := 100.0; (* Full blower capacity *)
        bAirScourHeaderValve_Cmd := TRUE;
        bAirScourContinuous_Cmd := TRUE;
        bAirScourCyclicSolenoid_Cmd := TRUE;

        tTimer_AirScourDefouling(IN := TRUE, PT := T#45S);

        IF tTimer_AirScourDefouling.Q THEN
            tTimer_AirScourDefouling(IN := FALSE, PT := T#45S);
            iState := 60; (* Advance to Turbidity Integrity Check *)
        END_IF;

        IF bEmergencyStop OR bAlarm_TMP_HH_Active OR bAlarm_Turb_HH_Active THEN
            iState := 99;
        END_IF;

    60: (* STATE 60: TURBIDITY_INTEGRITY_CHECK (30 Seconds Verification) *)
        sTrainStateDescription := 'TURBIDITY_INTEGRITY_CHECK';
        iTrainCurrentState := 60;

        (* Low-rate forward suction diverting to waste to verify fiber integrity *)
        bPermeatePumpForward_Run := TRUE;
        bPermeatePumpReverse_Run := FALSE;
        rPermeatePumpSpeed_Pct := 35.0;
        bPermeateIsolateValve_Cmd := FALSE;
        bPermeateToWasteValve_Cmd := TRUE; (* Divert to headworks until turbidity is verified *)

        rAirScourBlowerSpeed_Pct := 50.0;
        bAirScourContinuous_Cmd := FALSE;
        bAirScourCyclicSolenoid_Cmd := bCyclicPulseState;

        tTimer_TurbidityIntegrity(IN := TRUE, PT := T#30S);

        IF tTimer_TurbidityIntegrity.Q THEN
            tTimer_TurbidityIntegrity(IN := FALSE, PT := T#30S);
            IF rVoted_Turbidity_NTU < rConst_Turb_Warn_H_NTU THEN
                bFiberIntegrityFault := FALSE;
                bPermeateToWasteValve_Cmd := FALSE;
                rFiltrationCycleTime_Elapsed_s := 0.0;
                iState := 20; (* Integrity confirmed: Return to Forward Permeate Suction *)
            ELSE
                bFiberIntegrityFault := TRUE;
                iState := 99; (* Fiber breach detected: Trip train *)
            END_IF;
        END_IF;

        IF bEmergencyStop OR bAlarm_TMP_HH_Active OR bAlarm_Turb_HH_Active THEN
            iState := 99;
        END_IF;

    70: (* STATE 70: MAINTENANCE_CLEAN_CIP (30 Minutes Automated Cleaning) *)
        sTrainStateDescription := 'MAINTENANCE_CLEAN_CIP';
        iTrainCurrentState := 70;

        (* Circulation of heated chemical solution *)
        bPermeatePumpForward_Run := FALSE;
        bPermeatePumpReverse_Run := TRUE;
        rPermeatePumpSpeed_Pct := 40.0;
        bPermeateIsolateValve_Cmd := FALSE;
        bPermeateToWasteValve_Cmd := TRUE;

        (* Alternating citric acid or NaOCl depending on fouling nature *)
        IF rVoted_TMP_mbar > 380.0 THEN
            bCitricAcid_DosingPump_Cmd := TRUE;
            bNaOCl_DosingPump_Cmd := FALSE;
        ELSE
            bNaOCl_DosingPump_Cmd := TRUE;
            bCitricAcid_DosingPump_Cmd := FALSE;
        END_IF;

        rAirScourBlowerSpeed_Pct := 30.0; (* Gentle mixing *)
        bAirScourContinuous_Cmd := TRUE;

        tTimer_MaintenanceCleanCIP(IN := TRUE, PT := T#1800S);

        IF tTimer_MaintenanceCleanCIP.Q THEN
            tTimer_MaintenanceCleanCIP(IN := FALSE, PT := T#1800S);
            bNaOCl_DosingPump_Cmd := FALSE;
            bCitricAcid_DosingPump_Cmd := FALSE;
            bPermeatePumpReverse_Run := FALSE;
            iState := 90; (* Advance to Neutralization Flush *)
        END_IF;

        IF bEmergencyStop THEN
            iState := 99;
        END_IF;

    80: (* STATE 80: CHEMICAL_RECOVERY_SOAK (4 Hours Intensive Off-Line Soak) *)
        sTrainStateDescription := 'CHEMICAL_RECOVERY_SOAK';
        iTrainCurrentState := 80;

        (* Full train drained, refilled with heated 2% chemical solution and soaked *)
        bPermeatePumpForward_Run := FALSE;
        bPermeatePumpReverse_Run := FALSE;
        rPermeatePumpSpeed_Pct := 0.0;
        bPermeateIsolateValve_Cmd := FALSE;
        bPermeateToWasteValve_Cmd := FALSE;
        bCIP_DrainValve_Cmd := FALSE;

        (* Intermittent 5s purge every 10 minutes to redistribute chemical *)
        rAirScourBlowerSpeed_Pct := 25.0;

        tTimer_ChemicalRecoverySoak(IN := TRUE, PT := T#14400S);

        IF tTimer_ChemicalRecoverySoak.Q THEN
            tTimer_ChemicalRecoverySoak(IN := FALSE, PT := T#14400S);
            bCIP_Required_Flag := FALSE;
            iState := 90; (* Advance to Neutralization Flush *)
        END_IF;

        IF bEmergencyStop THEN
            iState := 99;
        END_IF;

    90: (* STATE 90: MEMBRANE_FLUSH_DISCHARGE (10 Minutes Neutralization Rinse) *)
        sTrainStateDescription := 'MEMBRANE_FLUSH_DISCHARGE';
        iTrainCurrentState := 90;

        (* High-flow flush discharging residual cleaning chemicals to wastewater plant headworks *)
        bPermeatePumpForward_Run := TRUE;
        bPermeatePumpReverse_Run := FALSE;
        rPermeatePumpSpeed_Pct := 80.0;
        bPermeateIsolateValve_Cmd := FALSE;
        bPermeateToWasteValve_Cmd := TRUE;

        rAirScourBlowerSpeed_Pct := 85.0;
        bAirScourHeaderValve_Cmd := TRUE;
        bAirScourContinuous_Cmd := TRUE;

        tTimer_MembraneFlushDischarge(IN := TRUE, PT := T#600S);

        IF tTimer_MembraneFlushDischarge.Q THEN
            tTimer_MembraneFlushDischarge(IN := FALSE, PT := T#600S);
            bPermeateToWasteValve_Cmd := FALSE;
            bPermeatePumpForward_Run := FALSE;
            rFiltrationCycleTime_Elapsed_s := 0.0;
            iState := 0; (* Reset to Standby Idle, ready for production *)
        END_IF;

        IF bEmergencyStop THEN
            iState := 99;
        END_IF;

    99: (* STATE 99: CRITICAL_FOULING_TRIP_LOCKOUT *)
        sTrainStateDescription := 'CRITICAL_FOULING_TRIP_LOCKOUT';
        iTrainCurrentState := 99;

        (* Immediate fail-safe isolation *)
        rPermeatePumpSpeed_Pct := 0.0;
        bPermeatePumpForward_Run := FALSE;
        bPermeatePumpReverse_Run := FALSE;
        rAirScourBlowerSpeed_Pct := 0.0;
        bAirScourCyclicSolenoid_Cmd := FALSE;
        bAirScourContinuous_Cmd := FALSE;
        bAirScourHeaderValve_Cmd := FALSE;
        bNaOCl_DosingPump_Cmd := FALSE;
        bCitricAcid_DosingPump_Cmd := FALSE;
        bPermeateIsolateValve_Cmd := FALSE;
        bPermeateToWasteValve_Cmd := TRUE; (* Relieve header pressure to drain *)
        bCIP_DrainValve_Cmd := FALSE;

        (* Manual reset condition: E-Stop cleared, fault acknowledged, TMP recovered *)
        IF NOT bEmergencyStop AND bAcknowledgeFault AND NOT bAlarm_TMP_HH_Active AND
           NOT bAlarm_Turb_HH_Active AND NOT bTMP_CriticalFailure_All THEN
            bFiberIntegrityFault := FALSE;
            iState := 0; (* Return to Standby Idle *)
        END_IF;

END_CASE;
""")

    # PHASE 5: ISA-18.2 ALARMS & DIAGNOSTIC WORD BITFIELD PACKING
    parts.append("""
(* === PHASE 5: ISA-18.2 ALARMS & DIAGNOSTIC WORD BITFIELD PACKING === *)
(* Multi-tiered hysteresis ladder: Priority 1 (Trip) and Priority 2 (Critical) packed *)
(* into wISA_AlarmWord_High; Priority 3 (Warning) and Priority 4 (Advisory) packed     *)
(* into wISA_AlarmWord_Low. DWORD diagnostic word tracking TMR sensor degradation.     *)

(* 5.1 Transmembrane Pressure (TMP) Alarms with Deadband Hysteresis *)
(* HH Trip: 450 mbar *)
IF rVoted_TMP_mbar >= rConst_TMP_Trip_HH_mbar THEN
    bAlarm_TMP_HH_Active := TRUE;
    bCIP_Required_Flag := TRUE;
ELSIF rVoted_TMP_mbar <= (rConst_TMP_Trip_HH_mbar - rConst_TMP_Deadband_mbar) THEN
    IF bAcknowledgeFault THEN
        bAlarm_TMP_HH_Active := FALSE;
    END_IF;
END_IF;

(* H Warning: 350 mbar *)
IF rVoted_TMP_mbar >= rConst_TMP_Warn_H_mbar THEN
    bAlarm_TMP_H_Active := TRUE;
ELSIF rVoted_TMP_mbar <= (rConst_TMP_Warn_H_mbar - rConst_TMP_Deadband_mbar) THEN
    bAlarm_TMP_H_Active := FALSE;
END_IF;

(* L Advisory: 10 mbar *)
IF (rVoted_TMP_mbar <= rConst_TMP_Low_L_mbar) AND (iState = 20) AND (rFiltrationCycleTime_Elapsed_s > 30.0) THEN
    bAlarm_TMP_L_Active := TRUE;
ELSIF rVoted_TMP_mbar >= (rConst_TMP_Low_L_mbar + rConst_TMP_Deadband_mbar) THEN
    bAlarm_TMP_L_Active := FALSE;
END_IF;

(* LL Trip: -50 mbar (Vacuum reversal) *)
IF rVoted_TMP_mbar <= rConst_TMP_Trip_LL_mbar THEN
    bAlarm_TMP_LL_Active := TRUE;
ELSIF rVoted_TMP_mbar >= (rConst_TMP_Trip_LL_mbar + rConst_TMP_Deadband_mbar) THEN
    IF bAcknowledgeFault THEN
        bAlarm_TMP_LL_Active := FALSE;
    END_IF;
END_IF;

(* 5.2 Permeate Turbidity Alarms with Deadband Hysteresis *)
(* HH Trip: 0.250 NTU (Fiber rupture) *)
IF rVoted_Turbidity_NTU >= rConst_Turb_Trip_HH_NTU THEN
    bAlarm_Turb_HH_Active := TRUE;
    bFiberIntegrityFault := TRUE;
ELSIF rVoted_Turbidity_NTU <= (rConst_Turb_Trip_HH_NTU - rConst_Turb_Deadband_NTU) THEN
    IF bAcknowledgeFault THEN
        bAlarm_Turb_HH_Active := FALSE;
    END_IF;
END_IF;

(* H Warning: 0.150 NTU *)
IF rVoted_Turbidity_NTU >= rConst_Turb_Warn_H_NTU THEN
    bAlarm_Turb_H_Active := TRUE;
ELSIF rVoted_Turbidity_NTU <= (rConst_Turb_Warn_H_NTU - rConst_Turb_Deadband_NTU) THEN
    bAlarm_Turb_H_Active := FALSE;
END_IF;

(* 5.3 Aerobic Basin Dissolved Oxygen (DO) Alarms with Deadband Hysteresis *)
(* LL Trip: 0.80 mg/L (Nitrification failure hazard) *)
IF rVoted_DO_mgL <= rConst_DO_Trip_LL_mgL THEN
    bAlarm_DO_LL_Active := TRUE;
ELSIF rVoted_DO_mgL >= (rConst_DO_Trip_LL_mgL + rConst_DO_Deadband_mgL) THEN
    bAlarm_DO_LL_Active := FALSE;
END_IF;

(* L Warning: 1.20 mg/L *)
IF rVoted_DO_mgL <= rConst_DO_Warn_L_mgL THEN
    bAlarm_DO_L_Active := TRUE;
ELSIF rVoted_DO_mgL >= (rConst_DO_Warn_L_mgL + rConst_DO_Deadband_mgL) THEN
    bAlarm_DO_L_Active := FALSE;
END_IF;

(* H Warning: 3.00 mg/L (Aeration energy waste) *)
IF rVoted_DO_mgL >= rConst_DO_Warn_H_mgL THEN
    bAlarm_DO_H_Active := TRUE;
ELSIF rVoted_DO_mgL <= (rConst_DO_Warn_H_mgL - rConst_DO_Deadband_mgL) THEN
    bAlarm_DO_H_Active := FALSE;
END_IF;

(* HH Trip: 4.50 mg/L (Over-aeration floc shearing) *)
IF rVoted_DO_mgL >= rConst_DO_Trip_HH_mgL THEN
    bAlarm_DO_HH_Active := TRUE;
ELSIF rVoted_DO_mgL <= (rConst_DO_Trip_HH_mgL - rConst_DO_Deadband_mgL) THEN
    bAlarm_DO_HH_Active := FALSE;
END_IF;

(* 5.4 Membrane Basin Hydrostatic Level Alarms with Deadband Hysteresis *)
(* LL Trip: 2.20 m (Exposed hollow fibers) *)
IF rFeedBasinLevel_m <= rConst_Level_Trip_LL_m THEN
    bAlarm_Level_LL_Active := TRUE;
ELSIF rFeedBasinLevel_m >= (rConst_Level_Trip_LL_m + rConst_Level_Deadband_m) THEN
    IF bAcknowledgeFault THEN
        bAlarm_Level_LL_Active := FALSE;
    END_IF;
END_IF;

(* L Warning: 2.80 m *)
IF rFeedBasinLevel_m <= rConst_Level_Warn_L_m THEN
    bAlarm_Level_L_Active := TRUE;
ELSIF rFeedBasinLevel_m >= (rConst_Level_Warn_L_m + rConst_Level_Deadband_m) THEN
    bAlarm_Level_L_Active := FALSE;
END_IF;

(* H Warning: 3.80 m *)
IF rFeedBasinLevel_m >= rConst_Level_Warn_H_m THEN
    bAlarm_Level_H_Active := TRUE;
ELSIF rFeedBasinLevel_m <= (rConst_Level_Warn_H_m - rConst_Level_Deadband_m) THEN
    bAlarm_Level_H_Active := FALSE;
END_IF;

(* HH Trip: 4.20 m (Basin overflow hazard) *)
IF rFeedBasinLevel_m >= rConst_Level_Trip_HH_m THEN
    bAlarm_Level_HH_Active := TRUE;
ELSIF rFeedBasinLevel_m <= (rConst_Level_Trip_HH_m - rConst_Level_Deadband_m) THEN
    IF bAcknowledgeFault THEN
        bAlarm_Level_HH_Active := FALSE;
    END_IF;
END_IF;

(* 5.5 Bitfield Packing into ISA-18.2 Standard Words *)
wISA_AlarmWord_High := 16#0000;
IF bEmergencyStop THEN          wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0001; END_IF;
IF bAlarm_TMP_HH_Active THEN    wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0002; END_IF;
IF bAlarm_TMP_LL_Active THEN    wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0004; END_IF;
IF bAlarm_Turb_HH_Active THEN   wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0008; END_IF;
IF bAlarm_DO_LL_Active THEN     wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0010; END_IF;
IF bAlarm_DO_HH_Active THEN     wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0020; END_IF;
IF bAlarm_Level_LL_Active THEN  wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0040; END_IF;
IF bAlarm_Level_HH_Active THEN  wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0080; END_IF;
IF bTMP_CriticalFailure_All THEN wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0100; END_IF;
IF bFiberIntegrityFault THEN    wISA_AlarmWord_High := wISA_AlarmWord_High OR 16#0200; END_IF;

wISA_AlarmWord_Low := 16#0000;
IF bAlarm_TMP_H_Active THEN     wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0001; END_IF;
IF bAlarm_TMP_L_Active THEN     wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0002; END_IF;
IF bAlarm_Turb_H_Active THEN    wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0004; END_IF;
IF bAlarm_DO_L_Active THEN      wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0008; END_IF;
IF bAlarm_DO_H_Active THEN      wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0010; END_IF;
IF bAlarm_Level_L_Active THEN   wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0020; END_IF;
IF bAlarm_Level_H_Active THEN   wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0040; END_IF;
IF bTMP_Degraded_1oo2 THEN      wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0080; END_IF;
IF bDO_Degraded_1oo2 THEN       wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0100; END_IF;
IF bTurb_Degraded_1oo2 THEN     wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0200; END_IF;
IF bCIP_Required_Flag THEN      wISA_AlarmWord_Low := wISA_AlarmWord_Low OR 16#0400; END_IF;

(* 5.6 Diagnostic Word (DWORD) Sensor Health & Degradation Status *)
dwDiagnosticWord := 16#0000_0000;
IF bTMP_Ch1_Fault THEN          dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0001; END_IF;
IF bTMP_Ch2_Fault THEN          dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0002; END_IF;
IF bTMP_Ch3_Fault THEN          dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0004; END_IF;
IF bDO_Ch1_Fault THEN           dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0010; END_IF;
IF bDO_Ch2_Fault THEN           dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0020; END_IF;
IF bDO_Ch3_Fault THEN           dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0040; END_IF;
IF bTurb_Ch1_Fault THEN         dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0100; END_IF;
IF bTurb_Ch2_Fault THEN         dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0200; END_IF;
IF bTurb_Ch3_Fault THEN         dwDiagnosticWord := dwDiagnosticWord OR 16#0000_0400; END_IF;
IF bTMP_Degraded_1oo2 THEN      dwDiagnosticWord := dwDiagnosticWord OR 16#0001_0000; END_IF;
IF bDO_Degraded_1oo2 THEN       dwDiagnosticWord := dwDiagnosticWord OR 16#0002_0000; END_IF;
IF bTurb_Degraded_1oo2 THEN     dwDiagnosticWord := dwDiagnosticWord OR 16#0004_0000; END_IF;
IF (iState = 20) THEN           dwDiagnosticWord := dwDiagnosticWord OR 16#0100_0000; END_IF;
IF (iState = 40) THEN           dwDiagnosticWord := dwDiagnosticWord OR 16#0200_0000; END_IF;
IF (iState = 70) THEN           dwDiagnosticWord := dwDiagnosticWord OR 16#0400_0000; END_IF;
IF (iState = 99) THEN           dwDiagnosticWord := dwDiagnosticWord OR 16#8000_0000; END_IF;

(* 5.7 Master Health Summary Flag *)
bTrainHealthy := (wISA_AlarmWord_High = 16#0000) AND NOT bEmergencyStop AND NOT bFiberIntegrityFault;

END_FUNCTION_BLOCK
```""")

    return "".join(parts)

if __name__ == "__main__":
    code = build_iec_code()
    print("Generated IEC ST length:", len(code), "characters")
