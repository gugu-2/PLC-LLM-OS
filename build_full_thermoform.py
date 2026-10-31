# build_full_thermoform.py
import json
import re
import sys

def build_full_dataset():
    # 1. Header
    header = """FUNCTION_BLOCK FB_Plastics_RotaryThermoforming_MultiStation
(*
 ====================================================================================================
  PROJECT:       HEAVY COMMERCIAL PLASTICS & POLYMER PROCESSING AUTOMATION
  SUBSYSTEM:     4-STATION ROTARY CAROUSEL HEAVY SHEET THERMOFORMING MACHINE
                 (AUTOMOTIVE DOOR TRIMS, REFRIGERATOR INNER LINERS, AEROSPACE PANELS)
  TECHNOLOGY:    MULTI-ZONE CERAMIC QUARTZ RADIANT HEATING OVEN (96 INDEPENDENT ZONES),
                 HIGH-SPEED SERVO PLUG ASSIST KINEMATIC LINEAR ACTUATOR, DYNAMIC BUBBLE
                 PRE-INFLATION AIR TABLE, HIGH-VACUUM FAST EVACUATION SURGE TANKS,
                 2oo3 TRIPLE MODULAR REDUNDANT SENSING, DISCRETE STATE-SPACE & RECEDING HORIZON MPC
  IEC STANDARD:  IEC 61131-3 3RD EDITION COMPLIANT (DETERMINISTIC EMBEDDED REAL-TIME CONTROL)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX-PERSONA)
  SCAN CYCLE Ts: 5.000 MILLISECOND SYNCHRONOUS PLC SCAN TICK [ms]
 ====================================================================================================
  CYBER-PHYSICAL SYSTEM OVERVIEW & MASS-PRODUCTION KINETICS:
  ----------------------------------------------------------------------------------------------------
  1. 4-Station Continuous Rotary Carousel Architecture:
     - Station 1: Raw Polymer Sheet De-Stacking, Optical Centering & Pneumatic Clamping Frame Lock.
                  Automated vacuum suction destacker feeds heavy polymer sheets (ABS, HIPS, TPO, PC,
                  thickness 1.5 to 6.0 [mm], area up to 2.4 x 1.6 [m]). Clamping frame secures sheet
                  perimeter with pneumatic toggle cylinders exerting > 120 [kN] total perimeter hold.
     - Station 2: Multi-Zone Dual Radiant Quartz Heating Oven (48 Top Zones + 48 Bottom Zones).
                  Top/bottom radiant quartz ceramic heating arrays emit targeted infrared radiation
                  (peak wavelength 1.5 to 4.0 [um] tuned directly to the C-H polymer vibrational
                  absorption band). Shaping thermal gradient across the sheet ensures uniform corner
                  flow without localized polymer degradation or scorching.
     - Station 3: Thermoforming Station with Upper Platen Servo Plug Assist & Lower Vacuum Box.
                  Hydraulic / electric toggle mechanism locks clamping platens with 1,200 [kN] tonnage.
                  Lower table injects controlled pneumatic air pulse (0.1 to 0.4 [bar]) forming a
                  hemispherical pre-blow bubble. Upper kinematic servo plug assist (45 [kW] linear motor
                  with syntactic foam plug, 900 [mm] stroke, 1.2 [m/s] downstroke) penetrates deep into
                  the bubble cavity. Multi-stage vacuum surge tanks evacuate mold cavity to < 50 [mbar]
                  absolute pressure in < 350 [ms], drawing sheet against chilled aluminum mold tools.
     - Station 4: Ultrasonic / CNC Perimeter Trimming & Finished Component Egress.
                  Multi-axis robotic ultrasonic knife executes net-shape edge trimming and aperture
                  punching. Finished automotive door trim is transferred to outgoing collation conveyor.
  
  2. Rheological & Viscoelastic Physics of Hot Heavy Thermoplastic Sheets:
     - Non-linear viscoelastic constitutive behavior modeled via generalized Maxwell-Weichert model:
         sigma(t) = Integral_{0}^{t} G(t - s) * (d epsilon / ds) ds
         G(t) = G_e + Sum_{m=1}^{M} G_m * exp(-t / tau_m)
     - Temperature shift factor follows the Arrhenius / Williams-Landel-Ferry (WLF) formulation:
         ln(a_T) = -C1 * (T - T_ref) / (C2 + T - T_ref)
     - Catenary Thermal Sheet Sag Kinetics:
         Under gravitational load and exponential softening above glass transition (T_g) / melt (T_m),
         the sheet sags into a catenary profile:
           z(x) = (H_sag / (cosh(L / (2 * a)) - 1)) * (cosh(x / a) - 1)
           h_sag(t) approx= (rho * g * L^2) / (8 * sigma_yield(T))
         where sigma_yield(T) decays exponentially with core temperature:
           sigma_yield(T) = sigma_0 * exp(-beta_sag * (T - T_ref))
         Excessive sag (> 75.0 [mm]) creates catastrophic fire risk by approaching bottom quartz
         heaters, triggering automated pneumatic fire shield deployment.
  
  3. Dynamic Bubble Pre-Blow Thermodynamics & Spherical Cap Geometry:
     - Closed-loop pneumatic air cushion pulse inflates sheet into a uniform upward bubble:
         V_bubble(h) = (pi * h / 6) * (3 * r_aperture^2 + h^2)
         R_curvature(h) = (h / 2) + (r_aperture^2 / (2 * h))
         sigma_membrane = (P_bubble * R_curvature) / (2 * t_sheet)
     - Equi-biaxial pre-stretching equalizes polymer strain energy, preventing corner thinning defects
       and ensuring finished automotive door trim corner wall thickness remains within +/- 0.10 [mm].
  
  4. High-Speed Kinematic Servo Plug Assist & Cavity Evacuation:
     - Syntactic foam plug (low thermal conductivity k < 0.12 [W/(m*K)]) minimizes localized sheet
       freezing upon contact. Plug drives into cavity following an S-curve motion profile with
       controlled jerk:
         z_plug(t), v_plug(t), a_plug(t)
     - Contact friction force dynamics:
         F_plug = mu_coulomb * F_normal + A_contact(z) * eta_shear(gamma_dot, T) * (v_plug / t_sheet)
     - Vacuum Evacuation Choked / Sub-Sonic Flow:
         dP_cavity / dt = - (C_d * A_ports / V_cavity) * P_cavity * sqrt((gamma / (R_gas * T)) * ...)
  
  5. Discrete State-Space Formulation (16 States, 8 Actuators):
     - x[k+1] = A * x[k] + B * u[k]
     - Receding-Horizon Model Predictive Control (MPC) quadratic cost optimization:
         J = Sum_{p=1}^{N_p} ((x_{k+p} - x_ref)^T * Q * (x_{k+p} - x_ref)) + Sum_{p=0}^{N_c-1} (delta_u^T * R * delta_u)
     - Real-time active-set gradient updates with strict physical constraint clamping.
 ====================================================================================================
*)"""

    # 2. VAR_INPUT
    var_input = """VAR_INPUT
    (* ================================================================================= *)
    (* MASTER SYSTEM CONTROL & DIGITAL SUPERVISORY COMMANDS                              *)
    (* ================================================================================= *)
    bEnableMaster                   : BOOL;     (* Master automated thermoforming cell sequence enable [BOOL] *)
    bAutoCycleStart                 : BOOL;     (* Automatic 4-station continuous cycle start strobe [BOOL] *)
    bCycleHaltRequest               : BOOL;     (* Controlled normal cycle stop at station index completion [BOOL] *)
    bSafetyEStop_OK                 : BOOL;     (* Dual-channel emergency stop safety circuit healthy [BOOL] *)
    bSafetyLightCurtain_OK          : BOOL;     (* Station 1 and Station 4 optical perimeter safety light curtains clear [BOOL] *)
    bSafetyEnclosureDoors_OK        : BOOL;     (* Interlocked heavy acoustic & thermal safety enclosure doors locked [BOOL] *)
    bAckAlarm                       : BOOL;     (* Operator master alarm acknowledge pushbutton command [BOOL] *)
    bOvenExhaustFanRunning          : BOOL;     (* Thermal oven catalytic VOC exhaust ventilation fan running [BOOL] *)
    bCoolingWaterFlow_OK            : BOOL;     (* MTC closed-loop cooling water circuit flow switch healthy [BOOL] *)
    bCompressedAirSupply_OK         : BOOL;     (* Main pneumatic air reservoir pressure switch healthy (> 6.0 bar) [BOOL] *)

    (* ================================================================================= *)
    (* POLYMER RECIPE & THERMAL PROCESS SPECIFICATIONS                                   *)
    (* ================================================================================= *)
    nMaterialTypeID                 : INT;      (* Polymer resin grade: 1=ABS, 2=HIPS, 3=TPO, 4=Polycarbonate [-] *)
    rSheetNominalThickness_mm       : REAL;     (* Raw extruded polymer sheet nominal thickness [mm] *)
    rSheetWidth_mm                  : REAL;     (* Raw sheet cut width dimension [mm] *)
    rSheetLength_mm                 : REAL;     (* Raw sheet cut length dimension [mm] *)
    rTargetFormingTemp_degC         : REAL;     (* Target viscoelastic rubbery plateau forming temperature setpoint [deg C] *)
    rMaxAllowableSag_mm             : REAL;     (* Maximum allowable sheet thermal catenary sag limit before trip [mm] *)
    rPreBlowBubbleApexSP_mm         : REAL;     (* Pneumatic pre-blow bubble apex height target setpoint [mm] *)
    rPreBlowPressureSP_bar          : REAL;     (* Pneumatic pre-blow pulse line pressure target setpoint [bar] *)
    rPlugStrokeSP_mm                : REAL;     (* Servo plug assist final penetration stroke depth setpoint [mm] *)
    rPlugVelocitySP_ms              : REAL;     (* Servo plug assist maximum downstroke penetration velocity [m/s] *)
    rCavityVacuumSP_mbar            : REAL;     (* Target mold forming cavity absolute vacuum pressure setpoint [mbar] *)
    rMoldSurfaceTempSP_degC         : REAL;     (* Mold temperature controller (MTC) aluminum surface target [deg C] *)
    rCoolingDwellTimeSP_s           : REAL;     (* In-mold chilled air vortex cooling dwell duration setpoint [s] *)
    rCycleTimeTarget_s              : REAL;     (* Nominal 4-station carousel index cycle duration target [s] *)
    rScanCycleTime_ms               : REAL;     (* Synchronous controller scan cycle period [ms] *)

    (* ================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: SHEET CATENARY SAG OPTICAL LASER SENSORS [mm]     *)
    (* ================================================================================= *)
    rSheetSag_ChA_mm                : REAL;     (* High-precision optical laser distance sensor Ch A [mm] *)
    rSheetSag_ChB_mm                : REAL;     (* High-precision optical laser distance sensor Ch B [mm] *)
    rSheetSag_ChC_mm                : REAL;     (* High-precision optical laser distance sensor Ch C [mm] *)

    (* ================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: MOLD CAVITY VACUUM ABSOLUTE TRANSMITTERS [mbar]   *)
    (* ================================================================================= *)
    rCavityVacuum_ChA_mbar          : REAL;     (* Piezoresistive mold cavity absolute vacuum transmitter Ch A [mbar] *)
    rCavityVacuum_ChB_mbar          : REAL;     (* Piezoresistive mold cavity absolute vacuum transmitter Ch B [mbar] *)
    rCavityVacuum_ChC_mbar          : REAL;     (* Piezoresistive mold cavity absolute vacuum transmitter Ch B [mbar] *)

    (* ================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: SHEET SURFACE INFRARED PYROMETERS [deg C]        *)
    (* ================================================================================= *)
    rSheetPyrometer_ChA_degC        : REAL;     (* Non-contact high-speed infrared pyrometer Ch A [deg C] *)
    rSheetPyrometer_ChB_degC        : REAL;     (* Non-contact high-speed infrared pyrometer Ch B [deg C] *)
    rSheetPyrometer_ChC_degC        : REAL;     (* Non-contact high-speed infrared pyrometer Ch C [deg C] *)

    (* ================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY: SERVO PLUG ASSIST LOAD CELL FORCE SENSORS [kN]    *)
    (* ================================================================================= *)
    rPlugForce_ChA_kN               : REAL;     (* Dynamic piezoelectric quartz force link load cell Ch A [kN] *)
    rPlugForce_ChB_kN               : REAL;     (* Dynamic piezoelectric quartz force link load cell Ch B [kN] *)
    rPlugForce_ChC_kN               : REAL;     (* Dynamic piezoelectric quartz force link load cell Ch C [kN] *)

    (* ================================================================================= *)
    (* AUXILIARY PROCESS TRANSDUCERS & KINEMATIC ACTUATOR FEEDBACKS                      *)
    (* ================================================================================= *)
    rVacuumSurgeTankPres_mbar       : REAL;     (* Primary vacuum surge buffer reservoir absolute pressure [mbar] *)
    rPreBlowLineSupplyPres_bar      : REAL;     (* High-flow pneumatic air cushion supply manifold pressure [bar] *)
    rCarouselAngle_deg              : REAL;     (* Rotary carousel 4-station high-resolution absolute encoder angle [deg] *)
    rCarouselVelocity_degs          : REAL;     (* Rotary carousel indexing drive angular velocity [deg/s] *)
    rPlugActualPos_mm               : REAL;     (* Servo plug assist linear absolute optical glass scale position [mm] *)
    rPlugActualVel_ms               : REAL;     (* Servo plug assist linear motor actual velocity feedback [m/s] *)
    rPlatenTonnageActual_kN         : REAL;     (* Hydraulic toggle mold platen locking tonnage transducer [kN] *)
    rClampFramePressure_bar         : REAL;     (* Sheet perimeter pneumatic clamping frame locking pressure [bar] *)
    rMTC_SupplyTemp_degC            : REAL;     (* Mold temperature controller circulating thermal fluid supply temp [deg C] *)
    rMTC_ReturnTemp_degC            : REAL;     (* Mold temperature controller circulating thermal fluid return temp [deg C] *)
    rMTC_FluidFlowRate_Lmin         : REAL;     (* Mold temperature controller fluid circuit volumetric flow [L/min] *)
    rChilledAirSupplyPres_bar       : REAL;     (* In-mold vortex chilled air cooling nozzle header pressure [bar] *)
    rTrimRobotArmPosition_mm        : REAL;     (* Station 4 robotic trimming arm Cartesian tool center point [mm] *)

    (* ================================================================================= *)
    (* 96-ZONE QUARTZ RADIANT HEATING ARRAY CURRENT SENSOR TELEMETRY [A]                 *)
    (* ================================================================================= *)
    aHeaterCurrent_Top_A            : ARRAY[1..48] OF REAL; (* Top quartz ceramic heating zones current feedback [A] *)
    aHeaterCurrent_Bot_A            : ARRAY[1..48] OF REAL; (* Bottom quartz ceramic heating zones current feedback [A] *)

    (* ================================================================================= *)
    (* MANUAL OPERATOR MAINTENANCE JOG & STEP OVERRIDE SIGNALS                          *)
    (* ================================================================================= *)
    bManualModeSelected             : BOOL;     (* Manual maintenance commissioning mode active [BOOL] *)
    bManualJogCarousel              : BOOL;     (* Manual jog rotary carousel forward command [BOOL] *)
    bManualJogPlugDown              : BOOL;     (* Manual jog servo plug assist downwards command [BOOL] *)
    bManualJogPlugUp                : BOOL;     (* Manual jog servo plug assist upwards command [BOOL] *)
    bManualToggleClampFrame         : BOOL;     (* Manual toggle sheet holding clamp frame lock [BOOL] *)
    bManualFireShieldTest           : BOOL      (* Manual emergency pneumatic fire shield drop test [BOOL] *)
END_VAR"""

    # 3. VAR_OUTPUT
    var_output = """VAR_OUTPUT
    (* ================================================================================= *)
    (* 96-ZONE CERAMIC QUARTZ RADIANT HEATER PWM DUTY CYCLE COMMANDS [%]                *)
    (* ================================================================================= *)
    aZoneDuty_Top_pct               : ARRAY[1..48] OF REAL; (* Top quartz array zones PWM duty cycle command [0.0..100.0 %] *)
    aZoneDuty_Bot_pct               : ARRAY[1..48] OF REAL; (* Bottom quartz array zones PWM duty cycle command [0.0..100.0 %] *)

    (* ================================================================================= *)
    (* 4-STATION ROTARY CAROUSEL MOTION ACTUATOR TRAJECTORIES                           *)
    (* ================================================================================= *)
    rCarouselTorqueCmd_Nm           : REAL;     (* Rotary carousel indexing servo motor torque feedforward [Nm] *)
    rCarouselVelocityCmd_degs       : REAL;     (* Rotary carousel indexing servo velocity trajectory command [deg/s] *)
    bCarouselBrakeRelease           : BOOL;     (* Rotary carousel heavy mechanical fail-safe holding brake release *)
    bCarouselIndexComplete          : BOOL;     (* Rotary carousel 90-degree indexing motion complete pulse *)

    (* ================================================================================= *)
    (* HIGH-SPEED SERVO PLUG ASSIST MOTION & TORQUE ACTUATOR COMMANDS                   *)
    (* ================================================================================= *)
    rPlugPosCmd_mm                  : REAL;     (* Servo plug assist linear position trajectory setpoint [mm] *)
    rPlugVelCmd_ms                  : REAL;     (* Servo plug assist linear velocity feedforward trajectory [m/s] *)
    rPlugTorqueLimit_Nm             : REAL;     (* Servo plug assist active torque clamping limit for collision safety [Nm] *)
    bPlugAssistInPosition           : BOOL;     (* Servo plug assist has achieved target penetration stroke depth *)
    bPlugAssistRetractedHome        : BOOL;     (* Servo plug assist retracted completely clear to home position *)

    (* ================================================================================= *)
    (* FORMING FLUID POWER & PNEUMATIC/VACUUM PROPORTIONAL ACTUATORS                    *)
    (* ================================================================================= *)
    rPreBlowValveCmd_pct            : REAL;     (* Pneumatic air cushion bubble pre-inflation proportional valve [0..100 %] *)
    bPreBlowPulseSolenoid           : BOOL;     (* High-speed pneumatic directional solenoid for fast bubble pre-blow *)
    rVacuumProportionalValve_pct    : REAL;     (* Mold cavity vacuum evacuation proportional ramping valve [0..100 %] *)
    bVacuumFastDumpSolenoid         : BOOL;     (* Mold cavity high-vacuum fast evacuation surge tank solenoid *)
    rPlatenToggleHydValve_pct       : REAL;     (* Mold closing toggle mechanism hydraulic proportional valve [0..100 %] *)
    bPlatenTonnageLocked            : BOOL;     (* Mold platen toggle mechanism locked at full forming tonnage *)
    bChilledAirCoolingJet           : BOOL;     (* Mold cavity internal vortex chilled air jet cooling solenoid *)
    bMoldEjectorPinExtend           : BOOL;     (* Mold aluminum tool mechanical stripper ejector pins extend *)
    bMoldVacuumVentValve            : BOOL;     (* Mold cavity atmospheric vacuum breaking vent valve *)

    (* ================================================================================= *)
    (* STATION 1 & STATION 4 MATERIAL HANDLING & TRIMMING COMMANDS                      *)
    (* ================================================================================= *)
    bClampFrameLockSol              : BOOL;     (* Station 1 sheet perimeter holding clamp frame pneumatic toggle lock *)
    bSheetDestackerVacuumOn         : BOOL;     (* Station 1 raw polymer sheet de-stacker suction cups vacuum enable *)
    bStation4TrimArmEnable          : BOOL;     (* Station 4 multi-axis robotic ultrasonic perimeter trimmer enable *)
    bStation4TrimCycleStart         : BOOL;     (* Station 4 robotic trimming execution cycle start trigger *)
    bFinishedPartUnloadReady        : BOOL;     (* Finished automotive trim part ready for robotic egress collation *)

    (* ================================================================================= *)
    (* SAFETY SHIELD & EMERGENCY MITIGATION ACTUATORS                                    *)
    (* ================================================================================= *)
    bOvenFireShieldDrop             : BOOL;     (* Emergency pneumatic radiant oven thermal fire shield drop solenoid *)
    bOvenExhaustDamperOpen          : BOOL;     (* Emergency oven high-temperature exhaust thermal damper open *)

    (* ================================================================================= *)
    (* OPERATIONAL FINITE STATE MACHINE (FSM) TELEMETRY & STATUS                         *)
    (* ================================================================================= *)
    nActiveFSMState                 : INT;      (* Active thermoforming machine operational state index [0..12] *)
    sActiveStateDesc                : STRING[80]; (* Human-readable diagnostic string description of active state *)
    rStateElapsedTimer_s            : REAL;     (* Elapsed execution duration in current active state [s] *)
    rOverallCycleTimer_s            : REAL;     (* Overall 4-station carousel machine cycle elapsed timer [s] *)

    (* ================================================================================= *)
    (* 2oo3 TMR VALIDATED SYNTHETIC PROCESS SIGNALS                                     *)
    (* ================================================================================= *)
    rVotedSheetSag_mm               : REAL;     (* 2oo3 TMR validated polymer sheet thermal catenary sag [mm] *)
    rVotedSheetTemp_degC            : REAL;     (* 2oo3 TMR validated polymer sheet infrared surface temperature [deg C] *)
    rVotedCavityVacuum_mbar         : REAL;     (* 2oo3 TMR validated mold forming cavity absolute vacuum [mbar] *)
    rVotedPlugForce_kN              : REAL;     (* 2oo3 TMR validated servo plug assist deep-draw resistance force [kN] *)

    (* ================================================================================= *)
    (* CYBER-PHYSICAL IN-LINE PART QUALITY & MODEL ESTIMATORS                            *)
    (* ================================================================================= *)
    rPredictedMinWall_mm            : REAL;     (* Real-time observer calculated critical corner minimum wall thickness [mm] *)
    rPredictedMaxWall_mm            : REAL;     (* Real-time observer calculated flange perimeter maximum wall thickness [mm] *)
    rEstBubbleVolume_L              : REAL;     (* Real-time observer calculated pneumatic pre-blow bubble volume [L] *)
    rEstBubbleApex_mm               : REAL;     (* Real-time observer calculated pre-blow bubble apex displacement [mm] *)
    rMPCCostResidual                : REAL;     (* Model Predictive Control receding-horizon quadratic cost residual *)
    bMPCOptimizerConverged          : BOOL;     (* Model Predictive Control active-set solver convergence flag *)

    (* ================================================================================= *)
    (* ISA-18.2 MULTI-TIERED ALARM & DIAGNOSTIC BIT-PACKED WORDS                         *)
    (* ================================================================================= *)
    dwAlarmsGroup1                  : DWORD;    (* Category 1: Critical safety, fire hazard & platen collision trip alarms *)
    dwAlarmsGroup2                  : DWORD;    (* Category 2: Process deviation, vacuum shortfall & wall thickness defects *)
    dwWarningsGroup1                : DWORD;    (* Category 3: Preventive maintenance, sensor TMR degradation & heater health *)
    dwStatusWord                    : DWORD     (* Subsystem operational telemetry, interlocking status & sequence readiness *)
END_VAR"""

    # 4. VAR internal declarations
    var_internal = """VAR
    (* ================================================================================= *)
    (* DISCRETE STATE-SPACE CYBER-PHYSICAL MATRICES (16 STATES, 8 ACTUATOR INPUTS)       *)
    (*   x[k+1] = A * x[k] + B * u[k]                                                    *)
    (*   y[k]   = C * x[k] + D * u[k]                                                    *)
    (* ================================================================================= *)
    aMatrix_A                       : ARRAY[1..16, 1..16] OF REAL;  (* Continuous-to-discrete 16x16 system dynamics matrix *)
    aMatrix_B                       : ARRAY[1..16, 1..8] OF REAL;   (* Discrete 16x8 actuator input coupling matrix *)
    aMatrix_C                       : ARRAY[1..16, 1..16] OF REAL;  (* Discrete 16x16 measurement state mapping matrix *)
    aMatrix_D                       : ARRAY[1..16, 1..8] OF REAL;   (* Discrete 16x8 direct feedthrough matrix *)

    (* State and Actuator Vectors *)
    aState_x                        : ARRAY[1..16] OF REAL;         (* Current estimated cyber-physical state vector *)
    aState_x_next                   : ARRAY[1..16] OF REAL;         (* Predicted next-step state vector *)
    aState_ref                      : ARRAY[1..16] OF REAL;         (* Active setpoint reference trajectory vector *)
    aInput_u                        : ARRAY[1..8] OF REAL;          (* Current actuator command vector *)
    aOutput_y                       : ARRAY[1..16] OF REAL;         (* Current model output observation vector *)
    aOptimal_u                      : ARRAY[1..8] OF REAL;          (* Optimal control actions computed by MPC solver *)
    aDelta_u                        : ARRAY[1..8] OF REAL;          (* Actuator rate-of-change vector *)
    bStateSpaceInitialized          : BOOL := FALSE;                (* State-space matrices initialized latch *)

    (* ================================================================================= *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION MATRICES             *)
    (* Cost Formulation: J = Sum(e^T * Q * e) + Sum(du^T * R * du) + (e_N^T * P * e_N)   *)
    (* ================================================================================= *)
    aMatrix_Q                       : ARRAY[1..16, 1..16] OF REAL;  (* 16x16 State error penalty weighting matrix *)
    aMatrix_R                       : ARRAY[1..8, 1..8] OF REAL;    (* 8x8 Actuator effort rate penalty weighting matrix *)
    aMatrix_P                       : ARRAY[1..16, 1..16] OF REAL;  (* 16x16 Receding-horizon terminal state penalty matrix *)
    aPredState                      : ARRAY[0..5, 1..16] OF REAL;   (* 5-step receding horizon state prediction buffer *)
    aGrad_u                         : ARRAY[1..8] OF REAL;          (* Quadratic cost gradient vector with respect to inputs *)
    rMPCLearningRate                : REAL := 0.0042;               (* Active-set gradient descent step scaling factor *)
    nMPCIterationsMax               : INT := 12;                    (* Maximum gradient descent iterations per scan *)

    (* ================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY SENSOR VOTING STRUCTURES & TIMERS                 *)
    (* ================================================================================= *)
    (* Triplet 1: Optical Sheet Catenary Sag Lasers [mm] *)
    bSag_ChA_Healthy                : BOOL := TRUE;
    bSag_ChB_Healthy                : BOOL := TRUE;
    bSag_ChC_Healthy                : BOOL := TRUE;
    rSag_Dev_AB                     : REAL := 0.0;
    rSag_Dev_BC                     : REAL := 0.0;
    rSag_Dev_CA                     : REAL := 0.0;
    rSag_DiscrepancyTimer_A         : REAL := 0.0;
    rSag_DiscrepancyTimer_B         : REAL := 0.0;
    rSag_DiscrepancyTimer_C         : REAL := 0.0;
    nSag_TMR_Mode                   : INT := 3;     (* 3=2oo3 TMR, 2=1oo2 Degraded, 1=Fail-Safe Hold, 0=Tripped *)

    (* Triplet 2: Mold Cavity Vacuum Manometers [mbar] *)
    bVac_ChA_Healthy                : BOOL := TRUE;
    bVac_ChB_Healthy                : BOOL := TRUE;
    bVac_ChC_Healthy                : BOOL := TRUE;
    rVac_Dev_AB                     : REAL := 0.0;
    rVac_Dev_BC                     : REAL := 0.0;
    rVac_Dev_CA                     : REAL := 0.0;
    rVac_DiscrepancyTimer_A         : REAL := 0.0;
    rVac_DiscrepancyTimer_B         : REAL := 0.0;
    rVac_DiscrepancyTimer_C         : REAL := 0.0;
    nVac_TMR_Mode                   : INT := 3;

    (* Triplet 3: Infrared Sheet Surface Pyrometers [deg C] *)
    bTemp_ChA_Healthy               : BOOL := TRUE;
    bTemp_ChB_Healthy               : BOOL := TRUE;
    bTemp_ChC_Healthy               : BOOL := TRUE;
    rTemp_Dev_AB                    : REAL := 0.0;
    rTemp_Dev_BC                    : REAL := 0.0;
    rTemp_Dev_CA                    : REAL := 0.0;
    rTemp_DiscrepancyTimer_A        : REAL := 0.0;
    rTemp_DiscrepancyTimer_B        : REAL := 0.0;
    rTemp_DiscrepancyTimer_C        : REAL := 0.0;
    nTemp_TMR_Mode                  : INT := 3;

    (* Triplet 4: Servo Plug Assist Force Load Cells [kN] *)
    bForce_ChA_Healthy              : BOOL := TRUE;
    bForce_ChB_Healthy              : BOOL := TRUE;
    bForce_ChC_Healthy              : BOOL := TRUE;
    rForce_Dev_AB                   : REAL := 0.0;
    rForce_Dev_BC                   : REAL := 0.0;
    rForce_Dev_CA                   : REAL := 0.0;
    rForce_DiscrepancyTimer_A       : REAL := 0.0;
    rForce_DiscrepancyTimer_B       : REAL := 0.0;
    rForce_DiscrepancyTimer_C       : REAL := 0.0;
    nForce_TMR_Mode                 : INT := 3;

    (* Discrepancy Thresholds & Debounce Constants *)
    rSag_TolThreshold_mm            : REAL := 5.0;  (* Permissible inter-sensor sag deviation [mm] *)
    rVac_TolThreshold_mbar          : REAL := 35.0; (* Permissible inter-sensor vacuum deviation [mbar] *)
    rTemp_TolThreshold_degC         : REAL := 12.0; (* Permissible inter-sensor temperature deviation [deg C] *)
    rForce_TolThreshold_kN          : REAL := 2.5;  (* Permissible inter-sensor force deviation [kN] *)
    rTMR_DebounceLimit_s            : REAL := 0.25; (* Fault qualification time duration [s] *)

    (* ================================================================================= *)
    (* 96-ZONE QUARTZ RADIANT HEATING ARRAY PID CONTROLLER STRUCTURES                    *)
    (* ================================================================================= *)
    aZoneTop_SP                     : ARRAY[1..48] OF REAL; (* Top heating zones temperature setpoints [deg C] *)
    aZoneTop_PV                     : ARRAY[1..48] OF REAL; (* Top heating zones estimated process temperatures [deg C] *)
    aZoneTop_CV                     : ARRAY[1..48] OF REAL; (* Top heating zones calculated control variables [0..100 %] *)
    aZoneTop_Integral               : ARRAY[1..48] OF REAL; (* Top heating zones integral accumulation terms *)
    aZoneTop_PrevError              : ARRAY[1..48] OF REAL; (* Top heating zones previous scan errors *)
    aZoneTop_DerivFilt              : ARRAY[1..48] OF REAL; (* Top heating zones low-pass filtered derivatives *)

    aZoneBot_SP                     : ARRAY[1..48] OF REAL; (* Bottom heating zones temperature setpoints [deg C] *)
    aZoneBot_PV                     : ARRAY[1..48] OF REAL; (* Bottom heating zones estimated process temperatures [deg C] *)
    aZoneBot_CV                     : ARRAY[1..48] OF REAL; (* Bottom heating zones calculated control variables [0..100 %] *)
    aZoneBot_Integral               : ARRAY[1..48] OF REAL; (* Bottom heating zones integral accumulation terms *)
    aZoneBot_PrevError              : ARRAY[1..48] OF REAL; (* Bottom heating zones previous scan errors *)
    aZoneBot_DerivFilt              : ARRAY[1..48] OF REAL; (* Bottom heating zones low-pass filtered derivatives *)

    (* PID Tuning Parameters for Center, Mid-Ring and Perimeter Zones *)
    rPID_Kp_Center                  : REAL := 1.85; (* Center zone proportional gain *)
    rPID_Ti_Center_s                : REAL := 22.0; (* Center zone integral reset time [s] *)
    rPID_Td_Center_s                : REAL := 3.40; (* Center zone derivative lead time [s] *)
    rPID_Kp_Edge                    : REAL := 2.45; (* Clamp frame edge zone proportional gain *)
    rPID_Ti_Edge_s                  : REAL := 18.0; (* Clamp frame edge zone integral reset time [s] *)
    rPID_Td_Edge_s                  : REAL := 4.20; (* Clamp frame edge zone derivative lead time [s] *)
    rPID_Kp_Corner                  : REAL := 2.95; (* Corner high-draw zone proportional gain *)
    rPID_Ti_Corner_s                : REAL := 15.0; (* Corner high-draw zone integral reset time [s] *)
    rPID_Td_Corner_s                : REAL := 5.10; (* Corner high-draw zone derivative lead time [s] *)
    rPID_DerivFilter_N              : REAL := 10.0; (* Derivative low-pass filter coefficient *)

    (* Heater Burnout & Open-Circuit Detection Timers *)
    aHeaterFaultTimer_Top           : ARRAY[1..48] OF REAL;
    aHeaterFaultTimer_Bot           : ARRAY[1..48] OF REAL;

    (* ================================================================================= *)
    (* 4-STATION CAROUSEL KINEMATIC S-CURVE / CYCLOIDAL PROFILER VARIABLES               *)
    (*   Cycloidal Cam Profile: theta(tau) = 90 deg * (tau - (1/(2*pi)) * sin(2*pi*tau)) *)
    (* ================================================================================= *)
    rCarouselStartIndexAngle_deg    : REAL := 0.0;
    rCarouselTargetIndexAngle_deg   : REAL := 90.0;
    rCarouselIndexDuration_s        : REAL := 2.80; (* Complete 90-degree indexing duration [s] *)
    rCarouselNormTime_tau           : REAL := 0.0;
    rCarouselTrajAngle_deg          : REAL := 0.0;
    rCarouselTrajSpeed_degs         : REAL := 0.0;

    (* ================================================================================= *)
    (* HIGH-SPEED SERVO PLUG ASSIST KINEMATIC S-CURVE MOTION PROFILER                    *)
    (* ================================================================================= *)
    rPlugProfilePos_mm              : REAL := 0.0;
    rPlugProfileVel_ms              : REAL := 0.0;
    rPlugProfileAcc_ms2             : REAL := 0.0;
    rPlugTargetAcc_ms2              : REAL := 4.50; (* Maximum downstroke penetration acceleration [m/s^2] *)
    rPlugJerkLimit_ms3              : REAL := 25.0; (* Maximum linear servo jerk rate [m/s^3] *)
    rPlugContactDepth_mm            : REAL := 120.0;(* Depth where plug contacts pre-blown bubble [mm] *)
    rPlugContactFriction_mu         : REAL := 0.18; (* Dynamic friction coefficient between foam and polymer *)
    rPlugNormalForce_kN             : REAL := 0.0;

    (* ================================================================================= *)
    (* PNEUMATIC BUBBLE PRE-INFLATION THERMODYNAMIC OBSERVER                             *)
    (* ================================================================================= *)
    rBubbleApexCalculated_mm        : REAL := 0.0;
    rBubbleCurvRadius_mm            : REAL := 0.0;
    rBubbleSurfaceArea_m2           : REAL := 0.0;
    rBubbleBiaxialStretchRatio      : REAL := 1.0;
    rAirInjectionFlow_Nm3s          : REAL := 0.0;
    rAccumulatedAirMass_kg          : REAL := 0.0;

    (* ================================================================================= *)
    (* DYNAMIC CAVITY VACUUM EVACUATION OBSERVER & TOOL HEAT TRANSFER                    *)
    (* ================================================================================= *)
    rCavityModelPressure_mbar       : REAL := 1013.25;
    rEvacuationSpeed_m3h            : REAL := 0.0;
    rPolymerCoreTemp_degC           : REAL := 175.0;
    rPolymerSkinTemp_degC           : REAL := 80.0;
    rToolSurfaceTemp_degC           : REAL := 65.0;
    rTransientHeatFlux_kWm2         : REAL := 0.0;

    (* ================================================================================= *)
    (* FINITE STATE MACHINE (FSM) ENGINE VARIABLES                                       *)
    (* ================================================================================= *)
    nFSM_CurrentState               : INT := 0;     (* 0: Idle, 1: Load, 2: Index, 3: Heat, 4: Sag Check, etc. *)
    nFSM_PreviousState              : INT := -1;
    rFSM_StateTimer_s               : REAL := 0.0;
    rFSM_MasterCycleTimer_s         : REAL := 0.0;
    bFSM_TransitionStrobe           : BOOL := FALSE;

    (* ================================================================================= *)
    (* ISA-18.2 ALARM TRIP DEBOUNCE TIMERS & HISTORICAL FAULT FLAGS                      *)
    (* ================================================================================= *)
    rAlarmDebounce_SagHH            : REAL := 0.0;
    rAlarmDebounce_TempHH           : REAL := 0.0;
    rAlarmDebounce_VacLL            : REAL := 0.0;
    rAlarmDebounce_ForceHH          : REAL := 0.0;
    rAlarmDebounce_LightCurtain     : REAL := 0.0;
    bAlarmLatched_FireShield        : BOOL := FALSE;
    bAlarmLatched_CollisionTrip     : BOOL := FALSE;

    (* ================================================================================= *)
    (* MATH CALCULATION TEMPORARY SCRATCHPAD VARIABLES                                   *)
    (* ================================================================================= *)
    i                               : INT;
    j                               : INT;
    k                               : INT;
    p                               : INT;
    nIter                           : INT;
    rTempA                          : REAL;
    rTempB                          : REAL;
    rTempC                          : REAL;
    rMedian                         : REAL;
    rSumAccum                       : REAL;
    rErrorVal                       : REAL;
    rDerivVal                       : REAL;
    rP_term                         : REAL;
    rI_term                         : REAL;
    rD_term                         : REAL;
    rDeltaTime_s                    : REAL;
    rRadTopFlux                     : REAL;
    rRadBotFlux                     : REAL;
    rE_Modulus                      : REAL;
    rCatenaryDenom                  : REAL;
    rCosVal                         : REAL;
    rSinVal                         : REAL
END_VAR"""

    from gen_thermoform import generate_matrices_init
    mat_init = generate_matrices_init()

    # Build the body phases
    phases = []

    # -------------------------------------------------------------
    # PHASE 1: 2oo3 TMR SENSOR VOTING
    # -------------------------------------------------------------
    phase1 = """(* ================================================================================= *)
(* === PHASE 1: 2oo3 TMR SENSOR VOTING & INSTRUMENT HEALTH FAULT TOLERANCE ===       *)
(* Evaluates 4 Triplets: Sheet Sag Lasers, Cavity Vacuum, IR Pyrometers, Plug Force  *)
(* Performs range checking, pairwise deviation tracking, discrepancy timing, and     *)
(* bumpless voting degradation: 2oo3 (Median) -> 1oo2 (Mean) -> Fail-Safe Hold.      *)
(* ================================================================================= *)
rDeltaTime_s := rScanCycleTime_ms / 1000.0;
IF rDeltaTime_s <= 0.0001 THEN
    rDeltaTime_s := 0.0050;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* TRIPLET 1: OPTICAL SHEET CATENARY SAG TRIANGULATION LASERS [mm]                   *)
(* --------------------------------------------------------------------------------- *)
rSag_Dev_AB := ABS(rSheetSag_ChA_mm - rSheetSag_ChB_mm);
rSag_Dev_BC := ABS(rSheetSag_ChB_mm - rSheetSag_ChC_mm);
rSag_Dev_CA := ABS(rSheetSag_ChC_mm - rSheetSag_ChA_mm);

(* Discrepancy Qualification Channel A *)
IF (rSag_Dev_AB > rSag_TolThreshold_mm) AND (rSag_Dev_CA > rSag_TolThreshold_mm) THEN
    rSag_DiscrepancyTimer_A := rSag_DiscrepancyTimer_A + rDeltaTime_s;
    IF rSag_DiscrepancyTimer_A >= rTMR_DebounceLimit_s THEN
        bSag_ChA_Healthy := FALSE;
    END_IF;
ELSE
    rSag_DiscrepancyTimer_A := MAX(0.0, rSag_DiscrepancyTimer_A - rDeltaTime_s * 0.5);
    IF (rSheetSag_ChA_mm >= -5.0) AND (rSheetSag_ChA_mm <= 150.0) THEN
        bSag_ChA_Healthy := TRUE;
    END_IF;
END_IF;

(* Discrepancy Qualification Channel B *)
IF (rSag_Dev_AB > rSag_TolThreshold_mm) AND (rSag_Dev_BC > rSag_TolThreshold_mm) THEN
    rSag_DiscrepancyTimer_B := rSag_DiscrepancyTimer_B + rDeltaTime_s;
    IF rSag_DiscrepancyTimer_B >= rTMR_DebounceLimit_s THEN
        bSag_ChB_Healthy := FALSE;
    END_IF;
ELSE
    rSag_DiscrepancyTimer_B := MAX(0.0, rSag_DiscrepancyTimer_B - rDeltaTime_s * 0.5);
    IF (rSheetSag_ChB_mm >= -5.0) AND (rSheetSag_ChB_mm <= 150.0) THEN
        bSag_ChB_Healthy := TRUE;
    END_IF;
END_IF;

(* Discrepancy Qualification Channel C *)
IF (rSag_Dev_BC > rSag_TolThreshold_mm) AND (rSag_Dev_CA > rSag_TolThreshold_mm) THEN
    rSag_DiscrepancyTimer_C := rSag_DiscrepancyTimer_C + rDeltaTime_s;
    IF rSag_DiscrepancyTimer_C >= rTMR_DebounceLimit_s THEN
        bSag_ChC_Healthy := FALSE;
    END_IF;
ELSE
    rSag_DiscrepancyTimer_C := MAX(0.0, rSag_DiscrepancyTimer_C - rDeltaTime_s * 0.5);
    IF (rSheetSag_ChC_mm >= -5.0) AND (rSheetSag_ChC_mm <= 150.0) THEN
        bSag_ChC_Healthy := TRUE;
    END_IF;
END_IF;

(* Bumpless Voting Degradation for Sheet Sag *)
IF bSag_ChA_Healthy AND bSag_ChB_Healthy AND bSag_ChC_Healthy THEN
    nSag_TMR_Mode := 3; (* Full 2oo3 Triple Redundancy *)
    IF (rSheetSag_ChA_mm >= rSheetSag_ChB_mm AND rSheetSag_ChA_mm <= rSheetSag_ChC_mm) OR
       (rSheetSag_ChA_mm >= rSheetSag_ChC_mm AND rSheetSag_ChA_mm <= rSheetSag_ChB_mm) THEN
        rVotedSheetSag_mm := rSheetSag_ChA_mm;
    ELSIF (rSheetSag_ChB_mm >= rSheetSag_ChA_mm AND rSheetSag_ChB_mm <= rSheetSag_ChC_mm) OR
          (rSheetSag_ChB_mm >= rSheetSag_ChC_mm AND rSheetSag_ChB_mm <= rSheetSag_ChA_mm) THEN
        rVotedSheetSag_mm := rSheetSag_ChB_mm;
    ELSE
        rVotedSheetSag_mm := rSheetSag_ChC_mm;
    END_IF;
ELSIF bSag_ChA_Healthy AND bSag_ChB_Healthy THEN
    nSag_TMR_Mode := 2; (* 1oo2 Degraded Mode: Ch A + Ch B *)
    rVotedSheetSag_mm := (rSheetSag_ChA_mm + rSheetSag_ChB_mm) * 0.5;
ELSIF bSag_ChB_Healthy AND bSag_ChC_Healthy THEN
    nSag_TMR_Mode := 2; (* 1oo2 Degraded Mode: Ch B + Ch C *)
    rVotedSheetSag_mm := (rSheetSag_ChB_mm + rSheetSag_ChC_mm) * 0.5;
ELSIF bSag_ChC_Healthy AND bSag_ChA_Healthy THEN
    nSag_TMR_Mode := 2; (* 1oo2 Degraded Mode: Ch C + Ch A *)
    rVotedSheetSag_mm := (rSheetSag_ChC_mm + rSheetSag_ChA_mm) * 0.5;
ELSIF bSag_ChA_Healthy THEN
    nSag_TMR_Mode := 1; (* 1oo1 Degraded Mode: Single Channel A *)
    rVotedSheetSag_mm := rSheetSag_ChA_mm;
ELSIF bSag_ChB_Healthy THEN
    nSag_TMR_Mode := 1; (* 1oo1 Degraded Mode: Single Channel B *)
    rVotedSheetSag_mm := rSheetSag_ChB_mm;
ELSIF bSag_ChC_Healthy THEN
    nSag_TMR_Mode := 1; (* 1oo1 Degraded Mode: Single Channel C *)
    rVotedSheetSag_mm := rSheetSag_ChC_mm;
ELSE
    nSag_TMR_Mode := 0; (* Complete Sensor Loss: Conservative Worst-Case Trip *)
    rVotedSheetSag_mm := rMaxAllowableSag_mm + 10.0;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* TRIPLET 2: MOLD CAVITY VACUUM ABSOLUTE TRANSMITTERS [mbar]                       *)
(* --------------------------------------------------------------------------------- *)
rVac_Dev_AB := ABS(rCavityVacuum_ChA_mbar - rCavityVacuum_ChB_mbar);
rVac_Dev_BC := ABS(rCavityVacuum_ChB_mbar - rCavityVacuum_ChC_mbar);
rVac_Dev_CA := ABS(rCavityVacuum_ChC_mbar - rCavityVacuum_ChA_mbar);

(* Discrepancy Qualification Channel A *)
IF (rVac_Dev_AB > rVac_TolThreshold_mbar) AND (rVac_Dev_CA > rVac_TolThreshold_mbar) THEN
    rVac_DiscrepancyTimer_A := rVac_DiscrepancyTimer_A + rDeltaTime_s;
    IF rVac_DiscrepancyTimer_A >= rTMR_DebounceLimit_s THEN
        bVac_ChA_Healthy := FALSE;
    END_IF;
ELSE
    rVac_DiscrepancyTimer_A := MAX(0.0, rVac_DiscrepancyTimer_A - rDeltaTime_s * 0.5);
    IF (rCavityVacuum_ChA_mbar >= 0.0) AND (rCavityVacuum_ChA_mbar <= 1100.0) THEN
        bVac_ChA_Healthy := TRUE;
    END_IF;
END_IF;

(* Discrepancy Qualification Channel B *)
IF (rVac_Dev_AB > rVac_TolThreshold_mbar) AND (rVac_Dev_BC > rVac_TolThreshold_mbar) THEN
    rVac_DiscrepancyTimer_B := rVac_DiscrepancyTimer_B + rDeltaTime_s;
    IF rVac_DiscrepancyTimer_B >= rTMR_DebounceLimit_s THEN
        bVac_ChB_Healthy := FALSE;
    END_IF;
ELSE
    rVac_DiscrepancyTimer_B := MAX(0.0, rVac_DiscrepancyTimer_B - rDeltaTime_s * 0.5);
    IF (rCavityVacuum_ChB_mbar >= 0.0) AND (rCavityVacuum_ChB_mbar <= 1100.0) THEN
        bVac_ChB_Healthy := TRUE;
    END_IF;
END_IF;

(* Discrepancy Qualification Channel C *)
IF (rVac_Dev_BC > rVac_TolThreshold_mbar) AND (rVac_Dev_CA > rVac_TolThreshold_mbar) THEN
    rVac_DiscrepancyTimer_C := rVac_DiscrepancyTimer_C + rDeltaTime_s;
    IF rVac_DiscrepancyTimer_C >= rTMR_DebounceLimit_s THEN
        bVac_ChC_Healthy := FALSE;
    END_IF;
ELSE
    rVac_DiscrepancyTimer_C := MAX(0.0, rVac_DiscrepancyTimer_C - rDeltaTime_s * 0.5);
    IF (rCavityVacuum_ChC_mbar >= 0.0) AND (rCavityVacuum_ChC_mbar <= 1100.0) THEN
        bVac_ChC_Healthy := TRUE;
    END_IF;
END_IF;

(* Bumpless Voting Degradation for Mold Cavity Vacuum *)
IF bVac_ChA_Healthy AND bVac_ChB_Healthy AND bVac_ChC_Healthy THEN
    nVac_TMR_Mode := 3;
    IF (rCavityVacuum_ChA_mbar >= rCavityVacuum_ChB_mbar AND rCavityVacuum_ChA_mbar <= rCavityVacuum_ChC_mbar) OR
       (rCavityVacuum_ChA_mbar >= rCavityVacuum_ChC_mbar AND rCavityVacuum_ChA_mbar <= rCavityVacuum_ChB_mbar) THEN
        rVotedCavityVacuum_mbar := rCavityVacuum_ChA_mbar;
    ELSIF (rCavityVacuum_ChB_mbar >= rCavityVacuum_ChA_mbar AND rCavityVacuum_ChB_mbar <= rCavityVacuum_ChC_mbar) OR
          (rCavityVacuum_ChB_mbar >= rCavityVacuum_ChC_mbar AND rCavityVacuum_ChB_mbar <= rCavityVacuum_ChA_mbar) THEN
        rVotedCavityVacuum_mbar := rCavityVacuum_ChB_mbar;
    ELSE
        rVotedCavityVacuum_mbar := rCavityVacuum_ChC_mbar;
    END_IF;
ELSIF bVac_ChA_Healthy AND bVac_ChB_Healthy THEN
    nVac_TMR_Mode := 2;
    rVotedCavityVacuum_mbar := (rCavityVacuum_ChA_mbar + rCavityVacuum_ChB_mbar) * 0.5;
ELSIF bVac_ChB_Healthy AND bVac_ChC_Healthy THEN
    nVac_TMR_Mode := 2;
    rVotedCavityVacuum_mbar := (rCavityVacuum_ChB_mbar + rCavityVacuum_ChC_mbar) * 0.5;
ELSIF bVac_ChC_Healthy AND bVac_ChA_Healthy THEN
    nVac_TMR_Mode := 2;
    rVotedCavityVacuum_mbar := (rCavityVacuum_ChC_mbar + rCavityVacuum_ChA_mbar) * 0.5;
ELSIF bVac_ChA_Healthy THEN
    nVac_TMR_Mode := 1;
    rVotedCavityVacuum_mbar := rCavityVacuum_ChA_mbar;
ELSIF bVac_ChB_Healthy THEN
    nVac_TMR_Mode := 1;
    rVotedCavityVacuum_mbar := rCavityVacuum_ChB_mbar;
ELSIF bVac_ChC_Healthy THEN
    nVac_TMR_Mode := 1;
    rVotedCavityVacuum_mbar := rCavityVacuum_ChC_mbar;
ELSE
    nVac_TMR_Mode := 0;
    rVotedCavityVacuum_mbar := 1013.25; (* Safe Default: Atmospheric Pressure *)
END_IF;

(* --------------------------------------------------------------------------------- *)
(* TRIPLET 3: INFRARED SHEET SURFACE PYROMETERS [deg C]                             *)
(* --------------------------------------------------------------------------------- *)
rTemp_Dev_AB := ABS(rSheetPyrometer_ChA_degC - rSheetPyrometer_ChB_degC);
rTemp_Dev_BC := ABS(rSheetPyrometer_ChB_degC - rSheetPyrometer_ChC_degC);
rTemp_Dev_CA := ABS(rSheetPyrometer_ChC_degC - rSheetPyrometer_ChA_degC);

(* Discrepancy Qualification Channel A *)
IF (rTemp_Dev_AB > rTemp_TolThreshold_degC) AND (rTemp_Dev_CA > rTemp_TolThreshold_degC) THEN
    rTemp_DiscrepancyTimer_A := rTemp_DiscrepancyTimer_A + rDeltaTime_s;
    IF rTemp_DiscrepancyTimer_A >= rTMR_DebounceLimit_s THEN
        bTemp_ChA_Healthy := FALSE;
    END_IF;
ELSE
    rTemp_DiscrepancyTimer_A := MAX(0.0, rTemp_DiscrepancyTimer_A - rDeltaTime_s * 0.5);
    IF (rSheetPyrometer_ChA_degC >= 15.0) AND (rSheetPyrometer_ChA_degC <= 300.0) THEN
        bTemp_ChA_Healthy := TRUE;
    END_IF;
END_IF;

(* Discrepancy Qualification Channel B *)
IF (rTemp_Dev_AB > rTemp_TolThreshold_degC) AND (rTemp_Dev_BC > rTemp_TolThreshold_degC) THEN
    rTemp_DiscrepancyTimer_B := rTemp_DiscrepancyTimer_B + rDeltaTime_s;
    IF rTemp_DiscrepancyTimer_B >= rTMR_DebounceLimit_s THEN
        bTemp_ChB_Healthy := FALSE;
    END_IF;
ELSE
    rTemp_DiscrepancyTimer_B := MAX(0.0, rTemp_DiscrepancyTimer_B - rDeltaTime_s * 0.5);
    IF (rSheetPyrometer_ChB_degC >= 15.0) AND (rSheetPyrometer_ChB_degC <= 300.0) THEN
        bTemp_ChB_Healthy := TRUE;
    END_IF;
END_IF;

(* Discrepancy Qualification Channel C *)
IF (rTemp_Dev_BC > rTemp_TolThreshold_degC) AND (rTemp_Dev_CA > rTemp_TolThreshold_degC) THEN
    rTemp_DiscrepancyTimer_C := rTemp_DiscrepancyTimer_C + rDeltaTime_s;
    IF rTemp_DiscrepancyTimer_C >= rTMR_DebounceLimit_s THEN
        bTemp_ChC_Healthy := FALSE;
    END_IF;
ELSE
    rTemp_DiscrepancyTimer_C := MAX(0.0, rTemp_DiscrepancyTimer_C - rDeltaTime_s * 0.5);
    IF (rSheetPyrometer_ChC_degC >= 15.0) AND (rSheetPyrometer_ChC_degC <= 300.0) THEN
        bTemp_ChC_Healthy := TRUE;
    END_IF;
END_IF;

(* Bumpless Voting Degradation for Sheet Surface Temperature *)
IF bTemp_ChA_Healthy AND bTemp_ChB_Healthy AND bTemp_ChC_Healthy THEN
    nTemp_TMR_Mode := 3;
    IF (rSheetPyrometer_ChA_degC >= rSheetPyrometer_ChB_degC AND rSheetPyrometer_ChA_degC <= rSheetPyrometer_ChC_degC) OR
       (rSheetPyrometer_ChA_degC >= rSheetPyrometer_ChC_degC AND rSheetPyrometer_ChA_degC <= rSheetPyrometer_ChB_degC) THEN
        rVotedSheetTemp_degC := rSheetPyrometer_ChA_degC;
    ELSIF (rSheetPyrometer_ChB_degC >= rSheetPyrometer_ChA_degC AND rSheetPyrometer_ChB_degC <= rSheetPyrometer_ChC_degC) OR
          (rSheetPyrometer_ChB_degC >= rSheetPyrometer_ChC_degC AND rSheetPyrometer_ChB_degC <= rSheetPyrometer_ChA_degC) THEN
        rVotedSheetTemp_degC := rSheetPyrometer_ChB_degC;
    ELSE
        rVotedSheetTemp_degC := rSheetPyrometer_ChC_degC;
    END_IF;
ELSIF bTemp_ChA_Healthy AND bTemp_ChB_Healthy THEN
    nTemp_TMR_Mode := 2;
    rVotedSheetTemp_degC := (rSheetPyrometer_ChA_degC + rSheetPyrometer_ChB_degC) * 0.5;
ELSIF bTemp_ChB_Healthy AND bTemp_ChC_Healthy THEN
    nTemp_TMR_Mode := 2;
    rVotedSheetTemp_degC := (rSheetPyrometer_ChB_degC + rSheetPyrometer_ChC_degC) * 0.5;
ELSIF bTemp_ChC_Healthy AND bTemp_ChA_Healthy THEN
    nTemp_TMR_Mode := 2;
    rVotedSheetTemp_degC := (rSheetPyrometer_ChC_degC + rSheetPyrometer_ChA_degC) * 0.5;
ELSIF bTemp_ChA_Healthy THEN
    nTemp_TMR_Mode := 1;
    rVotedSheetTemp_degC := rSheetPyrometer_ChA_degC;
ELSIF bTemp_ChB_Healthy THEN
    nTemp_TMR_Mode := 1;
    rVotedSheetTemp_degC := rSheetPyrometer_ChB_degC;
ELSIF bTemp_ChC_Healthy THEN
    nTemp_TMR_Mode := 1;
    rVotedSheetTemp_degC := rSheetPyrometer_ChC_degC;
ELSE
    nTemp_TMR_Mode := 0;
    rVotedSheetTemp_degC := 240.0; (* Safe Default: Over-Temperature Trip *)
END_IF;

(* --------------------------------------------------------------------------------- *)
(* TRIPLET 4: SERVO PLUG ASSIST LOAD CELL FORCE SENSORS [kN]                         *)
(* --------------------------------------------------------------------------------- *)
rForce_Dev_AB := ABS(rPlugForce_ChA_kN - rPlugForce_ChB_kN);
rForce_Dev_BC := ABS(rPlugForce_ChB_kN - rPlugForce_ChC_kN);
rForce_Dev_CA := ABS(rPlugForce_ChC_kN - rPlugForce_ChA_kN);

(* Discrepancy Qualification Channel A *)
IF (rForce_Dev_AB > rForce_TolThreshold_kN) AND (rForce_Dev_CA > rForce_TolThreshold_kN) THEN
    rForce_DiscrepancyTimer_A := rForce_DiscrepancyTimer_A + rDeltaTime_s;
    IF rForce_DiscrepancyTimer_A >= rTMR_DebounceLimit_s THEN
        bForce_ChA_Healthy := FALSE;
    END_IF;
ELSE
    rForce_DiscrepancyTimer_A := MAX(0.0, rForce_DiscrepancyTimer_A - rDeltaTime_s * 0.5);
    IF (rPlugForce_ChA_kN >= -2.0) AND (rPlugForce_ChA_kN <= 35.0) THEN
        bForce_ChA_Healthy := TRUE;
    END_IF;
END_IF;

(* Discrepancy Qualification Channel B *)
IF (rForce_Dev_AB > rForce_TolThreshold_kN) AND (rForce_Dev_BC > rForce_TolThreshold_kN) THEN
    rForce_DiscrepancyTimer_B := rForce_DiscrepancyTimer_B + rDeltaTime_s;
    IF rForce_DiscrepancyTimer_B >= rTMR_DebounceLimit_s THEN
        bForce_ChB_Healthy := FALSE;
    END_IF;
ELSE
    rForce_DiscrepancyTimer_B := MAX(0.0, rForce_DiscrepancyTimer_B - rDeltaTime_s * 0.5);
    IF (rPlugForce_ChB_kN >= -2.0) AND (rPlugForce_ChB_kN <= 35.0) THEN
        bForce_ChB_Healthy := TRUE;
    END_IF;
END_IF;

(* Discrepancy Qualification Channel C *)
IF (rForce_Dev_BC > rForce_TolThreshold_kN) AND (rForce_Dev_CA > rForce_TolThreshold_kN) THEN
    rForce_DiscrepancyTimer_C := rForce_DiscrepancyTimer_C + rDeltaTime_s;
    IF rForce_DiscrepancyTimer_C >= rTMR_DebounceLimit_s THEN
        bForce_ChC_Healthy := FALSE;
    END_IF;
ELSE
    rForce_DiscrepancyTimer_C := MAX(0.0, rForce_DiscrepancyTimer_C - rDeltaTime_s * 0.5);
    IF (rPlugForce_ChC_kN >= -2.0) AND (rPlugForce_ChC_kN <= 35.0) THEN
        bForce_ChC_Healthy := TRUE;
    END_IF;
END_IF;

(* Bumpless Voting Degradation for Servo Plug Force *)
IF bForce_ChA_Healthy AND bForce_ChB_Healthy AND bForce_ChC_Healthy THEN
    nForce_TMR_Mode := 3;
    IF (rPlugForce_ChA_kN >= rPlugForce_ChB_kN AND rPlugForce_ChA_kN <= rPlugForce_ChC_kN) OR
       (rPlugForce_ChA_kN >= rPlugForce_ChC_kN AND rPlugForce_ChA_kN <= rPlugForce_ChB_kN) THEN
        rVotedPlugForce_kN := rPlugForce_ChA_kN;
    ELSIF (rPlugForce_ChB_kN >= rPlugForce_ChA_kN AND rPlugForce_ChB_kN <= rPlugForce_ChC_kN) OR
          (rPlugForce_ChB_kN >= rPlugForce_ChC_kN AND rPlugForce_ChB_kN <= rPlugForce_ChA_kN) THEN
        rVotedPlugForce_kN := rPlugForce_ChB_kN;
    ELSE
        rVotedPlugForce_kN := rPlugForce_ChC_kN;
    END_IF;
ELSIF bForce_ChA_Healthy AND bForce_ChB_Healthy THEN
    nForce_TMR_Mode := 2;
    rVotedPlugForce_kN := (rPlugForce_ChA_kN + rPlugForce_ChB_kN) * 0.5;
ELSIF bForce_ChB_Healthy AND bForce_ChC_Healthy THEN
    nForce_TMR_Mode := 2;
    rVotedPlugForce_kN := (rPlugForce_ChB_kN + rPlugForce_ChC_kN) * 0.5;
ELSIF bForce_ChC_Healthy AND bForce_ChA_Healthy THEN
    nForce_TMR_Mode := 2;
    rVotedPlugForce_kN := (rPlugForce_ChC_kN + rPlugForce_ChA_kN) * 0.5;
ELSIF bForce_ChA_Healthy THEN
    nForce_TMR_Mode := 1;
    rVotedPlugForce_kN := rPlugForce_ChA_kN;
ELSIF bForce_ChB_Healthy THEN
    nForce_TMR_Mode := 1;
    rVotedPlugForce_kN := rPlugForce_ChB_kN;
ELSIF bForce_ChC_Healthy THEN
    nForce_TMR_Mode := 1;
    rVotedPlugForce_kN := rPlugForce_ChC_kN;
ELSE
    nForce_TMR_Mode := 0;
    rVotedPlugForce_kN := 25.0; (* Safe Default: Collision Overload Trip *)
END_IF;"""
    phases.append(phase1)

    # -------------------------------------------------------------
    # PHASE 2: 96-ZONE QUARTZ RADIANT HEATING ARRAY PID
    # -------------------------------------------------------------
    phase2 = """(* ================================================================================= *)
(* === PHASE 2: 96-ZONE QUARTZ RADIANT HEATING ARRAY PID LOOPS & THERMAL PROFILING ===*)
(* 48 Top Zones + 48 Bottom Zones independently controlled with individual PID loops. *)
(* Dynamic recipe setpoint calculation based on resin grade and sheet thickness.      *)
(* Edge loss and corner deep-draw thermal compensation profiles applied.              *)
(* Heater burnout open-circuit current monitoring with debounced diagnostic flags.    *)
(* ================================================================================= *)
CASE nMaterialTypeID OF
    1: (* Acrylonitrile Butadiene Styrene (ABS) *)
        rTempA := 178.0; (* Base Top Radiation [deg C] *)
        rTempB := 172.0; (* Base Bottom Radiation [deg C] *)
    2: (* High Impact Polystyrene (HIPS) *)
        rTempA := 162.0; (* Base Top Radiation [deg C] *)
        rTempB := 156.0; (* Base Bottom Radiation [deg C] *)
    3: (* Thermoplastic Polyolefin (TPO) *)
        rTempA := 188.0; (* Base Top Radiation [deg C] *)
        rTempB := 182.0; (* Base Bottom Radiation [deg C] *)
    4: (* Polycarbonate (PC) *)
        rTempA := 215.0; (* Base Top Radiation [deg C] *)
        rTempB := 208.0; (* Base Bottom Radiation [deg C] *)
ELSE
    rTempA := 175.0;
    rTempB := 170.0;
END_CASE;

(* Sheet Thickness Thermal Compensation Factor *)
rTempC := 1.0 + 0.075 * (rSheetNominalThickness_mm - 2.0);
IF rTempC < 0.85 THEN
    rTempC := 0.85;
ELSIF rTempC > 1.45 THEN
    rTempC := 1.45;
END_IF;

(* --------------------------------------------------------------------------------- *)
(* TOP HEATING ARRAY: 48 ZONES PID EXECUTION & ZONE PROFILING                        *)
(* --------------------------------------------------------------------------------- *)
FOR i := 1 TO 48 DO
    (* Spatial Heat Profiling across Top Array *)
    IF i <= 16 THEN
        (* Center Grid Zones 1..16: Reduced setpoint to prevent center thermal dome *)
        aZoneTop_SP[i] := rTempA * rTempC - 4.2;
        rP_term := rPID_Kp_Center;
        rI_term := rPID_Ti_Center_s;
        rD_term := rPID_Td_Center_s;
    ELSIF i <= 32 THEN
        (* Mid-Ring Zones 17..32: Nominal forming setpoint *)
        aZoneTop_SP[i] := rTempA * rTempC + 1.8;
        rP_term := rPID_Kp_Center * 1.15;
        rI_term := rPID_Ti_Center_s * 0.90;
        rD_term := rPID_Td_Center_s * 1.05;
    ELSE
        (* Clamp Frame Perimeter & Corner Zones 33..48: Elevated setpoint for edge sink *)
        aZoneTop_SP[i] := rTempA * rTempC + 11.5;
        rP_term := rPID_Kp_Corner;
        rI_term := rPID_Ti_Corner_s;
        rD_term := rPID_Td_Corner_s;
    END_IF;

    (* Zone Estimated Temperature PV *)
    aZoneTop_PV[i] := rVotedSheetTemp_degC + (aZoneTop_CV[i] - 50.0) * 0.12;
    rErrorVal := aZoneTop_SP[i] - aZoneTop_PV[i];

    (* Proportional Term *)
    rP_term := rP_term * rErrorVal;

    (* Integral Term with Anti-Windup Clamping *)
    IF rI_term > 0.1 THEN
        aZoneTop_Integral[i] := aZoneTop_Integral[i] + (rP_term / rI_term) * rDeltaTime_s;
        IF aZoneTop_Integral[i] > 100.0 THEN
            aZoneTop_Integral[i] := 100.0;
        ELSIF aZoneTop_Integral[i] < 0.0 THEN
            aZoneTop_Integral[i] := 0.0;
        END_IF;
    END_IF;

    (* Derivative Term with Low-Pass Filtering *)
    rDerivVal := (rErrorVal - aZoneTop_PrevError[i]) / rDeltaTime_s;
    aZoneTop_DerivFilt[i] := aZoneTop_DerivFilt[i] + (rDeltaTime_s / (rDeltaTime_s + rD_term / rPID_DerivFilter_N)) * (rDerivVal - aZoneTop_DerivFilt[i]);
    aZoneTop_PrevError[i] := rErrorVal;

    (* Summation and Actuator Duty Clamping *)
    aZoneTop_CV[i] := rP_term + aZoneTop_Integral[i] + rD_term * aZoneTop_DerivFilt[i];
    IF aZoneTop_CV[i] > 100.0 THEN
        aZoneTop_CV[i] := 100.0;
    ELSIF aZoneTop_CV[i] < 0.0 THEN
        aZoneTop_CV[i] := 0.0;
    END_IF;
    aZoneDuty_Top_pct[i] := aZoneTop_CV[i];

    (* Quartz Heating Element Open-Circuit Current Telemetry Verification *)
    IF (aZoneTop_CV[i] > 25.0) AND (aHeaterCurrent_Top_A[i] < 0.45) THEN
        aHeaterFaultTimer_Top[i] := aHeaterFaultTimer_Top[i] + rDeltaTime_s;
        IF aHeaterFaultTimer_Top[i] >= 2.0 THEN
            dwWarningsGroup1 := dwWarningsGroup1 OR 16#00000001; (* Bit 0: Top Quartz Heater Burnout *)
        END_IF;
    ELSE
        aHeaterFaultTimer_Top[i] := MAX(0.0, aHeaterFaultTimer_Top[i] - rDeltaTime_s * 0.5);
    END_IF;
END_FOR;

(* --------------------------------------------------------------------------------- *)
(* BOTTOM HEATING ARRAY: 48 ZONES PID EXECUTION & ZONE PROFILING                     *)
(* --------------------------------------------------------------------------------- *)
FOR i := 1 TO 48 DO
    (* Spatial Heat Profiling across Bottom Array *)
    IF i <= 16 THEN
        aZoneBot_SP[i] := rTempB * rTempC - 5.0;
        rP_term := rPID_Kp_Center;
        rI_term := rPID_Ti_Center_s;
        rD_term := rPID_Td_Center_s;
    ELSIF i <= 32 THEN
        aZoneBot_SP[i] := rTempB * rTempC + 1.2;
        rP_term := rPID_Kp_Center * 1.15;
        rI_term := rPID_Ti_Center_s * 0.90;
        rD_term := rPID_Td_Center_s * 1.05;
    ELSE
        aZoneBot_SP[i] := rTempB * rTempC + 10.8;
        rP_term := rPID_Kp_Corner;
        rI_term := rPID_Ti_Corner_s;
        rD_term := rPID_Td_Corner_s;
    END_IF;

    aZoneBot_PV[i] := (rVotedSheetTemp_degC - 4.5) + (aZoneBot_CV[i] - 50.0) * 0.11;
    rErrorVal := aZoneBot_SP[i] - aZoneBot_PV[i];

    rP_term := rP_term * rErrorVal;

    IF rI_term > 0.1 THEN
        aZoneBot_Integral[i] := aZoneBot_Integral[i] + (rP_term / rI_term) * rDeltaTime_s;
        IF aZoneBot_Integral[i] > 100.0 THEN
            aZoneBot_Integral[i] := 100.0;
        ELSIF aZoneBot_Integral[i] < 0.0 THEN
            aZoneBot_Integral[i] := 0.0;
        END_IF;
    END_IF;

    rDerivVal := (rErrorVal - aZoneBot_PrevError[i]) / rDeltaTime_s;
    aZoneBot_DerivFilt[i] := aZoneBot_DerivFilt[i] + (rDeltaTime_s / (rDeltaTime_s + rD_term / rPID_DerivFilter_N)) * (rDerivVal - aZoneBot_DerivFilt[i]);
    aZoneBot_PrevError[i] := rErrorVal;

    aZoneBot_CV[i] := rP_term + aZoneBot_Integral[i] + rD_term * aZoneBot_DerivFilt[i];
    IF aZoneBot_CV[i] > 100.0 THEN
        aZoneBot_CV[i] := 100.0;
    ELSIF aZoneBot_CV[i] < 0.0 THEN
        aZoneBot_CV[i] := 0.0;
    END_IF;
    aZoneDuty_Bot_pct[i] := aZoneBot_CV[i];

    IF (aZoneBot_CV[i] > 25.0) AND (aHeaterCurrent_Bot_A[i] < 0.45) THEN
        aHeaterFaultTimer_Bot[i] := aHeaterFaultTimer_Bot[i] + rDeltaTime_s;
        IF aHeaterFaultTimer_Bot[i] >= 2.0 THEN
            dwWarningsGroup1 := dwWarningsGroup1 OR 16#00000002; (* Bit 1: Bottom Quartz Heater Burnout *)
        END_IF;
    ELSE
        aHeaterFaultTimer_Bot[i] := MAX(0.0, aHeaterFaultTimer_Bot[i] - rDeltaTime_s * 0.5);
    END_IF;
END_FOR;"""
    phases.append(phase2)

    # -------------------------------------------------------------
    # PHASE 3: DISCRETE STATE-SPACE MODEL & PROPAGATION
    # -------------------------------------------------------------
    phase3 = """(* ================================================================================= *)
(* === PHASE 3: DISCRETE STATE-SPACE MODEL & STATE PROPAGATION (x[k+1] = A*x + B*u) ===*)
(* 16 Cyber-Physical State Variables coupled through continuous-to-discrete physics.  *)
(* Incorporates Stefan-Boltzmann radiation, non-linear catenary viscoelastic sag,     *)
(* spherical bubble pre-inflation acoustics, vacuum orifice fluid flow, and cooling.  *)
(* ================================================================================= *)
IF NOT bStateSpaceInitialized THEN
""" + mat_init + """
    bStateSpaceInitialized := TRUE;
END_IF;

(* Map Actuators to Input Vector u[1..8] *)
rRadTopFlux := 0.0;
rRadBotFlux := 0.0;
FOR i := 1 TO 48 DO
    rRadTopFlux := rRadTopFlux + aZoneDuty_Top_pct[i];
    rRadBotFlux := rRadBotFlux + aZoneDuty_Bot_pct[i];
END_FOR;
aInput_u[1] := rRadTopFlux / 48.0;              (* Average Top Quartz Power [%] *)
aInput_u[2] := rRadBotFlux / 48.0;              (* Average Bot Quartz Power [%] *)
aInput_u[3] := rPreBlowValveCmd_pct;            (* Pre-Blow Proportional Valve [%] *)
aInput_u[4] := rVacuumProportionalValve_pct;    (* Vacuum Proportional Valve [%] *)
aInput_u[5] := rPlugVelCmd_ms * 120.0;          (* Servo Plug Assist Estimated Torque [Nm] *)
aInput_u[6] := (rMTC_SupplyTemp_degC - 50.0) * 1.5; (* MTC Coolant Valve Position [%] *)
aInput_u[7] := rCarouselTorqueCmd_Nm;           (* Rotary Carousel Servo Torque [Nm] *)
IF bChilledAirCoolingJet THEN
    aInput_u[8] := 100.0;                       (* Chilled Air Cooling Jet Header [%] *)
ELSE
    aInput_u[8] := 0.0;
END_IF;

(* Discrete State-Space Propagation Matrix Multiplication: x_next = A * x + B * u *)
FOR i := 1 TO 16 DO
    rSumAccum := 0.0;
    FOR j := 1 TO 16 DO
        rSumAccum := rSumAccum + aMatrix_A[i, j] * aState_x[j];
    END_FOR;
    FOR k := 1 TO 8 DO
        rSumAccum := rSumAccum + aMatrix_B[i, k] * aInput_u[k];
    END_FOR;
    aState_x_next[i] := rSumAccum;
END_FOR;

(* Non-Linear Cyber-Physical Rheology Corrections *)
(* Sheet Core Temperature Softening & Sag Acceleration *)
rE_Modulus := 2400.0 * EXP(-0.026 * (MAX(20.0, aState_x_next[3]) - 23.0)); (* Elastic modulus decay [MPa] *)
IF aState_x_next[3] > 135.0 THEN
    (* Viscoelastic rubbery plateau rapid catenary sag growth *)
    aState_x_next[5] := aState_x_next[5] + 0.0125 * (aState_x_next[3] - 135.0) * rDeltaTime_s;
    aState_x_next[4] := aState_x_next[4] + aState_x_next[5] * rDeltaTime_s;
END_IF;

(* Non-linear Vacuum Evacuation Choked Orifice Flow Rate *)
IF aState_x_next[8] > rVacuumSurgeTankPres_mbar THEN
    rEvacuationSpeed_m3h := 720.0 * (aInput_u[4] / 100.0) * SQRT((aState_x_next[8] - rVacuumSurgeTankPres_mbar) / 1013.25);
    aState_x_next[9] := 0.88 * aState_x_next[9] + 0.12 * rEvacuationSpeed_m3h;
ELSE
    aState_x_next[9] := 0.0;
END_IF;

(* Transfer Next State into Active State Vector *)
FOR i := 1 TO 16 DO
    aState_x[i] := aState_x_next[i];
END_FOR;

(* Luenberger Observer / Kalman Measurement Blending with 2oo3 Voted Sensors *)
aState_x[1]  := 0.84 * aState_x[1]  + 0.16 * rVotedSheetTemp_degC;
aState_x[2]  := 0.84 * aState_x[2]  + 0.16 * (rVotedSheetTemp_degC - 5.0);
aState_x[4]  := 0.80 * aState_x[4]  + 0.20 * rVotedSheetSag_mm;
aState_x[8]  := 0.78 * aState_x[8]  + 0.22 * rVotedCavityVacuum_mbar;
aState_x[10] := 0.90 * aState_x[10] + 0.10 * rPlugActualPos_mm;
aState_x[11] := 0.88 * aState_x[11] + 0.12 * rPlugActualVel_ms;
aState_x[12] := 0.82 * aState_x[12] + 0.18 * rVotedPlugForce_kN;
aState_x[13] := 0.86 * aState_x[13] + 0.14 * rMoldSurfaceTempSP_degC;
aState_x[15] := 0.95 * aState_x[15] + 0.05 * rCarouselAngle_deg;

(* Model Output Vector y = C * x + D * u *)
FOR i := 1 TO 16 DO
    aOutput_y[i] := aState_x[i];
END_FOR;"""
    phases.append(phase3)

    # -------------------------------------------------------------
    # PHASE 4: RECEDING-HORIZON MPC OPTIMIZATION
    # -------------------------------------------------------------
    phase4 = """(* ================================================================================= *)
(* === PHASE 4: RECEDING-HORIZON MPC OPTIMIZATION & ACTUATOR TRAJECTORIES ===        *)
(* Formulates 5-step predictive horizon, evaluates quadratic cost:                   *)
(* J = Sum(e^T * Q * e) + Sum(du^T * R * du) + e_N^T * P * e_N                       *)
(* Executes projected gradient descent optimization with actuator saturation limits. *)
(* Paces quartz radiant heating, pre-blow air pulse, and vacuum evacuation ramp.     *)
(* ================================================================================= *)
(* Dynamic Reference State Trajectory Construction based on Active Sequence *)
aState_ref[1]  := rTargetFormingTemp_degC;          (* x1: Top surface target [deg C] *)
aState_ref[2]  := rTargetFormingTemp_degC - 4.5;    (* x2: Bottom surface target [deg C] *)
aState_ref[3]  := rTargetFormingTemp_degC - 2.0;    (* x3: Core mid-plane target [deg C] *)
aState_ref[4]  := MIN(25.0, rMaxAllowableSag_mm * 0.45); (* x4: Controlled thermal sag setpoint [mm] *)
aState_ref[5]  := 0.0;                              (* x5: Zero sag velocity target *)
aState_ref[6]  := rPreBlowBubbleApexSP_mm;          (* x6: Bubble apex height setpoint [mm] *)
aState_ref[7]  := rPreBlowPressureSP_bar * 1000.0;  (* x7: Bubble chamber pressure [mbar] *)
aState_ref[8]  := rCavityVacuumSP_mbar;             (* x8: Target vacuum setpoint [mbar] *)
aState_ref[9]  := 450.0;                            (* x9: Nominal evacuation flow [m3/h] *)
aState_ref[10] := rPlugStrokeSP_mm;                 (* x10: Plug penetration depth [mm] *)
aState_ref[11] := rPlugVelocitySP_ms;               (* x11: Plug penetration speed [m/s] *)
aState_ref[12] := 12.5;                             (* x12: Nominal plug drawing force [kN] *)
aState_ref[13] := rMoldSurfaceTempSP_degC;          (* x13: Aluminum mold tool temperature [deg C] *)
aState_ref[14] := 14.5;                             (* x14: In-mold cooling rate setpoint [deg C/s] *)
aState_ref[15] := rCarouselTargetIndexAngle_deg;    (* x15: Rotary carousel target index [deg] *)
aState_ref[16] := 4.2;                              (* x16: Optimal polymer stretch stress [MPa] *)

(* Initialize 5-Step Horizon Prediction Buffer *)
FOR i := 1 TO 16 DO
    aPredState[0, i] := aState_x[i];
END_FOR;

(* Initialize Optimal Control Candidate with Current Inputs *)
FOR k := 1 TO 8 DO
    aOptimal_u[k] := aInput_u[k];
END_FOR;

(* Projected Gradient Descent Optimization Loop *)
bMPCOptimizerConverged := FALSE;
rMPCCostResidual := 0.0;

FOR nIter := 1 TO nMPCIterationsMax DO
    (* 1. Forward State Prediction over 5-Step Horizon *)
    FOR p := 1 TO 5 DO
        FOR i := 1 TO 16 DO
            rSumAccum := 0.0;
            FOR j := 1 TO 16 DO
                rSumAccum := rSumAccum + aMatrix_A[i, j] * aPredState[p - 1, j];
            END_FOR;
            FOR k := 1 TO 8 DO
                rSumAccum := rSumAccum + aMatrix_B[i, k] * aOptimal_u[k];
            END_FOR;
            aPredState[p, i] := rSumAccum;
        END_FOR;
    END_FOR;

    (* 2. Evaluate Quadratic Cost & Actuator Gradient Vector *)
    rMPCCostResidual := 0.0;
    FOR k := 1 TO 8 DO
        aGrad_u[k] := 0.0;
    END_FOR;

    (* State Error and Terminal Cost Accumulation *)
    FOR p := 1 TO 5 DO
        FOR i := 1 TO 16 DO
            rErrorVal := aPredState[p, i] - aState_ref[i];
            IF p < 5 THEN
                rMPCCostResidual := rMPCCostResidual + aMatrix_Q[i, i] * (rErrorVal * rErrorVal);
                FOR k := 1 TO 8 DO
                    aGrad_u[k] := aGrad_u[k] + 2.0 * aMatrix_Q[i, i] * rErrorVal * aMatrix_B[i, k];
                END_FOR;
            ELSE
                rMPCCostResidual := rMPCCostResidual + aMatrix_P[i, i] * (rErrorVal * rErrorVal);
                FOR k := 1 TO 8 DO
                    aGrad_u[k] := aGrad_u[k] + 2.0 * aMatrix_P[i, i] * rErrorVal * aMatrix_B[i, k];
                END_FOR;
            END_IF;
        END_FOR;
    END_FOR;

    (* Control Effort Rate Delta Penalty *)
    FOR k := 1 TO 8 DO
        aDelta_u[k] := aOptimal_u[k] - aInput_u[k];
        rMPCCostResidual := rMPCCostResidual + aMatrix_R[k, k] * (aDelta_u[k] * aDelta_u[k]);
        aGrad_u[k] := aGrad_u[k] + 2.0 * aMatrix_R[k, k] * aDelta_u[k];
    END_FOR;

    (* 3. Gradient Descent Step *)
    FOR k := 1 TO 8 DO
        aOptimal_u[k] := aOptimal_u[k] - rMPCLearningRate * aGrad_u[k];
    END_FOR;

    (* 4. Actuator Saturation Constraints Clamping *)
    (* u[1]: Top Quartz Radiant Power [0.0 .. 100.0 %] *)
    IF aOptimal_u[1] > 100.0 THEN aOptimal_u[1] := 100.0; ELSIF aOptimal_u[1] < 0.0 THEN aOptimal_u[1] := 0.0; END_IF;
    (* u[2]: Bottom Quartz Radiant Power [0.0 .. 100.0 %] *)
    IF aOptimal_u[2] > 100.0 THEN aOptimal_u[2] := 100.0; ELSIF aOptimal_u[2] < 0.0 THEN aOptimal_u[2] := 0.0; END_IF;
    (* u[3]: Pre-Blow Pneumatic Proportional Valve [0.0 .. 100.0 %] *)
    IF aOptimal_u[3] > 100.0 THEN aOptimal_u[3] := 100.0; ELSIF aOptimal_u[3] < 0.0 THEN aOptimal_u[3] := 0.0; END_IF;
    (* u[4]: Mold Cavity Vacuum Proportional Valve [0.0 .. 100.0 %] *)
    IF aOptimal_u[4] > 100.0 THEN aOptimal_u[4] := 100.0; ELSIF aOptimal_u[4] < 0.0 THEN aOptimal_u[4] := 0.0; END_IF;
    (* u[5]: Servo Plug Assist Drive Torque [-450.0 .. 450.0 Nm] *)
    IF aOptimal_u[5] > 450.0 THEN aOptimal_u[5] := 450.0; ELSIF aOptimal_u[5] < -450.0 THEN aOptimal_u[5] := -450.0; END_IF;
    (* u[6]: MTC Coolant Flow Valve [0.0 .. 100.0 %] *)
    IF aOptimal_u[6] > 100.0 THEN aOptimal_u[6] := 100.0; ELSIF aOptimal_u[6] < 0.0 THEN aOptimal_u[6] := 0.0; END_IF;
    (* u[7]: Rotary Carousel Indexing Servo Torque [-750.0 .. 750.0 Nm] *)
    IF aOptimal_u[7] > 750.0 THEN aOptimal_u[7] := 750.0; ELSIF aOptimal_u[7] < -750.0 THEN aOptimal_u[7] := -750.0; END_IF;
    (* u[8]: In-Mold Chilled Air Jet Header Valve [0.0 .. 100.0 %] *)
    IF aOptimal_u[8] > 100.0 THEN aOptimal_u[8] := 100.0; ELSIF aOptimal_u[8] < 0.0 THEN aOptimal_u[8] := 0.0; END_IF;

    (* Convergence Check *)
    IF rMPCCostResidual < 15.0 THEN
        bMPCOptimizerConverged := TRUE;
    END_IF;
END_FOR;"""
    phases.append(phase4)

    # -------------------------------------------------------------
    # PHASE 5: BUBBLE PRE-INFLATION & SERVO PLUG ASSIST PROFILING
    # -------------------------------------------------------------
    phase5 = """(* ================================================================================= *)
(* === PHASE 5: BUBBLE PRE-INFLATION & HIGH-SPEED SERVO PLUG ASSIST PROFILING ===    *)
(* Dynamic spherical cap bubble geometry, biaxial stretch ratio, and membrane stress. *)
(* Kinematic S-curve trajectory for servo plug assist: jerk, accel, constant v, decel.*)
(* In-line finished part corner wall thickness predictor & collision protection.      *)
(* ================================================================================= *)
(* Spherical Cap Geometry Observer *)
rTempA := 0.5 * SQRT((rSheetWidth_mm * rSheetLength_mm) / 3.14159265); (* Equivalent circular aperture radius [mm] *)
rEstBubbleApex_mm := MAX(1.0, aState_x[6]);

(* Curvature Radius R_c = (h/2) + (R_0^2 / (2*h)) *)
rBubbleCurvRadius_mm := (rEstBubbleApex_mm * 0.5) + ((rTempA * rTempA) / (2.0 * rEstBubbleApex_mm));

(* Spherical Cap Enclosed Volume V = (pi * h / 6) * (3 * R_0^2 + h^2) [Liters] *)
rEstBubbleVolume_L := ((3.14159265 * rEstBubbleApex_mm) / 6.0) * (3.0 * (rTempA * rTempA) + (rEstBubbleApex_mm * rEstBubbleApex_mm)) * 1.0E-6;

(* Biaxial Pre-Blow Stretch Ratio *)
rBubbleBiaxialStretchRatio := SQRT(1.0 + ((rEstBubbleApex_mm * rEstBubbleApex_mm) / (rTempA * rTempA)));

(* Membrane Equi-Biaxial Tension Stress [MPa] *)
IF rSheetNominalThickness_mm > 0.1 THEN
    rBubbleSurfaceArea_m2 := 2.0 * 3.14159265 * (rBubbleCurvRadius_mm * 1.0E-3) * (rEstBubbleApex_mm * 1.0E-3);
    rTempB := (aState_x[7] * 100.0 * (rBubbleCurvRadius_mm * 1.0E-3)) / (2.0 * (rSheetNominalThickness_mm * 1.0E-3)) * 1.0E-6;
END_IF;

(* In-Line Finished Part Wall Thickness Estimator *)
(* Predicts thinning at deep-drawn corners based on bubble stretch and plug draw ratio *)
IF (rBubbleBiaxialStretchRatio > 0.5) AND (rPlugStrokeSP_mm > 10.0) THEN
    rPredictedMinWall_mm := rSheetNominalThickness_mm / ((rBubbleBiaxialStretchRatio * rBubbleBiaxialStretchRatio) * (1.0 + 0.62 * (aState_x[10] / rPlugStrokeSP_mm)));
    rPredictedMaxWall_mm := rSheetNominalThickness_mm * (1.0 - 0.06 * rBubbleBiaxialStretchRatio);
ELSE
    rPredictedMinWall_mm := rSheetNominalThickness_mm * 0.40;
    rPredictedMaxWall_mm := rSheetNominalThickness_mm * 0.95;
END_IF;

(* High-Speed Servo Plug Assist Kinematic S-Curve Downstroke Profiling *)
IF nFSM_CurrentState = 7 THEN
    (* State 7: Active Plug Downstroke *)
    IF rPlugProfilePos_mm < rPlugStrokeSP_mm THEN
        IF rPlugProfileVel_ms < rPlugVelocitySP_ms THEN
            rPlugProfileAcc_ms2 := MIN(rPlugTargetAcc_ms2, rPlugProfileAcc_ms2 + rPlugJerkLimit_ms3 * rDeltaTime_s);
            rPlugProfileVel_ms := rPlugProfileVel_ms + rPlugProfileAcc_ms2 * rDeltaTime_s;
        ELSE
            rPlugProfileAcc_ms2 := 0.0;
        END_IF;
        rPlugProfilePos_mm := rPlugProfilePos_mm + (rPlugProfileVel_ms * 1000.0) * rDeltaTime_s;
    ELSE
        rPlugProfilePos_mm := rPlugStrokeSP_mm;
        rPlugProfileVel_ms := 0.0;
        rPlugProfileAcc_ms2 := 0.0;
        bPlugAssistInPosition := TRUE;
    END_IF;
    rPlugPosCmd_mm := rPlugProfilePos_mm;
    rPlugVelCmd_ms := rPlugProfileVel_ms;
    rPlugTorqueLimit_Nm := 380.0;
    bPlugAssistRetractedHome := FALSE;
ELSIF (nFSM_CurrentState = 10) OR (nFSM_CurrentState = 12) THEN
    (* State 10 / 12: Retract Plug to Home Position *)
    IF rPlugProfilePos_mm > 0.0 THEN
        rPlugProfileVel_ms := -rPlugVelocitySP_ms * 0.85;
        rPlugProfilePos_mm := MAX(0.0, rPlugProfilePos_mm + (rPlugProfileVel_ms * 1000.0) * rDeltaTime_s);
    ELSE
        rPlugProfilePos_mm := 0.0;
        rPlugProfileVel_ms := 0.0;
        bPlugAssistRetractedHome := TRUE;
    END_IF;
    rPlugPosCmd_mm := rPlugProfilePos_mm;
    rPlugVelCmd_ms := rPlugProfileVel_ms;
    rPlugTorqueLimit_Nm := 250.0;
    bPlugAssistInPosition := FALSE;
ELSE
    rPlugPosCmd_mm := 0.0;
    rPlugVelCmd_ms := 0.0;
    rPlugTorqueLimit_Nm := 150.0;
    bPlugAssistRetractedHome := (rPlugActualPos_mm <= 2.0);
    bPlugAssistInPosition := FALSE;
END_IF;

(* Servo Plug Dynamic Collision Force Clamping *)
IF rVotedPlugForce_kN > 22.0 THEN
    bAlarmLatched_CollisionTrip := TRUE;
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000020; (* Bit 5: Plug Assist Collision Trip *)
    rPlugTorqueLimit_Nm := 20.0;                    (* Immediate torque clamp *)
END_IF;"""
    phases.append(phase5)

    # -------------------------------------------------------------
    # PHASE 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------
    phase6 = """(* ================================================================================= *)
(* === PHASE 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) ===                  *)
(* Fully automated continuous rotary carousel sequence for heavy sheet thermoforming:*)
(* State 0 : System Idle / Standby Initialization                                    *)
(* State 1 : Station 1 - Raw Sheet De-Stacking & Pneumatic Clamp Frame Lock          *)
(* State 2 : 4-Station Carousel Indexing Cycloidal Rotary Acceleration (0 to 90 deg) *)
(* State 3 : Station 2 - Radiant Oven Infeed & 96-Zone Multi-Zone Thermal Soak       *)
(* State 4 : Station 2 - Sheet Sag Optical Closed-Loop Monitoring & Heat Shaping     *)
(* State 5 : Station 3 - Pneumatic Bubble Pre-Inflation Stretch (Air Cushion Table)  *)
(* State 6 : Station 3 - Mold Clamping Toggle Tonnage Lock (Hydraulic Platens)       *)
(* State 7 : Station 3 - Servo Plug Assist High-Speed Downstroke Deep Draw           *)
(* State 8 : Station 3 - High-Vacuum Fast Evacuation Forming (< 50 mbar)             *)
(* State 9 : Station 3 - In-Mold Vortex Chilled Air Jet Cooling & Solidification     *)
(* State 10: Station 3 - Mold Stripping, Mechanical Ejector Pins & Plug Retraction   *)
(* State 11: Station 4 - Robotic Perimeter Trim, Hole Punching & Finished Egress     *)
(* State 12: Emergency Safety Heat Shield Drop, Vacuum Fast Dump & Safe Abort        *)
(* ================================================================================= *)
rStateElapsedTimer_s := rStateElapsedTimer_s + rDeltaTime_s;
rOverallCycleTimer_s := rOverallCycleTimer_s + rDeltaTime_s;

(* Emergency Interlock Override Check *)
IF NOT bSafetyEStop_OK OR NOT bSafetyLightCurtain_OK OR NOT bSafetyEnclosureDoors_OK OR
   bAlarmLatched_FireShield OR bAlarmLatched_CollisionTrip THEN
    IF nFSM_CurrentState <> 12 THEN
        nFSM_PreviousState := nFSM_CurrentState;
        nFSM_CurrentState := 12; (* Jump immediately to Emergency State 12 *)
        rStateElapsedTimer_s := 0.0;
    END_IF;
END_IF;

CASE nFSM_CurrentState OF
    0: (* SYSTEM IDLE / STANDBY INITIALIZATION *)
        sActiveStateDesc := 'STATE 0: SYSTEM IDLE / STANDBY INITIALIZATION';
        bCarouselBrakeRelease        := FALSE;
        rCarouselTorqueCmd_Nm        := 0.0;
        rCarouselVelocityCmd_degs    := 0.0;
        rPreBlowValveCmd_pct         := 0.0;
        bPreBlowPulseSolenoid        := FALSE;
        rVacuumProportionalValve_pct := 0.0;
        bVacuumFastDumpSolenoid      := FALSE;
        bMoldVacuumVentValve         := TRUE;
        rPlatenToggleHydValve_pct    := 0.0;
        bPlatenTonnageLocked         := FALSE;
        bChilledAirCoolingJet        := FALSE;
        bMoldEjectorPinExtend        := FALSE;
        bClampFrameLockSol           := FALSE;
        bSheetDestackerVacuumOn      := FALSE;
        bStation4TrimArmEnable       := FALSE;
        bStation4TrimCycleStart      := FALSE;
        bOvenFireShieldDrop          := FALSE;

        IF bEnableMaster AND bAutoCycleStart AND bSafetyEStop_OK AND bSafetyLightCurtain_OK THEN
            nFSM_PreviousState   := 0;
            nFSM_CurrentState    := 1;
            rStateElapsedTimer_s := 0.0;
            rOverallCycleTimer_s := 0.0;
        END_IF;

    1: (* STATION 1: RAW SHEET DE-STACKING & PNEUMATIC CLAMP LOCK *)
        sActiveStateDesc := 'STATE 1: STATION 1 - DE-STACKING & PNEUMATIC CLAMP LOCK';
        bSheetDestackerVacuumOn := TRUE;
        IF rStateElapsedTimer_s > 0.8 THEN
            bClampFrameLockSol := TRUE;
        END_IF;

        (* Advance when clamping frame pressure confirms perimeter seal (> 5.5 bar) *)
        IF (rStateElapsedTimer_s >= 2.2) AND (rClampFramePressure_bar >= 5.5) THEN
            nFSM_PreviousState   := 1;
            nFSM_CurrentState    := 2;
            rStateElapsedTimer_s := 0.0;
            rCarouselStartIndexAngle_deg  := rCarouselAngle_deg;
            rCarouselTargetIndexAngle_deg := rCarouselAngle_deg + 90.0;
        END_IF;

    2: (* 4-STATION CAROUSEL INDEXING ROTARY ACCELERATION (0 TO 90 DEG) *)
        sActiveStateDesc := 'STATE 2: 4-STATION CAROUSEL INDEXING (0 TO 90 DEG)';
        bCarouselBrakeRelease := TRUE;

        (* Execute Cycloidal Cam Profile: theta(tau) = 90 deg * (tau - (1/(2*pi)) * sin(2*pi*tau)) *)
        rCarouselNormTime_tau := MIN(1.0, rStateElapsedTimer_s / rCarouselIndexDuration_s);
        rSinVal := SIN(2.0 * 3.14159265 * rCarouselNormTime_tau);
        rCosVal := COS(2.0 * 3.14159265 * rCarouselNormTime_tau);

        rCarouselTrajAngle_deg := rCarouselStartIndexAngle_deg + 90.0 * (rCarouselNormTime_tau - (1.0 / (2.0 * 3.14159265)) * rSinVal);
        rCarouselTrajSpeed_degs := (90.0 / rCarouselIndexDuration_s) * (1.0 - rCosVal);

        rCarouselVelocityCmd_degs := rCarouselTrajSpeed_degs;
        rCarouselTorqueCmd_Nm := aOptimal_u[7];

        IF rCarouselNormTime_tau >= 1.0 THEN
            bCarouselBrakeRelease := FALSE;
            rCarouselVelocityCmd_degs := 0.0;
            rCarouselTorqueCmd_Nm := 0.0;
            bCarouselIndexComplete := TRUE;
            nFSM_PreviousState   := 2;
            nFSM_CurrentState    := 3;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    3: (* STATION 2: RADIANT OVEN INFEED & 96-ZONE MULTI-ZONE THERMAL SOAK *)
        sActiveStateDesc := 'STATE 3: STATION 2 - 96-ZONE MULTI-ZONE THERMAL SOAK';
        bCarouselIndexComplete := FALSE;
        (* Heating active under Phase 2 PID control *)

        (* Transition to closed-loop sag monitoring as sheet approaches rubbery plateau *)
        IF (rVotedSheetTemp_degC >= (rTargetFormingTemp_degC - 25.0)) OR (rStateElapsedTimer_s >= 14.0) THEN
            nFSM_PreviousState   := 3;
            nFSM_CurrentState    := 4;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    4: (* STATION 2: SHEET SAG OPTICAL CLOSED-LOOP MONITORING & HEAT SHAPING *)
        sActiveStateDesc := 'STATE 4: STATION 2 - SHEET SAG MONITORING & HEAT SHAPING';
        (* If sheet sags towards limit, apply low-pressure air support pulse *)
        IF rVotedSheetSag_mm > (rMaxAllowableSag_mm * 0.70) THEN
            rPreBlowValveCmd_pct := 35.0;
            bPreBlowPulseSolenoid := TRUE;
        ELSE
            rPreBlowValveCmd_pct := 0.0;
            bPreBlowPulseSolenoid := FALSE;
        END_IF;

        (* Sheet achieves target forming temperature and stable catenary profile *)
        IF (rVotedSheetTemp_degC >= rTargetFormingTemp_degC) AND (rStateElapsedTimer_s >= 4.0) THEN
            nFSM_PreviousState   := 4;
            nFSM_CurrentState    := 5;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    5: (* STATION 3: PNEUMATIC BUBBLE PRE-INFLATION STRETCH (AIR CUSHION TABLE) *)
        sActiveStateDesc := 'STATE 5: STATION 3 - PNEUMATIC BUBBLE PRE-INFLATION';
        rPreBlowValveCmd_pct  := aOptimal_u[3];
        bPreBlowPulseSolenoid := TRUE;

        (* Complete bubble inflation when apex achieves target height *)
        IF (rEstBubbleApex_mm >= rPreBlowBubbleApexSP_mm) OR (rStateElapsedTimer_s >= 1.6) THEN
            bPreBlowPulseSolenoid := FALSE;
            rPreBlowValveCmd_pct  := 10.0; (* Low holding pressure *)
            nFSM_PreviousState   := 5;
            nFSM_CurrentState    := 6;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    6: (* STATION 3: MOLD CLAMPING TOGGLE TONNAGE LOCK (HYDRAULIC PLATENS) *)
        sActiveStateDesc := 'STATE 6: STATION 3 - MOLD CLAMPING TONNAGE LOCK';
        rPlatenToggleHydValve_pct := 90.0;

        (* Confirm toggle mechanism mechanical lock tonnage (> 750 kN) *)
        IF (rPlatenTonnageActual_kN >= 750.0) AND (rStateElapsedTimer_s >= 0.8) THEN
            bPlatenTonnageLocked := TRUE;
            nFSM_PreviousState   := 6;
            nFSM_CurrentState    := 7;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    7: (* STATION 3: SERVO PLUG ASSIST HIGH-SPEED DOWNSTROKE DEEP DRAW *)
        sActiveStateDesc := 'STATE 7: STATION 3 - SERVO PLUG ASSIST DOWNSTROKE';
        (* S-curve downstroke calculated in Phase 5 *)

        IF bPlugAssistInPosition OR (rStateElapsedTimer_s >= 1.5) THEN
            nFSM_PreviousState   := 7;
            nFSM_CurrentState    := 8;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    8: (* STATION 3: HIGH-VACUUM FAST EVACUATION FORMING (< 50 mbar) *)
        sActiveStateDesc := 'STATE 8: STATION 3 - HIGH-VACUUM FAST EVACUATION FORMING';
        bVacuumFastDumpSolenoid      := TRUE;
        rVacuumProportionalValve_pct := 100.0;
        bMoldVacuumVentValve         := FALSE;

        (* Part draws against aluminum mold surface, vacuum achieves deep target *)
        IF (rVotedCavityVacuum_mbar <= rCavityVacuumSP_mbar) OR (rStateElapsedTimer_s >= 1.8) THEN
            nFSM_PreviousState   := 8;
            nFSM_CurrentState    := 9;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    9: (* STATION 3: IN-MOLD VORTEX CHILLED AIR JET COOLING & SOLIDIFICATION *)
        sActiveStateDesc := 'STATE 9: STATION 3 - CHILLED AIR JET COOLING';
        bChilledAirCoolingJet := TRUE;
        rVacuumProportionalValve_pct := 40.0; (* Maintain holding vacuum *)

        (* Dwell until polymer solidifies below Heat Deflection Temperature (HDT) *)
        IF rStateElapsedTimer_s >= rCoolingDwellTimeSP_s THEN
            bChilledAirCoolingJet := FALSE;
            nFSM_PreviousState   := 9;
            nFSM_CurrentState    := 10;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    10: (* STATION 3: MOLD STRIPPING, MECHANICAL EJECTOR PINS & PLUG RETRACTION *)
        sActiveStateDesc := 'STATE 10: STATION 3 - MOLD STRIPPING & PLUG RETRACT';
        rVacuumProportionalValve_pct := 0.0;
        bVacuumFastDumpSolenoid      := FALSE;
        bMoldVacuumVentValve         := TRUE; (* Vent mold cavity to atmosphere *)
        rPlatenToggleHydValve_pct    := 0.0;
        bPlatenTonnageLocked         := FALSE;
        bMoldEjectorPinExtend        := TRUE;

        (* Wait until servo plug assist is fully retracted and ejector extended *)
        IF bPlugAssistRetractedHome AND (rStateElapsedTimer_s >= 1.8) THEN
            bMoldEjectorPinExtend := FALSE;
            nFSM_PreviousState   := 10;
            nFSM_CurrentState    := 11;
            rStateElapsedTimer_s := 0.0;
        END_IF;

    11: (* STATION 4: ROBOTIC PERIMETER TRIM, HOLE PUNCHING & FINISHED EGRESS *)
        sActiveStateDesc := 'STATE 11: STATION 4 - ROBOTIC TRIMMING & EGRESS';
        bStation4TrimArmEnable  := TRUE;
        bStation4TrimCycleStart := TRUE;
        bFinishedPartUnloadReady := TRUE;

        IF rStateElapsedTimer_s >= 3.5 THEN
            bStation4TrimCycleStart  := FALSE;
            bFinishedPartUnloadReady := FALSE;
            IF bAutoCycleStart AND NOT bCycleHaltRequest THEN
                nFSM_PreviousState   := 11;
                nFSM_CurrentState    := 1; (* Continuous auto cycle rollover *)
                rStateElapsedTimer_s := 0.0;
                rOverallCycleTimer_s := 0.0;
            ELSE
                nFSM_PreviousState   := 11;
                nFSM_CurrentState    := 0; (* Stop at standby idle *)
                rStateElapsedTimer_s := 0.0;
            END_IF;
        END_IF;

    12: (* EMERGENCY SAFETY HEAT SHIELD DROP, VACUUM FAST DUMP & SAFE ABORT *)
        sActiveStateDesc := 'STATE 12: EMERGENCY FIRE SHIELD DROP & SAFE ABORT';
        bOvenFireShieldDrop          := TRUE;  (* Drop pneumatic radiant heat barrier *)
        bOvenExhaustDamperOpen       := TRUE;  (* Vent hot exhaust VOC gases *)
        bCarouselBrakeRelease        := FALSE; (* Lock heavy carousel holding brake *)
        rCarouselTorqueCmd_Nm        := 0.0;
        rCarouselVelocityCmd_degs    := 0.0;
        rPreBlowValveCmd_pct         := 0.0;
        bPreBlowPulseSolenoid        := FALSE;
        rVacuumProportionalValve_pct := 0.0;
        bVacuumFastDumpSolenoid      := FALSE;
        bMoldVacuumVentValve         := TRUE;  (* Fast vent cavity *)
        rPlatenToggleHydValve_pct    := 0.0;
        bPlatenTonnageLocked         := FALSE;
        bChilledAirCoolingJet        := FALSE;
        bMoldEjectorPinExtend        := FALSE;
        bSheetDestackerVacuumOn      := FALSE;
        bStation4TrimArmEnable       := FALSE;
        bStation4TrimCycleStart      := FALSE;

        (* Zero all heating duty commands for immediate thermal shutdown *)
        FOR i := 1 TO 48 DO
            aZoneDuty_Top_pct[i] := 0.0;
            aZoneDuty_Bot_pct[i] := 0.0;
        END_FOR;

        (* Latch emergency state until operator fault acknowledge and reset *)
        IF bAckAlarm AND bSafetyEStop_OK AND bSafetyLightCurtain_OK AND bSafetyEnclosureDoors_OK THEN
            bAlarmLatched_FireShield    := FALSE;
            bAlarmLatched_CollisionTrip := FALSE;
            bOvenFireShieldDrop         := FALSE;
            bOvenExhaustDamperOpen      := FALSE;
            nFSM_PreviousState   := 12;
            nFSM_CurrentState    := 0;
            rStateElapsedTimer_s := 0.0;
        END_IF;
END_CASE;

nActiveFSMState := nFSM_CurrentState;"""
    phases.append(phase6)

    # -------------------------------------------------------------
    # PHASE 7: ISA-18.2 ALARMS & DIAGNOSTICS WORD PACKING
    # -------------------------------------------------------------
    phase7 = """(* ================================================================================= *)
(* === PHASE 7: ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING ===                        *)
(* Multi-tiered industrial alarm evaluation with deadband hysteresis, debounce       *)
(* timing, priority tiering, and bit-packed telemetry DWORD words.                   *)
(* dwAlarmsGroup1   : Priority 1 - Critical machine safety, platen & fire trips      *)
(* dwAlarmsGroup2   : Priority 2 - Process quality, vacuum shortfall & wall defects  *)
(* dwWarningsGroup1 : Priority 3 - Preventive maintenance, heater burnout & TMR      *)
(* dwStatusWord     : System telemetry, interlocking status & sequence readiness     *)
(* ================================================================================= *)
dwAlarmsGroup1   := 16#00000000;
dwAlarmsGroup2   := 16#00000000;
dwStatusWord     := 16#00000000;

(* --- ALARMS GROUP 1: CRITICAL TRIPS & SAFETY INTERLOCKS --- *)
(* Bit 0: Emergency Stop Circuit Tripped *)
IF NOT bSafetyEStop_OK THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000001;
END_IF;

(* Bit 1: Safety Light Curtain Perimeter Tripped *)
IF NOT bSafetyLightCurtain_OK THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000002;
END_IF;

(* Bit 2: Safety Enclosure Door Interlock Open *)
IF NOT bSafetyEnclosureDoors_OK THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000004;
END_IF;

(* Bit 3: Sheet Catenary Sag Critical Fire Risk HH Trip (> 75.0 mm) *)
IF rVotedSheetSag_mm >= rMaxAllowableSag_mm THEN
    rAlarmDebounce_SagHH := rAlarmDebounce_SagHH + rDeltaTime_s;
    IF rAlarmDebounce_SagHH >= 0.15 THEN
        dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000008;
        bAlarmLatched_FireShield := TRUE;
    END_IF;
ELSE
    rAlarmDebounce_SagHH := MAX(0.0, rAlarmDebounce_SagHH - rDeltaTime_s * 0.5);
END_IF;

(* Bit 4: Sheet Surface Temperature Critical Fire Hazard HH Trip (> 230 deg C) *)
IF rVotedSheetTemp_degC >= 230.0 THEN
    rAlarmDebounce_TempHH := rAlarmDebounce_TempHH + rDeltaTime_s;
    IF rAlarmDebounce_TempHH >= 0.20 THEN
        dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000010;
        bAlarmLatched_FireShield := TRUE;
    END_IF;
ELSE
    rAlarmDebounce_TempHH := MAX(0.0, rAlarmDebounce_TempHH - rDeltaTime_s * 0.5);
END_IF;

(* Bit 5: Servo Plug Assist Force Collision Overload Trip (> 22.0 kN) *)
IF rVotedPlugForce_kN >= 22.0 THEN
    rAlarmDebounce_ForceHH := rAlarmDebounce_ForceHH + rDeltaTime_s;
    IF rAlarmDebounce_ForceHH >= 0.05 THEN
        dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000020;
        bAlarmLatched_CollisionTrip := TRUE;
    END_IF;
ELSE
    rAlarmDebounce_ForceHH := MAX(0.0, rAlarmDebounce_ForceHH - rDeltaTime_s * 0.5);
END_IF;

(* Bit 6: Hydraulic Clamp Tonnage Failure During Forming (< 200 kN in State 6..9) *)
IF (nFSM_CurrentState >= 6) AND (nFSM_CurrentState <= 9) AND (rPlatenTonnageActual_kN < 200.0) THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000040;
END_IF;

(* Bit 7: Vacuum Surge Tank Loss of Primary Vacuum Reservoir (> 350 mbar) *)
IF rVacuumSurgeTankPres_mbar > 350.0 THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000080;
END_IF;

(* Bit 8: Pre-Blow Pneumatic Overpressure Burst Risk (> 0.60 bar) *)
IF rPreBlowLineSupplyPres_bar > 0.60 THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000100;
END_IF;

(* Bit 9: Carousel Index Rotary Angle Discrepancy Error (> 2.5 deg) *)
IF (nFSM_CurrentState = 2) AND (ABS(rCarouselAngle_deg - rCarouselTrajAngle_deg) > 2.5) THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000200;
END_IF;

(* Bit 10: 2oo3 Sheet Sag Sensors Complete Failure (Mode 0) *)
IF nSag_TMR_Mode = 0 THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000400;
END_IF;

(* Bit 11: 2oo3 Cavity Vacuum Transmitters Complete Failure (Mode 0) *)
IF nVac_TMR_Mode = 0 THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00000800;
END_IF;

(* Bit 12: 2oo3 IR Pyrometers Complete Failure (Mode 0) *)
IF nTemp_TMR_Mode = 0 THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00001000;
END_IF;

(* Bit 13: 2oo3 Plug Force Sensors Complete Failure (Mode 0) *)
IF nForce_TMR_Mode = 0 THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00002000;
END_IF;

(* Bit 14: Main Pneumatic Compressed Air Supply Pressure Low (< 5.0 bar) *)
IF NOT bCompressedAirSupply_OK THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00004000;
END_IF;

(* Bit 15: Oven Catalytic Exhaust VOC Ventilation Fan Failed *)
IF NOT bOvenExhaustFanRunning THEN
    dwAlarmsGroup1 := dwAlarmsGroup1 OR 16#00008000;
END_IF;

(* --- ALARMS GROUP 2: PROCESS DEVIATION & FORMING QUALITY DEFECTS --- *)
(* Bit 0: Mold Cavity Vacuum Shortfall LL Alarm (> 120 mbar during State 8/9) *)
IF (nFSM_CurrentState = 8) AND (rStateElapsedTimer_s > 1.2) AND (rVotedCavityVacuum_mbar > 120.0) THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000001;
END_IF;

(* Bit 1: Sheet Forming Under-Temperature LL Alarm (< 145 deg C in State 5) *)
IF (nFSM_CurrentState = 5) AND (rVotedSheetTemp_degC < 145.0) THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000002;
END_IF;

(* Bit 2: Critical Corner Minimum Wall Thickness LL Defect (< 0.65 mm) *)
IF rPredictedMinWall_mm < 0.65 THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000004;
END_IF;

(* Bit 3: Flange Perimeter Maximum Wall Thickness High Defect (> 4.80 mm) *)
IF rPredictedMaxWall_mm > 4.80 THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000008;
END_IF;

(* Bit 4: Bubble Pre-Blow Apex Height Deviation Alarm (> 25 mm error in State 5) *)
IF (nFSM_CurrentState = 5) AND (ABS(rEstBubbleApex_mm - rPreBlowBubbleApexSP_mm) > 25.0) THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000010;
END_IF;

(* Bit 5: Servo Plug Stroke Depth Shortfall Alarm (< 92% of Setpoint in State 7) *)
IF (nFSM_CurrentState = 7) AND (rStateElapsedTimer_s > 1.2) AND (rPlugActualPos_mm < rPlugStrokeSP_mm * 0.92) THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000020;
END_IF;

(* Bit 6: Aluminum Mold Tool Surface Temperature High Alarm (> 92 deg C) *)
IF rMTC_ReturnTemp_degC > 92.0 THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000040;
END_IF;

(* Bit 7: Aluminum Mold Tool Surface Temperature Low Alarm (< 50 deg C) *)
IF rMTC_SupplyTemp_degC < 50.0 THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000080;
END_IF;

(* Bit 8: MTC Circulating Fluid Circuit Low Flow Alarm (< 12 L/min) *)
IF NOT bCoolingWaterFlow_OK OR (rMTC_FluidFlowRate_Lmin < 12.0) THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000100;
END_IF;

(* Bit 9: In-Mold Chilled Air Jet Header Pressure Low (< 3.8 bar) *)
IF bChilledAirCoolingJet AND (rChilledAirSupplyPres_bar < 3.8) THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000200;
END_IF;

(* Bit 10: Pneumatic Clamping Frame Pressure Low (< 4.8 bar in State 2..10) *)
IF (nFSM_CurrentState >= 2) AND (nFSM_CurrentState <= 10) AND (rClampFramePressure_bar < 4.8) THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000400;
END_IF;

(* Bit 11: Total Machine Cycle Time Exceeded Watchdog Alarm (> 48.0 s) *)
IF rOverallCycleTimer_s > 48.0 THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00000800;
END_IF;

(* Bit 12: Station 4 Robotic Trimming Tool Position Deviation Fault *)
IF bStation4TrimArmEnable AND (rTrimRobotArmPosition_mm < -10.0) THEN
    dwAlarmsGroup2 := dwAlarmsGroup2 OR 16#00001000;
END_IF;

(* --- WARNINGS GROUP 1: PREVENTIVE MAINTENANCE & SENSOR DEGRADATION --- *)
(* Bit 2: Sheet Sag Sensor Degraded (1oo2 Mode) *)
IF nSag_TMR_Mode = 2 THEN
    dwWarningsGroup1 := dwWarningsGroup1 OR 16#00000004;
END_IF;

(* Bit 3: Cavity Vacuum Sensor Degraded (1oo2 Mode) *)
IF nVac_TMR_Mode = 2 THEN
    dwWarningsGroup1 := dwWarningsGroup1 OR 16#00000008;
END_IF;

(* Bit 4: IR Pyrometer Sensor Degraded (1oo2 Mode) *)
IF nTemp_TMR_Mode = 2 THEN
    dwWarningsGroup1 := dwWarningsGroup1 OR 16#00000010;
END_IF;

(* Bit 5: Plug Force Sensor Degraded (1oo2 Mode) *)
IF nForce_TMR_Mode = 2 THEN
    dwWarningsGroup1 := dwWarningsGroup1 OR 16#00000020;
END_IF;

(* Bit 6: MPC Optimizer Sub-Optimal Convergence *)
IF NOT bMPCOptimizerConverged THEN
    dwWarningsGroup1 := dwWarningsGroup1 OR 16#00000040;
END_IF;

(* --- STATUS WORD: SUBSYSTEM OPERATIONAL TELEMETRY --- *)
(* Bit 0: Cell Sequence Master Enabled *)
IF bEnableMaster THEN
    dwStatusWord := dwStatusWord OR 16#00000001;
END_IF;

(* Bit 1: Automatic Cycle In Progress *)
IF (nFSM_CurrentState >= 1) AND (nFSM_CurrentState <= 11) THEN
    dwStatusWord := dwStatusWord OR 16#00000002;
END_IF;

(* Bit 2: Carousel Turntable Motion Active *)
IF nFSM_CurrentState = 2 THEN
    dwStatusWord := dwStatusWord OR 16#00000004;
END_IF;

(* Bit 3: Radiant Heating Oven Active *)
IF (nFSM_CurrentState = 3) OR (nFSM_CurrentState = 4) THEN
    dwStatusWord := dwStatusWord OR 16#00000008;
END_IF;

(* Bit 4: Pneumatic Bubble Pre-Blow Active *)
IF nFSM_CurrentState = 5 THEN
    dwStatusWord := dwStatusWord OR 16#00000010;
END_IF;

(* Bit 5: Mold Platen Tonnage Clamped *)
IF bPlatenTonnageLocked THEN
    dwStatusWord := dwStatusWord OR 16#00000020;
END_IF;

(* Bit 6: Servo Plug Assist In Motion *)
IF (nFSM_CurrentState = 7) OR (nFSM_CurrentState = 10) THEN
    dwStatusWord := dwStatusWord OR 16#00000040;
END_IF;

(* Bit 7: Mold Cavity Deep Vacuum Applied *)
IF (nFSM_CurrentState = 8) OR (nFSM_CurrentState = 9) THEN
    dwStatusWord := dwStatusWord OR 16#00000080;
END_IF;

(* Bit 8: In-Mold Vortex Chilled Air Active *)
IF bChilledAirCoolingJet THEN
    dwStatusWord := dwStatusWord OR 16#00000100;
END_IF;

(* Bit 9: Mold Ejector Stripper Pins Extended *)
IF bMoldEjectorPinExtend THEN
    dwStatusWord := dwStatusWord OR 16#00000200;
END_IF;

(* Bit 10: Station 4 Robotic Trimming Active *)
IF nFSM_CurrentState = 11 THEN
    dwStatusWord := dwStatusWord OR 16#00000400;
END_IF;

(* Bit 11: Emergency Fire Shield Dropped *)
IF bOvenFireShieldDrop THEN
    dwStatusWord := dwStatusWord OR 16#00000800;
END_IF;

(* Bit 12: All 2oo3 Sensor Triplets Healthy *)
IF (nSag_TMR_Mode = 3) AND (nVac_TMR_Mode = 3) AND (nTemp_TMR_Mode = 3) AND (nForce_TMR_Mode = 3) THEN
    dwStatusWord := dwStatusWord OR 16#00001000;
END_IF;

(* Bit 13: Part Quality Criteria Passed (Wall Thickness OK) *)
IF (rPredictedMinWall_mm >= 0.75) AND (rPredictedMaxWall_mm <= 4.50) THEN
    dwStatusWord := dwStatusWord OR 16#00002000;
END_IF;

(* Bit 14: Station Index Complete Strobe *)
IF bCarouselIndexComplete THEN
    dwStatusWord := dwStatusWord OR 16#00004000;
END_IF;

(* Bit 15: Master Sequence Ready For Next Cycle *)
IF (nFSM_CurrentState = 0) AND bSafetyEStop_OK AND bSafetyLightCurtain_OK THEN
    dwStatusWord := dwStatusWord OR 16#00008000;
END_IF;"""
    phases.append(phase7)

    # Closing
    closing = "END_FUNCTION_BLOCK"

    # Assemble ST
    full_st = "\n\n".join([header, var_input, var_output, var_internal] + phases + [closing])
    return full_st

if __name__ == "__main__":
    st_code = build_full_dataset()
    print(f"Generated ST Character Length: {len(st_code)}")
    print(f"First 100 chars:\n{st_code[:100]}")
    print(f"Last 100 chars:\n{st_code[-100:]}")
