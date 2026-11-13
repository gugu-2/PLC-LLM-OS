# semiconductor_tcb_builder/build_st_var.py

def get_var_declarations():
    return """VAR
    (* ============================================================================================== *)
    (* SECTION 1: EXECUTION CYCLE TIMING, SAMPLING INTERVAL & INTERNAL CONTROL SEQUENCING           *)
    (* ============================================================================================== *)
    bFirstScan                          : BOOL := TRUE;     (* First-cycle boot initialization trigger [-] *)
    dt_s                                : REAL := 0.0010;   (* Active execution delta time [s] *)
    rCycleTimeAccum_ms                  : REAL := 0.0;      (* Cumulative bond cycle elapsed time [ms] *)
    rStateTimeAccum_ms                  : REAL := 0.0;      (* Time elapsed within active FSM state [ms] *)
    iExecutionCycleCounter              : DINT := 0;        (* Total cyclic PLC task execution counter [-] *)
    iTotalBondCyclesCompleted           : DINT := 0;        (* Good completed chiplet assemblies [-] *)
    iTotalBondCyclesAborted             : DINT := 0;        (* Aborted / rejected chiplet assemblies [-] *)
    bStateTransitionTrigger             : BOOL := FALSE;    (* Single-cycle pulse on FSM stage advance [-] *)
    iNextFsmState                       : INT := 0;         (* Pending state target for atomic handoff [-] *)
    bInternalHaltRequested              : BOOL := FALSE;    (* Internal trip request latch [-] *)
    bPostBondAcousticComplete           : BOOL := FALSE;    (* Acoustic scan acquisition complete flag [-] *)

    (* ============================================================================================== *)
    (* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES & TIMERS             *)
    (* ============================================================================================== *)
    (* Bank 1: Bond Head Quartz Force Load Cells [N] *)
    rForce_Diff_12                      : REAL := 0.0;      (* Absolute deviation Ch1 vs Ch2 [N] *)
    rForce_Diff_23                      : REAL := 0.0;      (* Absolute deviation Ch2 vs Ch3 [N] *)
    rForce_Diff_31                      : REAL := 0.0;      (* Absolute deviation Ch3 vs Ch1 [N] *)
    rForce_DiscrepancyTimer_Ch1         : REAL := 0.0;      (* Channel 1 discrepancy persistence timer [s] *)
    rForce_DiscrepancyTimer_Ch2         : REAL := 0.0;      (* Channel 2 discrepancy persistence timer [s] *)
    rForce_DiscrepancyTimer_Ch3         : REAL := 0.0;      (* Channel 3 discrepancy persistence timer [s] *)
    bForce_Ch1_Healthy                  : BOOL := TRUE;     (* Channel 1 diagnostic health status [-] *)
    bForce_Ch2_Healthy                  : BOOL := TRUE;     (* Channel 2 diagnostic health status [-] *)
    bForce_Ch3_Healthy                  : BOOL := TRUE;     (* Channel 3 diagnostic health status [-] *)
    iForce_VotingMode                   : INT := 1;         (* Voting Mode: 1=2oo3, 2=1oo2, 3=1oo1, 4=Fault [-] *)
    rForce_Tolerance_N                  : REAL := 2.50;     (* Permissible inter-sensor force deviation [N] *)
    rForce_DiscrepancyTripTime_s        : REAL := 0.020;    (* Discrepancy persistence timeout limit [s] *)

    (* Bank 2: Ceramic Pulse Heater Thin-Film Thermocouples [deg C] *)
    rTemp_Diff_12                       : REAL := 0.0;      (* Absolute deviation Ch1 vs Ch2 [deg C] *)
    rTemp_Diff_23                       : REAL := 0.0;      (* Absolute deviation Ch2 vs Ch3 [deg C] *)
    rTemp_Diff_31                       : REAL := 0.0;      (* Absolute deviation Ch3 vs Ch1 [deg C] *)
    rTemp_DiscrepancyTimer_Ch1          : REAL := 0.0;      (* Channel 1 discrepancy persistence timer [s] *)
    rTemp_DiscrepancyTimer_Ch2          : REAL := 0.0;      (* Channel 2 discrepancy persistence timer [s] *)
    rTemp_DiscrepancyTimer_Ch3          : REAL := 0.0;      (* Channel 3 discrepancy persistence timer [s] *)
    bTemp_Ch1_Healthy                   : BOOL := TRUE;     (* Channel 1 diagnostic health status [-] *)
    bTemp_Ch2_Healthy                   : BOOL := TRUE;     (* Channel 2 diagnostic health status [-] *)
    bTemp_Ch3_Healthy                   : BOOL := TRUE;     (* Channel 3 diagnostic health status [-] *)
    iTemp_VotingMode                    : INT := 1;         (* Voting Mode: 1=2oo3, 2=1oo2, 3=1oo1, 4=Fault [-] *)
    rTemp_Tolerance_degC                : REAL := 6.00;     (* Permissible inter-sensor temperature deviation [deg C] *)
    rTemp_DiscrepancyTripTime_s         : REAL := 0.015;    (* Discrepancy persistence timeout limit [s] *)

    (* Bank 3: Bond Head Linear Optical Glass Encoders [um] *)
    rZPos_Diff_12                       : REAL := 0.0;      (* Absolute deviation Ch1 vs Ch2 [um] *)
    rZPos_Diff_23                       : REAL := 0.0;      (* Absolute deviation Ch2 vs Ch3 [um] *)
    rZPos_Diff_31                       : REAL := 0.0;      (* Absolute deviation Ch3 vs Ch1 [um] *)
    rZPos_DiscrepancyTimer_Ch1          : REAL := 0.0;      (* Channel 1 discrepancy persistence timer [s] *)
    rZPos_DiscrepancyTimer_Ch2          : REAL := 0.0;      (* Channel 2 discrepancy persistence timer [s] *)
    rZPos_DiscrepancyTimer_Ch3          : REAL := 0.0;      (* Channel 3 discrepancy persistence timer [s] *)
    bZPos_Ch1_Healthy                   : BOOL := TRUE;     (* Channel 1 diagnostic health status [-] *)
    bZPos_Ch2_Healthy                   : BOOL := TRUE;     (* Channel 2 diagnostic health status [-] *)
    bZPos_Ch3_Healthy                   : BOOL := TRUE;     (* Channel 3 diagnostic health status [-] *)
    iZPos_VotingMode                    : INT := 1;         (* Voting Mode: 1=2oo3, 2=1oo2, 3=1oo1, 4=Fault [-] *)
    rZPos_Tolerance_um                  : REAL := 0.40;     (* Permissible inter-sensor position deviation [um] *)
    rZPos_DiscrepancyTripTime_s         : REAL := 0.010;    (* Discrepancy persistence timeout limit [s] *)

    (* Bank 4: Substrate Vacuum Chuck Capacitance Diaphragm Gauges [kPa] *)
    rChuckVac_Diff_12                   : REAL := 0.0;      (* Absolute deviation Ch1 vs Ch2 [kPa] *)
    rChuckVac_Diff_23                   : REAL := 0.0;      (* Absolute deviation Ch2 vs Ch3 [kPa] *)
    rChuckVac_Diff_31                   : REAL := 0.0;      (* Absolute deviation Ch3 vs Ch1 [kPa] *)
    rChuckVac_DiscrepancyTimer_Ch1      : REAL := 0.0;      (* Channel 1 discrepancy persistence timer [s] *)
    rChuckVac_DiscrepancyTimer_Ch2      : REAL := 0.0;      (* Channel 2 discrepancy persistence timer [s] *)
    rChuckVac_DiscrepancyTimer_Ch3      : REAL := 0.0;      (* Channel 3 discrepancy persistence timer [s] *)
    bChuckVac_Ch1_Healthy               : BOOL := TRUE;     (* Channel 1 diagnostic health status [-] *)
    bChuckVac_Ch2_Healthy               : BOOL := TRUE;     (* Channel 2 diagnostic health status [-] *)
    bChuckVac_Ch3_Healthy               : BOOL := TRUE;     (* Channel 3 diagnostic health status [-] *)
    iChuckVac_VotingMode                : INT := 1;         (* Voting Mode: 1=2oo3, 2=1oo2, 3=1oo1, 4=Fault [-] *)
    rChuckVac_Tolerance_kPa             : REAL := 3.50;     (* Permissible inter-sensor vacuum deviation [kPa] *)
    rChuckVac_DiscrepancyTripTime_s     : REAL := 0.050;    (* Discrepancy persistence timeout limit [s] *)

    (* ============================================================================================== *)
    (* SECTION 3: CYBER-PHYSICAL DISCRETE STATE-SPACE (6x6) MATRICES & KALMAN OBSERVER                *)
    (* ============================================================================================== *)
    (* State Vector x:
       x[1] = Dynamic Bond Force Error e_F [N]
       x[2] = Bond Head Z Thermal Expansion Elongation Delta_L [um]
       x[3] = Micro-Bump Solder Viscoplastic Collapse Depth h_col [um]
       x[4] = Pulse Heater Substrate Interface Temperature T_int [deg C]
       x[5] = Chuck Holding Vacuum Differential Pressure P_vac [kPa]
       x[6] = 6-Axis Chuck Co-Planarity Tilt Pitch Error Theta_Rx [urad]
    *)
    matA                                : ARRAY[1..6, 1..6] OF REAL; (* Discrete State Transition Matrix *)
    matB                                : ARRAY[1..6, 1..5] OF REAL; (* Discrete Control Input Gain Matrix *)
    matC                                : ARRAY[1..6, 1..6] OF REAL; (* Discrete Measurement Matrix *)
    matD                                : ARRAY[1..6, 1..5] OF REAL; (* Discrete Direct Feedthrough Matrix *)
    matKalmanL                          : ARRAY[1..6, 1..6] OF REAL; (* Steady-State Kalman Filter Gain Matrix *)

    vecX_State                          : ARRAY[1..6] OF REAL;       (* Prior State Estimate x[k|k-1] *)
    vecX_Hat                            : ARRAY[1..6] OF REAL;       (* Corrected State Estimate x[k|k] *)
    vecX_Next                           : ARRAY[1..6] OF REAL;       (* Predicted Future State x[k+1|k] *)
    vecY_Meas                           : ARRAY[1..6] OF REAL;       (* Process Measured Vector y[k] *)
    vecY_Hat                            : ARRAY[1..6] OF REAL;       (* Estimated Measurement C*x_hat *)
    vecInnovation                       : ARRAY[1..6] OF REAL;       (* Innovation Residual y_meas - y_hat *)
    vecX_Ref                            : ARRAY[1..6] OF REAL;       (* Reference State Setpoints *)

    (* Actuator Vector u:
       u[1] = Piezo Micro-Actuator Trim Displacement [um] (-10.0 .. +10.0)
       u[2] = Voice Coil Linear Motor Current [A] (-15.0 .. +15.0)
       u[3] = Ceramic Pulse Heater Duty Cycle [%] (0.0 .. 100.0)
       u[4] = Chilled Nitrogen Quench Valve [%] (0.0 .. 100.0)
       u[5] = Formic Acid Vapor Purge Flow [%] (0.0 .. 100.0)
    *)
    vecU_Active                         : ARRAY[1..5] OF REAL;       (* Active Executing Control Inputs *)
    vecU_Prev                           : ARRAY[1..5] OF REAL;       (* Previous Scan Actuator Commands *)
    vecDeltaU                           : ARRAY[1..5] OF REAL;       (* Actuator Rate of Change Slew *)

    (* Physical Process Parameters *)
    rColletCTE_ppm_K                    : REAL := 2.60;     (* Ceramic collet coefficient of thermal expansion [ppm/K] *)
    rColletLength_mm                    : REAL := 45.0;     (* Effective thermal length of bond collet [mm] *)
    rColletBaseTemp_degC                : REAL := 25.0;     (* Ambient collet mount reference temperature [deg C] *)
    rSolderMeltingPoint_degC            : REAL := 217.0;    (* Sn-Ag eutectic micro-bump liquidus temperature [deg C] *)
    rSolderViscosity_mPa_s              : REAL := 2.20;     (* Dynamic viscosity of molten micro-solder [mPa.s] *)
    rSurfaceTension_N_m                 : REAL := 0.485;    (* Liquid solder surface tension coefficient [N/m] *)
    rInitialMicroBumpHeight_um          : REAL := 22.50;    (* As-fabricated micro-bump initial height [um] *)
    rCurrentBumpHeight_um               : REAL := 22.50;    (* Instantaneous dynamic micro-bump height [um] *)
    rTotalBumpArea_mm2                  : REAL := 0.0;      (* Aggregate contact footprint area [mm2] *)
    rBondZ_TouchDatum_um                : REAL := 0.0;      (* Latched Z linear encoder coordinate at 5N contact [um] *)
    bBondZ_DatumLatched                 : BOOL := FALSE;    (* Touch coordinate latch valid flag [-] *)

    (* ============================================================================================== *)
    (* SECTION 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & PGD OPTIMIZATION                  *)
    (* ============================================================================================== *)
    (* Penalty Weighting Matrices *)
    matQ_Diag                           : ARRAY[1..6] OF REAL;       (* State Tracking Penalty Diagonal *)
    matR_Diag                           : ARRAY[1..5] OF REAL;       (* Control Effort Penalty Diagonal *)
    matS_Diag                           : ARRAY[1..5] OF REAL;       (* Slew Rate Slew Penalty Diagonal *)
    matP_Diag                           : ARRAY[1..6] OF REAL;       (* Terminal State Penalty Diagonal *)

    (* Horizon Trajectory Buffers: Np = 10 Steps *)
    arrU_Horiz                          : ARRAY[0..9, 1..5] OF REAL; (* Future Control Horizon Sequence *)
    arrX_Horiz                          : ARRAY[0..10, 1..6] OF REAL;(* Forward Predicted State Horizon *)
    arrLambda                           : ARRAY[0..10, 1..6] OF REAL;(* Backward Adjoint Co-State Vector *)
    arrGradU                            : ARRAY[0..9, 1..5] OF REAL; (* Analytical Cost Gradient dJ/du *)

    (* Actuator Hard Saturation & Slew Constraints *)
    rU_LowerBound                       : ARRAY[1..5] OF REAL;       (* Actuator minimum saturation limits *)
    rU_UpperBound                       : ARRAY[1..5] OF REAL;       (* Actuator maximum saturation limits *)
    rDeltaU_MaxRate                     : ARRAY[1..5] OF REAL;       (* Actuator maximum rate per cycle *)
    rPgdStepSize                        : REAL := 0.0028;            (* Unrolled PGD gradient step length *)

    (* Loop Counters for Unrolled Iterative Engine *)
    iPgdIteration                       : INT := 0;
    iHorizStep                          : INT := 0;
    iStateIdx                           : INT := 0;
    iInputIdx                           : INT := 0;
    rGradDotProduct                     : REAL := 0.0;
    rCostFunctionVal                    : REAL := 0.0;

    (* ============================================================================================== *)
    (* SECTION 5: 6-AXIS CHUCK LEVELING HEXAPOD KINEMATICS & AUTONOMOUS LEVELING                      *)
    (* ============================================================================================== *)
    matChuckKinematics                  : ARRAY[1..6, 1..6] OF REAL; (* Decoupling Transformation Matrix *)
    rChuckCorrection_Tx                 : REAL := 0.0;      (* Cartesian translation adjustment X [um] *)
    rChuckCorrection_Ty                 : REAL := 0.0;      (* Cartesian translation adjustment Y [um] *)
    rChuckCorrection_Tz                 : REAL := 0.0;      (* Cartesian translation adjustment Z [um] *)
    rChuckCorrection_Rx                 : REAL := 0.0;      (* Angular tilt adjustment pitch Rx [urad] *)
    rChuckCorrection_Ry                 : REAL := 0.0;      (* Angular tilt adjustment roll Ry [urad] *)
    rChuckCorrection_Rz                 : REAL := 0.0;      (* Angular rotation adjustment yaw Rz [urad] *)
    rHexapodStrut1_Cmd_um               : REAL := 0.0;      (* Vertical Piezo Strut 1 displacement [um] *)
    rHexapodStrut2_Cmd_um               : REAL := 0.0;      (* Vertical Piezo Strut 2 displacement [um] *)
    rHexapodStrut3_Cmd_um               : REAL := 0.0;      (* Vertical Piezo Strut 3 displacement [um] *)
    rHexapodShear1_Cmd_um               : REAL := 0.0;      (* Lateral Shear Flexure 1 displacement [um] *)
    rHexapodShear2_Cmd_um               : REAL := 0.0;      (* Lateral Shear Flexure 2 displacement [um] *)
    rHexapodShear3_Cmd_um               : REAL := 0.0;      (* Lateral Shear Flexure 3 displacement [um] *)
    bChuckLevelingSettled               : BOOL := FALSE;    (* Co-planarity tilt within tolerance < 1.5 urad *)

    (* ============================================================================================== *)
    (* SECTION 6: 5TH-ORDER S-CURVE TRAJECTORY GENERATOR FOR Z-AXIS APPROACH                           *)
    (* ============================================================================================== *)
    rZ_Traj_TargetPos_um                : REAL := 0.0;      (* Commanded destination Z-coordinate [um] *)
    rZ_Traj_CurrentPos_um               : REAL := 0.0;      (* Real-time trajectory reference position [um] *)
    rZ_Traj_CurrentVel_um_s             : REAL := 0.0;      (* Real-time trajectory reference velocity [um/s] *)
    rZ_Traj_CurrentAcc_um_s2            : REAL := 0.0;      (* Real-time trajectory reference acceleration [um/s2] *)
    rZ_Traj_MaxVel_um_s                 : REAL := 120000.0; (* Peak traverse velocity (120 mm/s) [um/s] *)
    rZ_Traj_MaxAcc_um_s2                : REAL := 800000.0; (* Peak trajectory acceleration (0.8g) [um/s2] *)
    rZ_Traj_MaxJerk_um_s3               : REAL := 25000000.0;(* Peak jerk rate of change [um/s3] *)
    rZ_Traj_PhaseTime_s                 : REAL := 0.0;      (* Internal trajectory phase time elapsed [s] *)
    iZ_Traj_Phase                       : INT := 0;         (* 0=Idle, 1=Jerk+, 2=AccConst, 3=Jerk-, 4=VelConst, 5=Decel *)
    bZ_Traj_ProfileDone                 : BOOL := FALSE;    (* Trajectory profile completed flag [-] *)

    (* ============================================================================================== *)
    (* SECTION 7: PULSE CERAMIC HEATER & COOLING DYNAMICS                                             *)
    (* ============================================================================================== *)
    rHeater_IntegralError               : REAL := 0.0;      (* Temperature PID integral accumulator [deg C.s] *)
    rHeater_PrevTemp                    : REAL := 25.0;     (* Prior cycle temperature for derivative [deg C] *)
    rHeater_CurrentRate_degC_s          : REAL := 0.0;      (* Instantaneous measured heating rate [deg C/s] *)
    rHeater_FeedforwardDuty             : REAL := 0.0;      (* Theoretical thermal power feedforward [%] *)
    rHeater_PidDuty                     : REAL := 0.0;      (* Closed-loop thermal correction duty [%] *)
    rQuench_PidValve                    : REAL := 0.0;      (* Closed-loop quench gas proportional valve [%] *)
    rPeakTemperatureReached_degC        : REAL := 0.0;      (* Peak bond temperature captured this cycle [deg C] *)
    rPeakBondForceReached_N             : REAL := 0.0;      (* Peak compressive force captured this cycle [N] *)

    (* ============================================================================================== *)
    (* SECTION 8: FORMIC ACID DEOXIDATION ATMOSPHERE CONTROL                                          *)
    (* ============================================================================================== *)
    rFormicMassFlow_sccm                : REAL := 0.0;      (* Formic vapor delivery flow rate [sccm] *)
    rCarrierN2Flow_slpm                 : REAL := 0.0;      (* Shroud dilution inert N2 flow [slpm] *)
    rOxideLayerThickness_nm             : REAL := 4.50;     (* Estimated native Cu2O/CuO oxide layer [nm] *)
    rReductionReactionRate_nm_s         : REAL := 0.0;      (* Chemical reduction rate by HCOOH vapor [nm/s] *)
    bDeoxidationAtmosphereReady         : BOOL := FALSE;    (* O2 < 30 ppm and HCOOH concentration verified *)

    (* ============================================================================================== *)
    (* SECTION 9: POST-BOND ACOUSTIC PULSE-ECHO INTEGRITY & SOLDER JOINT QUALITY                      *)
    (* ============================================================================================== *)
    rAcousticImpedance_Si_MRayl         : REAL := 19.70;    (* Acoustic impedance of silicon chiplet [MRayl] *)
    rAcousticImpedance_Cu_MRayl         : REAL := 44.30;    (* Acoustic impedance of copper pillar [MRayl] *)
    rAcousticImpedance_SnAg_MRayl       : REAL := 24.20;    (* Acoustic impedance of Sn-Ag eutectic cap [MRayl] *)
    rTheoreticalTransmissionCoeff       : REAL := 0.92;     (* Ideal acoustic transmission coefficient [-] *)
    rMeasuredEchoAmplitudeRatio         : REAL := 0.0;      (* Ratio of reflected amplitude to baseline [-] *)
    rEstimatedInterfacialVoidPct        : REAL := 0.0;      (* Calculated micro-void area percentage [%] *)
    rTotalJointShearStrength_Est_MPa    : REAL := 0.0;      (* Joint shear strength prediction [MPa] *)

    (* ============================================================================================== *)
    (* SECTION 10: ISA-18.2 MULTI-TIER ALARM TRIP THRESHOLDS & DEADBAND HYSTERESIS                    *)
    (* ============================================================================================== *)
    (* Force Thresholds [N] *)
    rTrip_Force_HH_N                    : REAL := 475.0;    (* Emergency Over-Force High-High Trip [N] *)
    rTrip_Force_H_N                     : REAL := 455.0;    (* Bond Force High Warning [N] *)
    rTrip_Force_L_N                     : REAL := 3.50;     (* Touch Force Low Warning [N] *)
    rTrip_Force_LL_N                    : REAL := 1.00;     (* Loss of Contact Low-Low Trip [N] *)
    rDeadband_Force_N                   : REAL := 2.00;     (* Force Alarm Clearance Hysteresis [N] *)

    (* Temperature Thresholds [deg C] *)
    rTrip_Temp_HH_degC                  : REAL := 440.0;    (* Thermal Runaway High-High Trip [deg C] *)
    rTrip_Temp_H_degC                   : REAL := 425.0;    (* Temperature High Warning [deg C] *)
    rTrip_Temp_L_degC                   : REAL := 120.0;    (* Melt Phase Temperature Low Warning [deg C] *)
    rTrip_Temp_LL_degC                  : REAL := 45.0;     (* Pre-Heat Loss Low-Low Trip [deg C] *)
    rDeadband_Temp_degC                 : REAL := 3.00;     (* Temperature Alarm Hysteresis [deg C] *)

    (* Z-Axis Micro-Bump Collapse Depth Thresholds [um] *)
    rTrip_Collapse_HH_um                : REAL := 22.00;    (* Excessive Squeeze-Out Short-Circuit Trip [um] *)
    rTrip_Collapse_H_um                 : REAL := 16.50;    (* Solder Collapse High Warning [um] *)
    rTrip_Collapse_L_um                 : REAL := 4.50;     (* Solder Collapse Low Warning [um] *)
    rTrip_Collapse_LL_um                : REAL := 1.50;     (* Insufficient Melt Non-Wet Low-Low Trip [um] *)
    rDeadband_Collapse_um               : REAL := 0.50;     (* Collapse Alarm Hysteresis [um] *)

    (* Vacuum Holding Thresholds [kPa] *)
    rTrip_Vac_HH_kPa                    : REAL := -25.0;    (* Severe Vacuum Loss High-High Trip [kPa] *)
    rTrip_Vac_H_kPa                     : REAL := -65.0;    (* Vacuum Degradation Warning [kPa] *)
    rDeadband_Vac_kPa                   : REAL := 3.00;     (* Vacuum Alarm Hysteresis [kPa] *)

    (* Chuck Co-Planarity Tilt Thresholds [urad] *)
    rTrip_Tilt_HH_urad                  : REAL := 12.00;    (* Co-Planarity Critical Misalignment Trip [urad] *)
    rTrip_Tilt_H_urad                   : REAL := 6.00;     (* Co-Planarity Tilt High Warning [urad] *)
    rDeadband_Tilt_urad                 : REAL := 0.50;     (* Tilt Alarm Hysteresis [urad] *)

    (* Process Atmosphere Oxygen & Formic Concentration Thresholds *)
    rTrip_O2_HH_PPM                     : REAL := 80.00;    (* Oxygen Ingress High-High Trip [ppm] *)
    rTrip_O2_H_PPM                      : REAL := 40.00;    (* Oxygen Level High Warning [ppm] *)
    rTrip_Formic_LL_Pct                 : REAL := 0.80;     (* Formic Vapor Insufficient Low-Low Trip [%] *)
    rTrip_Formic_L_Pct                  : REAL := 1.40;     (* Formic Vapor Low Warning [%] *)
    rTrip_Formic_H_Pct                  : REAL := 4.20;     (* Formic Vapor High Warning [%] *)
    rTrip_Formic_HH_Pct                 : REAL := 5.00;     (* Formic Acid Flammability High-High Trip [%] *)

    (* Active Alarm Latch Status Flags *)
    bAlarm_Force_HH                     : BOOL := FALSE;
    bAlarm_Force_H                      : BOOL := FALSE;
    bAlarm_Force_L                      : BOOL := FALSE;
    bAlarm_Force_LL                     : BOOL := FALSE;
    bAlarm_Temp_HH                      : BOOL := FALSE;
    bAlarm_Temp_H                       : BOOL := FALSE;
    bAlarm_Temp_L                       : BOOL := FALSE;
    bAlarm_Temp_LL                      : BOOL := FALSE;
    bAlarm_Collapse_HH                  : BOOL := FALSE;
    bAlarm_Collapse_H                   : BOOL := FALSE;
    bAlarm_Collapse_L                   : BOOL := FALSE;
    bAlarm_Collapse_LL                  : BOOL := FALSE;
    bAlarm_Vac_HH                       : BOOL := FALSE;
    bAlarm_Vac_H                        : BOOL := FALSE;
    bAlarm_Tilt_HH                      : BOOL := FALSE;
    bAlarm_Tilt_H                       : BOOL := FALSE;
    bAlarm_O2_HH                        : BOOL := FALSE;
    bAlarm_O2_H                         : BOOL := FALSE;
    bAlarm_Formic_HH                    : BOOL := FALSE;
    bAlarm_Formic_LL                    : BOOL := FALSE;
    bAlarm_TMR_ForceDiscrepancy         : BOOL := FALSE;
    bAlarm_TMR_TempDiscrepancy          : BOOL := FALSE;
    bAlarm_TMR_ZPosDiscrepancy          : BOOL := FALSE;
    bAlarm_TMR_VacDiscrepancy           : BOOL := FALSE;
END_VAR
"""
