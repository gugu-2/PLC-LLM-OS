import os
import sys
import json
import re

def generate_iec_st():
    parts = []
    
    # Header block
    parts.append("""FUNCTION_BLOCK FB_FoodBev_CIP_SIP_MultiLoopSanitization_Skid
(*
====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - SYNTHETIC IEC 61131-3 DATASET ENGINE
  SYSTEM DESIGNATION: CPS-FOODBEV-CIP-SIP-MULTILOOP-SKID-V7
  DOMAIN ASSIGNMENT: Food & Beverage Processing: Multi-Loop Continuous Caustic & Acid Clean-In-Place
                     / Steam-In-Place (CIP/SIP) Skid with Dual Conductivity & F0 Lethality Integration
  STANDARDS COMPLIANCE:
    - IEC 61131-3 3rd Edition (Deterministic Industrial Automation Structured Text)
    - 3-A Sanitary Standards (ANSI/3-A 00-01, 605-04 for CIP Processing Systems)
    - EHEDG (European Hygienic Engineering & Design Group) Guidelines Doc 2, 8, 13 (CIP / SIP Design)
    - ASME BPE-2022 (Bioprocessing Equipment - Pure Steam Sterilization & Bioburden Thermal Inactivation)
    - FDA 21 CFR Part 117 (Current Good Manufacturing Practice for Human Food)
    - FDA 21 CFR Part 211 (CGMP for Finished Pharmaceuticals - Validation of Cleaning & Sterilization)
    - European Pharmacopoeia (Ph. Eur.) & USP <1229> (Sterilization of Equipment by Steam Under Pressure)
    - ISA-88.01 (Batch Control Part 1: Models & Terminology - Recipe Procedural Entity Execution)
    - ISA-18.2 / EEMUA 191 (Management of Alarm Systems for the Process Industries)
    - IEC 61508 / IEC 61511 (Functional Safety SIL-2 Safety Instrumented Functions)
  PERSONA:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Industrial Systems Tenure)
====================================================================================================
  MATHEMATICAL & CYBER-PHYSICAL PROCESS SPECIFICATION:

  1. CLEAN-IN-PLACE (CIP) CLEANING DYNAMICS & THE FOUR SINNER FACTORS:
     CIP sanitization efficacy is governed by the classic Sinner Circle interactions:
       Efficacy = f( Chemical Action, Thermal Action, Mechanical Wall Shear, Contact Dwell Time )
     a) Chemical Saponification & Solubilization:
        - Caustic Wash (Sodium Hydroxide NaOH, 2.0% - 3.0% w/w):
          Hydrolyzes fatty acids (triglycerides + 3 NaOH -> glycerol + 3 fatty acid sodium salts)
          and cleaves peptide bonds in denatured protein biofilms via nucleophilic hydroxyl attack.
        - Acid Wash (Nitric Acid HNO3 / Phosphoric Acid H3PO4, 1.0% - 1.5% w/w):
          Dissolves insoluble alkaline earth salts (milkstone calcium phosphate Ca3(PO4)2 and beerstone
          calcium oxalate CaC2O4) via acidic dissolution:
            Ca3(PO4)2 + 4 H+ -> 3 Ca2+ + 2 H2PO4-
          Passivates electropolished 316L stainless steel surfaces, restoring the chromium oxide Cr2O3 passive film.
     b) Thermal Reaction Rate Acceleration (Arrhenius Kinetics):
        Reaction kinetics follow the Arrhenius relationship:
          k_clean(T) = A_arr * exp( -E_act / (R_gas * (T + 273.15)) )
        where E_act = 42.5 kJ/mol for organic soil dissolution. Elevating temperature from 20 deg C to 85 deg C
        multiplies dissolution reaction rates by approximately 18.4x.
     c) Mechanical Boundary Wall Shear Stress (Turbulent Pipe Hydraulics):
        To dislodge sticky protein matrix biofilms, turbulent hydrodynamic scrubbing is mandatory.
        Fluid flow Reynolds number through sanitary tubing (internal diameter D_pipe = 0.0721 m):
          Re = (rho_fluid * v_mean * D_pipe) / mu_fluid
        For complete turbulent scouring, operating velocity v_mean >= 1.8 to 2.2 m/s, yielding Re >= 200,000.
        Darcy friction factor f_darcy via the Swamee-Jain explicit Colebrook-White approximation:
          f_darcy = 0.25 / [ log10( (epsilon_rough / (3.7 * D_pipe)) + (5.74 / (Re^0.9)) ) ]^2
        where sanitary tubing electropolished surface roughness epsilon_rough = 0.51 um (Ra = 20 u-inch).
        Pipe wall shear stress:
          tau_wall = 0.125 * f_darcy * rho_fluid * (v_mean^2)
        The skid closed-loop control guarantees tau_wall >= 1.50 Pa across all circuit branches.

  2. TOROIDAL INDUCTIVE CONDUCTIVITY TEMPERATURE COMPENSATION & CONCENTRATION:
     Toroidal inductive conductivity sensors (electrodeless) induce an alternating magnetic field inside
     the fluid bore, measuring specific conductance Kappa_meas [mS/cm].
     Because electrolytic conductivity exhibits a high positive temperature coefficient (~1.8% to 2.3%/deg C),
     raw conductivity must be normalized to standard reference temperature T_ref = 25.0 deg C:
       Kappa_25 = Kappa_meas / [ 1.0 + alpha_chem * (T_meas - 25.0) ]
     where:
       alpha_caustic = 0.0210 per deg C (2.10%/deg C for NaOH electrolytes)
       alpha_acid    = 0.0165 per deg C (1.65%/deg C for HNO3/H3PO4 electrolytes)
       alpha_water   = 0.0220 per deg C (2.20%/deg C for purified rinse water)
     Concentration is computed from compensated conductivity Kappa_25 via calibrated quadratic polynomials:
       C_NaOH [% w/w] = a0 + a1 * Kappa_25 + a2 * (Kappa_25^2)
         (a0 = 0.0120, a1 = 0.0385, a2 = 0.000142 mS^-1*cm)
       C_HNO3 [% w/w] = b0 + b1 * Kappa_25 + b2 * (Kappa_25^2)
         (b0 = 0.0080, b1 = 0.0224, b2 = 0.000088 mS^-1*cm)

  3. STEAM-IN-PLACE (SIP) THERMAL STERILIZATION & LOGARITHMIC F0 LETHALITY INTEGRATION:
     SIP sterilization operates by driving high-purity saturated steam through all piping, valves, and vessels.
     Bacterial endospore thermal destruction kinetics (reference microorganism: Geobacillus stearothermophilus)
     follow the Bigelow log-linear thermal death model:
       d(log10(N)) / dt = -1.0 / D_T
     where D_T is the decimal reduction time at temperature T:
       D_T = D_121.1 * 10^( (121.11 - T) / z )
     Standard reference parameters:
       T_ref_sip = 121.11 deg C (250.0 deg F)
       z_value   = 10.00 deg C
       D_121.1   = 1.50 minutes (for 12-log reduction, minimum F0 = 12 * 1.50 = 18.0 min; design target = 30.0 min).
     The instantaneous lethal rate L(T) is given by:
       L(T) = 10^( (T(t) - 121.11) / 10.0 )
     Accumulated sterilization equivalent lethality F0 [minutes]:
       F0 = Integral_{0}^{t_sip} L(T(tau)) dtau = Integral_{0}^{t_sip} 10^( (T(tau) - 121.11) / 10.0 ) dtau
     Numerical integration in this block uses the trapezoidal quadrature rule:
       Delta_F0[k] = 0.5 * ( L(T[k]) + L(T[k-1]) ) * (Ts / 60.0)
       F0[k] = F0[k-1] + Delta_F0[k]
     Sterilization is governed by the worst-case Cold-Spot sensor:
       F0_voted = min( F0_ColdSpot_A, F0_ColdSpot_B, F0_ColdSpot_C )
     Furthermore, saturated steam quality is verified against the Antoine vapor pressure formulation:
       P_sat_calc [bar abs] = exp( 11.6834 - (3816.44 / (T_meas + 227.02)) )
     A deviation |P_meas - P_sat_calc| > 0.35 bar flags non-condensable air pocket binding or superheat anomaly.

  4. DISCRETE STATE-SPACE MODEL (10x10 SYSTEM: x[k+1] = A*x[k] + B*u[k]):
     State Vector x (10 states):
       x[1]:  Shell-and-tube product delivery temperature T_sup [deg C]
       x[2]:  Shell steam condensing temperature T_stm [deg C]
       x[3]:  Return line scavenge header fluid temperature T_ret [deg C]
       x[4]:  Supply delivery in-line conductivity Kappa_sup [mS/cm]
       x[5]:  Return scavenge in-line conductivity Kappa_ret [mS/cm]
       x[6]:  Active buffer tank chemical concentration C_tank [%]
       x[7]:  Forward delivery volumetric flow rate Q_sup [m3/h]
       x[8]:  Return scavenge pump volumetric flow rate Q_ret [m3/h]
       x[9]:  Active buffer tank hydrostatic fluid level H_tank [m]
       x[10]: Critical piping cold-spot drain temperature T_cold [deg C]
     Control Input Vector u (8 inputs):
       u[1]: Shell-and-tube sanitary steam modulating valve command X_stm [%]
       u[2]: Main CIP forward delivery centrifugal pump speed N_sup [%]
       u[3]: Self-priming liquid-ring return scavenging pump speed N_ret [%]
       u[4]: Concentrated Caustic (50% NaOH) progressive cavity dosing pump speed N_dose_caustic [%]
       u[5]: Concentrated Acid (60% HNO3) progressive cavity dosing pump speed N_dose_acid [%]
       u[6]: Fresh deionized water (WFI/RO) make-up inlet valve position X_wfi [%]
       u[7]: Return diversion 3-way routing valve position X_divert [%] (0=Drain, 50=Recovery, 100=Recirc)
       u[8]: Pure steam SIP barrier injection control valve position X_sip_stm [%]

  5. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION:
     Solves an unrolled receding-horizon quadratic optimization with input rate and amplitude constraints:
       min_u J = 0.5 * sum_{i=1..10} Q[i] * (x[i] - x_ref[i])^2
               + 0.5 * sum_{j=1..8} R[j] * (u[j])^2
               + 0.5 * sum_{j=1..8} Rd[j] * (u[j] - u_prev[j])^2
               + 0.5 * sum_{i=1..10} P[i] * (x_next[i] - x_ref[i])^2
     Optimization uses iterative projected gradient descent with Armijo-style adaptive learning rate
     and physical actuator slew rate limiting. Prevents scavenging return pump cavitation by enforcing
     net positive suction head available (NPSHa) constraint margins.

  6. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE:
     Triplicated sensor arrays for mission-critical instruments:
       a) Supply Toroidal Conductivity Transmitters (A, B, C)
       b) Return Toroidal Conductivity Transmitters (A, B, C)
       c) Supply Sanitary Magnetic Flowmeters (A, B, C)
       d) Return Sanitary Magnetic Flowmeters (A, B, C)
       e) Critical Cold-Spot PT100 RTD Temperature Probes (A, B, C)
     Voting algorithm executes middle-value selection (median) when all 3 channels are healthy,
     degrades to average of 2 healthy channels upon single-channel discrepancy timeout (tau_discrep = 2.0 s),
     and initiates fail-safe hold / alarm latching upon dual-channel failure.
====================================================================================================
*)
""")

    # VAR_INPUT
    parts.append("""VAR_INPUT
    (* ========================================================================================= *)
    (* 1. SYSTEM CONTROL, PERMISSIVES & OPERATOR RECIPE COMMANDS                                 *)
    (* ========================================================================================= *)
    bMasterEnable                   : BOOL;         (* Master skid automation control permissive [active HIGH] *)
    bEmergencyStop                  : BOOL;         (* Hardwired SIL-3 emergency stop circuit healthy [active HIGH] *)
    bStartCIPCycleCmd               : BOOL;         (* Operator push button / SCADA request to initiate CIP/SIP sequence *)
    bAbortCycleCmd                  : BOOL;         (* Operator emergency sequence abort and safe drain flush command *)
    bAcknowledgeAlarms              : BOOL;         (* ISA-18.2 master alarm acknowledge push button *)
    bSanitaryPipingInterlockClosed  : BOOL;         (* Flow divert plate swing elbow proximity switches made *)
    bCausticTankSupplyPermissive    : BOOL;         (* NaOH bulk storage tank level and suction permissive OK *)
    bAcidTankSupplyPermissive       : BOOL;         (* HNO3 bulk storage tank level and suction permissive OK *)
    bPureSteamSupplyPermissive      : BOOL;         (* High-purity clean steam utility pressure available >= 3.0 bar *)
    bSterileAirSupplyPermissive     : BOOL;         (* Sterile overpressure barrier air utility available >= 4.0 bar *)

    (* ========================================================================================= *)
    (* 2. TRIPLE MODULAR REDUNDANT (2oo3 TMR) PRIMARY PROCESS TELEMETRY                          *)
    (* ========================================================================================= *)
    (* Sanitary Toroidal Inductive Conductivity Transmitters - Supply Line [mS/cm] *)
    rSupplyConductivity_ChA         : REAL;         (* Supply line toroidal conductivity Channel A [mS/cm] *)
    rSupplyConductivity_ChB         : REAL;         (* Supply line toroidal conductivity Channel B [mS/cm] *)
    rSupplyConductivity_ChC         : REAL;         (* Supply line toroidal conductivity Channel C [mS/cm] *)

    (* Sanitary Toroidal Inductive Conductivity Transmitters - Return Scavenge Line [mS/cm] *)
    rReturnConductivity_ChA         : REAL;         (* Return line toroidal conductivity Channel A [mS/cm] *)
    rReturnConductivity_ChB         : REAL;         (* Return line toroidal conductivity Channel B [mS/cm] *)
    rReturnConductivity_ChC         : REAL;         (* Return line toroidal conductivity Channel C [mS/cm] *)

    (* Sanitary Electromagnetic Flowmeters - Supply Forward Delivery [m3/h] *)
    rSupplyFlowRate_ChA             : REAL;         (* Forward delivery magmeter Channel A [m3/h] *)
    rSupplyFlowRate_ChB             : REAL;         (* Forward delivery magmeter Channel B [m3/h] *)
    rSupplyFlowRate_ChC             : REAL;         (* Forward delivery magmeter Channel C [m3/h] *)

    (* Sanitary Electromagnetic Flowmeters - Scavenge Return Line [m3/h] *)
    rReturnFlowRate_ChA             : REAL;         (* Scavenge return magmeter Channel A [m3/h] *)
    rReturnFlowRate_ChB             : REAL;         (* Scavenge return magmeter Channel B [m3/h] *)
    rReturnFlowRate_ChC             : REAL;         (* Scavenge return magmeter Channel C [m3/h] *)

    (* Sanitary 4-Wire PT100 RTDs - Critical Low-Point Cold-Spot SIP Drain [deg C] *)
    rColdSpotTemp_ChA               : REAL;         (* Low-point sanitary diaphragm RTD Channel A [deg C] *)
    rColdSpotTemp_ChB               : REAL;         (* Low-point sanitary diaphragm RTD Channel B [deg C] *)
    rColdSpotTemp_ChC               : REAL;         (* Low-point sanitary diaphragm RTD Channel C [deg C] *)

    (* ========================================================================================= *)
    (* 3. AUXILIARY THERMODYNAMIC, HYDRAULIC & ANALYTICAL TELEMETRY                              *)
    (* ========================================================================================= *)
    rSupplyHeaderTemp               : REAL;         (* Shell-and-tube heat exchanger outlet delivery fluid temp [deg C] *)
    rReturnHeaderTemp               : REAL;         (* Return manifold scavenge fluid temperature [deg C] *)
    rSteamSupplyPressure            : REAL;         (* Plant utility clean steam supply header pressure [bar] *)
    rSteamCondensateTemp            : REAL;         (* Heat exchanger condensate pot drainage temperature [deg C] *)
    rSupplyPressure                 : REAL;         (* Forward delivery centrifugal pump discharge pressure [bar] *)
    rReturnSuctionPressure          : REAL;         (* Scavenge return pump suction line pressure [bar] *)
    rActiveTankLevel                : REAL;         (* Active wash/rinse buffer tank hydrostatic fluid level [m] *)
    rTurbidityReturn                : REAL;         (* Optical backscatter return rinse water turbidity [NTU] *)

    (* ========================================================================================= *)
    (* 4. BATCH RECIPE RECEDING-HORIZON SETPOINTS                                                *)
    (* ========================================================================================= *)
    rSelectedCausticTargetPct       : REAL;         (* Recipe target NaOH concentration setpoint [%] (nominal 2.50%) *)
    rSelectedAcidTargetPct          : REAL;         (* Recipe target HNO3 concentration setpoint [%] (nominal 1.20%) *)
    rTargetF0LethalityMin           : REAL;         (* Recipe target sterilization accumulated lethality [min] (30.0 min) *)
    rTargetWashFlowRate             : REAL;         (* Recipe target delivery flow rate for turbulent scouring [m3/h] *)
    rTargetCausticTemp              : REAL;         (* Recipe target caustic washing temperature [deg C] (nominal 85.0 C) *)
    rTargetAcidTemp                 : REAL;         (* Recipe target acid descaling temperature [deg C] (nominal 65.0 C) *)
    rTargetSIPTemp                  : REAL;         (* Recipe target pure steam holding temperature [deg C] (nominal 122.5 C) *)
END_VAR
""")

    # VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. PROCESS ACTUATOR MODULATION & SAFETY SOLENOID COMMANDS                                 *)
    (* ========================================================================================= *)
    rSteamModulatingValveCmd        : REAL;         (* Proportional sanitary steam valve analog position [%] *)
    rSupplyPumpSpeedCmd             : REAL;         (* CIP main forward delivery centrifugal pump VFD speed [%] *)
    rReturnScavengePumpSpeedCmd     : REAL;         (* Self-priming liquid-ring return pump VFD speed [%] *)
    rCausticDosingPumpSpeedCmd      : REAL;         (* 50% NaOH progressive cavity dosing pump speed [%] *)
    rAcidDosingPumpSpeedCmd         : REAL;         (* 60% HNO3 progressive cavity dosing pump speed [%] *)
    rWfiInletValveCmd               : REAL;         (* Deionized WFI make-up proportional control valve [%] *)
    rReturnDivertValveCmd           : REAL;         (* 3-way sanitary return routing valve [%] (0=Drain, 50=Recov, 100=Recirc) *)
    rPureSteamSIPValveCmd           : REAL;         (* Direct pure steam injection sanitary modulating valve [%] *)
    rSterileAirCoolingValveCmd      : REAL;         (* Sterile overpressure barrier air injection valve [%] *)
    bSupplyPumpRunContactor         : BOOL;         (* Forward centrifugal pump VFD run command enable *)
    bReturnPumpRunContactor         : BOOL;         (* Return scavenging pump VFD run command enable *)
    bCausticDosingPumpRun           : BOOL;         (* Caustic metering pump motor run enable contactor *)
    bAcidDosingPumpRun              : BOOL;         (* Acid metering pump motor run enable contactor *)
    bDrainDumpValveOpen             : BOOL;         (* Fast-acting pneumatic drain dump sanitary valve *)
    bCausticRecoveryValveOpen       : BOOL;         (* Sanitary valve directing reclaimed wash to Caustic Tank *)
    bAcidRecoveryValveOpen          : BOOL;         (* Sanitary valve directing reclaimed wash to Acid Tank *)
    bSteamTrapBlowdownValve         : BOOL;         (* Sanitary thermodynamic steam trap bypass blowdown valve *)
    bSterileBarrierAirSealValve     : BOOL;         (* Positive pressure sterile air barrier block valve *)
    bAudibleVisualAlarmStrobe       : BOOL;         (* Industrial horn and multi-color beacon alarm output *)

    (* ========================================================================================= *)
    (* 2. CONSOLIDATED 2oo3 TMR ESTIMATES & CYBER-PHYSICAL STATE ESTIMATES                       *)
    (* ========================================================================================= *)
    rVotedSupplyConductivity        : REAL;         (* 2oo3 TMR consolidated supply conductivity [mS/cm] *)
    rVotedReturnConductivity        : REAL;         (* 2oo3 TMR consolidated return conductivity [mS/cm] *)
    rVotedSupplyFlow                : REAL;         (* 2oo3 TMR consolidated supply volumetric flow [m3/h] *)
    rVotedReturnFlow                : REAL;         (* 2oo3 TMR consolidated return volumetric flow [m3/h] *)
    rVotedColdSpotTemp              : REAL;         (* 2oo3 TMR consolidated cold-spot RTD temperature [deg C] *)
    rCompensatedSupplyCond25        : REAL;         (* Normalized supply conductivity compensated to 25 deg C [mS/cm] *)
    rCompensatedReturnCond25        : REAL;         (* Normalized return conductivity compensated to 25 deg C [mS/cm] *)
    rCalculatedCausticPct           : REAL;         (* Dynamic real-time calculated NaOH concentration [%] *)
    rCalculatedAcidPct              : REAL;         (* Dynamic real-time calculated HNO3 concentration [%] *)
    rReynoldsNumberSupply           : REAL;         (* Calculated turbulent flow Reynolds number Re [-] *)
    rWallShearStressPa              : REAL;         (* Sanitary piping boundary wall shear stress [Pa] *)
    rAccumulatedF0Lethality         : REAL;         (* Real-time integrated logarithmic sterilization lethality [min] *)
    rInstantaneousLethalRate        : REAL;         (* Current lethal rate L(T) = 10^((T-121.1)/10) [min/min] *)
    rCycleElapsedTimeSec            : REAL;         (* Cumulative active recipe phase elapsed time [s] *)
    rPhaseRemainingTimeSec          : REAL;         (* Estimated remaining dwell time in current CIP/SIP step [s] *)

    (* ========================================================================================= *)
    (* 3. ISA-88 RECIPE STATUS & ISA-18.2 MULTI-TIER ALARM REGISTERS                             *)
    (* ========================================================================================= *)
    wSkidOperationalState           : WORD;         (* System high-level supervisory state word *)
    wFSM_CurrentPhase               : WORD;         (* Active 12-stage CIP/SIP phase identification number *)
    dwAlarmWord_Trips               : DWORD;        (* ISA-18.2 Priority 1 Bit-packed Critical Emergency Trips *)
    dwAlarmWord_Severe              : DWORD;        (* ISA-18.2 Priority 2 Bit-packed Process Deviation Alarms *)
    dwAlarmWord_Warning             : DWORD;        (* ISA-18.2 Priority 3 Bit-packed Advisory & Discrepancy Warnings *)
    wTMR_DiscrepancyStatus          : WORD;         (* 2oo3 voting discrepancy and degradation status word *)
    bCIPCycleRunning                : BOOL;         (* Sequence actively in progress flag *)
    bCIPCycleCompleted              : BOOL;         (* Entire 12-stage recipe finished successfully pulse *)
    bSterilizationValidated         : BOOL;         (* SIP accumulated F0 >= target validated QA record flag *)
    bMasterFaultTrip                : BOOL;         (* Skid in latched trip condition requiring manual reset *)
END_VAR
""")

    # VAR block
    parts.append("""VAR
    (* ========================================================================================= *)
    (* 1. THERMODYNAMIC, CHEMICAL & GEOMETRIC SYSTEM CONSTANTS                                   *)
    (* ========================================================================================= *)
    rConst_ScanDeltaTime            : REAL := 0.100;        (* Periodic execution scan time Ts = 100 ms [s] *)
    rConst_PipeDiameterInner        : REAL := 0.0721;       (* Sanitary tubing internal bore diameter (3-inch OD) [m] *)
    rConst_PipeCrossSectionArea     : REAL := 0.0040828;    (* Cross-sectional area of process conduit [m^2] *)
    rConst_PipeSurfaceRoughness     : REAL := 0.00000051;   (* Surface roughness epsilon (Ra = 20 micro-inch electropolished) [m] *)
    rConst_WaterDensity             : REAL := 1000.0;       (* Pure water baseline density at 20 deg C [kg/m^3] *)
    rConst_CausticDensity           : REAL := 1028.0;       (* 2.5% NaOH solution operational density [kg/m^3] *)
    rConst_AcidDensity              : REAL := 1015.0;       (* 1.2% HNO3 solution operational density [kg/m^3] *)
    rConst_WaterDynamicViscosity    : REAL := 0.001002;     (* Water dynamic viscosity at 20 deg C [Pa*s] *)
    rConst_CausticViscosity         : REAL := 0.000850;     (* Caustic solution dynamic viscosity at 85 deg C [Pa*s] *)
    rConst_AcidViscosity            : REAL := 0.000720;     (* Acid solution dynamic viscosity at 65 deg C [Pa*s] *)
    rConst_TempCoeffCaustic         : REAL := 0.0210;       (* Linear temp compensation alpha for NaOH [1/deg C] *)
    rConst_TempCoeffAcid            : REAL := 0.0165;       (* Linear temp compensation alpha for HNO3 [1/deg C] *)
    rConst_TempCoeffWater           : REAL := 0.0220;       (* Linear temp compensation alpha for rinse water [1/deg C] *)
    rConst_CausticPoly_a0           : REAL := 0.0120;       (* NaOH polynomial intercept *)
    rConst_CausticPoly_a1           : REAL := 0.0385;       (* NaOH polynomial linear slope *)
    rConst_CausticPoly_a2           : REAL := 0.000142;     (* NaOH polynomial quadratic curvature *)
    rConst_AcidPoly_b0              : REAL := 0.0080;       (* HNO3 polynomial intercept *)
    rConst_AcidPoly_b1              : REAL := 0.0224;       (* HNO3 polynomial linear slope *)
    rConst_AcidPoly_b2              : REAL := 0.000088;     (* HNO3 polynomial quadratic curvature *)
    rConst_SIP_RefTemp              : REAL := 121.11;       (* Standard sterilization reference temperature T_ref [deg C] *)
    rConst_SIP_ZValue               : REAL := 10.00;        (* Inactivation thermal sensitivity z-value [deg C] *)
    rConst_SIP_DValueRef            : REAL := 1.50;         (* D-value at 121.11 C for G. stearothermophilus [min] *)
    rConst_MinTurbulentReynolds     : REAL := 200000.0;     (* Minimum Reynolds number for turbulent film scrubbing *)
    rConst_MinWallShearStress       : REAL := 1.50;         (* Minimum boundary wall shear stress for biofilm removal [Pa] *)
    rConst_TankBaseArea             : REAL := 1.7671;       (* Active wash buffer tank internal cross section area [m^2] *)

    (* ========================================================================================= *)
    (* 2. DISCRETE STATE-SPACE MATRICES (10x10 SYSTEM: x[k+1] = A*x[k] + B*u[k])                  *)
    (* States x[1..10]:                                                                          *)
    (*   x[1]:  T_sup  - Shell-and-tube product delivery temperature [deg C]                     *)
    (*   x[2]:  T_stm  - Shell condensing steam temperature [deg C]                              *)
    (*   x[3]:  T_ret  - Return line scavenge fluid temperature [deg C]                          *)
    (*   x[4]:  Kap_sup- Supply line in-line conductivity [mS/cm]                                *)
    (*   x[5]:  Kap_ret- Return line in-line conductivity [mS/cm]                                *)
    (*   x[6]:  C_tank - Active buffer tank chemical concentration [%]                           *)
    (*   x[7]:  Q_sup  - Forward delivery volumetric flow rate [m3/h]                            *)
    (*   x[8]:  Q_ret  - Return scavenge pump flow rate [m3/h]                                   *)
    (*   x[9]:  H_tank - Active buffer tank hydrostatic fluid level [m]                          *)
    (*   x[10]: T_cold - Low-point piping cold-spot drain temperature [deg C]                   *)
    (* Inputs u[1..8]:                                                                           *)
    (*   u[1]:  X_stm  - Steam modulating valve command [%]                                      *)
    (*   u[2]:  N_sup  - Supply pump speed [%]                                                   *)
    (*   u[3]:  N_ret  - Return scavenge pump speed [%]                                          *)
    (*   u[4]:  N_d_cst- Caustic dosing pump speed [%]                                           *)
    (*   u[5]:  N_d_acd- Acid dosing pump speed [%]                                              *)
    (*   u[6]:  X_wfi  - WFI make-up valve [%]                                                   *)
    (*   u[7]:  X_div  - Return divert valve [%] (0=Drain, 50=Recov, 100=Recirc)                 *)
    (*   u[8]:  X_sip  - Pure steam direct SIP valve [%]                                         *)
    (* ========================================================================================= *)
    arrA                            : ARRAY[1..10, 1..10] OF REAL; (* Discrete state transition matrix A *)
    arrB                            : ARRAY[1..10, 1..8] OF REAL;  (* Discrete input coupling matrix B *)
    arrC                            : ARRAY[1..10, 1..10] OF REAL; (* Measurement observation matrix C *)
    arrD                            : ARRAY[1..10, 1..8] OF REAL;  (* Direct feedthrough matrix D *)
    arrState_x                      : ARRAY[1..10] OF REAL;        (* Current state vector x[k] *)
    arrState_x_next                 : ARRAY[1..10] OF REAL;        (* Predicted state vector x[k+1] *)
    arrState_x_hat                  : ARRAY[1..10] OF REAL;        (* Filtered estimated state vector x_hat[k] *)
    arrStateRef                     : ARRAY[1..10] OF REAL;        (* Dynamic reference trajectory setpoints *)
    arrControl_u                    : ARRAY[1..8] OF REAL;         (* Active control input command vector u[k] *)
    arrControl_u_prev               : ARRAY[1..8] OF REAL;         (* Previous execution scan command vector u[k-1] *)
    arrMeasurement_z                : ARRAY[1..10] OF REAL;        (* Feedback measurement vector z[k] *)
    arrInnovation_e                 : ARRAY[1..10] OF REAL;        (* Kalman residual innovation vector e[k] *)

    (* ========================================================================================= *)
    (* 3. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZER                              *)
    (* ========================================================================================= *)
    arrQ_MpcCost                    : ARRAY[1..10] OF REAL;        (* State error quadratic penalty weights Q *)
    arrR_MpcCost                    : ARRAY[1..8] OF REAL;         (* Actuator effort quadratic penalty weights R *)
    arrRd_MpcRateCost               : ARRAY[1..8] OF REAL;         (* Actuator slew rate penalty weights Rd *)
    arrP_TerminalCost               : ARRAY[1..10] OF REAL;        (* Terminal state penalty weights P *)
    arrMpcGradient                  : ARRAY[1..8] OF REAL;         (* Objective function gradient nabla_J *)
    arrU_LowerBound                 : ARRAY[1..8] OF REAL;         (* Actuator lower saturation bounds *)
    arrU_UpperBound                 : ARRAY[1..8] OF REAL;         (* Actuator upper saturation bounds *)
    arrDeltaU_Max                   : ARRAY[1..8] OF REAL;         (* Maximum allowable actuator delta per scan *)
    rMpcLearningRate                : REAL := 0.042;               (* Gradient descent optimization step size *)
    nMpcIterations                  : INT := 10;                   (* Unrolled solver inner iteration limit *)
    rMpcObjectiveValue              : REAL := 0.0;                 (* Current scan evaluated scalar cost J *)

    (* ========================================================================================= *)
    (* 4. EXTENDED KALMAN FILTER (EKF) OBSERVER GAIN & COVARIANCE                                *)
    (* ========================================================================================= *)
    arrKalmanGain                   : ARRAY[1..10, 1..10] OF REAL; (* Steady-state observer Kalman gain matrix *)
    arrErrorCov_P                   : ARRAY[1..10, 1..10] OF REAL; (* State estimation error covariance matrix *)
    arrProcessNoise_Q               : ARRAY[1..10] OF REAL;        (* Process disturbance covariance diagonal *)
    arrSensorNoise_R                : ARRAY[1..10] OF REAL;        (* Sensor measurement noise covariance diagonal *)

    (* ========================================================================================= *)
    (* 5. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING CHANNELS & FAULT ACCUMULATORS              *)
    (* ========================================================================================= *)
    (* Supply Toroidal Conductivity Transmitters (A, B, C) *)
    rSupplyCond_TmrThreshold        : REAL := 4.50;                (* Maximum allowable deviation [mS/cm] *)
    bSupplyCond_ChA_Valid           : BOOL := TRUE;
    bSupplyCond_ChB_Valid           : BOOL := TRUE;
    bSupplyCond_ChC_Valid           : BOOL := TRUE;
    tSupplyCond_ChA_FaultTimer      : REAL := 0.0;
    tSupplyCond_ChB_FaultTimer      : REAL := 0.0;
    tSupplyCond_ChC_FaultTimer      : REAL := 0.0;

    (* Return Toroidal Conductivity Transmitters (A, B, C) *)
    rReturnCond_TmrThreshold        : REAL := 4.50;                (* Maximum allowable deviation [mS/cm] *)
    bReturnCond_ChA_Valid           : BOOL := TRUE;
    bReturnCond_ChB_Valid           : BOOL := TRUE;
    bReturnCond_ChC_Valid           : BOOL := TRUE;
    tReturnCond_ChA_FaultTimer      : REAL := 0.0;
    tReturnCond_ChB_FaultTimer      : REAL := 0.0;
    tReturnCond_ChC_FaultTimer      : REAL := 0.0;

    (* Supply Sanitary Flowmeters (A, B, C) *)
    rSupplyFlow_TmrThreshold        : REAL := 2.50;                (* Maximum allowable deviation [m3/h] *)
    bSupplyFlow_ChA_Valid           : BOOL := TRUE;
    bSupplyFlow_ChB_Valid           : BOOL := TRUE;
    bSupplyFlow_ChC_Valid           : BOOL := TRUE;
    tSupplyFlow_ChA_FaultTimer      : REAL := 0.0;
    tSupplyFlow_ChB_FaultTimer      : REAL := 0.0;
    tSupplyFlow_ChC_FaultTimer      : REAL := 0.0;

    (* Return Sanitary Flowmeters (A, B, C) *)
    rReturnFlow_TmrThreshold        : REAL := 2.50;                (* Maximum allowable deviation [m3/h] *)
    bReturnFlow_ChA_Valid           : BOOL := TRUE;
    bReturnFlow_ChB_Valid           : BOOL := TRUE;
    bReturnFlow_ChC_Valid           : BOOL := TRUE;
    tReturnFlow_ChA_FaultTimer      : REAL := 0.0;
    tReturnFlow_ChB_FaultTimer      : REAL := 0.0;
    tReturnFlow_ChC_FaultTimer      : REAL := 0.0;

    (* Critical Low-Point Cold-Spot Drain RTDs (A, B, C) *)
    rColdSpotTemp_TmrThreshold      : REAL := 1.80;                (* Maximum allowable deviation [deg C] *)
    bColdSpotTemp_ChA_Valid         : BOOL := TRUE;
    bColdSpotTemp_ChB_Valid         : BOOL := TRUE;
    bColdSpotTemp_ChC_Valid         : BOOL := TRUE;
    tColdSpotTemp_ChA_FaultTimer    : REAL := 0.0;
    tColdSpotTemp_ChB_FaultTimer    : REAL := 0.0;
    tColdSpotTemp_ChC_FaultTimer    : REAL := 0.0;

    rTmrPersistenceTimeout          : REAL := 2.00;                (* Discrepancy qualification persistence [s] *)

    (* ========================================================================================= *)
    (* 6. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) STEP REGISTERS                         *)
    (* ========================================================================================= *)
    eCurrentState                   : INT := 0;                    (* Active 12-stage FSM step index *)
    eNextState                      : INT := 0;                    (* Next pending sequence step index *)
    tStateDwellTimer                : REAL := 0.0;                 (* Elapsed duration in current state [s] *)
    bStateFirstScan                 : BOOL := TRUE;                (* State transition entry trigger *)
    tPreRinsePhaseTimer             : REAL := 0.0;                 (* Pre-rinse to drain elapsed time [s] *)
    tCausticWashTimer               : REAL := 0.0;                 (* Caustic circulation elapsed time [s] *)
    tCausticRecovTimer              : REAL := 0.0;                 (* Caustic reclamation elapsed time [s] *)
    tInterRinseTimer                : REAL := 0.0;                 (* Intermediate water rinse elapsed time [s] *)
    tAcidWashTimer                  : REAL := 0.0;                 (* Acid descaling elapsed time [s] *)
    tAcidRecovTimer                 : REAL := 0.0;                 (* Acid reclamation elapsed time [s] *)
    tFinalRinseTimer                : REAL := 0.0;                 (* Final purified WFI rinse elapsed time [s] *)
    tSIPAirPurgeTimer               : REAL := 0.0;                 (* SIP steam air blowdown purge elapsed time [s] *)
    tSIPHeatUpTimer                 : REAL := 0.0;                 (* Pure steam superheating elapsed time [s] *)
    tSIPHoldTimer                   : REAL := 0.0;                 (* SIP sterilizing hold elapsed time [s] *)
    tSIPCooldownTimer               : REAL := 0.0;                 (* Sterile air overpressure cool elapsed time [s] *)
    tTotalCycleTimer                : REAL := 0.0;                 (* Total multi-phase batch runtime [s] *)
    nTotalBatchesCompleted          : DINT := 0;                   (* Lifetime validated CIP/SIP cycle counter *)

    (* Preset Recipe Stage Dwell Duration Thresholds [s] *)
    rTargetDuration_PreRinse        : REAL := 300.0;               (* Stage 1: Pre-rinse duration [s] *)
    rTargetDuration_CausticWash     : REAL := 1200.0;              (* Stage 2: Caustic wash contact hold [s] *)
    rTargetDuration_CausticRecov    : REAL := 180.0;               (* Stage 3: Caustic recovery flush timeout [s] *)
    rTargetDuration_InterRinse      : REAL := 450.0;               (* Stage 4: Intermediate fresh water rinse [s] *)
    rTargetDuration_AcidWash        : REAL := 900.0;               (* Stage 5: Acid descaling circulation [s] *)
    rTargetDuration_AcidRecov       : REAL := 150.0;               (* Stage 6: Acid recovery flush timeout [s] *)
    rTargetDuration_FinalRinse      : REAL := 600.0;               (* Stage 7: Final WFI rinse validation [s] *)
    rTargetDuration_SIPAirPurge     : REAL := 180.0;               (* Stage 8: Steam trap air evacuation purge [s] *)
    rTargetDuration_SIPHeatUp       : REAL := 400.0;               (* Stage 9: Heating ramp to 121.1 C [s] *)
    rTargetDuration_SIPHoldMax      : REAL := 2400.0;              (* Stage 10: Maximum allowable SIP hold [s] *)
    rTargetDuration_SIPCooling      : REAL := 600.0;               (* Stage 11: Sterile air pressure cooling [s] *)

    (* ========================================================================================= *)
    (* 7. ISA-18.2 MULTI-TIER ALARM TRIP POINTS, LIMITS & DEADBANDS                              *)
    (* ========================================================================================= *)
    (* Supply Delivery Temperature Alarms [deg C] *)
    rAlarmTemp_HH                   : REAL := 138.0;               (* Thermal runaway pure steam blowout trip [deg C] *)
    rAlarmTemp_H                    : REAL := 92.0;                (* High delivery wash temperature warning [deg C] *)
    rAlarmTemp_L                    : REAL := 60.0;                (* Low wash temperature effectiveness warning [deg C] *)
    rAlarmTemp_LL                   : REAL := 15.0;                (* Cryogenic freeze protection trip [deg C] *)
    rDeadband_Temp                  : REAL := 1.5;                 (* Thermal hysteresis reset deadband [deg C] *)

    (* Forward Delivery Line Pressure Alarms [bar] *)
    rAlarmSupplyPress_HH            : REAL := 6.50;                (* High-High piping overpressure emergency trip [bar] *)
    rAlarmSupplyPress_H             : REAL := 5.20;                (* High delivery pressure relief warning [bar] *)
    rAlarmSupplyPress_L             : REAL := 1.20;                (* Low delivery pressure scouring loss warning [bar] *)
    rAlarmSupplyPress_LL            : REAL := 0.40;                (* Pump deadhead / pipe burst emergency trip [bar] *)
    rDeadband_Press                 : REAL := 0.15;                (* Pressure reset deadband [bar] *)

    (* Scavenge Return Suction Pressure Alarms [bar] *)
    rAlarmReturnPress_LL            : REAL := 0.08;                (* Liquid-ring pump cavitation vacuum trip [bar] *)
    rAlarmReturnPress_L             : REAL := 0.25;                (* Return pump cavitation pre-warning [bar] *)
    rDeadband_ReturnPress           : REAL := 0.05;                (* Return pressure reset deadband [bar] *)

    (* Active Buffer Tank Fluid Level Alarms [m] *)
    rAlarmTankLevel_HH              : REAL := 2.85;                (* Tank overfill emergency dump trip [m] *)
    rAlarmTankLevel_H               : REAL := 2.60;                (* Tank high level inlet throttling warning [m] *)
    rAlarmTankLevel_L               : REAL := 0.45;                (* Tank low level make-up advisory warning [m] *)
    rAlarmTankLevel_LL              : REAL := 0.20;                (* Centrifugal pump run-dry cavitation trip [m] *)
    rDeadband_TankLevel             : REAL := 0.05;                (* Tank level reset deadband [m] *)

    (* Chemical Concentration Alarms [%] *)
    rAlarmCausticConc_DevLimit      : REAL := 0.35;                (* Maximum allowable NaOH error from setpoint [%] *)
    rAlarmAcidConc_DevLimit         : REAL := 0.25;                (* Maximum allowable HNO3 error from setpoint [%] *)
    rAlarmTurbidity_High            : REAL := 8.00;                (* Gross soil particulate turbidity warning [NTU] *)
    rAlarmFinalWfi_ConductivityMax  : REAL := 0.0025;              (* Final WFI pure rinse conductivity limit (2.5 uS/cm) [mS/cm] *)

    (* SIP Thermal Sterilization Cold-Spot Alarms *)
    rAlarmColdSpot_HoldLL           : REAL := 121.11;              (* Minimum cold-spot temperature during hold [deg C] *)
    rAlarmSIP_PressureVaporDiffMax  : REAL := 0.35;                (* Max allowed deviation from saturated steam [bar] *)

    (* Internal Flags, Iterators & Scratchpad Variables *)
    bMasterFirstScanDone            : BOOL := FALSE;               (* Cold-start memory parameterization latch *)
    nIdx_i                          : INT := 1;                    (* Matrix row index *)
    nIdx_j                          : INT := 1;                    (* Matrix column index *)
    nIdx_k                          : INT := 1;                    (* Matrix inner product index *)
    nMpcLoop                        : INT := 1;                    (* MPC gradient solver loop index *)
    rScratch1                       : REAL := 0.0;                 (* Arithmetic scratchpad register 1 *)
    rScratch2                       : REAL := 0.0;                 (* Arithmetic scratchpad register 2 *)
    rScratch3                       : REAL := 0.0;                 (* Arithmetic scratchpad register 3 *)
    rScratch4                       : REAL := 0.0;                 (* Arithmetic scratchpad register 4 *)
    rScratch5                       : REAL := 0.0;                 (* Arithmetic scratchpad register 5 *)
    rScratch6                       : REAL := 0.0;                 (* Arithmetic scratchpad register 6 *)
    rScratch7                       : REAL := 0.0;                 (* Arithmetic scratchpad register 7 *)
    rScratch8                       : REAL := 0.0;                 (* Arithmetic scratchpad register 8 *)
    rScratch9                       : REAL := 0.0;                 (* Arithmetic scratchpad register 9 *)
    rScratch10                      : REAL := 0.0;                 (* Arithmetic scratchpad register 10 *)
    rPrevLethalRate                 : REAL := 0.0;                 (* Lethal rate at previous scan L[k-1] *)
    rCalculatedSatVaporPress        : REAL := 0.0;                 (* Saturated steam vapor pressure Antoine [bar] *)
    rActiveFluidDensity             : REAL := 1000.0;              (* Fluid density based on phase [kg/m^3] *)
    rActiveDynamicViscosity         : REAL := 0.0010;              (* Dynamic viscosity based on phase [Pa*s] *)
    rFlowVelocityMean               : REAL := 0.0;                 (* Mean conduit linear velocity [m/s] *)
    rDarcyFrictionFactor            : REAL := 0.020;               (* Darcy turbulent friction factor f [-] *)
    rRoughnessRatio                 : REAL := 0.0;                 (* Relative roughness epsilon / D [-] *)
END_VAR
""")

    # Phase 1: Cold start & matrix initialization
    parts.append("""(* ============================================================================================= *)
(* SECTION 1: MASTER INITIALIZATION & DISCRETE STATE-SPACE MATRICES PARAMETERIZATION            *)
(* ============================================================================================= *)
IF NOT bMasterFirstScanDone THEN
    (* 1.1 Zero-initialize all 10x10 and 10x8 arrays *)
    FOR nIdx_i := 1 TO 10 DO
        FOR nIdx_j := 1 TO 10 DO
            arrA[nIdx_i, nIdx_j] := 0.0;
            arrC[nIdx_i, nIdx_j] := 0.0;
            arrKalmanGain[nIdx_i, nIdx_j] := 0.0;
            arrErrorCov_P[nIdx_i, nIdx_j] := 0.0;
        END_FOR;
        FOR nIdx_k := 1 TO 8 DO
            arrB[nIdx_i, nIdx_k] := 0.0;
            arrD[nIdx_i, nIdx_k] := 0.0;
        END_FOR;
        arrState_x[nIdx_i] := 0.0;
        arrState_x_next[nIdx_i] := 0.0;
        arrState_x_hat[nIdx_i] := 0.0;
        arrStateRef[nIdx_i] := 0.0;
        arrMeasurement_z[nIdx_i] := 0.0;
        arrInnovation_e[nIdx_i] := 0.0;
        arrProcessNoise_Q[nIdx_i] := 0.01;
        arrSensorNoise_R[nIdx_i] := 0.05;
        arrQ_MpcCost[nIdx_i] := 10.0;
        arrP_TerminalCost[nIdx_i] := 50.0;
    END_FOR;

    FOR nIdx_k := 1 TO 8 DO
        arrControl_u[nIdx_k] := 0.0;
        arrControl_u_prev[nIdx_k] := 0.0;
        arrMpcGradient[nIdx_k] := 0.0;
        arrR_MpcCost[nIdx_k] := 1.0;
        arrRd_MpcRateCost[nIdx_k] := 5.0;
        arrU_LowerBound[nIdx_k] := 0.0;
        arrU_UpperBound[nIdx_k] := 100.0;
        arrDeltaU_Max[nIdx_k] := 5.0;
    END_FOR;

    (* 1.2 Euler-Mapped Continuous-to-Discrete State Matrix arrA (Ts = 0.100 s) *)
    (* State 1: T_sup - Shell-and-tube product delivery temperature [deg C] *)
    arrA[1, 1] := 0.945000;      (* Thermal self-decay / fluid residence transit *)
    arrA[1, 2] := 0.048000;      (* Heat conduction from condensing shell steam *)
    arrA[1, 3] := 0.005000;      (* Return fluid recirculation thermal carryover *)
    arrA[1, 7] := -0.001850;     (* Higher forward flow increases convective heat uptake rate *)

    (* State 2: T_stm - Shell condensing steam temperature [deg C] *)
    arrA[2, 2] := 0.885000;      (* Rapid condensation thermal dissipation *)
    arrA[2, 1] := -0.062000;     (* Heat transfer loss to colder tube-side product *)

    (* State 3: T_ret - Return line scavenge fluid temperature [deg C] *)
    arrA[3, 3] := 0.932000;      (* Piping convective transport thermal decay *)
    arrA[3, 1] := 0.055000;      (* Thermal propagation from supply circuit through equipment *)

    (* State 4: Kap_sup - Supply line in-line conductivity [mS/cm] *)
    arrA[4, 4] := 0.920000;      (* In-line conductivity mixing dynamic decay *)
    arrA[4, 6] := 0.075000;      (* Chemical concentration in buffer tank directly feeds supply *)

    (* State 5: Kap_ret - Return line in-line conductivity [mS/cm] *)
    arrA[5, 5] := 0.895000;      (* Transport lag dispersion through cleaned process circuit *)
    arrA[5, 4] := 0.098000;      (* Supply chemical concentration wave arrival *)

    (* State 6: C_tank - Active buffer tank chemical concentration [%] *)
    arrA[6, 6] := 0.985000;      (* Tank large fluid volume dilution retention *)
    arrA[6, 5] := 0.012500;      (* Return fluid reclaim chemical recirculation into tank *)

    (* State 7: Q_sup - Forward delivery volumetric flow rate [m3/h] *)
    arrA[7, 7] := 0.865000;      (* Centrifugal pump hydraulic momentum response *)
    arrA[7, 9] := 0.045000;      (* Positive suction hydrostatic head boosts pump intake *)

    (* State 8: Q_ret - Return scavenge pump flow rate [m3/h] *)
    arrA[8, 8] := 0.840000;      (* Self-priming liquid-ring hydraulic response *)
    arrA[8, 7] := 0.120000;      (* Circuit mass balance: return scavenge follows supply flow *)

    (* State 9: H_tank - Active buffer tank hydrostatic fluid level [m] *)
    arrA[9, 9] := 1.000000;      (* Pure integrator: tank fluid mass accumulation *)
    arrA[9, 7] := -0.000065;     (* Outflow: supply pump drawing fluid lowers level *)
    arrA[9, 8] := 0.000062;      (* Inflow: return scavenge flow replenishes level *)

    (* State 10: T_cold - Low-point piping cold-spot drain temperature [deg C] *)
    arrA[10, 10] := 0.962000;    (* Heavy sanitary valve body thermal inertia *)
    arrA[10, 1] := 0.018000;     (* Convective steam heat reaching cold spot drain *)
    arrA[10, 2] := 0.015000;     (* Thermal radiation and conduction along steam line *)

    (* 1.3 Discrete Input Coupling Matrix arrB (Ts = 0.100 s) *)
    (* Input 1: u[1] = X_stm (Shell steam valve [%]) *)
    arrB[1, 1] := 0.014500;      (* Indirect delivery temperature ramp *)
    arrB[2, 1] := 0.185000;      (* Direct steam pressure/temperature ramp in shell *)

    (* Input 2: u[2] = N_sup (Supply pump speed [%]) *)
    arrB[7, 2] := 0.420000;      (* Forward flow delivery rate increase per % speed *)
    arrB[9, 2] := -0.000450;     (* Tank level drawdown per % pump speed *)

    (* Input 3: u[3] = N_ret (Return scavenge pump speed [%]) *)
    arrB[8, 3] := 0.385000;      (* Scavenge evacuation rate per % speed *)
    arrB[9, 3] := 0.000420;      (* Tank level recovery per % return scavenge speed *)

    (* Input 4: u[4] = N_dose_caustic (50% NaOH dosing pump [%]) *)
    arrB[4, 4] := 0.065000;      (* Supply conductivity increase from concentrated caustic *)
    arrB[6, 4] := 0.014500;      (* Buffer tank caustic concentration enrichment *)

    (* Input 5: u[5] = N_dose_acid (60% HNO3 dosing pump [%]) *)
    arrB[4, 5] := 0.052000;      (* Supply conductivity increase from concentrated acid *)
    arrB[6, 5] := 0.011800;      (* Buffer tank acid concentration enrichment *)

    (* Input 6: u[6] = X_wfi (WFI make-up valve [%]) *)
    arrB[4, 6] := -0.035000;     (* Conductivity dilution via pure water addition *)
    arrB[6, 6] := -0.008500;     (* Chemical concentration dilution in tank *)
    arrB[9, 6] := 0.000550;      (* Tank fluid level rise per % make-up valve *)

    (* Input 7: u[7] = X_divert (3-way return divert valve [%]) *)
    arrB[6, 7] := 0.004200;      (* Reclaim chemical mass return into active tank *)
    arrB[9, 7] := 0.000380;      (* Return volume directed into tank vs trade drain *)

    (* Input 8: u[8] = X_sip_stm (Pure steam direct SIP injection [%]) *)
    arrB[1, 8] := 0.125000;      (* Rapid piping superheating during SIP *)
    arrB[10, 8] := 0.245000;     (* Direct cold-spot drain heating from pure steam *)

    (* 1.4 Output Mapping Matrix arrC (Direct Identity Telemetry) *)
    FOR nIdx_i := 1 TO 10 DO
        arrC[nIdx_i, nIdx_i] := 1.000000;
    END_FOR;

    (* 1.5 Receding-Horizon MPC Quadratic Penalty Tuning Weights *)
    arrQ_MpcCost[1] := 1200.0;    (* Delivery temperature tracking (critical for cleaning & SIP) *)
    arrQ_MpcCost[2] := 250.0;     (* Shell steam temperature penalty *)
    arrQ_MpcCost[3] := 450.0;     (* Return temperature tracking penalty *)
    arrQ_MpcCost[4] := 1800.0;    (* Supply conductivity tracking penalty *)
    arrQ_MpcCost[5] := 950.0;     (* Return conductivity tracking penalty *)
    arrQ_MpcCost[6] := 2400.0;    (* Chemical concentration error penalty *)
    arrQ_MpcCost[7] := 1500.0;    (* Scouring flow rate penalty (guarantee Re >= 200,000) *)
    arrQ_MpcCost[8] := 1600.0;    (* Return flow balancing penalty (prevent pump cavitation) *)
    arrQ_MpcCost[9] := 3200.0;    (* Tank level regulation (prevent run-dry and overflow) *)
    arrQ_MpcCost[10] := 5000.0;   (* Cold-spot temperature penalty during SIP hold *)

    arrR_MpcCost[1] := 3.5;       (* Steam valve throttling effort *)
    arrR_MpcCost[2] := 1.2;       (* Supply pump VFD modulation *)
    arrR_MpcCost[3] := 1.5;       (* Return pump VFD modulation *)
    arrR_MpcCost[4] := 8.0;       (* Caustic dosing chemical usage penalty *)
    arrR_MpcCost[5] := 9.0;       (* Acid dosing chemical usage penalty *)
    arrR_MpcCost[6] := 2.0;       (* WFI make-up valve effort *)
    arrR_MpcCost[7] := 1.0;       (* Return divert valve positioning *)
    arrR_MpcCost[8] := 4.5;       (* Pure steam SIP valve effort *)

    arrRd_MpcRateCost[1] := 12.0;  (* Damp steam valve thermal shocks *)
    arrRd_MpcRateCost[2] := 8.0;   (* Damp supply pump water hammer *)
    arrRd_MpcRateCost[3] := 10.0;  (* Damp return pump cavitation surges *)
    arrRd_MpcRateCost[4] := 25.0;  (* Damp dosing pump chemical pulsing *)
    arrRd_MpcRateCost[5] := 28.0;  (* Damp acid dosing pulsing *)
    arrRd_MpcRateCost[6] := 6.0;   (* WFI valve movement smoothing *)
    arrRd_MpcRateCost[7] := 4.0;   (* Divert valve switching smoothing *)
    arrRd_MpcRateCost[8] := 15.0;  (* Pure steam SIP valve smoothing *)

    (* Terminal State Penalties *)
    FOR nIdx_i := 1 TO 10 DO
        arrP_TerminalCost[nIdx_i] := arrQ_MpcCost[nIdx_i] * 3.5;
    END_FOR;

    (* 1.6 Extended Kalman Filter Steady-State Gains *)
    arrKalmanGain[1, 1] := 0.285;
    arrKalmanGain[2, 2] := 0.312;
    arrKalmanGain[3, 3] := 0.264;
    arrKalmanGain[4, 4] := 0.345;
    arrKalmanGain[5, 5] := 0.298;
    arrKalmanGain[6, 6] := 0.185;
    arrKalmanGain[7, 7] := 0.410;
    arrKalmanGain[8, 8] := 0.380;
    arrKalmanGain[9, 9] := 0.450;
    arrKalmanGain[10, 10] := 0.330;

    bMasterFirstScanDone := TRUE;
END_IF;
""")

    # Phase 2: 2oo3 TMR Voting Logic
    parts.append("""(* ============================================================================================= *)
(* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS          *)
(* ============================================================================================= *)
(* 2.1 Supply Toroidal Conductivity Transmitters (A, B, C) *)
IF (ABS(rSupplyConductivity_ChA - rSupplyConductivity_ChB) > rSupplyCond_TmrThreshold) AND
   (ABS(rSupplyConductivity_ChA - rSupplyConductivity_ChC) > rSupplyCond_TmrThreshold) THEN
    tSupplyCond_ChA_FaultTimer := tSupplyCond_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tSupplyCond_ChA_FaultTimer >= rTmrPersistenceTimeout THEN
        bSupplyCond_ChA_Valid := FALSE;
    END_IF;
ELSE
    tSupplyCond_ChA_FaultTimer := MAX(0.0, tSupplyCond_ChA_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bSupplyCond_ChA_Valid := TRUE;
END_IF;

IF (ABS(rSupplyConductivity_ChB - rSupplyConductivity_ChA) > rSupplyCond_TmrThreshold) AND
   (ABS(rSupplyConductivity_ChB - rSupplyConductivity_ChC) > rSupplyCond_TmrThreshold) THEN
    tSupplyCond_ChB_FaultTimer := tSupplyCond_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tSupplyCond_ChB_FaultTimer >= rTmrPersistenceTimeout THEN
        bSupplyCond_ChB_Valid := FALSE;
    END_IF;
ELSE
    tSupplyCond_ChB_FaultTimer := MAX(0.0, tSupplyCond_ChB_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bSupplyCond_ChB_Valid := TRUE;
END_IF;

IF (ABS(rSupplyConductivity_ChC - rSupplyConductivity_ChA) > rSupplyCond_TmrThreshold) AND
   (ABS(rSupplyConductivity_ChC - rSupplyConductivity_ChB) > rSupplyCond_TmrThreshold) THEN
    tSupplyCond_ChC_FaultTimer := tSupplyCond_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tSupplyCond_ChC_FaultTimer >= rTmrPersistenceTimeout THEN
        bSupplyCond_ChC_Valid := FALSE;
    END_IF;
ELSE
    tSupplyCond_ChC_FaultTimer := MAX(0.0, tSupplyCond_ChC_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bSupplyCond_ChC_Valid := TRUE;
END_IF;

(* Supply Conductivity Voting Resolution *)
IF bSupplyCond_ChA_Valid AND bSupplyCond_ChB_Valid AND bSupplyCond_ChC_Valid THEN
    (* 2oo3 Median Selection *)
    IF ((rSupplyConductivity_ChA >= rSupplyConductivity_ChB) AND (rSupplyConductivity_ChA <= rSupplyConductivity_ChC)) OR
       ((rSupplyConductivity_ChA >= rSupplyConductivity_ChC) AND (rSupplyConductivity_ChA <= rSupplyConductivity_ChB)) THEN
        rVotedSupplyConductivity := rSupplyConductivity_ChA;
    ELSIF ((rSupplyConductivity_ChB >= rSupplyConductivity_ChA) AND (rSupplyConductivity_ChB <= rSupplyConductivity_ChC)) OR
          ((rSupplyConductivity_ChB >= rSupplyConductivity_ChC) AND (rSupplyConductivity_ChB <= rSupplyConductivity_ChA)) THEN
        rVotedSupplyConductivity := rSupplyConductivity_ChB;
    ELSE
        rVotedSupplyConductivity := rSupplyConductivity_ChC;
    END_IF;
ELSIF bSupplyCond_ChA_Valid AND bSupplyCond_ChB_Valid THEN
    rVotedSupplyConductivity := 0.5 * (rSupplyConductivity_ChA + rSupplyConductivity_ChB);
ELSIF bSupplyCond_ChA_Valid AND bSupplyCond_ChC_Valid THEN
    rVotedSupplyConductivity := 0.5 * (rSupplyConductivity_ChA + rSupplyConductivity_ChC);
ELSIF bSupplyCond_ChB_Valid AND bSupplyCond_ChC_Valid THEN
    rVotedSupplyConductivity := 0.5 * (rSupplyConductivity_ChB + rSupplyConductivity_ChC);
ELSIF bSupplyCond_ChA_Valid THEN
    rVotedSupplyConductivity := rSupplyConductivity_ChA;
ELSIF bSupplyCond_ChB_Valid THEN
    rVotedSupplyConductivity := rSupplyConductivity_ChB;
ELSE
    rVotedSupplyConductivity := rSupplyConductivity_ChC;
END_IF;

(* 2.2 Return Toroidal Conductivity Transmitters (A, B, C) *)
IF (ABS(rReturnConductivity_ChA - rReturnConductivity_ChB) > rReturnCond_TmrThreshold) AND
   (ABS(rReturnConductivity_ChA - rReturnConductivity_ChC) > rReturnCond_TmrThreshold) THEN
    tReturnCond_ChA_FaultTimer := tReturnCond_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tReturnCond_ChA_FaultTimer >= rTmrPersistenceTimeout THEN
        bReturnCond_ChA_Valid := FALSE;
    END_IF;
ELSE
    tReturnCond_ChA_FaultTimer := MAX(0.0, tReturnCond_ChA_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bReturnCond_ChA_Valid := TRUE;
END_IF;

IF (ABS(rReturnConductivity_ChB - rReturnConductivity_ChA) > rReturnCond_TmrThreshold) AND
   (ABS(rReturnConductivity_ChB - rReturnConductivity_ChC) > rReturnCond_TmrThreshold) THEN
    tReturnCond_ChB_FaultTimer := tReturnCond_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tReturnCond_ChB_FaultTimer >= rTmrPersistenceTimeout THEN
        bReturnCond_ChB_Valid := FALSE;
    END_IF;
ELSE
    tReturnCond_ChB_FaultTimer := MAX(0.0, tReturnCond_ChB_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bReturnCond_ChB_Valid := TRUE;
END_IF;

IF (ABS(rReturnConductivity_ChC - rReturnConductivity_ChA) > rReturnCond_TmrThreshold) AND
   (ABS(rReturnConductivity_ChC - rReturnConductivity_ChB) > rReturnCond_TmrThreshold) THEN
    tReturnCond_ChC_FaultTimer := tReturnCond_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tReturnCond_ChC_FaultTimer >= rTmrPersistenceTimeout THEN
        bReturnCond_ChC_Valid := FALSE;
    END_IF;
ELSE
    tReturnCond_ChC_FaultTimer := MAX(0.0, tReturnCond_ChC_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bReturnCond_ChC_Valid := TRUE;
END_IF;

(* Return Conductivity Voting Resolution *)
IF bReturnCond_ChA_Valid AND bReturnCond_ChB_Valid AND bReturnCond_ChC_Valid THEN
    IF ((rReturnConductivity_ChA >= rReturnConductivity_ChB) AND (rReturnConductivity_ChA <= rReturnConductivity_ChC)) OR
       ((rReturnConductivity_ChA >= rReturnConductivity_ChC) AND (rReturnConductivity_ChA <= rReturnConductivity_ChB)) THEN
        rVotedReturnConductivity := rReturnConductivity_ChA;
    ELSIF ((rReturnConductivity_ChB >= rReturnConductivity_ChA) AND (rReturnConductivity_ChB <= rReturnConductivity_ChC)) OR
          ((rReturnConductivity_ChB >= rReturnConductivity_ChC) AND (rReturnConductivity_ChB <= rReturnConductivity_ChA)) THEN
        rVotedReturnConductivity := rReturnConductivity_ChB;
    ELSE
        rVotedReturnConductivity := rReturnConductivity_ChC;
    END_IF;
ELSIF bReturnCond_ChA_Valid AND bReturnCond_ChB_Valid THEN
    rVotedReturnConductivity := 0.5 * (rReturnConductivity_ChA + rReturnConductivity_ChB);
ELSIF bReturnCond_ChA_Valid AND bReturnCond_ChC_Valid THEN
    rVotedReturnConductivity := 0.5 * (rReturnConductivity_ChA + rReturnConductivity_ChC);
ELSIF bReturnCond_ChB_Valid AND bReturnCond_ChC_Valid THEN
    rVotedReturnConductivity := 0.5 * (rReturnConductivity_ChB + rReturnConductivity_ChC);
ELSIF bReturnCond_ChA_Valid THEN
    rVotedReturnConductivity := rReturnConductivity_ChA;
ELSIF bReturnCond_ChB_Valid THEN
    rVotedReturnConductivity := rReturnConductivity_ChB;
ELSE
    rVotedReturnConductivity := rReturnConductivity_ChC;
END_IF;

(* 2.3 Forward Delivery Sanitary Flowmeters (A, B, C) *)
IF (ABS(rSupplyFlowRate_ChA - rSupplyFlowRate_ChB) > rSupplyFlow_TmrThreshold) AND
   (ABS(rSupplyFlowRate_ChA - rSupplyFlowRate_ChC) > rSupplyFlow_TmrThreshold) THEN
    tSupplyFlow_ChA_FaultTimer := tSupplyFlow_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tSupplyFlow_ChA_FaultTimer >= rTmrPersistenceTimeout THEN
        bSupplyFlow_ChA_Valid := FALSE;
    END_IF;
ELSE
    tSupplyFlow_ChA_FaultTimer := MAX(0.0, tSupplyFlow_ChA_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bSupplyFlow_ChA_Valid := TRUE;
END_IF;

IF (ABS(rSupplyFlowRate_ChB - rSupplyFlowRate_ChA) > rSupplyFlow_TmrThreshold) AND
   (ABS(rSupplyFlowRate_ChB - rSupplyFlowRate_ChC) > rSupplyFlow_TmrThreshold) THEN
    tSupplyFlow_ChB_FaultTimer := tSupplyFlow_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tSupplyFlow_ChB_FaultTimer >= rTmrPersistenceTimeout THEN
        bSupplyFlow_ChB_Valid := FALSE;
    END_IF;
ELSE
    tSupplyFlow_ChB_FaultTimer := MAX(0.0, tSupplyFlow_ChB_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bSupplyFlow_ChB_Valid := TRUE;
END_IF;

IF (ABS(rSupplyFlowRate_ChC - rSupplyFlowRate_ChA) > rSupplyFlow_TmrThreshold) AND
   (ABS(rSupplyFlowRate_ChC - rSupplyFlowRate_ChB) > rSupplyFlow_TmrThreshold) THEN
    tSupplyFlow_ChC_FaultTimer := tSupplyFlow_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tSupplyFlow_ChC_FaultTimer >= rTmrPersistenceTimeout THEN
        bSupplyFlow_ChC_Valid := FALSE;
    END_IF;
ELSE
    tSupplyFlow_ChC_FaultTimer := MAX(0.0, tSupplyFlow_ChC_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bSupplyFlow_ChC_Valid := TRUE;
END_IF;

(* Supply Flow Voting Resolution *)
IF bSupplyFlow_ChA_Valid AND bSupplyFlow_ChB_Valid AND bSupplyFlow_ChC_Valid THEN
    IF ((rSupplyFlowRate_ChA >= rSupplyFlowRate_ChB) AND (rSupplyFlowRate_ChA <= rSupplyFlowRate_ChC)) OR
       ((rSupplyFlowRate_ChA >= rSupplyFlowRate_ChC) AND (rSupplyFlowRate_ChA <= rSupplyFlowRate_ChB)) THEN
        rVotedSupplyFlow := rSupplyFlowRate_ChA;
    ELSIF ((rSupplyFlowRate_ChB >= rSupplyFlowRate_ChA) AND (rSupplyFlowRate_ChB <= rSupplyFlowRate_ChC)) OR
          ((rSupplyFlowRate_ChB >= rSupplyFlowRate_ChC) AND (rSupplyFlowRate_ChB <= rSupplyFlowRate_ChA)) THEN
        rVotedSupplyFlow := rSupplyFlowRate_ChB;
    ELSE
        rVotedSupplyFlow := rSupplyFlowRate_ChC;
    END_IF;
ELSIF bSupplyFlow_ChA_Valid AND bSupplyFlow_ChB_Valid THEN
    rVotedSupplyFlow := 0.5 * (rSupplyFlowRate_ChA + rSupplyFlowRate_ChB);
ELSIF bSupplyFlow_ChA_Valid AND bSupplyFlow_ChC_Valid THEN
    rVotedSupplyFlow := 0.5 * (rSupplyFlowRate_ChA + rSupplyFlowRate_ChC);
ELSIF bSupplyFlow_ChB_Valid AND bSupplyFlow_ChC_Valid THEN
    rVotedSupplyFlow := 0.5 * (rSupplyFlowRate_ChB + rSupplyFlowRate_ChC);
ELSIF bSupplyFlow_ChA_Valid THEN
    rVotedSupplyFlow := rSupplyFlowRate_ChA;
ELSIF bSupplyFlow_ChB_Valid THEN
    rVotedSupplyFlow := rSupplyFlowRate_ChB;
ELSE
    rVotedSupplyFlow := rSupplyFlowRate_ChC;
END_IF;

(* 2.4 Return Scavenge Sanitary Flowmeters (A, B, C) *)
IF (ABS(rReturnFlowRate_ChA - rReturnFlowRate_ChB) > rReturnFlow_TmrThreshold) AND
   (ABS(rReturnFlowRate_ChA - rReturnFlowRate_ChC) > rReturnFlow_TmrThreshold) THEN
    tReturnFlow_ChA_FaultTimer := tReturnFlow_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tReturnFlow_ChA_FaultTimer >= rTmrPersistenceTimeout THEN
        bReturnFlow_ChA_Valid := FALSE;
    END_IF;
ELSE
    tReturnFlow_ChA_FaultTimer := MAX(0.0, tReturnFlow_ChA_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bReturnFlow_ChA_Valid := TRUE;
END_IF;

IF (ABS(rReturnFlowRate_ChB - rReturnFlowRate_ChA) > rReturnFlow_TmrThreshold) AND
   (ABS(rReturnFlowRate_ChB - rReturnFlowRate_ChC) > rReturnFlow_TmrThreshold) THEN
    tReturnFlow_ChB_FaultTimer := tReturnFlow_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tReturnFlow_ChB_FaultTimer >= rTmrPersistenceTimeout THEN
        bReturnFlow_ChB_Valid := FALSE;
    END_IF;
ELSE
    tReturnFlow_ChB_FaultTimer := MAX(0.0, tReturnFlow_ChB_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bReturnFlow_ChB_Valid := TRUE;
END_IF;

IF (ABS(rReturnFlowRate_ChC - rReturnFlowRate_ChA) > rReturnFlow_TmrThreshold) AND
   (ABS(rReturnFlowRate_ChC - rReturnFlowRate_ChB) > rReturnFlow_TmrThreshold) THEN
    tReturnFlow_ChC_FaultTimer := tReturnFlow_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tReturnFlow_ChC_FaultTimer >= rTmrPersistenceTimeout THEN
        bReturnFlow_ChC_Valid := FALSE;
    END_IF;
ELSE
    tReturnFlow_ChC_FaultTimer := MAX(0.0, tReturnFlow_ChC_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bReturnFlow_ChC_Valid := TRUE;
END_IF;

(* Return Flow Voting Resolution *)
IF bReturnFlow_ChA_Valid AND bReturnFlow_ChB_Valid AND bReturnFlow_ChC_Valid THEN
    IF ((rReturnFlowRate_ChA >= rReturnFlowRate_ChB) AND (rReturnFlowRate_ChA <= rReturnFlowRate_ChC)) OR
       ((rReturnFlowRate_ChA >= rReturnFlowRate_ChC) AND (rReturnFlowRate_ChA <= rReturnFlowRate_ChB)) THEN
        rVotedReturnFlow := rReturnFlowRate_ChA;
    ELSIF ((rReturnFlowRate_ChB >= rReturnFlowRate_ChA) AND (rReturnFlowRate_ChB <= rReturnFlowRate_ChC)) OR
          ((rReturnFlowRate_ChB >= rReturnFlowRate_ChC) AND (rReturnFlowRate_ChB <= rReturnFlowRate_ChA)) THEN
        rVotedReturnFlow := rReturnFlowRate_ChB;
    ELSE
        rVotedReturnFlow := rReturnFlowRate_ChC;
    END_IF;
ELSIF bReturnFlow_ChA_Valid AND bReturnFlow_ChB_Valid THEN
    rVotedReturnFlow := 0.5 * (rReturnFlowRate_ChA + rReturnFlowRate_ChB);
ELSIF bReturnFlow_ChA_Valid AND bReturnFlow_ChC_Valid THEN
    rVotedReturnFlow := 0.5 * (rReturnFlowRate_ChA + rReturnFlowRate_ChC);
ELSIF bReturnFlow_ChB_Valid AND bReturnFlow_ChC_Valid THEN
    rVotedReturnFlow := 0.5 * (rReturnFlowRate_ChB + rReturnFlowRate_ChC);
ELSIF bReturnFlow_ChA_Valid THEN
    rVotedReturnFlow := rReturnFlowRate_ChA;
ELSIF bReturnFlow_ChB_Valid THEN
    rVotedReturnFlow := rReturnFlowRate_ChB;
ELSE
    rVotedReturnFlow := rReturnFlowRate_ChC;
END_IF;

(* 2.5 Critical Low-Point Cold-Spot Drain RTDs (A, B, C) *)
IF (ABS(rColdSpotTemp_ChA - rColdSpotTemp_ChB) > rColdSpotTemp_TmrThreshold) AND
   (ABS(rColdSpotTemp_ChA - rColdSpotTemp_ChC) > rColdSpotTemp_TmrThreshold) THEN
    tColdSpotTemp_ChA_FaultTimer := tColdSpotTemp_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tColdSpotTemp_ChA_FaultTimer >= rTmrPersistenceTimeout THEN
        bColdSpotTemp_ChA_Valid := FALSE;
    END_IF;
ELSE
    tColdSpotTemp_ChA_FaultTimer := MAX(0.0, tColdSpotTemp_ChA_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bColdSpotTemp_ChA_Valid := TRUE;
END_IF;

IF (ABS(rColdSpotTemp_ChB - rColdSpotTemp_ChA) > rColdSpotTemp_TmrThreshold) AND
   (ABS(rColdSpotTemp_ChB - rColdSpotTemp_ChC) > rColdSpotTemp_TmrThreshold) THEN
    tColdSpotTemp_ChB_FaultTimer := tColdSpotTemp_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tColdSpotTemp_ChB_FaultTimer >= rTmrPersistenceTimeout THEN
        bColdSpotTemp_ChB_Valid := FALSE;
    END_IF;
ELSE
    tColdSpotTemp_ChB_FaultTimer := MAX(0.0, tColdSpotTemp_ChB_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bColdSpotTemp_ChB_Valid := TRUE;
END_IF;

IF (ABS(rColdSpotTemp_ChC - rColdSpotTemp_ChA) > rColdSpotTemp_TmrThreshold) AND
   (ABS(rColdSpotTemp_ChC - rColdSpotTemp_ChB) > rColdSpotTemp_TmrThreshold) THEN
    tColdSpotTemp_ChC_FaultTimer := tColdSpotTemp_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tColdSpotTemp_ChC_FaultTimer >= rTmrPersistenceTimeout THEN
        bColdSpotTemp_ChC_Valid := FALSE;
    END_IF;
ELSE
    tColdSpotTemp_ChC_FaultTimer := MAX(0.0, tColdSpotTemp_ChC_FaultTimer - (rConst_ScanDeltaTime * 0.5));
    bColdSpotTemp_ChC_Valid := TRUE;
END_IF;

(* Cold-Spot Temperature Voting Resolution (Conservative Selection: Minimum of Healthy Probes) *)
IF bColdSpotTemp_ChA_Valid AND bColdSpotTemp_ChB_Valid AND bColdSpotTemp_ChC_Valid THEN
    (* During SIP sterilization, selecting minimum temperature guarantees conservative lethality validation *)
    rVotedColdSpotTemp := MIN(rColdSpotTemp_ChA, MIN(rColdSpotTemp_ChB, rColdSpotTemp_ChC));
ELSIF bColdSpotTemp_ChA_Valid AND bColdSpotTemp_ChB_Valid THEN
    rVotedColdSpotTemp := MIN(rColdSpotTemp_ChA, rColdSpotTemp_ChB);
ELSIF bColdSpotTemp_ChA_Valid AND bColdSpotTemp_ChC_Valid THEN
    rVotedColdSpotTemp := MIN(rColdSpotTemp_ChA, rColdSpotTemp_ChC);
ELSIF bColdSpotTemp_ChB_Valid AND bColdSpotTemp_ChC_Valid THEN
    rVotedColdSpotTemp := MIN(rColdSpotTemp_ChB, rColdSpotTemp_ChC);
ELSIF bColdSpotTemp_ChA_Valid THEN
    rVotedColdSpotTemp := rColdSpotTemp_ChA;
ELSIF bColdSpotTemp_ChB_Valid THEN
    rVotedColdSpotTemp := rColdSpotTemp_ChB;
ELSE
    rVotedColdSpotTemp := rColdSpotTemp_ChC;
END_IF;

(* Bit-Pack TMR Discrepancy Status Word *)
wTMR_DiscrepancyStatus.0 := NOT bSupplyCond_ChA_Valid;
wTMR_DiscrepancyStatus.1 := NOT bSupplyCond_ChB_Valid;
wTMR_DiscrepancyStatus.2 := NOT bSupplyCond_ChC_Valid;
wTMR_DiscrepancyStatus.3 := NOT bReturnCond_ChA_Valid;
wTMR_DiscrepancyStatus.4 := NOT bReturnCond_ChB_Valid;
wTMR_DiscrepancyStatus.5 := NOT bReturnCond_ChC_Valid;
wTMR_DiscrepancyStatus.6 := NOT bSupplyFlow_ChA_Valid;
wTMR_DiscrepancyStatus.7 := NOT bSupplyFlow_ChB_Valid;
wTMR_DiscrepancyStatus.8 := NOT bSupplyFlow_ChC_Valid;
wTMR_DiscrepancyStatus.9 := NOT bReturnFlow_ChA_Valid;
wTMR_DiscrepancyStatus.10 := NOT bReturnFlow_ChB_Valid;
wTMR_DiscrepancyStatus.11 := NOT bReturnFlow_ChC_Valid;
wTMR_DiscrepancyStatus.12 := NOT bColdSpotTemp_ChA_Valid;
wTMR_DiscrepancyStatus.13 := NOT bColdSpotTemp_ChB_Valid;
wTMR_DiscrepancyStatus.14 := NOT bColdSpotTemp_ChC_Valid;
""")

    # Phase 3: Analytical & Cyber-Physical Conversions
    parts.append("""(* ============================================================================================= *)
(* SECTION 3: ANALYTICAL & CYBER-PHYSICAL PROCESS CONVERSIONS                                    *)
(* ============================================================================================= *)
(* 3.1 Toroidal Conductivity Temperature Normalization to 25.0 deg C *)
(* Select active thermal coefficient based on FSM phase *)
IF (eCurrentState = 2) OR (eCurrentState = 3) THEN
    (* Caustic Wash Phase: alpha = 0.0210 / deg C *)
    rCompensatedSupplyCond25 := rVotedSupplyConductivity / MAX(0.20, (1.0 + (rConst_TempCoeffCaustic * (rSupplyHeaderTemp - 25.0))));
    rCompensatedReturnCond25 := rVotedReturnConductivity / MAX(0.20, (1.0 + (rConst_TempCoeffCaustic * (rReturnHeaderTemp - 25.0))));
ELSIF (eCurrentState = 5) OR (eCurrentState = 6) THEN
    (* Acid Wash Phase: alpha = 0.0165 / deg C *)
    rCompensatedSupplyCond25 := rVotedSupplyConductivity / MAX(0.20, (1.0 + (rConst_TempCoeffAcid * (rSupplyHeaderTemp - 25.0))));
    rCompensatedReturnCond25 := rVotedReturnConductivity / MAX(0.20, (1.0 + (rConst_TempCoeffAcid * (rReturnHeaderTemp - 25.0))));
ELSE
    (* Water Rinse / WFI Phase: alpha = 0.0220 / deg C *)
    rCompensatedSupplyCond25 := rVotedSupplyConductivity / MAX(0.20, (1.0 + (rConst_TempCoeffWater * (rSupplyHeaderTemp - 25.0))));
    rCompensatedReturnCond25 := rVotedReturnConductivity / MAX(0.20, (1.0 + (rConst_TempCoeffWater * (rReturnHeaderTemp - 25.0))));
END_IF;

(* 3.2 Dynamic Chemical Concentration Polynomial Formulation *)
(* Caustic NaOH Concentration [% w/w] *)
rCalculatedCausticPct := rConst_CausticPoly_a0 +
                         (rConst_CausticPoly_a1 * rCompensatedSupplyCond25) +
                         (rConst_CausticPoly_a2 * (rCompensatedSupplyCond25 * rCompensatedSupplyCond25));
rCalculatedCausticPct := MAX(0.0, MIN(10.0, rCalculatedCausticPct));

(* Acid HNO3 Concentration [% w/w] *)
rCalculatedAcidPct := rConst_AcidPoly_b0 +
                      (rConst_AcidPoly_b1 * rCompensatedSupplyCond25) +
                      (rConst_AcidPoly_b2 * (rCompensatedSupplyCond25 * rCompensatedSupplyCond25));
rCalculatedAcidPct := MAX(0.0, MIN(10.0, rCalculatedAcidPct));

(* 3.3 Hydrodynamic Boundary Layer Scouring & Sinner Circle Mechanical Action *)
(* Determine fluid properties based on state *)
IF (eCurrentState = 2) OR (eCurrentState = 3) THEN
    rActiveFluidDensity := rConst_CausticDensity;
    rActiveDynamicViscosity := rConst_CausticViscosity;
ELSIF (eCurrentState = 5) OR (eCurrentState = 6) THEN
    rActiveFluidDensity := rConst_AcidDensity;
    rActiveDynamicViscosity := rConst_AcidViscosity;
ELSE
    rActiveFluidDensity := rConst_WaterDensity;
    rActiveDynamicViscosity := rConst_WaterDynamicViscosity;
END_IF;

(* Mean linear pipe flow velocity: v = Q [m3/s] / A_pipe [m2] *)
rFlowVelocityMean := (rVotedSupplyFlow / 3600.0) / rConst_PipeCrossSectionArea;

(* Pipe Reynolds Number: Re = (rho * v * D) / mu *)
rReynoldsNumberSupply := (rActiveFluidDensity * rFlowVelocityMean * rConst_PipeDiameterInner) / MAX(0.0001, rActiveDynamicViscosity);

(* Swamee-Jain explicit Darcy friction factor approximation *)
IF rReynoldsNumberSupply > 4000.0 THEN
    rRoughnessRatio := rConst_PipeSurfaceRoughness / (3.7 * rConst_PipeDiameterInner);
    rScratch1 := rRoughnessRatio + (5.74 / MAX(1.0, EXPT(rReynoldsNumberSupply, 0.9)));
    rScratch2 := LOG(rScratch1); (* natural log base e *)
    rScratch3 := rScratch2 / 2.302585; (* convert to log10 *)
    rDarcyFrictionFactor := 0.25 / MAX(0.00001, (rScratch3 * rScratch3));
    rDarcyFrictionFactor := MAX(0.008, MIN(0.060, rDarcyFrictionFactor));
ELSE
    (* Laminar boundary transition fallback *)
    rDarcyFrictionFactor := 64.0 / MAX(1.0, rReynoldsNumberSupply);
END_IF;

(* Boundary wall shear stress: tau_wall = 0.125 * f * rho * v^2 [Pa] *)
rWallShearStressPa := 0.125 * rDarcyFrictionFactor * rActiveFluidDensity * (rFlowVelocityMean * rFlowVelocityMean);

(* 3.4 Steam-In-Place (SIP) Logarithmic Lethality & Saturated Vapor Pressure Integration *)
(* Bigelow Thermal Death Model: L(T) = 10^((T - 121.11) / 10.0) *)
IF (rVotedColdSpotTemp > 100.0) THEN
    rScratch4 := (rVotedColdSpotTemp - rConst_SIP_RefTemp) / rConst_SIP_ZValue;
    (* Clamp exponent range between -4.0 and 2.5 for numerical stability *)
    rScratch4 := MAX(-4.0, MIN(2.5, rScratch4));
    rInstantaneousLethalRate := EXPT(10.0, rScratch4);
ELSE
    rInstantaneousLethalRate := 0.0;
END_IF;

(* Trapezoidal numerical integration of equivalent sterilization lethality F0 *)
IF (eCurrentState = 10) OR ((eCurrentState = 9) AND (rVotedColdSpotTemp >= 121.11)) THEN
    rScratch5 := 0.5 * (rInstantaneousLethalRate + rPrevLethalRate) * (rConst_ScanDeltaTime / 60.0);
    rAccumulatedF0Lethality := rAccumulatedF0Lethality + rScratch5;
END_IF;
rPrevLethalRate := rInstantaneousLethalRate;

(* Antoine Saturated Steam Vapor Pressure: P_sat [bar abs] = exp(11.6834 - 3816.44 / (T + 227.02)) *)
IF rVotedColdSpotTemp > 50.0 THEN
    rCalculatedSatVaporPress := EXP(11.6834 - (3816.44 / (rVotedColdSpotTemp + 227.02)));
ELSE
    rCalculatedSatVaporPress := 1.013;
END_IF;
""")

    # Phase 4: Extended Kalman Filter & State Propagation
    parts.append("""(* ============================================================================================= *)
(* SECTION 4: EXTENDED KALMAN FILTER (EKF) & STATE-SPACE PROPAGATION                            *)
(* ============================================================================================= *)
(* 4.1 Assemble Feedback Measurement Vector z[k] from Voted Telemetry *)
arrMeasurement_z[1] := rSupplyHeaderTemp;
arrMeasurement_z[2] := rSteamCondensateTemp;
arrMeasurement_z[3] := rReturnHeaderTemp;
arrMeasurement_z[4] := rVotedSupplyConductivity;
arrMeasurement_z[5] := rVotedReturnConductivity;
IF (eCurrentState = 2) OR (eCurrentState = 3) THEN
    arrMeasurement_z[6] := rCalculatedCausticPct;
ELSIF (eCurrentState = 5) OR (eCurrentState = 6) THEN
    arrMeasurement_z[6] := rCalculatedAcidPct;
ELSE
    arrMeasurement_z[6] := 0.0;
END_IF;
arrMeasurement_z[7] := rVotedSupplyFlow;
arrMeasurement_z[8] := rVotedReturnFlow;
arrMeasurement_z[9] := rActiveTankLevel;
arrMeasurement_z[10] := rVotedColdSpotTemp;

(* 4.2 Compute Kalman Innovation Residual: e[i] = z[i] - y_hat[i] *)
FOR nIdx_i := 1 TO 10 DO
    rScratch1 := 0.0;
    FOR nIdx_j := 1 TO 10 DO
        rScratch1 := rScratch1 + (arrC[nIdx_i, nIdx_j] * arrState_x[nIdx_j]);
    END_FOR;
    arrInnovation_e[nIdx_i] := arrMeasurement_z[nIdx_i] - rScratch1;
END_FOR;

(* 4.3 Measurement Correction Update: x_hat = x + K * e *)
FOR nIdx_i := 1 TO 10 DO
    rScratch2 := 0.0;
    FOR nIdx_j := 1 TO 10 DO
        rScratch2 := rScratch2 + (arrKalmanGain[nIdx_i, nIdx_j] * arrInnovation_e[nIdx_j]);
    END_FOR;
    arrState_x_hat[nIdx_i] := arrState_x[nIdx_i] + rScratch2;
END_FOR;

(* 4.4 Time Propagation / State-Space Prediction: x[k+1] = A * x_hat + B * u *)
FOR nIdx_i := 1 TO 10 DO
    rScratch3 := 0.0;
    FOR nIdx_j := 1 TO 10 DO
        rScratch3 := rScratch3 + (arrA[nIdx_i, nIdx_j] * arrState_x_hat[nIdx_j]);
    END_FOR;
    rScratch4 := 0.0;
    FOR nIdx_k := 1 TO 8 DO
        rScratch4 := rScratch4 + (arrB[nIdx_i, nIdx_k] * arrControl_u[nIdx_k]);
    END_FOR;
    arrState_x_next[nIdx_i] := rScratch3 + rScratch4;
    arrState_x[nIdx_i] := arrState_x_next[nIdx_i];
END_FOR;
""")

    # Phase 5: Receding-Horizon MPC Controller
    parts.append("""(* ============================================================================================= *)
(* SECTION 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZER                         *)
(* ============================================================================================= *)
(* 5.1 Set Reference Targets Based on Active Recipe Phase *)
CASE eCurrentState OF
    0: (* IDLE STANDBY *)
        arrStateRef[1] := 20.0;   (* Ambient temp *)
        arrStateRef[4] := 0.0;    (* No conductivity *)
        arrStateRef[6] := 0.0;    (* 0% chemical *)
        arrStateRef[7] := 0.0;    (* No delivery flow *)
        arrStateRef[8] := 0.0;    (* No return flow *)
        arrStateRef[9] := 1.20;   (* Target resting level *)
        arrStateRef[10] := 20.0;
    1: (* PRE-RINSE TO DRAIN *)
        arrStateRef[1] := 25.0;   (* Ambient deionized water flush *)
        arrStateRef[4] := 0.05;   (* Fresh rinse water *)
        arrStateRef[6] := 0.0;
        arrStateRef[7] := rTargetWashFlowRate; (* Maximum turbulent scouring flow *)
        arrStateRef[8] := rTargetWashFlowRate; (* Scavenge balance *)
        arrStateRef[9] := 1.50;
        arrStateRef[10] := 25.0;
    2: (* CAUSTIC HEATING & RECIRCULATION *)
        arrStateRef[1] := rTargetCausticTemp;     (* 85.0 C *)
        arrStateRef[4] := 68.5;                   (* Target ~2.5% NaOH conductivity *)
        arrStateRef[6] := rSelectedCausticTargetPct;
        arrStateRef[7] := rTargetWashFlowRate;
        arrStateRef[8] := rTargetWashFlowRate;
        arrStateRef[9] := 1.60;
        arrStateRef[10] := rTargetCausticTemp - 3.0;
    3: (* CAUSTIC RECOVERY *)
        arrStateRef[1] := rTargetCausticTemp;
        arrStateRef[4] := 68.5;
        arrStateRef[6] := rSelectedCausticTargetPct;
        arrStateRef[7] := rTargetWashFlowRate * 0.75; (* Slightly reduced push flow *)
        arrStateRef[8] := rTargetWashFlowRate * 0.75;
        arrStateRef[9] := 1.50;
        arrStateRef[10] := 80.0;
    4: (* INTERMEDIATE WATER RINSE *)
        arrStateRef[1] := 30.0;
        arrStateRef[4] := 0.02;   (* Purging chemical residual *)
        arrStateRef[6] := 0.0;
        arrStateRef[7] := rTargetWashFlowRate;
        arrStateRef[8] := rTargetWashFlowRate;
        arrStateRef[9] := 1.50;
        arrStateRef[10] := 30.0;
    5: (* ACID DESCALING CIRCULATION *)
        arrStateRef[1] := rTargetAcidTemp;        (* 65.0 C *)
        arrStateRef[4] := 45.2;                   (* Target ~1.2% HNO3 conductivity *)
        arrStateRef[6] := rSelectedAcidTargetPct;
        arrStateRef[7] := rTargetWashFlowRate;
        arrStateRef[8] := rTargetWashFlowRate;
        arrStateRef[9] := 1.60;
        arrStateRef[10] := rTargetAcidTemp - 2.0;
    6: (* ACID RECOVERY *)
        arrStateRef[1] := rTargetAcidTemp;
        arrStateRef[4] := 45.2;
        arrStateRef[6] := rSelectedAcidTargetPct;
        arrStateRef[7] := rTargetWashFlowRate * 0.75;
        arrStateRef[8] := rTargetWashFlowRate * 0.75;
        arrStateRef[9] := 1.50;
        arrStateRef[10] := 60.0;
    7: (* FINAL PURIFIED WFI RINSE *)
        arrStateRef[1] := 25.0;
        arrStateRef[4] := 0.0015; (* <= 1.5 uS/cm *)
        arrStateRef[6] := 0.0;
        arrStateRef[7] := rTargetWashFlowRate;
        arrStateRef[8] := rTargetWashFlowRate;
        arrStateRef[9] := 1.50;
        arrStateRef[10] := 25.0;
    8: (* SIP AIR PURGE VENTING *)
        arrStateRef[1] := 105.0;
        arrStateRef[7] := 0.0;    (* Pumps off during SIP *)
        arrStateRef[8] := 0.0;
        arrStateRef[10] := 102.0;
    9: (* PURE STEAM SUPERHEATING *)
        arrStateRef[1] := rTargetSIPTemp;
        arrStateRef[7] := 0.0;
        arrStateRef[8] := 0.0;
        arrStateRef[10] := rTargetSIPTemp;
    10: (* SIP HOLD & F0 ACCUMULATION *)
        arrStateRef[1] := rTargetSIPTemp;         (* 122.5 C *)
        arrStateRef[7] := 0.0;
        arrStateRef[8] := 0.0;
        arrStateRef[10] := rTargetSIPTemp;        (* 122.5 C at cold-spot *)
    11: (* STERILE AIR COOLING *)
        arrStateRef[1] := 30.0;
        arrStateRef[7] := 0.0;
        arrStateRef[8] := 0.0;
        arrStateRef[10] := 35.0;
    12: (* SYSTEM SANITIZED READY *)
        arrStateRef[1] := 22.0;
        arrStateRef[7] := 0.0;
        arrStateRef[8] := 0.0;
        arrStateRef[10] := 22.0;
    ELSE
        arrStateRef[1] := 20.0;
        arrStateRef[7] := 0.0;
        arrStateRef[8] := 0.0;
END_CASE;

(* 5.2 Receding-Horizon Gradient Descent Optimization Loop (Unrolled) *)
FOR nMpcLoop := 1 TO nMpcIterations DO
    (* Evaluate Gradient: nabla_J = R*u + Rd*(u - u_prev) + B^T * Q * (x_hat - x_ref) *)
    FOR nIdx_k := 1 TO 8 DO
        rScratch6 := 0.0;
        FOR nIdx_i := 1 TO 10 DO
            rScratch7 := arrState_x_hat[nIdx_i] - arrStateRef[nIdx_i];
            rScratch6 := rScratch6 + (arrB[nIdx_i, nIdx_k] * arrQ_MpcCost[nIdx_i] * rScratch7);
        END_FOR;
        
        arrMpcGradient[nIdx_k] := (arrR_MpcCost[nIdx_k] * arrControl_u[nIdx_k]) +
                                  (arrRd_MpcRateCost[nIdx_k] * (arrControl_u[nIdx_k] - arrControl_u_prev[nIdx_k])) +
                                  rScratch6;

        (* Candidate Control Input Update *)
        rScratch8 := arrControl_u[nIdx_k] - (rMpcLearningRate * arrMpcGradient[nIdx_k]);

        (* Slew Rate Clamping *)
        rScratch9 := rScratch8 - arrControl_u_prev[nIdx_k];
        rScratch9 := MAX(-arrDeltaU_Max[nIdx_k], MIN(arrDeltaU_Max[nIdx_k], rScratch9));
        rScratch8 := arrControl_u_prev[nIdx_k] + rScratch9;

        (* Saturation Bounds Clamping *)
        arrControl_u[nIdx_k] := MAX(arrU_LowerBound[nIdx_k], MIN(arrU_UpperBound[nIdx_k], rScratch8));
    END_FOR;
END_FOR;

(* 5.3 Special Cyber-Physical Protection Interlocks on Actuator Demands *)
(* Cavitation Avoidance: Throttle return pump if suction vacuum is deep *)
IF (rReturnSuctionPressure < rAlarmReturnPress_L) AND (arrControl_u[3] > 20.0) THEN
    arrControl_u[3] := MAX(15.0, arrControl_u[3] - 12.0);
END_IF;

(* Supply Pump Run-Dry Protection: Inhibit forward pump if tank level critical *)
IF (rActiveTankLevel < rAlarmTankLevel_L) THEN
    arrControl_u[2] := MIN(arrControl_u[2], 25.0);
END_IF;
IF (rActiveTankLevel < rAlarmTankLevel_LL) THEN
    arrControl_u[2] := 0.0;
END_IF;

(* Assign Modulated Control Commands to Outputs *)
rSteamModulatingValveCmd   := arrControl_u[1];
rSupplyPumpSpeedCmd        := arrControl_u[2];
rReturnScavengePumpSpeedCmd:= arrControl_u[3];
rCausticDosingPumpSpeedCmd := arrControl_u[4];
rAcidDosingPumpSpeedCmd    := arrControl_u[5];
rWfiInletValveCmd          := arrControl_u[6];
rReturnDivertValveCmd      := arrControl_u[7];
rPureSteamSIPValveCmd      := arrControl_u[8];
""")

    # Phase 6: 12-Stage Operational Finite State Machine
    parts.append("""(* ============================================================================================= *)
(* SECTION 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                    *)
(* ============================================================================================= *)
(* Abort Cycle Interlock *)
IF bAbortCycleCmd OR (NOT bMasterEnable) OR (NOT bEmergencyStop) OR bMasterFaultTrip THEN
    eCurrentState := 0;
    bCIPCycleRunning := FALSE;
    bStateFirstScan := TRUE;
END_IF;

CASE eCurrentState OF
    0: (* PHASE 0: IDLE STANDBY *)
        wSkidOperationalState := 16#0001;
        wFSM_CurrentPhase := 0;
        bCIPCycleRunning := FALSE;
        bSupplyPumpRunContactor := FALSE;
        bReturnPumpRunContactor := FALSE;
        bCausticDosingPumpRun := FALSE;
        bAcidDosingPumpRun := FALSE;
        bDrainDumpValveOpen := FALSE;
        bCausticRecoveryValveOpen := FALSE;
        bAcidRecoveryValveOpen := FALSE;
        bSteamTrapBlowdownValve := FALSE;
        bSterileBarrierAirSealValve := FALSE;
        rSterileAirCoolingValveCmd := 0.0;

        IF bStartCIPCycleCmd AND bMasterEnable AND bEmergencyStop AND (NOT bMasterFaultTrip) AND bSanitaryPipingInterlockClosed THEN
            eCurrentState := 1;
            bCIPCycleRunning := TRUE;
            bCIPCycleCompleted := FALSE;
            bSterilizationValidated := FALSE;
            tStateDwellTimer := 0.0;
            tTotalCycleTimer := 0.0;
            rAccumulatedF0Lethality := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    1: (* PHASE 1: PRE-RINSE TO DRAIN *)
        wSkidOperationalState := 16#0002;
        wFSM_CurrentPhase := 1;
        bSupplyPumpRunContactor := TRUE;
        bReturnPumpRunContactor := TRUE;
        bDrainDumpValveOpen := TRUE;       (* Gross organic soils flushed directly to trade waste *)
        bCausticRecoveryValveOpen := FALSE;
        bAcidRecoveryValveOpen := FALSE;
        bCausticDosingPumpRun := FALSE;
        bAcidDosingPumpRun := FALSE;
        bSteamTrapBlowdownValve := FALSE;
        bSterileBarrierAirSealValve := FALSE;

        tPreRinsePhaseTimer := tPreRinsePhaseTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tPreRinsePhaseTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_PreRinse - tPreRinsePhaseTimer);

        (* Advance when rinse time elapsed AND return water turbidity cleared < 8.0 NTU *)
        IF (tPreRinsePhaseTimer >= rTargetDuration_PreRinse) AND (rTurbidityReturn <= rAlarmTurbidity_High) THEN
            eCurrentState := 2;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    2: (* PHASE 2: CAUSTIC HEATING & RECIRCULATION *)
        wSkidOperationalState := 16#0004;
        wFSM_CurrentPhase := 2;
        bSupplyPumpRunContactor := TRUE;
        bReturnPumpRunContactor := TRUE;
        bDrainDumpValveOpen := FALSE;
        bCausticRecoveryValveOpen := FALSE;
        bAcidRecoveryValveOpen := FALSE;
        bCausticDosingPumpRun := TRUE;     (* 50% NaOH dosing enabled *)
        bAcidDosingPumpRun := FALSE;
        bSteamTrapBlowdownValve := FALSE;
        bSterileBarrierAirSealValve := FALSE;

        (* Dwell timer only advances once cleaning temperature >= (Target - 2.0 C) AND concentration in spec *)
        IF (rSupplyHeaderTemp >= (rTargetCausticTemp - 2.0)) AND 
           (rCalculatedCausticPct >= (rSelectedCausticTargetPct - 0.20)) THEN
            tCausticWashTimer := tCausticWashTimer + rConst_ScanDeltaTime;
        END_IF;
        tStateDwellTimer := tCausticWashTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_CausticWash - tCausticWashTimer);

        IF tCausticWashTimer >= rTargetDuration_CausticWash THEN
            eCurrentState := 3;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    3: (* PHASE 3: CAUSTIC RECOVERY *)
        wSkidOperationalState := 16#0008;
        wFSM_CurrentPhase := 3;
        bSupplyPumpRunContactor := TRUE;
        bReturnPumpRunContactor := TRUE;
        bCausticDosingPumpRun := FALSE;
        bAcidDosingPumpRun := FALSE;

        (* Smart Routing: Divert to Caustic Storage Tank while conductivity is high; dump tail to drain *)
        IF rCompensatedReturnCond25 >= 18.0 THEN
            bCausticRecoveryValveOpen := TRUE;
            bDrainDumpValveOpen := FALSE;
        ELSE
            bCausticRecoveryValveOpen := FALSE;
            bDrainDumpValveOpen := TRUE;
        END_IF;

        tCausticRecovTimer := tCausticRecovTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tCausticRecovTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_CausticRecov - tCausticRecovTimer);

        IF (tCausticRecovTimer >= rTargetDuration_CausticRecov) OR (rCompensatedReturnCond25 < 3.0) THEN
            eCurrentState := 4;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    4: (* PHASE 4: INTERMEDIATE WATER RINSE *)
        wSkidOperationalState := 16#0010;
        wFSM_CurrentPhase := 4;
        bSupplyPumpRunContactor := TRUE;
        bReturnPumpRunContactor := TRUE;
        bDrainDumpValveOpen := TRUE;       (* Flush caustic residues directly to drain *)
        bCausticRecoveryValveOpen := FALSE;
        bAcidRecoveryValveOpen := FALSE;
        bCausticDosingPumpRun := FALSE;
        bAcidDosingPumpRun := FALSE;

        tInterRinseTimer := tInterRinseTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tInterRinseTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_InterRinse - tInterRinseTimer);

        (* Advance when conductivity drops below 0.35 mS/cm and time satisfied *)
        IF (tInterRinseTimer >= rTargetDuration_InterRinse) AND (rCompensatedReturnCond25 <= 0.35) THEN
            eCurrentState := 5;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    5: (* PHASE 5: ACID DESCALING CIRCULATION *)
        wSkidOperationalState := 16#0020;
        wFSM_CurrentPhase := 5;
        bSupplyPumpRunContactor := TRUE;
        bReturnPumpRunContactor := TRUE;
        bDrainDumpValveOpen := FALSE;
        bCausticRecoveryValveOpen := FALSE;
        bAcidRecoveryValveOpen := FALSE;
        bCausticDosingPumpRun := FALSE;
        bAcidDosingPumpRun := TRUE;        (* 60% HNO3 dosing enabled *)

        IF (rSupplyHeaderTemp >= (rTargetAcidTemp - 2.0)) AND 
           (rCalculatedAcidPct >= (rSelectedAcidTargetPct - 0.15)) THEN
            tAcidWashTimer := tAcidWashTimer + rConst_ScanDeltaTime;
        END_IF;
        tStateDwellTimer := tAcidWashTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_AcidWash - tAcidWashTimer);

        IF tAcidWashTimer >= rTargetDuration_AcidWash THEN
            eCurrentState := 6;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    6: (* PHASE 6: ACID RECOVERY *)
        wSkidOperationalState := 16#0040;
        wFSM_CurrentPhase := 6;
        bSupplyPumpRunContactor := TRUE;
        bReturnPumpRunContactor := TRUE;
        bCausticDosingPumpRun := FALSE;
        bAcidDosingPumpRun := FALSE;

        (* Divert to Acid Tank while return concentration is high; purge tail to neutralization drain *)
        IF rCompensatedReturnCond25 >= 12.0 THEN
            bAcidRecoveryValveOpen := TRUE;
            bDrainDumpValveOpen := FALSE;
        ELSE
            bAcidRecoveryValveOpen := FALSE;
            bDrainDumpValveOpen := TRUE;
        END_IF;

        tAcidRecovTimer := tAcidRecovTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tAcidRecovTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_AcidRecov - tAcidRecovTimer);

        IF (tAcidRecovTimer >= rTargetDuration_AcidRecov) OR (rCompensatedReturnCond25 < 1.5) THEN
            eCurrentState := 7;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    7: (* PHASE 7: FINAL PURIFIED WFI RINSE *)
        wSkidOperationalState := 16#0080;
        wFSM_CurrentPhase := 7;
        bSupplyPumpRunContactor := TRUE;
        bReturnPumpRunContactor := TRUE;
        bDrainDumpValveOpen := TRUE;
        bCausticRecoveryValveOpen := FALSE;
        bAcidRecoveryValveOpen := FALSE;
        bCausticDosingPumpRun := FALSE;
        bAcidDosingPumpRun := FALSE;

        tFinalRinseTimer := tFinalRinseTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tFinalRinseTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_FinalRinse - tFinalRinseTimer);

        (* Advance when return conductivity <= 2.5 uS/cm (0.0025 mS/cm) and minimum rinse elapsed *)
        IF (tFinalRinseTimer >= rTargetDuration_FinalRinse) AND 
           (rCompensatedReturnCond25 <= rAlarmFinalWfi_ConductivityMax) THEN
            eCurrentState := 8;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    8: (* PHASE 8: STEAM-IN-PLACE (SIP) AIR PURGE *)
        wSkidOperationalState := 16#0100;
        wFSM_CurrentPhase := 8;
        bSupplyPumpRunContactor := FALSE;  (* Pumps stopped for steam blow *)
        bReturnPumpRunContactor := FALSE;
        bDrainDumpValveOpen := FALSE;
        bSteamTrapBlowdownValve := TRUE;   (* Bypass open to rapidly evacuate air and condensate *)
        bSterileBarrierAirSealValve := FALSE;

        tSIPAirPurgeTimer := tSIPAirPurgeTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tSIPAirPurgeTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_SIPAirPurge - tSIPAirPurgeTimer);

        (* Once air displaced and cold spot reaches 100.0 C, close blowdown trap and ramp steam *)
        IF (tSIPAirPurgeTimer >= rTargetDuration_SIPAirPurge) AND (rVotedColdSpotTemp >= 100.0) THEN
            bSteamTrapBlowdownValve := FALSE;
            eCurrentState := 9;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    9: (* PHASE 9: PURE STEAM SUPERHEATING *)
        wSkidOperationalState := 16#0200;
        wFSM_CurrentPhase := 9;
        bSupplyPumpRunContactor := FALSE;
        bReturnPumpRunContactor := FALSE;
        bSteamTrapBlowdownValve := FALSE;
        bSterileBarrierAirSealValve := FALSE;

        tSIPHeatUpTimer := tSIPHeatUpTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tSIPHeatUpTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_SIPHeatUp - tSIPHeatUpTimer);

        (* Advance when all voted cold spot sensors reach reference sterilization temperature *)
        IF (rVotedColdSpotTemp >= rConst_SIP_RefTemp) THEN
            eCurrentState := 10;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    10: (* PHASE 10: SIP TEMPERATURE HOLD & F0 ACCUMULATION *)
        wSkidOperationalState := 16#0400;
        wFSM_CurrentPhase := 10;
        bSupplyPumpRunContactor := FALSE;
        bReturnPumpRunContactor := FALSE;
        bSteamTrapBlowdownValve := FALSE;
        bSterileBarrierAirSealValve := FALSE;

        tSIPHoldTimer := tSIPHoldTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tSIPHoldTimer;
        
        (* Estimate remaining time based on current lethal rate *)
        IF rInstantaneousLethalRate > 0.05 THEN
            rPhaseRemainingTimeSec := MAX(0.0, (rTargetF0LethalityMin - rAccumulatedF0Lethality) / rInstantaneousLethalRate * 60.0);
        ELSE
            rPhaseRemainingTimeSec := 999.0;
        END_IF;

        (* Advance when target F0 lethality reached (nominally >= 30.0 min) *)
        IF (rAccumulatedF0Lethality >= rTargetF0LethalityMin) THEN
            bSterilizationValidated := TRUE;
            eCurrentState := 11;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    11: (* PHASE 11: STERILE AIR OVERPRESSURE COOLING *)
        wSkidOperationalState := 16#0800;
        wFSM_CurrentPhase := 11;
        bSupplyPumpRunContactor := FALSE;
        bReturnPumpRunContactor := FALSE;
        bSterileBarrierAirSealValve := TRUE; (* Positive pressure air blanket injected *)
        rSterileAirCoolingValveCmd := 65.0;  (* Maintain 1.50 bar overpressure preventing vacuum collapse *)

        tSIPCooldownTimer := tSIPCooldownTimer + rConst_ScanDeltaTime;
        tStateDwellTimer := tSIPCooldownTimer;
        rPhaseRemainingTimeSec := MAX(0.0, rTargetDuration_SIPCooling - tSIPCooldownTimer);

        (* Advance when cold spot cooled down below 38.0 deg C under sterile air blanket *)
        IF (tSIPCooldownTimer >= rTargetDuration_SIPCooling) OR (rVotedColdSpotTemp <= 38.0) THEN
            eCurrentState := 12;
            tStateDwellTimer := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

    12: (* PHASE 12: SYSTEM SANITIZED READY *)
        wSkidOperationalState := 16#1000;
        wFSM_CurrentPhase := 12;
        bCIPCycleRunning := FALSE;
        bCIPCycleCompleted := TRUE;
        bSterileBarrierAirSealValve := TRUE; (* Maintain sterile air seal barrier *)
        rSterileAirCoolingValveCmd := 15.0;  (* Low maintenance trickle overpressure *)
        nTotalBatchesCompleted := nTotalBatchesCompleted + 1;
        rPhaseRemainingTimeSec := 0.0;

    ELSE
        (* Fail-safe fallback *)
        eCurrentState := 0;
        bCIPCycleRunning := FALSE;
        bSupplyPumpRunContactor := FALSE;
        bReturnPumpRunContactor := FALSE;
END_CASE;

(* Accumulate Total Batch Runtime *)
IF bCIPCycleRunning THEN
    tTotalCycleTimer := tTotalCycleTimer + rConst_ScanDeltaTime;
END_IF;
rCycleElapsedTimeSec := tTotalCycleTimer;
""")

    # Phase 7: ISA-18.2 Alarms & Bit-Packing
    parts.append("""(* ============================================================================================= *)
(* SECTION 7: ISA-18.2 MULTI-TIERED ALARM EVALUATION & TELEMETRY REGISTERS                      *)
(* ============================================================================================= *)
(* 7.1 Priority 1: Critical Emergency Trips (Shutdown Skid Actuators) *)
(* Trip 0: Emergency Stop Pressed *)
IF NOT bEmergencyStop THEN
    dwAlarmWord_Trips.0 := TRUE;
ELSIF bAcknowledgeAlarms THEN
    dwAlarmWord_Trips.0 := FALSE;
END_IF;

(* Trip 1: High-High Pressure Steam Blowout (P_sup >= 6.50 bar) *)
IF (rSupplyPressure >= rAlarmSupplyPress_HH) THEN
    dwAlarmWord_Trips.1 := TRUE;
ELSIF (rSupplyPressure <= (rAlarmSupplyPress_HH - rDeadband_Press)) AND bAcknowledgeAlarms THEN
    dwAlarmWord_Trips.1 := FALSE;
END_IF;

(* Trip 2: High-High Thermal Runaway Over-temperature (T_sup >= 138.0 C) *)
IF (rSupplyHeaderTemp >= rAlarmTemp_HH) THEN
    dwAlarmWord_Trips.2 := TRUE;
ELSIF (rSupplyHeaderTemp <= (rAlarmTemp_HH - rDeadband_Temp)) AND bAcknowledgeAlarms THEN
    dwAlarmWord_Trips.2 := FALSE;
END_IF;

(* Trip 3: Buffer Tank High-High Overfill (H_tank >= 2.85 m) *)
IF (rActiveTankLevel >= rAlarmTankLevel_HH) THEN
    dwAlarmWord_Trips.3 := TRUE;
ELSIF (rActiveTankLevel <= (rAlarmTankLevel_HH - rDeadband_TankLevel)) AND bAcknowledgeAlarms THEN
    dwAlarmWord_Trips.3 := FALSE;
END_IF;

(* Trip 4: Supply Pump Seal Run-Dry Cavitation (H_tank <= 0.20 m AND Pump Running) *)
IF (rActiveTankLevel <= rAlarmTankLevel_LL) AND bSupplyPumpRunContactor THEN
    dwAlarmWord_Trips.4 := TRUE;
ELSIF (rActiveTankLevel >= (rAlarmTankLevel_LL + rDeadband_TankLevel)) AND bAcknowledgeAlarms THEN
    dwAlarmWord_Trips.4 := FALSE;
END_IF;

(* Trip 5: Scavenge Return Pump Deep Vacuum Cavitation (P_ret <= 0.08 bar AND Pump Running) *)
IF (rReturnSuctionPressure <= rAlarmReturnPress_LL) AND bReturnPumpRunContactor THEN
    dwAlarmWord_Trips.5 := TRUE;
ELSIF (rReturnSuctionPressure >= (rAlarmReturnPress_LL + rDeadband_ReturnPress)) AND bAcknowledgeAlarms THEN
    dwAlarmWord_Trips.5 := FALSE;
END_IF;

(* Trip 6: Flow Scouring Loss in High-Velocity Wash Phase (Q_sup <= 2.50 m3/h) *)
IF ((eCurrentState = 2) OR (eCurrentState = 5)) AND (rVotedSupplyFlow <= 2.50) AND (tStateDwellTimer > 15.0) THEN
    dwAlarmWord_Trips.6 := TRUE;
ELSIF (rVotedSupplyFlow >= 5.0) AND bAcknowledgeAlarms THEN
    dwAlarmWord_Trips.6 := FALSE;
END_IF;

(* Trip 7: Dual 2oo3 TMR Channel Failure (Total Loss of Redundancy) *)
IF ((NOT bSupplyCond_ChA_Valid) AND (NOT bSupplyCond_ChB_Valid)) OR
   ((NOT bSupplyCond_ChA_Valid) AND (NOT bSupplyCond_ChC_Valid)) OR
   ((NOT bSupplyCond_ChB_Valid) AND (NOT bSupplyCond_ChC_Valid)) OR
   ((NOT bColdSpotTemp_ChA_Valid) AND (NOT bColdSpotTemp_ChB_Valid)) OR
   ((NOT bColdSpotTemp_ChA_Valid) AND (NOT bColdSpotTemp_ChC_Valid)) OR
   ((NOT bColdSpotTemp_ChB_Valid) AND (NOT bColdSpotTemp_ChC_Valid)) THEN
    dwAlarmWord_Trips.7 := TRUE;
ELSIF bAcknowledgeAlarms THEN
    dwAlarmWord_Trips.7 := FALSE;
END_IF;

(* 7.2 Priority 2: Severe Process Deviation Alarms *)
(* Severe 0: Caustic Concentration Low Deviation *)
IF (eCurrentState = 2) AND (tCausticWashTimer > 60.0) AND 
   (rCalculatedCausticPct < (rSelectedCausticTargetPct - rAlarmCausticConc_DevLimit)) THEN
    dwAlarmWord_Severe.0 := TRUE;
ELSIF (rCalculatedCausticPct >= (rSelectedCausticTargetPct - 0.10)) OR (eCurrentState <> 2) THEN
    dwAlarmWord_Severe.0 := FALSE;
END_IF;

(* Severe 1: Caustic Concentration High Deviation *)
IF (eCurrentState = 2) AND 
   (rCalculatedCausticPct > (rSelectedCausticTargetPct + rAlarmCausticConc_DevLimit)) THEN
    dwAlarmWord_Severe.1 := TRUE;
ELSIF (rCalculatedCausticPct <= (rSelectedCausticTargetPct + 0.10)) OR (eCurrentState <> 2) THEN
    dwAlarmWord_Severe.1 := FALSE;
END_IF;

(* Severe 2: Acid Concentration Low Deviation *)
IF (eCurrentState = 5) AND (tAcidWashTimer > 60.0) AND 
   (rCalculatedAcidPct < (rSelectedAcidTargetPct - rAlarmAcidConc_DevLimit)) THEN
    dwAlarmWord_Severe.2 := TRUE;
ELSIF (rCalculatedAcidPct >= (rSelectedAcidTargetPct - 0.08)) OR (eCurrentState <> 5) THEN
    dwAlarmWord_Severe.2 := FALSE;
END_IF;

(* Severe 3: Acid Concentration High Deviation *)
IF (eCurrentState = 5) AND 
   (rCalculatedAcidPct > (rSelectedAcidTargetPct + rAlarmAcidConc_DevLimit)) THEN
    dwAlarmWord_Severe.3 := TRUE;
ELSIF (rCalculatedAcidPct <= (rSelectedAcidTargetPct + 0.08)) OR (eCurrentState <> 5) THEN
    dwAlarmWord_Severe.3 := FALSE;
END_IF;

(* Severe 4: Reynolds Number Scouring Flow Velocity Warning (Re < 150,000 during wash) *)
IF ((eCurrentState = 2) OR (eCurrentState = 5)) AND (rReynoldsNumberSupply < 150000.0) AND (tStateDwellTimer > 20.0) THEN
    dwAlarmWord_Severe.4 := TRUE;
ELSIF (rReynoldsNumberSupply >= rConst_MinTurbulentReynolds) OR ((eCurrentState <> 2) AND (eCurrentState <> 5)) THEN
    dwAlarmWord_Severe.4 := FALSE;
END_IF;

(* Severe 5: Low Wash Supply Temperature *)
IF (eCurrentState = 2) AND (tCausticWashTimer > 45.0) AND (rSupplyHeaderTemp < (rTargetCausticTemp - 5.0)) THEN
    dwAlarmWord_Severe.5 := TRUE;
ELSIF (rSupplyHeaderTemp >= (rTargetCausticTemp - 1.5)) OR (eCurrentState <> 2) THEN
    dwAlarmWord_Severe.5 := FALSE;
END_IF;

(* Severe 6: Cold-Spot Temperature Drop During SIP Sterilization Hold *)
IF (eCurrentState = 10) AND (rVotedColdSpotTemp < rAlarmColdSpot_HoldLL) THEN
    dwAlarmWord_Severe.6 := TRUE;
ELSIF (rVotedColdSpotTemp >= (rAlarmColdSpot_HoldLL + 0.50)) OR (eCurrentState <> 10) THEN
    dwAlarmWord_Severe.6 := FALSE;
END_IF;

(* Severe 7: SIP Lethality Accumulation Stall Warning (L < 0.50 min/min during hold) *)
IF (eCurrentState = 10) AND (rInstantaneousLethalRate < 0.50) THEN
    dwAlarmWord_Severe.7 := TRUE;
ELSIF (rInstantaneousLethalRate >= 0.85) OR (eCurrentState <> 10) THEN
    dwAlarmWord_Severe.7 := FALSE;
END_IF;

(* 7.3 Priority 3: Advisory & Sensor Drift Warnings *)
dwAlarmWord_Warning.0 := NOT bSupplyCond_ChA_Valid;
dwAlarmWord_Warning.1 := NOT bSupplyCond_ChB_Valid;
dwAlarmWord_Warning.2 := NOT bSupplyCond_ChC_Valid;
dwAlarmWord_Warning.3 := NOT bReturnCond_ChA_Valid;
dwAlarmWord_Warning.4 := NOT bReturnCond_ChB_Valid;
dwAlarmWord_Warning.5 := NOT bReturnCond_ChC_Valid;
dwAlarmWord_Warning.6 := NOT bSupplyFlow_ChA_Valid;
dwAlarmWord_Warning.7 := NOT bSupplyFlow_ChB_Valid;
dwAlarmWord_Warning.8 := NOT bSupplyFlow_ChC_Valid;
dwAlarmWord_Warning.9 := NOT bReturnFlow_ChA_Valid;
dwAlarmWord_Warning.10 := NOT bReturnFlow_ChB_Valid;
dwAlarmWord_Warning.11 := NOT bReturnFlow_ChC_Valid;
dwAlarmWord_Warning.12 := NOT bColdSpotTemp_ChA_Valid;
dwAlarmWord_Warning.13 := NOT bColdSpotTemp_ChB_Valid;
dwAlarmWord_Warning.14 := NOT bColdSpotTemp_ChC_Valid;

(* Warning 15: Saturated Steam Vapor Pressure Deviation (Air Pocket Detection) *)
IF (eCurrentState = 9) OR (eCurrentState = 10) THEN
    IF ABS(rSteamSupplyPressure - rCalculatedSatVaporPress) > rAlarmSIP_PressureVaporDiffMax THEN
        dwAlarmWord_Warning.15 := TRUE;
    ELSE
        dwAlarmWord_Warning.15 := FALSE;
    END_IF;
ELSE
    dwAlarmWord_Warning.15 := FALSE;
END_IF;

(* Master Fault Latching & Acoustic/Visual Strobe Activation *)
bMasterFaultTrip := (dwAlarmWord_Trips <> 16#00000000);
bAudibleVisualAlarmStrobe := bMasterFaultTrip OR (dwAlarmWord_Severe <> 16#00000000);

(* 7.4 Housekeeping: Store Previous Commands *)
FOR nIdx_k := 1 TO 8 DO
    arrControl_u_prev[nIdx_k] := arrControl_u[nIdx_k];
END_FOR;

END_FUNCTION_BLOCK
""")

    code = "".join(parts)
    return code

if __name__ == "__main__":
    code = generate_iec_st()
    print(f"Generated code length: {len(code)} characters")
    
    # Check parity and lines
    lines = code.splitlines()
    print(f"First line: {lines[0]}")
    print(f"Last line: {lines[-1]}")
    
    # Save to file
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Food & Beverage Processing: Multi-Loop Continuous Caustic & Acid Clean-In-Place / Steam-In-Place (CIP/SIP) Skid with Dual Conductivity & F0 Lethality Integration**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_FoodBev_CIP_SIP_MultiLoopSanitization_Skid
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [deg C], [m3/h], [mS/cm], [%], [l/h], [min], [rpm], [Pa], [NTU])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR, WHILE and END_WHILE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_FoodBev_CIP_SIP_MultiLoopSanitization_Skid
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_e419b02a.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Food & Beverage Processing: Multi-Loop Continuous Caustic & Acid Clean-In-Place / Steam-In-Place (CIP/SIP) Skid with Dual Conductivity & F0 Lethality Integration"""

    full_content = f"```iec-st\n{code}\n```"
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_content}
        ]
    }
    
    out_path = "data/swarm_raw/agent_e419b02a.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved to {out_path}")
