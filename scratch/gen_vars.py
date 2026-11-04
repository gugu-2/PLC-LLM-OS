# VAR ... END_VAR declarations for FB_Mining_SAG_BallMill_GrindingCircuit

def get_vars():
    return """VAR
    (* ========================================================================================= *)
    (* INTERNAL CYBER-PHYSICAL STATE REGISTERS, VECTORS, MATRICES & CONTROL MEMORY              *)
    (* ========================================================================================= *)
    bFirstScanInitialized           : BOOL := FALSE;    (* Memory allocation and matrix init cold-start flag *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. SAG MILL & TWIN BALL MILL MECHANICAL GEOMETRY, VOLUMES & KINEMATICS                    *)
    (* ----------------------------------------------------------------------------------------- *)
    rSagDiameterInsideLiners_m      : REAL := 12.192;   (* 40.0 ft SAG mill internal diameter [m] *)
    rSagLengthInsideLiners_m        : REAL := 7.620;    (* 25.0 ft SAG mill effective grinding length [m] *)
    rSagInternalVolume_m3           : REAL := 889.65;   (* Total cylindrical internal volume [m3] *)
    rSagCriticalSpeed_rpm           : REAL := 12.112;   (* Theoretical centrifuging speed N_c [rpm] *)
    rSagShellTareMass_tons          : REAL := 640.00;   (* Structural mass of shell, trunnions and liners [t] *)
    rSagNominalBallCharge_tons      : REAL := 240.00;   (* 15.0% volume filling of 125 mm forged steel balls [t] *)
    rSagMaxAllowableMass_tons       : REAL := 1550.00;  (* Trunnion bearing and shell structural limit [t] *)
    rSagMinBedProtectionMass_tons   : REAL := 800.00;   (* Minimum charge mass to protect liners from impact [t] *)

    (* Trunnion Hydrostatic Bearing Jacking Pad Calibration Factors *)
    rFeedTrunnionPadArea_m2         : REAL := 0.4150;   (* Feed trunnion 4-pad effective jacking lift area [m2] *)
    rDischTrunnionPadArea_m2        : REAL := 0.4450;   (* Discharge trunnion 4-pad effective jacking area [m2] *)
    rFeedLiftFactor_tons_per_bar    : REAL := 4.2304;   (* Metric tons lift per bar oil pressure on feed trunnion *)
    rDischLiftFactor_tons_per_bar   : REAL := 4.5362;   (* Metric tons lift per bar oil pressure on discharge trunnion *)
    rTrunnionTareOffset_tons        : REAL := 148.50;   (* Static tare offset calibration parameter [t] *)
    rHydrodynamicLiftWedgeSlope     : REAL := 6.4500;   (* Dynamic hydrodynamic film pressure wedge slope [t/rpm] *)

    (* Secondary Twin Ball Mills Geometry *)
    rBallMill1_Diameter_m           : REAL := 7.925;    (* 26.0 ft ball mill #1 internal diameter [m] *)
    rBallMill1_Length_m             : REAL := 12.192;   (* 40.0 ft ball mill #1 length [m] *)
    rBallMill1_BallMass_tons        : REAL := 320.00;   (* Ball Mill #1 steel ball charge (75 mm balls) [t] *)
    rBallMill2_Diameter_m           : REAL := 7.925;    (* 26.0 ft ball mill #2 internal diameter [m] *)
    rBallMill2_Length_m             : REAL := 12.192;   (* 40.0 ft ball mill #2 length [m] *)
    rBallMill2_BallMass_tons        : REAL := 320.00;   (* Ball Mill #2 steel ball charge (75 mm balls) [t] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY TOLERANCES & VOTED REGISTERS          *)
    (* ----------------------------------------------------------------------------------------- *)
    c_rTol_TrunnionLift_bar         : REAL := 2.50;     (* Max allowable deviation between trunnion pressure cells [bar] *)
    c_rTol_MotorPower_MW            : REAL := 0.45;     (* Max allowable deviation between motor power transducers [MW] *)
    c_rTol_MotorSpeed_rpm           : REAL := 0.08;     (* Max allowable deviation between speed tachometers [rpm] *)
    c_rTol_ShellAcoustic_dB         : REAL := 3.50;     (* Max allowable deviation between acoustic microphone signals [dB] *)
    c_rTol_SumpLevel_pct            : REAL := 3.00;     (* Max allowable deviation between sump level transmitters [%] *)
    c_rTol_FeedDensity_SG           : REAL := 0.035;    (* Max allowable deviation between gamma density gauges [t/m3] *)
    c_rTol_ManifoldPress_kPa        : REAL := 6.00;     (* Max allowable deviation between cyclone pressure cells [kPa] *)
    c_rTol_ProductP80_um            : REAL := 4.00;     (* Max allowable deviation between ultrasonic P80 channels [um] *)
    c_rDiscrepancyTripTime_s        : REAL := 0.500;    (* Discrepancy accumulation qualification timer threshold [s] *)

    (* Filtered / 2oo3 Voted Process Variables *)
    rVoted_FeedTrunnionLift_bar     : REAL := 182.50;
    rVoted_DischTrunnionLift_bar    : REAL := 194.20;
    rVoted_MotorPower_MW            : REAL := 22.85;
    rVoted_MotorSpeed_rpm           : REAL := 9.18;
    rVoted_MotorTorque_pct          : REAL := 78.40;
    rVoted_ShellAcousticToe_dB      : REAL := 74.20;
    rVoted_ShellAcousticHighFreq_dB : REAL := 26.50;
    rVoted_ShellAcousticLowFreq_dB  : REAL := 84.80;
    rVoted_SumpLevel_pct            : REAL := 62.40;
    rVoted_CycloneFeedDensity_SG    : REAL := 1.585;
    rVoted_CycloneManifoldPress_kPa : REAL := 105.40;
    rVoted_ProductP80_um            : REAL := 75.20;
    rVoted_ProductDensity_SG        : REAL := 1.285;

    (* 2oo3 Triplet Pairwise Difference & Fault Timers *)
    rDiff_FeedTrunnion_AB : REAL := 0.0; rDiff_FeedTrunnion_BC : REAL := 0.0; rDiff_FeedTrunnion_AC : REAL := 0.0;
    rTimer_FeedTrunnion_Disc : REAL := 0.0; bFault_FeedTrunnion : BOOL := FALSE;

    rDiff_DischTrunnion_AB : REAL := 0.0; rDiff_DischTrunnion_BC : REAL := 0.0; rDiff_DischTrunnion_AC : REAL := 0.0;
    rTimer_DischTrunnion_Disc : REAL := 0.0; bFault_DischTrunnion : BOOL := FALSE;

    rDiff_MotorPower_AB : REAL := 0.0; rDiff_MotorPower_BC : REAL := 0.0; rDiff_MotorPower_AC : REAL := 0.0;
    rTimer_MotorPower_Disc : REAL := 0.0; bFault_MotorPower : BOOL := FALSE;

    rDiff_MotorSpeed_AB : REAL := 0.0; rDiff_MotorSpeed_BC : REAL := 0.0; rDiff_MotorSpeed_AC : REAL := 0.0;
    rTimer_MotorSpeed_Disc : REAL := 0.0; bFault_MotorSpeed : BOOL := FALSE;

    rDiff_AcousticToe_AB : REAL := 0.0; rDiff_AcousticToe_BC : REAL := 0.0; rDiff_AcousticToe_AC : REAL := 0.0;
    rTimer_AcousticToe_Disc : REAL := 0.0; bFault_AcousticToe : BOOL := FALSE;

    rDiff_AcousticHighFreq_AB : REAL := 0.0; rDiff_AcousticHighFreq_BC : REAL := 0.0; rDiff_AcousticHighFreq_AC : REAL := 0.0;
    rTimer_AcousticHighFreq_Disc : REAL := 0.0; bFault_AcousticHighFreq : BOOL := FALSE;

    rDiff_SumpLevel_AB : REAL := 0.0; rDiff_SumpLevel_BC : REAL := 0.0; rDiff_SumpLevel_AC : REAL := 0.0;
    rTimer_SumpLevel_Disc : REAL := 0.0; bFault_SumpLevel : BOOL := FALSE;

    rDiff_FeedDensity_AB : REAL := 0.0; rDiff_FeedDensity_BC : REAL := 0.0; rDiff_FeedDensity_AC : REAL := 0.0;
    rTimer_FeedDensity_Disc : REAL := 0.0; bFault_FeedDensity : BOOL := FALSE;

    rDiff_ProductP80_AB : REAL := 0.0; rDiff_ProductP80_BC : REAL := 0.0; rDiff_ProductP80_AC : REAL := 0.0;
    rTimer_ProductP80_Disc : REAL := 0.0; bFault_ProductP80 : BOOL := FALSE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. DISCRETE 8x8 CYBER-PHYSICAL STATE-SPACE MATRICES & VECTORS                             *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Sampling period Ts = 50 ms. Discrete State Vector x:
       x[1] = Total SAG mill charge mass [tons] (800..1500 t)
       x[2] = Internal slurry liquid-solid volumetric hold-up [m3] (150..350 m3)
       x[3] = Dynamic rock/ball charge toe impact angle [deg] (35..50 deg)
       x[4] = Gearless ring motor gross electrical power draw [MW] (15..28 MW)
       x[5] = Cyclone feed sump slurry level [%] (30..85%)
       x[6] = Final cyclone overflow slurry density [t/m3] (1.18..1.35 t/m3)
       x[7] = Twin ball mill recirculating circulating load mass [t/h] (1200..2600 t/h)
       x[8] = Final flotation product fineness 80% passing size P80 [um] (65..85 um)
    *)
    aMatrix_A                       : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Dynamics Transition Matrix A *)
    aMatrix_B                       : ARRAY[1..8, 1..8] OF REAL; (* Discrete Actuator Input Gain Matrix B *)
    aMatrix_C                       : ARRAY[1..8, 1..8] OF REAL; (* Discrete Sensor Output Measurement Matrix C *)
    aMatrix_D                       : ARRAY[1..8, 1..8] OF REAL; (* Discrete Direct Feedthrough Matrix D *)

    aState_x                        : ARRAY[1..8] OF REAL;       (* Current Discrete State Vector x[k] *)
    aState_x_next                   : ARRAY[1..8] OF REAL;       (* Projected Discrete State Vector x[k+1] *)
    aState_x_ref                    : ARRAY[1..8] OF REAL;       (* Target Steady-State Reference Vector x_ref *)
    aControl_u                      : ARRAY[1..8] OF REAL;       (* Current Actuator Command Vector u[k] *)
    aControl_u_prev                 : ARRAY[1..8] OF REAL;       (* Previous Cycle Actuator Vector u[k-1] *)
    aDelta_u                        : ARRAY[1..8] OF REAL;       (* Actuator Rate-of-Change Vector Delta_u[k] *)
    aOutput_y                       : ARRAY[1..8] OF REAL;       (* Observed Output Vector y[k] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 4. MODEL PREDICTIVE CONTROL (MPC) HORIZON VECTORS, WEIGHTS & CONSTRAINTS                  *)
    (* ----------------------------------------------------------------------------------------- *)
    c_iMpcPredictionHorizon_Np      : INT := 5;                  (* Receding-Horizon Prediction Steps (Np = 5 * 50ms = 250 ms) *)
    c_iMpcControlHorizon_Nu         : INT := 3;                  (* Receding-Horizon Control Steps (Nu = 3) *)
    c_iMpcMaxIterations             : INT := 12;                 (* Maximum KKT Projected Gradient Descent Iterations *)

    aWeights_Q                      : ARRAY[1..8] OF REAL;       (* State Error Quadratic Penalty Diagonal Matrix Q *)
    aWeights_R                      : ARRAY[1..8] OF REAL;       (* Actuator Rate-of-Change Penalty Diagonal Matrix R *)
    aWeights_P                      : ARRAY[1..8] OF REAL;       (* Terminal State Error Quadratic Penalty Matrix P *)

    aMpc_X_pred                     : ARRAY[1..5, 1..8] OF REAL; (* Multi-Step State Trajectory Prediction Array *)
    aMpc_U_cand                     : ARRAY[1..3, 1..8] OF REAL; (* Candidate Actuator Control Trajectory Array *)
    aMpc_Grad_u                     : ARRAY[1..8] OF REAL;       (* Objective Function Gradient with respect to u[0] *)

    (* Actuator Physical Clamping Limits *)
    aMin_u                          : ARRAY[1..8] OF REAL;       (* Minimum Actuator Bounds *)
    aMax_u                          : ARRAY[1..8] OF REAL;       (* Maximum Actuator Bounds *)
    aMaxSlewRate_u                  : ARRAY[1..8] OF REAL;       (* Maximum Allowable Slew Rate per Execution Scan *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 5. CYBER-PHYSICAL OBSERVER INTERMEDIATE REGISTERS                                         *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Dynamic Trunnion Hydrostatic Lift & Viscosity Observer *)
    rOilDynamicViscosity_Pa_s       : REAL := 0.085;    (* ISO VG 320 lubricating oil dynamic viscosity [Pa*s] *)
    rBearingOilTempAvg_degC         : REAL := 56.50;    (* Average trunnion bearing metal temperature [deg C] *)
    rDynamicFilmThickness_Feed_um   : REAL := 141.20;   (* Feed bearing dynamic oil film thickness [um] *)
    rDynamicFilmThickness_Disch_um  : REAL := 143.80;   (* Discharge bearing dynamic oil film thickness [um] *)
    rRawEstimatedMass_tons          : REAL := 1285.50;  (* Unfiltered reconstructed live mill charge weight [t] *)

    (* Shell Acoustic Trajectory & Direct Impact Observer *)
    rAcousticImpactSeverity_dB      : REAL := 26.50;    (* High-frequency impact noise power [dB] *)
    rDirectLinerImpactEnergy_pct    : REAL := 12.50;    (* Percentage of impact energy striking bare liner *)
    rReconstructedToeAngle_deg      : REAL := 42.80;    (* Reconstructed charge toe angle [deg] *)
    rReconstructedShoulderAngle_deg : REAL := 318.50;   (* Reconstructed charge shoulder departure angle [deg] *)
    rBallTrajectoryInitialVel_ms    : REAL := 9.42;     (* Tangential departure velocity of cataracts [m/s] *)
    rBallImpactVelocity_ms          : REAL := 11.45;    (* Free-fall parabolic impact velocity in the toe bed [m/s] *)

    (* Frozen Charge Detection Registers *)
    rMillRotationalDisplacement_deg : REAL := 0.00;     (* Integrated cumulative mill rotation angle [deg] *)
    rAccumulatedTorqueWork_kJ       : REAL := 0.00;     (* Integrated mechanical torque work during rotation [kJ] *)
    rFrozenChargeAcousticBaseline_dB: REAL := 0.00;     (* Acoustic noise baseline during mill starting [dB] *)
    tFrozenChargeScanTimer_s        : REAL := 0.00;     (* Frozen charge qualification time accumulator [s] *)
    bFrozenChargePotentialDetected  : BOOL := FALSE;    (* Preliminary frozen charge indicator latch *)

    (* Plitt Hydrocyclone Cluster Observer *)
    rSlurryVolumetricSolids_Cv      : REAL := 0.385;    (* Volumetric solids concentration fraction C_v *)
    rSlurryDynamicViscosity_cP      : REAL := 8.45;     (* Slurry apparent dynamic viscosity [cP] *)
    rPlittCutSize_d50c_um           : REAL := 74.80;    (* Plitt corrected classification cut size d50c [um] *)
    rPlittWaterSplitRecovery_Rf     : REAL := 0.342;    (* Water recovery fraction to hydrocyclone underflow *)
    rPlittSharpnessIndex_m          : REAL := 2.65;     (* Plitt classification sharpness index m *)
    rClusterTotalSlurryFlow_m3h     : REAL := 4650.00;  (* Total feed slurry volumetric flow [m3/h] *)
    rPredictedManifoldPress_kPa     : REAL := 105.40;   (* Hydraulic predicted manifold pressure [kPa] *)
    arCycloneOperatingHours         : ARRAY[1..16] OF REAL := [16(1250.0)]; (* Cumulative operating hours per cyclone *)
    iCycloneRotationPointer         : INT := 1;         (* Wear-leveling staging rotational pointer index *)
    rCycloneSwitchingDelayTimer_s   : REAL := 0.00;     (* Minimum dwell time between opening/closing valves [s] *)

    (* In-Line Ultrasonic Attenuation Particle Size Spectrometer Inversion *)
    rAttenuationCoeff_2MHz_dB_cm    : REAL := 1.25;     (* Ultrasonic acoustic attenuation at 2.0 MHz [dB/cm] *)
    rAttenuationCoeff_10MHz_dB_cm   : REAL := 4.82;     (* Ultrasonic acoustic attenuation at 10.0 MHz [dB/cm] *)
    rAttenuationCoeff_30MHz_dB_cm   : REAL := 14.65;    (* Ultrasonic acoustic attenuation at 30.0 MHz [dB/cm] *)
    rInversionResidualError         : REAL := 0.008;    (* ECAH particle size distribution fitting residual error *)
    rCalculatedP50_microns          : REAL := 44.50;    (* Estimated 50% passing particle size [um] *)
    rCalculatedP80_microns          : REAL := 75.20;    (* Estimated 80% passing particle size P80 [um] *)
    rCalculatedP95_microns          : REAL := 115.40;   (* Estimated 95% passing particle size [um] *)

    (* Pebble Recirculation Mass Balance *)
    rPebbleSurgeBinLevel_pct        : REAL := 54.20;    (* Secondary pebble crusher surge bin live level [%] *)
    rPebbleMassExtractionRate_tph   : REAL := 380.00;   (* Pebble port mass extraction rate from SAG trommel [t/h] *)
    rPebbleCrusherMotorTorque_pct   : REAL := 68.40;    (* Cone crusher eccentric shaft load [%] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 6. CASCADE PID REGULATORY CONTROLLERS                                                     *)
    (* ----------------------------------------------------------------------------------------- *)
    (* PID 1: Sump Level to Cyclone Pump Speed *)
    rPid1_Kp : REAL := 0.85; rPid1_Ti : REAL := 45.0; rPid1_Td : REAL := 2.5;
    rPid1_Error : REAL := 0.0; rPid1_Integral : REAL := 55.0; rPid1_Derivative : REAL := 0.0;
    rPid1_Output : REAL := 74.20; rPid1_PrevError : REAL := 0.0;

    (* PID 2: Cyclone Feed Density to Sump Dilution Water Valve *)
    rPid2_Kp : REAL := 1.20; rPid2_Ti : REAL := 30.0; rPid2_Td : REAL := 1.5;
    rPid2_Error : REAL := 0.0; rPid2_Integral : REAL := 42.5; rPid2_Derivative : REAL := 0.0;
    rPid2_Output : REAL := 42.50; rPid2_PrevError : REAL := 0.0;

    (* PID 3: Overflow P80 to Cyclone Cluster Pressure Setpoint *)
    rPid3_Kp : REAL := 0.65; rPid3_Ti : REAL := 60.0; rPid3_Td : REAL := 4.0;
    rPid3_Error : REAL := 0.0; rPid3_Integral : REAL := 105.0; rPid3_Derivative : REAL := 0.0;
    rPid3_Output : REAL := 105.40; rPid3_PrevError : REAL := 0.0;

    (* PID 4: Acoustic Toe Angle to SAG Mill Speed Trim *)
    rPid4_Kp : REAL := 0.045; rPid4_Ti : REAL := 25.0; rPid4_Td : REAL := 1.2;
    rPid4_Error : REAL := 0.0; rPid4_Integral : REAL := 0.0; rPid4_Derivative : REAL := 0.0;
    rPid4_Output : REAL := 0.00; rPid4_PrevError : REAL := 0.0;

    (* PID 5: SAG Mill Power Draw to Feeder Throughput Lead *)
    rPid5_Kp : REAL := 0.75; rPid5_Ti : REAL := 90.0; rPid5_Td : REAL := 5.0;
    rPid5_Error : REAL := 0.0; rPid5_Integral : REAL := 85.5; rPid5_Derivative : REAL := 0.0;
    rPid5_Output : REAL := 85.50; rPid5_PrevError : REAL := 0.0;

    (* PID 6: Trunnion Total Weight to Feed Water Ratio *)
    rPid6_Kp : REAL := 0.55; rPid6_Ti : REAL := 40.0; rPid6_Td : REAL := 2.0;
    rPid6_Error : REAL := 0.0; rPid6_Integral : REAL := 1150.0; rPid6_Derivative : REAL := 0.0;
    rPid6_Output : REAL := 1150.00; rPid6_PrevError : REAL := 0.0;

    (* PID 7 & 8: Secondary Twin Ball Mill Feed Split Balancing *)
    rPid7_Kp : REAL := 0.50; rPid7_Ti : REAL := 50.0; rPid7_Error : REAL := 0.0;
    rPid7_Integral : REAL := 1850.0; rPid7_Output : REAL := 1850.00; rPid7_PrevError : REAL := 0.0;

    rPid8_Kp : REAL := 0.50; rPid8_Ti : REAL := 50.0; rPid8_Error : REAL := 0.0;
    rPid8_Integral : REAL := 1850.0; rPid8_Output : REAL := 1850.00; rPid8_PrevError : REAL := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* 7. DETERMINISTIC 12-STAGE OPERATIONAL FSM TIMERS & REGISTERS                              *)
    (* ----------------------------------------------------------------------------------------- *)
    iState                          : INT := 1;                  (* Active operational state index (1..12) *)
    iPreviousState                  : INT := 1;                  (* Previous operational state index *)
    rStateTimer_s                   : REAL := 0.00;              (* Active state elapsed time monitor [s] *)
    rLubePermissiveTimer_s          : REAL := 0.00;              (* High-pressure oil lift pressure soak timer [s] *)
    rInchingDisengageTimer_s        : REAL := 0.00;              (* Inching drive disengagement confirm timer [s] *)
    rMillRampTimer_s                : REAL := 0.00;              (* Ring motor acceleration ramp time accumulator [s] *)
    rWaterLeadTimer_s               : REAL := 0.00;              (* Process water pre-wetting lead timer [s] *)
    rFeederStartRampTimer_s         : REAL := 0.00;              (* Coarse ore feeder rate ramping timer [s] *)
    rAcousticOptimizeTimer_s        : REAL := 0.00;              (* Toe trajectory stabilization timer [s] *)
    rPebbleCutInTimer_s             : REAL := 0.00;              (* Pebble recycle conveyor cut-in timer [s] *)
    rBallMillBalanceTimer_s         : REAL := 0.00;              (* Twin ball mill feed balance timer [s] *)
    rCycloneSequenceTimer_s         : REAL := 0.00;              (* Hydrocyclone staging stabilization timer [s] *)
    rOverfillCutbackTimer_s         : REAL := 0.00;              (* Over-filling feed cutback debounce timer [s] *)
    rGrindOutFlushTimer_s           : REAL := 0.00;              (* Controlled charge flush & grind-out duration timer [s] *)
    rFrozenChargeTripLatchTimer_s   : REAL := 0.00;              (* Emergency frozen charge trip holding timer [s] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 8. ISA-18.2 MULTI-TIERED ALARM THRESHOLDS, HYSTERESIS & SCRATCH REGISTERS                 *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Thresholds for 16 primary process channels *)
    c_rTrunnionLift_LL_bar          : REAL := 140.0; c_rTrunnionLift_L_bar  : REAL := 155.0;
    c_rTrunnionLift_H_bar           : REAL := 215.0; c_rTrunnionLift_HH_bar : REAL := 235.0;

    c_rBabbittTemp_H_degC           : REAL := 68.0;  c_rBabbittTemp_HH_degC : REAL := 76.0;
    c_rMotorPower_H_MW              : REAL := 26.5;  c_rMotorPower_HH_MW    : REAL := 28.5;
    c_rStatorTemp_H_degC            : REAL := 105.0; c_rStatorTemp_HH_degC  : REAL := 125.0;
    c_rAirgap_LL_mm                 : REAL := 9.5;   c_rAirgap_L_mm         : REAL := 11.5;

    c_rShellImpact_H_dB             : REAL := 40.0;  c_rShellImpact_HH_dB   : REAL := 50.0;
    c_rToeAngle_LL_deg              : REAL := 32.0;  c_rToeAngle_HH_deg     : REAL := 54.0;

    c_rChargeWeight_LL_tons         : REAL := 780.0; c_rChargeWeight_L_tons : REAL := 850.0;
    c_rChargeWeight_H_tons          : REAL := 1450.0;c_rChargeWeight_HH_tons: REAL := 1550.0;

    c_rSumpLevel_LL_pct             : REAL := 18.0;  c_rSumpLevel_L_pct     : REAL := 30.0;
    c_rSumpLevel_H_pct              : REAL := 80.0;  c_rSumpLevel_HH_pct    : REAL := 90.0;

    c_rFeedDensity_L_SG             : REAL := 1.450; c_rFeedDensity_H_SG    : REAL := 1.720;
    c_rProductP80_L_um              : REAL := 65.0;  c_rProductP80_H_um     : REAL := 85.0;  c_rProductP80_HH_um : REAL := 95.0;

    c_rAlarmHysteresis_pct          : REAL := 2.50;  (* Deadband hysteresis [% of span] to eliminate chatter *)

    (* Loop and Math Counters *)
    iLoopRow                        : INT := 1;
    iLoopCol                        : INT := 1;
    iMpcStep                        : INT := 1;
    iMpcIter                        : INT := 1;
    iCycloneIdx                     : INT := 1;
    rScratchSum                     : REAL := 0.00;
    rScratchTerm                    : REAL := 0.00;
    rScratchGrad                    : REAL := 0.00;
    rScratchCost                    : REAL := 0.00;
    bStateTransitionPermissive      : BOOL := FALSE;
END_VAR
"""
