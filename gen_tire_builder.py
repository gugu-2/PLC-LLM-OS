import json
import os
import re

def generate_code():
    parts = []

    # ----------------------------------------------------------------------------------------------------------
    # HEADER & DECLARATION
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_Plastics_RadialTire_BuildingMachine_DualDrum
(*
    ==========================================================================================================
    LUMINA CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL ROBOTICS SPECIFICATION
    Domain: Plastics, Rubber & Tire Manufacturing: Automated Dual-Drum Steel-Belted Radial Passenger / 
            Light Truck Tire Building Machine (TBM) with Dynamic Carcass Shaping Bladder & Laser Centering
    System Architecture: High-Precision Dual-Drum Tire Building Cell (VMI MAXX / Krupp Tier-1 Architecture)
    Compliance: ISO 20430:2020 (Rubber and plastics machines - Tyre building machines), ISO 13849-1 PL-e,
                IEC 62061 SIL-3, ISA-18.2 Alarm Management, RMA / ETRTO Radial Green Tire Standards
    Cycle Target: High-speed passenger radial (PCR) / light truck (LTR) cycle time < 38.5 s / green tire
    
    Subsystems Controlled:
      1. Drum 1 (Carcass Drum): Segmented collapsible drum, mechanical bead-locking slides, turn-up bladders,
         high-precision center toroidal shaping bladder, inner liner / body ply servicer electronic line shaft.
      2. Drum 2 (Breaker & Tread Drum): Expanding segmented belt drum, steel belt ply 1 (+21 deg) & ply 2
         (-21 deg) applicators, high-speed 0-degree spiral nylon cap ply winder, extruded rubber tread servicer.
      3. Multi-Axis Dynamic Transfer Ring: Coaxial servo gantry carriage, 24-segment radial gripper ring,
         vacuum retention cups, dynamic centering metrology (+/- 0.1 mm concentricity transfer over Drum 1).
      4. In-Line 3D Blue-Laser Triangulation Scanners: 360-deg circumferential profile metrology measuring
         splice overlap width (1.5 to 3.5 mm), ply thickness step, dog-ear mismatch, and 1H/2H runout harmonics.
      5. Dynamic Carcass Shaping & Dual Ballscrew Bead Locks: Polytropic pneumatic bladder expansion (0.5 to
         2.5 bar) synchronized with symmetric ballscrew bead slide translation to form true toroidal geometry.
      6. Twin Multi-Axis Robotic Stitchers: Left-hand and right-hand servo stitcher arms with closed-loop
         normal/tangential load-cell force vector control (up to 2,500 N) tracing crown-to-bead meridian contour.
      7. High-Speed Servicer Festoons: Dancer arm potentiometers and regenerative servo drives maintaining web
         tension to prevent irreversible uncured elastomeric cord distortion.
      8. Discrete State-Space Model: 16x16 state matrix A, 16x8 matrix B, C, D incorporating Maxwell-Wiechert
         viscoelastic rubber stress relaxation, bladder pneumatic-volume dynamics, and stitcher contact kinetics.
      9. Receding-Horizon Model Predictive Control (MPC): 5-step predictive horizon optimization minimizing
         quadratic tracking errors and actuator rate penalties with analytical projected gradient descent.
      10. 2oo3 Triple Modular Redundancy (TMR): 4 redundant transducer banks with bumpless degradation.
      11. 12-Stage Operational Finite State Machine (FSM): Full lifecycle green tire building sequence.
      12. ISA-18.2 Multi-Tiered Alarm Matrix: Deadband hysteresis, priority escalation, and bitfield telemetry.
    ==========================================================================================================
*)
""")

    # ----------------------------------------------------------------------------------------------------------
    # VAR_INPUT
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* Master Hardware System & Supervisory Interlocks *)
    bMasterEnable                       : BOOL;       (* Master operational cell enable command [binary] *)
    bEmergencyStop_CircuitOK            : BOOL;       (* Dual-channel safety circuit status [binary] *)
    bSafetyScannerClear                 : BOOL;       (* Perimeter safety area laser scanner zone clear [binary] *)
    bRecipeStartTrigger                 : BOOL;       (* Host recipe sequence execution start trigger [binary] *)
    bRecipeAbortTrigger                 : BOOL;       (* Host recipe emergency abort trigger [binary] *)
    bFaultReset                         : BOOL;       (* HMI alarm acknowledgment and reset push-button [binary] *)
    iTireRecipeID                       : INT;        (* Tire SKU recipe selector (1=225/55R18, 2=205/55R16, 3=245/45R19) [dimensionless] *)
    rTireTargetCrownOD_mm               : REAL;       (* Green tire target crown outer diameter [mm] *)
    rTargetBeadDistance_mm              : REAL;       (* Green tire target bead-to-bead axial spacing [mm] *)
    rTargetShapingPressure_bar          : REAL;       (* Target internal carcass toroidal shaping pressure [bar] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Bank 1: Drum 1 Optical Absolute Resolvers *)
    rDrum1_ResolverAngle_deg_ChA        : REAL;       (* Drum 1 carcass drum optical resolver angle channel A [deg] *)
    rDrum1_ResolverAngle_deg_ChB        : REAL;       (* Drum 1 carcass drum optical resolver angle channel B [deg] *)
    rDrum1_ResolverAngle_deg_ChC        : REAL;       (* Drum 1 carcass drum optical resolver angle channel C [deg] *)
    rDrum1_Speed_rpm_ChA                : REAL;       (* Drum 1 rotational velocity feedback channel A [rpm] *)
    rDrum1_Speed_rpm_ChB                : REAL;       (* Drum 1 rotational velocity feedback channel B [rpm] *)
    rDrum1_Speed_rpm_ChC                : REAL;       (* Drum 1 rotational velocity feedback channel C [rpm] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Bank 2: Carcass Shaping Air Pressure Transducers *)
    rShapingPressure_bar_ChA            : REAL;       (* Carcass shaping bladder pressure transducer channel A [bar] *)
    rShapingPressure_bar_ChB            : REAL;       (* Carcass shaping bladder pressure transducer channel B [bar] *)
    rShapingPressure_bar_ChC            : REAL;       (* Carcass shaping bladder pressure transducer channel C [bar] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Bank 3: In-Line 3D Blue-Laser Splice Overlap Sensors *)
    rLaser_SpliceOverlap_mm_ChA         : REAL;       (* Drum 1 3D blue-laser splice overlap measurement channel A [mm] *)
    rLaser_SpliceOverlap_mm_ChB         : REAL;       (* Drum 1 3D blue-laser splice overlap measurement channel B [mm] *)
    rLaser_SpliceOverlap_mm_ChC         : REAL;       (* Drum 1 3D blue-laser splice overlap measurement channel C [mm] *)
    rLaser_SpliceThickness_mm           : REAL;       (* Laser measured splice seam thickness step [mm] *)
    rLaser_LateralOffset_mm             : REAL;       (* Laser detected ply centerline lateral offset deviation [mm] *)
    rLaser_AngularSkew_deg              : REAL;       (* Laser detected ply leading edge angular skew [deg] *)
    rLaser_DogEar_Height_mm             : REAL;       (* Laser detected dog-ear corner splice height mismatch [mm] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Bank 4: Twin Stitcher Piezoelectric Load Cells *)
    rStitcherForce_LH_N_ChA             : REAL;       (* Left-hand stitcher roller radial load cell channel A [N] *)
    rStitcherForce_LH_N_ChB             : REAL;       (* Left-hand stitcher roller radial load cell channel B [N] *)
    rStitcherForce_LH_N_ChC             : REAL;       (* Left-hand stitcher roller radial load cell channel C [N] *)
    rStitcherForce_RH_N_ChA             : REAL;       (* Right-hand stitcher roller radial load cell channel A [N] *)
    rStitcherForce_RH_N_ChB             : REAL;       (* Right-hand stitcher roller radial load cell channel B [N] *)
    rStitcherForce_RH_N_ChC             : REAL;       (* Right-hand stitcher roller radial load cell channel C [N] *)

    (* Drum 2 (Breaker/Belt & Tread Drum) Servos & Sensors *)
    rDrum2_ResolverAngle_deg            : REAL;       (* Drum 2 belt drum optical resolver position [deg] *)
    rDrum2_Speed_rpm                    : REAL;       (* Drum 2 rotational velocity feedback [rpm] *)
    rDrum2_SegmentDiameter_mm           : REAL;       (* Drum 2 expanding segmented circumference diameter [mm] *)
    bDrum2_Expanded_Prox                : BOOL;       (* Drum 2 fully expanded mechanical limit switch [binary] *)
    bDrum2_Collapsed_Prox               : BOOL;       (* Drum 2 fully collapsed mechanical limit switch [binary] *)

    (* Bead Slide & Setter Positions *)
    rBeadSlide_LH_Pos_mm                : REAL;       (* Left-hand mechanical bead lock slide linear position [mm] *)
    rBeadSlide_RH_Pos_mm                : REAL;       (* Right-hand mechanical bead lock slide linear position [mm] *)
    rBeadSetter_LH_Pos_mm               : REAL;       (* Left-hand bead applicator ring carriage linear position [mm] *)
    rBeadSetter_RH_Pos_mm               : REAL;       (* Right-hand bead applicator ring carriage linear position [mm] *)
    bBeadLock_LH_Clamped                : BOOL;       (* Left-hand bead core mechanical clamp confirmed [binary] *)
    bBeadLock_RH_Clamped                : BOOL;       (* Right-hand bead core mechanical clamp confirmed [binary] *)

    (* Multi-Axis Dynamic Transfer Ring Gantry *)
    rTransferRing_AxialPos_mm           : REAL;       (* Transfer ring gantry longitudinal carriage position [mm] *)
    rTransferRing_SegmentDiam_mm        : REAL;       (* Transfer ring segmented internal gripper diameter [mm] *)
    bTransferRing_VacuumLocked          : BOOL;       (* Transfer ring vacuum suction cups hold confirmed [binary] *)
    rTransferRing_LaserConcentricity_mm : REAL;       (* Dynamic laser coaxial runout sensor [mm] *)

    (* High-Speed Servicer Festoons & Dancers *)
    rFestoonTension_InnerLiner_N        : REAL;       (* Inner liner servicer web dancer tension load cell [N] *)
    rFestoonTension_BodyPly_N           : REAL;       (* Body ply servicer web dancer tension load cell [N] *)
    rFestoonTension_Belt1_N             : REAL;       (* Steel belt 1 servicer web dancer tension load cell [N] *)
    rFestoonTension_Belt2_N             : REAL;       (* Steel belt 2 servicer web dancer tension load cell [N] *)
    rFestoonTension_CapPly_N            : REAL;       (* Nylon cap ply high-speed tension transducer [N] *)
    rFestoonTension_Tread_N             : REAL;       (* Extruded tread festoon dancer tension load cell [N] *)
    rDancerPosition_InnerLiner_pct      : REAL;       (* Inner liner dancer arm position potentiometer [%] *)
    rDancerPosition_Tread_pct           : REAL;       (* Tread festoon dancer arm position potentiometer [%] *)

    (* Stitcher Multi-Axis Servo Position Feedbacks *)
    rStitcherArm_LH_Axial_mm            : REAL;       (* Left-hand stitcher carriage axial position [mm] *)
    rStitcherArm_RH_Axial_mm            : REAL;       (* Right-hand stitcher carriage axial position [mm] *)
    rStitcherArm_LH_Radial_mm           : REAL;       (* Left-hand stitcher roller radial position [mm] *)
    rStitcherArm_RH_Radial_mm           : REAL;       (* Right-hand stitcher roller radial position [mm] *)
    rStitcherArm_LH_Angle_deg           : REAL;       (* Left-hand stitcher roller swivel orientation angle [deg] *)
    rStitcherArm_RH_Angle_deg           : REAL;       (* Right-hand stitcher roller swivel orientation angle [deg] *)
END_VAR
""")

    # ----------------------------------------------------------------------------------------------------------
    # VAR_OUTPUT
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* Supervisory System Status *)
    bSystemReady                        : BOOL;       (* TBM dual-drum cell ready for automatic cycle [binary] *)
    bCycleInProgress                    : BOOL;       (* Automatic tire building sequence actively executing [binary] *)
    bCycleCompleted                     : BOOL;       (* Green tire build cycle successfully completed strobe [binary] *)
    bGeneralFault                       : BOOL;       (* Active fault condition blocking operation [binary] *)
    bEmergencyHalted                    : BOOL;       (* Emergency stop or protective stop activated [binary] *)
    iCurrentStage                       : INT;        (* Active 12-stage FSM state index (1-12) [dimensionless] *)
    rCycleTimeElapsed_s                 : REAL;       (* Current tire building cycle elapsed timer [s] *)
    rGreenTire_OD_Actual_mm             : REAL;       (* Laser measured finished green tire outer diameter [mm] *)
    rGreenTire_BeadDist_Actual_mm       : REAL;       (* Measured finished green tire bead distance [mm] *)
    bSpliceQuality_Passed               : BOOL;       (* All carcass, belt, and tread splices within tolerance [binary] *)

    (* Drum 1 & 2 Actuator Commands *)
    rDrum1_SpeedCmd_rpm                 : REAL;       (* Drum 1 carcass drum servo speed setpoint [rpm] *)
    rDrum1_TorqueLimit_Nm               : REAL;       (* Drum 1 servo motor torque limit [Nm] *)
    rDrum2_SpeedCmd_rpm                 : REAL;       (* Drum 2 belt drum servo speed setpoint [rpm] *)
    rDrum2_TorqueLimit_Nm               : REAL;       (* Drum 2 servo motor torque limit [Nm] *)
    bDrum1_ExpandCmd                    : BOOL;       (* Drum 1 segment mechanical expansion solenoid [binary] *)
    bDrum1_CollapseCmd                  : BOOL;       (* Drum 1 segment collapse solenoid [binary] *)
    bDrum2_ExpandCmd                    : BOOL;       (* Drum 2 segment mechanical expansion solenoid [binary] *)
    bDrum2_CollapseCmd                  : BOOL;       (* Drum 2 segment collapse solenoid [binary] *)

    (* Shaping Bladder & Turn-Up Pneumatics Actuation *)
    rShapingPressure_Cmd_bar            : REAL;       (* Proportional pressure control valve command [bar] *)
    bShapingAir_InflateValve            : BOOL;       (* Main shaping air high-volume fill valve [binary] *)
    bShapingAir_ExhaustValve            : BOOL;       (* Main shaping air rapid exhaust safety valve [binary] *)
    bTurnUpBladder_LH_Cmd               : BOOL;       (* Left-hand turn-up bladder inflation valve [binary] *)
    bTurnUpBladder_RH_Cmd               : BOOL;       (* Right-hand turn-up bladder inflation valve [binary] *)

    (* Bead Slide & Setter Actuation *)
    rBeadSlide_LH_SpeedCmd_mms          : REAL;       (* Left-hand bead lock slide servo velocity [mm/s] *)
    rBeadSlide_RH_SpeedCmd_mms          : REAL;       (* Right-hand bead lock slide servo velocity [mm/s] *)
    bBeadLock_ClampCmd                  : BOOL;       (* Bead lock mechanical toggle clamp actuation [binary] *)
    rBeadSetter_LH_PosCmd_mm            : REAL;       (* Left-hand bead setter gantry target position [mm] *)
    rBeadSetter_RH_PosCmd_mm            : REAL;       (* Right-hand bead setter gantry target position [mm] *)

    (* Dynamic Transfer Ring Gantry Commands *)
    rTransferRing_AxialSpeedCmd_mms     : REAL;       (* Transfer ring gantry servo traverse velocity [mm/s] *)
    rTransferRing_TargetAxialPos_mm     : REAL;       (* Transfer ring gantry target axial position [mm] *)
    rTransferRing_SegmentDiamCmd_mm     : REAL;       (* Transfer ring segment clamp target diameter [mm] *)
    bTransferRing_VacuumCmd             : BOOL;       (* Transfer ring suction cup vacuum ejector enable [binary] *)
    bTransferRing_GripLocked            : BOOL;       (* Transfer ring mechanical segment lock engaged [binary] *)

    (* Twin Multi-Axis Stitcher Servo Actuation *)
    rStitcher_LH_ForceCmd_N             : REAL;       (* Left-hand stitcher roller closed-loop radial force command [N] *)
    rStitcher_RH_ForceCmd_N             : REAL;       (* Right-hand stitcher roller closed-loop radial force command [N] *)
    rStitcher_LH_AxialVelCmd_mms        : REAL;       (* Left-hand stitcher carriage axial feed velocity [mm/s] *)
    rStitcher_RH_AxialVelCmd_mms        : REAL;       (* Right-hand stitcher carriage axial feed velocity [mm/s] *)
    rStitcher_LH_SwivelAngleCmd_deg     : REAL;       (* Left-hand stitcher roller normal contour angle [deg] *)
    rStitcher_RH_SwivelAngleCmd_deg     : REAL;       (* Right-hand stitcher roller normal contour angle [deg] *)

    (* Servicers & Auxiliaries *)
    rServicer_InnerLiner_SpeedCmd_mms   : REAL;       (* Inner liner servicer feed drive velocity [mm/s] *)
    rServicer_Tread_SpeedCmd_mms        : REAL;       (* Tread applicator servicer feed drive velocity [mm/s] *)
    rCapPly_Winder_TensionCmd_N         : REAL;       (* Nylon cap ply high-speed winder brake tension [N] *)
    bUltrasonicCutter_Trigger           : BOOL;       (* Tread ultrasonic guillotine cutter cut trigger [binary] *)
    bGreenTireUnloader_PickCmd          : BOOL;       (* Green tire unloading manipulator pick command [binary] *)

    (* Diagnostic Telemetry Words *)
    dwDiagnosticWord_01                 : DWORD;      (* System operational status and TMR health telemetry [bitfield] *)
    dwDiagnosticWord_02                 : DWORD;      (* ISA-18.2 Warning and High Alarms [bitfield] *)
    dwDiagnosticWord_03                 : DWORD;      (* ISA-18.2 Critical High-High and Low-Low Trip Alarms [bitfield] *)
    dwDiagnosticWord_04                 : DWORD;      (* Laser metrology and quality inspection status [bitfield] *)
END_VAR
""")

    # ----------------------------------------------------------------------------------------------------------
    # VAR (INTERNAL DATA STRUCTURES)
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""VAR
    (* ====================================================================================================== *)
    (* SECTION 1: DISCRETE STATE-SPACE (16x16) & RECEDING-HORIZON MPC DATA STRUCTURES                       *)
    (* ====================================================================================================== *)
    (* State Vector x[0..15]:
         x[0]  : Drum 1 angular speed [rad/s]
         x[1]  : Drum 1 angular position [rad]
         x[2]  : Drum 2 angular speed [rad/s]
         x[3]  : Drum 2 angular position [rad]
         x[4]  : Carcass shaping bladder pressure [bar]
         x[5]  : Carcass shaping bladder volume [dm3]
         x[6]  : LH Bead slide position [mm]
         x[7]  : RH Bead slide position [mm]
         x[8]  : Viscoelastic rubber relaxation stress [kPa]
         x[9]  : LH Stitcher roller radial contact force [N]
         x[10] : RH Stitcher roller radial contact force [N]
         x[11] : Transfer ring gantry axial position [mm]
         x[12] : Transfer ring radial gripper diameter [mm]
         x[13] : Carcass crown outer diameter [mm]
         x[14] : Servicer festoon web tension [N]
         x[15] : Splice seam offset deviation [mm]
    *)
    x                                   : ARRAY[0..15] OF REAL;      (* Current discrete state vector *)
    x_prev                              : ARRAY[0..15] OF REAL;      (* Previous discrete state vector *)
    x_hat                               : ARRAY[0..15] OF REAL;      (* Observer estimated state vector *)
    x_pred                              : ARRAY[0..15] OF REAL;      (* One-step state prediction vector *)
    x_ref                               : ARRAY[0..15] OF REAL;      (* Dynamic reference trajectory vector *)

    (* Control Input Vector u[0..7]:
         u[0] : Drum 1 motor torque command [Nm]
         u[1] : Drum 2 motor torque command [Nm]
         u[2] : Shaping bladder proportional air mass flow valve [slpm]
         u[3] : Bead slide ballscrew velocity command [mm/s]
         u[4] : LH Stitcher radial force servo command [N]
         u[5] : RH Stitcher radial force servo command [N]
         u[6] : Transfer ring axial velocity command [mm/s]
         u[7] : Servicer festoon dancer tension trim command [Nm]
    *)
    u                                   : ARRAY[0..7] OF REAL;       (* Current control input vector *)
    u_mpc                               : ARRAY[0..7] OF REAL;       (* MPC optimized control vector *)
    u_prev                              : ARRAY[0..7] OF REAL;       (* Previous cycle control input vector *)
    y                                   : ARRAY[0..15] OF REAL;      (* Output measurement vector *)

    (* Discrete State Transition Matrix A (16x16), Input Matrix B (16x8), Output C (16x16), Feedthrough D (16x8) *)
    matA                                : ARRAY[0..15, 0..15] OF REAL;
    matB                                : ARRAY[0..15, 0..7] OF REAL;
    matC                                : ARRAY[0..15, 0..15] OF REAL;
    matD                                : ARRAY[0..15, 0..7] OF REAL;

    (* MPC Quadratic Cost Functional Weights *)
    Q_diag                              : ARRAY[0..15] OF REAL;      (* State tracking error penalty weights *)
    R_diag                              : ARRAY[0..7] OF REAL;       (* Control actuator effort penalty weights *)
    P_diag                              : ARRAY[0..15] OF REAL;      (* Terminal state error penalty weights *)

    (* Receding-Horizon Prediction Matrices (5-step lookahead) *)
    x_horizon                           : ARRAY[0..4, 0..15] OF REAL;
    u_horizon                           : ARRAY[0..4, 0..7] OF REAL;
    delta_u                             : ARRAY[0..7] OF REAL;
    grad_J                              : ARRAY[0..7] OF REAL;
    bModelInitialized                   : BOOL := FALSE;

    (* ====================================================================================================== *)
    (* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSING STRUCTURES                                    *)
    (* ====================================================================================================== *)
    (* Bank 1: Drum 1 Optical Resolvers *)
    rVoted_Drum1_Angle_deg              : REAL;
    rVoted_Drum1_Speed_rpm              : REAL;
    rDiff_D1_AB                         : REAL;
    rDiff_D1_BC                         : REAL;
    rDiff_D1_CA                         : REAL;
    bDrum1_Resolver_Discrepancy         : BOOL;
    tDrum1_Resolver_Timer               : TON;
    iDrum1_TMR_HealthState              : INT := 3;   (* 3=Healthy 3-ch, 2=Degraded 1oo2, 0=Fault *)

    (* Bank 2: Carcass Shaping Air Pressure Transducers *)
    rVoted_ShapingPressure_bar          : REAL;
    rDiff_Press_AB                      : REAL;
    rDiff_Press_BC                      : REAL;
    rDiff_Press_CA                      : REAL;
    bShapingPress_Discrepancy           : BOOL;
    tShapingPress_Timer                 : TON;
    iShapingPress_TMR_HealthState       : INT := 3;

    (* Bank 3: In-Line 3D Blue-Laser Splice Overlap Sensors *)
    rVoted_SpliceOverlap_mm             : REAL;
    rDiff_Splice_AB                     : REAL;
    rDiff_Splice_BC                     : REAL;
    rDiff_Splice_CA                     : REAL;
    bSplice_Discrepancy                 : BOOL;
    tSplice_Timer                       : TON;
    iSplice_TMR_HealthState             : INT := 3;

    (* Bank 4: Twin Stitcher Piezoelectric Load Cells *)
    rVoted_StitcherForce_LH_N           : REAL;
    rVoted_StitcherForce_RH_N           : REAL;
    rDiff_StitcherLH_AB                 : REAL;
    rDiff_StitcherLH_BC                 : REAL;
    rDiff_StitcherLH_CA                 : REAL;
    rDiff_StitcherRH_AB                 : REAL;
    rDiff_StitcherRH_BC                 : REAL;
    rDiff_StitcherRH_CA                 : REAL;
    bStitcher_Discrepancy               : BOOL;
    tStitcher_Timer                     : TON;
    iStitcher_TMR_HealthState           : INT := 3;

    (* ====================================================================================================== *)
    (* SECTION 3: IN-LINE LASER TRIANGULATION & CIRCUMFERENTIAL METROLOGY                                    *)
    (* ====================================================================================================== *)
    rLaser_ScanBuffer                   : ARRAY[0..35] OF REAL;      (* 36 measurement points every 10 deg *)
    iLaser_BufferIdx                    : INT := 0;
    rCalculated_Runout_Radial_mm        : REAL := 0.0;
    rCalculated_Runout_Lateral_mm       : REAL := 0.0;
    rCalculated_Harmonic_1H_mm          : REAL := 0.0;
    rCalculated_Harmonic_2H_mm          : REAL := 0.0;
    rSumFourierCos1                     : REAL := 0.0;
    rSumFourierSin1                     : REAL := 0.0;
    rSumFourierCos2                     : REAL := 0.0;
    rSumFourierSin2                     : REAL := 0.0;
    bSpliceOverlap_InRange              : BOOL := FALSE;
    bSpliceThickness_InRange            : BOOL := FALSE;
    bDogEar_Defect_Detected             : BOOL := FALSE;

    (* ====================================================================================================== *)
    (* SECTION 4: VISCOELASTIC RUBBER RELAXATION & TOROIDAL SHAPING DYNAMICS                                  *)
    (* ====================================================================================================== *)
    rToroidalCarcassRadius_mm           : REAL := 210.0;
    rToroidalCarcassVolume_dm3          : REAL := 12.5;
    rTargetToroidalRadius_mm            : REAL := 345.0;
    rBeadSpacingCurrent_mm              : REAL := 380.0;
    rBeadSlideSymmetricTarget_mm        : REAL := 185.0;
    rShapingPressure_PID_P              : REAL := 1.45;
    rShapingPressure_PID_I              : REAL := 0.52;
    rShapingPressure_PID_D              : REAL := 0.06;
    rShapingPressure_Integral           : REAL := 0.0;
    rShapingPressure_PrevErr            : REAL := 0.0;
    rShapingAirMassFlow_slpm            : REAL := 0.0;
    rRubberStrainRate                   : REAL := 0.0;
    rRubberViscoRelaxation_kPa          : REAL := 0.0;

    (* ====================================================================================================== *)
    (* SECTION 5: TWIN ROBOTIC STITCHER PROFILE CONTROL                                                      *)
    (* ====================================================================================================== *)
    rStitcherProgress_pct               : REAL := 0.0;
    rStitcherTargetForce_N              : REAL := 0.0;
    rStitcherForcePID_P                 : REAL := 0.95;
    rStitcherForcePID_I                 : REAL := 0.42;
    rStitcherForcePID_D                 : REAL := 0.04;
    rStitcherForce_Integral_LH          : REAL := 0.0;
    rStitcherForce_Integral_RH          : REAL := 0.0;
    rStitcherForce_PrevErr_LH           : REAL := 0.0;
    rStitcherForce_PrevErr_RH           : REAL := 0.0;

    (* ====================================================================================================== *)
    (* SECTION 6: HIGH-SPEED SERVICER FESTOON DANCER CONTROL                                                 *)
    (* ====================================================================================================== *)
    rDancer_PID_P                       : REAL := 2.10;
    rDancer_PID_I                       : REAL := 0.85;
    rDancer_InnerLiner_Integral         : REAL := 0.0;
    rDancer_Tread_Integral              : REAL := 0.0;

    (* ====================================================================================================== *)
    (* SECTION 7: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) VARIABLES                                  *)
    (* ====================================================================================================== *)
    iFSM_State                          : INT := 0;   (* 0=IDLE, 1..12=STAGES, 99=FAULT *)
    iFSM_PrevState                      : INT := 0;
    rStageTimer_s                       : REAL := 0.0;
    rStepTimer_s                        : REAL := 0.0;
    rTotalCycleTimer_s                  : REAL := 0.0;
    iSubStep                            : INT := 0;
    bStageInitDone                      : BOOL := FALSE;
    tStateTimeout                       : TON;

    (* ====================================================================================================== *)
    (* SECTION 8: ISA-18.2 ALARMS, LIMITS, HYSTERESIS & TELEMETRY                                            *)
    (* ====================================================================================================== *)
    bAlarm_SpliceOverlap_HH             : BOOL := FALSE;
    bAlarm_SpliceOverlap_LL             : BOOL := FALSE;
    bAlarm_ShapingPressure_HH           : BOOL := FALSE;
    bAlarm_ShapingPressure_H            : BOOL := FALSE;
    bAlarm_ShapingPressure_L            : BOOL := FALSE;
    bAlarm_ShapingPressure_LL           : BOOL := FALSE;
    bAlarm_TransferRingRunout_HH        : BOOL := FALSE;
    bAlarm_StitcherForce_HH             : BOOL := FALSE;
    bAlarm_StitcherForce_LL             : BOOL := FALSE;
    bAlarm_FestoonTension_HH            : BOOL := FALSE;
    bAlarm_FestoonTension_LL            : BOOL := FALSE;
    bAlarm_TMR_BankFailure              : BOOL := FALSE;

    (* Constants for Physics, Geometry, and Calibration Limits *)
    c_rSampleTime_s                     : REAL := 0.010;  (* 10 ms deterministic scan time *)
    c_rPi                               : REAL := 3.141592653589793;
    c_rDrum1_NominalOD_mm               : REAL := 420.0;
    c_rDrum2_NominalOD_mm               : REAL := 640.0;
    c_rDrum1_CenterAxialPos_mm          : REAL := 1250.0;
    c_rDrum2_CenterAxialPos_mm          : REAL := 250.0;
    c_rSpliceOverlap_Nominal_mm         : REAL := 2.5;
    c_rSpliceOverlap_Tol_mm             : REAL := 1.0;
    c_rSpliceOverlap_HH_mm              : REAL := 4.5;
    c_rSpliceOverlap_LL_mm              : REAL := 1.0;
    c_rDogEar_Max_mm                    : REAL := 0.8;
    c_rPressure_HH_bar                  : REAL := 2.70;
    c_rPressure_H_bar                   : REAL := 2.40;
    c_rPressure_L_bar                   : REAL := 0.60;
    c_rPressure_LL_bar                  : REAL := 0.35;
    c_rTransferRingConcentricityTol_mm  : REAL := 0.10;
    c_rTransferRingRunout_HH_mm         : REAL := 0.25;
    c_rStitcherForce_HH_N               : REAL := 2600.0;
    c_rStitcherForce_LL_N               : REAL := 400.0;
    c_rFestoonTension_HH_N              : REAL := 180.0;
    c_rFestoonTension_LL_N              : REAL := 20.0;
    c_rHysteresis_bar                   : REAL := 0.05;
    c_rHysteresis_mm                    : REAL := 0.15;
    c_rHysteresis_N                     : REAL := 30.0;

    (* Iteration & Matrix Indices *)
    iRow                                : INT := 0;
    iCol                                : INT := 0;
    kStep                               : INT := 0;
    iScan                               : INT := 0;
    iInput                              : INT := 0;
END_VAR
""")

    # ----------------------------------------------------------------------------------------------------------
    # EXECUTION BODY: INITIALIZATION & SAFETY INTERLOCKS
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* MAIN EXECUTION BODY: CYBER-PHYSICAL ADVANCED TIRE MANUFACTURING CONTROL (CYCLE TIME Ts = 10 ms)             *)
(* ========================================================================================================== *)

(* --- STEP 0: HARDWARE SAFETY CHAIN, PERIMETER SCANNER & WATCHDOG EVALUATION --- *)
IF NOT bEmergencyStop_CircuitOK OR NOT bSafetyScannerClear THEN
    bSystemReady := FALSE;
    bCycleInProgress := FALSE;
    bEmergencyHalted := TRUE;
    bGeneralFault := TRUE;
    
    (* Force emergency collapse and instant bladder depressurization *)
    rDrum1_SpeedCmd_rpm := 0.0;
    rDrum2_SpeedCmd_rpm := 0.0;
    rDrum1_TorqueLimit_Nm := 0.0;
    rDrum2_TorqueLimit_Nm := 0.0;
    rShapingPressure_Cmd_bar := 0.0;
    bShapingAir_InflateValve := FALSE;
    bShapingAir_ExhaustValve := TRUE; (* Dump air instantly through rapid exhaust *)
    bTurnUpBladder_LH_Cmd := FALSE;
    bTurnUpBladder_RH_Cmd := FALSE;
    rBeadSlide_LH_SpeedCmd_mms := 0.0;
    rBeadSlide_RH_SpeedCmd_mms := 0.0;
    bBeadLock_ClampCmd := FALSE;
    rTransferRing_AxialSpeedCmd_mms := 0.0;
    bTransferRing_VacuumCmd := FALSE;
    rStitcher_LH_ForceCmd_N := 0.0;
    rStitcher_RH_ForceCmd_N := 0.0;
    rStitcher_LH_AxialVelCmd_mms := 0.0;
    rStitcher_RH_AxialVelCmd_mms := 0.0;
    rServicer_InnerLiner_SpeedCmd_mms := 0.0;
    rServicer_Tread_SpeedCmd_mms := 0.0;
    rCapPly_Winder_TensionCmd_N := 0.0;
    bUltrasonicCutter_Trigger := FALSE;
    
    iFSM_State := 12; (* Jump immediately to Stage 12: Emergency Deflate & Collapse *)
    iCurrentStage := 12;
    dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#80000000; (* Safety chain tripped *)
    RETURN;
END_IF;

(* Reset Emergency Halted bit if safety circuit is sound *)
bEmergencyHalted := FALSE;

(* --- ONE-TIME MODEL MATRICES INITIALIZATION --- *)
IF NOT bModelInitialized THEN
    (* Zero all elements of matrices matA, matB, matC, matD *)
    FOR iRow := 0 TO 15 DO
        FOR iCol := 0 TO 15 DO
            matA[iRow, iCol] := 0.0;
            matC[iRow, iCol] := 0.0;
        END_FOR;
        FOR iCol := 0 TO 7 DO
            matB[iRow, iCol] := 0.0;
            matD[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------------ *)
    (* Discrete State Transition Matrix A (16x16) Coupling Parameters (Ts = 0.010 s)                          *)
    (* ------------------------------------------------------------------------------------------------------ *)
    (* Row 0: Drum 1 Angular Speed Dynamics (Spindle Inertia & Viscous Friction) *)
    matA[0, 0] := 0.9820;  (* Spindle momentum retention *)
    matA[0, 8] := -0.0035; (* Rubber carcass rotational drag torque coupling *)
    matA[0, 9] := -0.0018; (* Stitcher LH contact friction braking torque *)
    matA[0, 10] := -0.0018;(* Stitcher RH contact friction braking torque *)

    (* Row 1: Drum 1 Angular Position Integration *)
    matA[1, 0] := 0.0100;  (* theta_D1[k+1] = theta_D1[k] + Ts * omega_D1[k] *)
    matA[1, 1] := 1.0000;

    (* Row 2: Drum 2 Angular Speed Dynamics *)
    matA[2, 2] := 0.9840;  (* Belt drum momentum retention *)
    matA[2, 14] := -0.0022;(* Festoon web tension reaction torque *)

    (* Row 3: Drum 2 Angular Position Integration *)
    matA[3, 2] := 0.0100;  (* theta_D2[k+1] = theta_D2[k] + Ts * omega_D2[k] *)
    matA[3, 3] := 1.0000;

    (* Row 4: Carcass Shaping Bladder Internal Air Pressure Dynamics *)
    matA[4, 4] := 0.9650;  (* Bladder pneumatic capacitance and natural seal leakage *)
    matA[4, 5] := -0.0420; (* Polytropic expansion pressure drop dP/dV *)
    matA[4, 6] := 0.0180;  (* LH Bead inward motion compression effect *)
    matA[4, 7] := 0.0180;  (* RH Bead inward motion compression effect *)

    (* Row 5: Carcass Shaping Bladder Volume Dynamics *)
    matA[5, 5] := 0.9880;  (* Viscoelastic bladder expansion compliance *)
    matA[5, 4] := 0.0520;  (* Internal pressure driven volume expansion rate *)
    matA[5, 8] := -0.0150; (* Rubber carcass carcass cord tension constraining expansion *)

    (* Row 6: LH Bead Slide Linear Position Dynamics *)
    matA[6, 6] := 0.9920;  (* Ballscrew friction and lead nut positioning *)
    matA[6, 4] := -0.0045; (* Reaction thrust force from internal shaping pressure *)

    (* Row 7: RH Bead Slide Linear Position Dynamics *)
    matA[7, 7] := 0.9920;  (* Ballscrew friction and lead nut positioning *)
    matA[7, 4] := -0.0045; (* Reaction thrust force from internal shaping pressure *)

    (* Row 8: Maxwell-Wiechert Viscoelastic Rubber Stress Relaxation *)
    matA[8, 8] := 0.8950;  (* exp(-Ts / tau_relax) where tau_relax = 0.091 s *)
    matA[8, 4] := 0.1250;  (* Elastic stress generation from bladder pressure *)
    matA[8, 13] := 0.0850; (* Tangential cord elongation hoop stress *)

    (* Row 9: LH Stitcher Roller Radial Contact Force Dynamics *)
    matA[9, 9] := 0.9120;  (* Stitcher pneumatic/servo compliance *)
    matA[9, 4] := 0.0380;  (* Carcass internal pressure pushback *)
    matA[9, 8] := 0.0240;  (* Rubber carcass surface stiffness variation *)

    (* Row 10: RH Stitcher Roller Radial Contact Force Dynamics *)
    matA[10, 10] := 0.9120;(* Stitcher pneumatic/servo compliance *)
    matA[10, 4] := 0.0380; (* Carcass internal pressure pushback *)
    matA[10, 8] := 0.0240; (* Rubber carcass surface stiffness variation *)

    (* Row 11: Transfer Ring Gantry Axial Position Dynamics *)
    matA[11, 11] := 0.9950;(* Gantry servo track carriage inertia *)

    (* Row 12: Transfer Ring Segment Radial Gripper Diameter *)
    matA[12, 12] := 0.9900;(* Segmented gripper linkage compliance *)

    (* Row 13: Carcass Crown Outer Diameter Dynamics *)
    matA[13, 13] := 0.9780;(* Elastic cord elongation retention *)
    matA[13, 4] := 0.0650; (* Shaping pressure crown diametral expansion gain *)
    matA[13, 6] := 0.0350; (* Bead slide convergence geometric bulging *)
    matA[13, 7] := 0.0350; (* Bead slide convergence geometric bulging *)

    (* Row 14: Servicer Festoon Web Tension Dynamics *)
    matA[14, 14] := 0.9250;(* Festoon elastomeric web damping *)
    matA[14, 0] := 0.0480; (* Drum 1 payout draw rate *)
    matA[14, 2] := 0.0480; (* Drum 2 payout draw rate *)

    (* Row 15: Splice Seam Offset Deviation Kinematics *)
    matA[15, 15] := 0.9980;(* Cumulative splice tracking error *)
    matA[15, 0] := 0.0012; (* High-speed centrifugal ply centrifugal drift *)

    (* ------------------------------------------------------------------------------------------------------ *)
    (* Input Coupling Matrix B (16x8) Parameters                                                             *)
    (* ------------------------------------------------------------------------------------------------------ *)
    matB[0, 0] := 0.0850;  (* Drum 1 Torque u[0] -> Drum 1 Speed *)
    matB[1, 0] := 0.0004;  (* Drum 1 Torque u[0] -> Drum 1 Angle *)
    matB[2, 1] := 0.0780;  (* Drum 2 Torque u[1] -> Drum 2 Speed *)
    matB[3, 1] := 0.0004;  (* Drum 2 Torque u[1] -> Drum 2 Angle *)
    matB[4, 2] := 0.0620;  (* Shaping Air Valve u[2] -> Bladder Pressure *)
    matB[5, 2] := 0.0150;  (* Shaping Air Valve u[2] -> Bladder Volume *)
    matB[6, 3] := 0.0100;  (* Bead Slide Vel u[3] -> LH Bead Slide Pos *)
    matB[7, 3] := -0.0100; (* Bead Slide Vel u[3] -> RH Bead Slide Pos (Symmetric) *)
    matB[8, 2] := 0.0085;  (* Shaping Air Valve u[2] -> Rubber Stress *)
    matB[9, 4] := 0.0920;  (* LH Stitcher Force Cmd u[4] -> LH Force *)
    matB[10, 5] := 0.0920; (* RH Stitcher Force Cmd u[5] -> RH Force *)
    matB[11, 6] := 0.0100; (* Transfer Ring Vel u[6] -> Transfer Ring Pos *)
    matB[12, 6] := 0.0025; (* Transfer Ring Vel u[6] -> Gripper Segment Diam *)
    matB[13, 2] := 0.0045; (* Shaping Air Valve u[2] -> Crown OD *)
    matB[13, 3] := 0.0080; (* Bead Slide Vel u[3] -> Crown OD Bulging *)
    matB[14, 7] := 0.0750; (* Festoon Trim u[7] -> Web Tension *)
    matB[15, 0] := 0.0008; (* Drum 1 Torque u[0] -> Splice Skew *)

    (* ------------------------------------------------------------------------------------------------------ *)
    (* Output Measurement Matrix C (16x16) - Direct State Identity Sensing                                   *)
    (* ------------------------------------------------------------------------------------------------------ *)
    FOR iRow := 0 TO 15 DO
        matC[iRow, iRow] := 1.0000;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------------ *)
    (* MPC Quadratic Cost Functional Weights                                                                 *)
    (* ------------------------------------------------------------------------------------------------------ *)
    Q_diag[0] := 1.20;   (* Drum 1 Speed error penalty *)
    Q_diag[1] := 2.50;   (* Drum 1 Angular position error penalty *)
    Q_diag[2] := 1.20;   (* Drum 2 Speed error penalty *)
    Q_diag[3] := 2.50;   (* Drum 2 Angular position error penalty *)
    Q_diag[4] := 15.00;  (* Shaping bladder pressure critical penalty *)
    Q_diag[5] := 5.00;   (* Bladder volume penalty *)
    Q_diag[6] := 8.00;   (* LH Bead slide position penalty *)
    Q_diag[7] := 8.00;   (* RH Bead slide position penalty *)
    Q_diag[8] := 0.80;   (* Viscoelastic rubber stress penalty *)
    Q_diag[9] := 12.00;  (* LH Stitcher contact force critical penalty *)
    Q_diag[10] := 12.00; (* RH Stitcher contact force critical penalty *)
    Q_diag[11] := 18.00; (* Transfer ring axial coaxial positioning critical penalty *)
    Q_diag[12] := 14.00; (* Transfer ring segmented gripper diameter critical penalty *)
    Q_diag[13] := 20.00; (* Green tire target crown OD critical penalty *)
    Q_diag[14] := 4.50;  (* Servicer web tension penalty *)
    Q_diag[15] := 16.00; (* Splice overlap offset alignment penalty *)

    R_diag[0] := 0.08;   (* Drum 1 torque actuator penalty *)
    R_diag[1] := 0.08;   (* Drum 2 torque actuator penalty *)
    R_diag[2] := 0.15;   (* Shaping air proportional valve effort penalty *)
    R_diag[3] := 0.25;   (* Bead slide servo velocity rate penalty *)
    R_diag[4] := 0.12;   (* LH Stitcher force actuator penalty *)
    R_diag[5] := 0.12;   (* RH Stitcher force actuator penalty *)
    R_diag[6] := 0.35;   (* Transfer ring gantry velocity rate penalty *)
    R_diag[7] := 0.18;   (* Servicer festoon dancer trim actuator penalty *)

    FOR iRow := 0 TO 15 DO
        P_diag[iRow] := Q_diag[iRow] * 2.50; (* Terminal cost weighting matrix *)
    END_FOR;

    bModelInitialized := TRUE;
END_IF;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 1: 2oo3 TMR SENSOR VOTING
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH BUMPLESS DEGRADATION                     *)
(* ========================================================================================================== *)

(* --- Bank 1: Drum 1 Optical Resolvers (Angle & Speed) --- *)
rDiff_D1_AB := ABS(rDrum1_ResolverAngle_deg_ChA - rDrum1_ResolverAngle_deg_ChB);
rDiff_D1_BC := ABS(rDrum1_ResolverAngle_deg_ChB - rDrum1_ResolverAngle_deg_ChC);
rDiff_D1_CA := ABS(rDrum1_ResolverAngle_deg_ChC - rDrum1_ResolverAngle_deg_ChA);

(* Resolver discrepancy threshold: 0.25 deg *)
IF (rDiff_D1_AB <= 0.25) AND (rDiff_D1_BC <= 0.25) AND (rDiff_D1_CA <= 0.25) THEN
    (* All 3 channels agree: True Median Selection *)
    IF (rDrum1_ResolverAngle_deg_ChA >= rDrum1_ResolverAngle_deg_ChB AND rDrum1_ResolverAngle_deg_ChA <= rDrum1_ResolverAngle_deg_ChC) OR
       (rDrum1_ResolverAngle_deg_ChA <= rDrum1_ResolverAngle_deg_ChB AND rDrum1_ResolverAngle_deg_ChA >= rDrum1_ResolverAngle_deg_ChC) THEN
        rVoted_Drum1_Angle_deg := rDrum1_ResolverAngle_deg_ChA;
        rVoted_Drum1_Speed_rpm := rDrum1_Speed_rpm_ChA;
    ELSIF (rDrum1_ResolverAngle_deg_ChB >= rDrum1_ResolverAngle_deg_ChA AND rDrum1_ResolverAngle_deg_ChB <= rDrum1_ResolverAngle_deg_ChC) OR
          (rDrum1_ResolverAngle_deg_ChB <= rDrum1_ResolverAngle_deg_ChA AND rDrum1_ResolverAngle_deg_ChB >= rDrum1_ResolverAngle_deg_ChC) THEN
        rVoted_Drum1_Angle_deg := rDrum1_ResolverAngle_deg_ChB;
        rVoted_Drum1_Speed_rpm := rDrum1_Speed_rpm_ChB;
    ELSE
        rVoted_Drum1_Angle_deg := rDrum1_ResolverAngle_deg_ChC;
        rVoted_Drum1_Speed_rpm := rDrum1_Speed_rpm_ChC;
    END_IF;
    bDrum1_Resolver_Discrepancy := FALSE;
    iDrum1_TMR_HealthState := 3;
ELSIF (rDiff_D1_AB <= 0.25) THEN
    (* ChA and ChB agree, ChC is deviant: Bumpless degradation to 1oo2 average *)
    rVoted_Drum1_Angle_deg := (rDrum1_ResolverAngle_deg_ChA + rDrum1_ResolverAngle_deg_ChB) * 0.5;
    rVoted_Drum1_Speed_rpm := (rDrum1_Speed_rpm_ChA + rDrum1_Speed_rpm_ChB) * 0.5;
    bDrum1_Resolver_Discrepancy := TRUE;
    iDrum1_TMR_HealthState := 2;
ELSIF (rDiff_D1_BC <= 0.25) THEN
    (* ChB and ChC agree, ChA is deviant *)
    rVoted_Drum1_Angle_deg := (rDrum1_ResolverAngle_deg_ChB + rDrum1_ResolverAngle_deg_ChC) * 0.5;
    rVoted_Drum1_Speed_rpm := (rDrum1_Speed_rpm_ChB + rDrum1_Speed_rpm_ChC) * 0.5;
    bDrum1_Resolver_Discrepancy := TRUE;
    iDrum1_TMR_HealthState := 2;
ELSIF (rDiff_D1_CA <= 0.25) THEN
    (* ChC and ChA agree, ChB is deviant *)
    rVoted_Drum1_Angle_deg := (rDrum1_ResolverAngle_deg_ChC + rDrum1_ResolverAngle_deg_ChA) * 0.5;
    rVoted_Drum1_Speed_rpm := (rDrum1_Speed_rpm_ChC + rDrum1_Speed_rpm_ChA) * 0.5;
    bDrum1_Resolver_Discrepancy := TRUE;
    iDrum1_TMR_HealthState := 2;
ELSE
    (* Total TMR Failure across Drum 1 Resolvers *)
    bDrum1_Resolver_Discrepancy := TRUE;
    iDrum1_TMR_HealthState := 0;
END_IF;

tDrum1_Resolver_Timer(IN := bDrum1_Resolver_Discrepancy, PT := T#150MS);
IF tDrum1_Resolver_Timer.Q AND (iDrum1_TMR_HealthState = 0) THEN
    bAlarm_TMR_BankFailure := TRUE;
    bGeneralFault := TRUE;
    dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000001; (* Resolver TMR Trip *)
END_IF;

(* --- Bank 2: Carcass Shaping Air Pressure Transducers --- *)
rDiff_Press_AB := ABS(rShapingPressure_bar_ChA - rShapingPressure_bar_ChB);
rDiff_Press_BC := ABS(rShapingPressure_bar_ChB - rShapingPressure_bar_ChC);
rDiff_Press_CA := ABS(rShapingPressure_bar_ChC - rShapingPressure_bar_ChA);

(* Shaping pressure discrepancy threshold: 0.08 bar *)
IF (rDiff_Press_AB <= 0.08) AND (rDiff_Press_BC <= 0.08) AND (rDiff_Press_CA <= 0.08) THEN
    (* 3-Channel Median *)
    IF (rShapingPressure_bar_ChA >= rShapingPressure_bar_ChB AND rShapingPressure_bar_ChA <= rShapingPressure_bar_ChC) OR
       (rShapingPressure_bar_ChA <= rShapingPressure_bar_ChB AND rShapingPressure_bar_ChA >= rShapingPressure_bar_ChC) THEN
        rVoted_ShapingPressure_bar := rShapingPressure_bar_ChA;
    ELSIF (rShapingPressure_bar_ChB >= rShapingPressure_bar_ChA AND rShapingPressure_bar_ChB <= rShapingPressure_bar_ChC) OR
          (rShapingPressure_bar_ChB <= rShapingPressure_bar_ChA AND rShapingPressure_bar_ChB >= rShapingPressure_bar_ChC) THEN
        rVoted_ShapingPressure_bar := rShapingPressure_bar_ChB;
    ELSE
        rVoted_ShapingPressure_bar := rShapingPressure_bar_ChC;
    END_IF;
    bShapingPress_Discrepancy := FALSE;
    iShapingPress_TMR_HealthState := 3;
ELSIF (rDiff_Press_AB <= 0.08) THEN
    rVoted_ShapingPressure_bar := (rShapingPressure_bar_ChA + rShapingPressure_bar_ChB) * 0.5;
    bShapingPress_Discrepancy := TRUE;
    iShapingPress_TMR_HealthState := 2;
ELSIF (rDiff_Press_BC <= 0.08) THEN
    rVoted_ShapingPressure_bar := (rShapingPressure_bar_ChB + rShapingPressure_bar_ChC) * 0.5;
    bShapingPress_Discrepancy := TRUE;
    iShapingPress_TMR_HealthState := 2;
ELSIF (rDiff_Press_CA <= 0.08) THEN
    rVoted_ShapingPressure_bar := (rShapingPressure_bar_ChC + rShapingPressure_bar_ChA) * 0.5;
    bShapingPress_Discrepancy := TRUE;
    iShapingPress_TMR_HealthState := 2;
ELSE
    bShapingPress_Discrepancy := TRUE;
    iShapingPress_TMR_HealthState := 0;
END_IF;

tShapingPress_Timer(IN := bShapingPress_Discrepancy, PT := T#150MS);
IF tShapingPress_Timer.Q AND (iShapingPress_TMR_HealthState = 0) THEN
    bAlarm_TMR_BankFailure := TRUE;
    bGeneralFault := TRUE;
    dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000002; (* Pressure TMR Trip *)
END_IF;

(* --- Bank 3: In-Line 3D Blue-Laser Splice Overlap Sensors --- *)
rDiff_Splice_AB := ABS(rLaser_SpliceOverlap_mm_ChA - rLaser_SpliceOverlap_mm_ChB);
rDiff_Splice_BC := ABS(rLaser_SpliceOverlap_mm_ChB - rLaser_SpliceOverlap_mm_ChC);
rDiff_Splice_CA := ABS(rLaser_SpliceOverlap_mm_ChC - rLaser_SpliceOverlap_mm_ChA);

(* Splice overlap discrepancy threshold: 0.20 mm *)
IF (rDiff_Splice_AB <= 0.20) AND (rDiff_Splice_BC <= 0.20) AND (rDiff_Splice_CA <= 0.20) THEN
    IF (rLaser_SpliceOverlap_mm_ChA >= rLaser_SpliceOverlap_mm_ChB AND rLaser_SpliceOverlap_mm_ChA <= rLaser_SpliceOverlap_mm_ChC) OR
       (rLaser_SpliceOverlap_mm_ChA <= rLaser_SpliceOverlap_mm_ChB AND rLaser_SpliceOverlap_mm_ChA >= rLaser_SpliceOverlap_mm_ChC) THEN
        rVoted_SpliceOverlap_mm := rLaser_SpliceOverlap_mm_ChA;
    ELSIF (rLaser_SpliceOverlap_mm_ChB >= rLaser_SpliceOverlap_mm_ChA AND rLaser_SpliceOverlap_mm_ChB <= rLaser_SpliceOverlap_mm_ChC) OR
          (rLaser_SpliceOverlap_mm_ChB <= rLaser_SpliceOverlap_mm_ChA AND rLaser_SpliceOverlap_mm_ChB >= rLaser_SpliceOverlap_mm_ChC) THEN
        rVoted_SpliceOverlap_mm := rLaser_SpliceOverlap_mm_ChB;
    ELSE
        rVoted_SpliceOverlap_mm := rLaser_SpliceOverlap_mm_ChC;
    END_IF;
    bSplice_Discrepancy := FALSE;
    iSplice_TMR_HealthState := 3;
ELSIF (rDiff_Splice_AB <= 0.20) THEN
    rVoted_SpliceOverlap_mm := (rLaser_SpliceOverlap_mm_ChA + rLaser_SpliceOverlap_mm_ChB) * 0.5;
    bSplice_Discrepancy := TRUE;
    iSplice_TMR_HealthState := 2;
ELSIF (rDiff_Splice_BC <= 0.20) THEN
    rVoted_SpliceOverlap_mm := (rLaser_SpliceOverlap_mm_ChB + rLaser_SpliceOverlap_mm_ChC) * 0.5;
    bSplice_Discrepancy := TRUE;
    iSplice_TMR_HealthState := 2;
ELSIF (rDiff_Splice_CA <= 0.20) THEN
    rVoted_SpliceOverlap_mm := (rLaser_SpliceOverlap_mm_ChC + rLaser_SpliceOverlap_mm_ChA) * 0.5;
    bSplice_Discrepancy := TRUE;
    iSplice_TMR_HealthState := 2;
ELSE
    bSplice_Discrepancy := TRUE;
    iSplice_TMR_HealthState := 0;
END_IF;

tSplice_Timer(IN := bSplice_Discrepancy, PT := T#200MS);
IF tSplice_Timer.Q AND (iSplice_TMR_HealthState = 0) THEN
    bAlarm_TMR_BankFailure := TRUE;
    dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000004; (* Splice Laser TMR Trip *)
END_IF;

(* --- Bank 4: Twin Stitcher Piezoelectric Load Cells (LH & RH) --- *)
rDiff_StitcherLH_AB := ABS(rStitcherForce_LH_N_ChA - rStitcherForce_LH_N_ChB);
rDiff_StitcherLH_BC := ABS(rStitcherForce_LH_N_ChB - rStitcherForce_LH_N_ChC);
rDiff_StitcherLH_CA := ABS(rStitcherForce_LH_N_ChC - rStitcherForce_LH_N_ChA);

(* Stitcher force discrepancy threshold: 50.0 N *)
IF (rDiff_StitcherLH_AB <= 50.0) AND (rDiff_StitcherLH_BC <= 50.0) AND (rDiff_StitcherLH_CA <= 50.0) THEN
    IF (rStitcherForce_LH_N_ChA >= rStitcherForce_LH_N_ChB AND rStitcherForce_LH_N_ChA <= rStitcherForce_LH_N_ChC) OR
       (rStitcherForce_LH_N_ChA <= rStitcherForce_LH_N_ChB AND rStitcherForce_LH_N_ChA >= rStitcherForce_LH_N_ChC) THEN
        rVoted_StitcherForce_LH_N := rStitcherForce_LH_N_ChA;
    ELSIF (rStitcherForce_LH_N_ChB >= rStitcherForce_LH_N_ChA AND rStitcherForce_LH_N_ChB <= rStitcherForce_LH_N_ChC) OR
          (rStitcherForce_LH_N_ChB <= rStitcherForce_LH_N_ChA AND rStitcherForce_LH_N_ChB >= rStitcherForce_LH_N_ChC) THEN
        rVoted_StitcherForce_LH_N := rStitcherForce_LH_N_ChB;
    ELSE
        rVoted_StitcherForce_LH_N := rStitcherForce_LH_N_ChC;
    END_IF;
    bStitcher_Discrepancy := FALSE;
    iStitcher_TMR_HealthState := 3;
ELSIF (rDiff_StitcherLH_AB <= 50.0) THEN
    rVoted_StitcherForce_LH_N := (rStitcherForce_LH_N_ChA + rStitcherForce_LH_N_ChB) * 0.5;
    bStitcher_Discrepancy := TRUE;
    iStitcher_TMR_HealthState := 2;
ELSIF (rDiff_StitcherLH_BC <= 50.0) THEN
    rVoted_StitcherForce_LH_N := (rStitcherForce_LH_N_ChB + rStitcherForce_LH_N_ChC) * 0.5;
    bStitcher_Discrepancy := TRUE;
    iStitcher_TMR_HealthState := 2;
ELSIF (rDiff_StitcherLH_CA <= 50.0) THEN
    rVoted_StitcherForce_LH_N := (rStitcherForce_LH_N_ChC + rStitcherForce_LH_N_ChA) * 0.5;
    bStitcher_Discrepancy := TRUE;
    iStitcher_TMR_HealthState := 2;
ELSE
    bStitcher_Discrepancy := TRUE;
    iStitcher_TMR_HealthState := 0;
END_IF;

(* Same 2oo3 logic for RH Stitcher Load Cell *)
rDiff_StitcherRH_AB := ABS(rStitcherForce_RH_N_ChA - rStitcherForce_RH_N_ChB);
rDiff_StitcherRH_BC := ABS(rStitcherForce_RH_N_ChB - rStitcherForce_RH_N_ChC);
rDiff_StitcherRH_CA := ABS(rStitcherForce_RH_N_ChC - rStitcherForce_RH_N_ChA);

IF (rDiff_StitcherRH_AB <= 50.0) AND (rDiff_StitcherRH_BC <= 50.0) AND (rDiff_StitcherRH_CA <= 50.0) THEN
    IF (rStitcherForce_RH_N_ChA >= rStitcherForce_RH_N_ChB AND rStitcherForce_RH_N_ChA <= rStitcherForce_RH_N_ChC) OR
       (rStitcherForce_RH_N_ChA <= rStitcherForce_RH_N_ChB AND rStitcherForce_RH_N_ChA >= rStitcherForce_RH_N_ChC) THEN
        rVoted_StitcherForce_RH_N := rStitcherForce_RH_N_ChA;
    ELSIF (rStitcherForce_RH_N_ChB >= rStitcherForce_RH_N_ChA AND rStitcherForce_RH_N_ChB <= rStitcherForce_RH_N_ChC) OR
          (rStitcherForce_RH_N_ChB <= rStitcherForce_RH_N_ChA AND rStitcherForce_RH_N_ChB >= rStitcherForce_RH_N_ChC) THEN
        rVoted_StitcherForce_RH_N := rStitcherForce_RH_N_ChB;
    ELSE
        rVoted_StitcherForce_RH_N := rStitcherForce_RH_N_ChC;
    END_IF;
ELSIF (rDiff_StitcherRH_AB <= 50.0) THEN
    rVoted_StitcherForce_RH_N := (rStitcherForce_RH_N_ChA + rStitcherForce_RH_N_ChB) * 0.5;
ELSIF (rDiff_StitcherRH_BC <= 50.0) THEN
    rVoted_StitcherForce_RH_N := (rStitcherForce_RH_N_ChB + rStitcherForce_RH_N_ChC) * 0.5;
ELSIF (rDiff_StitcherRH_CA <= 50.0) THEN
    rVoted_StitcherForce_RH_N := (rStitcherForce_RH_N_ChC + rStitcherForce_RH_N_ChA) * 0.5;
END_IF;

tStitcher_Timer(IN := bStitcher_Discrepancy, PT := T#200MS);
IF tStitcher_Timer.Q AND (iStitcher_TMR_HealthState = 0) THEN
    bAlarm_TMR_BankFailure := TRUE;
    dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000008; (* Stitcher Load Cell TMR Trip *)
END_IF;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 2: DISCRETE STATE-SPACE PROPAGATION
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 2: DISCRETE STATE-SPACE PROPAGATION & VISCOELASTIC COUPLED ESTIMATION                                *)
(* ========================================================================================================== *)

(* Populate Physical Measurements into State Vector x[k] *)
x[0] := (rVoted_Drum1_Speed_rpm * 2.0 * c_rPi) / 60.0; (* rad/s *)
x[1] := (rVoted_Drum1_Angle_deg * c_rPi) / 180.0;      (* rad *)
x[2] := (rDrum2_Speed_rpm * 2.0 * c_rPi) / 60.0;       (* rad/s *)
x[3] := (rDrum2_ResolverAngle_deg * c_rPi) / 180.0;     (* rad *)
x[4] := rVoted_ShapingPressure_bar;                    (* bar *)
x[5] := rToroidalCarcassVolume_dm3;                    (* dm3 *)
x[6] := rBeadSlide_LH_Pos_mm;                          (* mm *)
x[7] := rBeadSlide_RH_Pos_mm;                          (* mm *)
x[8] := rRubberViscoRelaxation_kPa;                    (* kPa *)
x[9] := rVoted_StitcherForce_LH_N;                     (* N *)
x[10] := rVoted_StitcherForce_RH_N;                    (* N *)
x[11] := rTransferRing_AxialPos_mm;                    (* mm *)
x[12] := rTransferRing_SegmentDiam_mm;                 (* mm *)
x[13] := rToroidalCarcassRadius_mm * 2.0;              (* mm *)
x[14] := rFestoonTension_InnerLiner_N;                 (* N *)
x[15] := rLaser_LateralOffset_mm;                      (* mm *)

(* Populate Actuator Control Vector u[k] *)
u[0] := rDrum1_TorqueLimit_Nm;
u[1] := rDrum2_TorqueLimit_Nm;
u[2] := rShapingAirMassFlow_slpm;
u[3] := rBeadSlide_LH_SpeedCmd_mms;
u[4] := rStitcher_LH_ForceCmd_N;
u[5] := rStitcher_RH_ForceCmd_N;
u[6] := rTransferRing_AxialSpeedCmd_mms;
u[7] := rCapPly_Winder_TensionCmd_N;

(* State Propagation Equation: x_pred[k+1] = A * x[k] + B * u[k] *)
FOR iRow := 0 TO 15 DO
    x_pred[iRow] := 0.0;
    FOR iCol := 0 TO 15 DO
        x_pred[iRow] := x_pred[iRow] + (matA[iRow, iCol] * x[iCol]);
    END_FOR;
    FOR iInput := 0 TO 7 DO
        x_pred[iRow] := x_pred[iRow] + (matB[iRow, iInput] * u[iInput]);
    END_FOR;
END_FOR;

(* Output Estimation Equation: y[k] = C * x[k] + D * u[k] *)
FOR iRow := 0 TO 15 DO
    y[iRow] := 0.0;
    FOR iCol := 0 TO 15 DO
        y[iRow] := y[iRow] + (matC[iRow, iCol] * x[iCol]);
    END_FOR;
    FOR iInput := 0 TO 7 DO
        y[iRow] := y[iRow] + (matD[iRow, iInput] * u[iInput]);
    END_FOR;
END_FOR;

(* --- Viscoelastic Maxwell-Wiechert Stress Relaxation Model --- *)
(* dSigma/dt = -Sigma / tau_relax + E_modulus * dEpsilon/dt *)
rRubberStrainRate := (x[13] - x_prev[13]) / (c_rDrum1_NominalOD_mm * c_rSampleTime_s);
rRubberViscoRelaxation_kPa := (rRubberViscoRelaxation_kPa * 0.8950) + (4.50 * rRubberStrainRate * c_rSampleTime_s * 1000.0);

(* --- Dynamic Toroidal Carcass Volume & Geometry Estimation --- *)
rBeadSpacingCurrent_mm := ABS(rBeadSlide_LH_Pos_mm - rBeadSlide_RH_Pos_mm);
IF rBeadSpacingCurrent_mm < 50.0 THEN
    rBeadSpacingCurrent_mm := 50.0; (* Prevent division by zero *)
END_IF;

(* Toroidal expansion volume: V = (Pi^2 / 4) * (R_crown - R_bead) * (R_crown + R_bead)^2 / 1000.0 *)
IF x[4] > 0.10 THEN
    rToroidalCarcassRadius_mm := (c_rDrum1_NominalOD_mm * 0.5) + (x[4] * 42.50) + ((rTargetBeadDistance_mm - rBeadSpacingCurrent_mm) * 0.45);
    IF rToroidalCarcassRadius_mm > (rTireTargetCrownOD_mm * 0.55) THEN
        rToroidalCarcassRadius_mm := rTireTargetCrownOD_mm * 0.55;
    END_IF;
    rToroidalCarcassVolume_dm3 := (c_rPi * c_rPi / 4.0) * (rToroidalCarcassRadius_mm - (c_rDrum1_NominalOD_mm * 0.5)) * 
                                  (rToroidalCarcassRadius_mm + (c_rDrum1_NominalOD_mm * 0.5)) * 
                                  (rToroidalCarcassRadius_mm + (c_rDrum1_NominalOD_mm * 0.5)) / 1000000.0;
ELSE
    rToroidalCarcassRadius_mm := c_rDrum1_NominalOD_mm * 0.5;
    rToroidalCarcassVolume_dm3 := 5.0;
END_IF;

(* Save previous state vector *)
FOR iRow := 0 TO 15 DO
    x_prev[iRow] := x[iRow];
END_FOR;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION                                     *)
(* ========================================================================================================== *)

(* Formulate Dynamic Target Reference Vector x_ref Based on Active FSM Stage *)
x_ref[0] := (rDrum1_SpeedCmd_rpm * 2.0 * c_rPi) / 60.0;
x_ref[1] := x[1]; (* Tracking continuous position *)
x_ref[2] := (rDrum2_SpeedCmd_rpm * 2.0 * c_rPi) / 60.0;
x_ref[3] := x[3];
x_ref[4] := rTargetShapingPressure_bar;
x_ref[5] := 18.5; (* Nominal shaping volume [dm3] *)
x_ref[6] := rBeadSlideSymmetricTarget_mm;
x_ref[7] := -rBeadSlideSymmetricTarget_mm;
x_ref[8] := 0.0;  (* Minimize residual elastomeric stress *)
x_ref[9] := rStitcherTargetForce_N;
x_ref[10] := rStitcherTargetForce_N;
x_ref[11] := rTransferRing_TargetAxialPos_mm;
x_ref[12] := rTransferRing_SegmentDiamCmd_mm;
x_ref[13] := rTireTargetCrownOD_mm;
x_ref[14] := 75.0; (* 75 N nominal web tension *)
x_ref[15] := 0.0;  (* Zero splice lateral runout *)

(* Initialize 5-Step Horizon Simulation *)
FOR iRow := 0 TO 15 DO
    x_horizon[0, iRow] := x_pred[iRow];
END_FOR;
FOR iInput := 0 TO 7 DO
    u_horizon[0, iInput] := u[iInput];
END_FOR;

(* Unrolled 5-Step Lookahead Prediction Loop *)
FOR kStep := 0 TO 3 DO
    FOR iRow := 0 TO 15 DO
        x_horizon[kStep + 1, iRow] := 0.0;
        FOR iCol := 0 TO 15 DO
            x_horizon[kStep + 1, iRow] := x_horizon[kStep + 1, iRow] + (matA[iRow, iCol] * x_horizon[kStep, iCol]);
        END_FOR;
        FOR iInput := 0 TO 7 DO
            x_horizon[kStep + 1, iRow] := x_horizon[kStep + 1, iRow] + (matB[iRow, iInput] * u_horizon[kStep, iInput]);
        END_FOR;
    END_FOR;
    FOR iInput := 0 TO 7 DO
        u_horizon[kStep + 1, iInput] := u_horizon[kStep, iInput];
    END_FOR;
END_FOR;

(* Analytical Projected Gradient Calculation of Quadratic Cost: J = (x-xref)^T Q (x-xref) + u^T R u *)
FOR iInput := 0 TO 7 DO
    grad_J[iInput] := 2.0 * R_diag[iInput] * u[iInput];
    FOR iRow := 0 TO 15 DO
        (* Backpropagate state error through input matrix B *)
        grad_J[iInput] := grad_J[iInput] + 2.0 * matB[iRow, iInput] * Q_diag[iRow] * (x_horizon[4, iRow] - x_ref[iRow]);
    END_FOR;
    
    (* Projected Gradient Descent Step: delta_u = -alpha * grad_J *)
    delta_u[iInput] := -0.015 * grad_J[iInput];
    
    (* Apply Actuator Slew Rate Limiter *)
    IF delta_u[iInput] > 15.0 THEN delta_u[iInput] := 15.0; END_IF;
    IF delta_u[iInput] < -15.0 THEN delta_u[iInput] := -15.0; END_IF;
    
    u_mpc[iInput] := u[iInput] + delta_u[iInput];
END_FOR;

(* Saturate MPC Control Signals within Certified Mechanical Bounds *)
IF u_mpc[0] > 180.0 THEN u_mpc[0] := 180.0; END_IF; (* Drum 1 max torque [Nm] *)
IF u_mpc[0] < -180.0 THEN u_mpc[0] := -180.0; END_IF;
IF u_mpc[1] > 220.0 THEN u_mpc[1] := 220.0; END_IF; (* Drum 2 max torque [Nm] *)
IF u_mpc[1] < -220.0 THEN u_mpc[1] := -220.0; END_IF;
IF u_mpc[2] > 250.0 THEN u_mpc[2] := 250.0; END_IF; (* Shaping air max flow [slpm] *)
IF u_mpc[2] < 0.0 THEN u_mpc[2] := 0.0; END_IF;
IF u_mpc[3] > 60.0 THEN u_mpc[3] := 60.0; END_IF;   (* Bead slide max vel [mm/s] *)
IF u_mpc[3] < -60.0 THEN u_mpc[3] := -60.0; END_IF;
IF u_mpc[4] > c_rMaxStitcherForce_N THEN u_mpc[4] := c_rMaxStitcherForce_N; END_IF;
IF u_mpc[4] < 0.0 THEN u_mpc[4] := 0.0; END_IF;
IF u_mpc[5] > c_rMaxStitcherForce_N THEN u_mpc[5] := c_rMaxStitcherForce_N; END_IF;
IF u_mpc[5] < 0.0 THEN u_mpc[5] := 0.0; END_IF;
IF u_mpc[6] > 800.0 THEN u_mpc[6] := 800.0; END_IF; (* Transfer ring gantry max traverse [mm/s] *)
IF u_mpc[6] < -800.0 THEN u_mpc[6] := -800.0; END_IF;
IF u_mpc[7] > 45.0 THEN u_mpc[7] := 45.0; END_IF;   (* Festoon tension trim [Nm] *)
IF u_mpc[7] < -45.0 THEN u_mpc[7] := -45.0; END_IF;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 4: IN-LINE 3D LASER TRIANGULATION SPLICE METROLOGY & CENTERING
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 4: IN-LINE 3D LASER TRIANGULATION SPLICE METROLOGY & CIRCUMFERENTIAL RUNOUT HARMONICS               *)
(* ========================================================================================================== *)

(* Record Laser Radial Measurement into 36-Point Circular Buffer (10 deg resolution) *)
iLaser_BufferIdx := REAL_TO_INT(rVoted_Drum1_Angle_deg / 10.0) MOD 36;
IF iLaser_BufferIdx >= 0 AND iLaser_BufferIdx < 36 THEN
    rLaser_ScanBuffer[iLaser_BufferIdx] := rLaser_SpliceThickness_mm;
END_IF;

(* Evaluate Splice Overlap Width against Nominal [1.5, 3.5] mm Window *)
IF (rVoted_SpliceOverlap_mm >= c_rSpliceOverlap_Min_mm) AND 
   (rVoted_SpliceOverlap_mm <= c_rSpliceOverlap_Max_mm) THEN
    bSpliceOverlap_InRange := TRUE;
ELSE
    bSpliceOverlap_InRange := FALSE;
END_IF;

(* Evaluate Dog-Ear Splice Height Step Discontinuity *)
IF rLaser_DogEar_Height_mm > c_rDogEar_Max_mm THEN
    bDogEar_Defect_Detected := TRUE;
ELSE
    bDogEar_Defect_Detected := FALSE;
END_IF;

(* Compute 1st Harmonic (Radial Eccentricity) & 2nd Harmonic (Radial Ovality) via Discrete Fourier Integration *)
rSumFourierCos1 := 0.0;
rSumFourierSin1 := 0.0;
rSumFourierCos2 := 0.0;
rSumFourierSin2 := 0.0;

FOR iScan := 0 TO 35 DO
    rSumFourierCos1 := rSumFourierCos1 + (rLaser_ScanBuffer[iScan] * COS(iScan * 2.0 * c_rPi / 36.0));
    rSumFourierSin1 := rSumFourierSin1 + (rLaser_ScanBuffer[iScan] * SIN(iScan * 2.0 * c_rPi / 36.0));
    rSumFourierCos2 := rSumFourierCos2 + (rLaser_ScanBuffer[iScan] * COS(iScan * 4.0 * c_rPi / 36.0));
    rSumFourierSin2 := rSumFourierSin2 + (rLaser_ScanBuffer[iScan] * SIN(iScan * 4.0 * c_rPi / 36.0));
END_FOR;

rCalculated_Harmonic_1H_mm := (2.0 / 36.0) * SQRT((rSumFourierCos1 * rSumFourierCos1) + (rSumFourierSin1 * rSumFourierSin1));
rCalculated_Harmonic_2H_mm := (2.0 / 36.0) * SQRT((rSumFourierCos2 * rSumFourierCos2) + (rSumFourierSin2 * rSumFourierSin2));
rCalculated_Runout_Radial_mm := rCalculated_Harmonic_1H_mm + rCalculated_Harmonic_2H_mm;
rCalculated_Runout_Lateral_mm := ABS(rLaser_LateralOffset_mm);

(* Set Splice Quality Master Boolean *)
IF bSpliceOverlap_InRange AND NOT bDogEar_Defect_Detected AND (rCalculated_Runout_Radial_mm < 0.65) THEN
    bSpliceQuality_Passed := TRUE;
ELSE
    bSpliceQuality_Passed := FALSE;
END_IF;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 5: DYNAMIC CARCASS SHAPING & BALLSCREW BEAD LOCK SYNCHRONIZATION
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 5: DYNAMIC CARCASS SHAPING & BALLSCREW BEAD LOCK SYNCHRONIZATION                                     *)
(* ========================================================================================================== *)

(* Closed-Loop Proportional-Integral-Derivative (PID) Shaping Bladder Pressure Regulation *)
IF (iFSM_State = 4) OR (iFSM_State = 9) OR (iFSM_State = 10) THEN
    (* Pressure Error *)
    rShapingPressure_PrevErr := rTargetShapingPressure_bar - rVoted_ShapingPressure_bar;
    rShapingPressure_Integral := rShapingPressure_Integral + (rShapingPressure_PrevErr * c_rSampleTime_s);
    
    (* Anti-Windup Clamping on Pressure Integral *)
    IF rShapingPressure_Integral > 1.50 THEN rShapingPressure_Integral := 1.50; END_IF;
    IF rShapingPressure_Integral < -0.50 THEN rShapingPressure_Integral := -0.50; END_IF;
    
    (* Total Proportional Valve Command: Feedforward Target + Closed Loop PID *)
    rShapingPressure_Cmd_bar := rTargetShapingPressure_bar + 
                                (rShapingPressure_PID_P * rShapingPressure_PrevErr) + 
                                (rShapingPressure_PID_I * rShapingPressure_Integral) + 
                                (rShapingPressure_PID_D * (rShapingPressure_PrevErr - rShapingPressure_PrevErr) / c_rSampleTime_s);
                                
    IF rShapingPressure_Cmd_bar > c_rMaxShapingPressure_bar THEN
        rShapingPressure_Cmd_bar := c_rMaxShapingPressure_bar;
    END_IF;
    IF rShapingPressure_Cmd_bar < 0.0 THEN
        rShapingPressure_Cmd_bar := 0.0;
    END_IF;
    
    bShapingAir_InflateValve := TRUE;
    bShapingAir_ExhaustValve := FALSE;
    rShapingAirMassFlow_slpm := rShapingPressure_Cmd_bar * 65.0; (* Proportional valve flow curve *)
ELSE
    IF iFSM_State = 11 OR iFSM_State = 12 OR iFSM_State = 0 THEN
        rShapingPressure_Cmd_bar := 0.0;
        bShapingAir_InflateValve := FALSE;
        bShapingAir_ExhaustValve := TRUE; (* Open rapid exhaust valve *)
        rShapingAirMassFlow_slpm := 0.0;
        rShapingPressure_Integral := 0.0;
    ELSE
        rShapingPressure_Cmd_bar := 0.20; (* Holding bias pressure *)
        bShapingAir_InflateValve := FALSE;
        bShapingAir_ExhaustValve := FALSE;
        rShapingAirMassFlow_slpm := 0.0;
    END_IF;
END_IF;

(* Synchronized Ballscrew Bead Slide Velocity Profiling *)
IF iFSM_State = 4 THEN
    (* Move inward symmetrically to form toroid *)
    IF rBeadSpacingCurrent_mm > rTargetBeadDistance_mm THEN
        rBeadSlide_LH_SpeedCmd_mms := -35.0; (* Left slide moves positive X inward *)
        rBeadSlide_RH_SpeedCmd_mms := 35.0;  (* Right slide moves negative X inward *)
    ELSE
        rBeadSlide_LH_SpeedCmd_mms := 0.0;
        rBeadSlide_RH_SpeedCmd_mms := 0.0;
    END_IF;
ELSIF iFSM_State = 11 OR iFSM_State = 12 THEN
    (* Retract bead slides back to carcass loading position *)
    IF rBeadSlide_LH_Pos_mm < 350.0 THEN
        rBeadSlide_LH_SpeedCmd_mms := 45.0;
        rBeadSlide_RH_SpeedCmd_mms := -45.0;
    ELSE
        rBeadSlide_LH_SpeedCmd_mms := 0.0;
        rBeadSlide_RH_SpeedCmd_mms := 0.0;
    END_IF;
ELSE
    rBeadSlide_LH_SpeedCmd_mms := 0.0;
    rBeadSlide_RH_SpeedCmd_mms := 0.0;
END_IF;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 6: DUAL-DRUM ROTARY & FESTOON WEB TENSION SYNCHRONIZATION
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 6: DUAL-DRUM ROTARY & FESTOON WEB TENSION ELECTRONIC LINE-SHAFT SYNCHRONIZATION                     *)
(* ========================================================================================================== *)

(* Inner Liner Payout Servicer Synchronous Electronic Cam Following *)
IF iFSM_State = 1 THEN
    (* Tangential Surface Speed Match: v = omega * r *)
    rServicer_InnerLiner_SpeedCmd_mms := (rVoted_Drum1_Speed_rpm * c_rPi * c_rDrum1_NominalOD_mm) / 60.0;
    
    (* Closed-Loop Dancer Potentiometer Position PI Trim (50% neutral target) *)
    rDancer_InnerLiner_Integral := rDancer_InnerLiner_Integral + ((50.0 - rDancerPosition_InnerLiner_pct) * c_rSampleTime_s);
    IF rDancer_InnerLiner_Integral > 25.0 THEN rDancer_InnerLiner_Integral := 25.0; END_IF;
    IF rDancer_InnerLiner_Integral < -25.0 THEN rDancer_InnerLiner_Integral := -25.0; END_IF;
    
    rServicer_InnerLiner_SpeedCmd_mms := rServicer_InnerLiner_SpeedCmd_mms + 
                                         (rDancer_PID_P * (50.0 - rDancerPosition_InnerLiner_pct)) + 
                                         (rDancer_PID_I * rDancer_InnerLiner_Integral);
ELSE
    rServicer_InnerLiner_SpeedCmd_mms := 0.0;
    rDancer_InnerLiner_Integral := 0.0;
END_IF;

(* Extruded Rubber Tread Servicer Electronic Cam Following on Drum 2 *)
IF iFSM_State = 7 THEN
    rServicer_Tread_SpeedCmd_mms := (rDrum2_Speed_rpm * c_rPi * c_rDrum2_NominalOD_mm) / 60.0;
    
    rDancer_Tread_Integral := rDancer_Tread_Integral + ((50.0 - rDancerPosition_Tread_pct) * c_rSampleTime_s);
    IF rDancer_Tread_Integral > 30.0 THEN rDancer_Tread_Integral := 30.0; END_IF;
    IF rDancer_Tread_Integral < -30.0 THEN rDancer_Tread_Integral := -30.0; END_IF;
    
    rServicer_Tread_SpeedCmd_mms := rServicer_Tread_SpeedCmd_mms + 
                                    (rDancer_PID_P * (50.0 - rDancerPosition_Tread_pct)) + 
                                    (rDancer_PID_I * rDancer_Tread_Integral);
ELSE
    rServicer_Tread_SpeedCmd_mms := 0.0;
    rDancer_Tread_Integral := 0.0;
END_IF;

(* Nylon Cap Ply High-Speed Spiral Winder Tension Regulation *)
IF iFSM_State = 6 THEN
    rCapPly_Winder_TensionCmd_N := 28.5; (* 28.5 N target winding tension *)
ELSE
    rCapPly_Winder_TensionCmd_N := 5.0;  (* Standby retention tension *)
END_IF;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 7: TWIN MULTI-AXIS ROBOTIC STITCHER PROFILE CONTROL
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 7: TWIN MULTI-AXIS ROBOTIC STITCHER CONTOUR FORCE VECTOR CONTROL                                    *)
(* ========================================================================================================== *)

IF iFSM_State = 10 THEN
    (* Progress from Crown (0%) to Bead Toe (100%) *)
    rStitcherProgress_pct := (rStepTimer_s / 12.0) * 100.0;
    IF rStitcherProgress_pct > 100.0 THEN rStitcherProgress_pct := 100.0; END_IF;
    
    (* Dynamic Force Profile: 1,500 N at crown, peaking at 2,200 N at shoulder, 1,800 N at sidewall *)
    IF rStitcherProgress_pct < 35.0 THEN
        rStitcherTargetForce_N := 1500.0 + ((rStitcherProgress_pct / 35.0) * 700.0);
    ELSIF rStitcherProgress_pct < 75.0 THEN
        rStitcherTargetForce_N := 2200.0 - (((rStitcherProgress_pct - 35.0) / 40.0) * 400.0);
    ELSE
        rStitcherTargetForce_N := 1800.0;
    END_IF;
    
    (* LH Stitcher Closed-Loop Force PI Control *)
    rStitcherForce_PrevErr_LH := rStitcherTargetForce_N - rVoted_StitcherForce_LH_N;
    rStitcherForce_Integral_LH := rStitcherForce_Integral_LH + (rStitcherForce_PrevErr_LH * c_rSampleTime_s);
    IF rStitcherForce_Integral_LH > 500.0 THEN rStitcherForce_Integral_LH := 500.0; END_IF;
    IF rStitcherForce_Integral_LH < -500.0 THEN rStitcherForce_Integral_LH := -500.0; END_IF;
    
    rStitcher_LH_ForceCmd_N := rStitcherTargetForce_N + 
                               (rStitcherForcePID_P * rStitcherForce_PrevErr_LH) + 
                               (rStitcherForcePID_I * rStitcherForce_Integral_LH);
                               
    (* RH Stitcher Closed-Loop Force PI Control *)
    rStitcherForce_PrevErr_RH := rStitcherTargetForce_N - rVoted_StitcherForce_RH_N;
    rStitcherForce_Integral_RH := rStitcherForce_Integral_RH + (rStitcherForce_PrevErr_RH * c_rSampleTime_s);
    IF rStitcherForce_Integral_RH > 500.0 THEN rStitcherForce_Integral_RH := 500.0; END_IF;
    IF rStitcherForce_Integral_RH < -500.0 THEN rStitcherForce_Integral_RH := -500.0; END_IF;
    
    rStitcher_RH_ForceCmd_N := rStitcherTargetForce_N + 
                               (rStitcherForcePID_P * rStitcherForce_PrevErr_RH) + 
                               (rStitcherForcePID_I * rStitcherForce_Integral_RH);
                               
    (* Axial Stitcher Feed Velocity Profile *)
    rStitcher_LH_AxialVelCmd_mms := -28.0; (* Traverse outward along left shoulder/sidewall *)
    rStitcher_RH_AxialVelCmd_mms := 28.0;  (* Traverse outward along right shoulder/sidewall *)
    
    (* Swivel Angle Follows Normal Meridian Tangent Angle *)
    rStitcher_LH_SwivelAngleCmd_deg := (rStitcherProgress_pct / 100.0) * 75.0;
    rStitcher_RH_SwivelAngleCmd_deg := -(rStitcherProgress_pct / 100.0) * 75.0;
ELSE
    rStitcher_LH_ForceCmd_N := 0.0;
    rStitcher_RH_ForceCmd_N := 0.0;
    rStitcher_LH_AxialVelCmd_mms := 0.0;
    rStitcher_RH_AxialVelCmd_mms := 0.0;
    rStitcher_LH_SwivelAngleCmd_deg := 0.0;
    rStitcher_RH_SwivelAngleCmd_deg := 0.0;
    rStitcherForce_Integral_LH := 0.0;
    rStitcherForce_Integral_RH := 0.0;
    rStitcherProgress_pct := 0.0;
END_IF;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                                  *)
(* ========================================================================================================== *)
rStageTimer_s := rStageTimer_s + c_rSampleTime_s;
rStepTimer_s := rStepTimer_s + c_rSampleTime_s;
rTotalCycleTimer_s := rTotalCycleTimer_s + c_rSampleTime_s;
rCycleTimeElapsed_s := rTotalCycleTimer_s;

CASE iFSM_State OF
    0: (* IDLE & PRE-CYCLE VERIFICATION *)
        bSystemReady := TRUE;
        bCycleInProgress := FALSE;
        bCycleCompleted := FALSE;
        rDrum1_SpeedCmd_rpm := 0.0;
        rDrum2_SpeedCmd_rpm := 0.0;
        bDrum1_ExpandCmd := FALSE;
        bDrum1_CollapseCmd := TRUE;
        bDrum2_ExpandCmd := FALSE;
        bDrum2_CollapseCmd := TRUE;
        rTargetShapingPressure_bar := 0.0;
        rStageTimer_s := 0.0;
        rStepTimer_s := 0.0;
        rTotalCycleTimer_s := 0.0;
        iSubStep := 0;
        
        IF bRecipeStartTrigger AND bMasterEnable AND NOT bGeneralFault THEN
            bSystemReady := FALSE;
            bCycleInProgress := TRUE;
            iFSM_State := 1; (* Initiate Stage 1 *)
            rStageTimer_s := 0.0;
            rStepTimer_s := 0.0;
        END_IF;

    1: (* STAGE 1: DRUM 1 INNER LINER & BODY PLY WINDING *)
        bDrum1_ExpandCmd := TRUE;
        bDrum1_CollapseCmd := FALSE;
        
        CASE iSubStep OF
            0: (* Expand Drum 1 segments *)
                IF rStageTimer_s > 1.2 THEN
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Wind Inner Liner and 1st Body Ply at 60 rpm *)
                rDrum1_SpeedCmd_rpm := 60.0;
                rDrum1_TorqueLimit_Nm := 140.0;
                IF rVoted_Drum1_Angle_deg >= 375.0 OR rStepTimer_s >= 2.5 THEN
                    rDrum1_SpeedCmd_rpm := 0.0;
                    iSubStep := 2;
                    rStepTimer_s := 0.0;
                END_IF;
            2: (* Splicing tack stitch roll-down *)
                IF rStepTimer_s >= 0.8 THEN
                    iFSM_State := 2; (* Advance to Splice Laser Metrology *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    2: (* STAGE 2: SPLICE LASER METROLOGY VERIFICATION *)
        rDrum1_SpeedCmd_rpm := 12.0; (* Slow crawl for precision 3D blue-laser profiling *)
        rDrum1_TorqueLimit_Nm := 80.0;
        
        IF rStepTimer_s >= 3.0 THEN
            rDrum1_SpeedCmd_rpm := 0.0;
            IF bSpliceQuality_Passed THEN
                iFSM_State := 3; (* Splice passed: Advance to Bead Setting *)
                iSubStep := 0;
                rStageTimer_s := 0.0;
                rStepTimer_s := 0.0;
            ELSE
                bGeneralFault := TRUE;
                dwDiagnosticWord_04 := dwDiagnosticWord_04 OR 16#00000001; (* Splice reject *)
                iFSM_State := 12; (* Defect reject: emergency abort *)
            END_IF;
        END_IF;

    3: (* STAGE 3: DUAL BEAD CORE SETTING & MECHANICAL LOCK *)
        rBeadSetter_LH_PosCmd_mm := rTargetBeadDistance_mm * 0.5;
        rBeadSetter_RH_PosCmd_mm := -rTargetBeadDistance_mm * 0.5;
        
        CASE iSubStep OF
            0: (* Advance bead setter carriage rings *)
                IF rStepTimer_s >= 1.5 THEN
                    bBeadLock_ClampCmd := TRUE; (* Lock mechanical toggle clamps *)
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Verify bead lock clamped status *)
                IF bBeadLock_LH_Clamped AND bBeadLock_RH_Clamped AND (rStepTimer_s >= 0.8) THEN
                    rBeadSetter_LH_PosCmd_mm := 450.0; (* Retract bead setter arms *)
                    rBeadSetter_RH_PosCmd_mm := -450.0;
                    iSubStep := 2;
                    rStepTimer_s := 0.0;
                END_IF;
            2: (* Bead setters safely parked *)
                IF rStepTimer_s >= 1.0 THEN
                    iFSM_State := 4; (* Advance to Carcass Shaping *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    4: (* STAGE 4: BLADDER INFLATION TOROIDAL SHAPING & PLY TURN-UP *)
        CASE iSubStep OF
            0: (* Pre-shape bladder inflation (0.65 bar) *)
                rTargetShapingPressure_bar := 0.65;
                IF (rVoted_ShapingPressure_bar >= 0.55) AND (rStepTimer_s >= 1.2) THEN
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Symmetric bead slide inward motion & full toroidal inflation (2.00 bar) *)
                rTargetShapingPressure_bar := 2.00;
                bTurnUpBladder_LH_Cmd := TRUE; (* Inflate turn-up bladders *)
                bTurnUpBladder_RH_Cmd := TRUE;
                IF (rBeadSpacingCurrent_mm <= (rTargetBeadDistance_mm + 2.0)) AND (rStepTimer_s >= 2.5) THEN
                    bTurnUpBladder_LH_Cmd := FALSE; (* Deflate turn-up bladders *)
                    bTurnUpBladder_RH_Cmd := FALSE;
                    iSubStep := 2;
                    rStepTimer_s := 0.0;
                END_IF;
            2: (* Toroidal shape established and stabilized *)
                IF rStepTimer_s >= 1.0 THEN
                    iFSM_State := 5; (* Advance to Drum 2 Belt Assembly *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    5: (* STAGE 5: DRUM 2 STEEL BELT 1 & 2 APPLICATION *)
        bDrum2_ExpandCmd := TRUE;
        bDrum2_CollapseCmd := FALSE;
        
        CASE iSubStep OF
            0: (* Expand Drum 2 *)
                IF rStepTimer_s >= 1.0 THEN
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Apply Steel Belt 1 (+21 deg cord bias) at 45 rpm *)
                rDrum2_SpeedCmd_rpm := 45.0;
                rDrum2_TorqueLimit_Nm := 160.0;
                IF rStepTimer_s >= 1.8 THEN
                    rDrum2_SpeedCmd_rpm := 0.0;
                    iSubStep := 2;
                    rStepTimer_s := 0.0;
                END_IF;
            2: (* Apply Steel Belt 2 (-21 deg cord bias) at 45 rpm *)
                rDrum2_SpeedCmd_rpm := 45.0;
                IF rStepTimer_s >= 1.8 THEN
                    rDrum2_SpeedCmd_rpm := 0.0;
                    iSubStep := 3;
                    rStepTimer_s := 0.0;
                END_IF;
            3: (* Belts application complete *)
                IF rStepTimer_s >= 0.5 THEN
                    iFSM_State := 6; (* Advance to Spiral Cap Ply Winding *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    6: (* STAGE 6: SPIRAL NYLON CAP PLY HIGH-SPEED WINDING *)
        rDrum2_SpeedCmd_rpm := 180.0; (* High-speed spiral wrap *)
        rDrum2_TorqueLimit_Nm := 120.0;
        
        IF rStepTimer_s >= 3.5 THEN
            rDrum2_SpeedCmd_rpm := 0.0;
            iFSM_State := 7; (* Advance to Extruded Tread Application *)
            iSubStep := 0;
            rStageTimer_s := 0.0;
            rStepTimer_s := 0.0;
        END_IF;

    7: (* STAGE 7: EXTRUDED TREAD APPLICATION & ULTRASONIC SPLICE CUT *)
        CASE iSubStep OF
            0: (* Feed and wrap extruded rubber tread slab at 30 rpm *)
                rDrum2_SpeedCmd_rpm := 30.0;
                rDrum2_TorqueLimit_Nm := 180.0;
                IF rStepTimer_s >= 2.2 THEN
                    rDrum2_SpeedCmd_rpm := 0.0;
                    bUltrasonicCutter_Trigger := TRUE; (* Trigger ultrasonic skive cut *)
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Consolidate tread bevel splice *)
                bUltrasonicCutter_Trigger := FALSE;
                IF rStepTimer_s >= 1.2 THEN
                    iFSM_State := 8; (* Advance to Transfer Ring Pick *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    8: (* STAGE 8: BELT/TREAD PACKAGE TRANSFER RING PICK *)
        CASE iSubStep OF
            0: (* Gantry traverses over Drum 2 centerline *)
                rTransferRing_TargetAxialPos_mm := c_rDrum2_CenterAxialPos_mm;
                rTransferRing_AxialSpeedCmd_mms := 600.0;
                IF (ABS(rTransferRing_AxialPos_mm - c_rDrum2_CenterAxialPos_mm) <= 0.5) AND (rStepTimer_s >= 1.5) THEN
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Segments clamp radially on belt/tread package & vacuum on *)
                rTransferRing_SegmentDiamCmd_mm := rDrum2_SegmentDiameter_mm;
                bTransferRing_VacuumCmd := TRUE;
                bTransferRing_GripLocked := TRUE;
                IF bTransferRing_VacuumLocked AND (rStepTimer_s >= 1.0) THEN
                    bDrum2_CollapseCmd := TRUE; (* Collapse Drum 2 *)
                    bDrum2_ExpandCmd := FALSE;
                    iSubStep := 2;
                    rStepTimer_s := 0.0;
                END_IF;
            2: (* Drum 2 collapsed: ready to transfer *)
                IF bDrum2_Collapsed_Prox AND (rStepTimer_s >= 1.0) THEN
                    iFSM_State := 9; (* Advance to Coaxial Transfer over Drum 1 *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    9: (* STAGE 9: COAXIAL ASSEMBLY OVER SHAPED CARCASS ON DRUM 1 *)
        CASE iSubStep OF
            0: (* Gantry traverses across machine centerline to Drum 1 *)
                rTransferRing_TargetAxialPos_mm := c_rDrum1_CenterAxialPos_mm;
                rTransferRing_AxialSpeedCmd_mms := 550.0;
                IF (ABS(rTransferRing_AxialPos_mm - c_rDrum1_CenterAxialPos_mm) <= 0.2) AND (rStepTimer_s >= 2.0) THEN
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Verify coaxial runout via laser sensor (< 0.10 mm) *)
                IF (ABS(rTransferRing_LaserConcentricity_mm) <= c_rTransferRingConcentricityTol_mm) AND (rStepTimer_s >= 0.8) THEN
                    (* Final inflation expansion pushes carcass crown into firm contact with belt ID *)
                    rTargetShapingPressure_bar := 2.20;
                    iSubStep := 2;
                    rStepTimer_s := 0.0;
                END_IF;
            2: (* Contact verified: advance to stitching *)
                IF (rVoted_ShapingPressure_bar >= 2.10) AND (rStepTimer_s >= 1.0) THEN
                    iFSM_State := 10; (* Advance to High Pressure Stitching *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    10: (* STAGE 10: HIGH-PRESSURE STITCHER ROLL-DOWN *)
        CASE iSubStep OF
            0: (* Release transfer ring vacuum & open segments *)
                bTransferRing_VacuumCmd := FALSE;
                bTransferRing_GripLocked := FALSE;
                rTransferRing_SegmentDiamCmd_mm := rTransferRing_SegmentDiamCmd_mm + 40.0;
                IF rStepTimer_s >= 0.8 THEN
                    rTransferRing_TargetAxialPos_mm := 1800.0; (* Retract transfer ring to neutral park *)
                    rTransferRing_AxialSpeedCmd_mms := 500.0;
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Twin stitchers execute crown-to-bead trajectory at 80 rpm drum rotation *)
                rDrum1_SpeedCmd_rpm := 80.0;
                rDrum1_TorqueLimit_Nm := 170.0;
                IF rStepTimer_s >= 12.0 THEN
                    rDrum1_SpeedCmd_rpm := 0.0;
                    iSubStep := 2;
                    rStepTimer_s := 0.0;
                END_IF;
            2: (* Stitching complete: log green tire dimensions *)
                rGreenTire_OD_Actual_mm := rToroidalCarcassRadius_mm * 2.0;
                rGreenTire_BeadDist_Actual_mm := rBeadSpacingCurrent_mm;
                IF rStepTimer_s >= 0.5 THEN
                    iFSM_State := 11; (* Advance to Discharge *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    11: (* STAGE 11: GREEN TIRE DISCHARGE TO CURING PRESS PALLET *)
        CASE iSubStep OF
            0: (* Exhaust shaping air & release mechanical bead clamps *)
                rTargetShapingPressure_bar := 0.0;
                bShapingAir_InflateValve := FALSE;
                bShapingAir_ExhaustValve := TRUE;
                bBeadLock_ClampCmd := FALSE;
                IF (rVoted_ShapingPressure_bar <= 0.15) AND (rStepTimer_s >= 1.5) THEN
                    bDrum1_CollapseCmd := TRUE; (* Collapse Drum 1 *)
                    bDrum1_ExpandCmd := FALSE;
                    iSubStep := 1;
                    rStepTimer_s := 0.0;
                END_IF;
            1: (* Green tire unloader swing arm picks green tire *)
                bGreenTireUnloader_PickCmd := TRUE;
                IF rStepTimer_s >= 2.0 THEN
                    bGreenTireUnloader_PickCmd := FALSE;
                    bCycleCompleted := TRUE;
                    iSubStep := 2;
                    rStepTimer_s := 0.0;
                END_IF;
            2: (* Cycle complete: return to IDLE *)
                IF rStepTimer_s >= 1.0 THEN
                    iFSM_State := 0; (* Return to Idle ready for next cycle *)
                    iSubStep := 0;
                    rStageTimer_s := 0.0;
                    rStepTimer_s := 0.0;
                END_IF;
        END_CASE;

    12: (* STAGE 12: EMERGENCY BLADDER DEFLATE & DRUM COLLAPSE *)
        rDrum1_SpeedCmd_rpm := 0.0;
        rDrum2_SpeedCmd_rpm := 0.0;
        rTargetShapingPressure_bar := 0.0;
        bShapingAir_InflateValve := FALSE;
        bShapingAir_ExhaustValve := TRUE; (* Dump air rapidly *)
        bTurnUpBladder_LH_Cmd := FALSE;
        bTurnUpBladder_RH_Cmd := FALSE;
        bBeadLock_ClampCmd := FALSE;
        bDrum1_CollapseCmd := TRUE;
        bDrum1_ExpandCmd := FALSE;
        bDrum2_CollapseCmd := TRUE;
        bDrum2_ExpandCmd := FALSE;
        bTransferRing_VacuumCmd := FALSE;
        bTransferRing_GripLocked := FALSE;
        rStitcher_LH_ForceCmd_N := 0.0;
        rStitcher_RH_ForceCmd_N := 0.0;
        bGeneralFault := TRUE;
        
        IF bFaultReset AND bEmergencyStop_CircuitOK AND bSafetyScannerClear THEN
            bGeneralFault := FALSE;
            iFSM_State := 0; (* Reset to IDLE *)
            iSubStep := 0;
            rStageTimer_s := 0.0;
            rStepTimer_s := 0.0;
        END_IF;

    ELSE
        iFSM_State := 12; (* Unrecognized state recovery *)
END_CASE;

iCurrentStage := iFSM_State;
""")

    # ----------------------------------------------------------------------------------------------------------
    # PHASE 9: ISA-18.2 ALARMS & BIT-PACKED DIAGNOSTIC TELEMETRY
    # ----------------------------------------------------------------------------------------------------------
    parts.append("""(* ========================================================================================================== *)
(* PHASE 9: ISA-18.2 MULTI-TIERED ALARMS & BIT-PACKED TELEMETRY DWORDS                                        *)
(* ========================================================================================================== *)

(* --- Splice Overlap Width Alarms --- *)
IF rVoted_SpliceOverlap_mm >= c_rSpliceOverlap_HH_mm THEN
    bAlarm_SpliceOverlap_HH := TRUE;
ELSIF rVoted_SpliceOverlap_mm <= (c_rSpliceOverlap_HH_mm - c_rHysteresis_mm) THEN
    bAlarm_SpliceOverlap_HH := FALSE;
END_IF;

IF rVoted_SpliceOverlap_mm <= c_rSpliceOverlap_LL_mm AND (iFSM_State = 2) THEN
    bAlarm_SpliceOverlap_LL := TRUE;
ELSIF rVoted_SpliceOverlap_mm >= (c_rSpliceOverlap_LL_mm + c_rHysteresis_mm) THEN
    bAlarm_SpliceOverlap_LL := FALSE;
END_IF;

(* --- Shaping Bladder Pressure Alarms (ISA-18.2 HH, H, L, LL) --- *)
IF rVoted_ShapingPressure_bar >= c_rPressure_HH_bar THEN
    bAlarm_ShapingPressure_HH := TRUE;
ELSIF rVoted_ShapingPressure_bar <= (c_rPressure_HH_bar - c_rHysteresis_bar) THEN
    bAlarm_ShapingPressure_HH := FALSE;
END_IF;

IF rVoted_ShapingPressure_bar >= c_rPressure_H_bar THEN
    bAlarm_ShapingPressure_H := TRUE;
ELSIF rVoted_ShapingPressure_bar <= (c_rPressure_H_bar - c_rHysteresis_bar) THEN
    bAlarm_ShapingPressure_H := FALSE;
END_IF;

IF (rVoted_ShapingPressure_bar <= c_rPressure_L_bar) AND (iFSM_State = 4 OR iFSM_State = 9 OR iFSM_State = 10) THEN
    bAlarm_ShapingPressure_L := TRUE;
ELSIF rVoted_ShapingPressure_bar >= (c_rPressure_L_bar + c_rHysteresis_bar) THEN
    bAlarm_ShapingPressure_L := FALSE;
END_IF;

IF (rVoted_ShapingPressure_bar <= c_rPressure_LL_bar) AND (iFSM_State = 4 OR iFSM_State = 9 OR iFSM_State = 10) THEN
    bAlarm_ShapingPressure_LL := TRUE;
ELSIF rVoted_ShapingPressure_bar >= (c_rPressure_LL_bar + c_rHysteresis_bar) THEN
    bAlarm_ShapingPressure_LL := FALSE;
END_IF;

(* --- Transfer Ring Concentricity Runout Alarm --- *)
IF ABS(rTransferRing_LaserConcentricity_mm) >= c_rTransferRingRunout_HH_mm THEN
    bAlarm_TransferRingRunout_HH := TRUE;
ELSIF ABS(rTransferRing_LaserConcentricity_mm) <= (c_rTransferRingRunout_HH_mm - c_rHysteresis_mm) THEN
    bAlarm_TransferRingRunout_HH := FALSE;
END_IF;

(* --- Stitcher Contact Force Alarms --- *)
IF (rVoted_StitcherForce_LH_N >= c_rStitcherForce_HH_N) OR (rVoted_StitcherForce_RH_N >= c_rStitcherForce_HH_N) THEN
    bAlarm_StitcherForce_HH := TRUE;
ELSIF (rVoted_StitcherForce_LH_N <= (c_rStitcherForce_HH_N - c_rHysteresis_N)) AND 
      (rVoted_StitcherForce_RH_N <= (c_rStitcherForce_HH_N - c_rHysteresis_N)) THEN
    bAlarm_StitcherForce_HH := FALSE;
END_IF;

IF ((rVoted_StitcherForce_LH_N <= c_rStitcherForce_LL_N) OR (rVoted_StitcherForce_RH_N <= c_rStitcherForce_LL_N)) AND (iFSM_State = 10) THEN
    bAlarm_StitcherForce_LL := TRUE;
ELSIF (rVoted_StitcherForce_LH_N >= (c_rStitcherForce_LL_N + c_rHysteresis_N)) AND 
      (rVoted_StitcherForce_RH_N >= (c_rStitcherForce_LL_N + c_rHysteresis_N)) THEN
    bAlarm_StitcherForce_LL := FALSE;
END_IF;

(* --- Servicer Festoon Web Tension Alarms --- *)
IF rFestoonTension_InnerLiner_N >= c_rFestoonTension_HH_N OR rFestoonTension_Tread_N >= c_rFestoonTension_HH_N THEN
    bAlarm_FestoonTension_HH := TRUE;
ELSIF rFestoonTension_InnerLiner_N <= (c_rFestoonTension_HH_N - c_rHysteresis_N) AND 
      rFestoonTension_Tread_N <= (c_rFestoonTension_HH_N - c_rHysteresis_N) THEN
    bAlarm_FestoonTension_HH := FALSE;
END_IF;

IF (rFestoonTension_InnerLiner_N <= c_rFestoonTension_LL_N AND iFSM_State = 1) OR 
   (rFestoonTension_Tread_N <= c_rFestoonTension_LL_N AND iFSM_State = 7) THEN
    bAlarm_FestoonTension_LL := TRUE;
ELSIF rFestoonTension_InnerLiner_N >= (c_rFestoonTension_LL_N + c_rHysteresis_N) AND 
      rFestoonTension_Tread_N >= (c_rFestoonTension_LL_N + c_rHysteresis_N) THEN
    bAlarm_FestoonTension_LL := FALSE;
END_IF;

(* Evaluate General Fault Status *)
IF bAlarm_SpliceOverlap_HH OR bAlarm_SpliceOverlap_LL OR bAlarm_ShapingPressure_HH OR 
   bAlarm_ShapingPressure_LL OR bAlarm_TransferRingRunout_HH OR bAlarm_TMR_BankFailure THEN
    bGeneralFault := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------- *)
(* PACK TELEMETRY DWORDS                                                                                      *)
(* ---------------------------------------------------------------------------------------------------------- *)
(* dwDiagnosticWord_01: Operational Status & FSM Stage *)
dwDiagnosticWord_01 := 16#00000000;
IF bSystemReady THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000001; END_IF;
IF bCycleInProgress THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000002; END_IF;
IF bCycleCompleted THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000004; END_IF;
IF bGeneralFault THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000008; END_IF;
IF bEmergencyHalted THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000010; END_IF;
IF bBeadLock_LH_Clamped THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000020; END_IF;
IF bBeadLock_RH_Clamped THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000040; END_IF;
IF bTransferRing_VacuumLocked THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000080; END_IF;
dwDiagnosticWord_01 := dwDiagnosticWord_01 OR SHL(INT_TO_DWORD(iFSM_State), 8);
dwDiagnosticWord_01 := dwDiagnosticWord_01 OR SHL(INT_TO_DWORD(iDrum1_TMR_HealthState), 16);
dwDiagnosticWord_01 := dwDiagnosticWord_01 OR SHL(INT_TO_DWORD(iShapingPress_TMR_HealthState), 20);

(* dwDiagnosticWord_02: Warning & High Alarms *)
dwDiagnosticWord_02 := 16#00000000;
IF bAlarm_ShapingPressure_H THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000001; END_IF;
IF bAlarm_ShapingPressure_L THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000002; END_IF;
IF bDrum1_Resolver_Discrepancy THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000004; END_IF;
IF bShapingPress_Discrepancy THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000008; END_IF;
IF bSplice_Discrepancy THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000010; END_IF;
IF bStitcher_Discrepancy THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000020; END_IF;
IF bAlarm_FestoonTension_HH THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000040; END_IF;
IF bAlarm_FestoonTension_LL THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000080; END_IF;

(* dwDiagnosticWord_03: Critical High-High & Low-Low Trip Alarms *)
dwDiagnosticWord_03 := 16#00000000;
IF bAlarm_SpliceOverlap_HH THEN dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000001; END_IF;
IF bAlarm_SpliceOverlap_LL THEN dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000002; END_IF;
IF bAlarm_ShapingPressure_HH THEN dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000004; END_IF;
IF bAlarm_ShapingPressure_LL THEN dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000008; END_IF;
IF bAlarm_TransferRingRunout_HH THEN dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000010; END_IF;
IF bAlarm_StitcherForce_HH THEN dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000020; END_IF;
IF bAlarm_StitcherForce_LL THEN dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000040; END_IF;
IF bAlarm_TMR_BankFailure THEN dwDiagnosticWord_03 := dwDiagnosticWord_03 OR 16#00000080; END_IF;

(* dwDiagnosticWord_04: Laser Metrology & Quality Inspection *)
dwDiagnosticWord_04 := 16#00000000;
IF bSpliceQuality_Passed THEN dwDiagnosticWord_04 := dwDiagnosticWord_04 OR 16#00000001; END_IF;
IF bSpliceOverlap_InRange THEN dwDiagnosticWord_04 := dwDiagnosticWord_04 OR 16#00000002; END_IF;
IF bDogEar_Defect_Detected THEN dwDiagnosticWord_04 := dwDiagnosticWord_04 OR 16#00000004; END_IF;
IF rCalculated_Runout_Radial_mm > 0.65 THEN dwDiagnosticWord_04 := dwDiagnosticWord_04 OR 16#00000008; END_IF;
IF rCalculated_Harmonic_1H_mm > 0.35 THEN dwDiagnosticWord_04 := dwDiagnosticWord_04 OR 16#00000010; END_IF;
IF rCalculated_Harmonic_2H_mm > 0.35 THEN dwDiagnosticWord_04 := dwDiagnosticWord_04 OR 16#00000020; END_IF;

END_FUNCTION_BLOCK
""")

    return "".join(parts)

print("generate_code function compiled successfully.")

PROMPT_TEXT = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Plastics, Rubber & Tire Manufacturing: Automated Dual-Drum Steel-Belted Radial Passenger/Truck Tire Building Machine (TBM) with Dynamic Carcass Shaping Bladder & Laser Centering**

Task: Implement the production-grade Function Block FB_Plastics_RadialTire_BuildingMachine_DualDrum governing:
1. High-precision dual-drum tire building machine: Drum 1 Carcass Building Drum (inner liner, body ply, chafer strips, sidewall extrusion), Drum 2 Breaker/Belt & Tread Drum (steel belt plies 1 & 2, nylon cap ply, extruded rubber tread).
2. Multi-axis dynamic transfer ring: high-speed linear gantry with precision pneumatic/servo segments picking the assembled belt/tread package from Drum 2 and transferring it coaxially over the carcass on Drum 1 (+/- 0.1 mm concentricity).
3. In-line laser line triangulation sensors: continuous 3D profile measurement detecting component edge position, splice overlap width (1.5 to 3.5 mm), and centering offsets (Delta X, Delta Y, Delta Theta) on high-speed rotating drums.
4. Dynamic carcass shaping: pneumatic bladder expansion and mechanical bead-lock slide mechanism expanding the flat carcass into toroidal shape (internal shaping pressure 0.5 to 2.5 bar) while twin stitching rollers roll down the rubber plies with programmable force vectors.
5. Dual-side bead setting mechanism: magnetic/pneumatic bead rings placing bead wire cores with high-precision bead distance monitoring.
6. High-speed servo servicer festoons: continuous rubber web tension control with dancer arm potentiometers preventing elastomeric stretch deformation.
7. Discrete State-Space Model (16x16 state matrix A, 16x8 B, C, D) incorporating viscoelastic rubber stress relaxation, pneumatic shaping bladder volume-pressure dynamics, drum servo mechanical compliance, and stitcher contact force kinetics.
8. Receding-horizon MPC for synchronized dual-drum rotary speeds, transfer ring positioning, and dynamic stitcher force vector profiling.
9. 2oo3 Triple Modular Redundancy (TMR) voting across drum optical resolvers, shaping air pressure transducers, laser edge detection sensors, and stitcher load cells with bumpless degradation.
10. 12-Stage Operational FSM (Drum 1 Inner Liner & Body Ply Winding, Splice Laser Metrology Verification, Dual Bead Core Setting & Mechanical Lock, Bladder Inflation Toroidal Shaping, Drum 2 Steel Belt 1 & 2 Application, Spiral Nylon Cap Ply High-Speed Winding, Extruded Tread Application & Ultrasonic Splice Cut, Belt/Tread Package Transfer Ring Pick, Coaxial Assembly Stitching on Shaped Carcass, High-Pressure Stitcher Roll-Down, Green Tire Discharge to Curing Press Pallet, Emergency Bladder Deflate & Drum Collapse).
11. ISA-18.2 multi-tiered alarm matrix (Splice overlap width out-of-tolerance HH reject, shaping bladder burst risk, transfer ring alignment deviation, stitcher force shortfall, safety area scanner breach) with bit-packed telemetry DWORDs.

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st.
2. EXACT AST PARITY: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
3. First line: FUNCTION_BLOCK FB_Plastics_RadialTire_BuildingMachine_DualDrum, Last line: END_FUNCTION_BLOCK.
4. Total length >= 55,000 characters (zero placeholders, zero truncation comments)."""

def assemble_dataset():
    code = generate_code()
    assistant_content = f"```iec-st\n{code}```"
    
    record = {
        "messages": [
            {"role": "user", "content": PROMPT_TEXT},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    target_file = "data/swarm_raw/agent_8a201b9f.json"
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated and wrote {target_file}")
    print(f"Assistant content character count: {len(assistant_content)}")

if __name__ == "__main__":
    assemble_dataset()

