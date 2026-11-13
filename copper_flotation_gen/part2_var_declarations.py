# copper_flotation_gen/part2_var_declarations.py

def get_var_declarations():
    return """VAR
    (* Execution Control & Initialization Flags *)
    bFirstScanDone                  : BOOL := FALSE;    (* First Scan Initialization Completed Flag [-] *)
    tScanCycleTime_s                : REAL := 0.020;    (* Discrete Task Execution Sample Period [s] *)
    iCycleCounter                   : DINT := 0;        (* Rolling Scan Execution Cycle Counter [-] *)

    (* Discrete State-Space Cyber-Physical Matrices (8 States x 6 Inputs) *)
    matA                            : ARRAY[0..7, 0..7] OF REAL; (* State Transition Dynamic Matrix A (8x8) [-] *)
    matB                            : ARRAY[0..7, 0..5] OF REAL; (* Actuator Input Mapping Matrix B (8x6) [-] *)
    matC                            : ARRAY[0..5, 0..7] OF REAL; (* Measurement Output Mapping Matrix C (6x8) [-] *)
    matD                            : ARRAY[0..5, 0..5] OF REAL; (* Direct Feedthrough Matrix D (6x6) [-] *)
    matL                            : ARRAY[0..7, 0..5] OF REAL; (* Luenberger Observer Innovation Gain L (8x6) [-] *)
    matM_hydro                      : ARRAY[0..5, 0..5] OF REAL; (* Inter-Cell Dart Valve Hydrostatic Cross-Coupling [-] *)

    (* State Vectors & Estimation Buffers *)
    vecX                            : ARRAY[0..7] OF REAL; (* Cyber-Physical Plant True/Predicted State Vector [-] *)
    vecX_hat                        : ARRAY[0..7] OF REAL; (* Luenberger Filtered State Estimate Vector [-] *)
    vecX_pred                       : ARRAY[0..7] OF REAL; (* One-Step-Ahead Observer State Prediction Vector [-] *)
    vecY_meas                       : ARRAY[0..5] OF REAL; (* Voted Sensor Measurement Vector [-] *)
    vecY_hat                        : ARRAY[0..5] OF REAL; (* Observer Estimated Measurement Vector [-] *)
    vecInnov                        : ARRAY[0..5] OF REAL; (* Innovation Estimation Residual Vector (y - y_hat) [-] *)
    vecU                            : ARRAY[0..5] OF REAL; (* Current Optimal Actuator Command Vector [-] *)
    vecU_prev                       : ARRAY[0..5] OF REAL; (* Previous Execution Cycle Actuator Command Vector [-] *)
    vecU_rate                       : ARRAY[0..5] OF REAL; (* Instantaneous Actuator Slew Rate Vector [%/s] *)
    vecD_feed                       : ARRAY[0..3] OF REAL; (* Measured Slurry Feed Inflow Disturbance Vector [-] *)
    vecX_target                     : ARRAY[0..7] OF REAL; (* Optimal Dynamic State Trajectory Setpoint Vector [-] *)
    vecU_target                     : ARRAY[0..5] OF REAL; (* Actuator Nominal Steady-State Setpoint Vector [-] *)

    (* Model Predictive Control (MPC) Cost Weighting & Sizing Arrays *)
    vecQ_weight                     : ARRAY[0..7] OF REAL; (* Quadratic State Tracking Penalty Diagonal Weights [-] *)
    vecR_weight                     : ARRAY[0..5] OF REAL; (* Actuator Effort Penalty Diagonal Weights [-] *)
    vecR_delta_weight               : ARRAY[0..5] OF REAL; (* Actuator Slew Rate-of-Change Penalty Weights [-] *)
    vecP_terminal                   : ARRAY[0..7] OF REAL; (* Terminal Horizon State Penalty Diagonal Weights [-] *)
    vecU_min                        : ARRAY[0..5] OF REAL; (* Actuator Absolute Physical Lower Saturation Bounds [%] *)
    vecU_max                        : ARRAY[0..5] OF REAL; (* Actuator Absolute Physical Upper Saturation Bounds [%] *)
    vecU_slewMax                    : ARRAY[0..5] OF REAL; (* Actuator Maximum Slew Rate Limit Per Execution Cycle [%] *)

    (* Receding-Horizon Prediction & Gradient Descent Workspace (Horizon N=5, Iterations=6) *)
    trajX_mpc                       : ARRAY[0..5, 0..7] OF REAL; (* MPC State Trajectory Over Horizon N=5 [-] *)
    trajU_mpc                       : ARRAY[0..4, 0..5] OF REAL; (* MPC Control Trajectory Over Horizon N=5 [-] *)
    trajU_cand                      : ARRAY[0..4, 0..5] OF REAL; (* PGD Candidate Actuator Update Trajectory [-] *)
    trajGrad_J                      : ARRAY[0..4, 0..5] OF REAL; (* Analytical Gradient Vector of Cost w.r.t U [-] *)
    rPgd_StepSize                   : REAL := 0.035;    (* Projected Gradient Descent Learning Step Size Gamma [-] *)
    rMpc_AccumulatedCost            : REAL := 0.0;      (* Unrolled MPC Quadratic Objective Cost Function Value [-] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Sensor Channels *)
    (* Channel Group 1: Rougher Cell 1 Pulp Level *)
    rPulpLevel_Cell1_Voted          : REAL := 1100.0;   (* 2oo3 Voted Cell 1 Slurry Pulp Level [mm] *)
    bPulpLevel_Cell1_HealthA        : BOOL := TRUE;     (* Channel 1A Ultrasonic Transmitter Healthy [-] *)
    bPulpLevel_Cell1_HealthB        : BOOL := TRUE;     (* Channel 1B Float Transmitter Healthy [-] *)
    bPulpLevel_Cell1_HealthC        : BOOL := TRUE;     (* Channel 1C Radar Transmitter Healthy [-] *)
    rPulpLevel_Cell1_Disc_AB_ms     : REAL := 0.0;      (* Channel 1A vs 1B Discrepancy Timer [ms] *)
    rPulpLevel_Cell1_Disc_BC_ms     : REAL := 0.0;      (* Channel 1B vs 1C Discrepancy Timer [ms] *)
    rPulpLevel_Cell1_Disc_CA_ms     : REAL := 0.0;      (* Channel 1C vs 1A Discrepancy Timer [ms] *)
    bPulpLevel_Cell1_Degraded       : BOOL := FALSE;    (* Cell 1 Level Operating on Degraded 2oo2 Voting [-] *)
    bPulpLevel_Cell1_SingleFallback : BOOL := FALSE;    (* Cell 1 Level Operating on Single Channel [-] *)
    bPulpLevel_Cell1_Trip           : BOOL := FALSE;    (* Cell 1 Level Sensor Complete Failure Trip [-] *)

    (* Channel Group 1 Mid: Cleaner Cell 6 Pulp Level *)
    rPulpLevel_Cell6_Voted          : REAL := 1050.0;   (* 2oo3 Voted Cell 6 Slurry Pulp Level [mm] *)
    bPulpLevel_Cell6_HealthA        : BOOL := TRUE;     (* Channel 1A Radar Transmitter Healthy [-] *)
    bPulpLevel_Cell6_HealthB        : BOOL := TRUE;     (* Channel 1B Float Transmitter Healthy [-] *)
    bPulpLevel_Cell6_HealthC        : BOOL := TRUE;     (* Channel 1C Ultrasonic Transmitter Healthy [-] *)
    rPulpLevel_Cell6_Disc_AB_ms     : REAL := 0.0;      (* Channel 1A vs 1B Discrepancy Timer [ms] *)
    rPulpLevel_Cell6_Disc_BC_ms     : REAL := 0.0;      (* Channel 1B vs 1C Discrepancy Timer [ms] *)
    rPulpLevel_Cell6_Disc_CA_ms     : REAL := 0.0;      (* Channel 1C vs 1A Discrepancy Timer [ms] *)
    bPulpLevel_Cell6_Degraded       : BOOL := FALSE;    (* Cell 6 Level Operating on Degraded 2oo2 Voting [-] *)
    bPulpLevel_Cell6_SingleFallback : BOOL := FALSE;    (* Cell 6 Level Operating on Single Channel [-] *)
    bPulpLevel_Cell6_Trip           : BOOL := FALSE;    (* Cell 6 Level Sensor Complete Failure Trip [-] *)

    (* Channel Group 1 End: Scavenger Cell 12 Pulp Level *)
    rPulpLevel_Cell12_Voted         : REAL := 1000.0;   (* 2oo3 Voted Cell 12 Slurry Pulp Level [mm] *)
    bPulpLevel_Cell12_HealthA       : BOOL := TRUE;     (* Channel 1A Radar Transmitter Healthy [-] *)
    bPulpLevel_Cell12_HealthB       : BOOL := TRUE;     (* Channel 1B Float Transmitter Healthy [-] *)
    bPulpLevel_Cell12_HealthC       : BOOL := TRUE;     (* Channel 1C Ultrasonic Transmitter Healthy [-] *)
    rPulpLevel_Cell12_Disc_AB_ms    : REAL := 0.0;      (* Channel 1A vs 1B Discrepancy Timer [ms] *)
    rPulpLevel_Cell12_Disc_BC_ms    : REAL := 0.0;      (* Channel 1B vs 1C Discrepancy Timer [ms] *)
    rPulpLevel_Cell12_Disc_CA_ms    : REAL := 0.0;      (* Channel 1C vs 1A Discrepancy Timer [ms] *)
    bPulpLevel_Cell12_Degraded      : BOOL := FALSE;    (* Cell 12 Level Operating on Degraded 2oo2 Voting [-] *)
    bPulpLevel_Cell12_SingleFallback: BOOL := FALSE;    (* Cell 12 Level Operating on Single Channel [-] *)
    bPulpLevel_Cell12_Trip          : BOOL := FALSE;    (* Cell 12 Level Sensor Complete Failure Trip [-] *)

    (* Channel Group 2: Froth Bed Depth Transmitters *)
    rFrothHeight_Voted              : REAL := 150.0;    (* 2oo3 Voted Froth Bed Lip Depth [mm] *)
    bFrothHeight_HealthA            : BOOL := TRUE;     (* Froth Sensor 2A Optical Camera Healthy [-] *)
    bFrothHeight_HealthB            : BOOL := TRUE;     (* Froth Sensor 2B Acoustic Sonic Echo Healthy [-] *)
    bFrothHeight_HealthC            : BOOL := TRUE;     (* Froth Sensor 2C Piezoresistive Buoyancy Healthy [-] *)
    rFrothHeight_Disc_AB_ms         : REAL := 0.0;      (* Froth Sensor 2A vs 2B Discrepancy Timer [ms] *)
    rFrothHeight_Disc_BC_ms         : REAL := 0.0;      (* Froth Sensor 2B vs 2C Discrepancy Timer [ms] *)
    rFrothHeight_Disc_CA_ms         : REAL := 0.0;      (* Froth Sensor 2C vs 2A Discrepancy Timer [ms] *)
    bFrothHeight_Degraded           : BOOL := FALSE;    (* Froth Sensor Operating on Degraded 2oo2 Voting [-] *)
    bFrothHeight_SingleFallback     : BOOL := FALSE;    (* Froth Sensor Operating on Single Channel [-] *)
    bFrothHeight_Trip               : BOOL := FALSE;    (* Froth Sensor Complete Failure Trip [-] *)

    (* Channel Group 3: Forced Aeration Differential Pressure *)
    rAirPress_Manifold_Voted        : REAL := 48.0;     (* 2oo3 Voted Air Blower Manifold Pressure [kPa] *)
    bAirPress_HealthA               : BOOL := TRUE;     (* Pressure Transmitter 3A Healthy [-] *)
    bAirPress_HealthB               : BOOL := TRUE;     (* Pressure Transmitter 3B Healthy [-] *)
    bAirPress_HealthC               : BOOL := TRUE;     (* Pressure Transmitter 3C Healthy [-] *)
    rAirPress_Disc_AB_ms            : REAL := 0.0;      (* Pressure Transmitter 3A vs 3B Discrepancy Timer [ms] *)
    rAirPress_Disc_BC_ms            : REAL := 0.0;      (* Pressure Transmitter 3B vs 3C Discrepancy Timer [ms] *)
    rAirPress_Disc_CA_ms            : REAL := 0.0;      (* Pressure Transmitter 3C vs 3A Discrepancy Timer [ms] *)
    bAirPress_Degraded              : BOOL := FALSE;    (* Air Pressure Operating on Degraded 2oo2 Voting [-] *)
    bAirPress_SingleFallback        : BOOL := FALSE;    (* Air Pressure Operating on Single Channel [-] *)
    bAirPress_Trip                  : BOOL := FALSE;    (* Air Pressure Complete Failure Trip [-] *)

    (* Channel Group 4: Concentrate Copper Grade Analyzers *)
    rXRF_ConcCu_Voted               : REAL := 28.5;     (* 2oo3 Voted Concentrate Copper Grade [% Cu] *)
    bXRF_ConcCu_HealthA             : BOOL := TRUE;     (* XRF Analyzer Flow Cell 4A Healthy [-] *)
    bXRF_ConcCu_HealthB             : BOOL := TRUE;     (* XRF Analyzer Flow Cell 4B Healthy [-] *)
    bXRF_ConcCu_HealthC             : BOOL := TRUE;     (* XRF Analyzer Flow Cell 4C Healthy [-] *)
    rXRF_ConcCu_Disc_AB_ms          : REAL := 0.0;      (* XRF Analyzer 4A vs 4B Discrepancy Timer [ms] *)
    rXRF_ConcCu_Disc_BC_ms          : REAL := 0.0;      (* XRF Analyzer 4B vs 4C Discrepancy Timer [ms] *)
    rXRF_ConcCu_Disc_CA_ms          : REAL := 0.0;      (* XRF Analyzer 4C vs 4A Discrepancy Timer [ms] *)
    bXRF_ConcCu_Degraded            : BOOL := FALSE;    (* XRF Analyzer Operating on Degraded 2oo2 Voting [-] *)
    bXRF_ConcCu_SingleFallback      : BOOL := FALSE;    (* XRF Analyzer Operating on Single Channel [-] *)
    bXRF_ConcCu_Trip                : BOOL := FALSE;    (* XRF Analyzer Complete Failure Trip [-] *)

    (* Channel Group 5: Scavenger Tailings Slurry Density Gauges *)
    rTailings_Density_Voted         : REAL := 1.35;     (* 2oo3 Voted Tailings Slurry Specific Gravity [g/cm3] *)
    bTailings_Density_HealthA       : BOOL := TRUE;     (* Nuclear Density Gauge 5A Healthy [-] *)
    bTailings_Density_HealthB       : BOOL := TRUE;     (* Nuclear Density Gauge 5B Healthy [-] *)
    bTailings_Density_HealthC       : BOOL := TRUE;     (* Coriolis Density Transmitter 5C Healthy [-] *)
    rTailings_Density_Disc_AB_ms    : REAL := 0.0;      (* Density Sensor 5A vs 5B Discrepancy Timer [ms] *)
    rTailings_Density_Disc_BC_ms    : REAL := 0.0;      (* Density Sensor 5B vs 5C Discrepancy Timer [ms] *)
    rTailings_Density_Disc_CA_ms    : REAL := 0.0;      (* Density Sensor 5C vs 5A Discrepancy Timer [ms] *)
    bTailings_Density_Degraded      : BOOL := FALSE;    (* Tailings Density Operating on Degraded 2oo2 Voting [-] *)
    bTailings_Density_SingleFallback: BOOL := FALSE;    (* Tailings Density Operating on Single Channel [-] *)
    bTailings_Density_Trip          : BOOL := FALSE;    (* Tailings Density Complete Failure Trip [-] *)

    (* Flotation Kinetics & Slurry Physics Calculated Intermediates *)
    rBubbleDiameter_d32_mm          : REAL := 1.25;     (* Sauter Mean Bubble Diameter d32 [mm] *)
    rSuperficialGasVelocity_cms     : REAL := 1.20;     (* Superficial Gas Velocity Jg = Q_air / A_cell [cm/s] *)
    rBubbleSurfaceAreaFlux_Sb_s     : REAL := 57.6;     (* Bubble Surface Area Flux Sb = 6*Jg/d32 [1/s] *)
    rFrothResidenceTime_tau_s       : REAL := 18.5;     (* Froth Retention & Lip Transport Time [s] *)
    rFrothRecoveryFactor_Alpha      : REAL := 0.68;     (* True Flotation Froth Recovery Factor Alpha_f [-] *)
    rEntrainmentRatio_Clay          : REAL := 0.045;    (* Hydrophilic Gangue Hydraulic Entrainment Ratio [-] *)
    rTrueFlotationRate_k_Cu         : REAL := 0.082;    (* First-Order Chalcopyrite Flotation Rate Constant [1/s] *)
    rCumulativeRecoveryCalc_pct     : REAL := 88.5;     (* Calculated Overall Copper Metal Recovery Efficiency [%] *)

    (* Cell Bottom Sanding Severity Index & Anti-Stiction Dither Variables *)
    rSandingSeverityIndex           : REAL := 0.0;      (* Cell Bottom Coarse Sanding & Packing Risk Index [-] *)
    rSandingIndex_Smooth            : REAL := 0.0;      (* Exponentially Filtered Sanding Risk Index [-] *)
    bSandingPreWarningActive        : BOOL := FALSE;    (* Slurry Sanding Pre-Warning Advisory Active [-] *)
    bSandingCriticalTripActive      : BOOL := FALSE;    (* Imminent Agitator Stall Sanding Trip Active [-] *)
    rDitherWaveform_pct             : REAL := 0.0;      (* Anti-Stiction Triangular Dither Displacement [%] *)
    rDitherPhaseRamp                : REAL := 0.0;      (* Periodic Dither Modulating Phase Angle [rad] *)
    rDartValve_StationaryTime_s     : ARRAY[0..5] OF REAL; (* Dart Valve Position Quiescence Timers [s] *)
    bDartValve_DitherActive         : ARRAY[0..5] OF BOOL; (* Valve Anti-Stiction Dither Active Flags [-] *)

    (* Deterministic 14-Stage Finite State Machine (FSM) Engine *)
    eState                          : INT := 0;         (* Active Operational State Index [0..13] *)
    ePrevState                      : INT := 0;         (* Previous Cycle Operational State Index [0..13] *)
    rStateTimer_s                   : REAL := 0.0;      (* Dwell Time Elapsed in Active State [s] *)
    rSubStateTimer_s                : REAL := 0.0;      (* Auxiliary Internal Sub-State Dwell Timer [s] *)
    iFsmStepIndex                   : INT := 0;         (* Sequential Step Index Within Active State [-] *)
    bFsmTransitionTrigger           : BOOL := FALSE;    (* Inter-State Discrete Transition Condition Met [-] *)

    (* Flush, Conditioning & Purge Specific Timers *)
    rWaterFlushTimer_s              : REAL := 0.0;      (* Water Line Valve Stroke Calibration Timer [s] *)
    rBlowerPurgeTimer_s             : REAL := 0.0;      (* Aeration Sparger Anti-Backflow Purge Timer [s] *)
    rSlurryFeedRampTimer_s          : REAL := 0.0;      (* Slurry Feed Introduction Volumetric Ramp Timer [s] *)
    rReagentConditionTimer_s        : REAL := 0.0;      (* Collector/Frother Conditioning Residence Timer [s] *)
    rFrothStabilizeTimer_s          : REAL := 0.0;      (* Froth Bed Formation & Weir Equilibrium Timer [s] *)
    rSurfactantBoostTimer_s         : REAL := 0.0;      (* Emergency Surfactant Reagent Boost Duration [s] *)
    rSanderUpFlushTimer_s           : REAL := 0.0;      (* High-Pressure De-Sanding Bottom Flush Duration [s] *)
    rEmergencyDumpTimer_s           : REAL := 0.0;      (* Emergency Slurry Launder Evacuation Dump Timer [s] *)

    (* ISA-18.2 Multi-Tier Process Alarm Limits, Deadbands & Timers *)
    (* Cell 1 Pulp Level Alarms *)
    rPulp1_HH_Limit_mm              : REAL := 1450.0;   (* Cell 1 High-High Overflow Danger Trip [mm] *)
    rPulp1_H_Limit_mm               : REAL := 1350.0;   (* Cell 1 High Level Deviation Warning [mm] *)
    rPulp1_L_Limit_mm               : REAL := 850.0;    (* Cell 1 Low Level Froth Loss Warning [mm] *)
    rPulp1_LL_Limit_mm              : REAL := 750.0;    (* Cell 1 Low-Low Impeller Exposure Trip [mm] *)
    rPulp1_Deadband_mm              : REAL := 15.0;     (* Cell 1 Level Alarm Clearance Hysteresis [mm] *)

    (* Cell 6 Pulp Level Alarms *)
    rPulp6_HH_Limit_mm              : REAL := 1400.0;   (* Cell 6 High-High Overflow Danger Trip [mm] *)
    rPulp6_H_Limit_mm               : REAL := 1300.0;   (* Cell 6 High Level Deviation Warning [mm] *)
    rPulp6_L_Limit_mm               : REAL := 800.0;    (* Cell 6 Low Level Froth Loss Warning [mm] *)
    rPulp6_LL_Limit_mm              : REAL := 700.0;    (* Cell 6 Low-Low Impeller Exposure Trip [mm] *)
    rPulp6_Deadband_mm              : REAL := 15.0;     (* Cell 6 Level Alarm Clearance Hysteresis [mm] *)

    (* Cell 12 Pulp Level Alarms *)
    rPulp12_HH_Limit_mm             : REAL := 1350.0;   (* Cell 12 High-High Overflow Danger Trip [mm] *)
    rPulp12_H_Limit_mm              : REAL := 1250.0;   (* Cell 12 High Level Deviation Warning [mm] *)
    rPulp12_L_Limit_mm              : REAL := 750.0;    (* Cell 12 Low Level Froth Loss Warning [mm] *)
    rPulp12_LL_Limit_mm             : REAL := 650.0;    (* Cell 12 Low-Low Tailings Siphon Trip [mm] *)
    rPulp12_Deadband_mm             : REAL := 15.0;     (* Cell 12 Level Alarm Clearance Hysteresis [mm] *)

    (* Froth Bed Thickness Alarms *)
    rFroth_HH_Limit_mm              : REAL := 350.0;    (* Froth Bed Over-Deep Gangue Entrainment Trip [mm] *)
    rFroth_H_Limit_mm               : REAL := 280.0;    (* Froth Bed Deep Deviation Warning [mm] *)
    rFroth_L_Limit_mm               : REAL := 60.0;     (* Froth Bed Thin Collapse Warning [mm] *)
    rFroth_LL_Limit_mm              : REAL := 30.0;     (* Froth Bed Complete Loss Pulp Lip Wash Trip [mm] *)
    rFroth_Deadband_mm              : REAL := 8.0;      (* Froth Bed Thickness Alarm Hysteresis [mm] *)

    (* Aeration Manifold Air Pressure Alarms *)
    rAirPress_HH_Limit_kPa          : REAL := 85.0;     (* Aeration Manifold Overpressure Trip [kPa] *)
    rAirPress_H_Limit_kPa           : REAL := 70.0;     (* Aeration Manifold High Pressure Warning [kPa] *)
    rAirPress_L_Limit_kPa           : REAL := 25.0;     (* Aeration Manifold Low Pressure Warning [kPa] *)
    rAirPress_LL_Limit_kPa          : REAL := 15.0;     (* Aeration Loss Sparger Slurry Ingress Trip [kPa] *)
    rAirPress_Deadband_kPa          : REAL := 2.5;      (* Air Pressure Alarm Clearance Hysteresis [kPa] *)

    (* Concentrate Copper Grade Alarms *)
    rXRF_ConcCu_HH_Limit_pct        : REAL := 36.0;     (* Grade Excessively High Mineral Loss in Tailings [% Cu] *)
    rXRF_ConcCu_H_Limit_pct         : REAL := 32.0;     (* Concentrate High Grade Deviation Advisory [% Cu] *)
    rXRF_ConcCu_L_Limit_pct         : REAL := 20.0;     (* Concentrate Low Grade Gangue Contamination [% Cu] *)
    rXRF_ConcCu_LL_Limit_pct        : REAL := 15.0;     (* Concentrate Low-Low Off-Spec Smelter Reject [% Cu] *)
    rXRF_ConcCu_Deadband_pct        : REAL := 0.5;      (* Copper Grade Alarm Clearance Hysteresis [% Cu] *)

    (* Scavenger Tailings Slurry Density Alarms *)
    rTailDensity_HH_Limit_gcc       : REAL := 1.60;     (* Tailings Slurry High-High Impeller Choke Trip [g/cm3] *)
    rTailDensity_H_Limit_gcc        : REAL := 1.48;     (* Tailings Slurry High Density Sanding Risk [g/cm3] *)
    rTailDensity_L_Limit_gcc        : REAL := 1.15;     (* Tailings Slurry Low Density Over-Dilution [g/cm3] *)
    rTailDensity_LL_Limit_gcc       : REAL := 1.05;     (* Tailings Slurry Water Only Loss of Slurry [g/cm3] *)
    rTailDensity_Deadband_gcc       : REAL := 0.02;     (* Tailings Density Alarm Clearance Hysteresis [g/cm3] *)

    (* Agitator Drive Torque Alarms *)
    rAgitatorTorque_HH_Limit_Nm     : REAL := 3200.0;   (* Agitator Drive Mechanical Shear Pin Overload Trip [Nm] *)
    rAgitatorTorque_H_Limit_Nm      : REAL := 2750.0;   (* Agitator Drive High Torque Sand Packing Warning [Nm] *)
    rAgitatorTorque_L_Limit_Nm      : REAL := 900.0;    (* Agitator Drive Low Torque Coupling Failure [Nm] *)
    rAgitatorTorque_LL_Limit_Nm     : REAL := 500.0;    (* Agitator Drive Shaft Broken Loss of Load Trip [Nm] *)
    rAgitatorTorque_Deadband_Nm     : REAL := 50.0;     (* Agitator Torque Alarm Clearance Hysteresis [Nm] *)

    (* Active Alarm Condition Latch Bits *)
    bPulp1_HH_Active                : BOOL := FALSE;
    bPulp1_H_Active                 : BOOL := FALSE;
    bPulp1_L_Active                 : BOOL := FALSE;
    bPulp1_LL_Active                : BOOL := FALSE;
    bPulp6_HH_Active                : BOOL := FALSE;
    bPulp6_H_Active                 : BOOL := FALSE;
    bPulp6_L_Active                 : BOOL := FALSE;
    bPulp6_LL_Active                : BOOL := FALSE;
    bPulp12_HH_Active               : BOOL := FALSE;
    bPulp12_H_Active                : BOOL := FALSE;
    bPulp12_L_Active                : BOOL := FALSE;
    bPulp12_LL_Active               : BOOL := FALSE;
    bFroth_HH_Active                : BOOL := FALSE;
    bFroth_H_Active                 : BOOL := FALSE;
    bFroth_L_Active                 : BOOL := FALSE;
    bFroth_LL_Active                : BOOL := FALSE;
    bAirPress_HH_Active             : BOOL := FALSE;
    bAirPress_H_Active              : BOOL := FALSE;
    bAirPress_L_Active              : BOOL := FALSE;
    bAirPress_LL_Active             : BOOL := FALSE;
    bXRF_ConcCu_HH_Active           : BOOL := FALSE;
    bXRF_ConcCu_H_Active            : BOOL := FALSE;
    bXRF_ConcCu_L_Active            : BOOL := FALSE;
    bXRF_ConcCu_LL_Active           : BOOL := FALSE;
    bTailDensity_HH_Active          : BOOL := FALSE;
    bTailDensity_H_Active           : BOOL := FALSE;
    bTailDensity_L_Active           : BOOL := FALSE;
    bTailDensity_LL_Active          : BOOL := FALSE;
    bAgitatorTorque_HH_Active       : BOOL := FALSE;
    bAgitatorTorque_H_Active        : BOOL := FALSE;
    bAgitatorTorque_L_Active        : BOOL := FALSE;
    bAgitatorTorque_LL_Active       : BOOL := FALSE;

    (* First-Out Latching Internal Logic *)
    bFirstOutLatched                : BOOL := FALSE;    (* First-Out Root Cause Frozen Latched Flag [-] *)
    dwFirstOutCapturedCode          : DWORD := 16#00000000; (* Captured Initial Fault Root Cause Code [-] *)

    (* Scratch Loop Counters & Temporary Math Computation Reals *)
    iIdx                            : INT := 0;         (* Primary State Vector Loop Counter [-] *)
    jIdx                            : INT := 0;         (* Matrix Column Loop Counter [-] *)
    mIdx                            : INT := 0;         (* Actuator Dimension Loop Counter [-] *)
    kStep                           : INT := 0;         (* MPC Horizon Time Step Counter [-] *)
    iIter                           : INT := 0;         (* PGD Optimization Unrolled Iteration Counter [-] *)
    rTempSum                        : REAL := 0.0;      (* Dot Product Matrix Multiply Accumulator [-] *)
    rTempDiff                       : REAL := 0.0;      (* Scalar Difference Intermediate Real [-] *)
    rTempCandidate                  : REAL := 0.0;      (* Actuator Gradient Candidate Value [-] *)
    rTempMaxDev                     : REAL := 0.0;      (* Maximum State Vector Deviation Diagnostic [-] *)
    rTempCrossCoupling              : REAL := 0.0;      (* Hydraulic Head Cross-Coupling Term [-] *)
END_VAR
"""
