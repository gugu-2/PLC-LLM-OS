# Modular generator for FB_Mining_SAG_BallMill_ComminutionClassification
import os
import sys
import json
import uuid
import re

def get_header():
    return """FUNCTION_BLOCK FB_Mining_SAG_BallMill_ComminutionClassification
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  MINING, HEAVY MINERAL PROCESSING & BENEFICIATION REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION : 40-FOOT SEMI-AUTOGENOUS GRINDING (SAG) & BALL MILL CLOSED COMMINUTION-CLASSIFICATION CIRCUIT
  DRIVE PLATFORM     : 28 MW GEARLESS RING MOTOR DRIVE (GMD / WRAP-AROUND SYNCHRONOUS MOTOR) WITH CYCLOCONVERTER
  BEARING TECHNOLOGY : HYDROSTATIC DUAL-TRUNNION SLIPPER BEARINGS WITH REYNOLDS DYNAMIC OIL VISCOSITY REGULATION
  CLASSIFICATION     : 14-CYCLONE RADIAL HYDROCYCLONE MANIFOLD WITH CORIOLIS SLURRY DENSITY & ULTRASONIC P80
  RECYCLE SUBSYSTEM  : VARIABLE-RATIO PEBBLE CRUSHER CIRCUIT WITH DYNAMIC MILL BELLY SLURRY POOL LEVEL OBSERVER
  PROCESS SAFETY     : IEC 61508 / IEC 61511 SIL-2/SIL-3 REDUNDANT PROTECTION WITH FROZEN CHARGE DROP ABORT
  NORMS & STANDARDS  : ISA-18.2 / IEC 62682 MANAGEMENT OF ALARMS, IEEE 841 / IEEE 1566 GMD SYSTEM INTEGRATION,
                       ISO 10816-3 INDUSTRIAL VIBRATION, DIN 31652 HYDRODYNAMIC JOURNAL BEARINGS,
                       BOND WORK INDEX COMMINUTION KINETICS, PLITT / AUSTIN HYDROCYCLONE & BALL MILL MODELS.
  AUTHOR             : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  FIRST-PRINCIPLES CYBER-PHYSICAL MODELING & COMMINUTION PHENOMENOLOGY:
  ----------------------------------------------------------------------------------------------------------------------
  1. 40-FOOT SAG MILL POWER DRAW & CHARGE DYNAMICS (HOGG & FUERSTENAU FORMULATION):
     - The SAG mill is a 40 ft (12.192 m) diameter by 25 ft (7.620 m) effective grinding length rotating cylinder.
       The charge consists of run-of-mine (ROM) coarse rock (-300 mm to +50 mm), steel grinding balls (125 mm diameter,
       occupying 12% to 18% of mill volume), water, and ore fines forming a high-density slurry.
     - The gross mechanical power drawn by the 28 MW gearless ring motor is governed by the center-of-mass offset
       of the active charge inside the rotating mill:
           P_draw = 2.05 * phi_bulk * L_eff * D_inside^2.5 * sin(alpha_toe) * (omega_mill / omega_crit) * (1 - beta_p * (omega_mill / omega_crit))
       where:
           phi_bulk   = Bulk density of dynamic charge mixture [t/m3] (typically 2.45 to 2.85 t/m3)
           L_eff      = Effective internal grinding length [m] = 7.62 m
           D_inside   = Inside mill diameter within shell liners [m] = 11.85 m
           omega_mill = Operational angular velocity [rad/s]
           omega_crit = Theoretical critical angular velocity [rad/s] = sqrt(2 * g / D_inside) = 1.286 rad/s (12.28 rpm)
           alpha_toe  = Dynamic dynamic lift angle of charge center-of-gravity (42 deg to 58 deg)
           beta_p     = High-speed slip slippage correction factor (0.10 to 0.18)

  2. FROZEN CHARGE DETECTION & BREAKAWAY DYNAMICS:
     - Following an un-cleared shutdown with slurry and grinding media remaining in the belly, the slurry solidifies
       into a cemented, cohesive monolithic arch ("frozen charge") keyed into the liner lifter bars.
     - When restarted, instead of tumbling freely at an angle of 35 deg to 45 deg, the frozen charge remains locked
       to the rotating shell until reaching an elevated angle (90 deg to 180 deg, apex), where gravity overcomes adhesion.
       The resulting 2,000-tonne mass free-falls onto the lower trunnions, causing catastrophic destruction of bearings,
       mill shell, and foundations.
     - Cyber-Physical Detection Criteria:
       During the initial slow inching or test-roll phase (0.5 to 1.0 rpm):
         a) Angle-Torque Breakaway: Loose charge naturally begins tumbling at rotor angle theta in [38 deg, 52 deg],
            accompanied by a distinct drop in motor torque dTm/dtheta < -K_breakaway.
         b) If motor torque continues rising past theta = 55 deg without torque relaxation, or if the integrated
            breakaway momentum exceeds safety limits, a catastrophic frozen charge is diagnosed.
         c) Acoustic Signature Confirmation: In healthy tumbling, shell microphones register continuous low-frequency
            slurry cascading sound. In a frozen charge condition, absolute acoustic stillness occurs until the drop.
         d) Failsafe Action: Instantaneous cycloconverter gate pulse inhibition, rapid mechanical caliper disc braking,
            and hydraulic jacking pump pressure sustain before rotor angle reaches 75 deg.

  3. HYDROSTATIC TRUNNION BEARING LUBRICATION & REYNOLDS VISCOSITY DYNAMICS:
     - The combined mill rotating mass with wet charge exceeds 4,200 metric tonnes, supported by dual hydrostatic
       trunnion bearings (feed and discharge journals, journal diameter 3.65 m).
     - Jacking Lift Phase: Multi-plunger high-pressure pumps deliver ISO VG 320 / 460 synthetic cylinder oil at
       320 to 420 bar into four opposed hydrostatic pockets per trunnion, generating hydrostatic lift:
           F_lift = sum(P_pocket_i * A_pocket_eff) >= M_total * g
       Eddy-current proximity transducers monitor lift height (nominal 140 to 220 um) before mill rotation is permitted.
     - Hydrodynamic Transition & Dynamic Viscosity Control:
       At operational speed (8.5 to 10.5 rpm), surface velocity reaches 1.8 to 2.2 m/s, generating hydrodynamic oil wedges
       governed by Reynolds lubrication equation:
           d/dx (h^3 / mu * dp/dx) + d/dz (h^3 / mu * dp/dz) = 6 * U_surf * dh/dx
       Dynamic viscosity mu(T) is strongly temperature dependent (Vogel-Fulcher-Tammann formulation):
           mu(T) = A_visc * exp(B_visc / (T_oil + C_visc))  [mPa.s or cP]
       Closed-loop cooling water modulating valves regulate oil header temperature to 42.0 deg C +/- 1.5 deg C.
       High oil temperature (> 55 deg C) causes viscosity collapse and bearing metal-to-metal boundary contact;
       low oil temperature (< 30 deg C) causes excessive hydraulic shear losses and pocket cavitation.

  4. 14-CYCLONE HYDROCYCLONE MANIFOLD CLASSIFICATION & CLOSED-CIRCUIT KINETICS:
     - SAG mill discharge slurry passes through a trommel screen (aperture 15 mm x 30 mm); undersize slurries into
       a 200 m3 cyclone feed sump. Sump slurry is pumped by a 1,600 kW variable-speed centrifugal slurry pump to
       a radial 14-cyclone manifold (Krebs 650 mm cyclones).
     - Hydrocyclone separation cut size d50c is modeled via the Plitt-Concha comminution classification equations:
           d50c = (K_plitt * D_cyc^0.46 * D_inlet^0.60 * D_vortex^1.21 * mu_slurry^0.50) /
                  (D_apex^0.71 * h_free^0.38 * Q_total^0.45 * (rho_solids - rho_liquid)^0.50)
     - Cyclone underflow (coarse fraction, 72% solids) gravitates to the 16 MW Ball Mill feed chute for finish grinding.
       Ball mill discharge recycles to the cyclone feed sump, establishing circulating load ratio:
           C_load = F_underflow / F_overflow = (rho_feed - rho_overflow) / (rho_underflow - rho_feed)
     - Cyclone overflow (fine product, target P80 = 75 um, 38% solids) overflows to flotation beneficiation.
       Particle size is continuously measured via on-line ultrasonic attenuation and laser diffraction spectrometry.

  5. PEBBLE CRUSHER RECYCLE & INTERNAL SLURRY POOL OBSERVER:
     - Trommel screen oversize ("critical size" pebbles, 15 to 65 mm resistant igneous ore core) is conveyed to a surge
       bin feeding two secondary cone pebble crushers.
     - Crusher product is either recycled back to the SAG mill feed conveyor to enhance comminution kinetic autogenous
       breakage, or diverted to ball mill feed based on pebble crusher power and circuit loading constraints.
     - Slurry Pool Volumetric Observer: When mill grate discharge slots blind or pulp lifters become hydraulically
       saturated, slurry pools in the SAG mill belly. The slurry pool cushions grinding ball impacts, reducing
       breakage kinetics and causing mill motor power draw to collapse while bearing pressure rises.
       The cyber-physical state observer continuously computes slurry pool volume V_pool from torque-angle acoustic ratios.
*)
"""

def get_var_declarations():
    return """VAR_INPUT
    (* Master Execution & Safety Interlocks *)
    bEnable                         : BOOL;     (* [bool] Master Function Block Execution Enable *)
    bReset                          : BOOL;     (* [bool] Master Fault & Latched Alarm Reset *)
    bAutoMode                       : BOOL;     (* [bool] Automatic Closed-Loop MPC Dispatch Permissive *)
    bStartCommand                   : BOOL;     (* [bool] Operator Circuit Start Sequence Initiate *)
    bStopCommand                    : BOOL;     (* [bool] Operator Controlled Grind-Out Flush Stop *)
    bEmergencyStop                  : BOOL;     (* [bool] Hardwired Dual-Channel SIL-3 Emergency Stop Loop *)

    (* Hydrostatic Bearing Sensors - 2oo3 TMR Channels *)
    rFeedTrunnionPressure_ChA       : REAL;     (* [bar] SAG Mill Feed Trunnion Hydrostatic Pad Oil Pressure Sensor Ch A *)
    rFeedTrunnionPressure_ChB       : REAL;     (* [bar] SAG Mill Feed Trunnion Hydrostatic Pad Oil Pressure Sensor Ch B *)
    rFeedTrunnionPressure_ChC       : REAL;     (* [bar] SAG Mill Feed Trunnion Hydrostatic Pad Oil Pressure Sensor Ch C *)
    rDischargeTrunnionPressure_ChA  : REAL;     (* [bar] SAG Mill Discharge Trunnion Hydrostatic Pad Oil Pressure Sensor Ch A *)
    rDischargeTrunnionPressure_ChB  : REAL;     (* [bar] SAG Mill Discharge Trunnion Hydrostatic Pad Oil Pressure Sensor Ch B *)
    rDischargeTrunnionPressure_ChC  : REAL;     (* [bar] SAG Mill Discharge Trunnion Hydrostatic Pad Oil Pressure Sensor Ch C *)
    rTrunnionOilFilm_Feed           : REAL;     (* [um] Eddy Current Proximity Probe Feed Lift Film Thickness *)
    rTrunnionOilFilm_Disch          : REAL;     (* [um] Eddy Current Proximity Probe Discharge Lift Film Thickness *)
    rBearingOilSupplyTemp           : REAL;     (* [deg C] Hydrostatic Lube Oil Header Supply Temperature *)

    (* 28 MW Gearless Ring Motor Drive (GMD) Sensors - 2oo3 TMR Channels *)
    rGMDActivePower_ChA             : REAL;     (* [kW] 28 MW GMD Active Electrical Power Transducer Ch A *)
    rGMDActivePower_ChB             : REAL;     (* [kW] 28 MW GMD Active Electrical Power Transducer Ch B *)
    rGMDActivePower_ChC             : REAL;     (* [kW] 28 MW GMD Active Electrical Power Transducer Ch C *)
    rGMDCurrent_RMS                 : REAL;     (* [A] GMD Stator Phase Current RMS Value *)
    rGMDRotorAngle                  : REAL;     (* [deg] High-Resolution Multi-Turn Resolver Absolute Rotor Angle [0..360] *)
    rGMDSpeed_Actual                : REAL;     (* [rpm] GMD Calibrated Rotational Speed Feedback *)

    (* Shell Acoustic Impact Transducers - 2oo3 TMR Channels *)
    rShellAcoustic_ChA              : REAL;     (* [%] Shell Piezo Acoustic Impact Microphone Ch A (Toe Zone) *)
    rShellAcoustic_ChB              : REAL;     (* [%] Shell Piezo Acoustic Impact Microphone Ch B (Mid Belly Zone) *)
    rShellAcoustic_ChC              : REAL;     (* [%] Shell Piezo Acoustic Impact Microphone Ch C (Shoulder Lifter Zone) *)
    rShellAcousticHighFreqPct       : REAL;     (* [%] Ball-on-Liner High Frequency Acoustic Energy Spectrum (>2kHz) *)

    (* Cyclone Feed Sump Slurry Level Transducers - 2oo3 TMR Channels *)
    rSumpSlurryLevel_ChA            : REAL;     (* [%] Cyclone Feed Sump Slurry Level Ultrasonic Transmitter Ch A *)
    rSumpSlurryLevel_ChB            : REAL;     (* [%] Cyclone Feed Sump Slurry Level Guided Radar Transmitter Ch B *)
    rSumpSlurryLevel_ChC            : REAL;     (* [%] Cyclone Feed Sump Slurry Level Hydrostatic Pressure Transmitter Ch C *)

    (* Cyclone Feed Slurry Density Transducers - 2oo3 TMR Channels *)
    rCycloneFeedDensity_ChA         : REAL;     (* [t/m3] Cyclone Feed Header Slurry Density Coriolis Meter Ch A *)
    rCycloneFeedDensity_ChB         : REAL;     (* [t/m3] Cyclone Feed Header Slurry Density Nuclear Density Gauge Ch B *)
    rCycloneFeedDensity_ChC         : REAL;     (* [t/m3] Cyclone Feed Header Slurry Density Radiometric Density Gauge Ch C *)

    (* Classification & Circuit Physical Process Variables *)
    rCycloneFeedPressure            : REAL;     (* [kPa] Radial Hydrocyclone Feed Ring Manifold Pressure *)
    rCycloneFeedFlowRate            : REAL;     (* [m3/h] Magnetic Flowmeter Cyclone Feed Total Slurry Flow *)
    rCycloneOverflowP80             : REAL;     (* [um] On-Line Ultrasonic Slurry Particle Size Analyzer P80 Passing *)
    rPebbleRecycleMassFlow          : REAL;     (* [t/h] Weightometer Pebble Crusher Discharge Recycle Mass Flow *)
    rBallMillActivePower            : REAL;     (* [kW] 16 MW Ball Mill Drive Active Electrical Power *)
    rBallMillTrunnionPressure       : REAL;     (* [bar] Ball Mill Hydrostatic Journal Bearing Pad Pressure *)

    (* Feedstock Geological & Competency Disturbances *)
    rBondWorkIndex_Estimated        : REAL;     (* [kWh/t] Ore Competency & Grindability Bond Work Index *)
    rOreFeedBulkDensity             : REAL;     (* [t/m3] Run-Of-Mine Coarse Ore Stockpile Bulk Density *)
    rOreFeedMoisturePct             : REAL;     (* [%] Microwave Moisture Sensor Raw Ore Moisture Content *)
END_VAR
VAR_OUTPUT
    (* Circuit Status & Safety Flags *)
    bReady                          : BOOL;     (* [bool] Comminution Circuit Ready for Normal Production Sequence *)
    bActive                         : BOOL;     (* [bool] SAG & Ball Mill Grinding Circuit Active in Production *)
    bFault                          : BOOL;     (* [bool] High-Severity Circuit Trip or Interlock Shutdown Active *)
    bFrozenChargeTrip               : BOOL;     (* [bool] Frozen Charge Detected - Immediate High-Speed Inching Abort *)
    bAcousticLinerAlert             : BOOL;     (* [bool] Direct Ball-on-Liner Impact Exceeds Safety Threshold *)
    bSlurryPoolAlert                : BOOL;     (* [bool] Internal Mill Belly Slurry Pool Holdup Overload Warning *)
    nFSM_CurrentState               : INT;      (* [enum] Active Finite State Machine Operational Stage [0..13] *)

    (* Actuator Dispatch Commands *)
    rFreshOreFeedRate_Cmd           : REAL;     (* [t/h] Variable Speed Ore Feeder Belt Tonnage Setpoint Command *)
    rSAGFeedWaterFlow_Cmd           : REAL;     (* [m3/h] SAG Mill Chute Dilution Water Flow Control Valve Setpoint *)
    rSAGSpeedSetpoint_Cmd           : REAL;     (* [rpm] 28 MW GMD Cycloconverter Speed Setpoint Reference *)
    rCyclonePumpSpeed_Cmd           : REAL;     (* [rpm] Cyclone Feed Slurry Pump VFD Speed Reference Command *)
    rSumpWaterFlow_Cmd              : REAL;     (* [m3/h] Cyclone Feed Sump Dilution Water Flow Valve Setpoint *)
    nActiveCyclones_Cmd             : INT;      (* [count] Number of Hydrocyclone Isolation Knife Gates Commanded Open [0..14] *)
    rPebbleRecycleRatio_Cmd         : REAL;     (* [%] Pebble Crusher Bypass/Recycle Splitter Flap Position Command *)
    rBallMillWaterFlow_Cmd          : REAL;     (* [m3/h] Ball Mill Feed Chute Dilution Water Valve Setpoint *)
    rBearingCoolingWaterValve_Cmd   : REAL;     (* [%] Lube Oil Plate Heat Exchanger Cooling Water Modulating Valve *)

    (* Cyber-Physical State & Classification Estimates *)
    rEstimatedSAGCharge_Tonnes      : REAL;     (* [t] Cyber-Physical State Estimate of SAG Mill Total Dynamic Charge *)
    rEstimatedSlurryPool_m3         : REAL;     (* [m3] Dynamic Volumetric Slurry Pool Level Holdup Estimate *)
    rEstimatedToeAngle_Deg          : REAL;     (* [deg] Angle-Torque Estimated Charge Dynamic Toe Impact Angle *)
    rCirculatingLoadRatio           : REAL;     (* [-] Calculated Hydrocyclone Circulating Load Ratio [F_under/F_over] *)

    (* Packed Diagnostics & ISA-18.2 Words *)
    dwStatusWord_Circuit            : DWORD;    (* [bits] Bit-Packed Comminution Subsystem Operational Status Word *)
    dwStatusWord_TMRHealth          : DWORD;    (* [bits] Bit-Packed 2oo3 Sensor Voting & Channel Degradation Health Word *)
    dwAlarmWord_Trips               : DWORD;    (* [bits] ISA-18.2 Priority 1 / Critical Trip Latched Alarm Word *)
    dwAlarmWord_Warnings            : DWORD;    (* [bits] ISA-18.2 Priority 2 / Advisory & Rate-of-Change Warning Word *)
END_VAR
VAR
    (* -------------------------------------------------------------------------
       8-STATE DISCRETE CYBER-PHYSICAL SYSTEM MATRICES (Ts = 0.050 s)
       States:
         x[1]: SAG Mill Total Dynamic Charge Mass [t]
         x[2]: SAG Mill Internal Slurry Volumetric Holdup [m3]
         x[3]: Dynamic Charge Toe Impact Angle [deg]
         x[4]: 28 MW GMD Active Electrical Power Draw [kW]
         x[5]: Cyclone Feed Sump Volumetric Slurry Level [%]
         x[6]: Cyclone Overflow Slurry Density [t/m3]
         x[7]: Ball Mill Total Circulating Load Mass Flow [t/h]
         x[8]: Final Product 80% Passing Particle Size P80 [um]
       ------------------------------------------------------------------------- *)
    aState_x                        : ARRAY[1..8] OF REAL;
    aState_x_next                   : ARRAY[1..8] OF REAL;
    aMatrix_A                       : ARRAY[1..8, 1..8] OF REAL;
    aMatrix_B                       : ARRAY[1..8, 1..8] OF REAL;
    aMatrix_C                       : ARRAY[1..8, 1..8] OF REAL;
    aMatrix_D                       : ARRAY[1..8, 1..8] OF REAL;
    aMatrix_E                       : ARRAY[1..8, 1..2] OF REAL;
    aDisturbance_d                  : ARRAY[1..2] OF REAL;
    aOutput_y                       : ARRAY[1..8] OF REAL;
    aOutput_y_meas                  : ARRAY[1..8] OF REAL;
    aObserverGain_L                 : ARRAY[1..8] OF REAL;
    aInnovation_e                   : ARRAY[1..8] OF REAL;
    bStateSpaceInitialized          : BOOL;

    (* -------------------------------------------------------------------------
       MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION STRUCTURES (Np = 10, Nc = 4)
       ------------------------------------------------------------------------- *)
    aWeight_Q                       : ARRAY[1..8] OF REAL;  (* Output tracking quadratic penalty diagonal *)
    aWeight_R                       : ARRAY[1..8] OF REAL;  (* Control action rate quadratic penalty diagonal *)
    aWeight_S                       : ARRAY[1..8] OF REAL;  (* Actuator boundary slack variable penalty diagonal *)
    aWeight_P                       : ARRAY[1..8] OF REAL;  (* Terminal state prediction penalty diagonal *)
    aSetpoints_r                    : ARRAY[1..8] OF REAL;  (* Reference trajectory setpoints *)
    aControl_u                      : ARRAY[1..8] OF REAL;  (* Dispatched control vector *)
    aControl_u_opt                  : ARRAY[1..8] OF REAL;  (* PGD optimizer candidate vector *)
    aControl_u_prev                 : ARRAY[1..8] OF REAL;  (* Previous cycle control vector for slew rate limits *)
    aDelta_u                        : ARRAY[1..8] OF REAL;  (* Control slew vector *)
    aActuator_Min                   : ARRAY[1..8] OF REAL;  (* Actuator lower box bounds *)
    aActuator_Max                   : ARRAY[1..8] OF REAL;  (* Actuator upper box bounds *)
    aActuator_MaxSlew               : ARRAY[1..8] OF REAL;  (* Max allowable actuator change per 50 ms cycle *)
    aGradient_u                     : ARRAY[1..8] OF REAL;  (* Gradient of quadratic objective wrt control vector *)
    aState_pred                     : ARRAY[0..10, 1..8] OF REAL; (* Forward predicted state trajectory *)
    aOutput_pred                    : ARRAY[1..10, 1..8] OF REAL; (* Forward predicted output trajectory *)
    rStepSize_alpha                 : REAL;     (* PGD gradient step size *)
    rCost_Tracking                  : REAL;     (* Running cumulative tracking cost *)
    rCost_ControlEffort             : REAL;     (* Running cumulative control effort penalty *)
    rCost_Terminal                  : REAL;     (* Running terminal cost *)
    rCost_Total                     : REAL;     (* Total quadratic objective value *)

    (* -------------------------------------------------------------------------
       2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES
       ------------------------------------------------------------------------- *)
    (* Channel 1: Feed Trunnion Pressure *)
    rFeedTrunnion_Voted             : REAL;
    bFeedTrunnion_ChA_Fault         : BOOL;
    bFeedTrunnion_ChB_Fault         : BOOL;
    bFeedTrunnion_ChC_Fault         : BOOL;
    rFeedTrunnion_Timer_AB          : REAL;
    rFeedTrunnion_Timer_BC          : REAL;
    rFeedTrunnion_Timer_CA          : REAL;
    nFeedTrunnion_HealthyCount      : INT;

    (* Channel 2: Discharge Trunnion Pressure *)
    rDischTrunnion_Voted            : REAL;
    bDischTrunnion_ChA_Fault        : BOOL;
    bDischTrunnion_ChB_Fault        : BOOL;
    bDischTrunnion_ChC_Fault        : BOOL;
    rDischTrunnion_Timer_AB         : REAL;
    rDischTrunnion_Timer_BC         : REAL;
    rDischTrunnion_Timer_CA         : REAL;
    nDischTrunnion_HealthyCount     : INT;

    (* Channel 3: 28 MW GMD Active Power *)
    rGMDPower_Voted                 : REAL;
    bGMDPower_ChA_Fault             : BOOL;
    bGMDPower_ChB_Fault             : BOOL;
    bGMDPower_ChC_Fault             : BOOL;
    rGMDPower_Timer_AB              : REAL;
    rGMDPower_Timer_BC              : REAL;
    rGMDPower_Timer_CA              : REAL;
    nGMDPower_HealthyCount          : INT;

    (* Channel 4: Shell Acoustic Impact *)
    rShellAcoustic_Voted            : REAL;
    bShellAcoustic_ChA_Fault        : BOOL;
    bShellAcoustic_ChB_Fault        : BOOL;
    bShellAcoustic_ChC_Fault        : BOOL;
    rShellAcoustic_Timer_AB         : REAL;
    rShellAcoustic_Timer_BC         : REAL;
    rShellAcoustic_Timer_CA         : REAL;
    nShellAcoustic_HealthyCount     : INT;

    (* Channel 5: Cyclone Sump Level *)
    rSumpLevel_Voted                : REAL;
    bSumpLevel_ChA_Fault            : BOOL;
    bSumpLevel_ChB_Fault            : BOOL;
    bSumpLevel_ChC_Fault            : BOOL;
    rSumpLevel_Timer_AB             : REAL;
    rSumpLevel_Timer_BC             : REAL;
    rSumpLevel_Timer_CA             : REAL;
    nSumpLevel_HealthyCount         : INT;

    (* Channel 6: Cyclone Feed Density *)
    rCycloneDensity_Voted           : REAL;
    bCycloneDensity_ChA_Fault       : BOOL;
    bCycloneDensity_ChB_Fault       : BOOL;
    bCycloneDensity_ChC_Fault       : BOOL;
    rCycloneDensity_Timer_AB        : REAL;
    rCycloneDensity_Timer_BC        : REAL;
    rCycloneDensity_Timer_CA        : REAL;
    nCycloneDensity_HealthyCount    : INT;

    (* Discrepancy Thresholds & Filters *)
    rTolerance_TrunnionPressure     : REAL;     (* [bar] Max acceptable channel discrepancy *)
    rTolerance_GMDPower             : REAL;     (* [kW] Max acceptable channel discrepancy *)
    rTolerance_ShellAcoustic        : REAL;     (* [%] Max acceptable channel discrepancy *)
    rTolerance_SumpLevel            : REAL;     (* [%] Max acceptable channel discrepancy *)
    rTolerance_CycloneDensity       : REAL;     (* [t/m3] Max acceptable channel discrepancy *)
    rDiscrepancyTimeLimit           : REAL;     (* [s] Max time before flagging failed transducer *)

    (* -------------------------------------------------------------------------
       REYNOLDS HYDRODYNAMIC LUBRICATION & BEARING THERMAL REGULATION
       ------------------------------------------------------------------------- *)
    rOilVisc_A                      : REAL;     (* Vogel viscosity constant A *)
    rOilVisc_B                      : REAL;     (* Vogel viscosity constant B *)
    rOilVisc_C                      : REAL;     (* Vogel viscosity constant C *)
    rLubeOilDynamicViscosity        : REAL;     (* [cP] Calculated dynamic viscosity mu(T) *)
    rLubeOilTemp_Setpoint           : REAL;     (* [deg C] Target oil header temperature (42.0 C) *)
    rLubeTemp_Error                 : REAL;     (* [deg C] Temperature regulation error *)
    rLubeTemp_Integral              : REAL;     (* Integral accumulator for cooling water valve *)
    rLubeTemp_Derivative            : REAL;     (* Derivative term for cooling water valve *)
    rLubeTemp_Error_Prev            : REAL;     (* Previous cycle temperature error *)
    bJackingPermissive              : BOOL;     (* True when hydrostatic lift pressure and film thickness verified *)
    tJackingWarmupTimer             : REAL;     (* [s] Jacking oil stabilization timer *)

    (* -------------------------------------------------------------------------
       FROZEN CHARGE DETECTION & BREAKAWAY MOMENTUM OBSERVER
       ------------------------------------------------------------------------- *)
    rRotorAngle_Prev                : REAL;     (* [deg] Previous scan absolute rotor angle *)
    rRotorAngle_Delta               : REAL;     (* [deg] Angular displacement per scan *)
    rRotorAngle_Integrated          : REAL;     (* [deg] Cumulative rotation from rest start *)
    rTorque_Actual                  : REAL;     (* [kNm] Estimated motor torque from GMD power and speed *)
    rTorque_PeakDetected            : REAL;     (* [kNm] Maximum observed torque during start roll *)
    rAngle_AtTorquePeak             : REAL;     (* [deg] Rotor angle when peak torque occurred *)
    bTorqueBreakoverObserved        : BOOL;     (* True if torque dropped by required margin *)
    rAcousticTumble_Integral        : REAL;     (* Integrated acoustic energy during roll *)
    bFrozenChargeAbortCondition     : BOOL;     (* Immediate abort trigger flag *)
    tFrozenRollTimer                : REAL;     (* [s] Test roll phase duration watchdog *)

    (* -------------------------------------------------------------------------
       SLURRY POOL OBSERVER & COMMINUTION PHENOMENOLOGY VARIABLES
       ------------------------------------------------------------------------- *)
    rPulpLifterMaxDischarge         : REAL;     (* [m3/h] Theoretical pulp lifter discharge capacity *)
    rSlurryInflowTotal              : REAL;     (* [m3/h] Sum of ore water and dilution water *)
    rSlurryDischargeEstimated       : REAL;     (* [m3/h] Model-estimated volumetric slurry discharge *)
    rSlurryPoolVolume_Observed      : REAL;     (* [m3] Filtered estimate of internal slurry pool *)
    rPlitt_d50c                     : REAL;     (* [um] Plitt model hydrocyclone cut size *)
    rPlitt_SharpnessIndex           : REAL;     (* [-] Hydrocyclone classification sharpness index *)
    rAustin_BreakageRate            : REAL;     (* [1/h] Ball mill primary breakage kinetic rate *)

    (* -------------------------------------------------------------------------
       ACOUSTIC SHELL PROTECTION & LINER DAMAGE MITIGATION
       ------------------------------------------------------------------------- *)
    rShellHighFreq_Filtered         : REAL;     (* [%] Filtered ball-on-liner impact energy *)
    rAcousticImpact_EMA_Alpha       : REAL;     (* Exponential moving average filter coefficient *)
    bLinerImpactWarningActive       : BOOL;     (* Liner damage risk warning *)
    rAcousticSpeedBackoffRate       : REAL;     (* [rpm] Speed trim deduction under high impact *)

    (* -------------------------------------------------------------------------
       14-STAGE FINITE STATE MACHINE (FSM) CONTROL REGISTERS
       ------------------------------------------------------------------------- *)
    nFSM_NextState                  : INT;      (* Next state transition target *)
    tFSM_StateTimer                 : REAL;     (* [s] Elapsed time in active state *)
    nFSM_SubPhase                   : INT;      (* Sub-phase execution index *)
    bFSM_TransitionRequested        : BOOL;     (* Handshake flag for state transition *)
    rSpeedRampTarget                : REAL;     (* [rpm] Intermediate speed setpoint during acceleration *)
    rOreFeedRampTarget              : REAL;     (* [t/h] Intermediate tonnage setpoint during feed ramp *)
    tGrindOutTimer                  : REAL;     (* [s] Countdown timer for flush grind-out *)

    (* -------------------------------------------------------------------------
       ISA-18.2 ALARM MATRIX LIMITS, DEADBANDS & STATUS WORDS
       ------------------------------------------------------------------------- *)
    (* Process Alarm Thresholds *)
    rLimit_FeedPress_HH             : REAL;     (* [bar] 85.0 *)
    rLimit_FeedPress_H              : REAL;     (* [bar] 75.0 *)
    rLimit_FeedPress_L              : REAL;     (* [bar] 45.0 *)
    rLimit_FeedPress_LL             : REAL;     (* [bar] 35.0 *)
    rDeadband_FeedPress             : REAL;     (* [bar] 2.5 *)

    rLimit_DischPress_HH            : REAL;     (* [bar] 90.0 *)
    rLimit_DischPress_H             : REAL;     (* [bar] 80.0 *)
    rLimit_DischPress_L             : REAL;     (* [bar] 48.0 *)
    rLimit_DischPress_LL            : REAL;     (* [bar] 38.0 *)
    rDeadband_DischPress            : REAL;     (* [bar] 2.5 *)

    rLimit_LubeTemp_HH              : REAL;     (* [deg C] 62.0 *)
    rLimit_LubeTemp_H               : REAL;     (* [deg C] 52.0 *)
    rLimit_LubeTemp_L               : REAL;     (* [deg C] 32.0 *)
    rLimit_LubeTemp_LL              : REAL;     (* [deg C] 25.0 *)
    rDeadband_LubeTemp              : REAL;     (* [deg C] 1.5 *)

    rLimit_GMDPower_HH              : REAL;     (* [kW] 27500.0 *)
    rLimit_GMDPower_H               : REAL;     (* [kW] 25500.0 *)
    rLimit_GMDPower_L               : REAL;     (* [kW] 8000.0 *)
    rLimit_GMDPower_LL              : REAL;     (* [kW] 3000.0 *)
    rDeadband_GMDPower              : REAL;     (* [kW] 350.0 *)

    rLimit_AcousticImpact_HH        : REAL;     (* [%] 85.0 *)
    rLimit_AcousticImpact_H         : REAL;     (* [%] 65.0 *)
    rDeadband_AcousticImpact        : REAL;     (* [%] 3.0 *)

    rLimit_SumpLevel_HH             : REAL;     (* [%] 92.0 *)
    rLimit_SumpLevel_H              : REAL;     (* [%] 80.0 *)
    rLimit_SumpLevel_L              : REAL;     (* [%] 25.0 *)
    rLimit_SumpLevel_LL             : REAL;     (* [%] 15.0 *)
    rDeadband_SumpLevel             : REAL;     (* [%] 2.0 *)

    rLimit_CycPressure_HH           : REAL;     (* [kPa] 160.0 *)
    rLimit_CycPressure_H            : REAL;     (* [kPa] 135.0 *)
    rLimit_CycPressure_L            : REAL;     (* [kPa] 70.0 *)
    rLimit_CycPressure_LL           : REAL;     (* [kPa] 50.0 *)
    rDeadband_CycPressure           : REAL;     (* [kPa] 4.0 *)

    rLimit_CycDensity_HH            : REAL;     (* [t/m3] 1.82 *)
    rLimit_CycDensity_H             : REAL;     (* [t/m3] 1.74 *)
    rLimit_CycDensity_L             : REAL;     (* [t/m3] 1.45 *)
    rLimit_CycDensity_LL            : REAL;     (* [t/m3] 1.35 *)
    rDeadband_CycDensity            : REAL;     (* [t/m3] 0.02 *)

    rLimit_OverflowP80_HH           : REAL;     (* [um] 115.0 *)
    rLimit_OverflowP80_H            : REAL;     (* [um] 95.0 *)
    rLimit_OverflowP80_L            : REAL;     (* [um] 55.0 *)
    rLimit_OverflowP80_LL           : REAL;     (* [um] 45.0 *)
    rDeadband_OverflowP80           : REAL;     (* [um] 2.5 *)

    rLimit_SAGCharge_HH             : REAL;     (* [t] 2350.0 *)
    rLimit_SAGCharge_H              : REAL;     (* [t] 2150.0 *)
    rLimit_SAGCharge_L              : REAL;     (* [t] 1400.0 *)
    rLimit_SAGCharge_LL             : REAL;     (* [t] 1200.0 *)
    rDeadband_SAGCharge             : REAL;     (* [t] 30.0 *)

    (* Rate-of-Change (RoC) Monitoring *)
    rFeedPress_PrevScan             : REAL;     (* [bar] Previous scan value *)
    rDischPress_PrevScan            : REAL;     (* [bar] Previous scan value *)
    rGMDPower_PrevScan              : REAL;     (* [kW] Previous scan value *)
    rSumpLevel_PrevScan             : REAL;     (* [%] Previous scan value *)
    rFeedPress_RoC                  : REAL;     (* [bar/s] *)
    rDischPress_RoC                 : REAL;     (* [bar/s] *)
    rGMDPower_RoC                   : REAL;     (* [kW/s] *)
    rSumpLevel_RoC                  : REAL;     (* [%/s] *)

    (* Loop and Math Iteration Counters *)
    i                               : INT;
    j                               : INT;
    k                               : INT;
    nIter                           : INT;
    nStep                           : INT;
    rTempSum                        : REAL;
    rTempGrad                       : REAL;
    rTempPrediction                 : REAL;
    rTempDiff                       : REAL;
    rTempSlack                      : REAL;
    rMinVal                         : REAL;
    rMaxVal                         : REAL;
    rMidVal                         : REAL;
END_VAR
"""

print("Header and VAR declarations ready.")
