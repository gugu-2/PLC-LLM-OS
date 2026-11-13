# mine_vod_fan_builder/st_var.py

def get_var_declarations():
    return """VAR
    (* ==================================================================================================== *)
    (* INTERNAL CYBER-PHYSICAL STATE-SPACE MATRICES & LUENBERGER OBSERVER SUITE                             *)
    (* ==================================================================================================== *)
    (* Discrete State Transition Matrix A (6x6) *)
    arrA : ARRAY[1..6, 1..6] OF REAL;
    (* Discrete Actuator Input Coupling Matrix B (6x6) *)
    arrB : ARRAY[1..6, 1..6] OF REAL;
    (* Discrete Measurement Output Matrix C (6x6) *)
    arrC : ARRAY[1..6, 1..6] OF REAL;
    (* Discrete Direct Feedthrough Matrix D (6x6) *)
    arrD : ARRAY[1..6, 1..6] OF REAL;
    (* Luenberger State Observer Innovation Gain Matrix L (6x6) *)
    arrL : ARRAY[1..6, 1..6] OF REAL;

    (* State Vector Estimates and Predictions *)
    arrX_hat : ARRAY[1..6] OF REAL; (* Estimated state vector at current scan k *)
    arrX_pred : ARRAY[1..6] OF REAL; (* One-step ahead predicted state vector k+1 *)
    arrU_vector : ARRAY[1..6] OF REAL; (* Current normalized actuator input vector [0..1] *)
    arrY_meas : ARRAY[1..6] OF REAL; (* Measured physical process output vector *)
    arrY_hat : ARRAY[1..6] OF REAL; (* Observer estimated process output vector *)
    arrY_err : ARRAY[1..6] OF REAL; (* Observer innovation measurement residual error vector *)

    (* State Normalization and Physical Scaling Factors *)
    arrX_scale : ARRAY[1..6] OF REAL; (* State vector engineering unit scaling multipliers *)
    arrU_scale : ARRAY[1..6] OF REAL; (* Actuator vector engineering unit scaling multipliers *)
    arrX_bias : ARRAY[1..6] OF REAL; (* State vector engineering unit offset biases *)
    arrU_bias : ARRAY[1..6] OF REAL; (* Actuator vector engineering unit offset biases *)

    (* One-Shot Initialization Interlock *)
    bStateSpaceInitialized : BOOL := FALSE; (* First-scan matrix memory allocation flag *)

    (* ==================================================================================================== *)
    (* RECEDING-HORIZON MPC OPTIMIZER (UNROLLED PROJECTED GRADIENT DESCENT)                                 *)
    (* ==================================================================================================== *)
    (* MPC Quadratic Penalty Weights *)
    arrQ_weights : ARRAY[1..6] OF REAL; (* Diagonal state tracking error penalties *)
    arrR_weights : ARRAY[1..6] OF REAL; (* Diagonal actuator control energy effort penalties *)
    arrS_weights : ARRAY[1..6] OF REAL; (* Diagonal actuator slew-rate smoothness penalties *)
    arrP_weights : ARRAY[1..6] OF REAL; (* Terminal state prediction penalty weights *)

    (* Actuator Box Saturation and Slew-Rate Constraints *)
    arrU_min : ARRAY[1..6] OF REAL; (* Lower physical actuator saturation limits *)
    arrU_max : ARRAY[1..6] OF REAL; (* Upper physical actuator saturation limits *)
    arrDeltaU_max : ARRAY[1..6] OF REAL; (* Maximum allowable actuator slew rate per cycle *)

    (* Optimizer Working State Vectors *)
    arrX_target : ARRAY[1..6] OF REAL; (* Target operational state setpoints *)
    arrU_opt : ARRAY[1..6] OF REAL; (* Optimized actuator command vector *)
    arrU_prev : ARRAY[1..6] OF REAL; (* Previous cycle actuator command memory *)
    arrGrad : ARRAY[1..6] OF REAL; (* Cost function gradient vector *)
    arrGrad_AntiStall : ARRAY[1..6] OF REAL; (* Non-linear anti-stall barrier gradient components *)
    arrGrad_SmokeLock : ARRAY[1..6] OF REAL; (* Smoke backlayering critical velocity barrier gradient *)
    rPGD_StepSize : REAL := 0.045; (* Projected gradient descent step size alpha *)
    rAntiStallBarrierWeight : REAL := 125.0; (* Steepness factor for anti-stall barrier potential *)
    rSmokeLockBarrierWeight : REAL := 250.0; (* Steepness factor for critical velocity barrier *)

    (* ==================================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING STRUCTURES & DISCREPANCY TIMERS                          *)
    (* ==================================================================================================== *)
    (* Channel 1: Main Fan Intake Differential Pressure [kPa] *)
    rDP_Voted : REAL := 3.5;
    rDP_Ch1_Delta : REAL := 0.0;
    rDP_Ch2_Delta : REAL := 0.0;
    rDP_Ch3_Delta : REAL := 0.0;
    rDP_Tolerance : REAL := 0.45; (* Discrepancy allowable window [kPa] *)
    tDP_Ch1_DiscrepancyTimer : REAL := 0.0;
    tDP_Ch2_DiscrepancyTimer : REAL := 0.0;
    tDP_Ch3_DiscrepancyTimer : REAL := 0.0;
    bDP_Ch1_Fault : BOOL := FALSE;
    bDP_Ch2_Fault : BOOL := FALSE;
    bDP_Ch3_Fault : BOOL := FALSE;
    iDP_HealthyCount : INT := 3;
    iDP_DegradationMode : INT := 0; (* 0=3 healthy (2oo3), 1=2 healthy (1oo2), 2=1 healthy (1oo1), 3=all failed *)

    (* Channel 2: Ultrasonic Exhaust Airway Velocity Flowmeter [m/s] *)
    rAirVel_Voted : REAL := 18.2;
    rAirVel_Ch1_Delta : REAL := 0.0;
    rAirVel_Ch2_Delta : REAL := 0.0;
    rAirVel_Ch3_Delta : REAL := 0.0;
    rAirVel_Tolerance : REAL := 1.85; (* Discrepancy allowable window [m/s] *)
    tAirVel_Ch1_DiscrepancyTimer : REAL := 0.0;
    tAirVel_Ch2_DiscrepancyTimer : REAL := 0.0;
    tAirVel_Ch3_DiscrepancyTimer : REAL := 0.0;
    bAirVel_Ch1_Fault : BOOL := FALSE;
    bAirVel_Ch2_Fault : BOOL := FALSE;
    bAirVel_Ch3_Fault : BOOL := FALSE;
    iAirVel_HealthyCount : INT := 3;
    iAirVel_DegradationMode : INT := 0;

    (* Channel 3: Work-Heading Multi-Gas Borehole Toxic Gas (CO) [ppm] *)
    rToxicGas_Voted : REAL := 12.0;
    rToxicGas_Ch1_Delta : REAL := 0.0;
    rToxicGas_Ch2_Delta : REAL := 0.0;
    rToxicGas_Ch3_Delta : REAL := 0.0;
    rToxicGas_Tolerance : REAL := 4.5; (* Discrepancy allowable window [ppm] *)
    tToxicGas_Ch1_DiscrepancyTimer : REAL := 0.0;
    tToxicGas_Ch2_DiscrepancyTimer : REAL := 0.0;
    tToxicGas_Ch3_DiscrepancyTimer : REAL := 0.0;
    bToxicGas_Ch1_Fault : BOOL := FALSE;
    bToxicGas_Ch2_Fault : BOOL := FALSE;
    bToxicGas_Ch3_Fault : BOOL := FALSE;
    iToxicGas_HealthyCount : INT := 3;
    iToxicGas_DegradationMode : INT := 0;

    (* Channel 4: Surface Main Fan Bearing Triaxial Vibration Velocity [mm/s RMS] *)
    rVib_Voted : REAL := 1.8;
    rVib_Ch1_Delta : REAL := 0.0;
    rVib_Ch2_Delta : REAL := 0.0;
    rVib_Ch3_Delta : REAL := 0.0;
    rVib_Tolerance : REAL := 0.75; (* Discrepancy allowable window [mm/s] *)
    tVib_Ch1_DiscrepancyTimer : REAL := 0.0;
    tVib_Ch2_DiscrepancyTimer : REAL := 0.0;
    tVib_Ch3_DiscrepancyTimer : REAL := 0.0;
    bVib_Ch1_Fault : BOOL := FALSE;
    bVib_Ch2_Fault : BOOL := FALSE;
    bVib_Ch3_Fault : BOOL := FALSE;
    iVib_HealthyCount : INT := 3;
    iVib_DegradationMode : INT := 0;

    (* Discrepancy Persistence Threshold Time *)
    tDiscrepancyLimit_s : REAL := 0.250; (* 250 milliseconds persistent discrepancy qualifies fault *)

    (* ==================================================================================================== *)
    (* SUBTERRANEAN THERMODYNAMICS, HYDROSTATIC BAROMETRICS & ATKINSON NETWORK VARIABLES                     *)
    (* ==================================================================================================== *)
    (* Universal Gas & Gravity Constants *)
    rGasConstant_Air : REAL := 287.058; (* Specific gas constant for dry air [J/(kg K)] *)
    rGravity_Acc : REAL := 9.80665; (* Gravitational acceleration constant [m/s2] *)
    rSpecificHeat_Cp : REAL := 1005.0; (* Specific heat capacity of air at constant pressure [J/(kg K)] *)
    rAdiabaticLapseRate : REAL := 0.00976; (* Dry adiabatic temperature lapse rate [deg C/m] *)
    rGeothermalGradient : REAL := 0.0185; (* Rock geothermal temperature gradient [deg C/m] *)

    (* Shaft Geometry & Hydrostatic Air Column Profiles *)
    rExhaustShaftDiameter_m : REAL := 6.5; (* Concrete-lined main exhaust upcast shaft inner diameter [m] *)
    rExhaustShaftArea_m2 : REAL := 33.183; (* Cross-sectional area of main exhaust shaft [m2] *)
    rIntakeShaftArea_m2 : REAL := 38.485; (* Cross-sectional area of downcast intake fresh air shaft [m2] *)
    rSurfaceAirDensity_kgm3 : REAL := 1.205; (* Density of air at surface collar conditions [kg/m3] *)
    rMeanAirwayDensity_kgm3 : REAL := 1.345; (* Integrated mean shaft air density [kg/m3] *)
    rNaturalVentilationPressure_kPa : REAL := 0.42; (* Thermal buoyancy driving pressure (NVP) [kPa] *)

    (* Dynamic Mine Equivalent Atkinson Resistance Calculation *)
    rAtkinsonShaftFriction_k : REAL := 0.0035; (* Atkinson friction factor for smooth concrete shaft [N s2/m4] *)
    rTotalMineResistance_Atkinson : REAL := 0.00785; (* Equivalent subterranean Atkinson resistance [kPa s2/m6] *)
    arrBranchResistance_Base : ARRAY[1..24] OF REAL; (* Base aerodynamic resistance per branch [kPa s2/m6] *)
    arrBranchCrossSection_m2 : ARRAY[1..24] OF REAL; (* Airway cross-sectional area per branch [m2] *)
    arrBranchRegulatoryFlowMin_m3s : ARRAY[1..24] OF REAL; (* Statutory minimum airflow per branch [m3/s] *)

    (* ==================================================================================================== *)
    (* AERODYNAMIC FAN CURVE, STALL BOUNDARY POLYNOMIALS & TIP TURBULENCE TRACKING                         *)
    (* ==================================================================================================== *)
    (* 3.5 MW Variable-Pitch Axial Fan Aerodynamic Parameters *)
    rFanRotorDiameter_m : REAL := 4.25; (* Fan impeller tip-to-tip diameter [m] *)
    rFanBladeHubDiameter_m : REAL := 1.95; (* Fan hub diameter [m] *)
    rFanNominalSpeed_RPM : REAL := 990.0; (* Rated synchronous operating speed [RPM] *)
    rFanMaxSpeed_RPM : REAL := 1050.0; (* Maximum overspeed mechanical limit [RPM] *)
    rFanMinSpeed_RPM : REAL := 350.0; (* Minimum speed limit to prevent motor cooling starvation [RPM] *)
    rBladePitchMin_deg : REAL := -12.0; (* Hydraulic blade feather zero-torque angle [deg] *)
    rBladePitchMax_deg : REAL := 38.0; (* Hydraulic blade maximum aerodynamic pitch angle [deg] *)
    rBladePitchRateMax_deg_s : REAL := 2.5; (* Maximum hydraulic blade pitch slew rate [deg/s] *)

    (* Fan Pressure-Flow-Pitch Characteristic Surface Polynomial Coefficients *)
    rPolyC0 : REAL := 5.85; (* Characteristic pressure base intercept [kPa] *)
    rPolyC1 : REAL := 0.0125; (* Linear flow coefficient [kPa / (m3/s)] *)
    rPolyC2 : REAL := -0.000185; (* Quadratic flow droop coefficient [kPa / (m3/s)2] *)
    rPolyC3 : REAL := 0.142; (* Blade pitch linear sensitivity coefficient [kPa / deg] *)
    rPolyC4 : REAL := -0.00165; (* Pitch-flow cross-coupling coefficient [kPa / (deg m3/s)] *)

    (* Stall Line Polynomial Coefficients: Q_stall = s0 + s1*DP + s2*DP^2 + s3*Pitch + s4*Pitch*DP *)
    rStallS0 : REAL := 115.0; (* Base stall boundary volumetric flow [m3/s] *)
    rStallS1 : REAL := 18.5; (* Stall boundary sensitivity to pressure rise [m3/s / kPa] *)
    rStallS2 : REAL := 1.45; (* Stall boundary quadratic pressure component [m3/s / kPa2] *)
    rStallS3 : REAL := 2.85; (* Stall boundary sensitivity to pitch angle [m3/s / deg] *)
    rStallS4 : REAL := 0.35; (* Stall boundary cross-coupling term [m3/s / (deg kPa)] *)

    (* Calculated Operating Point Stall Margins *)
    rCriticalStallFlow_m3s : REAL := 145.0; (* Computed rotating stall boundary volumetric flow [m3/s] *)
    rOperatingPointFlow_m3s : REAL := 210.0; (* Current operating point total volumetric exhaust flow [m3/s] *)
    rDynamicPressureTip_Pa : REAL := 350.0; (* Mean dynamic pressure at blade tips [Pa] *)
    rTurbulenceFilterAlpha : REAL := 0.12; (* First-order exponential filter coefficient for turbulence *)
    rFilteredTipTurbulence_Pa : REAL := 45.0; (* Filtered blade tip turbulence RMS value [Pa] *)

    (* ==================================================================================================== *)
    (* TOXIC GAS CLEARANCE DYNAMICS, DPM DISPERSION & POST-BLAST PURGE KINETICS                             *)
    (* ==================================================================================================== *)
    (* Regulatory Exposure Limits (Mine Safety & Health Administration MSHA / SafeWork) *)
    rCO_SafeReentryLimit_ppm : REAL := 25.0; (* 8-hr TWA regulatory safe re-entry limit for CO [ppm] *)
    rNO2_SafeReentryLimit_ppm : REAL := 3.0; (* Regulatory ceiling exposure limit for NO2 [ppm] *)
    rDPM_SafeReentryLimit_ug_m3 : REAL := 160.0; (* Diesel Particulate Matter elemental carbon limit [ug/m3] *)
    rDieselDPM_EmissionFactor_g_kWh : REAL := 0.15; (* Modern Tier 4 diesel engine DPM emission rate [g/kWh] *)
    rDieselAirflowRequirement_m3s_kW : REAL := 0.06; (* Statutory minimum airflow per diesel engine power [m3/(s kW)] *)

    (* Post-Blast Gas Dispersion Calculation Constants *)
    rHeadingVolume_m3 : REAL := 4500.0; (* Standard blind drift / stope active production volume [m3] *)
    rPurgeMixingEfficiency_eta : REAL := 0.78; (* Non-ideal dilution ventilation mixing efficiency factor *)
    rPurgeTimeRemaining_Internal : REAL := 0.0; (* Internal integrator for post-blast clearance time [s] *)
    tBlastPurgeElapsed_s : REAL := 0.0; (* Elapsed timer in active post-blast clearance mode [s] *)

    (* ==================================================================================================== *)
    (* UNDERGROUND FIRE SMOKE REVERSAL (BACKLAYERING) PREVENTION VARIABLES                                  *)
    (* ==================================================================================================== *)
    (* Thomas-Heselden-Kennedy Critical Backlayering Velocity Equation Constants *)
    rKennedyFactor_k : REAL := 0.61; (* Dimensionless critical velocity coefficient *)
    rFirePlumeHeight_m : REAL := 4.8; (* Underground drift nominal ceiling vertical height [m] *)
    rFireDriftArea_m2 : REAL := 24.5; (* Cross-sectional area of intake haulage airway drift [m2] *)
    rCriticalBacklayeringVel_Calc : REAL := 2.45; (* Computed critical velocity to halt smoke backlayering [m/s] *)
    rSmokeBacklayeringMargin_pct : REAL := 35.0; (* Current safety velocity margin above critical speed [%] *)

    (* ==================================================================================================== *)
    (* 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM) INTERNAL REGISTERS                      *)
    (* ==================================================================================================== *)
    eState : INT := 0; (* Internal current state pointer (0..13) *)
    ePrevState : INT := 0; (* State machine previous execution cycle memory *)
    tStateTimer_s : REAL := 0.0; (* Active elapsed time in current state [s] *)
    tSubStepTimer_s : REAL := 0.0; (* Sub-sequence step execution timer [s] *)
    iStateStep : INT := 0; (* Internal sub-step index for multi-phase state executions *)

    (* State Permissives & Progression Flags *)
    bLubeOilPressureEstablished : BOOL := FALSE; (* Fan lube oil pressure interlock satisfied *)
    bBladePitchAtZeroReturn : BOOL := FALSE; (* Fan hydraulic blades feathered to zero-torque start position *)
    bMotorSoftStartCompleted : BOOL := FALSE; (* High-voltage motor soft-starter / VFD at base synchronous RPM *)
    bBladePitchMinimumLoadRamped : BOOL := FALSE; (* Fan blade pitch safely advanced to minimum aerodynamic load *)
    bLouverSweepCompleted : BOOL := FALSE; (* All 24 underground branch louvers verified through full stroke *)
    bPostBlastPurgeCompleted : BOOL := FALSE; (* Heading toxic gas levels confirmed below statutory safe limits *)
    bStandbyPurgeCompleted : BOOL := FALSE; (* Surface fan motor and duct cooldown sequence finalized *)
    bEmergencyTripLatched : BOOL := FALSE; (* Critical SIL-3 trip condition latched until manual reset *)

    (* ==================================================================================================== *)
    (* ISA-18.2 MULTI-TIER PROCESS ALARM ENGINE THRESHOLDS & HYSTERESIS REGISTERS                           *)
    (* ==================================================================================================== *)
    (* Differential Pressure Alarm Setpoints [kPa] *)
    rDP_Trip_HH : REAL := 6.2; (* Main fan stall risk / airway blockage high-high trip [kPa] *)
    rDP_Warn_H : REAL := 5.2; (* Main fan high differential pressure warning [kPa] *)
    rDP_Warn_L : REAL := 1.8; (* Airway short-circuit / duct leakage low warning [kPa] *)
    rDP_Trip_LL : REAL := 0.8; (* Fan duct catastrophic collapse / fan stall low-low trip [kPa] *)
    rDP_Hysteresis : REAL := 0.15; (* Differential pressure alarm deadband hysteresis [kPa] *)

    (* Stall Margin Alarm Setpoints [%] *)
    rStall_Trip_LL : REAL := 8.0; (* Imminent rotating fan blade stall emergency trip [%] *)
    rStall_Warn_L : REAL := 18.0; (* Aerodynamic stall proximity advisory warning [%] *)
    rStall_Hysteresis : REAL := 2.5; (* Stall margin alarm deadband hysteresis [%] *)

    (* Blade Tip Dynamic Turbulence Setpoints [Pa RMS] *)
    rTurb_Trip_HH : REAL := 180.0; (* Rotating stall pre-stall turbulence high-high trip [Pa] *)
    rTurb_Warn_H : REAL := 95.0; (* Precursor aerodynamic turbulence warning [Pa] *)
    rTurb_Hysteresis : REAL := 10.0; (* Turbulence deadband hysteresis [Pa] *)

    (* Work-Heading Toxic Gas CO Alarm Setpoints [ppm] *)
    rCO_Trip_HH : REAL := 50.0; (* Immediate evacuation mandatory high-high trip [ppm] *)
    rCO_Warn_H : REAL := 25.0; (* Statutory threshold ventilation boost warning [ppm] *)
    rCO_Hysteresis : REAL := 2.0; (* Carbon monoxide alarm deadband hysteresis [ppm] *)

    (* Fan Bearing Vibration Velocity Setpoints [mm/s RMS] *)
    rVib_Trip_HH : REAL := 7.5; (* ISO 10816 Zone D mechanical danger seismic trip [mm/s] *)
    rVib_Warn_H : REAL := 4.5; (* ISO 10816 Zone C vibration alert warning [mm/s] *)
    rVib_Hysteresis : REAL := 0.35; (* Vibration deadband hysteresis [mm/s] *)

    (* Fan Motor Stator Winding Temperature Setpoints [deg C] *)
    rWindingTemp_Trip_HH : REAL := 135.0; (* Class F insulation high-high thermal trip [deg C] *)
    rWindingTemp_Warn_H : REAL := 115.0; (* High motor winding thermal warning [deg C] *)

    (* Fan Forced Lube Oil Pressure Setpoints [bar] *)
    rLubeOil_Trip_LL : REAL := 2.1; (* Hydrodynamic journal bearing oil starvation trip [bar] *)
    rLubeOil_Warn_L : REAL := 2.8; (* Low lubrication oil pressure warning [bar] *)

    (* Surface Intake Collar Air Temperature Setpoints [deg C] *)
    rIntakeTemp_Warn_L : REAL := 1.5; (* Intake shaft collar freeze warning [deg C] *)
    rIntakeTemp_Trip_LL : REAL := -2.0; (* Intake shaft severe icing formation trip [deg C] *)

    (* Loop Counters & Temporary Math Storage *)
    iLoopIdx : INT := 1;
    jLoopIdx : INT := 1;
    kPGD_Iter : INT := 1;
    rTempSum : REAL := 0.0;
    rTempDelta : REAL := 0.0;
    rSortTemp : REAL := 0.0;
    arrSortedValues : ARRAY[1..3] OF REAL;
END_VAR
"""
