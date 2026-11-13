# mine_vod_fan_builder/st_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Mining_VentilationOnDemand_MainMineFan_AntiStall_ToxicGas
(*
========================================================================================================================
CYBER-PHYSICAL SUBSYSTEM ARCHITECTURAL SPECIFICATION:
  - System Identifier  : FB_Mining_VentilationOnDemand_MainMineFan_AntiStall_ToxicGas
  - Industrial Domain  : Deep Underground Metal Mining & Subsurface Extraction (Gold / Copper / Platinum / Nickel)
  - Target Facility    : Dual 3.5 MW Variable-Pitch Axial Surface Main Exhaust Fans & 24 Automated Underground Louvers
  - Shaft Geometries   : Downcast Intake Shaft & Upcast Exhaust Shaft Depth: 2,400 meters (Hydrostatic Pressure Profile)
  - Fan Aerodynamics   : Dual Variable-Pitch In-Motion Variable-Speed Axial Fans (Lead/Lag or 2x Parallel 50% Operation)
  - Dynamic Anti-Stall : Real-Time Operating Point Distance-to-Stall Margin (SM) Tracking on Pressure-Flow Characteristic
  - Gas Dispersion     : Dynamic Clearance Tracking for Post-Blast Fumes (CO, NO2) and Diesel Particulate Matter (DPM)
  - Density Scaling    : Subterranean Hydrostatic Barometric Pressure Scaling: rho(z) = P(z) / (R_air * T(z))
  - Fire Safety Guard  : Thomas-Heselden-Kennedy Critical Backlayering Smoke Reversal Prevention Interlock
  - Execution Interval : Deterministic Real-Time Synchronous Execution Cycle Ts = 50.0 ms (20 Hz Scan Frequency)
========================================================================================================================
MATHEMATICAL & CYBER-PHYSICAL FOUNDATIONS:
  1. Discrete 6x6 State-Space Dynamic Matrices (A, B, C, D) representing:
     * x[1]: Surface main fan static pressure rise Delta_P [kPa]
     * x[2]: Total subterranean airway mass flow Q_mass [kg/s]
     * x[3]: Aerodynamic stall margin index SM [%] (Operating point distance to rotating stall line)
     * x[4]: Dynamic blade tip turbulence pressure fluctuations P_turb [Pa RMS]
     * x[5]: Underground work-heading equivalent toxic gas loading (CO/NO2/DPM composite) [ppm eq]
     * x[6]: Subterranean airway shaft differential barometric pressure Delta_P_shaft [kPa]
  2. Luenberger Dynamic State Observer with Innovation Gain Matrix L (6x6) for rapid estimation convergence.
  3. Receding-Horizon Model Predictive Control (MPC) with 10 Unrolled Projected Gradient Descent (PGD) Iterations:
     * Optimizes surface fan VFD RPM commands, hydraulic blade pitch servo angles, and 24 branch louver dampers.
     * Quadratic penalties: State tracking error Q, actuator effort R, slew-rate smoothness S, terminal cost P.
     * Anti-stall barrier penalty function: Exponential cost penalty as stall margin approaches critical limit (SM < 15%).
  4. 2oo3 Triple Modular Redundancy (TMR) Voting Architecture Across 4 Multi-Sensor Channels:
     * Main fan intake differential pressure transmitters (Fan_DP: 1, 2, 3) [kPa]
     * Ultrasonic multi-path airway velocity flowmeters (Air_Vel: 1, 2, 3) [m/s]
     * Borehole electrochemical toxic gas telemetry sensors (Toxic_Gas: 1, 2, 3) [ppm CO]
     * Fan bearing triaxial seismic vibration velocity transducers (Fan_Vib: 1, 2, 3) [mm/s RMS]
     * Discrepancy accumulation timers (250 ms threshold) with bumpless degradation (2oo3 -> 1oo2 -> 1oo1 -> Trip).
  5. Deterministic 14-Stage Production Finite State Machine (States 0 through 13):
     * State 0:  STATE_IDLE
     * State 1:  STATE_SURFACE_FAN_LUBE_OIL_PRESSURE_LOCK
     * State 2:  STATE_HYDRAULIC_BLADE_PITCH_ZERO_RETURN
     * State 3:  STATE_SURFACE_MAIN_MOTOR_SOFT_START_SPINUP
     * State 4:  STATE_AERODYNAMIC_BLADE_PITCH_MINIMUM_LOAD_RAMP
     * State 5:  STATE_UNDERGROUND_LOUVER_INITIAL_CALIBRATION_SWEEP
     * State 6:  STATE_NOMINAL_VOD_CLOSED_LOOP_MPC_RUN
     * State 7:  STATE_POST_BLAST_CLEARANCE_MAXIMUM_AIRFLOW_PURGE
     * State 8:  STATE_HEAVY_DIESEL_HAULAGE_LOCAL_BOOST_MODE
     * State 9:  STATE_AERODYNAMIC_STALL_WARNING_PITCH_RELIEF
     * State 10: STATE_AIRWAY_ICE_PREVENTION_INTAKE_COIL_HEAT
     * State 11: STATE_CONTROLLED_AIRWAY_RAMPDOWN_AND_FLOAT
     * State 12: STATE_SURFACE_FAN_STANDBY_COOLDOWN_PURGE
     * State 13: STATE_EMERGENCY_UNDERGROUND_FIRE_SMOKE_ISOLATION_TRIP
  6. ISA-18.2 Multi-Tier Process Alarms (HH, H, L, LL, Deadband Hysteresis) with 4x Bit-Packed 32-Bit DWORDs.
========================================================================================================================
*)
VAR_INPUT
    (* --- Master Supervisory Commands & Mode Controls --- *)
    bEnable : BOOL := FALSE; (* Master Ventilation on Demand System Enable Command [BOOL] *)
    bReset : BOOL := FALSE; (* Master Fault, Trip and Diagnostic Alarm Reset [BOOL] *)
    bAutoVOD_Mode : BOOL := FALSE; (* Automatic Ventilation on Demand closed-loop optimizer active [BOOL] *)
    bDualFanParallelMode : BOOL := FALSE; (* Dual 3.5 MW fan parallel run enable (TRUE) or single lead/lag (FALSE) [BOOL] *)
    bLeadFanSelect : BOOL := FALSE; (* Primary lead fan selector: FALSE = Fan 1 Lead, TRUE = Fan 2 Lead [BOOL] *)
    bPostBlastPurgeRequest : BOOL := FALSE; (* Post-blast fume clearance maximum purge cycle command [BOOL] *)
    bDieselHaulageBoostRequest : BOOL := FALSE; (* Dynamic diesel haulage fleet peak airflow boost request [BOOL] *)
    bAntiStallPitchReliefEnable : BOOL := TRUE; (* Automatic blade pitch relief interlock on stall warning [BOOL] *)
    bIcePreventionEnable : BOOL := TRUE; (* Surface collar intake coil thermal freeze prevention enable [BOOL] *)
    bFireSmokeEmergencyTrip : BOOL := FALSE; (* Underground fire emergency trip & smoke rollback containment [BOOL] *)
    bEmergencyStop : BOOL := FALSE; (* Hardwired SIL-3 emergency stop push-button interlock [BOOL] *)

    (* --- Surface Main Fan 1 Telemetry & Mechanical Health --- *)
    rFan1_MotorCurrent_A : REAL := 0.0; (* Fan 1 3.5 MW Induction Motor Stator Current [A] *)
    rFan1_MotorSpeed_RPM : REAL := 0.0; (* Fan 1 Motor Shaft Rotational Speed [RPM] *)
    rFan1_MotorWindingTemp_degC : REAL := 45.0; (* Fan 1 Motor Stator Winding Highest RTD Temperature [deg C] *)
    rFan1_BearingDriveEndTemp_degC : REAL := 42.0; (* Fan 1 Drive-End Journal Bearing Metal Temperature [deg C] *)
    rFan1_BearingNonDriveTemp_degC : REAL := 40.0; (* Fan 1 Non-Drive End Journal Bearing Metal Temperature [deg C] *)
    rFan1_LubeOilPressure_bar : REAL := 4.2; (* Fan 1 Forced Lubrication Supply Header Oil Pressure [bar] *)
    rFan1_LubeOilTemp_degC : REAL := 38.0; (* Fan 1 Lubrication Oil Sump Reservoir Temperature [deg C] *)
    rFan1_BladePitchFeedback_deg : REAL := 0.0; (* Fan 1 Hydraulic Actuator Blade Pitch Angle Feedback [deg] *)
    rFan1_HydraulicServoPressure_bar : REAL := 145.0; (* Fan 1 Blade Pitch Hydraulic Swashplate Servo Pressure [bar] *)

    (* --- Surface Main Fan 2 Telemetry & Mechanical Health --- *)
    rFan2_MotorCurrent_A : REAL := 0.0; (* Fan 2 3.5 MW Induction Motor Stator Current [A] *)
    rFan2_MotorSpeed_RPM : REAL := 0.0; (* Fan 2 Motor Shaft Rotational Speed [RPM] *)
    rFan2_MotorWindingTemp_degC : REAL := 45.0; (* Fan 2 Motor Stator Winding Highest RTD Temperature [deg C] *)
    rFan2_BearingDriveEndTemp_degC : REAL := 42.0; (* Fan 2 Drive-End Journal Bearing Metal Temperature [deg C] *)
    rFan2_BearingNonDriveTemp_degC : REAL := 40.0; (* Fan 2 Non-Drive End Journal Bearing Metal Temperature [deg C] *)
    rFan2_LubeOilPressure_bar : REAL := 4.2; (* Fan 2 Forced Lubrication Supply Header Oil Pressure [bar] *)
    rFan2_LubeOilTemp_degC : REAL := 38.0; (* Fan 2 Lubrication Oil Sump Reservoir Temperature [deg C] *)
    rFan2_BladePitchFeedback_deg : REAL := 0.0; (* Fan 2 Hydraulic Actuator Blade Pitch Angle Feedback [deg] *)
    rFan2_HydraulicServoPressure_bar : REAL := 145.0; (* Fan 2 Blade Pitch Hydraulic Swashplate Servo Pressure [bar] *)

    (* --- 2oo3 Triple Modular Redundant (TMR) Sensor Channels --- *)
    rFan_DP_Ch1 : REAL := 3.5; (* Surface Main Fan Intake Differential Pressure Transmitter Ch1 [kPa] *)
    rFan_DP_Ch2 : REAL := 3.5; (* Surface Main Fan Intake Differential Pressure Transmitter Ch2 [kPa] *)
    rFan_DP_Ch3 : REAL := 3.5; (* Surface Main Fan Intake Differential Pressure Transmitter Ch3 [kPa] *)
    rAir_Vel_Ch1 : REAL := 18.2; (* Surface Exhaust Shaft Ultrasonic Flowmeter Velocity Ch1 [m/s] *)
    rAir_Vel_Ch2 : REAL := 18.2; (* Surface Exhaust Shaft Ultrasonic Flowmeter Velocity Ch2 [m/s] *)
    rAir_Vel_Ch3 : REAL := 18.2; (* Surface Exhaust Shaft Ultrasonic Flowmeter Velocity Ch3 [m/s] *)
    rToxic_Gas_Ch1 : REAL := 12.0; (* Work-Heading Multi-Gas Borehole Telemetry Carbon Monoxide Ch1 [ppm] *)
    rToxic_Gas_Ch2 : REAL := 12.0; (* Work-Heading Multi-Gas Borehole Telemetry Carbon Monoxide Ch2 [ppm] *)
    rToxic_Gas_Ch3 : REAL := 12.0; (* Work-Heading Multi-Gas Borehole Telemetry Carbon Monoxide Ch3 [ppm] *)
    rFan_Vib_Ch1 : REAL := 1.8; (* Surface Fan Triaxial Seismic Bearing Vibration Velocity Ch1 [mm/s] *)
    rFan_Vib_Ch2 : REAL := 1.8; (* Surface Fan Triaxial Seismic Bearing Vibration Velocity Ch2 [mm/s] *)
    rFan_Vib_Ch3 : REAL := 1.8; (* Surface Fan Triaxial Seismic Bearing Vibration Velocity Ch3 [mm/s] *)

    (* --- Subterranean Environmental, Barometric & Thermodynamic Telemetry --- *)
    rSurfaceBaroPressure_kPa : REAL := 98.5; (* Surface Weather Substation Ambient Barometric Pressure [kPa] *)
    rSurfaceAirTemp_degC : REAL := 12.0; (* Surface Ambient Outside Air Temperature [deg C] *)
    rSurfaceRelativeHumidity_pct : REAL := 65.0; (* Surface Ambient Air Relative Humidity [%] *)
    rShaftDepth_m : REAL := 2400.0; (* Deep Metal Mine Total Vertical Shaft Depth [m] *)
    rShaftBottomBaroPressure_kPa : REAL := 128.5; (* 2,400 m Subterranean Level Hydrostatic Barometric Pressure [kPa] *)
    rShaftBottomAirTemp_degC : REAL := 34.5; (* 2,400 m Subterranean Level Intake Air Temperature [deg C] *)
    rUndergroundWBGT_degC : REAL := 27.8; (* Subterranean Mining Heading Wet-Bulb Globe Temperature [deg C] *)
    rIntakeHeatingCoilWaterSupplyTemp_degC : REAL := 75.0; (* Surface Intake Shaft Collar Heating Coil Water Supply [deg C] *)
    rIntakeHeatingCoilWaterReturnTemp_degC : REAL := 55.0; (* Surface Intake Shaft Collar Heating Coil Water Return [deg C] *)

    (* --- Mine Production, Diesel Fleet & Fire Hazard Parameters --- *)
    rTotalActiveDieselPower_kW : REAL := 4200.0; (* Sum of Operating Underground Diesel LHDs and Trucks [kW] *)
    rPostBlastFumeInitialMass_kg : REAL := 850.0; (* Blasting Event Estimated Toxic Gas Mass Release [kg] *)
    rEstimatedFireHeatRelease_MW : REAL := 5.0; (* Underground Fire Scenario Heat Release Rate Assessment [MW] *)
    iActiveBlastingZoneIndex : INT := 0; (* Active Post-Blast Ventilation Priority Zone Index (0 = None, 1..24) [count] *)
    iFireZoneIndex : INT := 0; (* Underground Fire Smoke Detection Active Zone Index (0 = None, 1..24) [count] *)

    (* --- 24 Underground Automated Branch Louvers / Regulators Telemetry --- *)
    arrLouverPosFeedback_pct : ARRAY[1..24] OF REAL; (* Branch 1..24 Active Louver Damper Position Feedback [%] *)
    arrZoneVelocity_mps : ARRAY[1..24] OF REAL; (* Branch 1..24 Airway Ultrasonic Flow Velocity Measurement [m/s] *)
    arrZoneCO_ppm : ARRAY[1..24] OF REAL; (* Branch 1..24 Electrochemical Sensor Carbon Monoxide Level [ppm] *)
    arrZoneNO2_ppm : ARRAY[1..24] OF REAL; (* Branch 1..24 Electrochemical Sensor Nitrogen Dioxide Level [ppm] *)
    arrZoneDPM_ug_m3 : ARRAY[1..24] OF REAL; (* Branch 1..24 Laser Photometer Diesel Particulate Matter [ug/m3] *)
    arrZoneDieselFleet_kW : ARRAY[1..24] OF REAL; (* Branch 1..24 Total Active Diesel Engine Nameplate Power [kW] *)
    arrZoneBlastActive : ARRAY[1..24] OF BOOL; (* Branch 1..24 Active Blasting Fume Clearance Sequence Flag [BOOL] *)
    arrZoneFireAlarm : ARRAY[1..24] OF BOOL; (* Branch 1..24 Thermal / Optical Fire Smoke Alarm Detected [BOOL] *)

    (* --- Execution Cycle Timing --- *)
    rCycleTime_s : REAL := 0.050; (* Real-time synchronous PLC scan execution cycle period [s] *)
END_VAR
VAR_OUTPUT
    (* --- Surface Main Fan Actuator Analog & Digital Commands --- *)
    rFan1_VFD_SpeedCmd_RPM : REAL; (* Main Fan 1 Variable Frequency Drive Speed Command [RPM] *)
    rFan1_BladePitchCmd_deg : REAL; (* Main Fan 1 Hydraulic Actuator Blade Pitch Angle Command [deg] *)
    rFan2_VFD_SpeedCmd_RPM : REAL; (* Main Fan 2 Variable Frequency Drive Speed Command [RPM] *)
    rFan2_BladePitchCmd_deg : REAL; (* Main Fan 2 Hydraulic Actuator Blade Pitch Angle Command [deg] *)
    bFan1_RunCmd : BOOL; (* Main Fan 1 3.5 MW Drive Motor Main Contactor Run Command [BOOL] *)
    bFan2_RunCmd : BOOL; (* Main Fan 2 3.5 MW Drive Motor Main Contactor Run Command [BOOL] *)
    bFanAntiStallBypassDamperOpenCmd : BOOL; (* Surface Fan Substation Emergency Stall-Relief Bypass Damper [BOOL] *)
    rIntakeCollarHeaterValveCmd_pct : REAL; (* Surface Collar Intake Shaft Thermal Freeze Protection Valve [%] *)
    rSurfaceFanLubePumpRunCmd : BOOL; (* Surface Fan Forced Lubrication Pump Motor Run Command [BOOL] *)
    rSurfaceFanHydraulicPumpRunCmd : BOOL; (* Surface Fan Blade Pitch Hydraulic Power Unit Run Command [BOOL] *)

    (* --- 24 Underground Automated Branch Louvers & Booster Commands --- *)
    arrLouverCmd_pct : ARRAY[1..24] OF REAL; (* Branch 1..24 Regulating Louver Damper Position Setpoint [%] *)
    arrAuxBoosterFanCmd_pct : ARRAY[1..24] OF REAL; (* Heading 1..24 Auxiliary Booster Fan VFD Speed Command [%] *)
    arrZoneAirflowDelivery_m3s : ARRAY[1..24] OF REAL; (* Branch 1..24 Real-Time Volumetric Airflow Delivered [m3/s] *)
    arrZoneAirflowDeficit_m3s : ARRAY[1..24] OF REAL; (* Branch 1..24 Airflow Deficit Relative to Regulatory Min [m3/s] *)
    arrZoneEvacuationRequired : ARRAY[1..24] OF BOOL; (* Branch 1..24 Toxic Gas Exceedance Personnel Evacuation Flag [BOOL] *)

    (* --- Key Aerodynamic, Thermodynamic & Anti-Stall Indicators --- *)
    rFanStallMargin_pct : REAL; (* Real-Time Calculated Distance-to-Stall Margin Index [%] *)
    rBladeTipTurbulenceRMS_Pa : REAL; (* High-Frequency Dynamic Pressure Sensor Blade Tip Turbulence [Pa] *)
    rTotalAirwayMassFlow_kgs : REAL; (* Subterranean Mine Total Exhaust Airway Mass Flow Rate [kg/s] *)
    rTotalAirwayVolumeFlow_m3s : REAL; (* Surface Substation Volumetric Exhaust Flow at Surface Density [m3/s] *)
    rSubterraneanAirDensity_kgm3 : REAL; (* 2,400 m Subterranean Level Hydrostatically Scaled Air Density [kg/m3] *)
    rAirwayCriticalBacklayeringVelocity_mps : REAL; (* Fire Smoke Upstream Reversal Prevention Critical Speed [m/s] *)
    rActiveMineAtkinsonResistance_kPas2_m6 : REAL; (* Real-Time Subterranean Airway Atkinson Resistance Equivalent [kPa.s2/m6] *)
    rPostBlastPurgeTimeRemaining_s : REAL; (* Calculated Clearance Time for Blast Gases to Drop Below Safe Limits [s] *)
    rMineThermalHeatStressIndex_degC : REAL; (* Heading Ambient Equivalent Wet-Bulb Heat Stress Indicator [deg C] *)

    (* --- Safety Interlocks, FSM Status & Alarms --- *)
    iCurrentState : INT; (* 14-Stage Production Finite State Machine Current State Index (0..13) [count] *)
    bTripGeneral : BOOL; (* Master Critical Process Trip Interlock Active [BOOL] *)
    bWarningGeneral : BOOL; (* Master Advisory Process Warning Interlock Active [BOOL] *)
    bAntiStallActive : BOOL; (* Dynamic Aerodynamic Stall Relief Sequence Currently Engaging [BOOL] *)
    bSmokeReversalLockEngaged : BOOL; (* Critical Airflow Smoke Backlayering Lock Preventing Louver Throttling [BOOL] *)
    dwAlarmWord1 : DWORD; (* ISA-18.2 Bit-Packed High-High (HH) and Low-Low (LL) Critical Trips [DWORD] *)
    dwAlarmWord2 : DWORD; (* ISA-18.2 Bit-Packed High (H) and Low (L) Warnings & Sensor Faults [DWORD] *)
    dwStatusWord1 : DWORD; (* Subsystem Operating States, Lead/Lag Fan Modes & FSM Indicators [DWORD] *)
    dwStatusWord2 : DWORD; (* VOD Active Sectors, TMR Redundancy Degradation & Interlock Locks [DWORD] *)
END_VAR
"""
