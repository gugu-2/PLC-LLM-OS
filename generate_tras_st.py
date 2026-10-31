# generate_tras_st.py
# High-density IEC 61131-3 generator for FB_Aerospace_JetEngine_HydraulicTRAS_LockSync
import os
import sys

def build_tras_block():
    sections = []

    # -------------------------------------------------------------------------
    # SECTION 1: HEADER & DECLARATION
    # -------------------------------------------------------------------------
    s1 = """FUNCTION_BLOCK FB_Aerospace_JetEngine_HydraulicTRAS_LockSync
(*
====================================================================================================
  LUMINA ADVANCED CYBER-PHYSICAL CONTROL SYSTEMS - SYNTHETIC IEC 61131-3 DATA ARCHITECTURE
  SYSTEM IDENTIFIER: AERO-PROP-TRAS-LOCKSYNC-FADEC-REV9.4
  CORE DOMAIN:
    Commercial Aircraft Jet Engine Hydraulic Thrust Reverser Actuation System (TRAS) with
    Multi-Sleeve Mechanical Synchronizer, Tertiary Lock Solenoids & Feedback LVDTs.
  STANDARDS & REGULATORY COMPLIANCE:
    - 14 CFR FAR § 25.933 (Reversing Systems Safety & In-Flight Uncommanded Deployment Mitigation)
    - RTCA DO-178C / EUROCAE ED-12C Software Considerations in Airborne Systems (Design Assurance Level A)
    - RTCA DO-254 / EUROCAE ED-80 Design Assurance Guidance for Airborne Electronic Hardware (DAL A)
    - RTCA DO-160G Environmental Conditions and Test Procedures for Airborne Equipment (Cat. A4, Thermal -55°C to +125°C)
    - SAE ARP4754A Guidelines for Development of Civil Aircraft and Systems
    - SAE ARP4761 Guidelines and Methods for Conducting the Safety Assessment Process on Civil Airborne Systems
    - SAE AS94900 Aerospace - Flight Control Systems - Design, Installation and Test of Piloted Aircraft, General Specification For
    - ISO 13849-1 / IEC 61508 / IEC 61511 Functional Safety of Safety-Related Embedded Architectures
    - ISA-18.2 / EEMUA 191 Management of Alarm Systems for the Process Industries & Aviation FADEC Fault Matrices
  ARCHITECT:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Veteran Experience)
----------------------------------------------------------------------------------------------------
  AEROSPACE PROPULSION & HYDRAULIC ACTUATION PHYSICAL THEORY:
    A modern high-bypass commercial turbofan engine (e.g. 70,000 to 115,000 lbf thrust class) utilizes
    a cascade-type cold stream thrust reverser. The reverser structure comprises two translating
    cowls (transcowls) located on the upper and lower nacelle halves (or left and right halves).
    During landing rollout, these transcowls translate aft by approximately 580 mm, deploying blocker
    doors into the fan bypass duct to redirect thousands of pounds of bypass airflow through fixed
    turning cascades in a forward-diagonal vector, thereby producing aerodynamic reverse thrust.

    1. Catastrophic Hazard of In-Flight Deployment (FAR § 25.933):
       Uncommanded deployment of a thrust reverser in flight creates massive asymmetric drag and pitching
       moments that exceed aerodynamic flight control authority, representing an extremely catastrophic
       failure condition (allowable probability < 1E-9 per flight hour). Therefore, the TRAS actuation
       architecture incorporates three independent, dissimilar mechanical locking barriers:
       a) Primary Track Locks (PL): Over-center mechanical latches integrated within the upper track beam.
       b) Secondary Lock (SL): Bi-directional hydraulic actuator internal locking detents.
       c) Tertiary Lock (TL): Solenoid-operated spring-loaded mechanical shear pin locking directly into
          the transcowl sync shaft or track structure, controlled by an independent electrical circuit
          interlocked with dual-dissimilar Weight-on-Wheels (WOW) squat switches, aircraft radio altimeter,
          and Throttle Resolver Angle (TRA) forward/reverse detent gates.

    2. Skydrol LD-4 Aviation Phosphate Ester Hydraulic Fluid Compressibility & Bulk Modulus:
       Commercial aircraft hydraulic systems operate at nominal 207 bar (3000 psi) or 345 bar (5000 psi).
       Phosphate ester fluids (Type IV / Type V, e.g., Skydrol LD-4, HyJet IV-Aplus) undergo dramatic
       variations in kinematic viscosity (nu = 1500 cSt at -40°C down to 3.8 cSt at +100°C) and isothermal
       bulk modulus (Beta = 1850 MPa at 0°C down to 1050 MPa at 120°C). Furthermore, undissolved air
       entrainment (0.2% to 1.5% by volume) drastically collapses the effective bulk modulus Beta_eff
       at low pressures:
         Beta_eff(T, P) = Beta_liquid(T) / [ 1 + (V_g0 / V_0) * (P_0 / P)^(1/gamma) * (Beta_liquid(T) / (gamma * P)) ]
       This pressure-dependent elasticity governs the hydraulic natural frequency omega_h = sqrt(4*Beta_eff*A_p^2 / (V_t*M))
       and introduces severe hydraulic water hammer pressure transients during high-speed valve stroking.

    3. Multi-Sleeve Mechanical Synchronizer & Flexible Sync Shaft Torsional Dynamics:
       The upper and lower translating sleeves are actuated by dedicated hydraulic linear cylinders equipped
       with internal ball screws. To prevent aerodynamic skewing (where one cowl travels faster than the
       other, causing catastrophic track binding, roller jamming, and cowl blow-off), a flexible
       synchronization shaft (sync shaft) connects the upper and lower actuator drive pinions via 90-degree
       bevel gearboxes. The sync shaft acts as a torsional spring-damper:
         tau_sync = K_sync * (theta_upper - theta_lower) + C_sync * (d_theta_upper/dt - d_theta_lower/dt)
       If the mechanical skew error epsilon_skew = x_upper - x_lower exceeds 3.5 mm, high mechanical binding
       forces induce excessive sync shaft torque. If skew exceeds 5.8 mm, the system must immediately abort
       deployment and engage fail-safe hydraulic damping before sync shaft shear pins fail at 280 Nm.

    4. Multi-State Model Predictive Control (MPC) and Dual-Observer Architecture:
       A continuous-to-discrete 8x8 state-space model running at Ts = 10 ms (100 Hz deterministic avionics task)
       propagates sleeve positions, velocities, actuator chamber differential pressures, sync shaft twist angle,
       and unmeasured aerodynamic disturbance forces. A constrained quadratic cost formulation balances
       actuator translation speed against dynamic skew suppression, while 2oo3 Triple Modular Redundancy (TMR)
       voting across dual-channel LVDTs, pressure transducers, and proximity switches provides instantaneous
       fault isolation and bumpless degradation.
====================================================================================================
*)

VAR_INPUT
    (* ========================================================================================= *)
    (* PRIMARY AVIONICS & TRAS TRANSDUCER TELEMETRY (STRONGLY TYPED PHYSICAL INPUTS)             *)
    (* ========================================================================================= *)
    (* 2oo3 Redundant Aircraft Main Hydraulic Supply Pressure Triplet [bar] *)
    rHydSupplyPress_bar_A       : REAL := 206.84;   (* Channel A piezoresistive supply rail pressure [bar] *)
    rHydSupplyPress_bar_B       : REAL := 206.84;   (* Channel B piezoresistive supply rail pressure [bar] *)
    rHydSupplyPress_bar_C       : REAL := 206.84;   (* Channel C piezoresistive supply rail pressure [bar] *)

    (* 2oo3 Redundant Aircraft Main Hydraulic Return Pressure Triplet [bar] *)
    rHydReturnPress_bar_A       : REAL := 3.45;     (* Channel A return line backpressure [bar] *)
    rHydReturnPress_bar_B       : REAL := 3.45;     (* Channel B return line backpressure [bar] *)
    rHydReturnPress_bar_C       : REAL := 3.45;     (* Channel C return line backpressure [bar] *)

    (* 2oo3 Redundant Upper Transcowl Linear Variable Differential Transformer (LVDT) Triplet [mm] *)
    rUpperLVDT_Pos_mm_A         : REAL := 0.00;     (* Channel A Upper sleeve high-precision LVDT position [mm] *)
    rUpperLVDT_Pos_mm_B         : REAL := 0.00;     (* Channel B Upper sleeve high-precision LVDT position [mm] *)
    rUpperLVDT_Pos_mm_C         : REAL := 0.00;     (* Channel C Upper sleeve high-precision LVDT position [mm] *)

    (* 2oo3 Redundant Lower Transcowl Linear Variable Differential Transformer (LVDT) Triplet [mm] *)
    rLowerLVDT_Pos_mm_A         : REAL := 0.00;     (* Channel A Lower sleeve high-precision LVDT position [mm] *)
    rLowerLVDT_Pos_mm_B         : REAL := 0.00;     (* Channel B Lower sleeve high-precision LVDT position [mm] *)
    rLowerLVDT_Pos_mm_C         : REAL := 0.00;     (* Channel C Lower sleeve high-precision LVDT position [mm] *)

    (* Hydraulic Fluid Thermodynamic & Environmental Telemetry *)
    rHydFluidTemp_degC          : REAL := 45.0;     (* Skydrol LD-4 bulk reservoir fluid temperature [deg C] *)
    rEngineFanBypassPress_bar   : REAL := 1.85;     (* Turbofan cold-stream bypass plenum total pressure [bar] *)
    rAircraftAirspeed_kts       : REAL := 132.5;    (* Indicated true airspeed from Air Data Inertial Reference Unit [kts] *)
    rThrottleReverseAngle_deg   : REAL := 0.00;     (* Cockpit Thrust Lever Angle (TRA) resolver feedback [deg] *)

    (* Aircraft Flight Deck, Landing Gear & Safety Critical Discrete Interlocks *)
    bWOW_Channel_A              : BOOL := FALSE;    (* Left Main Landing Gear Weight-On-Wheels squat switch *)
    bWOW_Channel_B              : BOOL := FALSE;    (* Right Main Landing Gear Weight-On-Wheels squat switch *)
    bWOW_Channel_C              : BOOL := FALSE;    (* Nose Landing Gear Weight-On-Wheels squat switch *)
    bTertiaryLockPin_Seat_A     : BOOL := TRUE;     (* Channel A inductive proximity: Tertiary Lock pin seated/locked *)
    bTertiaryLockPin_Seat_B     : BOOL := TRUE;     (* Channel B inductive proximity: Tertiary Lock pin seated/locked *)
    bTertiaryLockPin_Seat_C     : BOOL := TRUE;     (* Channel C inductive proximity: Tertiary Lock pin seated/locked *)
    bPrimaryLockLatch_A         : BOOL := TRUE;     (* Channel A Upper beam primary over-center latch seated *)
    bPrimaryLockLatch_B         : BOOL := TRUE;     (* Channel B Upper beam primary over-center latch seated *)
    bPrimaryLockLatch_C         : BOOL := TRUE;     (* Channel C Lower beam primary over-center latch seated *)
    bReverseThrustCommand       : BOOL := FALSE;    (* Cockpit FADEC reverse thrust deploy discrete command *)
    bEmergencyStowOverride     : BOOL := FALSE;    (* Cockpit emergency hardwired direct restow command *)
    bMasterResetAlarms          : BOOL := FALSE;    (* Flight deck / maintenance diagnostic fault reset *)
    bEnable                     : BOOL := TRUE;     (* Master electronic actuator controller execution enable *)
    tScanTime_s                 : REAL := 0.010;    (* Avionics deterministic cycle period [s] (100 Hz execution) *)
END_VAR
"""
    sections.append(s1)

    # -------------------------------------------------------------------------
    # SECTION 2: VAR_OUTPUT & VAR
    # -------------------------------------------------------------------------
    s2 = """VAR_OUTPUT
    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS, SERVO DRIVES & ENGINEERING TELEMETRY (STRONGLY TYPED PHYSICAL OUTPUTS) *)
    (* ========================================================================================= *)
    rEHSV_CurrentCmd_mA         : REAL := 0.00;     (* Electrohydraulic Servo Valve bipolar coil drive current [mA] *)
    rDeployIsolationValve_Pct   : REAL := 0.00;     (* Hydraulic Supply Isolation Valve (IV) pilot command [%] *)
    rDirectionalValve_Pct       : REAL := 50.00;    (* 4-Way 3-Position Directional Control Valve (DCV) cmd [%] *)
    bTertiaryLockSolenoidCmd    : BOOL := FALSE;    (* Dual-coil 28VDC tertiary lock pin release solenoid power *)
    rMeanCowlStroke_mm          : REAL := 0.00;     (* Voted mean translatory cowl displacement [mm] *)
    rCowlSkewDeviation_mm       : REAL := 0.00;     (* Instantaneous sleeve mechanical skew error: Upper - Lower [mm] *)
    rSyncShaftTorqueEst_Nm      : REAL := 0.00;     (* Observer estimated dynamic torsional load on sync shaft [Nm] *)
    rEffectiveBulkModulus_MPa   : REAL := 1420.0;   (* Skydrol LD-4 temperature & pressure compensated bulk modulus [MPa] *)
    rAerodynamicDragLoad_kN     : REAL := 0.00;     (* Calculated aerodynamic retarding force acting on transcowls [kN] *)
    rActuatorVelocity_mms       : REAL := 0.00;     (* Differentiated mean transcowl translation rate [mm/s] *)
    rHydraulicSupplyFlow_Lmin   : REAL := 0.00;     (* Calculated total instantaneous TRAS hydraulic flow [L/min] *)
    dwTRAS_StatusWord           : DWORD := 16#0000_0000; (* 32-bit packed TRAS operational and sequencing status *)
    dwTRAS_AlarmWord_Primary    : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 1 / Catastrophic Alarms *)
    dwTRAS_AlarmWord_Secondary  : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 Priority 2 / Advisory & Maintenance *)
    dwTMR_SensorHealthWord      : DWORD := 16#0000_0000; (* 32-bit packed 2oo3 sensor health, voting & degradation mask *)
    bDeployPermissiveGranted    : BOOL := FALSE;    (* FAR 25.933 interlock: WOW + TRA + Locks fully satisfied *)
    bReverserFullyDeployed      : BOOL := FALSE;    (* Full aerodynamic reverse deploy confirmed (stroke >= 575 mm) *)
    bReverserFullyStowed        : BOOL := FALSE;    (* Full aerodynamic stow confirmed (stroke <= 2 mm & all locks latched) *)
    bUncommandedMotionFault     : BOOL := FALSE;    (* Critical in-flight uncommanded sleeve displacement detected *)
    bSkewShutdownActive         : BOOL := FALSE;    (* Emergency hydraulic freeze due to excessive cowl skew *)
    bMPC_Active                 : BOOL := FALSE;    (* Model Predictive Controller active & in closed-loop regulation *)
    bGracefulDegradation        : BOOL := FALSE;    (* Secondary fallback control active due to sensor or EHSV fault *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* INTERNAL REGISTERS: MATRICES, 2oo3 VOTING, FLUID DYNAMICS, MPC OPTIMIZER & SEQUENCER     *)
    (* ========================================================================================= *)
    bFirstScanDone              : BOOL := FALSE;    (* Cold-start memory and matrix allocation flag *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. SKYDROL LD-4 HYDRAULIC FLUID & MECHANICAL GEOMETRIC SPECIFICATION                      *)
    (* ----------------------------------------------------------------------------------------- *)
    rPistonArea_Cap_m2          : REAL := 0.004560; (* Actuator cap-end effective piston working area [m2] *)
    rPistonArea_Rod_m2          : REAL := 0.002850; (* Actuator rod-end annular piston working area [m2] *)
    rActuatorFullStroke_mm      : REAL := 580.0;    (* Total translatory travel from full stow to full deploy [mm] *)
    rActuatorCylinderVolume_m3  : REAL := 0.002645; (* Total internal cylinder chamber volume [m3] *)
    rCowlMovingMass_kg          : REAL := 165.0;    (* Total translatory structural mass per cowl half [kg] *)
    rCoulombFriction_N          : REAL := 450.0;    (* Static / Coulomb seal and track friction force [N] *)
    rViscousFriction_Nsm        : REAL := 1250.0;   (* Viscous sliding friction damping coefficient [N*s/m] *)

    (* Synchronizer Flexible Shafting & Gearbox Parameters *)
    rSyncShaftStiffness_NmRad   : REAL := 345.0;    (* Torsional spring stiffness of flexible synchronizer shaft [Nm/rad] *)
    rSyncShaftDamping_NmsRad    : REAL := 8.50;     (* Torsional viscous damping of flexible shaft [Nm*s/rad] *)
    rBallScrewLead_mRev         : REAL := 0.0120;   (* Actuator internal ball screw lead pitch [m/rev] *)
    rGearboxRatio               : REAL := 3.250;    (* Angle gearbox speed ratio between ball screw and sync shaft *)
    rSyncShaftMaxTorque_Nm      : REAL := 280.0;    (* Shear pin mechanical failure threshold limit [Nm] *)

    (* EHSV Servo Valve Characteristics *)
    rEHSV_FlowGain_m3sA         : REAL := 0.00185;  (* EHSV rated flow gain at 70 bar drop [m3/(s*A)] *)
    rEHSV_PressureGain_PaA      : REAL := 2.50E8;   (* EHSV blocked-port pressure sensitivity [Pa/A] *)
    rEHSV_NaturalFreq_rads      : REAL := 440.0;    (* EHSV second-order torque motor natural frequency [rad/s] *)
    rEHSV_DampingRatio          : REAL := 0.72;     (* EHSV hydrodynamic damping ratio [-] *)
    rEHSV_MaxCurrent_mA         : REAL := 40.0;     (* Maximum allowable continuous servo current [mA] *)
    rEHSV_NullBias_mA           : REAL := 0.45;     (* Physical EHSV spring mechanical null offset bias [mA] *)

    (* Skydrol LD-4 Thermodynamic Equation Coefficients *)
    rFluidDensityBase_kgm3      : REAL := 1005.0;   (* Reference density at 20 deg C [kg/m3] *)
    rFluidThermalExpansion_1K   : REAL := 0.000785; (* Volumetric thermal expansion coefficient [1/K] *)
    rPureBulkModulusBase_MPa    : REAL := 1580.0;   (* Zero-gas reference liquid bulk modulus at 20 deg C [MPa] *)
    rBulkModTempSlope_MPaC      : REAL := 5.420;    (* Thermal degradation slope of bulk modulus [MPa/deg C] *)
    rAirEntrainmentRatio        : REAL := 0.0065;   (* Volumetric fraction of undissolved entrained air at 1 bar [-] *)
    rGasPolytropicIndex_gamma   : REAL := 1.35;     (* Air compression polytropic exponent [-] *)
    rAtmosphericPressure_bar    : REAL := 1.01325;  (* Standard sea level atmospheric pressure [bar] *)

    (* Aerodynamic Cowl Drag Load Polynomial Parameters *)
    rCowlFrontalArea_m2         : REAL := 1.720;    (* Total frontal area exposed to freestream airflow [m2] *)
    rCascadeArea_m2             : REAL := 2.450;    (* Total exposed turning cascade discharge area [m2] *)
    rAirDensity_kgm3            : REAL := 1.225;    (* Ambient atmospheric air density [kg/m3] *)
    rCd_Cowl_Min                : REAL := 0.045;    (* Stowed aerodynamic parasitic drag coefficient *)
    rCd_Cowl_Max                : REAL := 1.280;    (* Fully deployed aerodynamic drag coefficient *)
    rBypassTurningEfficiency    : REAL := 0.680;    (* Blocker door turning cascade momentum recovery factor *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) FILTERING & HEALTH STATUS REGISTERS               *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Voted Sensor Values *)
    rVoted_HydSupplyPress_bar   : REAL := 206.84;
    rVoted_HydReturnPress_bar   : REAL := 3.45;
    rVoted_UpperLVDT_Pos_mm     : REAL := 0.00;
    rVoted_LowerLVDT_Pos_mm     : REAL := 0.00;
    bVoted_WOW                  : BOOL := FALSE;
    bVoted_TertiaryLock_Seat    : BOOL := TRUE;
    bVoted_PrimaryLock_Latch    : BOOL := TRUE;

    (* Sensor Discrepancy Tolerance Limits *)
    rTol_SupplyPress_bar        : REAL := 14.0;     (* Max permissible variance across supply transmitters [bar] *)
    rTol_ReturnPress_bar        : REAL := 2.50;     (* Max permissible variance across return transmitters [bar] *)
    rTol_LVDT_Tracking_mm       : REAL := 1.80;     (* Max permissible variance across dual LVDT channels [mm] *)

    (* Stuck-Sensor Frozen Telemetry Counters *)
    iStuck_SupP_A : INT := 0; iStuck_SupP_B : INT := 0; iStuck_SupP_C : INT := 0;
    iStuck_RetP_A : INT := 0; iStuck_RetP_B : INT := 0; iStuck_RetP_C : INT := 0;
    iStuck_UpL_A  : INT := 0; iStuck_UpL_B  : INT := 0; iStuck_UpL_C  : INT := 0;
    iStuck_LwL_A  : INT := 0; iStuck_LwL_B  : INT := 0; iStuck_LwL_C  : INT := 0;

    (* Previous Scan Telemetry Values *)
    rPrev_SupP_A  : REAL := 206.84; rPrev_SupP_B  : REAL := 206.84; rPrev_SupP_C  : REAL := 206.84;
    rPrev_RetP_A  : REAL := 3.45;   rPrev_RetP_B  : REAL := 3.45;   rPrev_RetP_C  : REAL := 3.45;
    rPrev_UpL_A   : REAL := 0.00;   rPrev_UpL_B   : REAL := 0.00;   rPrev_UpL_C   : REAL := 0.00;
    rPrev_LwL_A   : REAL := 0.00;   rPrev_LwL_B   : REAL := 0.00;   rPrev_LwL_C   : REAL := 0.00;

    (* Individual Transducer Health Flags *)
    bHealth_SupP_A : BOOL := TRUE; bHealth_SupP_B : BOOL := TRUE; bHealth_SupP_C : BOOL := TRUE;
    bHealth_RetP_A : BOOL := TRUE; bHealth_RetP_B : BOOL := TRUE; bHealth_RetP_C : BOOL := TRUE;
    bHealth_UpL_A  : BOOL := TRUE; bHealth_UpL_B  : BOOL := TRUE; bHealth_UpL_C  : BOOL := TRUE;
    bHealth_LwL_A  : BOOL := TRUE; bHealth_LwL_B  : BOOL := TRUE; bHealth_LwL_C  : BOOL := TRUE;

    (* Degraded Voting State Flags *)
    bDegraded_SupP_1oo2 : BOOL := FALSE; bDegraded_SupP_1oo1 : BOOL := FALSE;
    bDegraded_RetP_1oo2 : BOOL := FALSE; bDegraded_RetP_1oo1 : BOOL := FALSE;
    bDegraded_UpL_1oo2  : BOOL := FALSE; bDegraded_UpL_1oo1  : BOOL := FALSE;
    bDegraded_LwL_1oo2  : BOOL := FALSE; bDegraded_LwL_1oo1  : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. 8x8 DISCRETE STATE-SPACE MATRICES & DUAL OBSERVER REGISTERS                            *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Vector x[0..7]:
         x[0]: Upper cowl stroke position deviation Delta x_upper [m]
         x[1]: Upper cowl translatory velocity Delta v_upper [m/s]
         x[2]: Lower cowl stroke position deviation Delta x_lower [m]
         x[3]: Lower cowl translatory velocity Delta v_lower [m/s]
         x[4]: Hydraulic actuator differential load pressure Delta P_load [Pa]
         x[5]: Sync shaft torsional deflection angle Delta theta_sync [rad]
         x[6]: Transcowl mechanical skew error Delta epsilon_skew = x_upper - x_lower [m]
         x[7]: Solenoid tertiary lock pin dynamic position Delta x_tl [m] *)
    aState_x                    : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_hat                : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aState_x_pred               : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

    (* Control Vector u[0..3]:
         u[0]: EHSV torque motor current command I_ehsv [mA] (Range -40.0 to +40.0 mA)
         u[1]: Hydraulic supply isolation valve pilot command V_iv [%] (0 to 100%)
         u[2]: Directional control valve spool command V_dcv [%] (0 to 100%)
         u[3]: Tertiary lock solenoid drive excitation V_tl_sol [V] (0 to 28 VDC) *)
    aControl_u                  : ARRAY[0..3] OF REAL := [0.0, 0.0, 50.0, 0.0];
    aControl_u_prev             : ARRAY[0..3] OF REAL := [0.0, 0.0, 50.0, 0.0];
    aControl_du                 : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Disturbance Vector d[0..2]:
         d[0]: Aerodynamic freestream dynamic pressure fluctuation Delta q_inf [kPa]
         d[1]: Engine fan bypass duct static plenum backpressure Delta P_fan [bar]
         d[2]: Hydraulic supply line pressure ripple Delta P_sup [bar] *)
    aDisturb_d                  : ARRAY[0..2] OF REAL := [0.0, 0.0, 0.0];

    (* Measurement Vector y[0..3]:
         y[0]: Mean cowl position y_pos_mean = 0.5 * (x_upper + x_lower) [m]
         y[1]: Mechanical skew error y_skew = x_upper - x_lower [m]
         y[2]: Actuator load differential pressure y_P_load [Pa]
         y[3]: Tertiary lock pin seated status y_tl_seat [0.0 = pulled, 1.0 = seated] *)
    aOutput_y                   : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 1.0];
    aOutput_y_sp                : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 1.0];
    aOutput_y_error             : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Discrete 8x8 State Transition Matrix A *)
    aMatrix_A                   : ARRAY[0..7, 0..7] OF REAL;
    (* Discrete 8x4 Input Coupling Matrix B *)
    aMatrix_B                   : ARRAY[0..7, 0..3] OF REAL;
    (* Discrete 4x8 Output Mapping Matrix C *)
    aMatrix_C                   : ARRAY[0..3, 0..7] OF REAL;
    (* Direct Feedthrough Matrix D (4x4) *)
    aMatrix_D                   : ARRAY[0..3, 0..3] OF REAL;
    (* Disturbance Input Matrix E (8x3) *)
    aMatrix_E                   : ARRAY[0..7, 0..2] OF REAL;
    (* Luenberger / Kalman Observer Gain Matrix L_obs (8x4) *)
    aMatrix_L_obs               : ARRAY[0..7, 0..3] OF REAL;

    (* ----------------------------------------------------------------------------------------- *)
    (* 4. MODEL PREDICTIVE CONTROL (MPC) CONSTRAINED QUADRATIC OPTIMIZER                         *)
    (* ----------------------------------------------------------------------------------------- *)
    aWeight_Q                   : ARRAY[0..3] OF REAL := [145.0, 480.0, 0.0025, 65.0]; (* Error penalty weights *)
    aWeight_R                   : ARRAY[0..3] OF REAL := [0.45, 0.12, 0.08, 0.02];    (* Actuator slew penalty *)
    aLimit_du_Max               : ARRAY[0..3] OF REAL := [4.50, 15.0, 10.0, 14.0];    (* Slew rate max per scan *)
    aLimit_du_Min               : ARRAY[0..3] OF REAL := [-4.50, -15.0, -10.0, -14.0]; (* Slew rate min per scan *)
    aLimit_u_Max                : ARRAY[0..3] OF REAL := [40.0, 100.0, 100.0, 28.0];   (* Max actuator position *)
    aLimit_u_Min                : ARRAY[0..3] OF REAL := [-40.0, 0.0, 0.0, 0.0];      (* Min actuator position *)

    (* Projected Gradient Optimization Workspace *)
    aGrad_g                     : ARRAY[0..3] OF REAL;
    aHessian_diag               : ARRAY[0..3] OF REAL;
    aStep_du                    : ARRAY[0..3] OF REAL;
    iIterQP                     : INT := 0;
    iMaxIterQP                  : INT := 10;
    rGradNorm                   : REAL := 0.0;
    rAlphaStep                  : REAL := 0.038;

    (* ----------------------------------------------------------------------------------------- *)
    (* 5. DECOUPLED FALLBACK PID SERVO CONTROLLERS (GRACEFUL DEGRADATION)                        *)
    (* ----------------------------------------------------------------------------------------- *)
    rPID_Kp_EHSV                : REAL := 0.185;
    rPID_Ki_EHSV                : REAL := 0.045;
    rPID_Kd_EHSV                : REAL := 0.008;
    rPID_Integ_EHSV             : REAL := 0.0;
    rPID_PrevErr_EHSV           : REAL := 0.0;

    rPID_Kp_Skew                : REAL := 1.850;
    rPID_Ki_Skew                : REAL := 0.120;
    rPID_Kd_Skew                : REAL := 0.035;
    rPID_Integ_Skew             : REAL := 0.0;
    rPID_PrevErr_Skew           : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 6. MULTI-STAGE FINITE STATE MACHINE (FSM) VARIABLES                                       *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Machine States:
         0  : STOWED_LOCKED         - In-flight baseline, all mechanical locks engaged, depressurized
         10 : WOW_ARMED             - On runway touchdown verified, reverse thrust armed, IV pressurized
         20 : UNLOCK_SEQUENCE       - Tertiary & Primary locks releasing, solenoid pulse active
         30 : TRANSLATING_DEPLOY    - Transcowls extending aft, EHSV skew compensation active
         40 : FULLY_DEPLOYED_HOLD   - Full stroke reached (>575 mm), reverse thrust locked in hold
         50 : STOW_COMMAND          - Throttle returned forward, DCV commanding cowl forward retraction
         60 : PRIMARY_LOCK_LATCH    - Cowls reaching stroke < 15 mm, primary latches engaging
         70 : VERIFY_STOWED         - Tertiary pin confirmed seated, hydraulic depressurization, safe
         90 : FAULT_ABORT_STOW      - Immediate abort & restow due to skew or hydraulic anomaly
         99 : EMERGENCY_SAFE_HOLD   - Catastrophic uncommanded motion containment, FADEC interlock *)
    iFSM_State                  : INT := 0;
    iPreviousFSM_State          : INT := 0;
    rStateTimer_s               : REAL := 0.0;
    rUnlockPulseTimer_s         : REAL := 0.0;
    rDeployTimeout_s            : REAL := 0.0;
    rStowTimeout_s              : REAL := 0.0;
    rLockVerifyTimer_s          : REAL := 0.0;
    iUnlockRetryCount           : INT := 0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 7. PHYSICAL COMPUTATION INTERMEDIATES & OBSERVER REGISTERS                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    rEffectiveFluidDensity      : REAL := 1005.0;   (* [kg/m3] *)
    rDynamicViscosity_Pa_s      : REAL := 0.0350;   (* [Pa*s] *)
    rGasVolumeFraction          : REAL := 0.0065;   (* [-] *)
    rAcousticVelocity_ms        : REAL := 1180.0;   (* [m/s] *)
    rDynamicPressure_kPa        : REAL := 0.00;     (* [kPa] *)
    rCowlDischargeFactor        : REAL := 0.00;     (* [-] *)
    rNetActuatorAeroForce_N     : REAL := 0.00;     (* [N] *)
    rUpperActuatorForce_N       : REAL := 0.00;     (* [N] *)
    rLowerActuatorForce_N       : REAL := 0.00;     (* [N] *)
    rSyncAngleEst_rad           : REAL := 0.00;     (* [rad] *)
    rSkewInnovation_m           : REAL := 0.00;     (* [m] *)
    rPrevMeanStroke_mm          : REAL := 0.00;     (* [mm] *)
    rActuatorAccEst_ms2         : REAL := 0.00;     (* [m/s2] *)
    rHydSupplyFlowEst_m3s       : REAL := 0.00;     (* [m3/s] *)

    (* Loop iterators *)
    iIdx                        : INT := 0;
    jIdx                        : INT := 0;
    rTmpSum                     : REAL := 0.0;
END_VAR
"""
    sections.append(s2)

    # -------------------------------------------------------------------------
    # SECTION 3: LOGIC PART 1 - SAFETY INTERLOCKS & MATRIX INITIALIZATION
    # -------------------------------------------------------------------------
    s3 = """(* ============================================================================================= *)
(* SECTION 1: EMERGENCY OVERRIDE INTERLOCK & COLD-START MATRIX INITIALIZATION                    *)
(* ============================================================================================= *)
(* Cockpit Direct Emergency Hardwired Restow Switch Override *)
IF bEmergencyStowOverride THEN
    iFSM_State                  := 90;              (* Direct jump to FAULT_ABORT_STOW *)
    rDirectionalValve_Pct       := 0.00;            (* Force DCV spool into 100% full forward STOW *)
    rDeployIsolationValve_Pct   := 100.0;           (* Maintain hydraulic pressure to force cowls closed *)
    rEHSV_CurrentCmd_mA         := -40.0;           (* Saturated reverse current command *)
    bTertiaryLockSolenoidCmd    := FALSE;           (* De-energize solenoid so spring forces pin to seat *)
    dwTRAS_AlarmWord_Primary    := dwTRAS_AlarmWord_Primary OR 16#8000_0000; (* Bit 31: EMERGENCY_STOW_ACTIVE *)
END_IF;

(* Master Block Execution Disabled *)
IF NOT bEnable THEN
    rEHSV_CurrentCmd_mA         := 0.00;
    rDeployIsolationValve_Pct   := 0.00;
    rDirectionalValve_Pct       := 50.0;            (* Neutral hydraulic lock position *)
    bTertiaryLockSolenoidCmd    := FALSE;
    bDeployPermissiveGranted    := FALSE;
    bReverserFullyDeployed      := FALSE;
    bReverserFullyStowed        := FALSE;
    bUncommandedMotionFault     := FALSE;
    bSkewShutdownActive         := FALSE;
    bMPC_Active                 := FALSE;
    bGracefulDegradation        := FALSE;
    dwTRAS_StatusWord           := 16#0000_0000;
    RETURN;
END_IF;

(* Cold-Start Matrix and Constant Allocation on First Scan *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x8 State-Space Transition Matrix A (Ts = 0.010 s, 100 Hz Avionics Task)      *)
    (* Models dual-cowl kinematic motion, hydraulic load compliance, and sync shaft torsion   *)
    (* ------------------------------------------------------------------------------------- *)
    (* Row 0: Upper stroke position x_upper[k+1] = x_upper + Ts * v_upper *)
    aMatrix_A[0,0] := 1.0000; aMatrix_A[0,1] := 0.0100; aMatrix_A[0,2] := 0.0000; aMatrix_A[0,3] := 0.0000;
    aMatrix_A[0,4] := 0.0000; aMatrix_A[0,5] := 0.0000; aMatrix_A[0,6] := 0.0000; aMatrix_A[0,7] := 0.0000;

    (* Row 1: Upper velocity v_upper[k+1] governed by hydraulic force, aero drag & sync torque *)
    aMatrix_A[1,0] := -0.0185; aMatrix_A[1,1] := 0.9420; aMatrix_A[1,2] := 0.0185; aMatrix_A[1,3] := 0.0042;
    aMatrix_A[1,4] := 0.0028;  aMatrix_A[1,5] := -0.0125; aMatrix_A[1,6] := -0.0245; aMatrix_A[1,7] := 0.0000;

    (* Row 2: Lower stroke position x_lower[k+1] = x_lower + Ts * v_lower *)
    aMatrix_A[2,0] := 0.0000; aMatrix_A[2,1] := 0.0000; aMatrix_A[2,2] := 1.0000; aMatrix_A[2,3] := 0.0100;
    aMatrix_A[2,4] := 0.0000; aMatrix_A[2,5] := 0.0000; aMatrix_A[2,6] := 0.0000; aMatrix_A[2,7] := 0.0000;

    (* Row 3: Lower velocity v_lower[k+1] symmetrical coupling via sync shaft *)
    aMatrix_A[3,0] := 0.0185; aMatrix_A[3,1] := 0.0042; aMatrix_A[3,2] := -0.0185; aMatrix_A[3,3] := 0.9420;
    aMatrix_A[3,4] := 0.0028; aMatrix_A[3,5] := 0.0125;  aMatrix_A[3,6] := 0.0245;  aMatrix_A[3,7] := 0.0000;

    (* Row 4: Hydraulic actuator differential load pressure dynamics *)
    aMatrix_A[4,0] := -450.0; aMatrix_A[4,1] := -8500.0; aMatrix_A[4,2] := -450.0; aMatrix_A[4,3] := -8500.0;
    aMatrix_A[4,4] := 0.8850; aMatrix_A[4,5] := 0.0000;  aMatrix_A[4,6] := 0.0000;  aMatrix_A[4,7] := 0.0000;

    (* Row 5: Sync shaft torsional deflection angle theta_sync *)
    aMatrix_A[5,0] := 18.25;  aMatrix_A[5,1] := 1.825;   aMatrix_A[5,2] := -18.25; aMatrix_A[5,3] := -1.825;
    aMatrix_A[5,4] := 0.0000; aMatrix_A[5,5] := 0.9250;  aMatrix_A[5,6] := 0.0000;  aMatrix_A[5,7] := 0.0000;

    (* Row 6: Transcowl mechanical skew error epsilon_skew = x_upper - x_lower *)
    aMatrix_A[6,0] := 0.0000; aMatrix_A[6,1] := 0.0100; aMatrix_A[6,2] := 0.0000; aMatrix_A[6,3] := -0.0100;
    aMatrix_A[6,4] := 0.0000; aMatrix_A[6,5] := 0.0000; aMatrix_A[6,6] := 0.9850; aMatrix_A[6,7] := 0.0000;

    (* Row 7: Solenoid tertiary lock pin position x_tl *)
    aMatrix_A[7,0] := 0.0000; aMatrix_A[7,1] := 0.0000; aMatrix_A[7,2] := 0.0000; aMatrix_A[7,3] := 0.0000;
    aMatrix_A[7,4] := 0.0000; aMatrix_A[7,5] := 0.0000; aMatrix_A[7,6] := 0.0000; aMatrix_A[7,7] := 0.8200;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 8x4 Input Coupling Matrix B                                                  *)
    (* Inputs: u[0]=I_ehsv [mA], u[1]=V_iv [%], u[2]=V_dcv [%], u[3]=V_tl_sol [V]           *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_B[0,0] := 0.00005; aMatrix_B[0,1] := 0.0000;  aMatrix_B[0,2] := 0.00008; aMatrix_B[0,3] := 0.0000;
    aMatrix_B[1,0] := 0.01250; aMatrix_B[1,1] := 0.0012;  aMatrix_B[1,2] := 0.01850; aMatrix_B[1,3] := 0.0000;
    aMatrix_B[2,0] := -0.00005; aMatrix_B[2,1] := 0.0000; aMatrix_B[2,2] := 0.00008; aMatrix_B[2,3] := 0.0000;
    aMatrix_B[3,0] := -0.01250; aMatrix_B[3,1] := 0.0012; aMatrix_B[3,2] := 0.01850; aMatrix_B[3,3] := 0.0000;
    aMatrix_B[4,0] := 185.000; aMatrix_B[4,1] := 45.000;  aMatrix_B[4,2] := 320.000; aMatrix_B[4,3] := 0.0000;
    aMatrix_B[5,0] := 0.04500; aMatrix_B[5,1] := 0.0000;  aMatrix_B[5,2] := 0.00000; aMatrix_B[5,3] := 0.0000;
    aMatrix_B[6,0] := 0.02500; aMatrix_B[6,1] := 0.0000;  aMatrix_B[6,2] := 0.00000; aMatrix_B[6,3] := 0.0000;
    aMatrix_B[7,0] := 0.00000; aMatrix_B[7,1] := 0.0000;  aMatrix_B[7,2] := 0.00000; aMatrix_B[7,3] := 0.0012;

    (* ------------------------------------------------------------------------------------- *)
    (* Discrete 4x8 Output Mapping Matrix C                                                  *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_C[0,0] := 0.500; aMatrix_C[0,1] := 0.000; aMatrix_C[0,2] := 0.500; aMatrix_C[0,3] := 0.000;
    aMatrix_C[0,4] := 0.000; aMatrix_C[0,5] := 0.000; aMatrix_C[0,6] := 0.000; aMatrix_C[0,7] := 0.000;

    aMatrix_C[1,0] := 1.000; aMatrix_C[1,1] := 0.000; aMatrix_C[1,2] := -1.000; aMatrix_C[1,3] := 0.000;
    aMatrix_C[1,4] := 0.000; aMatrix_C[1,5] := 0.000; aMatrix_C[1,6] := 0.000;  aMatrix_C[1,7] := 0.000;

    aMatrix_C[2,0] := 0.000; aMatrix_C[2,1] := 0.000; aMatrix_C[2,2] := 0.000; aMatrix_C[2,3] := 0.000;
    aMatrix_C[2,4] := 1.000; aMatrix_C[2,5] := 0.000; aMatrix_C[2,6] := 0.000; aMatrix_C[2,7] := 0.000;

    aMatrix_C[3,0] := 0.000; aMatrix_C[3,1] := 0.000; aMatrix_C[3,2] := 0.000; aMatrix_C[3,3] := 0.000;
    aMatrix_C[3,4] := 0.000; aMatrix_C[3,5] := 0.000; aMatrix_C[3,6] := 0.000; aMatrix_C[3,7] := 1.000;

    (* ------------------------------------------------------------------------------------- *)
    (* Direct Feedthrough Matrix D (4x4) (Zero strictly for physical causal actuation)      *)
    (* ------------------------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 3 DO
        FOR jIdx := 0 TO 3 DO
            aMatrix_D[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------- *)
    (* Disturbance Coupling Matrix E (8x3)                                                   *)
    (* Disturbances: d[0]=q_inf [kPa], d[1]=P_fan [bar], d[2]=P_sup [bar]                    *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_E[0,0] := -0.00001; aMatrix_E[0,1] := -0.00002; aMatrix_E[0,2] := 0.00004;
    aMatrix_E[1,0] := -0.00450; aMatrix_E[1,1] := -0.00850; aMatrix_E[1,2] := 0.00620;
    aMatrix_E[2,0] := -0.00001; aMatrix_E[2,1] := -0.00002; aMatrix_E[2,2] := 0.00004;
    aMatrix_E[3,0] := -0.00450; aMatrix_E[3,1] := -0.00850; aMatrix_E[3,2] := 0.00620;
    aMatrix_E[4,0] := -120.000; aMatrix_E[4,1] := -250.000; aMatrix_E[4,2] := 1850.00;
    aMatrix_E[5,0] := 0.00000;  aMatrix_E[5,1] := 0.00000;  aMatrix_E[5,2] := 0.00000;
    aMatrix_E[6,0] := 0.00000;  aMatrix_E[6,1] := 0.00000;  aMatrix_E[6,2] := 0.00000;
    aMatrix_E[7,0] := 0.00000;  aMatrix_E[7,1] := 0.00000;  aMatrix_E[7,2] := 0.00000;

    (* ------------------------------------------------------------------------------------- *)
    (* Luenberger / Kalman Observer Gain Matrix L_obs (8x4)                                  *)
    (* ------------------------------------------------------------------------------------- *)
    aMatrix_L_obs[0,0] := 0.2850; aMatrix_L_obs[0,1] := 0.1450; aMatrix_L_obs[0,2] := 0.0000; aMatrix_L_obs[0,3] := 0.0000;
    aMatrix_L_obs[1,0] := 1.4500; aMatrix_L_obs[1,1] := 0.8500; aMatrix_L_obs[1,2] := 0.0002; aMatrix_L_obs[1,3] := 0.0000;
    aMatrix_L_obs[2,0] := 0.2850; aMatrix_L_obs[2,1] := -0.1450; aMatrix_L_obs[2,2] := 0.0000; aMatrix_L_obs[2,3] := 0.0000;
    aMatrix_L_obs[3,0] := 1.4500; aMatrix_L_obs[3,1] := -0.8500; aMatrix_L_obs[3,2] := 0.0002; aMatrix_L_obs[3,3] := 0.0000;
    aMatrix_L_obs[4,0] := 0.0000; aMatrix_L_obs[4,1] := 0.0000;  aMatrix_L_obs[4,2] := 0.3200; aMatrix_L_obs[4,3] := 0.0000;
    aMatrix_L_obs[5,0] := 0.0000; aMatrix_L_obs[5,1] := 0.4200;  aMatrix_L_obs[5,2] := 0.0000; aMatrix_L_obs[5,3] := 0.0000;
    aMatrix_L_obs[6,0] := 0.0000; aMatrix_L_obs[6,1] := 0.8500;  aMatrix_L_obs[6,2] := 0.0000; aMatrix_L_obs[6,3] := 0.0000;
    aMatrix_L_obs[7,0] := 0.0000; aMatrix_L_obs[7,1] := 0.0000;  aMatrix_L_obs[7,2] := 0.0000; aMatrix_L_obs[7,3] := 0.4500;

    bFirstScanDone := TRUE;
END_IF;
"""
    sections.append(s3)

    # -------------------------------------------------------------------------
    # SECTION 4: LOGIC PART 2 - 2oo3 TMR VOTING & DEGRADATION
    # -------------------------------------------------------------------------
    s4 = """(* ============================================================================================= *)
(* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT DEGRADATION ENGINE            *)
(* ============================================================================================= *)
(* --------------------------------------------------------------------------------------------- *)
(* 1. Hydraulic Supply Pressure Transducers (rHydSupplyPress_bar_A, B, C)                        *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rHydSupplyPress_bar_A - rPrev_SupP_A) < 0.001 THEN iStuck_SupP_A := iStuck_SupP_A + 1; ELSE iStuck_SupP_A := 0; END_IF;
IF ABS(rHydSupplyPress_bar_B - rPrev_SupP_B) < 0.001 THEN iStuck_SupP_B := iStuck_SupP_B + 1; ELSE iStuck_SupP_B := 0; END_IF;
IF ABS(rHydSupplyPress_bar_C - rPrev_SupP_C) < 0.001 THEN iStuck_SupP_C := iStuck_SupP_C + 1; ELSE iStuck_SupP_C := 0; END_IF;
rPrev_SupP_A := rHydSupplyPress_bar_A; rPrev_SupP_B := rHydSupplyPress_bar_B; rPrev_SupP_C := rHydSupplyPress_bar_C;

bHealth_SupP_A := (rHydSupplyPress_bar_A >= 10.0) AND (rHydSupplyPress_bar_A <= 320.0) AND (iStuck_SupP_A < 250);
bHealth_SupP_B := (rHydSupplyPress_bar_B >= 10.0) AND (rHydSupplyPress_bar_B <= 320.0) AND (iStuck_SupP_B < 250);
bHealth_SupP_C := (rHydSupplyPress_bar_C >= 10.0) AND (rHydSupplyPress_bar_C <= 320.0) AND (iStuck_SupP_C < 250);

IF bHealth_SupP_A AND bHealth_SupP_B AND bHealth_SupP_C THEN
    bDegraded_SupP_1oo2 := FALSE; bDegraded_SupP_1oo1 := FALSE;
    IF ((rHydSupplyPress_bar_A >= rHydSupplyPress_bar_B) AND (rHydSupplyPress_bar_A <= rHydSupplyPress_bar_C)) OR
       ((rHydSupplyPress_bar_A >= rHydSupplyPress_bar_C) AND (rHydSupplyPress_bar_A <= rHydSupplyPress_bar_B)) THEN
        rVoted_HydSupplyPress_bar := rHydSupplyPress_bar_A;
    ELSIF ((rHydSupplyPress_bar_B >= rHydSupplyPress_bar_A) AND (rHydSupplyPress_bar_B <= rHydSupplyPress_bar_C)) OR
          ((rHydSupplyPress_bar_B >= rHydSupplyPress_bar_C) AND (rHydSupplyPress_bar_B <= rHydSupplyPress_bar_A)) THEN
        rVoted_HydSupplyPress_bar := rHydSupplyPress_bar_B;
    ELSE
        rVoted_HydSupplyPress_bar := rHydSupplyPress_bar_C;
    END_IF;
    IF (ABS(rHydSupplyPress_bar_A - rHydSupplyPress_bar_B) > rTol_SupplyPress_bar) OR
       (ABS(rHydSupplyPress_bar_B - rHydSupplyPress_bar_C) > rTol_SupplyPress_bar) OR
       (ABS(rHydSupplyPress_bar_A - rHydSupplyPress_bar_C) > rTol_SupplyPress_bar) THEN
        dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0001; (* Bit 0: Supply Pressure Discrepancy *)
    END_IF;
ELSIF bHealth_SupP_A AND bHealth_SupP_B THEN
    bDegraded_SupP_1oo2 := TRUE; rVoted_HydSupplyPress_bar := (rHydSupplyPress_bar_A + rHydSupplyPress_bar_B) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0002;
ELSIF bHealth_SupP_A AND bHealth_SupP_C THEN
    bDegraded_SupP_1oo2 := TRUE; rVoted_HydSupplyPress_bar := (rHydSupplyPress_bar_A + rHydSupplyPress_bar_C) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0002;
ELSIF bHealth_SupP_B AND bHealth_SupP_C THEN
    bDegraded_SupP_1oo2 := TRUE; rVoted_HydSupplyPress_bar := (rHydSupplyPress_bar_B + rHydSupplyPress_bar_C) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0002;
ELSIF bHealth_SupP_A THEN
    bDegraded_SupP_1oo1 := TRUE; rVoted_HydSupplyPress_bar := rHydSupplyPress_bar_A;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0004;
ELSIF bHealth_SupP_B THEN
    bDegraded_SupP_1oo1 := TRUE; rVoted_HydSupplyPress_bar := rHydSupplyPress_bar_B;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0004;
ELSIF bHealth_SupP_C THEN
    bDegraded_SupP_1oo1 := TRUE; rVoted_HydSupplyPress_bar := rHydSupplyPress_bar_C;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0004;
ELSE
    rVoted_HydSupplyPress_bar := 0.0;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0008; (* Total Supply Pressure Loss *)
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2. Upper Sleeve LVDT Transducers (rUpperLVDT_Pos_mm_A, B, C)                                  *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rUpperLVDT_Pos_mm_A - rPrev_UpL_A) < 0.0005 THEN iStuck_UpL_A := iStuck_UpL_A + 1; ELSE iStuck_UpL_A := 0; END_IF;
IF ABS(rUpperLVDT_Pos_mm_B - rPrev_UpL_B) < 0.0005 THEN iStuck_UpL_B := iStuck_UpL_B + 1; ELSE iStuck_UpL_B := 0; END_IF;
IF ABS(rUpperLVDT_Pos_mm_C - rPrev_UpL_C) < 0.0005 THEN iStuck_UpL_C := iStuck_UpL_C + 1; ELSE iStuck_UpL_C := 0; END_IF;
rPrev_UpL_A := rUpperLVDT_Pos_mm_A; rPrev_UpL_B := rUpperLVDT_Pos_mm_B; rPrev_UpL_C := rUpperLVDT_Pos_mm_C;

bHealth_UpL_A := (rUpperLVDT_Pos_mm_A >= -5.0) AND (rUpperLVDT_Pos_mm_A <= 620.0) AND (iStuck_UpL_A < 400);
bHealth_UpL_B := (rUpperLVDT_Pos_mm_B >= -5.0) AND (rUpperLVDT_Pos_mm_B <= 620.0) AND (iStuck_UpL_B < 400);
bHealth_UpL_C := (rUpperLVDT_Pos_mm_C >= -5.0) AND (rUpperLVDT_Pos_mm_C <= 620.0) AND (iStuck_UpL_C < 400);

IF bHealth_UpL_A AND bHealth_UpL_B AND bHealth_UpL_C THEN
    bDegraded_UpL_1oo2 := FALSE; bDegraded_UpL_1oo1 := FALSE;
    IF ((rUpperLVDT_Pos_mm_A >= rUpperLVDT_Pos_mm_B) AND (rUpperLVDT_Pos_mm_A <= rUpperLVDT_Pos_mm_C)) OR
       ((rUpperLVDT_Pos_mm_A >= rUpperLVDT_Pos_mm_C) AND (rUpperLVDT_Pos_mm_A <= rUpperLVDT_Pos_mm_B)) THEN
        rVoted_UpperLVDT_Pos_mm := rUpperLVDT_Pos_mm_A;
    ELSIF ((rUpperLVDT_Pos_mm_B >= rUpperLVDT_Pos_mm_A) AND (rUpperLVDT_Pos_mm_B <= rUpperLVDT_Pos_mm_C)) OR
          ((rUpperLVDT_Pos_mm_B >= rUpperLVDT_Pos_mm_C) AND (rUpperLVDT_Pos_mm_B <= rUpperLVDT_Pos_mm_A)) THEN
        rVoted_UpperLVDT_Pos_mm := rUpperLVDT_Pos_mm_B;
    ELSE
        rVoted_UpperLVDT_Pos_mm := rUpperLVDT_Pos_mm_C;
    END_IF;
    IF (ABS(rUpperLVDT_Pos_mm_A - rUpperLVDT_Pos_mm_B) > rTol_LVDT_Tracking_mm) OR
       (ABS(rUpperLVDT_Pos_mm_B - rUpperLVDT_Pos_mm_C) > rTol_LVDT_Tracking_mm) OR
       (ABS(rUpperLVDT_Pos_mm_A - rUpperLVDT_Pos_mm_C) > rTol_LVDT_Tracking_mm) THEN
        dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0010; (* Bit 4: Upper LVDT Discrepancy *)
    END_IF;
ELSIF bHealth_UpL_A AND bHealth_UpL_B THEN
    bDegraded_UpL_1oo2 := TRUE; rVoted_UpperLVDT_Pos_mm := (rUpperLVDT_Pos_mm_A + rUpperLVDT_Pos_mm_B) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0020;
ELSIF bHealth_UpL_A AND bHealth_UpL_C THEN
    bDegraded_UpL_1oo2 := TRUE; rVoted_UpperLVDT_Pos_mm := (rUpperLVDT_Pos_mm_A + rUpperLVDT_Pos_mm_C) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0020;
ELSIF bHealth_UpL_B AND bHealth_UpL_C THEN
    bDegraded_UpL_1oo2 := TRUE; rVoted_UpperLVDT_Pos_mm := (rUpperLVDT_Pos_mm_B + rUpperLVDT_Pos_mm_C) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0020;
ELSIF bHealth_UpL_A THEN
    bDegraded_UpL_1oo1 := TRUE; rVoted_UpperLVDT_Pos_mm := rUpperLVDT_Pos_mm_A;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0040;
ELSIF bHealth_UpL_B THEN
    bDegraded_UpL_1oo1 := TRUE; rVoted_UpperLVDT_Pos_mm := rUpperLVDT_Pos_mm_B;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0040;
ELSIF bHealth_UpL_C THEN
    bDegraded_UpL_1oo1 := TRUE; rVoted_UpperLVDT_Pos_mm := rUpperLVDT_Pos_mm_C;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0040;
ELSE
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0080; (* Critical Upper LVDT Failure *)
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 3. Lower Sleeve LVDT Transducers (rLowerLVDT_Pos_mm_A, B, C)                                  *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rLowerLVDT_Pos_mm_A - rPrev_LwL_A) < 0.0005 THEN iStuck_LwL_A := iStuck_LwL_A + 1; ELSE iStuck_LwL_A := 0; END_IF;
IF ABS(rLowerLVDT_Pos_mm_B - rPrev_LwL_B) < 0.0005 THEN iStuck_LwL_B := iStuck_LwL_B + 1; ELSE iStuck_LwL_B := 0; END_IF;
IF ABS(rLowerLVDT_Pos_mm_C - rPrev_LwL_C) < 0.0005 THEN iStuck_LwL_C := iStuck_LwL_C + 1; ELSE iStuck_LwL_C := 0; END_IF;
rPrev_LwL_A := rLowerLVDT_Pos_mm_A; rPrev_LwL_B := rLowerLVDT_Pos_mm_B; rPrev_LwL_C := rLowerLVDT_Pos_mm_C;

bHealth_LwL_A := (rLowerLVDT_Pos_mm_A >= -5.0) AND (rLowerLVDT_Pos_mm_A <= 620.0) AND (iStuck_LwL_A < 400);
bHealth_LwL_B := (rLowerLVDT_Pos_mm_B >= -5.0) AND (rLowerLVDT_Pos_mm_B <= 620.0) AND (iStuck_LwL_B < 400);
bHealth_LwL_C := (rLowerLVDT_Pos_mm_C >= -5.0) AND (rLowerLVDT_Pos_mm_C <= 620.0) AND (iStuck_LwL_C < 400);

IF bHealth_LwL_A AND bHealth_LwL_B AND bHealth_LwL_C THEN
    bDegraded_LwL_1oo2 := FALSE; bDegraded_LwL_1oo1 := FALSE;
    IF ((rLowerLVDT_Pos_mm_A >= rLowerLVDT_Pos_mm_B) AND (rLowerLVDT_Pos_mm_A <= rLowerLVDT_Pos_mm_C)) OR
       ((rLowerLVDT_Pos_mm_A >= rLowerLVDT_Pos_mm_C) AND (rLowerLVDT_Pos_mm_A <= rLowerLVDT_Pos_mm_B)) THEN
        rVoted_LowerLVDT_Pos_mm := rLowerLVDT_Pos_mm_A;
    ELSIF ((rLowerLVDT_Pos_mm_B >= rLowerLVDT_Pos_mm_A) AND (rLowerLVDT_Pos_mm_B <= rLowerLVDT_Pos_mm_C)) OR
          ((rLowerLVDT_Pos_mm_B >= rLowerLVDT_Pos_mm_C) AND (rLowerLVDT_Pos_mm_B <= rLowerLVDT_Pos_mm_A)) THEN
        rVoted_LowerLVDT_Pos_mm := rLowerLVDT_Pos_mm_B;
    ELSE
        rVoted_LowerLVDT_Pos_mm := rLowerLVDT_Pos_mm_C;
    END_IF;
    IF (ABS(rLowerLVDT_Pos_mm_A - rLowerLVDT_Pos_mm_B) > rTol_LVDT_Tracking_mm) OR
       (ABS(rLowerLVDT_Pos_mm_B - rLowerLVDT_Pos_mm_C) > rTol_LVDT_Tracking_mm) OR
       (ABS(rLowerLVDT_Pos_mm_A - rLowerLVDT_Pos_mm_C) > rTol_LVDT_Tracking_mm) THEN
        dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0100; (* Bit 8: Lower LVDT Discrepancy *)
    END_IF;
ELSIF bHealth_LwL_A AND bHealth_LwL_B THEN
    bDegraded_LwL_1oo2 := TRUE; rVoted_LowerLVDT_Pos_mm := (rLowerLVDT_Pos_mm_A + rLowerLVDT_Pos_mm_B) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0200;
ELSIF bHealth_LwL_A AND bHealth_LwL_C THEN
    bDegraded_LwL_1oo2 := TRUE; rVoted_LowerLVDT_Pos_mm := (rLowerLVDT_Pos_mm_A + rLowerLVDT_Pos_mm_C) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0200;
ELSIF bHealth_LwL_B AND bHealth_LwL_C THEN
    bDegraded_LwL_1oo2 := TRUE; rVoted_LowerLVDT_Pos_mm := (rLowerLVDT_Pos_mm_B + rLowerLVDT_Pos_mm_C) * 0.5;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0200;
ELSIF bHealth_LwL_A THEN
    bDegraded_LwL_1oo1 := TRUE; rVoted_LowerLVDT_Pos_mm := rLowerLVDT_Pos_mm_A;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0400;
ELSIF bHealth_LwL_B THEN
    bDegraded_LwL_1oo1 := TRUE; rVoted_LowerLVDT_Pos_mm := rLowerLVDT_Pos_mm_B;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0400;
ELSIF bHealth_LwL_C THEN
    bDegraded_LwL_1oo1 := TRUE; rVoted_LowerLVDT_Pos_mm := rLowerLVDT_Pos_mm_C;
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0400;
ELSE
    dwTMR_SensorHealthWord := dwTMR_SensorHealthWord OR 16#0000_0800; (* Critical Lower LVDT Failure *)
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 4. Discrete 2oo3 Voting for Weight-on-Wheels (WOW) Squat Switches                             *)
(* --------------------------------------------------------------------------------------------- *)
bVoted_WOW := (bWOW_Channel_A AND bWOW_Channel_B) OR
              (bWOW_Channel_B AND bWOW_Channel_C) OR
              (bWOW_Channel_A AND bWOW_Channel_C);

(* --------------------------------------------------------------------------------------------- *)
(* 5. Discrete 2oo3 Voting for Tertiary Lock Pin Seated Proximity Sensors                         *)
(* --------------------------------------------------------------------------------------------- *)
bVoted_TertiaryLock_Seat := (bTertiaryLockPin_Seat_A AND bTertiaryLockPin_Seat_B) OR
                            (bTertiaryLockPin_Seat_B AND bTertiaryLockPin_Seat_C) OR
                            (bTertiaryLockPin_Seat_A AND bTertiaryLockPin_Seat_C);

(* --------------------------------------------------------------------------------------------- *)
(* 6. Discrete 2oo3 Voting for Primary Track Lock Latches                                        *)
(* --------------------------------------------------------------------------------------------- *)
bVoted_PrimaryLock_Latch := (bPrimaryLockLatch_A AND bPrimaryLockLatch_B) OR
                            (bPrimaryLockLatch_B AND bPrimaryLockLatch_C) OR
                            (bPrimaryLockLatch_A AND bPrimaryLockLatch_C);

(* Mean Cowl Displacement and Mechanical Skew Deviation *)
rMeanCowlStroke_mm    := (rVoted_UpperLVDT_Pos_mm + rVoted_LowerLVDT_Pos_mm) * 0.50;
rCowlSkewDeviation_mm := rVoted_UpperLVDT_Pos_mm - rVoted_LowerLVDT_Pos_mm;
rActuatorVelocity_mms := (rMeanCowlStroke_mm - rPrevMeanStroke_mm) / tScanTime_s;
rPrevMeanStroke_mm    := rMeanCowlStroke_mm;
"""
    sections.append(s4)

    # -------------------------------------------------------------------------
    # SECTION 5: LOGIC PART 3 - FLUID PHYSICS & AERODYNAMICS
    # -------------------------------------------------------------------------
    s5 = """(* ============================================================================================= *)
(* SECTION 3: FLUID THERMODYNAMICS, BULK MODULUS & TRANSLATING COWL AERODYNAMIC FORCES          *)
(* ============================================================================================= *)
(* 1. Temperature-Dependent Skydrol LD-4 Physical Density *)
(* rho(T) = rho_base * (1 - beta_thermal * (T - 20.0)) *)
rEffectiveFluidDensity := rFluidDensityBase_kgm3 * (1.0 - rFluidThermalExpansion_1K * (rHydFluidTemp_degC - 20.0));
IF rEffectiveFluidDensity < 880.0 THEN rEffectiveFluidDensity := 880.0; END_IF;
IF rEffectiveFluidDensity > 1080.0 THEN rEffectiveFluidDensity := 1080.0; END_IF;

(* 2. Dynamic Viscosity Approximation (Vogel-Fulcher-Tammann Equation) *)
(* nu(T) surges dramatically below 0 deg C *)
IF rHydFluidTemp_degC < -20.0 THEN
    rDynamicViscosity_Pa_s := 0.2850;   (* Heavy viscous drag in sub-zero start *)
ELSIF rHydFluidTemp_degC < 10.0 THEN
    rDynamicViscosity_Pa_s := 0.0850;
ELSIF rHydFluidTemp_degC < 60.0 THEN
    rDynamicViscosity_Pa_s := 0.0240;
ELSE
    rDynamicViscosity_Pa_s := 0.0085;
END_IF;

(* 3. Pure Liquid Bulk Modulus vs Temperature *)
(* Beta_pure(T) = Beta_base - Slope * (T - 20.0) *)
rTmpSum := rPureBulkModulusBase_MPa - rBulkModTempSlope_MPaC * (rHydFluidTemp_degC - 20.0);
IF rTmpSum < 850.0 THEN rTmpSum := 850.0; END_IF;
IF rTmpSum > 1950.0 THEN rTmpSum := 1950.0; END_IF;

(* 4. Effective Bulk Modulus with Air Entrainment Compressibility *)
(* Governed by Henry's law and polytropic gas bubble elasticity *)
(* Beta_eff = Beta_pure / [ 1 + (Vg0/V0) * (P0/P)^(1/gamma) * (Beta_pure / (gamma * P)) ] *)
IF rVoted_HydSupplyPress_bar > 5.0 THEN
    rGasVolumeFraction := rAirEntrainmentRatio * EXPT((rAtmosphericPressure_bar / rVoted_HydSupplyPress_bar), (1.0 / rGasPolytropicIndex_gamma));
    rEffectiveBulkModulus_MPa := rTmpSum / (1.0 + rGasVolumeFraction * (rTmpSum / (rGasPolytropicIndex_gamma * rVoted_HydSupplyPress_bar * 0.10)));
ELSE
    rEffectiveBulkModulus_MPa := 350.0; (* Severe aeration compressibility at low pressure *)
END_IF;

(* 5. Hydraulic Acoustic Wave Propagation Velocity *)
(* c_acoustic = sqrt(Beta_eff [Pa] / rho [kg/m3]) *)
rAcousticVelocity_ms := SQRT((rEffectiveBulkModulus_MPa * 1.0E6) / rEffectiveFluidDensity);

(* 6. Translating Cowl Aerodynamic Drag & Cascade Blowback Forces *)
(* Dynamic freestream air pressure q_inf = 0.5 * rho_air * V_tas^2 [Pa] *)
(* Airspeed conversion: 1 knot = 0.514444 m/s *)
rTmpSum := rAircraftAirspeed_kts * 0.514444;
rDynamicPressure_kPa := (0.5 * rAirDensity_kgm3 * rTmpSum * rTmpSum) / 1000.0;

(* Cowl Opening Ratio alpha = Stroke / FullStroke [0.0 to 1.0] *)
IF rMeanCowlStroke_mm > 0.0 THEN
    rCowlDischargeFactor := rMeanCowlStroke_mm / rActuatorFullStroke_mm;
    IF rCowlDischargeFactor > 1.0 THEN rCowlDischargeFactor := 1.0; END_IF;
ELSE
    rCowlDischargeFactor := 0.0;
END_IF;

(* Dynamic drag coefficient increases non-linearly with cowl opening and cascade exposure *)
rTmpSum := rCd_Cowl_Min + (rCd_Cowl_Max - rCd_Cowl_Min) * (rCowlDischargeFactor * rCowlDischargeFactor);

(* Freestream aerodynamic retarding drag F_drag = q_inf * Area * Cd *)
rAerodynamicDragLoad_kN := (rDynamicPressure_kPa * 1000.0 * rCowlFrontalArea_m2 * rTmpSum) / 1000.0;

(* Bypass duct cold-stream plenum blowback force *)
(* P_fan * A_cascade * turning_efficiency acts in assist/retard depending on stroke *)
rNetActuatorAeroForce_N := (rAerodynamicDragLoad_kN * 1000.0) +
                           (rEngineFanBypassPress_bar * 1.0E5 * rCascadeArea_m2 * rCowlDischargeFactor * rBypassTurningEfficiency);

(* Flow rate estimation based on mean sleeve velocity *)
rHydSupplyFlowEst_m3s   := (ABS(rActuatorVelocity_mms) / 1000.0) * (rPistonArea_Cap_m2 + rPistonArea_Rod_m2);
rHydraulicSupplyFlow_Lmin := rHydSupplyFlowEst_m3s * 60000.0;
"""
    sections.append(s5)

    # -------------------------------------------------------------------------
    # SECTION 6: LOGIC PART 4 - MECHANICAL SYNCHRONIZER & SKEW OBSERVER
    # -------------------------------------------------------------------------
    s6 = """(* ============================================================================================= *)
(* SECTION 4: MULTI-SLEEVE MECHANICAL SYNCHRONIZER & DYNAMIC SKEW OBSERVER                       *)
(* ============================================================================================= *)
(* Torsional deflection between upper and lower ball screw drives *)
(* theta = (x_upper - x_lower) * (2*pi / L_screw) * N_gear *)
rSyncAngleEst_rad := ((rVoted_UpperLVDT_Pos_mm - rVoted_LowerLVDT_Pos_mm) / 1000.0) *
                     ((2.0 * 3.14159265) / rBallScrewLead_mRev) * rGearboxRatio;

(* Transmitted torque across flexible sync shaft: tau = K_sync * theta + C_sync * d_theta/dt *)
rSyncShaftTorqueEst_Nm := rSyncShaftStiffness_NmRad * rSyncAngleEst_rad;

(* Dynamic Skew Observer Innovation Update *)
(* e_skew = y_skew_meas - C[1,:] * x_hat *)
rSkewInnovation_m := (rCowlSkewDeviation_mm / 1000.0) - aState_x_hat[6];

(* Correct estimated skew state *)
aState_x_hat[6] := aState_x_hat[6] + aMatrix_L_obs[6, 1] * rSkewInnovation_m;
aState_x_hat[5] := rSyncAngleEst_rad;

(* High Skew Trip Protection (FAR 25.933 Mechanical Binding Mitigation) *)
IF ABS(rCowlSkewDeviation_mm) >= 5.80 THEN
    bSkewShutdownActive      := TRUE;
    iFSM_State               := 90;         (* Abort deployment *)
    dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0002; (* Bit 1: HIGH_SKEW_CRITICAL_TRIP *)
ELSIF ABS(rCowlSkewDeviation_mm) >= 3.50 THEN
    dwTRAS_AlarmWord_Secondary := dwTRAS_AlarmWord_Secondary OR 16#0000_0001; (* Bit 0: SKEW_WARNING_HIGH *)
END_IF;

(* Sync Shaft Overtorque Monitoring *)
IF ABS(rSyncShaftTorqueEst_Nm) >= rSyncShaftMaxTorque_Nm THEN
    bSkewShutdownActive      := TRUE;
    iFSM_State               := 90;
    dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0004; (* Bit 2: SYNC_SHAFT_OVERTORQUE_TRIP *)
END_IF;
"""
    sections.append(s6)

    # -------------------------------------------------------------------------
    # SECTION 7: LOGIC PART 5 - 8x8 STATE-SPACE PROPAGATION
    # -------------------------------------------------------------------------
    s7 = """(* ============================================================================================= *)
(* SECTION 5: 8x8 DISCRETE STATE-SPACE TIME PROPAGATION (x[k+1] = A*x[k] + B*u[k] + E*d[k])     *)
(* ============================================================================================= *)
(* Assign disturbance inputs from physical calculations *)
aDisturb_d[0] := rDynamicPressure_kPa;
aDisturb_d[1] := rEngineFanBypassPress_bar - 1.0;
aDisturb_d[2] := rVoted_HydSupplyPress_bar - 206.84;

(* Unroll State Prediction Vector x_pred = A * x_hat + B * u + E * d *)
FOR iIdx := 0 TO 7 DO
    rTmpSum := 0.0;
    (* State coupling *)
    FOR jIdx := 0 TO 7 DO
        rTmpSum := rTmpSum + aMatrix_A[iIdx, jIdx] * aState_x_hat[jIdx];
    END_FOR;
    (* Input coupling *)
    FOR jIdx := 0 TO 3 DO
        rTmpSum := rTmpSum + aMatrix_B[iIdx, jIdx] * aControl_u[jIdx];
    END_FOR;
    (* Disturbance coupling *)
    FOR jIdx := 0 TO 2 DO
        rTmpSum := rTmpSum + aMatrix_E[iIdx, jIdx] * aDisturb_d[jIdx];
    END_FOR;
    aState_x_pred[iIdx] := rTmpSum;
END_FOR;

(* Update Kalman / Luenberger Observer Innovations *)
(* Measurement output y_meas *)
aOutput_y[0] := rMeanCowlStroke_mm / 1000.0;
aOutput_y[1] := rCowlSkewDeviation_mm / 1000.0;
aOutput_y[2] := (rVoted_HydSupplyPress_bar - rVoted_HydReturnPress_bar) * 1.0E5;
IF bVoted_TertiaryLock_Seat THEN aOutput_y[3] := 1.0; ELSE aOutput_y[3] := 0.0; END_IF;

(* Correct state estimate with observer gain L_obs *)
FOR iIdx := 0 TO 7 DO
    rTmpSum := aState_x_pred[iIdx];
    FOR jIdx := 0 TO 3 DO
        rTmpSum := rTmpSum + aMatrix_L_obs[iIdx, jIdx] * (aOutput_y[jIdx] -
            (aMatrix_C[jIdx, 0]*aState_x_pred[0] + aMatrix_C[jIdx, 1]*aState_x_pred[1] +
             aMatrix_C[jIdx, 2]*aState_x_pred[2] + aMatrix_C[jIdx, 3]*aState_x_pred[3] +
             aMatrix_C[jIdx, 4]*aState_x_pred[4] + aMatrix_C[jIdx, 5]*aState_x_pred[5] +
             aMatrix_C[jIdx, 6]*aState_x_pred[6] + aMatrix_C[jIdx, 7]*aState_x_pred[7]));
    END_FOR;
    aState_x_hat[iIdx] := rTmpSum;
END_FOR;
"""
    sections.append(s7)

    # -------------------------------------------------------------------------
    # SECTION 8: LOGIC PART 6 - RECEDING-HORIZON MPC SOLVER
    # -------------------------------------------------------------------------
    s8 = """(* ============================================================================================= *)
(* SECTION 6: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) QP SOLVER                         *)
(* ============================================================================================= *)
(* Determine Output Setpoints from Current FSM State *)
IF iFSM_State = 30 OR iFSM_State = 40 THEN
    aOutput_y_sp[0] := rActuatorFullStroke_mm / 1000.0; (* Full deploy: 0.580 m *)
    aOutput_y_sp[1] := 0.000;                           (* Target zero skew *)
    aOutput_y_sp[2] := 150.0E5;                         (* Nominal load pressure *)
    aOutput_y_sp[3] := 0.000;                           (* Lock pin unseated *)
ELSE
    aOutput_y_sp[0] := 0.000;                           (* Full stow: 0.000 m *)
    aOutput_y_sp[1] := 0.000;                           (* Target zero skew *)
    aOutput_y_sp[2] := 0.0;                             (* Zero load pressure *)
    aOutput_y_sp[3] := 1.000;                           (* Lock pin seated *)
END_IF;

(* Output Tracking Error *)
aOutput_y_error[0] := aOutput_y[0] - aOutput_y_sp[0];
aOutput_y_error[1] := aOutput_y[1] - aOutput_y_sp[1];
aOutput_y_error[2] := (aOutput_y[2] - aOutput_y_sp[2]) * 1.0E-6; (* Scale to MPa *)
aOutput_y_error[3] := aOutput_y[3] - aOutput_y_sp[3];

(* If MPC is enabled and system is healthy, solve Quadratic Program via Projected Gradient *)
IF NOT bGracefulDegradation AND bEnable THEN
    bMPC_Active := TRUE;

    (* Approximate Diagonal Hessian: H_ii = C_i^T * Q * C_i + R_i *)
    aHessian_diag[0] := aWeight_Q[1] * 0.0004 + aWeight_R[0]; (* EHSV current *)
    aHessian_diag[1] := aWeight_Q[2] * 0.0120 + aWeight_R[1]; (* Isolation valve *)
    aHessian_diag[2] := aWeight_Q[0] * 0.0085 + aWeight_R[2]; (* Directional valve *)
    aHessian_diag[3] := aWeight_Q[3] * 0.0450 + aWeight_R[3]; (* Tertiary solenoid *)

    (* Gradient g = B^T * C^T * Q * error + R * (u - u_prev) *)
    aGrad_g[0] := aWeight_Q[1] * aOutput_y_error[1] * 45.0 + aWeight_R[0] * aControl_du[0];
    aGrad_g[1] := aWeight_Q[2] * aOutput_y_error[2] * 0.08 + aWeight_R[1] * aControl_du[1];
    aGrad_g[2] := aWeight_Q[0] * aOutput_y_error[0] * 120.0 + aWeight_R[2] * aControl_du[2];
    aGrad_g[3] := aWeight_Q[3] * aOutput_y_error[3] * 15.0 + aWeight_R[3] * aControl_du[3];

    (* Iterative Projected Gradient Descent *)
    FOR iIterQP := 1 TO iMaxIterQP DO
        FOR iIdx := 0 TO 3 DO
            (* Step along negative gradient *)
            aStep_du[iIdx] := aControl_du[iIdx] - (rAlphaStep / aHessian_diag[iIdx]) * aGrad_g[iIdx];

            (* Enforce slew rate bounds [du_min, du_max] *)
            IF aStep_du[iIdx] > aLimit_du_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Max[iIdx];
            ELSIF aStep_du[iIdx] < aLimit_du_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_du_Min[iIdx];
            END_IF;

            (* Enforce absolute actuator limits [u_min, u_max] *)
            IF (aControl_u[iIdx] + aStep_du[iIdx]) > aLimit_u_Max[iIdx] THEN
                aStep_du[iIdx] := aLimit_u_Max[iIdx] - aControl_u[iIdx];
            ELSIF (aControl_u[iIdx] + aStep_du[iIdx]) < aLimit_u_Min[iIdx] THEN
                aStep_du[iIdx] := aLimit_u_Min[iIdx] - aControl_u[iIdx];
            END_IF;

            aControl_du[iIdx] := aStep_du[iIdx];
        END_FOR;
    END_FOR;

    (* Apply optimal incremental moves *)
    aControl_u[0] := aControl_u[0] + aControl_du[0];
    aControl_u[1] := aControl_u[1] + aControl_du[1];
    aControl_u[2] := aControl_u[2] + aControl_du[2];
    aControl_u[3] := aControl_u[3] + aControl_du[3];
ELSE
    (* Fallback Decoupled Control (Graceful Degradation) *)
    bMPC_Active := FALSE;

    (* Skew Suppression PID driving EHSV *)
    rTmpSum := (0.0 - rCowlSkewDeviation_mm);
    rPID_Integ_Skew := rPID_Integ_Skew + rTmpSum * tScanTime_s;
    IF rPID_Integ_Skew > 25.0 THEN rPID_Integ_Skew := 25.0; END_IF;
    IF rPID_Integ_Skew < -25.0 THEN rPID_Integ_Skew := -25.0; END_IF;
    aControl_u[0] := rPID_Kp_Skew * rTmpSum + rPID_Ki_Skew * rPID_Integ_Skew +
                     rPID_Kd_Skew * ((rTmpSum - rPID_PrevErr_Skew) / tScanTime_s);
    rPID_PrevErr_Skew := rTmpSum;

    IF aControl_u[0] > 40.0 THEN aControl_u[0] := 40.0; END_IF;
    IF aControl_u[0] < -40.0 THEN aControl_u[0] := -40.0; END_IF;
END_IF;
"""
    sections.append(s8)

    # -------------------------------------------------------------------------
    # SECTION 9: LOGIC PART 7 - TERTIARY LOCK INTERLOCK & FSM
    # -------------------------------------------------------------------------
    s9 = """(* ============================================================================================= *)
(* SECTION 7: FAR 25.933 TERTIARY LOCK INTERLOCK & MULTI-STAGE SEQUENCING FSM                   *)
(* ============================================================================================= *)
(* Triple Independent Safety Permissive Evaluation *)
(* Deploy Permissive requires: WOW (aircraft on ground) AND Reverse Throttle Angle > 18.5 deg   *)
(* AND Airspeed safe for reverse rollout AND Hydraulic supply pressure adequate                 *)
bDeployPermissiveGranted := bVoted_WOW AND
                            (rThrottleReverseAngle_deg >= 18.50) AND
                            (rAircraftAirspeed_kts <= 185.0) AND
                            (rVoted_HydSupplyPress_bar >= 170.0);

(* Monotonic State Elapsed Timer *)
IF iFSM_State = iPreviousFSM_State THEN
    rStateTimer_s := rStateTimer_s + tScanTime_s;
ELSE
    rStateTimer_s      := 0.0;
    iPreviousFSM_State := iFSM_State;
END_IF;

(* Multi-Stage Deterministic Finite State Machine *)
CASE iFSM_State OF
    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 0: STOWED_LOCKED (Standard In-Flight Cruise & Takeoff Configuration)                *)
    (* ----------------------------------------------------------------------------------------- *)
    0:
        rDeployIsolationValve_Pct := 0.00;          (* Hydraulic supply isolated & depressurized *)
        rDirectionalValve_Pct     := 0.00;          (* DCV in full stow detent *)
        rEHSV_CurrentCmd_mA       := 0.00;          (* EHSV null current *)
        bTertiaryLockSolenoidCmd  := FALSE;         (* Solenoid unpowered, pin engaged by spring *)
        bReverserFullyDeployed    := FALSE;
        bReverserFullyStowed      := TRUE;

        (* Detection of Uncommanded In-Flight Motion (FAR § 25.933 Catastrophic Fault) *)
        IF (rMeanCowlStroke_mm >= 4.00) OR (NOT bVoted_TertiaryLock_Seat) THEN
            bUncommandedMotionFault  := TRUE;
            iFSM_State               := 99;         (* EMERGENCY_SAFE_HOLD *)
            dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0001; (* UNCOMMANDED_DEPLOY_TRIP_HH *)
        END_IF;

        (* Transition to WOW_ARMED when touchdown confirmed and pilot pulls reverse lever *)
        IF bDeployPermissiveGranted AND bReverseThrustCommand THEN
            iFSM_State := 10;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: WOW_ARMED (Touchdown Verified, System Arming & Line Pre-charge)                 *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        rDeployIsolationValve_Pct := 100.0;         (* Energize hydraulic isolation valve *)
        rDirectionalValve_Pct     := 0.00;          (* Hold DCV in stow until locks fully release *)
        rEHSV_CurrentCmd_mA       := -5.00;         (* Slight stow bias to relieve shear pin friction *)
        bTertiaryLockSolenoidCmd  := FALSE;
        bReverserFullyStowed      := TRUE;

        (* Verify line pressurization before pulsing release solenoids *)
        IF (rVoted_HydSupplyPress_bar >= 185.0) AND (rStateTimer_s >= 0.120) THEN
            iFSM_State := 20;                       (* Advance to UNLOCK_SEQUENCE *)
        END_IF;

        (* Abort if pilot pushes throttle back forward *)
        IF rThrottleReverseAngle_deg < 10.0 THEN
            iFSM_State := 0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 20: UNLOCK_SEQUENCE (Tertiary Solenoid Energize & Primary Latch Camming)           *)
    (* ----------------------------------------------------------------------------------------- *)
    20:
        rDeployIsolationValve_Pct := 100.0;
        rDirectionalValve_Pct     := 0.00;
        bTertiaryLockSolenoidCmd  := TRUE;          (* Energize 28VDC dual-coil solenoid *)
        rUnlockPulseTimer_s       := rUnlockPulseTimer_s + tScanTime_s;

        (* Check proximity confirmation that pin has retracted *)
        IF NOT bVoted_TertiaryLock_Seat THEN
            (* Pin successfully pulled clear of transcowl collar *)
            rUnlockPulseTimer_s := 0.0;
            iUnlockRetryCount   := 0;
            iFSM_State          := 30;              (* Advance to TRANSLATING_DEPLOY *)
        ELSIF rUnlockPulseTimer_s >= 0.850 THEN
            (* Solenoid release timeout *)
            iUnlockRetryCount := iUnlockRetryCount + 1;
            IF iUnlockRetryCount >= 3 THEN
                (* Mechanical pin jam detected *)
                dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0008; (* TERTIARY_LOCK_JAM_TRIP *)
                iFSM_State               := 90;     (* Abort deploy *)
            ELSE
                rUnlockPulseTimer_s := 0.0;
                iFSM_State          := 10;          (* Cycle stow pressure relief and retry *)
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 30: TRANSLATING_DEPLOY (Transcowls Translating Aft, Blocker Doors Deploying)        *)
    (* ----------------------------------------------------------------------------------------- *)
    30:
        rDeployIsolationValve_Pct := 100.0;
        rDirectionalValve_Pct     := 100.0;         (* DCV full deploy direction *)
        bTertiaryLockSolenoidCmd  := TRUE;          (* Keep solenoid energized during travel *)
        bReverserFullyStowed      := FALSE;

        (* Transfer calculated MPC current to physical output *)
        rEHSV_CurrentCmd_mA := aControl_u[0];

        (* Check full stroke arrival (580 mm nominal travel) *)
        IF rMeanCowlStroke_mm >= 575.0 THEN
            iFSM_State := 40;                       (* Advance to FULLY_DEPLOYED_HOLD *)
        END_IF;

        (* Slew timeout supervision (max 1.8 seconds deploy time) *)
        IF rStateTimer_s >= 2.20 THEN
            dwTRAS_AlarmWord_Secondary := dwTRAS_AlarmWord_Secondary OR 16#0000_0002; (* SLOW_DEPLOY_TIMEOUT *)
            IF rMeanCowlStroke_mm < 450.0 THEN
                iFSM_State := 90;                   (* Abort incomplete deploy *)
            ELSE
                iFSM_State := 40;                   (* Accept partial hold if above 450 mm *)
            END_IF;
        END_IF;

        (* Retract command from pilot *)
        IF rThrottleReverseAngle_deg < 10.0 THEN
            iFSM_State := 50;                       (* Transition to STOW_COMMAND *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 40: FULLY_DEPLOYED_HOLD (Maximum Reverse Thrust Maintained)                         *)
    (* ----------------------------------------------------------------------------------------- *)
    40:
        rDeployIsolationValve_Pct := 100.0;
        rDirectionalValve_Pct     := 85.0;          (* Moderate holding pressure against aerodynamic blowback *)
        rEHSV_CurrentCmd_mA       := 0.00;          (* Centered EHSV *)
        bTertiaryLockSolenoidCmd  := TRUE;
        bReverserFullyDeployed    := TRUE;
        bReverserFullyStowed      := FALSE;

        (* Return to forward idle command initiates stow sequence *)
        IF (rThrottleReverseAngle_deg < 12.0) OR (NOT bReverseThrustCommand) THEN
            iFSM_State := 50;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 50: STOW_COMMAND (Transcowls Retracting Forward to Nacelle Stowed Position)         *)
    (* ----------------------------------------------------------------------------------------- *)
    50:
        rDeployIsolationValve_Pct := 100.0;
        rDirectionalValve_Pct     := 0.00;          (* DCV in full STOW direction *)
        bTertiaryLockSolenoidCmd  := TRUE;          (* Keep pin pulled until near stowed position *)
        bReverserFullyDeployed    := FALSE;

        (* MPC or Fallback Skew compensation active during retraction *)
        rEHSV_CurrentCmd_mA := aControl_u[0];

        (* When stroke drops below 25 mm, release solenoid so pin rides collar ramp *)
        IF rMeanCowlStroke_mm <= 25.0 THEN
            bTertiaryLockSolenoidCmd := FALSE;
            iFSM_State               := 60;         (* Advance to PRIMARY_LOCK_LATCH *)
        END_IF;

        (* Retract timeout monitoring (max 2.4 seconds stow time) *)
        IF rStateTimer_s >= 3.00 THEN
            dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0010; (* STOW_TIMEOUT_EXCEEDED *)
            iFSM_State               := 90;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 60: PRIMARY_LOCK_LATCH (Primary Over-Center Latches Capturing Sleeves)              *)
    (* ----------------------------------------------------------------------------------------- *)
    60:
        rDeployIsolationValve_Pct := 100.0;
        rDirectionalValve_Pct     := 0.00;          (* Full pressure driving sleeves home into bumpers *)
        rEHSV_CurrentCmd_mA       := -15.0;         (* Hard stow bias *)
        bTertiaryLockSolenoidCmd  := FALSE;

        (* Verify primary mechanical latches engaged *)
        IF bVoted_PrimaryLock_Latch AND (rMeanCowlStroke_mm <= 2.50) THEN
            iFSM_State := 70;                       (* Advance to VERIFY_STOWED *)
        END_IF;

        IF rStateTimer_s >= 1.50 THEN
            dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0020; (* PRIMARY_LATCH_FAIL_HH *)
            iFSM_State               := 90;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 70: VERIFY_STOWED (Tertiary Pin Seated, Depressurizing & Safe Isolation)            *)
    (* ----------------------------------------------------------------------------------------- *)
    70:
        bTertiaryLockSolenoidCmd := FALSE;
        rLockVerifyTimer_s       := rLockVerifyTimer_s + tScanTime_s;

        IF bVoted_TertiaryLock_Seat AND bVoted_PrimaryLock_Latch AND (rMeanCowlStroke_mm <= 2.00) THEN
            (* All mechanical locking barriers fully seated *)
            IF rLockVerifyTimer_s >= 0.350 THEN
                rDeployIsolationValve_Pct := 0.00;  (* Depressurize TRAS hydraulic circuit *)
                rDirectionalValve_Pct     := 0.00;
                rEHSV_CurrentCmd_mA       := 0.00;
                bReverserFullyStowed      := TRUE;
                rLockVerifyTimer_s        := 0.0;
                iFSM_State                := 0;      (* Return to cold STOWED_LOCKED *)
            END_IF;
        ELSIF rLockVerifyTimer_s >= 2.00 THEN
            (* Pin failed to seat into collar *)
            dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0040; (* TERTIARY_PIN_SEAT_FAIL_HH *)
            iFSM_State               := 90;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 90: FAULT_ABORT_STOW (Emergency Hydraulic Closure Due to Anomaly)                   *)
    (* ----------------------------------------------------------------------------------------- *)
    90:
        rDeployIsolationValve_Pct := 100.0;         (* Full hydraulic power *)
        rDirectionalValve_Pct     := 0.00;          (* Full forward stow *)
        rEHSV_CurrentCmd_mA       := -40.0;         (* Max saturated restow drive *)
        bTertiaryLockSolenoidCmd  := FALSE;         (* Drop solenoid power to allow spring capture *)
        bReverserFullyDeployed    := FALSE;

        IF bVoted_TertiaryLock_Seat AND (rMeanCowlStroke_mm <= 2.00) THEN
            rDeployIsolationValve_Pct := 0.00;
            rEHSV_CurrentCmd_mA       := 0.00;
            bReverserFullyStowed      := TRUE;
            iFSM_State                := 0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 99: EMERGENCY_SAFE_HOLD (Flight Containment Mode - Pilot Caution & Thrust Cut)      *)
    (* ----------------------------------------------------------------------------------------- *)
    99:
        (* Immediate hydraulic lock to prevent further cowl aerodynamic migration *)
        rDeployIsolationValve_Pct := 100.0;
        rDirectionalValve_Pct     := 0.00;          (* Force full stow *)
        rEHSV_CurrentCmd_mA       := -40.0;
        bTertiaryLockSolenoidCmd  := FALSE;
        bReverserFullyDeployed    := FALSE;
        bReverserFullyStowed      := FALSE;
        bUncommandedMotionFault   := TRUE;
        dwTRAS_StatusWord         := dwTRAS_StatusWord OR 16#8000_0000; (* Bit 31: EMERGENCY_TRIP *)
END_CASE;
"""
    sections.append(s9)

    # -------------------------------------------------------------------------
    # SECTION 10: LOGIC PART 8 - ISA-18.2 ALARMS & DIAGNOSTIC PACKING
    # -------------------------------------------------------------------------
    s10 = """(* ============================================================================================= *)
(* SECTION 8: ISA-18.2 MULTI-TIERED ALARM MATRIX & DIAGNOSTIC WORD BIT-PACKING                  *)
(* ============================================================================================= *)
(* 1. Hydraulic Supply Pressure Alarms *)
IF rVoted_HydSupplyPress_bar < 130.0 THEN
    dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0100; (* Bit 8: HYD_SUPPLY_PRESS_LL_TRIP *)
ELSIF rVoted_HydSupplyPress_bar < 170.0 THEN
    dwTRAS_AlarmWord_Secondary := dwTRAS_AlarmWord_Secondary OR 16#0000_0010; (* Bit 4: HYD_SUPPLY_PRESS_L_WARN *)
END_IF;

(* 2. Hydraulic Return Line Backpressure Alarms *)
IF rVoted_HydReturnPress_bar > 12.0 THEN
    dwTRAS_AlarmWord_Primary := dwTRAS_AlarmWord_Primary OR 16#0000_0200; (* Bit 9: HYD_RETURN_PRESS_HH_TRIP *)
ELSIF rVoted_HydReturnPress_bar > 7.5 THEN
    dwTRAS_AlarmWord_Secondary := dwTRAS_AlarmWord_Secondary OR 16#0000_0020; (* Bit 5: HYD_RETURN_PRESS_H_WARN *)
END_IF;

(* 3. Hydraulic Fluid Thermal Boundary Alarms *)
IF rHydFluidTemp_degC > 110.0 THEN
    dwTRAS_AlarmWord_Secondary := dwTRAS_AlarmWord_Secondary OR 16#0000_0040; (* Bit 6: HYD_FLUID_OVERTEMP_H *)
ELSIF rHydFluidTemp_degC < -25.0 THEN
    dwTRAS_AlarmWord_Secondary := dwTRAS_AlarmWord_Secondary OR 16#0000_0080; (* Bit 7: HYD_FLUID_COLD_SOAK_L *)
END_IF;

(* 4. Weight-On-Wheels (WOW) Sensor Discordance *)
IF (bWOW_Channel_A <> bWOW_Channel_B) OR (bWOW_Channel_B <> bWOW_Channel_C) THEN
    dwTRAS_AlarmWord_Secondary := dwTRAS_AlarmWord_Secondary OR 16#0000_0100; (* Bit 8: WOW_SENSOR_DISCORDANCE *)
END_IF;

(* Master Alarm Acknowledgment & Latching Reset *)
IF bMasterResetAlarms THEN
    dwTRAS_AlarmWord_Primary   := 16#0000_0000;
    dwTRAS_AlarmWord_Secondary := 16#0000_0000;
    bSkewShutdownActive        := FALSE;
    bUncommandedMotionFault    := FALSE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 5. 32-Bit TRAS Operational Status Word Packing (dwTRAS_StatusWord)                            *)
(* --------------------------------------------------------------------------------------------- *)
(* Bits 0..7  : Current FSM State Integer [0..99] *)
(* Bit 8      : bDeployPermissiveGranted *)
(* Bit 9      : bReverserFullyDeployed *)
(* Bit 10     : bReverserFullyStowed *)
(* Bit 11     : bTertiaryLockSolenoidCmd *)
(* Bit 12     : bVoted_TertiaryLock_Seat *)
(* Bit 13     : bVoted_PrimaryLock_Latch *)
(* Bit 14     : bVoted_WOW *)
(* Bit 15     : bMPC_Active *)
(* Bit 16     : bGracefulDegradation *)
(* Bit 17     : bSkewShutdownActive *)
(* Bit 18     : bUncommandedMotionFault *)
(* Bit 31     : Master Emergency Trip Flag *)
dwTRAS_StatusWord := INT_TO_DWORD(iFSM_State);
IF bDeployPermissiveGranted THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0000_0100; END_IF;
IF bReverserFullyDeployed   THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0000_0200; END_IF;
IF bReverserFullyStowed     THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0000_0400; END_IF;
IF bTertiaryLockSolenoidCmd THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0000_0800; END_IF;
IF bVoted_TertiaryLock_Seat THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0000_1000; END_IF;
IF bVoted_PrimaryLock_Latch THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0000_2000; END_IF;
IF bVoted_WOW               THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0000_4000; END_IF;
IF bMPC_Active              THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0000_8000; END_IF;
IF bGracefulDegradation     THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0001_0000; END_IF;
IF bSkewShutdownActive      THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0002_0000; END_IF;
IF bUncommandedMotionFault  THEN dwTRAS_StatusWord := dwTRAS_StatusWord OR 16#0004_0000; END_IF;

END_FUNCTION_BLOCK
"""
    sections.append(s10)

    full_code = "".join(sections)
    return full_code

if __name__ == "__main__":
    code = build_tras_block()
    print(f"Total ST code length: {len(code)} characters")
