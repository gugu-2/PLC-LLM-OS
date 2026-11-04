FUNCTION_BLOCK FB_Plastics_TwinScrew_ReactiveExtrusion_SlitDie
(*
 ====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - ADVANCED POLYMER PROCESSING & REACTIVE EXTRUSION
 ====================================================================================================
  SYSTEM IDENTIFIER:   CO-ROTATING INTERMESHING TWIN-SCREW REACTIVE COMPOUNDING EXTRUDER WITH
                       INTEGRATED IN-LINE SLIT-DIE RHEOMETER & DECOUPLED MELT GEAR PUMP
  MACHINE GEOMETRY:    L/D RATIO = 56:1, SCREW DIAMETER D = 92.0 mm, NOMINAL THROUGHPUT = 2,500 kg/h
  PROCESS KINETICS:    FREE-RADICAL FUNCTIONAL MONOMER GRAFTING (PP-g-MAH) VIA CONTROLLED PEROXIDE
                       MASTERBATCH LIQUID MICRO-INJECTION (DBPH / LUPEROX 101 INITIATOR)
  THERMAL REGULATION:  10-ZONE MODULAR BARREL WITH DUAL-STAGE HIGH-FREQUENCY INDUCTION HEATING
                       AND SUPERCRITICAL CO2 (scCO2) DIRECT HIGH-PRESSURE INJECTION COOLING
  PRESSURE REGULATION: POSITIVE DISPLACEMENT MELT GEAR PUMP (176 cc/rev) PRESSURE DECOUPLING LOOP
                       (STABILIZING DIE HEAD PRESSURE AT 250.0 bar +/- 0.5 bar WITH ACTIVE ANTI-SURGE)
  RHEOLOGY OBSERVER:   IN-LINE SLIT-DIE HIGH-ACCURACY VISCOMETER (WEISSENBERG-RABINOWITSCH CORRECTED)
                       PROVIDING REAL-TIME SHEAR VISCOSITY AND MELT FLOW INDEX (MFI) FEEDBACK
  SAFETY INTEGRITY:    2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ON CRITICAL MELT PRESSURE & RHEOMETRY;
                       ISA-18.2 FIVE-TIER ALARM ARCHITECTURE WITH COLD-START INTERLOCK PREVENTING
                       SCREW ROTATION BELOW POLYMER MELTING POINT (Tm) AND DIE FREEZE TRIPS.
 ====================================================================================================
  STANDARDIZED INDUSTRIAL P&ID TRANSDUCER & ACTUATOR TAG MAPPING:
   - WT_GRAVIMETRIC_FEEDER_MAIN_101A/B/C : Main Polyolefin Base Resin Gravimetric Loss-in-Weight Feeder
   - WT_GRAVIMETRIC_FEEDER_SIDE_102A/B/C : Side Stuffer Functional Monomer (MAH) Gravimetric Feeder
   - FT_PEROXIDE_LIQUID_201A/B/C         : Coriolis Mass Flow Meter for Liquid Organic Peroxide Initiator
   - PT_BARREL_ZONE5_MELT_301A/B/C       : Barrel Zone 5 Melting / Plasticizing Transition Melt Pressure
   - PT_DIE_INLET_PRESSURE_401A/B/C      : Gear Pump Suction / Die Adapter Entrance Melt Pressure (2oo3)
   - TT_MELT_TRUE_PYRO_501A/B/C          : Fiber-Optic Non-Contact Infrared Pyrometer True Melt Temp (2oo3)
   - VISC_SLIT_DIE_RHEOMETER_601A/B/C    : Slit-Die Rheometer Multi-Tap Differential Pressure Array (2oo3)
   - ST_SCREW_MOTOR_SPEED_701A/B/C       : Twin-Screw Synchronous Drive High-Resolution Motor Encoder (2oo3)
   - ST_GEAR_PUMP_SPEED_801              : Melt Gear Pump AC Servo Drive Resolver / Feedback
 ====================================================================================================
*)
VAR_INPUT
    (* System Execution & Safety Supervision Permissives *)
    bEnable                             : BOOL;         (* Master Execution Enable Command *)
    bReset                              : BOOL;         (* Master Fault Reset Command *)
    bEmergencyStop                      : BOOL;         (* Hardwired E-Stop Circuit Status (Active LOW) *)
    iOperationMode                      : INT;          (* 0:Standby, 1:Manual, 2:Auto-Compounding, 3:Purge, 4:Calibration *)
    bPreheatStartCmd                    : BOOL;         (* Operator Command: Initiate Barrel Preheat & Soak Sequence *)
    bSoakOverridePermissive             : BOOL;         (* Key-Switch Bypass Permissive for Thermal Soak Timer *)
    bFeederTareCmd                      : BOOL;         (* Gravimetric Feeder Auto-Tare Re-Zero Calibration Command *)
    bEmergencyVentPush                  : BOOL;         (* Manual Emergency Vent Diverter Valve Open Command *)

    (* Recipe & Production Setpoints *)
    rThroughputSetPoint_kgh             : REAL;         (* Total Compounding Throughput Setpoint [kg/h] (Nominal: 2500.0) *)
    rBaseResinRatio_pct                 : REAL;         (* Main Base Resin Weight Fraction [%] (Nominal: 97.5 - 99.0) *)
    rSideMonomerRatio_pct               : REAL;         (* Side Stuffer Monomer Weight Fraction [%] (Nominal: 0.8 - 2.5) *)
    rPeroxideConcentration_ppm          : REAL;         (* Initiator Dosing Target Ratio [ppm] (Nominal: 500 - 3500) *)
    rTargetMFI_g10min                   : REAL;         (* Desired Product Melt Flow Index (230 deg C / 2.16 kg) [g/10min] *)
    rTargetDiePressure_bar              : REAL;         (* Slit-Die Discharge Target Pressure [bar] (Nominal: 250.0 bar) *)
    rTargetGearPumpInletPressure_bar    : REAL;         (* Gear Pump Suction Head Pressure Setpoint [bar] (Nominal: 35.0 bar) *)
    rScrewSpeedNominal_rpm              : REAL;         (* Twin-Screw Drive Master Speed Setpoint [rpm] (Nominal: 600.0) *)
    rPolymerMeltingPoint_Tm_degC        : REAL;         (* Base Polymer Crystalline Melting Point [deg C] (Nominal: 165.0) *)

    (* 10-Zone Barrel Temperature Recipe Setpoints [deg C] *)
    aBarrelTempSetpoints_degC           : ARRAY[1..10] OF REAL; (* Barrel Zones 1 to 10 Target Profile [deg C] *)
    rSlitDieTempSetpoint_degC           : REAL;         (* Slit-Die Body Temperature Setpoint [deg C] (Nominal: 220.0) *)

    (* Slit-Die Rheometer Tooling Geometry *)
    rSlitDieLength_mm                   : REAL;         (* Rheometer Channel Calibrated Length L [mm] (Nominal: 120.0) *)
    rSlitDieWidth_mm                    : REAL;         (* Rheometer Channel Calibrated Width W [mm] (Nominal: 50.0) *)
    rSlitDieGap_mm                      : REAL;         (* Rheometer Channel Calibrated Height/Gap H [mm] (Nominal: 1.20) *)

    (* 2oo3 TMR Transducer Bank 1: Main Gravimetric Feeder Loss-in-Weight [kg/h] *)
    WT_GRAVIMETRIC_FEEDER_MAIN_101A     : REAL;         (* Channel A Load Cell Signal [kg/h] *)
    WT_GRAVIMETRIC_FEEDER_MAIN_101B     : REAL;         (* Channel B Load Cell Signal [kg/h] *)
    WT_GRAVIMETRIC_FEEDER_MAIN_101C     : REAL;         (* Channel C Load Cell Signal [kg/h] *)

    (* 2oo3 TMR Transducer Bank 2: Side Stuffer Gravimetric Feeder Loss-in-Weight [kg/h] *)
    WT_GRAVIMETRIC_FEEDER_SIDE_102A     : REAL;         (* Channel A Side Feeder Load Cell [kg/h] *)
    WT_GRAVIMETRIC_FEEDER_SIDE_102B     : REAL;         (* Channel B Side Feeder Load Cell [kg/h] *)
    WT_GRAVIMETRIC_FEEDER_SIDE_102C     : REAL;         (* Channel C Side Feeder Load Cell [kg/h] *)

    (* 2oo3 TMR Transducer Bank 3: Liquid Peroxide Coriolis Mass Flow Meter [kg/h] *)
    FT_PEROXIDE_LIQUID_201A             : REAL;         (* Channel A Coriolis Mass Flow [kg/h] *)
    FT_PEROXIDE_LIQUID_201B             : REAL;         (* Channel B Coriolis Mass Flow [kg/h] *)
    FT_PEROXIDE_LIQUID_201C             : REAL;         (* Channel C Coriolis Mass Flow [kg/h] *)

    (* 2oo3 TMR Transducer Bank 4: Barrel Zone 5 Plasticizing Melt Pressure [bar] *)
    PT_BARREL_ZONE5_MELT_301A           : REAL;         (* Channel A Melt Pressure Zone 5 [bar] *)
    PT_BARREL_ZONE5_MELT_301B           : REAL;         (* Channel B Melt Pressure Zone 5 [bar] *)
    PT_BARREL_ZONE5_MELT_301C           : REAL;         (* Channel C Melt Pressure Zone 5 [bar] *)

    (* 2oo3 TMR Transducer Bank 5: Die Entrance / Gear Pump Inlet Melt Pressure [bar] (3.0 bar Trip Tol) *)
    PT_DIE_INLET_PRESSURE_401A          : REAL;         (* Channel A Melt Pressure Gear Pump Suction [bar] *)
    PT_DIE_INLET_PRESSURE_401B          : REAL;         (* Channel B Melt Pressure Gear Pump Suction [bar] *)
    PT_DIE_INLET_PRESSURE_401C          : REAL;         (* Channel C Melt Pressure Gear Pump Suction [bar] *)

    (* 2oo3 TMR Transducer Bank 6: True Melt Immersion Pyrometer Temperature [deg C] *)
    TT_MELT_TRUE_PYRO_501A              : REAL;         (* Channel A Optical Pyrometer Melt Temp [deg C] *)
    TT_MELT_TRUE_PYRO_501B              : REAL;         (* Channel B Optical Pyrometer Melt Temp [deg C] *)
    TT_MELT_TRUE_PYRO_501C              : REAL;         (* Channel C Optical Pyrometer Melt Temp [deg C] *)

    (* 2oo3 TMR Transducer Bank 7: Slit-Die Rheometer Multi-Tap Differential Pressure [bar] (1.2 bar Trip Tol) *)
    VISC_SLIT_DIE_RHEOMETER_601A        : REAL;         (* Channel A Slit Differential Pressure dP [bar] *)
    VISC_SLIT_DIE_RHEOMETER_601B        : REAL;         (* Channel B Slit Differential Pressure dP [bar] *)
    VISC_SLIT_DIE_RHEOMETER_601C        : REAL;         (* Channel C Slit Differential Pressure dP [bar] *)

    (* 2oo3 TMR Transducer Bank 8: Twin-Screw Synchronous Drive Encoder Speed [rpm] *)
    ST_SCREW_MOTOR_SPEED_701A           : REAL;         (* Channel A Optical Encoder Speed [rpm] *)
    ST_SCREW_MOTOR_SPEED_701B           : REAL;         (* Channel B Optical Encoder Speed [rpm] *)
    ST_SCREW_MOTOR_SPEED_701C           : REAL;         (* Channel C Optical Encoder Speed [rpm] *)

    (* Ancillary Process Sensors & Feedbacks *)
    aBarrelZoneTemp_degC                : ARRAY[1..10] OF REAL; (* Real-time Barrel Metal Thermocouple Temperatures [deg C] *)
    rGearPumpActualSpeed_rpm            : REAL;         (* Melt Gear Pump Drive Tachometer / Speed Feedback [rpm] *)
    rScrewMotorTorque_pct               : REAL;         (* Twin-Screw Drive Shaft Torque Feedback [% of 12,000 Nm rated] *)
    rGearPumpMotorTorque_pct            : REAL;         (* Gear Pump Drive Motor Torque Feedback [% of 1,800 Nm rated] *)
    rVacuumPressure_Zone4_mbar          : REAL;         (* Primary Degassing Zone Absolute Pressure [mbar] *)
    rVacuumPressure_Zone8_mbar          : REAL;         (* Secondary Reactive Devolatilization Absolute Pressure [mbar] *)
    rCoolingWaterTempIn_degC            : REAL;         (* Chilled Water Supply Temperature to Feed Throat [deg C] *)
    rCoolingWaterPressure_bar           : REAL;         (* Chilled Water Header Pressure [bar] *)
    rCO2SupplyPressure_bar              : REAL;         (* Supercritical CO2 Cooling High-Pressure Reservoir [bar] *)
    rCO2SupplyTemp_degC                 : REAL;         (* Supercritical CO2 Chilled Fluid Temperature [deg C] *)
END_VAR
VAR_OUTPUT
    (* Primary Actuator Speed & Rate Commands *)
    rScrewSpeedCmd_rpm                  : REAL;         (* Twin-Screw Drive Speed Reference Setpoint [rpm] *)
    rGearPumpSpeedCmd_rpm               : REAL;         (* Melt Gear Pump AC Servo Speed Reference Setpoint [rpm] *)
    rFeederMainCmd_kgh                  : REAL;         (* Main Base Resin Gravimetric Feeder Delivery Setpoint [kg/h] *)
    rFeederSideCmd_kgh                  : REAL;         (* Side Stuffer Functional Monomer Delivery Setpoint [kg/h] *)
    rPeroxidePumpCmd_pct                : REAL;         (* Liquid Peroxide Diaphragm Micro-Dosing Pump Stroke [%] *)

    (* 10-Zone Barrel Thermal Regulation Outputs [% Duty Cycle] *)
    aBarrelHeaterDuty_pct               : ARRAY[1..10] OF REAL; (* Induction Heating Solid-State Relay Duty [0.0..100.0 %] *)
    aBarrelCoolDuty_pct                 : ARRAY[1..10] OF REAL; (* Supercritical CO2 Modulating Direct Injection [0.0..100.0 %] *)
    rSlitDieHeaterDuty_pct              : REAL;         (* Slit-Die Body Cartridge Heater Modulated Duty [%] *)

    (* Vacuum & Safety Vent Actuator Solenoids *)
    bVacuumValveZone4_Cmd               : BOOL;         (* Zone 4 Degassing Vacuum Isolation Valve Command *)
    bVacuumValveZone8_Cmd               : BOOL;         (* Zone 8 Reactive Stripping Vacuum Isolation Valve Command *)
    bEmergencyVentDiverter_Cmd          : BOOL;         (* Rapid Emergency Melt Vent Diverter Valve Open Command *)

    (* Voted Telemetry & Rheological State Observers *)
    rDiePressure_Voted_bar              : REAL;         (* Slit-Die Entrance / Discharge Voted Melt Pressure [bar] *)
    rGearPumpSuction_Voted_bar          : REAL;         (* Melt Gear Pump Inlet Voted Melt Pressure [bar] *)
    rTrueMeltTemp_Voted_degC            : REAL;         (* Voted True Melt Temperature from Optical Pyrometer [deg C] *)
    rSlitDieShearRate_invs              : REAL;         (* In-Line Slit-Die Wall True Shear Rate (Rabinowitsch) [1/s] *)
    rSlitDieShearStress_kPa             : REAL;         (* In-Line Slit-Die Wall Shear Stress [kPa] *)
    rObservedViscosity_Pas              : REAL;         (* Slit-Die Observed True Dynamic Viscosity [Pa.s] *)
    rEstimatedMFI_g10min                : REAL;         (* Online Real-Time Melt Flow Index (MFI) Observer [g/10min] *)
    rGraftingConversion_pct             : REAL;         (* Polymer Free-Radical Grafting Conversion Yield [%] *)
    rCalculatedSME_kWh_ton              : REAL;         (* Specific Mechanical Energy Input [kWh/ton] *)
    rDegreeOfFill_pct                   : REAL;         (* Twin-Screw Channel Degree of Fill Fraction [%] *)
    rResinResidenceTime_s               : REAL;         (* Mean Polymer Melt Channel Transit / Residence Time [s] *)

    (* Digital Status Words & Safety Diagnostics *)
    wFSM_CurrentState                   : WORD;         (* 12-Stage Finite State Machine Current State Register *)
    dwSystemStatusWord                  : DWORD;        (* Global Cyber-Physical System Status Bitmask *)
    dwActuatorStatusWord                : DWORD;        (* Actuator Interlock & Operational Status Bitmask *)
    dwAlarmWord_Trip                    : DWORD;        (* Category 1 Critical Trip Alarm Bitmask *)
    dwAlarmWord_Warning                 : DWORD;        (* Category 2 Warning Alarm Bitmask *)
    dwSensorHealthMask                  : DWORD;        (* 2oo3 Sensor Bank Redundancy Health Bitmask *)
    bColdStartInterlockActive           : BOOL;         (* Mechanical Protection: Screw Rotation Forbidden (T < Tm) *)
    bDieFreezeInterlockActive           : BOOL;         (* Die Tooling Thermal Protection Interlock Active *)
    bEmergencyVentOpen                  : BOOL;         (* Emergency Melt Rupture Vent Diverter Active *)
    bSteadyStateActive                  : BOOL;         (* Process in Stable Reactive Compounding Regime *)
END_VAR
VAR
    (* ------------------------------------------------------------------------- *)
    (* SYSTEM CONSTANTS & PHYSICAL MODEL PARAMETERS                             *)
    (* ------------------------------------------------------------------------- *)
    c_Ts_s                              : REAL := 0.002;        (* Discrete Task Execution Time Ts = 2 ms *)
    c_rGasConstant_R                    : REAL := 8.31446;      (* Universal Gas Constant R [J/(mol*K)] *)
    c_rArrhenius_Ea                     : REAL := 142500.0;     (* Peroxide Decomposition Activation Energy [J/mol] *)
    c_rArrhenius_A0                     : REAL := 1.98E15;      (* Arrhenius Pre-Exponential Frequency Factor [1/s] *)
    c_rRadicalEfficiency_f              : REAL := 0.65;         (* Radical Cage Escape Initiation Efficiency *)
    c_rPeroxideMolarMass                : REAL := 290.44;       (* DBPH Peroxide Molecular Weight [g/mol] *)
    c_rPolymerDensity_Solid             : REAL := 905.0;        (* Solid Polypropylene Feed Density [kg/m3] *)
    c_rPolymerDensity_Melt0             : REAL := 760.0;        (* Reference Melt Density at 200 C, 1 bar [kg/m3] *)
    c_rThermalExpansionBeta             : REAL := 0.00068;      (* Volumetric Thermal Expansion Coefficient [1/K] *)
    c_rCompressibilityBetaP             : REAL := 0.00018;      (* Melt Compressibility Coefficient [1/bar] *)
    c_rScrewDiameter_m                  : REAL := 0.092;        (* Twin-Screw Outer Flight Diameter D = 92 mm [m] *)
    c_rScrewLength_m                    : REAL := 5.152;        (* Total Barrel Length L = 56 * D = 5.152 m *)
    c_rChannelDepth_m                   : REAL := 0.0125;       (* Screw Flight Channel Radial Depth h [m] *)
    c_rFlightClearance_m                : REAL := 0.0005;       (* Radial Flight-to-Barrel Clearance delta [m] *)
    c_rScrewFlightStarts                : REAL := 2.0;          (* Number of Intermeshing Screw Flight Starts (Double-Flighted) *)
    c_rScrewFlightPitch_m               : REAL := 0.060;        (* Axial Pitch of Conveying Elements [m] *)
    c_rScrewChannelNetVolume_m3         : REAL := 0.0242;       (* Total Intermeshing Free Screw Channel Void Volume [m3] *)
    c_rGearPumpDisplacement_m3          : REAL := 0.000176;     (* Positive Displacement Melt Gear Pump Volume [m3/rev] (176 cc/rev) *)
    c_rGearPumpSlipFactor               : REAL := 0.00000045;   (* Backflow Slip Leakage Constant [m3/(s*bar*Pa.s)] *)

    (* Cross-WLF Viscosity Model Constants (Unmodified Base Polypropylene) *)
    c_rCross_D1                         : REAL := 2.50E11;      (* WLF Glassy Viscosity Parameter D1 [Pa.s] *)
    c_rCross_A1                         : REAL := 28.50;        (* WLF Universal Shift Parameter A1 *)
    c_rCross_A2                         : REAL := 51.60;        (* WLF Temperature Parameter A2 [K] *)
    c_rCross_Tstar                      : REAL := 263.15;       (* WLF Glass Transition Reference Temp T* [K] *)
    c_rCross_Lambda0                    : REAL := 0.185;        (* Cross Relaxation Time Constant at Tref [s] *)
    c_rCross_PowerIndex_n               : REAL := 0.320;        (* Cross Pseudoplastic Shear-Thinning Power Law Index *)

    (* ------------------------------------------------------------------------- *)
    (* 2oo3 TMR REDUNDANCY VOTING & SENSOR HEALTH VARIABLES                     *)
    (* ------------------------------------------------------------------------- *)
    (* Bank 1: Main Feeder *)
    bMainFeeder_A_Ok, bMainFeeder_B_Ok, bMainFeeder_C_Ok : BOOL;
    iMainFeeder_HealthyCount            : INT;
    rMainFeeder_Voted_kgh               : REAL;
    rMainFeeder_Diff_AB, rMainFeeder_Diff_BC, rMainFeeder_Diff_CA : REAL;
    tMainFeeder_DiscrepancyTimer        : TON;
    bMainFeeder_DiscrepancyFault        : BOOL;

    (* Bank 2: Side Feeder *)
    bSideFeeder_A_Ok, bSideFeeder_B_Ok, bSideFeeder_C_Ok : BOOL;
    iSideFeeder_HealthyCount            : INT;
    rSideFeeder_Voted_kgh               : REAL;
    rSideFeeder_Diff_AB, rSideFeeder_Diff_BC, rSideFeeder_Diff_CA : REAL;
    tSideFeeder_DiscrepancyTimer        : TON;
    bSideFeeder_DiscrepancyFault        : BOOL;

    (* Bank 3: Peroxide Coriolis Flow *)
    bPeroxide_A_Ok, bPeroxide_B_Ok, bPeroxide_C_Ok : BOOL;
    iPeroxide_HealthyCount              : INT;
    rPeroxide_Voted_kgh                 : REAL;
    rPeroxide_Diff_AB, rPeroxide_Diff_BC, rPeroxide_Diff_CA : REAL;
    tPeroxide_DiscrepancyTimer          : TON;
    bPeroxide_DiscrepancyFault          : BOOL;

    (* Bank 4: Barrel Zone 5 Melt Pressure *)
    bZone5Press_A_Ok, bZone5Press_B_Ok, bZone5Press_C_Ok : BOOL;
    iZone5Press_HealthyCount            : INT;
    rZone5Press_Voted_bar               : REAL;
    rZone5Press_Diff_AB, rZone5Press_Diff_BC, rZone5Press_Diff_CA : REAL;
    tZone5Press_DiscrepancyTimer        : TON;
    bZone5Press_DiscrepancyFault        : BOOL;

    (* Bank 5: Die Entrance / Gear Pump Inlet Melt Pressure *)
    bDieInlet_A_Ok, bDieInlet_B_Ok, bDieInlet_C_Ok : BOOL;
    iDieInlet_HealthyCount              : INT;
    rDieInlet_Voted_bar                 : REAL;
    rDieInlet_Diff_AB, rDieInlet_Diff_BC, rDieInlet_Diff_CA : REAL;
    tDieInlet_DiscrepancyTimer          : TON;
    bDieInlet_DiscrepancyFault          : BOOL;

    (* Bank 6: True Melt Optical Pyrometer *)
    bPyro_A_Ok, bPyro_B_Ok, bPyro_C_Ok  : BOOL;
    iPyro_HealthyCount                  : INT;
    rPyro_Voted_degC                    : REAL;
    rPyro_Diff_AB, rPyro_Diff_BC, rPyro_Diff_CA : REAL;
    tPyro_DiscrepancyTimer              : TON;
    bPyro_DiscrepancyFault              : BOOL;

    (* Bank 7: Slit-Die Rheometer Differential Pressure *)
    bSlitDP_A_Ok, bSlitDP_B_Ok, bSlitDP_C_Ok : BOOL;
    iSlitDP_HealthyCount                : INT;
    rSlitDP_Voted_bar                   : REAL;
    rSlitDP_Diff_AB, rSlitDP_Diff_BC, rSlitDP_Diff_CA : REAL;
    tSlitDP_DiscrepancyTimer            : TON;
    bSlitDP_DiscrepancyFault            : BOOL;

    (* Bank 8: Twin-Screw Motor Speed *)
    bScrewSpeed_A_Ok, bScrewSpeed_B_Ok, bScrewSpeed_C_Ok : BOOL;
    iScrewSpeed_HealthyCount            : INT;
    rScrewSpeed_Voted_rpm               : REAL;
    rScrewSpeed_Diff_AB, rScrewSpeed_Diff_BC, rScrewSpeed_Diff_CA : REAL;
    tScrewSpeed_DiscrepancyTimer        : TON;
    bScrewSpeed_DiscrepancyFault        : BOOL;

    (* ------------------------------------------------------------------------- *)
    (* IN-LINE SLIT-DIE RHEOMETRY & CROSS-WLF CALCULATIONS                      *)
    (* ------------------------------------------------------------------------- *)
    rMeltDensity_Actual                 : REAL;
    rSlitChannelVolume_m3               : REAL;
    rSlitCrossSectionArea_m2            : REAL;
    rVolumetricThroughput_m3s           : REAL;
    rSlitApparentShearRate_invs         : REAL;
    rSlitWallShearStress_Pa             : REAL;
    rNonNewtonianIndex_neff             : REAL;
    rRabinowitschFactor_b               : REAL;
    rSlitTrueWallShearRate_invs         : REAL;
    rDynamicViscosity_Pas               : REAL;
    rWLF_ShiftFactor_aT                 : REAL;
    rZeroShearViscosity_Eta0            : REAL;
    rCrossModelViscosity_Pas            : REAL;
    rViscosityModelResidual_Pas         : REAL;
    rStandardMFI_ShearViscosity_Pas     : REAL;
    rCalculatedMFI_Online               : REAL;
    rMFI_TrackingError_pct              : REAL;

    (* ------------------------------------------------------------------------- *)
    (* REACTION KINETICS & VISCOUS DISSIPATION VARIABLES                       *)
    (* ------------------------------------------------------------------------- *)
    rAbsoluteMeltTemp_K                 : REAL;
    rPeroxideDecayConstant_kd           : REAL;
    rPeroxideHalfLife_s                 : REAL;
    rReactiveZoneTransitTime_s          : REAL;
    rPeroxideResidualFraction           : REAL;
    rPeroxideConversionYield            : REAL;
    rPrimaryRadicalFlux_mol_m3s         : REAL;
    rGraftingReactionRate_mol_m3s       : REAL;
    rCalculatedGraftingConversion       : REAL;
    rBetaScissionChainDegradationFactor : REAL;
    rScrewClearanceShearRate_invs       : REAL;
    rScrewChannelShearRate_invs         : REAL;
    rViscousHeatFlux_Clearance_kW       : REAL;
    rViscousHeatFlux_Channel_kW         : REAL;
    rTotalViscousDissipation_kW         : REAL;
    rTheoreticalMechanicalPower_kW      : REAL;
    rSpecificMechanicalEnergy_kWh_t     : REAL;
    rChannelFillDegree_Fraction         : REAL;

    (* ------------------------------------------------------------------------- *)
    (* 8x8 DISCRETE STATE-SPACE MATRICES & KALMAN OBSERVER                      *)
    (* ------------------------------------------------------------------------- *)
    bStateSpaceInitialized              : BOOL := FALSE;
    aMatrixA                            : ARRAY[1..8, 1..8] OF REAL;
    aMatrixB                            : ARRAY[1..8, 1..8] OF REAL;
    aMatrixC                            : ARRAY[1..8, 1..8] OF REAL;
    aMatrixD                            : ARRAY[1..8, 1..8] OF REAL;
    aMatrixL                            : ARRAY[1..8, 1..8] OF REAL; (* Observer Gain Matrix *)
    aStateVector_x                      : ARRAY[1..8] OF REAL;       (* Current State Estimate *)
    aStateVector_x_pred                 : ARRAY[1..8] OF REAL;       (* Prior Prediction *)
    aInputVector_u                      : ARRAY[1..8] OF REAL;       (* Control Action Vector *)
    aOutputVector_y                     : ARRAY[1..8] OF REAL;       (* Estimated Output Vector *)
    aMeasurementVector_z                : ARRAY[1..8] OF REAL;       (* Measured Physical Values *)
    aStateSetpoint_r                    : ARRAY[1..8] OF REAL;       (* Desired State Setpoint *)
    aStateError_e                       : ARRAY[1..8] OF REAL;       (* Setpoint Deviation *)
    aObserverInnovation_y_err           : ARRAY[1..8] OF REAL;       (* Measurement Residual *)

    (* ------------------------------------------------------------------------- *)
    (* MODEL PREDICTIVE CONTROL (MPC) RECEDING HORIZON ARRAYS                   *)
    (* ------------------------------------------------------------------------- *)
    aWeightQ                            : ARRAY[1..8] OF REAL;       (* State Deviation Penalty Diagonal *)
    aWeightR                            : ARRAY[1..8] OF REAL;       (* Actuator Magnitude Penalty *)
    aWeightS                            : ARRAY[1..8] OF REAL;       (* Actuator Rate-of-Change Slew Penalty *)
    aWeightP                            : ARRAY[1..8] OF REAL;       (* Terminal Horizon Penalty *)
    aInputMin                           : ARRAY[1..8] OF REAL;       (* Hard Lower Actuator Constraints *)
    aInputMax                           : ARRAY[1..8] OF REAL;       (* Hard Upper Actuator Constraints *)
    aDeltaInputMax                      : ARRAY[1..8] OF REAL;       (* Maximum Slew-Rate per Cycle *)
    aOptimalDeltaU                      : ARRAY[1..8] OF REAL;       (* Optimal Incremental Step *)
    aPrevInputVector_u                  : ARRAY[1..8] OF REAL;       (* Previous Control Action u[k-1] *)
    rMPC_ObjectiveCost_J                : REAL;
    iMPCIterationCounter                : INT;

    (* ------------------------------------------------------------------------- *)
    (* 10-ZONE BARREL TEMPERATURE REGULATION ARRAYS                              *)
    (* ------------------------------------------------------------------------- *)
    aBarrelZoneError_degC               : ARRAY[1..10] OF REAL;
    aBarrelZoneIntegral_degC_s          : ARRAY[1..10] OF REAL;
    aBarrelZonePrevError_degC           : ARRAY[1..10] OF REAL;
    aBarrelZoneDeriv_degC_s             : ARRAY[1..10] OF REAL;
    aBarrelZonePID_Output               : ARRAY[1..10] OF REAL;
    aBarrelZoneFeedforward_kW           : ARRAY[1..10] OF REAL;
    tThermalSoakTimer                   : TON;
    bAllZonesAtMeltingPoint             : BOOL;
    bThermalSoakComplete                : BOOL;
    rSlitDieTempError_degC              : REAL;
    rSlitDieIntegral_degC_s             : REAL;
    rSlitDiePrevError_degC              : REAL;

    (* ------------------------------------------------------------------------- *)
    (* MELT GEAR PUMP DECOUPLING & ANTI-SURGE CONTROLLER                        *)
    (* ------------------------------------------------------------------------- *)
    rGearPumpPressureError_bar          : REAL;
    rGearPumpSuctionError_bar           : REAL;
    rGearPumpIntegral_bar_s             : REAL;
    rGearPumpSuctionIntegral_bar_s      : REAL;
    rVolumetricEfficiency_eta           : REAL;
    rGearPumpFeedforwardSpeed_rpm       : REAL;
    rAntiSurgeDampingTrim_rpm           : REAL;
    rPrevDiePressure_bar                : REAL;
    rDiePressureROC_bars                : REAL;
    rSuctionPressureROC_bars            : REAL;

    (* ------------------------------------------------------------------------- *)
    (* MULTI-STAGE FINITE STATE MACHINE (FSM) TIMERS & REGISTERS                *)
    (* ------------------------------------------------------------------------- *)
    iFSM_State                          : INT := 0;  (* 0:Standby, 1:Preheat, 2:Homogenize, 3:Tare, 4:ScrewStart, 5:FloodFeed, 6:ReactiveInject, 7:SteadyState, 8:SurgeDamp, 9:Purge, 10:Drain, 11:EmergencyVent *)
    iFSM_PrevState                      : INT := 0;
    tStateTimer                         : TON;
    tSubStepTimer                       : TON;
    iSubStepIndex                       : INT := 0;
    bStateEntryFlag                     : BOOL := TRUE;
    bFeederTareCompleted                : BOOL := FALSE;
    bPurgeModeRequested                 : BOOL := FALSE;
    bControlledShutdownRequested        : BOOL := FALSE;

    (* ------------------------------------------------------------------------- *)
    (* ISA-18.2 ALARM ENGINE & FIRST-OUT REGISTERS                              *)
    (* ------------------------------------------------------------------------- *)
    (* Category 1: Critical Emergency Trips (Latchable) *)
    bAlarm_DiePressure_HH               : BOOL; (* P_die > 305 bar *)
    bAlarm_DiePressure_LL               : BOOL; (* P_die < 50 bar during production *)
    bAlarm_GearPumpSuction_HH           : BOOL; (* P_suction > 75 bar *)
    bAlarm_GearPumpSuction_LL           : BOOL; (* P_suction < 5 bar cavitation *)
    bAlarm_TrueMeltTemp_HH              : BOOL; (* T_melt > 265 deg C thermal degradation *)
    bAlarm_TrueMeltTemp_LL              : BOOL; (* T_melt < 160 deg C freeze interlock *)
    bAlarm_ScrewMotorTorque_HH          : BOOL; (* Torque > 95% rated *)
    bAlarm_SlitRheometer_HH             : BOOL; (* Viscosity or dP trip *)
    bAlarm_PeroxideRunaway_HH           : BOOL; (* Uncontrolled peroxide surge *)
    bAlarm_ColdStartInterlockTrip       : BOOL; (* Attempted rotation below Tm *)

    (* Category 2: Process Warnings *)
    bWarning_DiePressure_H              : BOOL; (* P_die > 280 bar *)
    bWarning_DiePressure_L              : BOOL; (* P_die < 150 bar *)
    bWarning_GearPumpSuction_H          : BOOL; (* P_suction > 55 bar *)
    bWarning_GearPumpSuction_L          : BOOL; (* P_suction < 20 bar *)
    bWarning_TrueMeltTemp_H             : BOOL; (* T_melt > 245 deg C *)
    bWarning_TrueMeltTemp_L             : BOOL; (* T_melt < 185 deg C *)
    bWarning_MFI_Deviation_H            : BOOL; (* MFI > 1.5% high *)
    bWarning_MFI_Deviation_L            : BOOL; (* MFI < 1.5% low *)
    bWarning_FeederStarvation           : BOOL;
    bWarning_TMR_ChannelDiscrepancy     : BOOL;
    bWarning_DiePressure_ROC            : BOOL;

    (* First-Out Latching Engine *)
    iFirstOutAlarmCode                  : INT := 0;
    dwFirstOutTimestamp                 : DWORD := 0;
    bTripLatched                        : BOOL := FALSE;
    bWarningLatched                     : BOOL := FALSE;
    iLoopIndex_i                        : INT;
    iLoopIndex_j                        : INT;
    rTempCalc_A                         : REAL;
    rTempCalc_B                         : REAL;
    rTempCalc_C                         : REAL;
END_VAR
