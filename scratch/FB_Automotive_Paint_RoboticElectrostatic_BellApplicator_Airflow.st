FUNCTION_BLOCK FB_Automotive_Paint_RoboticElectrostatic_BellApplicator_Airflow
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - IEC 61131-3 PRODUCTION BENCHMARK SUITE
AUTOMOTIVE & COMMERCIAL VEHICLE MANUFACTURING - ROBOTIC ELECTROSTATIC PAINT APPLICATION
========================================================================================================================
SYSTEM ARCHITECTURE & INDUSTRIAL PROCESS SPECIFICATION:
  - Applicator Type    : High-Speed Electrostatic Rotary Bell Cup Atomizer with Direct-Charge Cascade (100 kV DC).
  - Commercial Sector  : Automotive Exterior Clearcoat & Waterborne/Solventborne Metallic Basecoat Finishing.
  - Throughput Dynamic : 65 Jobs/Hour (JPH) Tact Time, 550 mm/s Nominal TCP Robotic Application Trajectory.
  - Drive Mechanism    : Ultra-Precision Air-Bearing Impulse Micro-Turbine (Nominal Speed 10,000 to 70,000 RPM).
  - Charging Subsystem : Direct Fluid/Cup Contact Charging via Integrated Wrist High-Voltage Solid-State Cascade.
  - Aerodynamic Shroud : Dual Concentric Shaping Air Rings (Inner SA1 for Pattern Fan Width 150-550 mm,
                         Outer SA2 for Peripheral Droplet Containment, Boundary Sharpness, and Mist Suppression).
  - Fluid Delivery     : Positive-Displacement Micro-Gear Servo Pump with Upstream/Downstream Closed-Loop Regulation.
  - Environmental Sync : Down-Draft Spray Booth Laminar Airflow Balance (0.25 to 0.45 m/s) and Psychrometric Guard.
  - Color Change Block : Integrated Fast Color-Change Block (CCB) with Rapid Solvent Slug & Air-Chop Purge Sequence.
  - Execution Profile  : Deterministic Real-Time Synchronous Execution Cycle Ts = 2.0 ms (500 Hz Scan Frequency).
========================================================================================================================
MATHEMATICAL & CYBER-PHYSICAL FOUNDATIONS:
  1. Discrete 6x6 State-Space Dynamic Matrices (A, B, C, D) representing:
     * x[1]: Bell turbine rotational speed dynamic slip & bearing load [RPM]
     * x[2]: Atomized paint droplet Sauter Mean Diameter (SMD d32) [um]
     * x[3]: Electrostatic transfer efficiency [%] and space-charge cloud potential [kV]
     * x[4]: Shaping air shroud pattern fan width [mm] and edge spray sharpness [N/m2]
     * x[5]: Paint fluid delivery dynamic pressure [bar] and gear pump volumetric flow [cc/min]
     * x[6]: Booth downdraft airflow laminar velocity [m/s] and relative humidity [% RH]
  2. Luenberger Dynamic State Observer with Innovation Feedback for 3x Faster Response than Open-Loop Decay.
  3. Receding-Horizon Model Predictive Control (MPC) with 10 Unrolled Projected Gradient Descent (PGD) Iterations:
     * State tracking error quadratic penalty matrix Q
     * Actuator energy control effort penalty matrix R
     * Actuator slew-rate smoothness penalty matrix S
     * Discrete Riccati terminal prediction penalty matrix P
     * Actuator rate-of-change and box saturation constraint projection
  4. 2oo3 Triple Modular Redundancy (TMR) Voting Architecture Across 4 Multi-Sensor Channels:
     * Bell air-turbine optical fiber frequency speed tachometers (Tach_Sensors: 1, 2, 3) [RPM]
     * Cascade high-voltage divider feedback sensors (HV_Voltage: 1, 2, 3) [kV]
     * Cascade load current feedback transducers (HV_Current: 1, 2, 3) [uA]
     * Paint fluid Coriolis mass flow meters (Paint_Flow: 1, 2, 3) [cc/min]
     * Discrepancy accumulation timers and bumpless degradation (2oo3 -> 1oo2 -> 1oo1 -> Trip)
  5. Deterministic 14-Stage Production Finite State Machine (States 0 through 13):
     * State 0:  STATE_IDLE
     * State 1:  STATE_BOOTH_LAMINAR_VENTILATION_LOCK
     * State 2:  STATE_COLOR_FEED_LINE_PRESSURIZATION
     * State 3:  STATE_TURBINE_BEARING_AIR_LIFT_LOCK
     * State 4:  STATE_BELL_TURBINE_SPEED_RAMP_ACCEL
     * State 5:  STATE_SHAPING_AIR_AERODYNAMIC_SHROUD_ESTABLISH
     * State 6:  STATE_HIGH_VOLTAGE_RAMP_AND_LEAK_CHECK
     * State 7:  STATE_TRIGGER_PAINT_SPRAY_PRODUCTION_RUN
     * State 8:  STATE_DYNAMIC_PATH_CORNERING_OVERFLOW_COMPENSATION
     * State 9:  STATE_INTER_COAT_STANDBY_IDLE_HOLD
     * State 10: STATE_HIGH_VOLTAGE_DECAY_AND_DISCHARGE
     * State 11: STATE_RAPID_SOLVENT_PURGE_AND_COLOR_CHANGE
     * State 12: STATE_TURBINE_DYNAMIC_BRAKING_DECEL
     * State 13: STATE_EMERGENCY_HV_SPARK_DETECTED_FAST_SHUTDOWN
  6. ISA-18.2 Multi-Tier Process Alarms (HH, H, L, LL, Deadband Hysteresis) with 4x Bit-Packed 32-Bit DWORDs.
========================================================================================================================
*)
VAR_INPUT
    (* --- System Supervisory Master Commands & Mode Selectors --- *)
    bEnable : BOOL := FALSE; (* Master Applicator Subsystem Enable Command [BOOL] *)
    bReset : BOOL := FALSE; (* Master Fault, Trip and Diagnostic Alarm Reset [BOOL] *)
    bRobotCycleStart : BOOL := FALSE; (* Industrial Robot Trajectory Paint Trigger Master Permissive [BOOL] *)
    bRobotPathCorneringActive : BOOL := FALSE; (* TCP High-Speed Robot Cornering Feedforward Trigger [BOOL] *)
    bColorChangeTrigger : BOOL := FALSE; (* Automated Rapid Color Change & Solvent Flush Request [BOOL] *)
    bSolventPurgeTrigger : BOOL := FALSE; (* Automated Tip & Shroud Wash Solvent/Air Chop Request [BOOL] *)
    bBoothLaminarPermissive : BOOL := FALSE; (* Downdraft Spray Booth Laminar Airflow Safety Interlock [BOOL] *)
    bStandbyHoldCommand : BOOL := FALSE; (* Inter-Coat Standby Energy & Bearing Air Hold Command [BOOL] *)
    
    (* --- Robotic Kinematic & Trajectory Telemetry --- *)
    rRobotLinearVelocity : REAL := 0.0; (* Applicator Tool Center Point (TCP) Linear Path Velocity [m/s] *)
    rRobotStandoffDistance : REAL := 250.0; (* Perpendicular Distance from Bell Cup Lip to Vehicle Body [mm] *)
    rRobotPathCurvature : REAL := 0.0; (* Instantaneous Trajectory Radius of Curvature Inverse [1/m] *)
    rRobotTrajectoryAcceleration : REAL := 0.0; (* Applicator Linear Kinematic Acceleration Vector [m/s2] *)
    
    (* --- Process Recipe Target Setpoints --- *)
    rTargetRotationalSpeed : REAL := 45000.0; (* Recipe Bell Cup Air-Turbine Rotational Speed Target [RPM] *)
    rTargetHighVoltage : REAL := 75.0; (* Recipe Electrostatic Direct-Charge Cascade Voltage Target [kV] *)
    rTargetPaintFlowRate : REAL := 280.0; (* Recipe Paint Fluid Volumetric Metering Target [cc/min] *)
    rTargetInnerShapingAir : REAL := 180.0; (* Recipe Inner Shaping Air SA1 Volumetric Delivery Rate [Nm3/h] *)
    rTargetOuterShapingAir : REAL := 260.0; (* Recipe Outer Shaping Air SA2 Volumetric Delivery Rate [Nm3/h] *)
    rTargetPatternWidth : REAL := 320.0; (* Desired Spray Pattern Deposition Fan Width on Substrate [mm] *)
    rTargetDropletSMD : REAL := 22.5; (* Desired Atomized Droplet Sauter Mean Diameter d32 Target [um] *)
    rTargetEdgeSharpness : REAL := 85.0; (* Desired Pattern Boundary Spray Gradient Steepness [N/m2] *)
    
    (* --- Paint Material Physical & Rheological Parameters --- *)
    rPaintViscosityNominal : REAL := 85.0; (* Low-Shear Base Dynamic Viscosity of Paint Formulation [mPa.s] *)
    rPaintDensity : REAL := 1025.0; (* Formulated Wet Paint Material Density / Specific Gravity [kg/m3] *)
    rPaintSurfaceTension : REAL := 0.0285; (* Paint Liquid-Air Equilibrium Surface Tension Coefficient [N/m] *)
    rPaintResistivity : REAL := 45.0; (* Paint Material Specific Bulk Electrical Resistivity [MOhm.cm] *)
    rPaintSolidsFraction : REAL := 0.52; (* Paint Non-Volatile Volume Solids Weight Fraction [fraction] *)
    
    (* --- 2oo3 Triple Modular Redundancy (TMR) Sensor Channels --- *)
    rTach_Raw1 : REAL := 0.0; (* Bell Speed Tachometer Channel 1 Optical Fiber Sensor [RPM] *)
    rTach_Raw2 : REAL := 0.0; (* Bell Speed Tachometer Channel 2 Magnetic Reluctance Sensor [RPM] *)
    rTach_Raw3 : REAL := 0.0; (* Bell Speed Tachometer Channel 3 Back-EMF Induction Sensor [RPM] *)
    
    rHV_Volt_Raw1 : REAL := 0.0; (* High Voltage Divider Measurement Channel 1 [kV] *)
    rHV_Volt_Raw2 : REAL := 0.0; (* High Voltage Divider Measurement Channel 2 [kV] *)
    rHV_Volt_Raw3 : REAL := 0.0; (* High Voltage Divider Measurement Channel 3 [kV] *)
    
    rHV_Curr_Raw1 : REAL := 0.0; (* High Voltage Cascade Output Current Shunt Transducer 1 [uA] *)
    rHV_Curr_Raw2 : REAL := 0.0; (* High Voltage Cascade Output Current Shunt Transducer 2 [uA] *)
    rHV_Curr_Raw3 : REAL := 0.0; (* High Voltage Cascade Output Current Shunt Transducer 3 [uA] *)
    
    rPaint_Flow_Raw1 : REAL := 0.0; (* Paint Delivery Dual-Tube Coriolis Mass Flow Meter Channel 1 [cc/min] *)
    rPaint_Flow_Raw2 : REAL := 0.0; (* Paint Delivery Dual-Tube Coriolis Mass Flow Meter Channel 2 [cc/min] *)
    rPaint_Flow_Raw3 : REAL := 0.0; (* Paint Positive-Displacement Servo Gear Pump Flow Encoder 3 [cc/min] *)
    
    (* --- Fluidic, Pneumatic & Atmospheric Supply Pressures --- *)
    rAirBearingPressure : REAL := 6.2; (* Bell Turbine Aerodynamic Lift Bearing Supply Pressure [bar] *)
    rDriveAirSupplyPressure : REAL := 7.0; (* Bell Turbine Drive Air Proportional Valve Supply Header [bar] *)
    rBrakeAirSupplyPressure : REAL := 6.5; (* Bell Turbine Dynamic Braking Air Proportional Header [bar] *)
    rShapingAirSupplyPressure : REAL := 5.8; (* Dual Shaping Air Shroud Pneumatic Header Supply Pressure [bar] *)
    rPaintLineDynamicPressure : REAL := 4.8; (* Paint Delivery Line Dynamic Pressure at Wrist Manifold [bar] *)
    rSolventSupplyPressure : REAL := 8.5; (* Automated Flush Solvent High-Pressure Delivery Line [bar] *)
    rChopAirSupplyPressure : REAL := 6.0; (* Purge Air Chop High-Velocity Pulsed Purge Pressure [bar] *)
    
    (* --- Environmental & Psychrometric Booth Telemetry --- *)
    rBoothAirVelocity : REAL := 0.35; (* Paint Spray Booth Down-Draft Laminar Airflow Velocity [m/s] *)
    rBoothTemperature : REAL := 21.5; (* Paint Spray Booth Ambient Dry-Bulb Air Temperature [deg C] *)
    rBoothRelativeHumidity : REAL := 65.0; (* Paint Spray Booth Ambient Moisture Relative Humidity [% RH] *)
    rBoothStaticPressure : REAL := 15.0; (* Spray Booth Differential Static Pressure vs Atmosphere [Pa] *)
    rCycleTime : REAL := 0.002; (* Real-Time Synchronous Periodic Task Scan Interval [s] *)
END_VAR

VAR_OUTPUT
    (* --- Discrete System Operating States & Actuations --- *)
    bSystemReady : BOOL := FALSE; (* Applicator Subsystem Initialized, Pressurized & Fully Ready [BOOL] *)
    bSprayTriggerActive : BOOL := FALSE; (* Paint Fluid Needle Trigger Actuator Digital Command [BOOL] *)
    bElectrostaticCascadeOn : BOOL := FALSE; (* High Voltage Electrostatic Cascade Direct-Charge Power Enable [BOOL] *)
    bFastColorChangeActive : BOOL := FALSE; (* Automated Rapid Color Change & Flush Sequence In Progress [BOOL] *)
    bEmergencyShutdown : BOOL := FALSE; (* Fast Spark Crowbar Quench / Safety Interlock E-Stop Active [BOOL] *)
    bBearingAirInterlockOk : BOOL := FALSE; (* Aerodynamic Turbine Bearing Air Lift Pressure Interlock Healthy [BOOL] *)
    bDowndraftVelocityOk : BOOL := FALSE; (* Spray Booth Laminar Ventilation Downdraft Within Window [BOOL] *)
    bInterCoatStandbyActive : BOOL := FALSE; (* Inter-Job Standby Energy Reduction Mode Engaged [BOOL] *)
    
    (* --- Continuous Proportional Actuator Servo Commands --- *)
    rTurbineDriveAirValve : REAL := 0.0; (* Proportional Air Turbine Drive Servo Valve Modulation [%] *)
    rTurbineBrakeAirValve : REAL := 0.0; (* Proportional Air Turbine Dynamic Braking Counter-Torque Valve [%] *)
    rHighVoltageCommand : REAL := 0.0; (* High Voltage Solid-State Cascade Closed-Loop Command [kV] *)
    rInnerShapingAirValve : REAL := 0.0; (* Inner Shaping Air SA1 Proportional Flow Valve Command [%] *)
    rOuterShapingAirValve : REAL := 0.0; (* Outer Shaping Air SA2 Proportional Flow Valve Command [%] *)
    rPaintGearPumpSpeedCmd : REAL := 0.0; (* Positive Displacement Micro-Gear Servo Pump Rotational Speed [RPM] *)
    rPaintFluidPressureReg : REAL := 0.0; (* Paint Fluid Dynamic Pressure Balancing Regulator Valve [%] *)
    rSolventFlushValveCmd : REAL := 0.0; (* Color Change Block Solvent Injection Proportional Valve [%] *)
    rAirChopPurgeValveCmd : REAL := 0.0; (* Color Change Block High-Pressure Pulsed Air Chop Valve [%] *)
    rBellWashRingValveCmd : REAL := 0.0; (* External Bell Cup Perimeter Cleaning Ring Solvent Valve [%] *)
    
    (* --- Validated 2oo3 TMR Process Telemetry --- *)
    rVotedTurbineSpeed : REAL := 0.0; (* 2oo3 TMR Validated Bell Turbine Rotational Speed [RPM] *)
    rVotedHighVoltage : REAL := 0.0; (* 2oo3 TMR Validated Cascade Direct Electrostatic High Voltage [kV] *)
    rVotedCascadeCurrent : REAL := 0.0; (* 2oo3 TMR Validated Cascade Space-Charge Cloud Current [uA] *)
    rVotedPaintFlowRate : REAL := 0.0; (* 2oo3 TMR Validated Paint Volumetric Delivery Metering Rate [cc/min] *)
    
    (* --- First-Principles Cyber-Physical Observer Estimates --- *)
    rEstimatedDropletSMD : REAL := 0.0; (* First-Principles Estimated Sauter Mean Diameter d32 [um] *)
    rEstimatedTransferEff : REAL := 0.0; (* First-Principles Estimated Electrostatic Transfer Efficiency [%] *)
    rEstimatedPatternWidth : REAL := 0.0; (* Aerodynamic Shroud Spray Pattern Fan Deposition Width [mm] *)
    rEstimatedEdgeSharpness : REAL := 0.0; (* Aerodynamic Shroud Boundary Spray Sharpness Metric [N/m2] *)
    rEstimatedFilmThickness : REAL := 0.0; (* Centrifugal Paint Liquid Film Thickness at Bell Cup Serration [um] *)
    rContainmentStabilityRatio : REAL := 0.0; (* Aerodynamic Shroud Vortex Containment Stability Index [dimensionless] *)
    rSpaceChargeCloudDensity : REAL := 0.0; (* Volume Space-Charge Cloud Electric Potential Density [kV/m3] *)
    rDynamicBearingClearance : REAL := 0.0; (* Spindle Aerodynamic Air Film Dynamic Flying Height [um] *)
    rSolventEvaporationLoss : REAL := 0.0; (* Atomized In-Flight Droplet Solvent Mass Loss Fraction [%] *)
    
    (* --- Supervisory State & ISA-18.2 Bit-Packed Status Words --- *)
    nFsmCurrentState : INT := 0; (* Deterministic 14-Stage Production Finite State Machine Index [-] *)
    dwStatusWord1 : DWORD := 16#00000000; (* Bit-Packed Operational State, Interlocks & Readiness [DWORD] *)
    dwStatusWord2 : DWORD := 16#00000000; (* Bit-Packed Actuator Health, Servo Links & Sensor Quality [DWORD] *)
    dwAlarmWord1 : DWORD := 16#00000000; (* Bit-Packed Category A Safety Critical Tripped Conditions [DWORD] *)
    dwAlarmWord2 : DWORD := 16#00000000; (* Bit-Packed Category B High/Low Process Threshold Warnings [DWORD] *)
    dwAlarmWord3 : DWORD := 16#00000000; (* Bit-Packed Category C 2oo3 TMR Sensor Discrepancy Faults [DWORD] *)
    dwAlarmWord4 : DWORD := 16#00000000; (* Bit-Packed Category D Color-Change, Purge & Maintenance Alerts [DWORD] *)
END_VAR

VAR
    (* --- Supervisory Lifecycle & One-Shot Flags --- *)
    bFirstScan : BOOL := TRUE; (* One-Shot Matrix Allocation and Parameter Initialization Flag *)
    sFsmStateName : STRING(64) := 'STATE_IDLE'; (* Diagnostic Description of Current Active FSM Stage *)
    rFsmStepTimer : REAL := 0.0; (* Accumulated In-State Dwell Timer [s] *)
    nPurgeSubStep : INT := 0; (* Internal Multi-Phase Color Change Purge Sequence Index *)
    rPurgeSubStepTimer : REAL := 0.0; (* Purge Sub-Step Execution Duration Timer [s] *)
    
    (* --- Cyber-Physical Constant Specifications --- *)
    rBellCupRadius : REAL := 0.0325; (* Outer Radius of Bell Cup Serrated Lip: 65 mm Diameter [m] *)
    rTurbineMomentOfInertia : REAL := 0.000185; (* Total Rotational Moment of Inertia of Spindle & Cup [kg.m2] *)
    rDielectricPermittivity : REAL := 8.854E-12; (* Free Space Electric Permittivity Epsilon-0 [F/m] *)
    rAirDensityRef : REAL := 1.184; (* Ambient Air Reference Density at 21.5 deg C [kg/m3] *)
    rTurbineViscousFriction : REAL := 1.25E-6; (* Aerodynamic Bearing Laminar Drag Coefficient [N.m.s/rad] *)
    rAeroDragTurbineCoeff : REAL := 4.8E-10; (* High-Speed Quadratic Turbulent Cup Air Drag [N.m.s2/rad2] *)
    rGearPumpDisplacement : REAL := 1.2; (* Micro-Gear Metering Pump Displacement Volume [cc/rev] *)
    
    (* --- Discrete State-Space Matrices (6x6 Model Dimensions) --- *)
    (* State x[1]: Rotational Speed Error & Dynamic Bearing Load [RPM]                                *)
    (* State x[2]: Droplet Sauter Mean Diameter (SMD d32) Deviation [um]                              *)
    (* State x[3]: Electrostatic Transfer Efficiency Deviation [%] & Cloud Potential                 *)
    (* State x[4]: Shaping Air Shroud Pattern Fan Width [mm] & Edge Spray Sharpness [N/m2]            *)
    (* State x[5]: Paint Fluid Delivery Dynamic Pressure [bar] & Metering Flow Rate [cc/min]          *)
    (* State x[6]: Booth Downdraft Laminar Airflow Velocity [m/s] & Relative Humidity [% RH]         *)
    matA : ARRAY[1..6, 1..6] OF REAL; (* Discrete System Dynamics Transition Matrix A *)
    matB : ARRAY[1..6, 1..6] OF REAL; (* Discrete Control Input Actuation Matrix B *)
    matC : ARRAY[1..6, 1..6] OF REAL; (* Output Sensor Measurement Matrix C *)
    matD : ARRAY[1..6, 1..6] OF REAL; (* Direct Feedthrough Matrix D *)
    matL : ARRAY[1..6, 1..6] OF REAL; (* Luenberger Dynamic State Observer Gain Matrix L *)
    
    (* --- Model Predictive Control (MPC) Cost & Horizon Matrices --- *)
    matQ : ARRAY[1..6, 1..6] OF REAL; (* State Tracking Error Quadratic Penalty Matrix Q *)
    matR : ARRAY[1..6, 1..6] OF REAL; (* Actuator Effort Energy Penalty Matrix R *)
    matS : ARRAY[1..6, 1..6] OF REAL; (* Actuator Slew-Rate Smoothness Penalty Matrix S *)
    matP : ARRAY[1..6, 1..6] OF REAL; (* Terminal Prediction Cost Matrix P *)
    
    (* --- Cyber-Physical State & Control Vectors --- *)
    vecX_Hat : ARRAY[1..6] OF REAL; (* Estimated State-Space Vector x_hat[k] *)
    vecX_Pred : ARRAY[1..6] OF REAL; (* Projected Next-Step State Vector x[k+1] *)
    vecX_Ref : ARRAY[1..6] OF REAL; (* Target Reference Equilibrium State Vector *)
    vecY_Meas : ARRAY[1..6] OF REAL; (* Measured Deviation Vector from Process Sensors *)
    vecY_Est : ARRAY[1..6] OF REAL; (* Estimated Sensor Output Vector from Observer *)
    vecObsErr : ARRAY[1..6] OF REAL; (* Innovation Error Vector (y_meas - y_est) *)
    vecU_Opt : ARRAY[1..6] OF REAL; (* Receding-Horizon Optimal Actuator Command Vector *)
    vecU_Prev : ARRAY[1..6] OF REAL; (* Stored Historical Actuator Command Vector [k-1] *)
    vecDeltaU : ARRAY[1..6] OF REAL; (* Rate of Change Delta Actuator Vector (u - u_prev) *)
    vecGrad : ARRAY[1..6] OF REAL; (* Projected Cost Function Analytical Gradient Vector *)
    vecX_ErrTemp : ARRAY[1..6] OF REAL; (* Temporary Vector for Projected Prediction Error *)
    vecWeightTemp : ARRAY[1..6] OF REAL; (* Temporary Vector for Weighted State Error *)
    vecU_Min : ARRAY[1..6] OF REAL; (* Hard Lower Saturation Limit Vector *)
    vecU_Max : ARRAY[1..6] OF REAL; (* Hard Upper Saturation Limit Vector *)
    vecDeltaU_Max : ARRAY[1..6] OF REAL; (* Maximum Allowable Slew-Rate Vector per Scan *)
    
    (* --- Projected Gradient Descent Optimization Parameters --- *)
    rPgdStepSize : REAL := 0.0035; (* Unrolled Gradient Step Size Alpha *)
    nIterIndex : INT := 1; (* Optimization Loop Index Variable *)
    nRow : INT := 1; (* Linear Algebra Matrix Row Loop Index *)
    nCol : INT := 1; (* Linear Algebra Matrix Column Loop Index *)
    rGradTermState : REAL := 0.0; (* Intermediate Gradient State Term Accumulator *)
    rGradTermEffort : REAL := 0.0; (* Intermediate Gradient Effort Term Accumulator *)
    rGradTermSlew : REAL := 0.0; (* Intermediate Gradient Slew Term Accumulator *)
    rDeltaVal : REAL := 0.0; (* Scalar Slew Rate Projection Delta Variable *)
    
    (* --- 2oo3 Triple Modular Redundancy Internal Diagnostics --- *)
    (* Channel 1: Optical Bell Speed Tachometer *)
    bTach_Healthy1 : BOOL := TRUE; (* Speed Sensor Channel 1 Plausibility & Health Status *)
    bTach_Healthy2 : BOOL := TRUE; (* Speed Sensor Channel 2 Plausibility & Health Status *)
    bTach_Healthy3 : BOOL := TRUE; (* Speed Sensor Channel 3 Plausibility & Health Status *)
    rTach_Diff12 : REAL := 0.0; (* Absolute Discrepancy Between Tach 1 and Tach 2 [RPM] *)
    rTach_Diff23 : REAL := 0.0; (* Absolute Discrepancy Between Tach 2 and Tach 3 [RPM] *)
    rTach_Diff31 : REAL := 0.0; (* Absolute Discrepancy Between Tach 3 and Tach 1 [RPM] *)
    rTach_DiscTimer1 : REAL := 0.0; (* Channel 1 Discrepancy Persistence Integration Timer [s] *)
    rTach_DiscTimer2 : REAL := 0.0; (* Channel 2 Discrepancy Persistence Integration Timer [s] *)
    rTach_DiscTimer3 : REAL := 0.0; (* Channel 3 Discrepancy Persistence Integration Timer [s] *)
    nTach_DegradeMode : INT := 0; (* 0: Healthy 2oo3, 1: Degraded 1oo2, 2: Simplex 1oo1, 3: Tripped *)
    rTach_PrevVoted : REAL := 0.0; (* Stored Previous Filtered Voted Turbine Speed [RPM] *)
    rTach_Selected : REAL := 0.0; (* Raw Selected Speed Prior to Smoothing Filter [RPM] *)
    
    (* Channel 2: Cascade High Voltage Divider *)
    bHV_Healthy1 : BOOL := TRUE; (* Voltage Sensor Channel 1 Plausibility & Health Status *)
    bHV_Healthy2 : BOOL := TRUE; (* Voltage Sensor Channel 2 Plausibility & Health Status *)
    bHV_Healthy3 : BOOL := TRUE; (* Voltage Sensor Channel 3 Plausibility & Health Status *)
    rHV_Diff12 : REAL := 0.0; (* Absolute Discrepancy Between HV 1 and HV 2 [kV] *)
    rHV_Diff23 : REAL := 0.0; (* Absolute Discrepancy Between HV 2 and HV 3 [kV] *)
    rHV_Diff31 : REAL := 0.0; (* Absolute Discrepancy Between HV 3 and HV 1 [kV] *)
    rHV_DiscTimer1 : REAL := 0.0; (* Channel 1 Voltage Discrepancy Persistence Timer [s] *)
    rHV_DiscTimer2 : REAL := 0.0; (* Channel 2 Voltage Discrepancy Persistence Timer [s] *)
    rHV_DiscTimer3 : REAL := 0.0; (* Channel 3 Voltage Discrepancy Persistence Timer [s] *)
    nHV_DegradeMode : INT := 0; (* 0: Healthy 2oo3, 1: Degraded 1oo2, 2: Simplex 1oo1, 3: Tripped *)
    rHV_PrevVoted : REAL := 0.0; (* Stored Previous Filtered Voted High Voltage [kV] *)
    rHV_Selected : REAL := 0.0; (* Raw Selected High Voltage Prior to Filter [kV] *)
    
    (* Channel 3: Cascade Electrostatic Output Current Shunt *)
    bCurr_Healthy1 : BOOL := TRUE; (* Current Sensor Channel 1 Plausibility & Health Status *)
    bCurr_Healthy2 : BOOL := TRUE; (* Current Sensor Channel 2 Plausibility & Health Status *)
    bCurr_Healthy3 : BOOL := TRUE; (* Current Sensor Channel 3 Plausibility & Health Status *)
    rCurr_Diff12 : REAL := 0.0; (* Absolute Discrepancy Between Current 1 and Current 2 [uA] *)
    rCurr_Diff23 : REAL := 0.0; (* Absolute Discrepancy Between Current 2 and Current 3 [uA] *)
    rCurr_Diff31 : REAL := 0.0; (* Absolute Discrepancy Between Current 3 and Current 1 [uA] *)
    rCurr_DiscTimer1 : REAL := 0.0; (* Channel 1 Current Discrepancy Persistence Timer [s] *)
    rCurr_DiscTimer2 : REAL := 0.0; (* Channel 2 Current Discrepancy Persistence Timer [s] *)
    rCurr_DiscTimer3 : REAL := 0.0; (* Channel 3 Current Discrepancy Persistence Timer [s] *)
    nCurr_DegradeMode : INT := 0; (* 0: Healthy 2oo3, 1: Degraded 1oo2, 2: Simplex 1oo1, 3: Tripped *)
    rCurr_PrevVoted : REAL := 0.0; (* Stored Previous Filtered Voted Output Current [uA] *)
    rCurr_Selected : REAL := 0.0; (* Raw Selected Output Current Prior to Filter [uA] *)
    
    (* Channel 4: Paint Fluid Metering Coriolis Flow *)
    bFlow_Healthy1 : BOOL := TRUE; (* Paint Flow Sensor Channel 1 Plausibility & Health Status *)
    bFlow_Healthy2 : BOOL := TRUE; (* Paint Flow Sensor Channel 2 Plausibility & Health Status *)
    bFlow_Healthy3 : BOOL := TRUE; (* Paint Flow Sensor Channel 3 Plausibility & Health Status *)
    rFlow_Diff12 : REAL := 0.0; (* Absolute Discrepancy Between Flow 1 and Flow 2 [cc/min] *)
    rFlow_Diff23 : REAL := 0.0; (* Absolute Discrepancy Between Flow 2 and Flow 3 [cc/min] *)
    rFlow_Diff31 : REAL := 0.0; (* Absolute Discrepancy Between Flow 3 and Flow 1 [cc/min] *)
    rFlow_DiscTimer1 : REAL := 0.0; (* Channel 1 Flow Discrepancy Persistence Timer [s] *)
    rFlow_DiscTimer2 : REAL := 0.0; (* Channel 2 Flow Discrepancy Persistence Timer [s] *)
    rFlow_DiscTimer3 : REAL := 0.0; (* Channel 3 Flow Discrepancy Persistence Timer [s] *)
    nFlow_DegradeMode : INT := 0; (* 0: Healthy 2oo3, 1: Degraded 1oo2, 2: Simplex 1oo1, 3: Tripped *)
    rFlow_PrevVoted : REAL := 0.0; (* Stored Previous Filtered Voted Paint Flow Rate [cc/min] *)
    rFlow_Selected : REAL := 0.0; (* Raw Selected Paint Flow Rate Prior to Filter [cc/min] *)
    
    (* --- Fast Electrostatic Spark Precursor Detection Variables --- *)
    rCurrRateOfChange : REAL := 0.0; (* Numerical Differential Current Derivative dI/dt [uA/s] *)
    rVoltRateOfChange : REAL := 0.0; (* Numerical Differential Voltage Derivative dV/dt [kV/s] *)
    rPrevCurrentSample : REAL := 0.0; (* High-Speed Sample of Current in Prior Scan [uA] *)
    rPrevVoltageSample : REAL := 0.0; (* High-Speed Sample of Voltage in Prior Scan [kV] *)
    bSparkQuenchTriggered : BOOL := FALSE; (* Fast Solid-State Crowbar Quench Latch Flag *)
    rSparkQuenchTimer : REAL := 0.0; (* Quench Duration and Post-Discharge Recovery Timer [s] *)
    
    (* --- First-Principles Physics Intermediate Equations --- *)
    rOmegaRadPerSec : REAL := 0.0; (* Bell Cup Angular Rotational Speed [rad/s] *)
    rCupTipVelocity : REAL := 0.0; (* Peripheral Linear Velocity of Bell Cup Rim [m/s] *)
    rPaintFilmThickness : REAL := 0.0; (* Dynamic Liquid Film Thickness Under Centrifugal Spreading [m] *)
    rShearRateCupRim : REAL := 0.0; (* High-Shear Deformation Rate at Outer Atomizing Serrations [1/s] *)
    rApparentViscosity : REAL := 0.0; (* Non-Newtonian Shear-Thinned Apparent Viscosity [Pa.s] *)
    rCentrifugalTorque : REAL := 0.0; (* Dynamic Mechanical Torque Load Imparted by Fluid Acceleration [N.m] *)
    rAerodynamicTorque : REAL := 0.0; (* Turbulent Air Drag Resistance Torque on Cup Face [N.m] *)
    rBearingDragTorque : REAL := 0.0; (* Laminar Shearing Friction Torque of Pressurized Air Film [N.m] *)
    rNetTurbineTorque : REAL := 0.0; (* Net Effective Accelerating Shaft Torque on Turbine Wheel [N.m] *)
    rDynamicBearingLoad : REAL := 0.0; (* Spindle Aerodynamic Air Bearing Radial/Axial Load Index [N] *)
    
    rWeberNumber : REAL := 0.0; (* Centrifugal Weber Dimensionless Grouping (Inertia vs Surface Tension) *)
    rOhnesorgeNumber : REAL := 0.0; (* Ohnesorge Dimensionless Grouping (Viscosity vs Surface Tension) *)
    rFlowNumber : REAL := 0.0; (* Normalized Liquid Flow Volumetric Dimensionless Coefficient *)
    rRawDropletSMD : REAL := 0.0; (* Unfiltered First-Principles Sauter Mean Diameter [um] *)
    
    rElectricFieldE0 : REAL := 0.0; (* Bulk Standoff Electrostatic Electric Field Magnitude [kV/m] *)
    rSpaceChargeDensity : REAL := 0.0; (* Space-Charge Ionized Aerosol Cloud Volume Charge Density [C/m3] *)
    rDropletSpecificCharge : REAL := 0.0; (* Charge-to-Mass Ratio of Saturated Atomized Droplets [C/kg] *)
    rCoulombicDriftVelocity : REAL := 0.0; (* Electrostatic Migration Velocity Towards Grounded Panel [m/s] *)
    rTransferEffCalc : REAL := 0.0; (* Unfiltered Electrostatic Transfer Efficiency Percentage [%] *)
    
    rInnerAirJetVelocity : REAL := 0.0; (* Inner Shaping Air SA1 Jet Orifice Velocity [m/s] *)
    rOuterAirJetVelocity : REAL := 0.0; (* Outer Shaping Air SA2 Jet Orifice Velocity [m/s] *)
    rInnerAirMomentumFlux : REAL := 0.0; (* Dynamic Momentum Flux of Inner Shroud Jet [N] *)
    rOuterAirMomentumFlux : REAL := 0.0; (* Dynamic Momentum Flux of Outer Shroud Jet [N] *)
    rPaintRadialMomentum : REAL := 0.0; (* Centrifugal Radial Momentum Flux of Ejected Paint Droplets [N] *)
    rShroudMomentumRatio : REAL := 0.0; (* Aerodynamic Shroud Momentum Deflection Ratio [dimensionless] *)
    rRawPatternWidth : REAL := 0.0; (* Unfiltered Spray Pattern Fan Deposition Width [mm] *)
    rEdgeSharpnessCalc : REAL := 0.0; (* Unfiltered Spray Boundary Sharpness Gradient [N/m2] *)
    rVortexContainmentIndex : REAL := 0.0; (* Shroud Vortex Containment Stability Ratio [dimensionless] *)
    
    (* --- Dynamic Path Cornering Feedforward Modulators --- *)
    rCorneringFlowBoostFactor : REAL := 1.0; (* Dynamic Multiplier for Paint Metering Flow Rate *)
    rCorneringPatternTrim : REAL := 0.0; (* Additive Fan Width Narrowing Trim for Sharp Contours [mm] *)
    rCorneringSpeedOffset : REAL := 0.0; (* Additive Bell Turbine RPM Trim for Droplet Centrifugal Shear [RPM] *)
    rCorneringAirShroudTrim : REAL := 0.0; (* Additive Shaping Air Pressure Boost for Droplet Inertia Containment [%] *)
    
    (* --- ISA-18.2 Multi-Tier Process Alarm Trip Setpoints & Hysteresis --- *)
    rTrip_Speed_HH : REAL := 68000.0; (* Bell Turbine Rotational Speed High-High Catastrophic Limit [RPM] *)
    rTrip_Speed_H : REAL := 62000.0; (* Bell Turbine Rotational Speed High Warning Threshold [RPM] *)
    rTrip_Speed_L : REAL := 18000.0; (* Bell Turbine Rotational Speed Low Warning Threshold [RPM] *)
    rTrip_Speed_LL : REAL := 12000.0; (* Bell Turbine Rotational Speed Low-Low Stall Limit [RPM] *)
    rDeadband_Speed : REAL := 800.0; (* Speed Alarm Hysteresis Deadband [RPM] *)
    
    rTrip_HV_HH : REAL := 95.0; (* High Voltage Cascade High-High Overvoltage Trip Limit [kV] *)
    rTrip_HV_H : REAL := 88.0; (* High Voltage Cascade High Warning Setpoint [kV] *)
    rTrip_HV_L : REAL := 25.0; (* High Voltage Cascade Low Warning Setpoint [kV] *)
    rTrip_HV_LL : REAL := 10.0; (* High Voltage Cascade Low-Low Field Collapse Trip Limit [kV] *)
    rDeadband_HV : REAL := 2.0; (* High Voltage Alarm Hysteresis Deadband [kV] *)
    
    rTrip_Curr_HH : REAL := 380.0; (* Cascade Discharge Current High-High Spark Precursor Trip [uA] *)
    rTrip_Curr_H : REAL := 300.0; (* Cascade Discharge Current High Pre-Spark Warning [uA] *)
    rTrip_Curr_L : REAL := 5.0; (* Cascade Discharge Current Low Under-Current Warning [uA] *)
    rTrip_Curr_LL : REAL := 1.0; (* Cascade Discharge Current Low-Low Disconnection Trip [uA] *)
    rDeadband_Curr : REAL := 10.0; (* Current Alarm Hysteresis Deadband [uA] *)
    
    rTrip_Flow_HH : REAL := 650.0; (* Paint Delivery Flow High-High Over-Delivery Trip [cc/min] *)
    rTrip_Flow_H : REAL := 550.0; (* Paint Delivery Flow High Process Warning [cc/min] *)
    rTrip_Flow_L : REAL := 45.0; (* Paint Delivery Flow Low Under-Delivery Warning [cc/min] *)
    rTrip_Flow_LL : REAL := 15.0; (* Paint Delivery Flow Low-Low Dry-Run Cavitation Trip [cc/min] *)
    rDeadband_Flow : REAL := 8.0; (* Paint Delivery Flow Alarm Hysteresis Deadband [cc/min] *)
    
    rTrip_Bearing_HH : REAL := 8.5; (* Spindle Aerodynamic Bearing Lift Pressure High-High Trip [bar] *)
    rTrip_Bearing_H : REAL := 7.5; (* Spindle Aerodynamic Bearing Lift Pressure High Warning [bar] *)
    rTrip_Bearing_L : REAL := 5.2; (* Spindle Aerodynamic Bearing Lift Pressure Low Warning [bar] *)
    rTrip_Bearing_LL : REAL := 4.6; (* Spindle Aerodynamic Bearing Lift Pressure Low-Low Crash Trip [bar] *)
    rDeadband_Bearing : REAL := 0.2; (* Bearing Pressure Alarm Hysteresis Deadband [bar] *)
    
    rTrip_Shaping_HH : REAL := 7.2; (* Dual Shaping Air Supply Header Pressure High-High Trip [bar] *)
    rTrip_Shaping_H : REAL := 6.4; (* Dual Shaping Air Supply Header Pressure High Warning [bar] *)
    rTrip_Shaping_L : REAL := 4.2; (* Dual Shaping Air Supply Header Pressure Low Warning [bar] *)
    rTrip_Shaping_LL : REAL := 3.4; (* Dual Shaping Air Supply Header Pressure Low-Low Shroud Loss [bar] *)
    rDeadband_Shaping : REAL := 0.25; (* Shaping Air Alarm Hysteresis Deadband [bar] *)
    
    rTrip_Booth_HH : REAL := 0.65; (* Spray Booth Down-Draft Air Velocity High-High Turbulence Trip [m/s] *)
    rTrip_Booth_H : REAL := 0.52; (* Spray Booth Down-Draft Air Velocity High Warning [m/s] *)
    rTrip_Booth_L : REAL := 0.22; (* Spray Booth Down-Draft Air Velocity Low Warning [m/s] *)
    rTrip_Booth_LL : REAL := 0.15; (* Spray Booth Down-Draft Air Velocity Low-Low Stagnation Trip [m/s] *)
    rDeadband_Booth : REAL := 0.03; (* Booth Velocity Alarm Hysteresis Deadband [m/s] *)
    
    (* --- Internal Discrete Alarm Latches & State Flags --- *)
    bAlarm_Speed_HH : BOOL := FALSE;
    bAlarm_Speed_H : BOOL := FALSE;
    bAlarm_Speed_L : BOOL := FALSE;
    bAlarm_Speed_LL : BOOL := FALSE;
    
    bAlarm_HV_HH : BOOL := FALSE;
    bAlarm_HV_H : BOOL := FALSE;
    bAlarm_HV_L : BOOL := FALSE;
    bAlarm_HV_LL : BOOL := FALSE;
    
    bAlarm_Curr_HH : BOOL := FALSE;
    bAlarm_Curr_H : BOOL := FALSE;
    bAlarm_Curr_L : BOOL := FALSE;
    bAlarm_Curr_LL : BOOL := FALSE;
    
    bAlarm_Flow_HH : BOOL := FALSE;
    bAlarm_Flow_H : BOOL := FALSE;
    bAlarm_Flow_L : BOOL := FALSE;
    bAlarm_Flow_LL : BOOL := FALSE;
    
    bAlarm_Bearing_HH : BOOL := FALSE;
    bAlarm_Bearing_H : BOOL := FALSE;
    bAlarm_Bearing_L : BOOL := FALSE;
    bAlarm_Bearing_LL : BOOL := FALSE;
    
    bAlarm_Shaping_HH : BOOL := FALSE;
    bAlarm_Shaping_H : BOOL := FALSE;
    bAlarm_Shaping_L : BOOL := FALSE;
    bAlarm_Shaping_LL : BOOL := FALSE;
    
    bAlarm_Booth_HH : BOOL := FALSE;
    bAlarm_Booth_H : BOOL := FALSE;
    bAlarm_Booth_L : BOOL := FALSE;
    bAlarm_Booth_LL : BOOL := FALSE;
    
    (* --- TMR Discrepancy Calibration Thresholds --- *)
    rTach_DiscThreshold : REAL := 2500.0; (* Speed Sensor Allowable Cross-Channel Tolerance [RPM] *)
    rHV_DiscThreshold : REAL := 4.5; (* High Voltage Sensor Cross-Channel Tolerance [kV] *)
    rCurr_DiscThreshold : REAL := 25.0; (* Cascade Current Sensor Cross-Channel Tolerance [uA] *)
    rFlow_DiscThreshold : REAL := 20.0; (* Paint Delivery Flow Sensor Cross-Channel Tolerance [cc/min] *)
    rDiscPersistTimeLimit : REAL := 0.25; (* Debounce Integration Threshold to Latch Channel Failure [s] *)
END_VAR

(* ==================================================================================================== *)
(* PHASE 0: ONE-SHOT CYBER-PHYSICAL STATE-SPACE ALLOCATION & PARAMETER INITIALIZATION                   *)
(* ==================================================================================================== *)
IF bFirstScan THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* Discrete State-Space Model Definition (x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k])   *)
    (* Sample Period Ts = 0.002 s (500 Hz). Derived via zero-order hold discretization of coupled ODEs  *)
    (* ------------------------------------------------------------------------------------------------ *)
    (* Row 1: Bell Turbine Speed & Air Bearing Dynamic Load [RPM] *)
    matA[1, 1] := 0.98520; matA[1, 2] := 0.00000; matA[1, 3] := 0.00000; matA[1, 4] := 0.00000; matA[1, 5] := -0.04120; matA[1, 6] := 0.00000;
    (* Row 2: Droplet Sauter Mean Diameter (SMD d32) Atomization [um] *)
    matA[2, 1] := -0.00340; matA[2, 2] := 0.94150; matA[2, 3] := 0.00000; matA[2, 4] := 0.00000; matA[2, 5] := 0.02850; matA[2, 6] := 0.00000;
    (* Row 3: Electrostatic Transfer Efficiency & Space Charge Potential [%] *)
    matA[3, 1] := 0.00180; matA[3, 2] := -0.01250; matA[3, 3] := 0.96200; matA[3, 4] := 0.00000; matA[3, 5] := -0.00550; matA[3, 6] := 0.00820;
    (* Row 4: Shroud Spray Pattern Fan Width & Edge Sharpness [mm, N/m2] *)
    matA[4, 1] := 0.00620; matA[4, 2] := 0.00000; matA[4, 3] := 0.00000; matA[4, 4] := 0.93500; matA[4, 5] := 0.01400; matA[4, 6] := -0.08500;
    (* Row 5: Paint Delivery Dynamic Pressure & Metering Flow Rate [bar, cc/min] *)
    matA[5, 1] := 0.00000; matA[5, 2] := 0.00000; matA[5, 3] := 0.00000; matA[5, 4] := 0.00000; matA[5, 5] := 0.92400; matA[5, 6] := 0.00000;
    (* Row 6: Booth Downdraft Laminar Airflow Velocity & Relative Humidity [m/s, % RH] *)
    matA[6, 1] := 0.00000; matA[6, 2] := 0.00000; matA[6, 3] := 0.00000; matA[6, 4] := 0.00450; matA[6, 5] := 0.00000; matA[6, 6] := 0.95800;
    
    (* Control Input Actuation Matrix B (6x6 Couplings to Physical Proportional Actuators) *)
    (* u[1]: Drive Air Valve [%], u[2]: HV Cascade [kV], u[3]: Inner SA1 [%], u[4]: Outer SA2 [%], u[5]: Gear Pump [RPM], u[6]: Pressure Reg [%] *)
    matB[1, 1] := 14.8500; matB[1, 2] := 0.00000; matB[1, 3] := 0.00000; matB[1, 4] := 0.00000; matB[1, 5] := -0.01200; matB[1, 6] := 0.00000;
    matB[2, 1] := -0.01850; matB[2, 2] := -0.00450; matB[2, 3] := 0.00000; matB[2, 4] := 0.00000; matB[2, 5] := 0.01500; matB[2, 6] := 0.00000;
    matB[3, 1] := 0.00220; matB[3, 2] := 0.08500; matB[3, 3] := 0.00000; matB[3, 4] := 0.00000; matB[3, 5] := -0.00800; matB[3, 6] := 0.00000;
    matB[4, 1] := 0.02100; matB[4, 2] := 0.00000; matB[4, 3] := -0.42500; matB[4, 4] := -0.68000; matB[4, 5] := 0.03500; matB[4, 6] := 0.00000;
    matB[5, 1] := 0.00000; matB[5, 2] := 0.00000; matB[5, 3] := 0.00000; matB[5, 4] := 0.00000; matB[5, 5] := 1.18500; matB[5, 6] := 0.14200;
    matB[6, 1] := 0.00000; matB[6, 2] := 0.00000; matB[6, 3] := 0.03800; matB[6, 4] := 0.05400; matB[6, 5] := 0.00000; matB[6, 6] := 0.00000;
    
    (* Sensor Output Measurement Matrix C (6x6 Direct Identity Map to Virtual Observers) *)
    matC[1, 1] := 1.0000; matC[1, 2] := 0.0000; matC[1, 3] := 0.0000; matC[1, 4] := 0.0000; matC[1, 5] := 0.0000; matC[1, 6] := 0.0000;
    matC[2, 1] := 0.0000; matC[2, 2] := 1.0000; matC[2, 3] := 0.0000; matC[2, 4] := 0.0000; matC[2, 5] := 0.0000; matC[2, 6] := 0.0000;
    matC[3, 1] := 0.0000; matC[3, 2] := 0.0000; matC[3, 3] := 1.0000; matC[3, 4] := 0.0000; matC[3, 5] := 0.0000; matC[3, 6] := 0.0000;
    matC[4, 1] := 0.0000; matC[4, 2] := 0.0000; matC[4, 3] := 0.0000; matC[4, 4] := 1.0000; matC[4, 5] := 0.0000; matC[4, 6] := 0.0000;
    matC[5, 1] := 0.0000; matC[5, 2] := 0.0000; matC[5, 3] := 0.0000; matC[5, 4] := 0.0000; matC[5, 5] := 1.0000; matC[5, 6] := 0.0000;
    matC[6, 1] := 0.0000; matC[6, 2] := 0.0000; matC[6, 3] := 0.0000; matC[6, 4] := 0.0000; matC[6, 5] := 0.0000; matC[6, 6] := 1.0000;
    
    (* Direct Feedthrough Transmission Matrix D (Strictly Zero D-Matrix) *)
    matD[1, 1] := 0.0; matD[1, 2] := 0.0; matD[1, 3] := 0.0; matD[1, 4] := 0.0; matD[1, 5] := 0.0; matD[1, 6] := 0.0;
    matD[2, 1] := 0.0; matD[2, 2] := 0.0; matD[2, 3] := 0.0; matD[2, 4] := 0.0; matD[2, 5] := 0.0; matD[2, 6] := 0.0;
    matD[3, 1] := 0.0; matD[3, 2] := 0.0; matD[3, 3] := 0.0; matD[3, 4] := 0.0; matD[3, 5] := 0.0; matD[3, 6] := 0.0;
    matD[4, 1] := 0.0; matD[4, 2] := 0.0; matD[4, 3] := 0.0; matD[4, 4] := 0.0; matD[4, 5] := 0.0; matD[4, 6] := 0.0;
    matD[5, 1] := 0.0; matD[5, 2] := 0.0; matD[5, 3] := 0.0; matD[5, 4] := 0.0; matD[5, 5] := 0.0; matD[5, 6] := 0.0;
    matD[6, 1] := 0.0; matD[6, 2] := 0.0; matD[6, 3] := 0.0; matD[6, 4] := 0.0; matD[6, 5] := 0.0; matD[6, 6] := 0.0;
    
    (* Luenberger Observer Matrix L (Poles Assigned for Asymptotic Innovation Convergence) *)
    matL[1, 1] := 0.1850; matL[1, 2] := 0.0000; matL[1, 3] := 0.0000; matL[1, 4] := 0.0000; matL[1, 5] := -0.0150; matL[1, 6] := 0.0000;
    matL[2, 1] := -0.0012; matL[2, 2] := 0.2240; matL[2, 3] := 0.0000; matL[2, 4] := 0.0000; matL[2, 5] := 0.0085; matL[2, 6] := 0.0000;
    matL[3, 1] := 0.0008; matL[3, 2] := -0.0045; matL[3, 3] := 0.2100; matL[3, 4] := 0.0000; matL[3, 5] := -0.0022; matL[3, 6] := 0.0035;
    matL[4, 1] := 0.0025; matL[4, 2] := 0.0000; matL[4, 3] := 0.0000; matL[4, 4] := 0.2450; matL[4, 5] := 0.0062; matL[4, 6] := -0.0320;
    matL[5, 1] := 0.0000; matL[5, 2] := 0.0000; matL[5, 3] := 0.0000; matL[5, 4] := 0.0000; matL[5, 5] := 0.2850; matL[5, 6] := 0.0000;
    matL[6, 1] := 0.0000; matL[6, 2] := 0.0000; matL[6, 3] := 0.0000; matL[6, 4] := 0.0018; matL[6, 5] := 0.0000; matL[6, 6] := 0.1950;
    
    (* Model Predictive Control (MPC) State Tracking Penalty Matrix Q *)
    matQ[1, 1] := 0.0015; matQ[1, 2] := 0.0; matQ[1, 3] := 0.0; matQ[1, 4] := 0.0; matQ[1, 5] := 0.0; matQ[1, 6] := 0.0;
    matQ[2, 1] := 0.0; matQ[2, 2] := 18.500; matQ[2, 3] := 0.0; matQ[2, 4] := 0.0; matQ[2, 5] := 0.0; matQ[2, 6] := 0.0;
    matQ[3, 1] := 0.0; matQ[3, 2] := 0.0; matQ[3, 3] := 8.250; matQ[3, 4] := 0.0; matQ[3, 5] := 0.0; matQ[3, 6] := 0.0;
    matQ[4, 1] := 0.0; matQ[4, 2] := 0.0; matQ[4, 3] := 0.0; matQ[4, 4] := 2.650; matQ[4, 5] := 0.0; matQ[4, 6] := 0.0;
    matQ[5, 1] := 0.0; matQ[5, 2] := 0.0; matQ[5, 3] := 0.0; matQ[5, 4] := 0.0; matQ[5, 5] := 0.085; matQ[5, 6] := 0.0;
    matQ[6, 1] := 0.0; matQ[6, 2] := 0.0; matQ[6, 3] := 0.0; matQ[6, 4] := 0.0; matQ[6, 5] := 0.0; matQ[6, 6] := 12.000;
    
    (* MPC Control Effort Penalty Matrix R *)
    matR[1, 1] := 0.045; matR[1, 2] := 0.0; matR[1, 3] := 0.0; matR[1, 4] := 0.0; matR[1, 5] := 0.0; matR[1, 6] := 0.0;
    matR[2, 1] := 0.0; matR[2, 2] := 0.025; matR[2, 3] := 0.0; matR[2, 4] := 0.0; matR[2, 5] := 0.0; matR[2, 6] := 0.0;
    matR[3, 1] := 0.0; matR[3, 2] := 0.0; matR[3, 3] := 0.035; matR[3, 4] := 0.0; matR[3, 5] := 0.0; matR[3, 6] := 0.0;
    matR[4, 1] := 0.0; matR[4, 2] := 0.0; matR[4, 3] := 0.0; matR[4, 4] := 0.035; matR[4, 5] := 0.0; matR[4, 6] := 0.0;
    matR[5, 1] := 0.0; matR[5, 2] := 0.0; matR[5, 3] := 0.0; matR[5, 4] := 0.0; matR[5, 5] := 0.055; matR[5, 6] := 0.0;
    matR[6, 1] := 0.0; matR[6, 2] := 0.0; matR[6, 3] := 0.0; matR[6, 4] := 0.0; matR[6, 5] := 0.0; matR[6, 6] := 0.020;
    
    (* MPC Actuator Slew Rate Smoothness Penalty Matrix S *)
    matS[1, 1] := 0.120; matS[1, 2] := 0.0; matS[1, 3] := 0.0; matS[1, 4] := 0.0; matS[1, 5] := 0.0; matS[1, 6] := 0.0;
    matS[2, 1] := 0.0; matS[2, 2] := 0.080; matS[2, 3] := 0.0; matS[2, 4] := 0.0; matS[2, 5] := 0.0; matS[2, 6] := 0.0;
    matS[3, 1] := 0.0; matS[3, 2] := 0.0; matS[3, 3] := 0.095; matS[3, 4] := 0.0; matS[3, 5] := 0.0; matS[3, 6] := 0.0;
    matS[4, 1] := 0.0; matS[4, 2] := 0.0; matS[4, 3] := 0.0; matS[4, 4] := 0.095; matS[4, 5] := 0.0; matS[4, 6] := 0.0;
    matS[5, 1] := 0.0; matS[5, 2] := 0.0; matS[5, 3] := 0.0; matS[5, 4] := 0.0; matS[5, 5] := 0.150; matS[5, 6] := 0.0;
    matS[6, 1] := 0.0; matS[6, 2] := 0.0; matS[6, 3] := 0.0; matS[6, 4] := 0.0; matS[6, 5] := 0.0; matS[6, 6] := 0.060;
    
    (* MPC Terminal Prediction Penalty Matrix P (Discrete Algebraic Riccati Equation Approximation) *)
    matP[1, 1] := 0.0035; matP[1, 2] := 0.0; matP[1, 3] := 0.0; matP[1, 4] := 0.0; matP[1, 5] := 0.0; matP[1, 6] := 0.0;
    matP[2, 1] := 0.0; matP[2, 2] := 35.000; matP[2, 3] := 0.0; matP[2, 4] := 0.0; matP[2, 5] := 0.0; matP[2, 6] := 0.0;
    matP[3, 1] := 0.0; matP[3, 2] := 0.0; matP[3, 3] := 16.500; matP[3, 4] := 0.0; matP[3, 5] := 0.0; matP[3, 6] := 0.0;
    matP[4, 1] := 0.0; matP[4, 2] := 0.0; matP[4, 3] := 0.0; matP[4, 4] := 5.800; matP[4, 5] := 0.0; matP[4, 6] := 0.0;
    matP[5, 1] := 0.0; matP[5, 2] := 0.0; matP[5, 3] := 0.0; matP[5, 4] := 0.0; matP[5, 5] := 0.190; matP[5, 6] := 0.0;
    matP[6, 1] := 0.0; matP[6, 2] := 0.0; matP[6, 3] := 0.0; matP[6, 4] := 0.0; matP[6, 5] := 0.0; matP[6, 6] := 25.000;
    
    (* Physical Actuation Saturation & Slew Bounds *)
    vecU_Min[1] := 0.0;   vecU_Max[1] := 100.0; vecDeltaU_Max[1] := 2.5;  (* Turbine Drive Air Valve [%] *)
    vecU_Min[2] := 0.0;   vecU_Max[2] := 100.0; vecDeltaU_Max[2] := 3.0;  (* High-Voltage Cascade [kV] *)
    vecU_Min[3] := 0.0;   vecU_Max[3] := 100.0; vecDeltaU_Max[3] := 3.5;  (* Inner Shaping Air Valve [%] *)
    vecU_Min[4] := 0.0;   vecU_Max[4] := 100.0; vecDeltaU_Max[4] := 3.5;  (* Outer Shaping Air Valve [%] *)
    vecU_Min[5] := 0.0;   vecU_Max[5] := 320.0; vecDeltaU_Max[5] := 8.0;  (* Paint Micro-Gear Pump [RPM] *)
    vecU_Min[6] := 0.0;   vecU_Max[6] := 100.0; vecDeltaU_Max[6] := 4.0;  (* Paint Dynamic Pressure Reg [%] *)
    
    (* Reset State Vector and Observer Memory Registers *)
    FOR nRow := 1 TO 6 DO
        vecX_Hat[nRow] := 0.0;
        vecX_Pred[nRow] := 0.0;
        vecX_Ref[nRow] := 0.0;
        vecY_Meas[nRow] := 0.0;
        vecY_Est[nRow] := 0.0;
        vecObsErr[nRow] := 0.0;
        vecU_Opt[nRow] := 0.0;
        vecU_Prev[nRow] := 0.0;
        vecDeltaU[nRow] := 0.0;
        vecGrad[nRow] := 0.0;
        vecX_ErrTemp[nRow] := 0.0;
        vecWeightTemp[nRow] := 0.0;
    END_FOR;
    
    bFirstScan := FALSE;
END_IF;

(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS            *)
(* ==================================================================================================== *)
(* ---------------------------------------------------------------------------------------------------- *)
(* CHANNEL 1: Bell Air-Turbine Rotational Speed Tachometers (Optical, Magnetic, Back-EMF) [RPM]         *)
(* ---------------------------------------------------------------------------------------------------- *)
bTach_Healthy1 := (rTach_Raw1 >= 0.0) AND (rTach_Raw1 <= 75000.0);
bTach_Healthy2 := (rTach_Raw2 >= 0.0) AND (rTach_Raw2 <= 75000.0);
bTach_Healthy3 := (rTach_Raw3 >= 0.0) AND (rTach_Raw3 <= 75000.0);
rTach_Diff12 := ABS(rTach_Raw1 - rTach_Raw2);
rTach_Diff23 := ABS(rTach_Raw2 - rTach_Raw3);
rTach_Diff31 := ABS(rTach_Raw3 - rTach_Raw1);

(* Discrepancy accumulation timer for Tachometer Channel 1 *)
IF (rTach_Diff12 > rTach_DiscThreshold) AND (rTach_Diff31 > rTach_DiscThreshold) THEN
    rTach_DiscTimer1 := rTach_DiscTimer1 + rCycleTime;
    IF rTach_DiscTimer1 >= rDiscPersistTimeLimit THEN
        bTach_Healthy1 := FALSE;
    END_IF;
ELSE
    rTach_DiscTimer1 := MAX(0.0, rTach_DiscTimer1 - (rCycleTime * 0.5));
END_IF;

(* Discrepancy accumulation timer for Tachometer Channel 2 *)
IF (rTach_Diff12 > rTach_DiscThreshold) AND (rTach_Diff23 > rTach_DiscThreshold) THEN
    rTach_DiscTimer2 := rTach_DiscTimer2 + rCycleTime;
    IF rTach_DiscTimer2 >= rDiscPersistTimeLimit THEN
        bTach_Healthy2 := FALSE;
    END_IF;
ELSE
    rTach_DiscTimer2 := MAX(0.0, rTach_DiscTimer2 - (rCycleTime * 0.5));
END_IF;

(* Discrepancy accumulation timer for Tachometer Channel 3 *)
IF (rTach_Diff23 > rTach_DiscThreshold) AND (rTach_Diff31 > rTach_DiscThreshold) THEN
    rTach_DiscTimer3 := rTach_DiscTimer3 + rCycleTime;
    IF rTach_DiscTimer3 >= rDiscPersistTimeLimit THEN
        bTach_Healthy3 := FALSE;
    END_IF;
ELSE
    rTach_DiscTimer3 := MAX(0.0, rTach_DiscTimer3 - (rCycleTime * 0.5));
END_IF;

(* Degraded voting arbitration for Tachometer Channels *)
IF bTach_Healthy1 AND bTach_Healthy2 AND bTach_Healthy3 THEN
    nTach_DegradeMode := 0; (* Nominal 2oo3 Median Voting *)
    IF ((rTach_Raw1 >= rTach_Raw2) AND (rTach_Raw1 <= rTach_Raw3)) OR ((rTach_Raw1 <= rTach_Raw2) AND (rTach_Raw1 >= rTach_Raw3)) THEN
        rTach_Selected := rTach_Raw1;
    ELSIF ((rTach_Raw2 >= rTach_Raw1) AND (rTach_Raw2 <= rTach_Raw3)) OR ((rTach_Raw2 <= rTach_Raw1) AND (rTach_Raw2 >= rTach_Raw3)) THEN
        rTach_Selected := rTach_Raw2;
    ELSE
        rTach_Selected := rTach_Raw3;
    END_IF;
ELSIF bTach_Healthy1 AND bTach_Healthy2 THEN
    nTach_DegradeMode := 1; (* Degraded 1oo2 Dual Sensor Mean *)
    rTach_Selected := (rTach_Raw1 + rTach_Raw2) * 0.5;
ELSIF bTach_Healthy2 AND bTach_Healthy3 THEN
    nTach_DegradeMode := 1; (* Degraded 1oo2 Dual Sensor Mean *)
    rTach_Selected := (rTach_Raw2 + rTach_Raw3) * 0.5;
ELSIF bTach_Healthy1 AND bTach_Healthy3 THEN
    nTach_DegradeMode := 1; (* Degraded 1oo2 Dual Sensor Mean *)
    rTach_Selected := (rTach_Raw1 + rTach_Raw3) * 0.5;
ELSIF bTach_Healthy1 THEN
    nTach_DegradeMode := 2; (* Simplex 1oo1 Failsafe Single Sensor *)
    rTach_Selected := rTach_Raw1;
ELSIF bTach_Healthy2 THEN
    nTach_DegradeMode := 2; (* Simplex 1oo1 Failsafe Single Sensor *)
    rTach_Selected := rTach_Raw2;
ELSIF bTach_Healthy3 THEN
    nTach_DegradeMode := 2; (* Simplex 1oo1 Failsafe Single Sensor *)
    rTach_Selected := rTach_Raw3;
ELSE
    nTach_DegradeMode := 3; (* Complete Sensor Tripped Mode *)
    rTach_Selected := rTach_PrevVoted;
END_IF;
(* Bumpless exponential smoothing filter on voted speed *)
rVotedTurbineSpeed := rTach_PrevVoted + (0.28 * (rTach_Selected - rTach_PrevVoted));
rTach_PrevVoted := rVotedTurbineSpeed;

(* ---------------------------------------------------------------------------------------------------- *)
(* CHANNEL 2: High Voltage Divider Feedback Sensors (Resistor String Transducers) [kV]                  *)
(* ---------------------------------------------------------------------------------------------------- *)
bHV_Healthy1 := (rHV_Volt_Raw1 >= 0.0) AND (rHV_Volt_Raw1 <= 110.0);
bHV_Healthy2 := (rHV_Volt_Raw2 >= 0.0) AND (rHV_Volt_Raw2 <= 110.0);
bHV_Healthy3 := (rHV_Volt_Raw3 >= 0.0) AND (rHV_Volt_Raw3 <= 110.0);
rHV_Diff12 := ABS(rHV_Volt_Raw1 - rHV_Volt_Raw2);
rHV_Diff23 := ABS(rHV_Volt_Raw2 - rHV_Volt_Raw3);
rHV_Diff31 := ABS(rHV_Volt_Raw3 - rHV_Volt_Raw1);

IF (rHV_Diff12 > rHV_DiscThreshold) AND (rHV_Diff31 > rHV_DiscThreshold) THEN
    rHV_DiscTimer1 := rHV_DiscTimer1 + rCycleTime;
    IF rHV_DiscTimer1 >= rDiscPersistTimeLimit THEN
        bHV_Healthy1 := FALSE;
    END_IF;
ELSE
    rHV_DiscTimer1 := MAX(0.0, rHV_DiscTimer1 - (rCycleTime * 0.5));
END_IF;

IF (rHV_Diff12 > rHV_DiscThreshold) AND (rHV_Diff23 > rHV_DiscThreshold) THEN
    rHV_DiscTimer2 := rHV_DiscTimer2 + rCycleTime;
    IF rHV_DiscTimer2 >= rDiscPersistTimeLimit THEN
        bHV_Healthy2 := FALSE;
    END_IF;
ELSE
    rHV_DiscTimer2 := MAX(0.0, rHV_DiscTimer2 - (rCycleTime * 0.5));
END_IF;

IF (rHV_Diff23 > rHV_DiscThreshold) AND (rHV_Diff31 > rHV_DiscThreshold) THEN
    rHV_DiscTimer3 := rHV_DiscTimer3 + rCycleTime;
    IF rHV_DiscTimer3 >= rDiscPersistTimeLimit THEN
        bHV_Healthy3 := FALSE;
    END_IF;
ELSE
    rHV_DiscTimer3 := MAX(0.0, rHV_DiscTimer3 - (rCycleTime * 0.5));
END_IF;

IF bHV_Healthy1 AND bHV_Healthy2 AND bHV_Healthy3 THEN
    nHV_DegradeMode := 0;
    IF ((rHV_Volt_Raw1 >= rHV_Volt_Raw2) AND (rHV_Volt_Raw1 <= rHV_Volt_Raw3)) OR ((rHV_Volt_Raw1 <= rHV_Volt_Raw2) AND (rHV_Volt_Raw1 >= rHV_Volt_Raw3)) THEN
        rHV_Selected := rHV_Volt_Raw1;
    ELSIF ((rHV_Volt_Raw2 >= rHV_Volt_Raw1) AND (rHV_Volt_Raw2 <= rHV_Volt_Raw3)) OR ((rHV_Volt_Raw2 <= rHV_Volt_Raw1) AND (rHV_Volt_Raw2 >= rHV_Volt_Raw3)) THEN
        rHV_Selected := rHV_Volt_Raw2;
    ELSE
        rHV_Selected := rHV_Volt_Raw3;
    END_IF;
ELSIF bHV_Healthy1 AND bHV_Healthy2 THEN
    nHV_DegradeMode := 1;
    rHV_Selected := (rHV_Volt_Raw1 + rHV_Volt_Raw2) * 0.5;
ELSIF bHV_Healthy2 AND bHV_Healthy3 THEN
    nHV_DegradeMode := 1;
    rHV_Selected := (rHV_Volt_Raw2 + rHV_Volt_Raw3) * 0.5;
ELSIF bHV_Healthy1 AND bHV_Healthy3 THEN
    nHV_DegradeMode := 1;
    rHV_Selected := (rHV_Volt_Raw1 + rHV_Volt_Raw3) * 0.5;
ELSIF bHV_Healthy1 THEN
    nHV_DegradeMode := 2;
    rHV_Selected := rHV_Volt_Raw1;
ELSIF bHV_Healthy2 THEN
    nHV_DegradeMode := 2;
    rHV_Selected := rHV_Volt_Raw2;
ELSIF bHV_Healthy3 THEN
    nHV_DegradeMode := 2;
    rHV_Selected := rHV_Volt_Raw3;
ELSE
    nHV_DegradeMode := 3;
    rHV_Selected := rHV_PrevVoted;
END_IF;
rVotedHighVoltage := rHV_PrevVoted + (0.32 * (rHV_Selected - rHV_PrevVoted));
rHV_PrevVoted := rVotedHighVoltage;

(* ---------------------------------------------------------------------------------------------------- *)
(* CHANNEL 3: Cascade Electrostatic Output Current Shunt Transducers [uA]                               *)
(* ---------------------------------------------------------------------------------------------------- *)
bCurr_Healthy1 := (rHV_Curr_Raw1 >= 0.0) AND (rHV_Curr_Raw1 <= 550.0);
bCurr_Healthy2 := (rHV_Curr_Raw2 >= 0.0) AND (rHV_Curr_Raw2 <= 550.0);
bCurr_Healthy3 := (rHV_Curr_Raw3 >= 0.0) AND (rHV_Curr_Raw3 <= 550.0);
rCurr_Diff12 := ABS(rHV_Curr_Raw1 - rHV_Curr_Raw2);
rCurr_Diff23 := ABS(rHV_Curr_Raw2 - rHV_Curr_Raw3);
rCurr_Diff31 := ABS(rHV_Curr_Raw3 - rHV_Curr_Raw1);

IF (rCurr_Diff12 > rCurr_DiscThreshold) AND (rCurr_Diff31 > rCurr_DiscThreshold) THEN
    rCurr_DiscTimer1 := rCurr_DiscTimer1 + rCycleTime;
    IF rCurr_DiscTimer1 >= rDiscPersistTimeLimit THEN
        bCurr_Healthy1 := FALSE;
    END_IF;
ELSE
    rCurr_DiscTimer1 := MAX(0.0, rCurr_DiscTimer1 - (rCycleTime * 0.5));
END_IF;

IF (rCurr_Diff12 > rCurr_DiscThreshold) AND (rCurr_Diff23 > rCurr_DiscThreshold) THEN
    rCurr_DiscTimer2 := rCurr_DiscTimer2 + rCycleTime;
    IF rCurr_DiscTimer2 >= rDiscPersistTimeLimit THEN
        bCurr_Healthy2 := FALSE;
    END_IF;
ELSE
    rCurr_DiscTimer2 := MAX(0.0, rCurr_DiscTimer2 - (rCycleTime * 0.5));
END_IF;

IF (rCurr_Diff23 > rCurr_DiscThreshold) AND (rCurr_Diff31 > rCurr_DiscThreshold) THEN
    rCurr_DiscTimer3 := rCurr_DiscTimer3 + rCycleTime;
    IF rCurr_DiscTimer3 >= rDiscPersistTimeLimit THEN
        bCurr_Healthy3 := FALSE;
    END_IF;
ELSE
    rCurr_DiscTimer3 := MAX(0.0, rCurr_DiscTimer3 - (rCycleTime * 0.5));
END_IF;

IF bCurr_Healthy1 AND bCurr_Healthy2 AND bCurr_Healthy3 THEN
    nCurr_DegradeMode := 0;
    IF ((rHV_Curr_Raw1 >= rHV_Curr_Raw2) AND (rHV_Curr_Raw1 <= rHV_Curr_Raw3)) OR ((rHV_Curr_Raw1 <= rHV_Curr_Raw2) AND (rHV_Curr_Raw1 >= rHV_Curr_Raw3)) THEN
        rCurr_Selected := rHV_Curr_Raw1;
    ELSIF ((rHV_Curr_Raw2 >= rHV_Curr_Raw1) AND (rHV_Curr_Raw2 <= rHV_Curr_Raw3)) OR ((rHV_Curr_Raw2 <= rHV_Curr_Raw1) AND (rHV_Curr_Raw2 >= rHV_Curr_Raw3)) THEN
        rCurr_Selected := rHV_Curr_Raw2;
    ELSE
        rCurr_Selected := rHV_Curr_Raw3;
    END_IF;
ELSIF bCurr_Healthy1 AND bCurr_Healthy2 THEN
    nCurr_DegradeMode := 1;
    rCurr_Selected := (rHV_Curr_Raw1 + rHV_Curr_Raw2) * 0.5;
ELSIF bCurr_Healthy2 AND bCurr_Healthy3 THEN
    nCurr_DegradeMode := 1;
    rCurr_Selected := (rHV_Curr_Raw2 + rHV_Curr_Raw3) * 0.5;
ELSIF bCurr_Healthy1 AND bCurr_Healthy3 THEN
    nCurr_DegradeMode := 1;
    rCurr_Selected := (rHV_Curr_Raw1 + rHV_Curr_Raw3) * 0.5;
ELSIF bCurr_Healthy1 THEN
    nCurr_DegradeMode := 2;
    rCurr_Selected := rHV_Curr_Raw1;
ELSIF bCurr_Healthy2 THEN
    nCurr_DegradeMode := 2;
    rCurr_Selected := rHV_Curr_Raw2;
ELSIF bCurr_Healthy3 THEN
    nCurr_DegradeMode := 2;
    rCurr_Selected := rHV_Curr_Raw3;
ELSE
    nCurr_DegradeMode := 3;
    rCurr_Selected := rCurr_PrevVoted;
END_IF;
rVotedCascadeCurrent := rCurr_PrevVoted + (0.35 * (rCurr_Selected - rCurr_PrevVoted));
rCurr_PrevVoted := rVotedCascadeCurrent;

(* ---------------------------------------------------------------------------------------------------- *)
(* CHANNEL 4: Paint Fluid Metering Coriolis Flow Rate Transducers [cc/min]                              *)
(* ---------------------------------------------------------------------------------------------------- *)
bFlow_Healthy1 := (rPaint_Flow_Raw1 >= 0.0) AND (rPaint_Flow_Raw1 <= 950.0);
bFlow_Healthy2 := (rPaint_Flow_Raw2 >= 0.0) AND (rPaint_Flow_Raw2 <= 950.0);
bFlow_Healthy3 := (rPaint_Flow_Raw3 >= 0.0) AND (rPaint_Flow_Raw3 <= 950.0);
rFlow_Diff12 := ABS(rPaint_Flow_Raw1 - rPaint_Flow_Raw2);
rFlow_Diff23 := ABS(rPaint_Flow_Raw2 - rPaint_Flow_Raw3);
rFlow_Diff31 := ABS(rPaint_Flow_Raw3 - rPaint_Flow_Raw1);

IF (rFlow_Diff12 > rFlow_DiscThreshold) AND (rFlow_Diff31 > rFlow_DiscThreshold) THEN
    rFlow_DiscTimer1 := rFlow_DiscTimer1 + rCycleTime;
    IF rFlow_DiscTimer1 >= rDiscPersistTimeLimit THEN
        bFlow_Healthy1 := FALSE;
    END_IF;
ELSE
    rFlow_DiscTimer1 := MAX(0.0, rFlow_DiscTimer1 - (rCycleTime * 0.5));
END_IF;

IF (rFlow_Diff12 > rFlow_DiscThreshold) AND (rFlow_Diff23 > rFlow_DiscThreshold) THEN
    rFlow_DiscTimer2 := rFlow_DiscTimer2 + rCycleTime;
    IF rFlow_DiscTimer2 >= rDiscPersistTimeLimit THEN
        bFlow_Healthy2 := FALSE;
    END_IF;
ELSE
    rFlow_DiscTimer2 := MAX(0.0, rFlow_DiscTimer2 - (rCycleTime * 0.5));
END_IF;

IF (rFlow_Diff23 > rFlow_DiscThreshold) AND (rFlow_Diff31 > rFlow_DiscThreshold) THEN
    rFlow_DiscTimer3 := rFlow_DiscTimer3 + rCycleTime;
    IF rFlow_DiscTimer3 >= rDiscPersistTimeLimit THEN
        bFlow_Healthy3 := FALSE;
    END_IF;
ELSE
    rFlow_DiscTimer3 := MAX(0.0, rFlow_DiscTimer3 - (rCycleTime * 0.5));
END_IF;

IF bFlow_Healthy1 AND bFlow_Healthy2 AND bFlow_Healthy3 THEN
    nFlow_DegradeMode := 0;
    IF ((rPaint_Flow_Raw1 >= rPaint_Flow_Raw2) AND (rPaint_Flow_Raw1 <= rPaint_Flow_Raw3)) OR ((rPaint_Flow_Raw1 <= rPaint_Flow_Raw2) AND (rPaint_Flow_Raw1 >= rPaint_Flow_Raw3)) THEN
        rFlow_Selected := rPaint_Flow_Raw1;
    ELSIF ((rPaint_Flow_Raw2 >= rPaint_Flow_Raw1) AND (rPaint_Flow_Raw2 <= rPaint_Flow_Raw3)) OR ((rPaint_Flow_Raw2 <= rPaint_Flow_Raw1) AND (rPaint_Flow_Raw2 >= rPaint_Flow_Raw3)) THEN
        rFlow_Selected := rPaint_Flow_Raw2;
    ELSE
        rFlow_Selected := rPaint_Flow_Raw3;
    END_IF;
ELSIF bFlow_Healthy1 AND bFlow_Healthy2 THEN
    nFlow_DegradeMode := 1;
    rFlow_Selected := (rPaint_Flow_Raw1 + rPaint_Flow_Raw2) * 0.5;
ELSIF bFlow_Healthy2 AND bFlow_Healthy3 THEN
    nFlow_DegradeMode := 1;
    rFlow_Selected := (rPaint_Flow_Raw2 + rPaint_Flow_Raw3) * 0.5;
ELSIF bFlow_Healthy1 AND bFlow_Healthy3 THEN
    nFlow_DegradeMode := 1;
    rFlow_Selected := (rPaint_Flow_Raw1 + rPaint_Flow_Raw3) * 0.5;
ELSIF bFlow_Healthy1 THEN
    nFlow_DegradeMode := 2;
    rFlow_Selected := rPaint_Flow_Raw1;
ELSIF bFlow_Healthy2 THEN
    nFlow_DegradeMode := 2;
    rFlow_Selected := rPaint_Flow_Raw2;
ELSIF bFlow_Healthy3 THEN
    nFlow_DegradeMode := 2;
    rFlow_Selected := rPaint_Flow_Raw3;
ELSE
    nFlow_DegradeMode := 3;
    rFlow_Selected := rFlow_PrevVoted;
END_IF;
rVotedPaintFlowRate := rFlow_PrevVoted + (0.30 * (rFlow_Selected - rFlow_PrevVoted));
rFlow_PrevVoted := rVotedPaintFlowRate;

(* ==================================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL OBSERVERS & NON-NEWTONIAN RHEOLOGY                          *)
(* ==================================================================================================== *)
(* 1. Rotational Mechanics & Centrifugal Liquid Spreading on Bell Cup *)
rOmegaRadPerSec := (rVotedTurbineSpeed * 2.0 * 3.14159265) / 60.0;
rCupTipVelocity := rOmegaRadPerSec * rBellCupRadius;

(* Centrifugal paint film thickness h_film = [ (3 * mu * Q) / (2 * pi * rho * omega^2 * R^2) ]^(1/3) *)
rPaintFilmThickness := 0.000035; (* Baseline default 35 um *)
IF rOmegaRadPerSec > 100.0 THEN
    rPaintFilmThickness := (3.0 * (rPaintViscosityNominal * 0.001) * (rVotedPaintFlowRate * 1.6667E-8)) /
                           (2.0 * 3.14159265 * rPaintDensity * (rOmegaRadPerSec * rOmegaRadPerSec) * (rBellCupRadius * rBellCupRadius));
    IF rPaintFilmThickness > 1.0E-14 THEN
        rPaintFilmThickness := EXP(LN(rPaintFilmThickness) / 3.0);
    ELSE
        rPaintFilmThickness := 0.000010;
    END_IF;
END_IF;
rEstimatedFilmThickness := rPaintFilmThickness * 1.0E6; (* Convert to [um] *)

(* High-shear rate at serrated cup rim gamma_dot = (omega * R) / h_film *)
rShearRateCupRim := (rOmegaRadPerSec * rBellCupRadius) / MAX(0.000005, rPaintFilmThickness);

(* Non-Newtonian Ostwald-de Waele shear thinning apparent viscosity *)
rApparentViscosity := (rPaintViscosityNominal * 0.001) * (1.0 + (0.00012 * rShearRateCupRim));
IF rShearRateCupRim > 1000.0 THEN
    rApparentViscosity := (rPaintViscosityNominal * 0.001) * EXP(-0.28 * LN(rShearRateCupRim / 1000.0));
    rApparentViscosity := MAX(0.0085, rApparentViscosity); (* Lower plateau infinite-shear viscosity *)
END_IF;

(* Dynamic torque loads acting on air-bearing impulse turbine *)
rCentrifugalTorque := (rPaintDensity * (rVotedPaintFlowRate * 1.6667E-8) * rOmegaRadPerSec * (rBellCupRadius * rBellCupRadius));
rAerodynamicTorque := rAeroDragTurbineCoeff * (rOmegaRadPerSec * rOmegaRadPerSec);
rBearingDragTorque := rTurbineViscousFriction * rOmegaRadPerSec;
rNetTurbineTorque := (0.0028 * rTurbineDriveAirValve * rDriveAirSupplyPressure) -
                    (0.0035 * rTurbineBrakeAirValve * rBrakeAirSupplyPressure) -
                    rCentrifugalTorque - rAerodynamicTorque - rBearingDragTorque;
rDynamicBearingLoad := (rCentrifugalTorque * 12.0) + (rAerodynamicTorque * 8.5) + (ABS(rRobotTrajectoryAcceleration) * 4.2);
rDynamicBearingClearance := 14.5 * SQRT(MAX(0.1, rAirBearingPressure / 6.0)) - (rDynamicBearingLoad * 0.035);
rDynamicBearingClearance := LIMIT(4.0, rDynamicBearingClearance, 22.0);

(* 2. Droplet Sauter Mean Diameter d32 First-Principles Semi-Empirical Model *)
IF (rOmegaRadPerSec > 200.0) AND (rVotedPaintFlowRate > 5.0) THEN
    rWeberNumber := (rPaintDensity * (rCupTipVelocity * rCupTipVelocity) * (2.0 * rBellCupRadius)) / MAX(0.005, rPaintSurfaceTension);
    rOhnesorgeNumber := rApparentViscosity / SQRT(MAX(0.001, rPaintDensity * rPaintSurfaceTension * 2.0 * rBellCupRadius));
    rFlowNumber := (rVotedPaintFlowRate * 1.6667E-8) / (rOmegaRadPerSec * (8.0 * rBellCupRadius * rBellCupRadius * rBellCupRadius));
    rRawDropletSMD := (2.0 * rBellCupRadius) * 2.1 *
                      EXP(-0.26 * LN(MAX(100.0, rWeberNumber))) *
                      EXP(0.14 * LN(MAX(0.0001, rOhnesorgeNumber))) *
                      EXP(0.21 * LN(MAX(1.0E-10, rFlowNumber))) * 1.0E6; (* [um] *)
ELSE
    rRawDropletSMD := 45.0; (* Default resting / low-speed particle size *)
END_IF;
rEstimatedDropletSMD := rEstimatedDropletSMD + (0.15 * (rRawDropletSMD - rEstimatedDropletSMD));
rEstimatedDropletSMD := LIMIT(8.0, rEstimatedDropletSMD, 85.0);

(* 3. Electrostatic Space Charge, Corona Field & Transfer Efficiency *)
rElectricFieldE0 := (rVotedHighVoltage) / MAX(0.05, rRobotStandoffDistance * 0.001); (* [kV/m] *)
rSpaceChargeDensity := (rVotedCascadeCurrent * 1.0E-6) / MAX(0.0005, (rVotedPaintFlowRate * 1.6667E-8) * 1500.0);
rSpaceChargeCloudDensity := (rSpaceChargeDensity * (rRobotStandoffDistance * 0.001) * (rRobotStandoffDistance * 0.001)) /
                            (2.0 * rDielectricPermittivity * 1000.0); (* [kV/m3] *)
rDropletSpecificCharge := (3.0 * rDielectricPermittivity * (rElectricFieldE0 * 1000.0)) /
                          (rPaintDensity * MAX(0.000005, (rEstimatedDropletSMD * 0.5E-6)));
rCoulombicDriftVelocity := (rDropletSpecificCharge * (rElectricFieldE0 * 1000.0) * (rEstimatedDropletSMD * 0.5E-6)) / (0.000185);
rTransferEffCalc := 48.0 + (46.0 * (1.0 - EXP(-0.042 * rVotedHighVoltage /
                                           (MAX(0.18, rBoothAirVelocity) * (rRobotStandoffDistance / 250.0))))) -
                    (0.045 * (rVotedTurbineSpeed / 1000.0)) - (0.015 * (rVotedPaintFlowRate / 100.0));
rEstimatedTransferEff := LIMIT(35.0, rTransferEffCalc, 98.0);

(* 4. Dual Shaping Air Aerodynamics, Fan Width & Edge Sharpness *)
rInnerAirJetVelocity := (rTargetInnerShapingAir * (rInnerShapingAirValve * 0.01)) / (0.00045 * 3600.0); (* [m/s] *)
rOuterAirJetVelocity := (rTargetOuterShapingAir * (rOuterShapingAirValve * 0.01)) / (0.00062 * 3600.0); (* [m/s] *)
rInnerAirMomentumFlux := rAirDensityRef * (rTargetInnerShapingAir * (rInnerShapingAirValve * 0.01) / 3600.0) * rInnerAirJetVelocity;
rOuterAirMomentumFlux := rAirDensityRef * (rTargetOuterShapingAir * (rOuterShapingAirValve * 0.01) / 3600.0) * rOuterAirJetVelocity;
rPaintRadialMomentum := rPaintDensity * (rVotedPaintFlowRate * 1.6667E-8) * rCupTipVelocity;
rShroudMomentumRatio := (rInnerAirMomentumFlux + (0.38 * rOuterAirMomentumFlux)) / MAX(0.0001, rPaintRadialMomentum);
rRawPatternWidth := 160.0 + (380.0 * EXP(-0.48 * SQRT(MAX(0.01, rShroudMomentumRatio)))) *
                    EXP(0.35 * LN(rRobotStandoffDistance / 250.0));
rEstimatedPatternWidth := LIMIT(120.0, rRawPatternWidth, 620.0);

(* Edge Spray Sharpness: rate of droplet deposition density decline at boundary [N/m2] *)
rEdgeSharpnessCalc := (rOuterAirMomentumFlux * 180.0) / MAX(20.0, rEstimatedPatternWidth * 0.5);
rEstimatedEdgeSharpness := LIMIT(20.0, rEdgeSharpnessCalc, 180.0);

(* Shroud Vortex Containment Stability Ratio *)
rVortexContainmentIndex := rOuterAirJetVelocity / MAX(1.0, (rInnerAirJetVelocity * 0.65) + (rBoothAirVelocity * 25.0));
rContainmentStabilityRatio := LIMIT(0.2, rVortexContainmentIndex, 3.5);

(* In-flight solvent evaporation loss fraction *)
rSolventEvaporationLoss := (1.0 - rPaintSolidsFraction) * 0.085 * (1.0 + (0.025 * (rBoothTemperature - 20.0))) *
                           (1.0 - (0.008 * (rBoothRelativeHumidity - 50.0))) * (rRobotStandoffDistance / 250.0);
rSolventEvaporationLoss := LIMIT(0.01, rSolventEvaporationLoss, 0.25) * 100.0; (* [%] *)

(* ==================================================================================================== *)
(* PHASE 3: DISCRETE STATE-SPACE PROPAGATION & LUENBERGER OBSERVER INNOVATION                           *)
(* ==================================================================================================== *)
(* Map cyber-physical process measurements into deviation vector y_meas[1..6] *)
vecY_Meas[1] := rVotedTurbineSpeed - rTargetRotationalSpeed;
vecY_Meas[2] := rEstimatedDropletSMD - rTargetDropletSMD;
vecY_Meas[3] := rEstimatedTransferEff - 88.0; (* Nominal 88.0% electrostatic transfer target *)
vecY_Meas[4] := rEstimatedPatternWidth - rTargetPatternWidth;
vecY_Meas[5] := rVotedPaintFlowRate - rTargetPaintFlowRate;
vecY_Meas[6] := (rBoothAirVelocity - 0.35) * 100.0; (* Scaled downdraft velocity deviation *)

(* Compute predicted output measurement vector vecY_Est = matC * vecX_Hat + matD * vecU_Opt *)
FOR nRow := 1 TO 6 DO
    vecY_Est[nRow] := 0.0;
    FOR nCol := 1 TO 6 DO
        vecY_Est[nRow] := vecY_Est[nRow] + (matC[nRow, nCol] * vecX_Hat[nCol]) + (matD[nRow, nCol] * vecU_Opt[nCol]);
    END_FOR;
    vecObsErr[nRow] := vecY_Meas[nRow] - vecY_Est[nRow];
END_FOR;

(* Propagate dynamic discrete Luenberger state observer: x_hat[k+1] = A*x_hat[k] + B*u[k] + L*e[k] *)
FOR nRow := 1 TO 6 DO
    vecX_Pred[nRow] := 0.0;
    FOR nCol := 1 TO 6 DO
        vecX_Pred[nRow] := vecX_Pred[nRow] + (matA[nRow, nCol] * vecX_Hat[nCol]) +
                           (matB[nRow, nCol] * vecU_Opt[nCol]) +
                           (matL[nRow, nCol] * vecObsErr[nCol]);
    END_FOR;
END_FOR;
FOR nRow := 1 TO 6 DO
    vecX_Hat[nRow] := vecX_Pred[nRow];
END_FOR;

(* ==================================================================================================== *)
(* PHASE 4: RECEDING-HORIZON MPC VIA 10 UNROLLED PROJECTED GRADIENT DESCENT (PGD) ITERATIONS            *)
(* ==================================================================================================== *)
(* Quadratic Cost Formulation:                                                                          *)
(* J = 1/2*(x_pred - x_ref)^T * (Q + P) * (x_pred - x_ref) + 1/2*u^T * R * u + 1/2*du^T * S * du       *)
(* Analytical Gradient: grad = B^T * (Q + P) * (A * x_hat + B * u - x_ref) + R * u + S * (u - u_prev)  *)
FOR nIterIndex := 1 TO 10 DO
    (* 1. Predict future state response x_pred = A * x_hat + B * u_opt *)
    FOR nRow := 1 TO 6 DO
        vecX_Pred[nRow] := 0.0;
        FOR nCol := 1 TO 6 DO
            vecX_Pred[nRow] := vecX_Pred[nRow] + (matA[nRow, nCol] * vecX_Hat[nCol]) + (matB[nRow, nCol] * vecU_Opt[nCol]);
        END_FOR;
        vecX_ErrTemp[nRow] := vecX_Pred[nRow] - vecX_Ref[nRow];
    END_FOR;
    
    (* 2. Compute state tracking error penalty weighting: vecWeightTemp = (Q + P) * vecX_ErrTemp *)
    FOR nRow := 1 TO 6 DO
        vecWeightTemp[nRow] := 0.0;
        FOR nCol := 1 TO 6 DO
            vecWeightTemp[nRow] := vecWeightTemp[nRow] + ((matQ[nRow, nCol] + matP[nRow, nCol]) * vecX_ErrTemp[nCol]);
        END_FOR;
    END_FOR;
    
    (* 3. Compute analytical gradient vector: grad = B^T * vecWeightTemp + R * u + S * (u - u_prev) *)
    FOR nRow := 1 TO 6 DO
        rGradTermState := 0.0;
        rGradTermEffort := 0.0;
        rGradTermSlew := 0.0;
        FOR nCol := 1 TO 6 DO
            rGradTermState := rGradTermState + (matB[nCol, nRow] * vecWeightTemp[nCol]);
            rGradTermEffort := rGradTermEffort + (matR[nRow, nCol] * vecU_Opt[nCol]);
            rGradTermSlew := rGradTermSlew + (matS[nRow, nCol] * (vecU_Opt[nCol] - vecU_Prev[nCol]));
        END_FOR;
        vecGrad[nRow] := rGradTermState + rGradTermEffort + rGradTermSlew;
    END_FOR;
    
    (* 4. Projected Gradient Descent update with slew-rate and box saturation limits *)
    FOR nRow := 1 TO 6 DO
        (* Step against cost gradient *)
        vecU_Opt[nRow] := vecU_Opt[nRow] - (rPgdStepSize * vecGrad[nRow]);
        
        (* Enforce dynamic slew-rate limit projection *)
        rDeltaVal := vecU_Opt[nRow] - vecU_Prev[nRow];
        IF rDeltaVal > vecDeltaU_Max[nRow] THEN
            vecU_Opt[nRow] := vecU_Prev[nRow] + vecDeltaU_Max[nRow];
        ELSIF rDeltaVal < -vecDeltaU_Max[nRow] THEN
            vecU_Opt[nRow] := vecU_Prev[nRow] - vecDeltaU_Max[nRow];
        END_IF;
        
        (* Enforce hard box saturation limits *)
        IF vecU_Opt[nRow] > vecU_Max[nRow] THEN
            vecU_Opt[nRow] := vecU_Max[nRow];
        ELSIF vecU_Opt[nRow] < vecU_Min[nRow] THEN
            vecU_Opt[nRow] := vecU_Min[nRow];
        END_IF;
    END_FOR;
END_FOR;

(* Update historical actuator tracking *)
FOR nRow := 1 TO 6 DO
    vecDeltaU[nRow] := vecU_Opt[nRow] - vecU_Prev[nRow];
    vecU_Prev[nRow] := vecU_Opt[nRow];
END_FOR;

(* Feedforward Actuator Mapping from MPC Optimizer *)
rTurbineDriveAirValve := vecU_Opt[1];
rHighVoltageCommand := vecU_Opt[2];
rInnerShapingAirValve := vecU_Opt[3];
rOuterShapingAirValve := vecU_Opt[4];
rPaintGearPumpSpeedCmd := vecU_Opt[5];
rPaintFluidPressureReg := vecU_Opt[6];

(* ==================================================================================================== *)
(* PHASE 5: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                                *)
(* ==================================================================================================== *)
rFsmStepTimer := rFsmStepTimer + rCycleTime;

CASE nFsmCurrentState OF
    0: (* STATE_IDLE *)
        sFsmStateName := 'STATE_IDLE';
        bSystemReady := FALSE;
        bSprayTriggerActive := FALSE;
        bElectrostaticCascadeOn := FALSE;
        bFastColorChangeActive := FALSE;
        bInterCoatStandbyActive := FALSE;
        rTurbineDriveAirValve := 0.0;
        rTurbineBrakeAirValve := 0.0;
        rHighVoltageCommand := 0.0;
        rInnerShapingAirValve := 5.0; (* Low idle purge *)
        rOuterShapingAirValve := 5.0; (* Low idle purge *)
        rPaintGearPumpSpeedCmd := 0.0;
        rPaintFluidPressureReg := 0.0;
        rSolventFlushValveCmd := 0.0;
        rAirChopPurgeValveCmd := 0.0;
        rBellWashRingValveCmd := 0.0;
        
        IF bEnable AND NOT bEmergencyShutdown THEN
            nFsmCurrentState := 1;
            rFsmStepTimer := 0.0;
        END_IF;
        
    1: (* STATE_BOOTH_LAMINAR_VENTILATION_LOCK *)
        sFsmStateName := 'STATE_BOOTH_LAMINAR_VENTILATION_LOCK';
        bSystemReady := FALSE;
        bDowndraftVelocityOk := (rBoothAirVelocity >= 0.25) AND (rBoothAirVelocity <= 0.48);
        
        IF bDowndraftVelocityOk AND bBoothLaminarPermissive AND (rFsmStepTimer >= 1.5) THEN
            nFsmCurrentState := 2;
            rFsmStepTimer := 0.0;
        ELSIF rFsmStepTimer > 10.0 THEN
            (* Booth downdraft interlock timeout *)
            nFsmCurrentState := 0;
            rFsmStepTimer := 0.0;
        END_IF;
        
    2: (* STATE_COLOR_FEED_LINE_PRESSURIZATION *)
        sFsmStateName := 'STATE_COLOR_FEED_LINE_PRESSURIZATION';
        rPaintFluidPressureReg := 45.0;
        
        IF (rPaintLineDynamicPressure >= 3.8) AND (rFsmStepTimer >= 1.0) THEN
            nFsmCurrentState := 3;
            rFsmStepTimer := 0.0;
        ELSIF rFsmStepTimer > 8.0 THEN
            nFsmCurrentState := 0;
            rFsmStepTimer := 0.0;
        END_IF;
        
    3: (* STATE_TURBINE_BEARING_AIR_LIFT_LOCK *)
        sFsmStateName := 'STATE_TURBINE_BEARING_AIR_LIFT_LOCK';
        bBearingAirInterlockOk := (rAirBearingPressure >= 5.5);
        
        IF bBearingAirInterlockOk AND (rFsmStepTimer >= 1.2) THEN
            nFsmCurrentState := 4;
            rFsmStepTimer := 0.0;
        ELSIF rFsmStepTimer > 5.0 THEN
            nFsmCurrentState := 0;
            rFsmStepTimer := 0.0;
        END_IF;
        
    4: (* STATE_BELL_TURBINE_SPEED_RAMP_ACCEL *)
        sFsmStateName := 'STATE_BELL_TURBINE_SPEED_RAMP_ACCEL';
        rTurbineDriveAirValve := MIN(65.0, rFsmStepTimer * 18.0);
        rTurbineBrakeAirValve := 0.0;
        
        IF (rVotedTurbineSpeed >= (rTargetRotationalSpeed - 800.0)) AND (rFsmStepTimer >= 2.5) THEN
            nFsmCurrentState := 5;
            rFsmStepTimer := 0.0;
        ELSIF rFsmStepTimer > 12.0 THEN
            nFsmCurrentState := 12; (* Turbine acceleration stall decel *)
            rFsmStepTimer := 0.0;
        END_IF;
        
    5: (* STATE_SHAPING_AIR_AERODYNAMIC_SHROUD_ESTABLISH *)
        sFsmStateName := 'STATE_SHAPING_AIR_AERODYNAMIC_SHROUD_ESTABLISH';
        rInnerShapingAirValve := MIN(55.0, 15.0 + (rFsmStepTimer * 25.0));
        rOuterShapingAirValve := MIN(65.0, 20.0 + (rFsmStepTimer * 30.0));
        
        IF (rContainmentStabilityRatio >= 0.85) AND (rContainmentStabilityRatio <= 1.45) AND (rFsmStepTimer >= 1.2) THEN
            nFsmCurrentState := 6;
            rFsmStepTimer := 0.0;
        ELSIF rFsmStepTimer > 6.0 THEN
            nFsmCurrentState := 12;
            rFsmStepTimer := 0.0;
        END_IF;
        
    6: (* STATE_HIGH_VOLTAGE_RAMP_AND_LEAK_CHECK *)
        sFsmStateName := 'STATE_HIGH_VOLTAGE_RAMP_AND_LEAK_CHECK';
        bElectrostaticCascadeOn := TRUE;
        rHighVoltageCommand := MIN(rTargetHighVoltage, rFsmStepTimer * 28.0);
        
        IF (rVotedHighVoltage >= (rTargetHighVoltage - 2.5)) AND (rVotedCascadeCurrent < 45.0) AND (rFsmStepTimer >= 2.0) THEN
            bSystemReady := TRUE;
            IF bRobotCycleStart THEN
                nFsmCurrentState := 7;
                rFsmStepTimer := 0.0;
            END_IF;
        ELSIF (rVotedCascadeCurrent >= 75.0) OR (rFsmStepTimer > 8.0) THEN
            (* Excessive leakage pre-spray check failed *)
            nFsmCurrentState := 10;
            rFsmStepTimer := 0.0;
        END_IF;
        
    7: (* STATE_TRIGGER_PAINT_SPRAY_PRODUCTION_RUN *)
        sFsmStateName := 'STATE_TRIGGER_PAINT_SPRAY_PRODUCTION_RUN';
        bSystemReady := TRUE;
        bSprayTriggerActive := TRUE;
        bElectrostaticCascadeOn := TRUE;
        
        IF bRobotPathCorneringActive THEN
            nFsmCurrentState := 8;
            rFsmStepTimer := 0.0;
        ELSIF bStandbyHoldCommand THEN
            nFsmCurrentState := 9;
            rFsmStepTimer := 0.0;
        ELSIF bColorChangeTrigger OR bSolventPurgeTrigger THEN
            nFsmCurrentState := 10;
            rFsmStepTimer := 0.0;
        ELSIF NOT bRobotCycleStart THEN
            nFsmCurrentState := 9;
            rFsmStepTimer := 0.0;
        END_IF;
        
    8: (* STATE_DYNAMIC_PATH_CORNERING_OVERFLOW_COMPENSATION *)
        sFsmStateName := 'STATE_DYNAMIC_PATH_CORNERING_OVERFLOW_COMPENSATION';
        bSystemReady := TRUE;
        bSprayTriggerActive := TRUE;
        bElectrostaticCascadeOn := TRUE;
        
        (* Feedforward cornering modulation based on TCP curvature *)
        rCorneringFlowBoostFactor := 1.0 + LIMIT(0.0, ABS(rRobotPathCurvature) * 0.45, 0.35);
        rCorneringPatternTrim := LIMIT(-60.0, -ABS(rRobotPathCurvature) * 80.0, 0.0);
        rCorneringSpeedOffset := LIMIT(0.0, ABS(rRobotPathCurvature) * 6000.0, 4500.0);
        rCorneringAirShroudTrim := LIMIT(0.0, ABS(rRobotPathCurvature) * 22.0, 16.0);
        
        rPaintGearPumpSpeedCmd := vecU_Opt[5] * rCorneringFlowBoostFactor;
        rInnerShapingAirValve := LIMIT(0.0, vecU_Opt[3] + rCorneringAirShroudTrim, 100.0);
        
        IF NOT bRobotPathCorneringActive THEN
            nFsmCurrentState := 7;
            rFsmStepTimer := 0.0;
        END_IF;
        
    9: (* STATE_INTER_COAT_STANDBY_IDLE_HOLD *)
        sFsmStateName := 'STATE_INTER_COAT_STANDBY_IDLE_HOLD';
        bSystemReady := TRUE;
        bSprayTriggerActive := FALSE;
        bInterCoatStandbyActive := TRUE;
        
        rTurbineDriveAirValve := 22.0; (* Holds ~25,000 RPM *)
        rHighVoltageCommand := 20.0; (* Low bias HV to prevent droplet back-attraction *)
        rInnerShapingAirValve := 12.0;
        rOuterShapingAirValve := 15.0;
        rPaintGearPumpSpeedCmd := 0.0;
        
        IF bRobotCycleStart THEN
            nFsmCurrentState := 4; (* Fast re-ramp to production speed *)
            rFsmStepTimer := 0.0;
        ELSIF bColorChangeTrigger OR bSolventPurgeTrigger THEN
            nFsmCurrentState := 10;
            rFsmStepTimer := 0.0;
        ELSIF NOT bEnable THEN
            nFsmCurrentState := 10;
            rFsmStepTimer := 0.0;
        END_IF;
        
    10: (* STATE_HIGH_VOLTAGE_DECAY_AND_DISCHARGE *)
        sFsmStateName := 'STATE_HIGH_VOLTAGE_DECAY_AND_DISCHARGE';
        bSystemReady := FALSE;
        bSprayTriggerActive := FALSE;
        bElectrostaticCascadeOn := FALSE;
        rHighVoltageCommand := 0.0;
        rPaintGearPumpSpeedCmd := 0.0;
        
        IF (rVotedHighVoltage <= 1.2) OR (rFsmStepTimer >= 2.0) THEN
            IF bColorChangeTrigger OR bSolventPurgeTrigger THEN
                nFsmCurrentState := 11;
                nPurgeSubStep := 0;
                rPurgeSubStepTimer := 0.0;
                rFsmStepTimer := 0.0;
            ELSE
                nFsmCurrentState := 12;
                rFsmStepTimer := 0.0;
            END_IF;
        END_IF;
        
    11: (* STATE_RAPID_SOLVENT_PURGE_AND_COLOR_CHANGE *)
        sFsmStateName := 'STATE_RAPID_SOLVENT_PURGE_AND_COLOR_CHANGE';
        bFastColorChangeActive := TRUE;
        bSprayTriggerActive := FALSE;
        bElectrostaticCascadeOn := FALSE;
        rHighVoltageCommand := 0.0;
        rPurgeSubStepTimer := rPurgeSubStepTimer + rCycleTime;
        
        CASE nPurgeSubStep OF
            0: (* Substep 0: Paint Pushback from Wrist Manifold *)
                rTurbineDriveAirValve := 25.0; (* Hold 28,000 RPM *)
                rPaintGearPumpSpeedCmd := -45.0; (* Reverse rotation pushback *)
                rSolventFlushValveCmd := 0.0;
                rAirChopPurgeValveCmd := 0.0;
                rBellWashRingValveCmd := 0.0;
                IF rPurgeSubStepTimer >= 1.2 THEN
                    nPurgeSubStep := 1;
                    rPurgeSubStepTimer := 0.0;
                END_IF;
                
            1: (* Substep 1: High Pressure Solvent Pre-Pulse *)
                rPaintGearPumpSpeedCmd := 0.0;
                rSolventFlushValveCmd := 85.0;
                rAirChopPurgeValveCmd := 0.0;
                rBellWashRingValveCmd := 40.0;
                IF rPurgeSubStepTimer >= 1.5 THEN
                    nPurgeSubStep := 2;
                    rPurgeSubStepTimer := 0.0;
                END_IF;
                
            2: (* Substep 2: Pulsed Air Chop Purge (Alternating Solvent and Air Slugs) *)
                IF (REAL_TO_INT(rPurgeSubStepTimer * 10.0) MOD 2) = 0 THEN
                    rSolventFlushValveCmd := 100.0;
                    rAirChopPurgeValveCmd := 0.0;
                ELSE
                    rSolventFlushValveCmd := 0.0;
                    rAirChopPurgeValveCmd := 100.0;
                END_IF;
                rBellWashRingValveCmd := 80.0;
                IF rPurgeSubStepTimer >= 3.5 THEN
                    nPurgeSubStep := 3;
                    rPurgeSubStepTimer := 0.0;
                END_IF;
                
            3: (* Substep 3: External Bell Cup Wash Ring Flush *)
                rSolventFlushValveCmd := 0.0;
                rAirChopPurgeValveCmd := 60.0;
                rBellWashRingValveCmd := 100.0;
                IF rPurgeSubStepTimer >= 1.5 THEN
                    nPurgeSubStep := 4;
                    rPurgeSubStepTimer := 0.0;
                END_IF;
                
            4: (* Substep 4: High-Speed Centrifugal Spin Off Dry *)
                rTurbineDriveAirValve := 75.0; (* Spin up to 60,000 RPM for drying *)
                rSolventFlushValveCmd := 0.0;
                rAirChopPurgeValveCmd := 0.0;
                rBellWashRingValveCmd := 0.0;
                rInnerShapingAirValve := 80.0;
                rOuterShapingAirValve := 80.0;
                IF rPurgeSubStepTimer >= 2.0 THEN
                    nPurgeSubStep := 5;
                    rPurgeSubStepTimer := 0.0;
                END_IF;
                
            5: (* Substep 5: New Color Prefill to Tip Needle *)
                rTurbineDriveAirValve := 35.0;
                rPaintGearPumpSpeedCmd := 85.0; (* Forward push new paint *)
                rInnerShapingAirValve := 25.0;
                rOuterShapingAirValve := 25.0;
                IF (rVotedPaintFlowRate >= 120.0) OR (rPurgeSubStepTimer >= 2.0) THEN
                    nPurgeSubStep := 6;
                    rPurgeSubStepTimer := 0.0;
                END_IF;
                
            6: (* Substep 6: Purge Sequence Complete *)
                rPaintGearPumpSpeedCmd := 0.0;
                bFastColorChangeActive := FALSE;
                IF bEnable THEN
                    nFsmCurrentState := 4; (* Transition to speed ramp for next car body *)
                    rFsmStepTimer := 0.0;
                ELSE
                    nFsmCurrentState := 12;
                    rFsmStepTimer := 0.0;
                END_IF;
        END_CASE;
        
    12: (* STATE_TURBINE_DYNAMIC_BRAKING_DECEL *)
        sFsmStateName := 'STATE_TURBINE_DYNAMIC_BRAKING_DECEL';
        bSystemReady := FALSE;
        bSprayTriggerActive := FALSE;
        bElectrostaticCascadeOn := FALSE;
        rTurbineDriveAirValve := 0.0;
        rTurbineBrakeAirValve := LIMIT(0.0, (rVotedTurbineSpeed / 50000.0) * 85.0, 95.0);
        rHighVoltageCommand := 0.0;
        rPaintGearPumpSpeedCmd := 0.0;
        
        IF (rVotedTurbineSpeed <= 800.0) OR (rFsmStepTimer >= 5.0) THEN
            rTurbineBrakeAirValve := 0.0;
            nFsmCurrentState := 0;
            rFsmStepTimer := 0.0;
        END_IF;
        
    13: (* STATE_EMERGENCY_HV_SPARK_DETECTED_FAST_SHUTDOWN *)
        sFsmStateName := 'STATE_EMERGENCY_HV_SPARK_DETECTED_FAST_SHUTDOWN';
        bSystemReady := FALSE;
        bSprayTriggerActive := FALSE;
        bElectrostaticCascadeOn := FALSE;
        bEmergencyShutdown := TRUE;
        
        (* Fast crowbar quench: Zero setpoint, engage max dynamic braking *)
        rHighVoltageCommand := 0.0;
        rPaintGearPumpSpeedCmd := 0.0;
        rTurbineDriveAirValve := 0.0;
        rTurbineBrakeAirValve := 100.0;
        rInnerShapingAirValve := 100.0; (* Maximum containment shroud blast *)
        rOuterShapingAirValve := 100.0;
        rSolventFlushValveCmd := 0.0;
        rAirChopPurgeValveCmd := 0.0;
        rBellWashRingValveCmd := 0.0;
        
        IF bReset THEN
            bEmergencyShutdown := FALSE;
            bSparkQuenchTriggered := FALSE;
            rTurbineBrakeAirValve := 0.0;
            nFsmCurrentState := 0;
            rFsmStepTimer := 0.0;
        END_IF;
END_CASE;
nFsmCurrentState := nFsmCurrentState;

(* ==================================================================================================== *)
(* PHASE 6: ISA-18.2 MULTI-TIER ALARMS, SPARK PRECURSOR & 32-BIT BIT-PACKED STATUS WORDS                *)
(* ==================================================================================================== *)
rCurrRateOfChange := (rVotedCascadeCurrent - rPrevCurrentSample) / MAX(0.0005, rCycleTime);
rVoltRateOfChange := (rVotedHighVoltage - rPrevVoltageSample) / MAX(0.0005, rCycleTime);
rPrevCurrentSample := rVotedCascadeCurrent;
rPrevVoltageSample := rVotedHighVoltage;

IF ((rCurrRateOfChange > 120000.0) AND (rVotedCascadeCurrent > 180.0)) OR
   ((rVotedCascadeCurrent >= rTrip_Curr_HH) AND (rVotedHighVoltage >= 35.0)) THEN
    bSparkQuenchTriggered := TRUE;
    nFsmCurrentState := 13;
END_IF;

(* 1. Bell Turbine Rotational Speed ISA-18.2 Alarms *)
IF rVotedTurbineSpeed >= rTrip_Speed_HH THEN
    bAlarm_Speed_HH := TRUE;
ELSIF rVotedTurbineSpeed <= (rTrip_Speed_HH - rDeadband_Speed) THEN
    bAlarm_Speed_HH := FALSE;
END_IF;

IF rVotedTurbineSpeed >= rTrip_Speed_H THEN
    bAlarm_Speed_H := TRUE;
ELSIF rVotedTurbineSpeed <= (rTrip_Speed_H - rDeadband_Speed) THEN
    bAlarm_Speed_H := FALSE;
END_IF;

IF (nFsmCurrentState >= 4) AND (nFsmCurrentState <= 8) THEN
    IF rVotedTurbineSpeed <= rTrip_Speed_LL THEN
        bAlarm_Speed_LL := TRUE;
    ELSIF rVotedTurbineSpeed >= (rTrip_Speed_LL + rDeadband_Speed) THEN
        bAlarm_Speed_LL := FALSE;
    END_IF;
    
    IF rVotedTurbineSpeed <= rTrip_Speed_L THEN
        bAlarm_Speed_L := TRUE;
    ELSIF rVotedTurbineSpeed >= (rTrip_Speed_L + rDeadband_Speed) THEN
        bAlarm_Speed_L := FALSE;
    END_IF;
ELSE
    bAlarm_Speed_L := FALSE;
    bAlarm_Speed_LL := FALSE;
END_IF;

(* 2. High Voltage Cascade ISA-18.2 Alarms *)
IF rVotedHighVoltage >= rTrip_HV_HH THEN
    bAlarm_HV_HH := TRUE;
ELSIF rVotedHighVoltage <= (rTrip_HV_HH - rDeadband_HV) THEN
    bAlarm_HV_HH := FALSE;
END_IF;

IF rVotedHighVoltage >= rTrip_HV_H THEN
    bAlarm_HV_H := TRUE;
ELSIF rVotedHighVoltage <= (rTrip_HV_H - rDeadband_HV) THEN
    bAlarm_HV_H := FALSE;
END_IF;

IF (nFsmCurrentState = 6) OR (nFsmCurrentState = 7) OR (nFsmCurrentState = 8) THEN
    IF rVotedHighVoltage <= rTrip_HV_LL THEN
        bAlarm_HV_LL := TRUE;
    ELSIF rVotedHighVoltage >= (rTrip_HV_LL + rDeadband_HV) THEN
        bAlarm_HV_LL := FALSE;
    END_IF;
    
    IF rVotedHighVoltage <= rTrip_HV_L THEN
        bAlarm_HV_L := TRUE;
    ELSIF rVotedHighVoltage >= (rTrip_HV_L + rDeadband_HV) THEN
        bAlarm_HV_L := FALSE;
    END_IF;
ELSE
    bAlarm_HV_L := FALSE;
    bAlarm_HV_LL := FALSE;
END_IF;

(* 3. Cascade Current ISA-18.2 Alarms *)
IF rVotedCascadeCurrent >= rTrip_Curr_HH THEN
    bAlarm_Curr_HH := TRUE;
ELSIF rVotedCascadeCurrent <= (rTrip_Curr_HH - rDeadband_Curr) THEN
    bAlarm_Curr_HH := FALSE;
END_IF;

IF rVotedCascadeCurrent >= rTrip_Curr_H THEN
    bAlarm_Curr_H := TRUE;
ELSIF rVotedCascadeCurrent <= (rTrip_Curr_H - rDeadband_Curr) THEN
    bAlarm_Curr_H := FALSE;
END_IF;

(* 4. Paint Metering Flow Rate ISA-18.2 Alarms *)
IF rVotedPaintFlowRate >= rTrip_Flow_HH THEN
    bAlarm_Flow_HH := TRUE;
ELSIF rVotedPaintFlowRate <= (rTrip_Flow_HH - rDeadband_Flow) THEN
    bAlarm_Flow_HH := FALSE;
END_IF;

IF rVotedPaintFlowRate >= rTrip_Flow_H THEN
    bAlarm_Flow_H := TRUE;
ELSIF rVotedPaintFlowRate <= (rTrip_Flow_H - rDeadband_Flow) THEN
    bAlarm_Flow_H := FALSE;
END_IF;

IF (nFsmCurrentState = 7) OR (nFsmCurrentState = 8) THEN
    IF rVotedPaintFlowRate <= rTrip_Flow_LL THEN
        bAlarm_Flow_LL := TRUE;
    ELSIF rVotedPaintFlowRate >= (rTrip_Flow_LL + rDeadband_Flow) THEN
        bAlarm_Flow_LL := FALSE;
    END_IF;
    
    IF rVotedPaintFlowRate <= rTrip_Flow_L THEN
        bAlarm_Flow_L := TRUE;
    ELSIF rVotedPaintFlowRate >= (rTrip_Flow_L + rDeadband_Flow) THEN
        bAlarm_Flow_L := FALSE;
    END_IF;
ELSE
    bAlarm_Flow_L := FALSE;
    bAlarm_Flow_LL := FALSE;
END_IF;

(* 5. Turbine Aerodynamic Bearing Lift Pressure Alarms *)
IF rAirBearingPressure >= rTrip_Bearing_HH THEN
    bAlarm_Bearing_HH := TRUE;
ELSIF rAirBearingPressure <= (rTrip_Bearing_HH - rDeadband_Bearing) THEN
    bAlarm_Bearing_HH := FALSE;
END_IF;

IF rAirBearingPressure <= rTrip_Bearing_LL THEN
    bAlarm_Bearing_LL := TRUE;
ELSIF rAirBearingPressure >= (rTrip_Bearing_LL + rDeadband_Bearing) THEN
    bAlarm_Bearing_LL := FALSE;
END_IF;

(* 6. Dual Shaping Air Header Supply Pressure Alarms *)
IF rShapingAirSupplyPressure >= rTrip_Shaping_HH THEN
    bAlarm_Shaping_HH := TRUE;
ELSIF rShapingAirSupplyPressure <= (rTrip_Shaping_HH - rDeadband_Shaping) THEN
    bAlarm_Shaping_HH := FALSE;
END_IF;

IF rShapingAirSupplyPressure <= rTrip_Shaping_LL THEN
    bAlarm_Shaping_LL := TRUE;
ELSIF rShapingAirSupplyPressure >= (rTrip_Shaping_LL + rDeadband_Shaping) THEN
    bAlarm_Shaping_LL := FALSE;
END_IF;

(* 7. Spray Booth Downdraft Velocity Alarms *)
IF rBoothAirVelocity >= rTrip_Booth_HH THEN
    bAlarm_Booth_HH := TRUE;
ELSIF rBoothAirVelocity <= (rTrip_Booth_HH - rDeadband_Booth) THEN
    bAlarm_Booth_HH := FALSE;
END_IF;

IF rBoothAirVelocity <= rTrip_Booth_LL THEN
    bAlarm_Booth_LL := TRUE;
ELSIF rBoothAirVelocity >= (rTrip_Booth_LL + rDeadband_Booth) THEN
    bAlarm_Booth_LL := FALSE;
END_IF;

(* Critical Safety Interlock Trip *)
IF bAlarm_Speed_HH OR bAlarm_Bearing_LL OR bAlarm_Shaping_LL OR (nTach_DegradeMode = 3) OR (nHV_DegradeMode = 3) THEN
    nFsmCurrentState := 13;
END_IF;

(* --- BIT-PACKING 32-BIT DWORD STATUS & ALARM REGISTERS --- *)
(* dwStatusWord1: Operational State & Master Modes *)
dwStatusWord1 := 16#00000000;
IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bSystemReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bRobotCycleStart THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bSprayTriggerActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bElectrostaticCascadeOn THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bRobotPathCorneringActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bInterCoatStandbyActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bFastColorChangeActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bEmergencyShutdown THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bSparkQuenchTriggered THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF bBearingAirInterlockOk THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bDowndraftVelocityOk THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(nFsmCurrentState AND 16#0F), 16);
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(nPurgeSubStep AND 16#0F), 20);

(* dwStatusWord2: Subsystem Health & Degraded Voting Enums *)
dwStatusWord2 := 16#00000000;
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nTach_DegradeMode AND 16#03), 0);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nHV_DegradeMode AND 16#03), 2);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nCurr_DegradeMode AND 16#03), 4);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nFlow_DegradeMode AND 16#03), 6);
IF bTach_Healthy1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bTach_Healthy2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bTach_Healthy3 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bHV_Healthy1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bHV_Healthy2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bHV_Healthy3 THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bCurr_Healthy1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF bCurr_Healthy2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;
IF bCurr_Healthy3 THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;
IF bFlow_Healthy1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bFlow_Healthy2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF bFlow_Healthy3 THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;

(* dwAlarmWord1: Category A Safety Critical Catastrophic Trips *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_Speed_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_Speed_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_HV_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_HV_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_Curr_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_Flow_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_Flow_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarm_Bearing_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bAlarm_Bearing_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF bAlarm_Shaping_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF bAlarm_Shaping_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF bAlarm_Booth_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF bAlarm_Booth_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF bSparkQuenchTriggered THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;
IF bEmergencyShutdown THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF;

(* dwAlarmWord2: Category B High & Low Process Warnings *)
dwAlarmWord2 := 16#00000000;
IF bAlarm_Speed_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlarm_Speed_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlarm_HV_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlarm_HV_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bAlarm_Curr_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bAlarm_Curr_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bAlarm_Flow_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bAlarm_Flow_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF bAlarm_Bearing_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF bAlarm_Bearing_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF bAlarm_Shaping_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF bAlarm_Shaping_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF bAlarm_Booth_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF bAlarm_Booth_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;

(* dwAlarmWord3: Category C 2oo3 TMR Sensor Discrepancies *)
dwAlarmWord3 := 16#00000000;
IF NOT bTach_Healthy1 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000001; END_IF;
IF NOT bTach_Healthy2 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000002; END_IF;
IF NOT bTach_Healthy3 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000004; END_IF;
IF NOT bHV_Healthy1 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000008; END_IF;
IF NOT bHV_Healthy2 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000010; END_IF;
IF NOT bHV_Healthy3 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000020; END_IF;
IF NOT bCurr_Healthy1 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000040; END_IF;
IF NOT bCurr_Healthy2 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000080; END_IF;
IF NOT bCurr_Healthy3 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000100; END_IF;
IF NOT bFlow_Healthy1 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000200; END_IF;
IF NOT bFlow_Healthy2 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000400; END_IF;
IF NOT bFlow_Healthy3 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00000800; END_IF;
IF nTach_DegradeMode > 0 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00010000; END_IF;
IF nHV_DegradeMode > 0 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00020000; END_IF;
IF nCurr_DegradeMode > 0 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00040000; END_IF;
IF nFlow_DegradeMode > 0 THEN dwAlarmWord3 := dwAlarmWord3 OR 16#00080000; END_IF;

(* dwAlarmWord4: Category D Color Change, Purge & Maintenance Alerts *)
dwAlarmWord4 := 16#00000000;
IF (rSolventSupplyPressure < 6.5) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000001; END_IF;
IF (rChopAirSupplyPressure < 5.0) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000002; END_IF;
IF (rBrakeAirSupplyPressure < 5.2) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000004; END_IF;
IF (rDriveAirSupplyPressure < 5.8) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000008; END_IF;
IF (rEstimatedDropletSMD > 42.0) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000010; END_IF;
IF (rEstimatedTransferEff < 65.0) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000020; END_IF;
IF (rContainmentStabilityRatio < 0.65) OR (rContainmentStabilityRatio > 1.85) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000040; END_IF;
IF (rBoothRelativeHumidity < 45.0) OR (rBoothRelativeHumidity > 80.0) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000080; END_IF;
IF (rBoothTemperature < 18.0) OR (rBoothTemperature > 26.0) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000100; END_IF;
IF (rDynamicBearingClearance < 6.0) THEN dwAlarmWord4 := dwAlarmWord4 OR 16#00000200; END_IF;

END_FUNCTION_BLOCK