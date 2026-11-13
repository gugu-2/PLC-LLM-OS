# brewery_builder/part1_header_io.py

def get_part1():
    return """FUNCTION_BLOCK FB_FoodBev_Brewery_LauterTun_WortRake_MashBoil
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: FOOD & BEVERAGE / INDUSTRIAL BREWERY PROCESSING
SYSTEM: 500 BBL/BREW COMMERCIAL BREWHOUSE CONTINUOUS PROCESS BLOCK
SUBSYSTEMS:
  1. LAUTER TUN RUNOFF & GRAIN BED COMPACTION (DARCY'S LAW FLUID DYNAMICS)
  2. MULTI-AXIS WORT RAKE VERTICAL ELEVATION & HYDRAULIC CUTTING VFD
  3. OPTICAL VORLAUF DUAL-ANGLE TURBIDITY RECIRCULATION CLARIFICATION
  4. INTERNAL FORCED-CIRCULATION CALANDRIA WORT KETTLE BOILING & EVAPORATION
  5. DIMETHYL SULFIDE (DMS) CHEMICAL DEGRADATION & VOLATILE STRIPPING OBSERVER
  6. TANGENTIAL INLET WHIRLPOOL HYDRODYNAMIC TRUB CONE CENTRIPETAL SEPARATION
  7. FIRST-PRINCIPLES 6-STATE DISCRETE STATE-SPACE OBSERVER (Ts = 100 [ms])
  8. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH UNROLLED PGD (10 ITERATIONS)
  9. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE (6 CRITICAL CHANNELS)
 10. DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (STATES 0 TO 13)
 11. ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX & 32-BIT PACKED TELEMETRY
====================================================================================================
MATHEMATICAL FOUNDATION & PROCESS DYNAMICS:
  - Grain Bed Fluid Flow (Darcy's Law for Compressible Porous Beds):
      Q_runoff = (K_bed * A_tun / (mu_wort * L_bed)) * Delta_P
      d(Delta_P)/dt = alpha_compaction * (Q_runoff)^1.8 - beta_rake * (omega_rake * z_rake_depth)
  - Turbidity Clearance (Vorlauf Recirculation Filtration Kinetics):
      d(Turb)/dt = - k_vorlauf * Q_recirc * Turb / (V_underlet + V_bed_void)
  - Kettle Calandria Heat Transfer & Evaporation Rate:
      Q_thermal = U_calandria * A_calandria * (T_steam - T_wort)
      d(T_wort)/dt = (Q_thermal - Q_loss - Q_evap) / (M_wort * Cp_wort)
      Evap_rate [%/h] = (m_dot_evap * 3600.0 / M_wort) * 100.0
  - DMS Stripping Reaction Kinetics (S-Methylmethionine -> DMS -> Vapor):
      d[SMM]/dt = - k_smm(T_wort) * [SMM]
      d[DMS]/dt = k_smm(T_wort) * [SMM] - k_vol(Evap_rate) * [DMS]
====================================================================================================
*)

VAR_INPUT
    (* Master Execution & Brewhouse Cycle Control *)
    bExecute                            : BOOL := FALSE;    (* Master Execution Enable Command *)
    bReset                              : BOOL := FALSE;    (* Fault Reset and Latched Alarm Clearance *)
    bAutoMode                           : BOOL := TRUE;     (* Brewhouse Operating Mode: TRUE=Automatic, FALSE=Manual *)
    bEmergencyStop                      : BOOL := FALSE;    (* Hardwired Emergency Stop Safety Circuit Healthy: FALSE=Tripped *)
    fScanCycleTime                      : REAL := 0.100;    (* Discrete Task Execution Sample Time Ts [s] *)

    (* Lauter Tun Differential Pressure 2oo3 TMR Sensor Channels *)
    fLauterDP_Sensor1                   : REAL := 0.0;      (* Lauter Tun Bed Differential Pressure Transmitter 1 [mbar] *)
    fLauterDP_Sensor2                   : REAL := 0.0;      (* Lauter Tun Bed Differential Pressure Transmitter 2 [mbar] *)
    fLauterDP_Sensor3                   : REAL := 0.0;      (* Lauter Tun Bed Differential Pressure Transmitter 3 [mbar] *)

    (* Vorlauf Optical Wort Turbidity 2oo3 TMR Sensor Channels *)
    fVorlaufTurb_Sensor1                : REAL := 0.0;      (* Vorlauf Runoff Wort Optical Clarity/Turbidity 1 [EBC] *)
    fVorlaufTurb_Sensor2                : REAL := 0.0;      (* Vorlauf Runoff Wort Optical Clarity/Turbidity 2 [EBC] *)
    fVorlaufTurb_Sensor3                : REAL := 0.0;      (* Vorlauf Runoff Wort Optical Clarity/Turbidity 3 [EBC] *)

    (* Wort Kettle Calandria Boiling Temperature 2oo3 TMR Sensor Channels *)
    fKettleTemp_Sensor1                 : REAL := 20.0;     (* Wort Kettle Boiling Temperature RTD Transmitter 1 [deg C] *)
    fKettleTemp_Sensor2                 : REAL := 20.0;     (* Wort Kettle Boiling Temperature RTD Transmitter 2 [deg C] *)
    fKettleTemp_Sensor3                 : REAL := 20.0;     (* Wort Kettle Boiling Temperature RTD Transmitter 3 [deg C] *)

    (* Wort Kettle Filling & Boiling Level 2oo3 TMR Sensor Channels *)
    fKettleLevel_Sensor1                : REAL := 0.0;      (* Wort Kettle Radar Level Transmitter 1 [%] *)
    fKettleLevel_Sensor2                : REAL := 0.0;      (* Wort Kettle Radar Level Transmitter 2 [%] *)
    fKettleLevel_Sensor3                : REAL := 0.0;      (* Wort Kettle Radar Level Transmitter 3 [%] *)

    (* Calandria Steam Supply Header Pressure 2oo3 TMR Sensor Channels *)
    fCalandriaSteamP_Sensor1            : REAL := 0.0;      (* Calandria Saturated Steam Header Pressure 1 [bar] *)
    fCalandriaSteamP_Sensor2            : REAL := 0.0;      (* Calandria Saturated Steam Header Pressure 2 [bar] *)
    fCalandriaSteamP_Sensor3            : REAL := 0.0;      (* Calandria Saturated Steam Header Pressure 3 [bar] *)

    (* Lauter Runoff Mass/Volumetric Flowmeter 2oo3 TMR Sensor Channels *)
    fRunoffFlow_Sensor1                 : REAL := 0.0;      (* Lauter Runoff Magnetic Flowmeter Channel 1 [hL/h] *)
    fRunoffFlow_Sensor2                 : REAL := 0.0;      (* Lauter Runoff Magnetic Flowmeter Channel 2 [hL/h] *)
    fRunoffFlow_Sensor3                 : REAL := 0.0;      (* Lauter Runoff Magnetic Flowmeter Channel 3 [hL/h] *)

    (* Brewhouse Process Instrumentation & Feedback Transmitters *)
    fLauterTunLevel                     : REAL := 0.0;      (* Lauter Tun Hydrostatic Head Liquid Level [mm] *)
    fRakeActualHeight                   : REAL := 0.0;      (* Wort Rake Vertical Position Laser/LVDT Feedback [mm] *)
    fRakeActualSpeed                    : REAL := 0.0;      (* Wort Rake Rotational Speed VFD Encoder Feedback [RPM] *)
    fRakeMotorTorque                    : REAL := 0.0;      (* Wort Rake Drive Motor Dynamic Load Torque [Nm] *)
    fRakeMotorCurrent                   : REAL := 0.0;      (* Wort Rake VFD Drive Output Current Feedback [A] *)
    fSpargeWaterTemp                    : REAL := 78.0;     (* Sparging Hot Liquor Supply Temperature Transmitter [deg C] *)
    fSpargeWaterFlow                    : REAL := 0.0;      (* Sparging Hot Liquor Mass Flowmeter Transmitter [hL/h] *)
    fWortGravityPlato                   : REAL := 12.0;     (* Inline Sound Velocity / Coriolis Wort Extract Density [deg Plato] *)
    fVaporCondenserCoolingFlow          : REAL := 15.0;     (* Kettle Vapor Condenser Cooling Water Flow [m3/h] *)
    fCalandriaCirculationPumpDiffP      : REAL := 1.2;      (* Calandria Forced Recirculation Pump Differential Head [bar] *)
    fWhirlpoolInletVelocity             : REAL := 0.0;      (* Whirlpool Tangential Nozzle Wort Velocity [m/s] *)
    fCIPCausticConductivity             : REAL := 0.0;      (* CIP Loop Caustic Wash Chemical Conductivity Transmitter [mS/cm] *)

    (* Brewhouse Recipe Setpoints & Process Configuration Parameters *)
    fBatchVolumeTarget                  : REAL := 586.0;    (* Brewhouse Batch Finished Wort Target Volume [hL] *)
    fTargetWortTurbidity                : REAL := 25.0;     (* Maximum Permissible Vorlauf Turbidity Threshold [EBC] *)
    fTargetBoilEvaporationRate          : REAL := 6.5;      (* Target Continuous Kettle Evaporation Rate [%/h] *)
    fTargetBoilDurationMinutes          : REAL := 60.0;     (* Target Vigorous Wort Kettle Boil Duration [min] *)
    fTargetWhirlpoolRestMinutes         : REAL := 20.0;     (* Target Tangential Whirlpool Trub Settling Rest [min] *)
    fSweetWaterCutoffPlato              : REAL := 1.8;      (* Sparging Runoff Gravity Cutoff Threshold [deg Plato] *)
    fMaxAllowedGrainBedDP               : REAL := 45.0;     (* Maximum Allowable Grain Bed Differential Pressure [mbar] *)
    fMaxPermissibleRakeTorque           : REAL := 1600.0;   (* Mechanical Trip Threshold for Wort Rake Drive Torque [Nm] *)
    fTargetDMSConcentration             : REAL := 28.0;     (* Target DMS Residual Concentration in Boiled Wort [ppb] *)
END_VAR

VAR_OUTPUT
    (* Actuator Command Outputs - Continuous & Proportional Positioning *)
    fRakeHeightCommand                  : REAL := 0.0;      (* Wort Rake Vertical Hydraulic Lift Command [mm] *)
    fRakeSpeedCommand                   : REAL := 0.0;      (* Wort Rake Rotational Speed VFD Setpoint [RPM] *)
    fRunoffValveCommand                 : REAL := 0.0;      (* Lauter Tun Runoff Flow Control Valve Position [%] *)
    fRecircValveCommand                 : REAL := 0.0;      (* Vorlauf Recirculation Diverter Valve Position [%] *)
    fCalandriaSteamValveCommand         : REAL := 0.0;      (* Calandria Steam Supply Pressure Control Valve [%] *)
    fSpargeValveCommand                 : REAL := 0.0;      (* Hot Liquor Sparging Water Metering Valve Position [%] *)
    fWhirlpoolPumpCommand               : REAL := 0.0;      (* Whirlpool Tangential Transfer Pump Speed Reference [%] *)

    (* Actuator Command Outputs - Discrete & Digital Contactors *)
    bRunoffPumpRun                      : BOOL := FALSE;    (* Lauter Tun Variable Speed Runoff Pump Run Permissive *)
    bRecircPumpRun                      : BOOL := FALSE;    (* Vorlauf Recirculation Booster Pump Run Permissive *)
    bCalandriaCircPumpRun               : BOOL := FALSE;    (* Kettle Calandria Forced Circulation Pump Contactor *)
    bSpentGrainDischargeDoorOpen        : BOOL := FALSE;    (* Lauter Tun Spent Grain Evacuation Door Hydraulic Actuator *)
    bHopDoserValve1                     : BOOL := FALSE;    (* Bittering Hop Dosing Vessel Discharge Valve Solenoid *)
    bHopDoserValve2                     : BOOL := FALSE;    (* Aroma Hop Dosing Vessel Discharge Valve Solenoid *)
    bCIPSupplyValveOpen                 : BOOL := FALSE;    (* Brewhouse Automated CIP Supply Manifold Isolation Valve *)
    bVaporCondenserPumpRun              : BOOL := FALSE;    (* Kettle Vapor Exhaust Condenser Spray Pump Contactor *)

    (* Process State & Quality Indicators *)
    iCurrentState                       : INT := 0;         (* Active Brewhouse Production Finite State Machine Code *)
    iCurrentSubStep                     : INT := 0;         (* Active FSM Internal Sequence Substep Identifier *)
    fStateElapsedTimeSec                : REAL := 0.0;      (* Time Elapsed in Current Master FSM Stage [s] *)
    fTotalBatchElapsedTimeMin           : REAL := 0.0;      (* Total Cumulative Brewhouse Batch Cycle Time [min] *)
    fEstimatedGrainBedPermeability      : REAL := 0.0;      (* Estimated Grain Bed Darcy Hydraulic Permeability [m2] *)
    fCumulativeEvaporationPercent       : REAL := 0.0;      (* Kettle Total Cumulative Evaporated Volume Fraction [%] *)
    fEstimatedResidualDMS               : REAL := 120.0;    (* Observer Estimated Volatile DMS Concentration [ppb] *)

    (* 2oo3 TMR Synthesized Voted Process Values *)
    fVotedGrainBedDP                    : REAL := 0.0;      (* 2oo3 Synthesized Lauter Tun Grain Bed Diff Pressure [mbar] *)
    fVotedWortTurbidity                 : REAL := 0.0;      (* 2oo3 Synthesized Vorlauf Runoff Wort Turbidity [EBC] *)
    fVotedKettleTemp                    : REAL := 20.0;     (* 2oo3 Synthesized Wort Kettle Boiling Temperature [deg C] *)
    fVotedKettleLevel                   : REAL := 0.0;      (* 2oo3 Synthesized Wort Kettle Hydrostatic Level [%] *)
    fVotedCalandriaSteamP               : REAL := 0.0;      (* 2oo3 Synthesized Calandria Steam Supply Pressure [bar] *)
    fVotedRunoffFlow                    : REAL := 0.0;      (* 2oo3 Synthesized Lauter Tun Runoff Mass Flow [hL/h] *)

    (* Standardized Bit-Packed Telemetry & Diagnostic Status Words *)
    dwStatusWord1                       : DWORD := 16#00000000; (* Brewhouse FSM States, Run Modes, Permissives *)
    dwStatusWord2                       : DWORD := 16#00000000; (* Actuator Feedbacks, TMR Degradation Status Masks *)
    dwAlarmWord1                        : DWORD := 16#00000000; (* ISA-18.2 Critical Process Alarms (HH / LL Trips) *)
    dwAlarmWord2                        : DWORD := 16#00000000; (* ISA-18.2 Warning Process Alarms (H / L Warnings) *)
    dwFirstOutWord                      : DWORD := 16#00000000; (* Root-Cause Latched Trip Identifier Mask *)

    (* Master Health & Interlock Outputs *)
    bReady                              : BOOL := FALSE;    (* Brewhouse Process Block Initialized and Ready *)
    bActive                             : BOOL := FALSE;    (* Brewhouse Process Block In Active Production Execution *)
    bError                              : BOOL := FALSE;    (* Brewhouse General Error Condition Latched *)
    bAlarmHighHigh                      : BOOL := FALSE;    (* Common Priority 1 (High-High) Critical Alarm Active *)
    bDegradedTMRMode                    : BOOL := FALSE;    (* 2oo3 TMR Operating in Degraded Sensor Redundancy Mode *)
    bBedChokeDetected                   : BOOL := FALSE;    (* Grain Bed Compaction / Hydraulic Choking Early Warning *)
    bCalandriaFoulingAlarm              : BOOL := FALSE;    (* Calandria Heat Exchanger Organic Scale / Fouling Warning *)
END_VAR
"""
