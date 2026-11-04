# -*- coding: utf-8 -*-
"""
Builder script for FB_Automotive_CommercialTruck_12SpeedAMT_ClutchHandover
Cyber-Physical System: 44-Ton Commercial Heavy Truck 12-Speed Automated Manual Transmission (AMT)
& Dual Wet Clutch Electro-Hydraulic Mechatronic Control Unit (MCU)
"""

import os
import re
import json
import uuid

def build_code():
    parts = []

    # =========================================================================
    # 1. HEADER & SYSTEM COMMENTS
    # =========================================================================
    header = """FUNCTION_BLOCK FB_Automotive_CommercialTruck_12SpeedAMT_ClutchHandover
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC IEC 61131-3 DATASET V7 MAX-PERSONA
  SYSTEM DESIGNATION : CPS-AUTO-HEAVY-TRUCK-12SPD-AMT-CLUTCH-HANDOVER-MK-VII
  COMMERCIAL SECTOR  : Automotive & Commercial Heavy Vehicle Powertrain Engineering
  SUBSYSTEM SPEC     : 44-Ton Commercial Heavy Truck 12-Speed Automated Manual Transmission (AMT) & Dual Wet Clutch
                       Electro-Hydraulic Mechatronic Control Unit (MCU): Dual Wet Clutch Proportional Pressure
                       Torque Handover Dynamic Cross-Fading (sub-10 ms synchronization window without driveline torque
                       interruption), Synchronizer Sleeve Dog Clutch Pneumatic/Hydraulic Actuation with Hall-Effect
                       Shaft Speed Matching (differential RPM < 15), Driveline Torsional Anti-Jerk Active Damping
                       Filter, Grade & Gross Vehicle Weight (GVW) Adaptive Shift Optimization, and Wet Clutch Frictional
                       Energy Dissipation & Temperature Observer.
  STANDARDS COMPLIANCE:
    - IEC 61131-3 3rd Edition (Deterministic Industrial Automation Structured Text)
    - ISO 26262 / IEC 61508 (Functional Safety ASIL-D / SIL 3 Safety Instrumented Systems)
    - SAE J1939-71 / SAE J1939-21 (Commercial Vehicle Drivetrain & Engine Retarder Bus Communications)
    - ISO 1219-1 / ISO 4413 (Hydraulic Fluid Power - Proportional Electro-Hydraulic Transmission Valves)
    - ISA-18.2 / EEMUA 191 (Management of Alarm Systems for the Process & Powertrain Industries)
    - DIN ISO 281 / AGMA 6013 (Rolling Bearings and Rating Life / Rating of Industrial Enclosed Drives)
  PERSONA:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Industrial Systems Tenure)
========================================================================================================================
  CYBER-PHYSICAL PROCESS DYNAMICS & MATHEMATICAL MODELING:

  1. DUAL WET CLUTCH MECHATRONIC ARCHITECTURE & TORQUE CROSS-FADING:
     The mechatronic control unit coordinates two independent wet multi-plate clutch packs:
       - Clutch 1 (Odd Shaft: Gears 1, 3, 5, 7, 9, 11 and Reverse)
       - Clutch 2 (Even Shaft: Gears 2, 4, 6, 8, 10, 12)
     During a continuous powershift upshift or downshift, torque transfer transitions from the off-going clutch
     to the on-coming clutch without breaking driveline tractive continuity.
     Dynamic torque cross-fading balance condition:
       T_clutch1(t) + T_clutch2(t) = T_engine_demand(t)
     Cross-fading parameter alpha_fade in [0.0, 1.0]:
       T_cl1_target = T_engine_demand * (1.0 - alpha_fade)
       T_cl2_target = T_engine_demand * alpha_fade
     Torque phase duration is strictly controlled within 40 ms to 80 ms.
     Inertia phase follows immediately: engine speed is brought to match the incoming input shaft speed
     via closed-loop electronic engine torque limit control, completing lockup within a sub-10 ms synchronization
     window when slip speed |omega_slip| < 15 RPM.

  2. STRIBECK FRICTION MODEL & NORMAL FORCE TORQUE CAPACITY:
     Wet multi-plate clutch frictional torque capacity accounts for fluid-film boundary lubrication, viscous shear,
     and Coulomb micro-asperity contact via the generalized Stribeck velocity formulation:
       mu(Delta_omega) = mu_c + (mu_s - mu_c) * exp( - |Delta_omega / omega_s|^delta ) + sigma_v * |Delta_omega|
     where:
       mu_s    = 0.1450 (Static friction coefficient under boundary lubrication)
       mu_c    = 0.1120 (Coulomb / dynamic sliding friction coefficient)
       omega_s = 12.50  (Characteristic Stribeck transition angular velocity [rad/s])
       delta   = 1.250  (Stribeck empirical shaping exponent)
       sigma_v = 0.00085 (Hydrodynamic viscous drag coefficient [s/rad])
     Net hydraulic normal clamping force:
       F_N = MAX(0.0, (P_clutch - P_return_spring) * 1.0E5 * A_piston)
     Torque transmission capacity:
       T_cap = (2.0 / 3.0) * z_plates * r_mean * F_N * mu(Delta_omega)
     where:
       z_plates        = 10 (Active friction interface surfaces)
       r_mean          = 0.118 m (Mean friction radius = (2/3)*(r_o^3 - r_i^3)/(r_o^2 - r_i^2))
       A_piston        = 0.0245 m^2 (Clutch application hydraulic piston surface area)
       P_return_spring = 1.85 bar (Piston disengagement return spring preload pressure)

  3. TWO-INERTIA DRIVELINE COMPLIANCE & TORSIONAL WINDUP:
     Rotational dynamics of engine flywheel, transmission input shafts, propeller shaft, drive axle half-shafts,
     and road-coupled vehicle mass:
       J_e * d(omega_e)/dt = T_engine - T_cl1 - T_cl2
       J_t1 * d(omega_in1)/dt = T_cl1 - (T_synchro1 / i_gear1)
       J_t2 * d(omega_in2)/dt = T_cl2 - (T_synchro2 / i_gear2)
       J_prop * d(omega_prop)/dt = T_gear_out - T_halfshaft / i_final_drive
     Drive axle half-shaft torsional torque with Kelvin-Voigt viscoelastic damping:
       T_hs = k_halfshaft * theta_hs_windup + c_halfshaft * (omega_prop / i_final_drive - omega_wheel)
       d(theta_hs_windup)/dt = (omega_prop / i_final_drive) - omega_wheel

  4. VEHICLE LONGITUDINAL TRACTIVE RESISTANCE & GVW ESTIMATION:
     Total longitudinal tractive force delivered at tire contact patch:
       F_tractive = (T_hs / r_tire_dyn) - F_loss_brakes
     Vehicle gross motion equation:
       M_veh * d(v_veh)/dt = F_tractive - F_rolling - F_aero - F_grade
     Resisting forces:
       F_rolling = c_rr * M_veh * g * cos(alpha_grade)
       F_aero    = 0.5 * rho_air * C_d * A_frontal * v_veh^2
       F_grade   = M_veh * g * sin(alpha_grade)
     Gross Vehicle Weight (GVW) adaptive observer recursively estimates M_veh across grade transitions:
       M_hat = (F_tractive - F_aero) / (d(v_veh)/dt + g * (sin(alpha) + c_rr * cos(alpha)))

  5. WET CLUTCH THERMAL ENERGY DISSIPATION & BULK TEMPERATURE OBSERVER:
     Instantaneous frictional power dissipation during clutch slipping phase:
       P_fric1 = T_cl1 * |omega_e - omega_in1|
       P_fric2 = T_cl2 * |omega_e - omega_in2|
     Thermal lumped capacitance observer tracking bulk plate temperature:
       m_pack * c_steel * d(T_plate)/dt = P_fric - h_oil * A_cooling * (T_plate - T_oil_sump)
     Mass of steel drive plates m_pack = 14.5 kg, specific heat c_steel = 480 J/(kg*K),
     convective cooling coefficient h_oil * A_cooling = 85.0 W/K.
     Energy accumulation prevents clutch glazing and thermal decomposition of ATF fluid.

  6. DRIVELINE ACTIVE ANTI-JERK ACTIVE DAMPING FILTER:
     Torsional elasticity of the heavy commercial driveline induces low-frequency shuffle / jerk (3 to 6 Hz).
     A digital 2nd-order lead-lag bandpass filter extracts the oscillating torsional speed error:
       omega_err_driveline = (omega_prop / i_final_drive) - (v_veh / r_tire_dyn)
     Active anti-jerk counter-torque trim is superimposed on the J1939 engine torque request:
       T_anti_jerk = - K_aj * omega_err_filtered - D_aj * d(omega_err_filtered)/dt
     This suppresses vehicle longitudinal jerk strictly within |da/dt| < 1.5 m/s^3.

  7. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) FORMULATION:
     Sampling period Ts = 0.001 s (1.0 ms deterministic powertrain scan).
     Discrete 8x8 State-Space Dynamics:
       x[k+1] = A * x[k] + B * u[k]
       y[k]   = C * x[k] + D * u[k]
     State vector x (8 states):
       x[1]: Engine crankshaft angular velocity deviation Delta_omega_e [rad/s]
       x[2]: Transmission Input Shaft 1 speed deviation Delta_omega_in1 [rad/s]
       x[3]: Transmission Input Shaft 2 speed deviation Delta_omega_in2 [rad/s]
       x[4]: Propeller shaft angular velocity deviation Delta_omega_prop [rad/s]
       x[5]: Drive axle half-shaft elastic torsional windup Delta_theta_hs [rad]
       x[6]: Vehicle longitudinal chassis velocity deviation Delta_v_veh [m/s]
       x[7]: Clutch 1 hydraulic chamber pressure deviation Delta_P_cl1 [bar]
       x[8]: Clutch 2 hydraulic chamber pressure deviation Delta_P_cl2 [bar]
     Control input vector u (4 inputs):
       u[1]: Clutch 1 proportional pressure valve current command Delta_i_sol1 [bar]
       u[2]: Clutch 2 proportional pressure valve current command Delta_i_sol2 [bar]
       u[3]: Engine J1939 electronic torque demand request Delta_T_eng [Nm]
       u[4]: Shift rail pneumatic/hydraulic directional valve displacement Delta_x_rail [mm]
     MPC quadratic cost functional J:
       J = sum_{i=1}^{Np} [ (x[k+i] - r[k+i])^T * Q * (x[k+i] - r[k+i]) + u[k+i]^T * R * u[k+i]
           + Delta_u[k+i]^T * S * Delta_u[k+i] ] + (x[k+Np] - r[k+Np])^T * P * (x[k+Np] - r[k+Np])
     4-iteration Projected Gradient Descent (PGD) minimizes J subject to actuator rate and amplitude bounds.

  8. SYNCHRONIZER SLEEVE SPEED MATCHING:
     Dog clutch sleeve engagement permissive window requires shaft speed differential:
       |omega_target - omega_in_shaft| < 15.0 RPM
     Pneumatic shift rail force profile modulates engagement through neutral, synchronization cone contact,
     unbalking, and positive dog teeth lockup, monitored by linear position LVDT/Hall sensors.
========================================================================================================================
*)"""
    parts.append(header)

    # =========================================================================
    # 2. VAR_INPUT
    # =========================================================================
    var_input = """VAR_INPUT
    (* ========================================================================================= *)
    (* 1. SYSTEM SUPERVISORY COMMANDS, PERMISSIVES & DRIVER DEMANDS                              *)
    (* ========================================================================================= *)
    bMasterEnable                   : BOOL := FALSE;    (* Master transmission control unit system enable permissive *)
    bEStopChainOK_NC                : BOOL := TRUE;     (* Dual-channel hardware E-Stop chain healthy [active HIGH] *)
    bDriverShiftRequest             : BOOL := FALSE;    (* Driver gear shift lever request trigger pulse *)
    nDriverTargetGear               : INT := 1;         (* Driver commanded target gear index [-1=Rev, 0=N, 1..12=Gears] *)
    rDriverThrottlePedal_Pct        : REAL := 0.0;      (* Electronic throttle pedal demand percentage [0.0..100.0 %] *)
    rDriverBrakePedal_Pct           : REAL := 0.0;      (* Service brake pedal application percentage [0.0..100.0 %] *)
    bEngineRetarderEnable           : BOOL := FALSE;    (* Engine compression / hydraulic retarder brake enable *)
    rEngineRetarderDemand_Pct       : REAL := 0.0;      (* Retarder braking torque demand level [0.0..100.0 %] *)
    bTrailerConnected               : BOOL := TRUE;     (* Semi-trailer CAN hitch connection status confirmed *)
    rGrossVehicleWeightManual_kg    : REAL := 44000.0;  (* Manual fallback gross vehicle weight (GVW) setting [kg] *)
    rAmbientAirTemp_degC            : REAL := 22.5;     (* Ambient atmospheric air temperature [deg C] *)
    bTransmissionPTO_Active         : BOOL := FALSE;    (* Power Take-Off (PTO) auxiliary hydraulic pump active *)
    bServiceBrakeApplied            : BOOL := FALSE;    (* Pneumatic service brake pressure switch active contact *)
    bParkingBrakeReleased           : BOOL := TRUE;     (* Spring brake pneumatic park chamber released confirm *)

    (* ========================================================================================= *)
    (* 2. TRIPLE MODULAR REDUNDANT (2oo3 TMR) P&ID PROCESS TRANSMITTERS                          *)
    (* ========================================================================================= *)
    (* PT_CLUTCH1_PRESSURE_101: Dual Wet Clutch 1 Proportional Hydraulic Clamping Pressure [bar] *)
    PT_CLUTCH1_PRESSURE_101A        : REAL := 0.0;      (* Wet Clutch 1 hydraulic pressure transducer Channel A [bar] *)
    PT_CLUTCH1_PRESSURE_101B        : REAL := 0.0;      (* Wet Clutch 1 hydraulic pressure transducer Channel B [bar] *)
    PT_CLUTCH1_PRESSURE_101C        : REAL := 0.0;      (* Wet Clutch 1 hydraulic pressure transducer Channel C [bar] *)

    (* PT_CLUTCH2_PRESSURE_102: Dual Wet Clutch 2 Proportional Hydraulic Clamping Pressure [bar] *)
    PT_CLUTCH2_PRESSURE_102A        : REAL := 0.0;      (* Wet Clutch 2 hydraulic pressure transducer Channel A [bar] *)
    PT_CLUTCH2_PRESSURE_102B        : REAL := 0.0;      (* Wet Clutch 2 hydraulic pressure transducer Channel B [bar] *)
    PT_CLUTCH2_PRESSURE_102C        : REAL := 0.0;      (* Wet Clutch 2 hydraulic pressure transducer Channel C [bar] *)

    (* PT_MAIN_LINE_HYDR_103: Transmission Hydraulic Main Line Supply Manifold Pressure [bar] *)
    PT_MAIN_LINE_HYDR_103A          : REAL := 24.5;     (* Main line electro-hydraulic supply pressure Channel A [bar] *)
    PT_MAIN_LINE_HYDR_103B          : REAL := 24.6;     (* Main line electro-hydraulic supply pressure Channel B [bar] *)
    PT_MAIN_LINE_HYDR_103C          : REAL := 24.4;     (* Main line electro-hydraulic supply pressure Channel C [bar] *)

    (* ST_ENGINE_CRANKSHAFT_201: Heavy Duty Diesel Engine Crankshaft / Flywheel Speed [rpm] *)
    ST_ENGINE_CRANKSHAFT_201A       : REAL := 650.0;    (* Engine flywheel magnetic variable-reluctance sensor A [rpm] *)
    ST_ENGINE_CRANKSHAFT_201B       : REAL := 650.5;    (* Engine flywheel magnetic variable-reluctance sensor B [rpm] *)
    ST_ENGINE_CRANKSHAFT_201C       : REAL := 649.5;    (* Engine flywheel magnetic variable-reluctance sensor C [rpm] *)

    (* ST_INPUT_SHAFT1_202: Transmission Odd Gears (1,3,5,7,9,11) Primary Input Shaft Speed [rpm] *)
    ST_INPUT_SHAFT1_202A            : REAL := 0.0;      (* Odd input shaft Hall-effect speed pulse sensor A [rpm] *)
    ST_INPUT_SHAFT1_202B            : REAL := 0.0;      (* Odd input shaft Hall-effect speed pulse sensor B [rpm] *)
    ST_INPUT_SHAFT1_202C            : REAL := 0.0;      (* Odd input shaft Hall-effect speed pulse sensor C [rpm] *)

    (* ST_INPUT_SHAFT2_203: Transmission Even Gears (2,4,6,8,10,12) Secondary Input Shaft Speed [rpm] *)
    ST_INPUT_SHAFT2_203A            : REAL := 0.0;      (* Even input shaft Hall-effect speed pulse sensor A [rpm] *)
    ST_INPUT_SHAFT2_203B            : REAL := 0.0;      (* Even input shaft Hall-effect speed pulse sensor B [rpm] *)
    ST_INPUT_SHAFT2_203C            : REAL := 0.0;      (* Even input shaft Hall-effect speed pulse sensor C [rpm] *)

    (* ST_OUTPUT_PROP_SHAFT_204: Transmission Output / Drive Propeller Shaft Rotational Speed [rpm] *)
    ST_OUTPUT_PROP_SHAFT_204A       : REAL := 0.0;      (* Transmission output flange tone wheel pickup A [rpm] *)
    ST_OUTPUT_PROP_SHAFT_204B       : REAL := 0.0;      (* Transmission output flange tone wheel pickup B [rpm] *)
    ST_OUTPUT_PROP_SHAFT_204C       : REAL := 0.0;      (* Transmission output flange tone wheel pickup C [rpm] *)

    (* ZT_SHIFT_RAIL_POS_301: Pneumatic/Hydraulic Shift Rail Synchronizer Sleeve Position [mm] *)
    ZT_SHIFT_RAIL_POS_301A          : REAL := 0.0;      (* Shift rail linear inductive LVDT / Hall position sensor A [mm] *)
    ZT_SHIFT_RAIL_POS_301B          : REAL := 0.0;      (* Shift rail linear inductive LVDT / Hall position sensor B [mm] *)
    ZT_SHIFT_RAIL_POS_301C          : REAL := 0.0;      (* Shift rail linear inductive LVDT / Hall position sensor C [mm] *)

    (* TT_TRANSMISSION_OIL_401: Transmission Sump Lubrication & Hydraulic Oil Temperature [deg C] *)
    TT_TRANSMISSION_OIL_401A        : REAL := 68.5;     (* Transmission oil pan PT100 RTD temperature probe A [deg C] *)
    TT_TRANSMISSION_OIL_401B        : REAL := 68.6;     (* Transmission oil pan PT100 RTD temperature probe B [deg C] *)
    TT_TRANSMISSION_OIL_401C        : REAL := 68.4;     (* Transmission oil pan PT100 RTD temperature probe C [deg C] *)

    (* TT_CLUTCH_FRICTION_PLATE_402: Dual Wet Clutch Multi-Plate Pack Interface Temperature [deg C] *)
    TT_CLUTCH_FRICTION_PLATE_402A   : REAL := 82.0;     (* Embedded multi-plate friction interface sensor A [deg C] *)
    TT_CLUTCH_FRICTION_PLATE_402B   : REAL := 82.3;     (* Embedded multi-plate friction interface sensor B [deg C] *)
    TT_CLUTCH_FRICTION_PLATE_402C   : REAL := 81.8;     (* Embedded multi-plate friction interface sensor C [deg C] *)

    (* AT_CHASSIS_INCLINOMETER_501: Commercial Truck Chassis Longitudinal Road Grade Inclinometer [%] *)
    AT_CHASSIS_INCLINOMETER_501A    : REAL := 0.0;      (* MEMS dual-axis chassis pitch inclinometer Channel A [%] *)
    AT_CHASSIS_INCLINOMETER_501B    : REAL := 0.0;      (* MEMS dual-axis chassis pitch inclinometer Channel B [%] *)
    AT_CHASSIS_INCLINOMETER_501C    : REAL := 0.0;      (* MEMS dual-axis chassis pitch inclinometer Channel C [%] *)
END_VAR"""
    parts.append(var_input)

    # =========================================================================
    # 3. VAR_OUTPUT
    # =========================================================================
    var_output = """VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. MECHATRONIC ACTUATOR COMMANDS & CAN J1939 POWERTRAIN CONTROL SIGNALS                   *)
    (* ========================================================================================= *)
    rClutch1_PropPressureCmd_bar    : REAL := 0.0;      (* Wet Clutch 1 proportional pressure valve setpoint [bar] *)
    rClutch2_PropPressureCmd_bar    : REAL := 0.0;      (* Wet Clutch 2 proportional pressure valve setpoint [bar] *)
    rEngineTorqueRequest_Nm         : REAL := 0.0;      (* Electronic Diesel Engine J1939 EEC1 torque demand [Nm] *)
    rEngineSpeedLimit_RPM           : REAL := 2200.0;   (* Dynamic electronic engine speed limitation setpoint [rpm] *)
    rShiftRail_PneumaticForceCmd_N  : REAL := 0.0;      (* Shift rail proportional pneumatic cylinder force [N] *)
    rRetarderBrakeTorqueCmd_Nm      : REAL := 0.0;      (* Hydraulic / engine compression retarder torque command [Nm] *)
    bClutch1_FastFillPulse          : BOOL := FALSE;    (* Clutch 1 electro-hydraulic rapid pre-fill ballistic pulse *)
    bClutch2_FastFillPulse          : BOOL := FALSE;    (* Clutch 2 electro-hydraulic rapid pre-fill ballistic pulse *)
    bShiftRail_LockPawlEngaged      : BOOL := FALSE;    (* Synchronizer rail mechanical detent locking pawl solenoid *)
    bEmergencyNeutralValveCmd       : BOOL := FALSE;    (* Fast-acting emergency neutral hydraulic dump solenoid *)

    (* ========================================================================================= *)
    (* 2. CONSOLIDATED TRIPLE MODULAR REDUNDANCY (2oo3 TMR) VOTED TELEMETRY                     *)
    (* ========================================================================================= *)
    rVotedClutch1Pressure_bar       : REAL := 0.0;      (* 2oo3 TMR voted Clutch 1 hydraulic clamping pressure [bar] *)
    rVotedClutch2Pressure_bar       : REAL := 0.0;      (* 2oo3 TMR voted Clutch 2 hydraulic clamping pressure [bar] *)
    rVotedMainLineHydr_bar          : REAL := 0.0;      (* 2oo3 TMR voted main hydraulic supply line pressure [bar] *)
    rVotedEngineSpeed_RPM           : REAL := 0.0;      (* 2oo3 TMR voted engine crankshaft flywheel speed [rpm] *)
    rVotedInputShaft1Speed_RPM      : REAL := 0.0;      (* 2oo3 TMR voted odd input shaft rotational speed [rpm] *)
    rVotedInputShaft2Speed_RPM      : REAL := 0.0;      (* 2oo3 TMR voted even input shaft rotational speed [rpm] *)
    rVotedPropShaftSpeed_RPM        : REAL := 0.0;      (* 2oo3 TMR voted transmission output propeller speed [rpm] *)
    rVotedShiftRailPos_mm           : REAL := 0.0;      (* 2oo3 TMR voted synchronizer shift rail linear position [mm] *)
    rVotedTransOilTemp_degC         : REAL := 0.0;      (* 2oo3 TMR voted transmission oil pan temperature [deg C] *)
    rVotedClutchPlateTemp_degC      : REAL := 0.0;      (* 2oo3 TMR voted wet clutch multi-plate temperature [deg C] *)
    rVotedRoadGrade_Pct             : REAL := 0.0;      (* 2oo3 TMR voted chassis inclinometer longitudinal grade [%] *)

    (* ========================================================================================= *)
    (* 3. CYBER-PHYSICAL STATE OBSERVERS, METROLOGY & POWERTRAIN ESTIMATES                       *)
    (* ========================================================================================= *)
    rObservedClutch1Torque_Nm       : REAL := 0.0;      (* State-space observed Clutch 1 transmitted torque [Nm] *)
    rObservedClutch2Torque_Nm       : REAL := 0.0;      (* State-space observed Clutch 2 transmitted torque [Nm] *)
    rDrivelineTorsionalTorque_Nm    : REAL := 0.0;      (* Observed drive axle half-shaft elastic torsional torque [Nm] *)
    rVehicleLongitudinalAcc_mps2    : REAL := 0.0;      (* Estimated vehicle longitudinal chassis acceleration [m/s2] *)
    rLongitudinalJerk_mps3          : REAL := 0.0;      (* Time derivative of acceleration da/dt (Jerk) [m/s3] *)
    rEstimatedGVW_Tons              : REAL := 44.0;     (* Adaptive recursive Gross Vehicle Weight estimate [t] *)
    rClutch1ThermalEnergy_kJ        : REAL := 0.0;      (* Integrated thermal energy dissipation on Clutch 1 [kJ] *)
    rClutch2ThermalEnergy_kJ        : REAL := 0.0;      (* Integrated thermal energy dissipation on Clutch 2 [kJ] *)
    rAntiJerkDampingTorque_Nm       : REAL := 0.0;      (* Dynamic active anti-jerk counter-torque compensation [Nm] *)
    nActiveGear                     : INT := 0;         (* Currently engaged active power transmission gear [0..12] *)
    nPreSelectedGear                : INT := 0;         (* Standby shaft synchronizer pre-selected target gear [0..12] *)
    rMPC_QuadraticCost              : REAL := 0.0;      (* Receding-horizon MPC objective cost function value J *)

    (* ========================================================================================= *)
    (* 4. ISA-18.2 ALARM WORDS, SEQUENTIAL FSM & SAFETY STATUS REGISTERS                         *)
    (* ========================================================================================= *)
    wFSM_CurrentState               : WORD := 16#0000;  (* 12-stage automated transmission FSM state index *)
    dwDiagnosticWord01_FSM          : DWORD := 16#0000; (* Transmission mechatronics operational diagnostic bitfield *)
    dwDiagnosticWord02_TMR          : DWORD := 16#0000; (* 2oo3 TMR sensor channel degradation and isolation status *)
    dwAlarmWord_Priority1_Trip      : DWORD := 16#0000; (* ISA-18.2 Priority 1 Emergency Trip & E-Stop bitfield *)
    dwAlarmWord_Priority2_Severe    : DWORD := 16#0000; (* ISA-18.2 Priority 2 Process Abort & Clutch Disengage *)
    dwAlarmWord_Priority3_Warning   : DWORD := 16#0000; (* ISA-18.2 Priority 3 Pre-Trip & Advisory Warning bitfield *)
    bTransmissionReady              : BOOL := FALSE;    (* Transmission MCU fully booted, calibrated and ready *)
    bShiftInProgress                : BOOL := FALSE;    (* Gear handover crossfade or inertia phase actively running *)
    bClutchOverheatWarning          : BOOL := FALSE;    (* Wet clutch friction plate thermal overload warning flag *)
    bShiftRailJamFault              : BOOL := FALSE;    (* Synchronizer sleeve mechanical motion jam detected *)
END_VAR"""
    parts.append(var_output)

    # =========================================================================
    # 4. VAR_INTERNAL
    # =========================================================================
    var_internal = """VAR
    (* ========================================================================================= *)
    (* 1. DRIVELINE MECHANICAL, KINEMATIC & GEOMETRIC CONSTANTS                                  *)
    (* ========================================================================================= *)
    rConst_SampleTimeTs             : REAL := 0.001000; (* Powertrain deterministic discrete scan Ts = 1.0 ms [s] *)
    rConst_Pi                       : REAL := 3.141592653589793; (* Pi mathematical constant *)
    rConst_Gravity                  : REAL := 9.80665;  (* Gravitational acceleration g [m/s2] *)
    rConst_AirDensity               : REAL := 1.225;    (* Standard sea-level dry air density rho [kg/m3] *)
    rConst_TruckFrontalArea         : REAL := 9.50;     (* Commercial truck aerodynamic frontal area A [m2] *)
    rConst_TruckDragCoeff           : REAL := 0.620;    (* Aerodynamic drag coefficient Cd [-] *)
    rConst_RollingResistCoeff       : REAL := 0.00550;  (* Heavy truck low rolling resistance tire coefficient Crr *)
    rConst_TireRadiusDyn            : REAL := 0.518;    (* Drive axle loaded dynamic rolling radius r_tire [m] *)
    rConst_FinalDriveAxleRatio      : REAL := 3.420;    (* Tandem drive axle differential hypoid gear reduction ratio *)
    rConst_EngineFlywheelInertia    : REAL := 2.850;    (* Heavy diesel engine crankshaft & flywheel inertia Je [kg*m2] *)
    rConst_TransInputInertia        : REAL := 0.420;    (* Transmission input shaft & clutch pack inertia Jt [kg*m2] *)
    rConst_HalfShaftStiffness       : REAL := 145000.0; (* Drive axle half-shaft torsional stiffness k_hs [Nm/rad] *)
    rConst_HalfShaftDamping         : REAL := 1250.0;   (* Drive axle half-shaft torsional damping c_hs [Nms/rad] *)
    rConst_EmptyTruckMass           : REAL := 14000.0;  (* Unladen commercial truck chassis tare mass [kg] *)
    rConst_MaxGrossTruckMass        : REAL := 44000.0;  (* Maximum legal 44-ton gross combination weight [kg] *)

    (* 12-Speed Automated Manual Transmission Gear Ratios *)
    arrGearRatios                   : ARRAY[1..12] OF REAL := [
        14.940, (* Gear 1  (Odd  - Clutch 1) - Low crawler range *)
        11.670, (* Gear 2  (Even - Clutch 2) - Crawler range *)
         9.120, (* Gear 3  (Odd  - Clutch 1) - Low haulage *)
         7.120, (* Gear 4  (Even - Clutch 2) - Low haulage *)
         5.560, (* Gear 5  (Odd  - Clutch 1) - Mid haulage *)
         4.350, (* Gear 6  (Even - Clutch 2) - Mid haulage *)
         3.430, (* Gear 7  (Odd  - Clutch 1) - Direct range low *)
         2.680, (* Gear 8  (Even - Clutch 2) - Direct range *)
         2.090, (* Gear 9  (Odd  - Clutch 1) - High range low *)
         1.630, (* Gear 10 (Even - Clutch 2) - High range *)
         1.280, (* Gear 11 (Odd  - Clutch 1) - High cruise *)
         1.000  (* Gear 12 (Even - Clutch 2) - Direct drive overdrive *)
    ];
    rGearRatioReverse               : REAL := -14.220;  (* Reverse gear ratio (Odd - Clutch 1) *)

    (* ========================================================================================= *)
    (* 2. WET MULTI-PLATE CLUTCH STRIBECK FRICTION & HYDRAULIC VALVE PARAMETERS                  *)
    (* ========================================================================================= *)
    rConst_ClutchPistonArea         : REAL := 0.02450;  (* Hydraulic application piston effective area [m2] *)
    rConst_ClutchReturnSpringP      : REAL := 1.850;    (* Disengagement diaphragm return spring pressure [bar] *)
    rConst_ClutchMeanRadius         : REAL := 0.1180;   (* Effective mean friction radius r_mean [m] *)
    nConst_ClutchFrictionFaces      : INT := 10;        (* Number of active carbon-paper friction interfaces *)
    rConst_StribeckMuStatic         : REAL := 0.1450;   (* Static boundary friction coefficient mu_s [-] *)
    rConst_StribeckMuCoulomb        : REAL := 0.1120;   (* Dynamic sliding Coulomb friction coefficient mu_c [-] *)
    rConst_StribeckVelocityWs       : REAL := 12.50;    (* Stribeck transition angular slip speed omega_s [rad/s] *)
    rConst_StribeckExponentDelta    : REAL := 1.250;    (* Empirical Stribeck transition exponent delta [-] *)
    rConst_StribeckViscousCoeff     : REAL := 0.000850; (* Fluid-film viscous shear damping coefficient sigma_v [s/rad] *)
    rConst_SolenoidHydrTau          : REAL := 0.004000; (* Proportional electro-hydraulic solenoid time constant [s] *)
    rConst_ClutchPlatePackMass      : REAL := 14.50;    (* Effective steel reaction plate pack thermal mass [kg] *)
    rConst_SteelSpecificHeat        : REAL := 480.0;    (* Specific heat capacity of steel plates c_p [J/(kg*K)] *)
    rConst_ConvectiveCoolingHA      : REAL := 85.0;     (* Convective forced-oil cooling heat transfer coeff h*A [W/K] *)

    (* ========================================================================================= *)
    (* 3. 8x8 DISCRETE STATE-SPACE MATRICES & VECTORS (x[k+1] = A*x[k] + B*u[k])                *)
    (* ========================================================================================= *)
    arrA                            : ARRAY[1..8, 1..8] OF REAL; (* Discrete state transition matrix A (8x8) *)
    arrB                            : ARRAY[1..8, 1..4] OF REAL; (* Discrete input coupling matrix B (8x4) *)
    arrC                            : ARRAY[1..8, 1..8] OF REAL; (* Measurement output matrix C (8x8) *)
    arrD                            : ARRAY[1..8, 1..4] OF REAL; (* Direct feedthrough matrix D (8x4) *)
    arrState_x                      : ARRAY[1..8] OF REAL;       (* Current state vector x[k] *)
    arrState_x_next                 : ARRAY[1..8] OF REAL;       (* Predicted state vector x[k+1] *)
    arrState_x_hat                  : ARRAY[1..8] OF REAL;       (* Estimated / filtered state vector x_hat[k] *)
    arrStateReference               : ARRAY[1..8] OF REAL;       (* Equilibrium reference trajectory vector x_ref *)
    arrControl_u                    : ARRAY[1..4] OF REAL;       (* Active control input command vector u[k] *)
    arrControl_u_prev               : ARRAY[1..4] OF REAL;       (* Previous control input command vector u[k-1] *)
    arrControl_u_delta              : ARRAY[1..4] OF REAL;       (* Actuator slew rate vector Delta_u[k] *)
    arrOutput_y                     : ARRAY[1..8] OF REAL;       (* Computed system output vector y[k] *)

    (* ========================================================================================= *)
    (* 4. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) MATRICES & TUNING                       *)
    (* ========================================================================================= *)
    arrQ_Cost                       : ARRAY[1..8] OF REAL;       (* State deviation penalty diagonal weights *)
    arrR_Cost                       : ARRAY[1..4] OF REAL;       (* Actuator effort penalty diagonal weights *)
    arrS_Cost                       : ARRAY[1..4] OF REAL;       (* Actuator slew rate penalty diagonal weights *)
    arrP_TerminalCost               : ARRAY[1..8] OF REAL;       (* Terminal state error penalty diagonal weights *)
    arrMpcGradient                  : ARRAY[1..4] OF REAL;       (* Analytical objective gradient nabla_J *)
    arrU_Min                        : ARRAY[1..4] OF REAL;       (* Hard lower actuator constraints *)
    arrU_Max                        : ARRAY[1..4] OF REAL;       (* Hard upper actuator constraints *)
    arrDeltaU_Max                   : ARRAY[1..4] OF REAL;       (* Maximum allowable slew per 1.0 ms scan *)
    rMpcStepAlpha                   : REAL := 0.000350;          (* Projected gradient descent learning rate *)
    nMpcIterations                  : INT := 4;                  (* Gradient solver inner iterations per cycle *)
    rMpcObjectiveValue              : REAL := 0.0;               (* Current scalar quadratic MPC cost *)

    (* ========================================================================================= *)
    (* 5. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING CHANNELS & PERSISTENCE TIMERS              *)
    (* ========================================================================================= *)
    (* Discrepancy Tolerances *)
    rTol_ClutchPressure_bar         : REAL := 0.80;  (* Wet clutch hydraulic pressure discrepancy threshold [bar] *)
    rTol_MainLineHydr_bar           : REAL := 1.20;  (* Main hydraulic line discrepancy threshold [bar] *)
    rTol_ShaftSpeed_RPM             : REAL := 10.0;  (* Engine and input shaft speed discrepancy threshold [rpm] *)
    rTol_PropShaftSpeed_RPM         : REAL := 8.0;   (* Propeller shaft speed discrepancy threshold [rpm] *)
    rTol_ShiftRailPos_mm            : REAL := 0.350; (* Shift rail position sensor discrepancy threshold [mm] *)
    rTol_TransOilTemp_degC          : REAL := 2.50;  (* Transmission oil temperature discrepancy threshold [deg C] *)
    rTol_ClutchPlateTemp_degC       : REAL := 5.00;  (* Clutch plate interface temperature discrepancy [deg C] *)
    rTol_RoadGrade_Pct              : REAL := 0.40;  (* Chassis inclinometer grade discrepancy threshold [%] *)
    rTmrPersistenceTimeout_s        : REAL := 0.050; (* Fault persistence qualification timeout (50 ms) [s] *)

    (* Channel Isolation & Discrepancy Fault Timers *)
    tTMR_Clutch1Pres_Timer          : REAL := 0.0;   bTMR_Clutch1Pres_A_Iso : BOOL := FALSE; bTMR_Clutch1Pres_B_Iso : BOOL := FALSE; bTMR_Clutch1Pres_C_Iso : BOOL := FALSE;
    tTMR_Clutch2Pres_Timer          : REAL := 0.0;   bTMR_Clutch2Pres_A_Iso : BOOL := FALSE; bTMR_Clutch2Pres_B_Iso : BOOL := FALSE; bTMR_Clutch2Pres_C_Iso : BOOL := FALSE;
    tTMR_MainLineHydr_Timer         : REAL := 0.0;   bTMR_MainLineHydr_A_Iso: BOOL := FALSE; bTMR_MainLineHydr_B_Iso: BOOL := FALSE; bTMR_MainLineHydr_C_Iso: BOOL := FALSE;
    tTMR_EngineSpeed_Timer          : REAL := 0.0;   bTMR_EngineSpeed_A_Iso : BOOL := FALSE; bTMR_EngineSpeed_B_Iso : BOOL := FALSE; bTMR_EngineSpeed_C_Iso : BOOL := FALSE;
    tTMR_InputShaft1_Timer          : REAL := 0.0;   bTMR_InputShaft1_A_Iso : BOOL := FALSE; bTMR_InputShaft1_B_Iso : BOOL := FALSE; bTMR_InputShaft1_C_Iso : BOOL := FALSE;
    tTMR_InputShaft2_Timer          : REAL := 0.0;   bTMR_InputShaft2_A_Iso : BOOL := FALSE; bTMR_InputShaft2_B_Iso : BOOL := FALSE; bTMR_InputShaft2_C_Iso : BOOL := FALSE;
    tTMR_PropShaft_Timer            : REAL := 0.0;   bTMR_PropShaft_A_Iso   : BOOL := FALSE; bTMR_PropShaft_B_Iso   : BOOL := FALSE; bTMR_PropShaft_C_Iso   : BOOL := FALSE;
    tTMR_ShiftRail_Timer            : REAL := 0.0;   bTMR_ShiftRail_A_Iso   : BOOL := FALSE; bTMR_ShiftRail_B_Iso   : BOOL := FALSE; bTMR_ShiftRail_C_Iso   : BOOL := FALSE;
    tTMR_TransOilTemp_Timer         : REAL := 0.0;   bTMR_TransOilTemp_A_Iso: BOOL := FALSE; bTMR_TransOilTemp_B_Iso: BOOL := FALSE; bTMR_TransOilTemp_C_Iso: BOOL := FALSE;
    tTMR_ClutchPlateTemp_Timer      : REAL := 0.0;   bTMR_ClutchPlateTemp_A_Iso: BOOL := FALSE; bTMR_ClutchPlateTemp_B_Iso: BOOL := FALSE; bTMR_ClutchPlateTemp_C_Iso: BOOL := FALSE;
    tTMR_RoadGrade_Timer            : REAL := 0.0;   bTMR_RoadGrade_A_Iso   : BOOL := FALSE; bTMR_RoadGrade_B_Iso   : BOOL := FALSE; bTMR_RoadGrade_C_Iso   : BOOL := FALSE;

    (* ========================================================================================= *)
    (* 6. DRIVELINE ACTIVE ANTI-JERK & TORSIONAL DAMPING REGISTERS                               *)
    (* ========================================================================================= *)
    rAntiJerk_Kp                    : REAL := 18.50;    (* Driveline anti-jerk proportional gain [Nm/(rad/s)] *)
    rAntiJerk_Kd                    : REAL := 1.250;    (* Driveline anti-jerk rate damping gain [Nms/(rad/s)] *)
    rAntiJerk_FilterState1          : REAL := 0.0;      (* Bandpass filter state variable 1 *)
    rAntiJerk_FilterState2          : REAL := 0.0;      (* Bandpass filter state variable 2 *)
    rAntiJerk_PrevError             : REAL := 0.0;      (* Previous scan driveline speed differential error *)
    rAntiJerk_TorqueLimitNm         : REAL := 280.0;    (* Maximum anti-jerk counter-torque compensation limit [Nm] *)

    (* ========================================================================================= *)
    (* 7. WET CLUTCH THERMAL ENERGY DISSIPATION & BULK TEMPERATURE OBSERVER                      *)
    (* ========================================================================================= *)
    rClutch1_SlipSpeedRadS          : REAL := 0.0;      (* Instantaneous angular slip velocity on Clutch 1 [rad/s] *)
    rClutch2_SlipSpeedRadS          : REAL := 0.0;      (* Instantaneous angular slip velocity on Clutch 2 [rad/s] *)
    rClutch1_FricPowerWatts         : REAL := 0.0;      (* Heat power generation rate on Clutch 1 [W] *)
    rClutch2_FricPowerWatts         : REAL := 0.0;      (* Heat power generation rate on Clutch 2 [W] *)
    rClutch1_BulkTempObserved       : REAL := 80.0;     (* Lumped capacitance model observed plate temp 1 [deg C] *)
    rClutch2_BulkTempObserved       : REAL := 80.0;     (* Lumped capacitance model observed plate temp 2 [deg C] *)

    (* ========================================================================================= *)
    (* 8. SYNCHRONIZER SLEEVE SPEED MATCHING & SHIFT RAIL SERVO REGISTERS                        *)
    (* ========================================================================================= *)
    rSynchro_TargetShaftSpeed_RPM   : REAL := 0.0;      (* Target rotational speed for incoming gear shaft [rpm] *)
    rSynchro_SpeedDiff_RPM          : REAL := 0.0;      (* Absolute speed differential |target - actual| [rpm] *)
    rSynchro_SpeedMatchTolerance    : REAL := 15.0;     (* Hall-effect dog clutch speed matching threshold [rpm] *)
    rShiftRail_TargetPos_mm         : REAL := 0.0;      (* Target synchronizer sleeve linear position [mm] *)
    rShiftRail_PosError_mm          : REAL := 0.0;      (* Shift rail position tracking deviation [mm] *)
    tShiftRail_JamTimer             : REAL := 0.0;      (* Mechanical rail jam persistence timer [s] *)
    rConst_ShiftRailJamTimeout      : REAL := 0.080;    (* Jam trip qualification time (80 ms) [s] *)
    rConst_ShiftRailJamTol_mm       : REAL := 1.80;     (* Jam displacement error threshold [mm] *)

    (* ========================================================================================= *)
    (* 9. SEQUENTIAL FINITE STATE MACHINE (12 STATES) & TIMING REGISTERS                         *)
    (* ========================================================================================= *)
    nFSM_State                      : INT := 1;         (* Active operational FSM state index (1..12) *)
    nFSM_NextState                  : INT := 1;         (* Next scheduled transition FSM state index *)
    tStateDwellTimer                : REAL := 0.0;      (* Elapsed residence time in active state [s] *)
    bStateFirstScan                 : BOOL := TRUE;     (* First scan strobe for state entry actions *)
    tCrossFadeTimer                 : REAL := 0.0;      (* Clutch torque handover crossfade timer [s] *)
    rCrossFadeDuration_s            : REAL := 0.065;    (* Dynamic torque cross-fading duration (65 ms) [s] *)
    rCrossFadeAlpha                 : REAL := 0.0;      (* Normalized handover interpolator alpha [0.0..1.0] *)
    tInertiaPhaseTimer              : REAL := 0.0;      (* Inertia phase speed pull-down timer [s] *)
    tFastFillTimer1                 : REAL := 0.0;      (* Clutch 1 electro-hydraulic fast-fill pulse timer [s] *)
    tFastFillTimer2                 : REAL := 0.0;      (* Clutch 2 electro-hydraulic fast-fill pulse timer [s] *)
    rFastFillPulseDuration          : REAL := 0.025;    (* Fast-fill ballistic pulse duration (25 ms) [s] *)
    rFastFillPressure_bar           : REAL := 18.0;     (* Fast-fill ballistic peak hydraulic pressure [bar] *)
    rTouchPointPressure_bar         : REAL := 2.85;     (* Clutch kissing / touch-point preload pressure [bar] *)
    nShiftCycleCount                : DINT := 0;        (* Total lifetime gearshift cycles completed *)

    (* FSM State Numerical Enumeration Constants *)
    c_STATE_BOOT_CALIBRATION        : INT := 1;         (* State 1: Cold start sensor validation & calibration *)
    c_STATE_NEUTRAL_IDLE            : INT := 2;         (* State 2: Neutral idle with both clutches disengaged *)
    c_STATE_FIRST_PRE_SELECT        : INT := 3;         (* State 3: Standby shaft pre-selects 1st / target gear *)
    c_STATE_LAUNCH_CLUTCH_SLIP      : INT := 4;         (* State 4: Vehicle launch control modulated clutch slip *)
    c_STATE_TORQUE_CROSSFADE        : INT := 5;         (* State 5: Dual clutch torque handover cross-fading *)
    c_STATE_INERTIA_SYNC            : INT := 6;         (* State 6: Engine speed inertia synchronization phase *)
    c_STATE_LOCKUP_CRUISE           : INT := 7;         (* State 7: Locked-up steady-state cruise efficiency *)
    c_STATE_SKIP_SHIFT_DECEL        : INT := 8;         (* State 8: Multi-gear skip shift deceleration *)
    c_STATE_GRADE_RETARDER          : INT := 9;         (* State 9: Downhill grade & engine retarder coordination *)
    c_STATE_OVERHEAT_LIMP           : INT := 10;        (* State 10: Clutch thermal overload limp-home protection *)
    c_STATE_RAIL_FAULT_LOCK         : INT := 11;        (* State 11: Shift rail jam mechanical safe lock mode *)
    c_STATE_EMERGENCY_NEUTRAL       : INT := 12;        (* State 12: Emergency neutral high-speed hydraulic dump *)

    (* ========================================================================================= *)
    (* 10. ISA-18.2 MULTI-TIERED ALARM SETPOINTS, DEADBANDS & PERSISTENCE                        *)
    (* ========================================================================================= *)
    (* Wet Clutch Friction Plate Temperature Alarms [deg C] *)
    rAlarmClutchTemp_HH             : REAL := 220.0;    (* Critical thermal breakdown trip point [deg C] *)
    rAlarmClutchTemp_H              : REAL := 180.0;    (* Clutch thermal overload advisory warning [deg C] *)
    rAlarmClutchTemp_Deadband       : REAL := 8.00;     (* Clutch thermal hysteresis reset deadband [deg C] *)
    rAlarmClutchTemp_MaxROC         : REAL := 25.0;     (* Maximum allowable temperature rate-of-change [deg C/s] *)

    (* Main Hydraulic Line Pressure Alarms [bar] *)
    rAlarmMainHydr_LL               : REAL := 12.00;    (* Severe hydraulic supply pressure loss trip [bar] *)
    rAlarmMainHydr_L                : REAL := 18.00;    (* Low hydraulic pressure advisory warning [bar] *)
    rAlarmMainHydr_Deadband         : REAL := 1.50;     (* Hydraulic pressure reset deadband [bar] *)

    (* Clutch Pressure Deviation Tracking Alarms [bar] *)
    rAlarmClutchDev_HH              : REAL := 3.50;     (* Severe clutch pressure servo tracking error trip [bar] *)
    rAlarmClutchDev_H               : REAL := 1.80;     (* Clutch pressure tracking deviation warning [bar] *)

    (* Driveline Longitudinal Jerk Alarms [m/s3] *)
    rAlarmLongJerk_Max              : REAL := 1.50;     (* Commercial truck longitudinal jerk comfort limit [m/s3] *)

    (* Prior Cycle Variables for Rate-of-Change (ROC) Calculations *)
    rPrevClutchPlateTemp            : REAL := 80.0;
    rROC_ClutchPlateTemp            : REAL := 0.0;
    rPrevVehicleAcc                 : REAL := 0.0;
    rPrevVehicleSpeed               : REAL := 0.0;
    rPrevMainHydrPressure           : REAL := 24.5;
    rROC_MainHydrPressure           : REAL := 0.0;

    (* Alarm Latched Status Bits *)
    bAlarm_ClutchPlateTemp_HH       : BOOL := FALSE;
    bAlarm_ClutchPlateTemp_H        : BOOL := FALSE;
    bAlarm_ClutchPlateTemp_ROC      : BOOL := FALSE;
    bAlarm_MainHydr_LL              : BOOL := FALSE;
    bAlarm_MainHydr_L               : BOOL := FALSE;
    bAlarm_ClutchDev1_HH            : BOOL := FALSE;
    bAlarm_ClutchDev2_HH            : BOOL := FALSE;
    bAlarm_LongJerkExceeded         : BOOL := FALSE;
    bAlarm_TMR_Degraded             : BOOL := FALSE;

    (* Arithmetic & Matrix Index Counters *)
    bColdStartInitialized           : BOOL := FALSE;    (* Cold-start memory setup confirmation *)
    iIdx                            : INT := 1;         (* Matrix row loop index *)
    jIdx                            : INT := 1;         (* Matrix column loop index *)
    kIdx                            : INT := 1;         (* Input dimension loop index *)
    mIdx                            : INT := 1;         (* MPC gradient iteration index *)
    rTempSum                        : REAL := 0.0;      (* Matrix arithmetic accumulation register *)
    rDiffAB                         : REAL := 0.0;      (* 2oo3 TMR Channel A vs B discrepancy *)
    rDiffBC                         : REAL := 0.0;      (* 2oo3 TMR Channel B vs C discrepancy *)
    rDiffAC                         : REAL := 0.0;      (* 2oo3 TMR Channel A vs C discrepancy *)
    bMatchAB                        : BOOL := FALSE;
    bMatchBC                        : BOOL := FALSE;
    bMatchAC                        : BOOL := FALSE;
END_VAR"""
    parts.append(var_internal)

    # =========================================================================
    # 5. PHASE 0: COLD START INITIALIZATION
    # =========================================================================
    phase0 = """(* ===================================================================================================================
 * PHASE 0: COLD-START DISCRETE STATE-SPACE MATRICES & CONTROL PARAMETER INITIALIZATION
 * =================================================================================================================== *)
IF NOT bColdStartInitialized THEN
    (* 8x8 State-Space System Matrix A discretized at Ts = 0.001 s (1.0 ms)
       States: [Delta_omega_e, Delta_omega_in1, Delta_omega_in2, Delta_omega_prop, Delta_theta_hs, Delta_v_veh, Delta_P_cl1, Delta_P_cl2] *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 8 DO
            arrA[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* Row 1: Engine crankshaft speed dynamics (Je = 2.85 kg*m2) *)
    arrA[1, 1] := 0.9965; (* Flywheel aerodynamic & viscous drag damping *)
    arrA[1, 7] := -0.0142; (* Direct torque coupling from Clutch 1 pressure *)
    arrA[1, 8] := -0.0142; (* Direct torque coupling from Clutch 2 pressure *)

    (* Row 2: Transmission Input Shaft 1 dynamics (Odd gears) *)
    arrA[2, 2] := 0.9920; (* Bearing viscous drag damping *)
    arrA[2, 7] := 0.0850; (* Torque acceleration from Clutch 1 clamping *)

    (* Row 3: Transmission Input Shaft 2 dynamics (Even gears) *)
    arrA[3, 3] := 0.9920; (* Bearing viscous drag damping *)
    arrA[3, 8] := 0.0850; (* Torque acceleration from Clutch 2 clamping *)

    (* Row 4: Propeller shaft output dynamics *)
    arrA[4, 4] := 0.9880; (* Driveline bearing drag *)
    arrA[4, 5] := -0.0450; (* Counter-torque from half-shaft windup *)

    (* Row 5: Drive axle half-shaft torsional windup kinematics: d(theta_hs)/dt = omega_prop/i_axle - v_veh/r_tire *)
    arrA[5, 4] := 0.000292; (* 0.001 s / i_axle (3.42) *)
    arrA[5, 5] := 0.9990;   (* Viscoelastic relaxation decay *)
    arrA[5, 6] := -0.001930; (* -0.001 s / r_tire (0.518 m) *)

    (* Row 6: Vehicle longitudinal chassis velocity dynamics (M_veh = 44,000 kg) *)
    arrA[6, 5] := 0.00636;  (* Half-shaft tractive force acceleration *)
    arrA[6, 6] := 0.9985;   (* Aerodynamic & rolling resistance decay *)

    (* Row 7: Clutch 1 proportional electro-hydraulic valve pressure dynamics (tau = 4.0 ms) *)
    arrA[7, 7] := 0.7788;   (* exp(-Ts / tau) = exp(-0.001 / 0.004) = 0.7788 *)

    (* Row 8: Clutch 2 proportional electro-hydraulic valve pressure dynamics (tau = 4.0 ms) *)
    arrA[8, 8] := 0.7788;   (* exp(-Ts / tau) = exp(-0.001 / 0.004) = 0.7788 *)

    (* 8x4 Discrete Input Coupling Matrix B
       Inputs: [u1: Delta_P_cl1_cmd, u2: Delta_P_cl2_cmd, u3: Delta_T_eng_demand, u4: Delta_x_rail] *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 4 DO
            arrB[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    arrB[1, 3] := 0.000351; (* Engine torque input to crankshaft: Ts / Je = 0.001 / 2.85 = 0.000351 *)
    arrB[7, 1] := 0.2212;   (* 1.0 - exp(-Ts / tau) = 1.0 - 0.7788 = 0.2212 *)
    arrB[8, 2] := 0.2212;   (* 1.0 - exp(-Ts / tau) = 1.0 - 0.7788 = 0.2212 *)
    arrB[4, 4] := 0.00185;  (* Synchronizer dog engagement force coupling *)

    (* 8x8 Output Measurement Matrix C (Identity state observation) *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 8 DO
            IF iIdx = jIdx THEN
                arrC[iIdx, jIdx] := 1.0;
            ELSE
                arrC[iIdx, jIdx] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* 8x4 Direct Feedthrough Matrix D *)
    FOR iIdx := 1 TO 8 DO
        FOR jIdx := 1 TO 4 DO
            arrD[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* Receding-Horizon MPC Quadratic Cost Diagonal Weights *)
    arrQ_Cost[1] := 2.50;  (* Engine speed deviation penalty *)
    arrQ_Cost[2] := 4.80;  (* Input shaft 1 speed tracking penalty *)
    arrQ_Cost[3] := 4.80;  (* Input shaft 2 speed tracking penalty *)
    arrQ_Cost[4] := 3.20;  (* Propeller shaft speed tracking penalty *)
    arrQ_Cost[5] := 18.50; (* Torsional half-shaft windup penalty (suppresses driveline jerk) *)
    arrQ_Cost[6] := 12.00; (* Vehicle speed tracking error penalty *)
    arrQ_Cost[7] := 1.50;  (* Clutch 1 pressure deviation penalty *)
    arrQ_Cost[8] := 1.50;  (* Clutch 2 pressure deviation penalty *)

    arrR_Cost[1] := 0.085; (* Clutch 1 hydraulic pressure command effort penalty *)
    arrR_Cost[2] := 0.085; (* Clutch 2 hydraulic pressure command effort penalty *)
    arrR_Cost[3] := 0.012; (* Engine torque modulation effort penalty *)
    arrR_Cost[4] := 0.250; (* Shift rail actuator force effort penalty *)

    arrS_Cost[1] := 0.450; (* Clutch 1 pressure slew rate penalty (ensures smooth handover) *)
    arrS_Cost[2] := 0.450; (* Clutch 2 pressure slew rate penalty (ensures smooth handover) *)
    arrS_Cost[3] := 0.050; (* Engine torque slew rate penalty (prevents turbo surge) *)
    arrS_Cost[4] := 0.850; (* Shift rail velocity slew rate penalty (prevents dog clash) *)

    FOR iIdx := 1 TO 8 DO
        arrP_TerminalCost[iIdx] := arrQ_Cost[iIdx] * 2.80;
    END_FOR;

    (* Actuator Hard Physical Saturation Limits *)
    arrU_Min[1] := 0.0;    arrU_Max[1] := 22.0;   (* Clutch 1 pressure command [0.0..22.0 bar] *)
    arrU_Min[2] := 0.0;    arrU_Max[2] := 22.0;   (* Clutch 2 pressure command [0.0..22.0 bar] *)
    arrU_Min[3] := -400.0; arrU_Max[3] := 2800.0; (* Engine net torque request [-400..2800 Nm] *)
    arrU_Min[4] := -15.0;  arrU_Max[4] := 15.0;   (* Shift rail position setpoint [-15..+15 mm] *)

    arrDeltaU_Max[1] := 0.85; (* Max Clutch 1 pressure slew per 1.0 ms scan [bar] *)
    arrDeltaU_Max[2] := 0.85; (* Max Clutch 2 pressure slew per 1.0 ms scan [bar] *)
    arrDeltaU_Max[3] := 45.0; (* Max Engine torque slew per 1.0 ms scan [Nm] *)
    arrDeltaU_Max[4] := 0.60; (* Max Shift rail slew per 1.0 ms scan [mm] *)

    bColdStartInitialized := TRUE;
END_IF;"""
    parts.append(phase0)

    # =========================================================================
    # 6. PHASE 1: 2oo3 TMR SENSOR VOTING
    # =========================================================================
    phase1 = """(* ===================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES
 * =================================================================================================================== *)

(* 1.1 PT_CLUTCH1_PRESSURE_101: Dual Wet Clutch 1 Hydraulic Clamping Pressure [bar] *)
rDiffAB := ABS(PT_CLUTCH1_PRESSURE_101A - PT_CLUTCH1_PRESSURE_101B);
rDiffBC := ABS(PT_CLUTCH1_PRESSURE_101B - PT_CLUTCH1_PRESSURE_101C);
rDiffAC := ABS(PT_CLUTCH1_PRESSURE_101A - PT_CLUTCH1_PRESSURE_101C);
bMatchAB := (rDiffAB <= rTol_ClutchPressure_bar);
bMatchBC := (rDiffBC <= rTol_ClutchPressure_bar);
bMatchAC := (rDiffAC <= rTol_ClutchPressure_bar);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedClutch1Pressure_bar := (PT_CLUTCH1_PRESSURE_101A + PT_CLUTCH1_PRESSURE_101B + PT_CLUTCH1_PRESSURE_101C) / 3.0;
    bTMR_Clutch1Pres_A_Iso := FALSE; bTMR_Clutch1Pres_B_Iso := FALSE; bTMR_Clutch1Pres_C_Iso := FALSE;
    tTMR_Clutch1Pres_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedClutch1Pressure_bar := (PT_CLUTCH1_PRESSURE_101A + PT_CLUTCH1_PRESSURE_101B) / 2.0;
    bTMR_Clutch1Pres_A_Iso := FALSE; bTMR_Clutch1Pres_B_Iso := FALSE; bTMR_Clutch1Pres_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedClutch1Pressure_bar := (PT_CLUTCH1_PRESSURE_101B + PT_CLUTCH1_PRESSURE_101C) / 2.0;
    bTMR_Clutch1Pres_A_Iso := TRUE; bTMR_Clutch1Pres_B_Iso := FALSE; bTMR_Clutch1Pres_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedClutch1Pressure_bar := (PT_CLUTCH1_PRESSURE_101A + PT_CLUTCH1_PRESSURE_101C) / 2.0;
    bTMR_Clutch1Pres_A_Iso := FALSE; bTMR_Clutch1Pres_B_Iso := TRUE; bTMR_Clutch1Pres_C_Iso := FALSE;
ELSE
    tTMR_Clutch1Pres_Timer := tTMR_Clutch1Pres_Timer + rConst_SampleTimeTs;
    rVotedClutch1Pressure_bar := PT_CLUTCH1_PRESSURE_101B; (* Mid-range fallback *)
    IF tTMR_Clutch1Pres_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.2 PT_CLUTCH2_PRESSURE_102: Dual Wet Clutch 2 Hydraulic Clamping Pressure [bar] *)
rDiffAB := ABS(PT_CLUTCH2_PRESSURE_102A - PT_CLUTCH2_PRESSURE_102B);
rDiffBC := ABS(PT_CLUTCH2_PRESSURE_102B - PT_CLUTCH2_PRESSURE_102C);
rDiffAC := ABS(PT_CLUTCH2_PRESSURE_102A - PT_CLUTCH2_PRESSURE_102C);
bMatchAB := (rDiffAB <= rTol_ClutchPressure_bar);
bMatchBC := (rDiffBC <= rTol_ClutchPressure_bar);
bMatchAC := (rDiffAC <= rTol_ClutchPressure_bar);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedClutch2Pressure_bar := (PT_CLUTCH2_PRESSURE_102A + PT_CLUTCH2_PRESSURE_102B + PT_CLUTCH2_PRESSURE_102C) / 3.0;
    bTMR_Clutch2Pres_A_Iso := FALSE; bTMR_Clutch2Pres_B_Iso := FALSE; bTMR_Clutch2Pres_C_Iso := FALSE;
    tTMR_Clutch2Pres_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedClutch2Pressure_bar := (PT_CLUTCH2_PRESSURE_102A + PT_CLUTCH2_PRESSURE_102B) / 2.0;
    bTMR_Clutch2Pres_A_Iso := FALSE; bTMR_Clutch2Pres_B_Iso := FALSE; bTMR_Clutch2Pres_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedClutch2Pressure_bar := (PT_CLUTCH2_PRESSURE_102B + PT_CLUTCH2_PRESSURE_102C) / 2.0;
    bTMR_Clutch2Pres_A_Iso := TRUE; bTMR_Clutch2Pres_B_Iso := FALSE; bTMR_Clutch2Pres_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedClutch2Pressure_bar := (PT_CLUTCH2_PRESSURE_102A + PT_CLUTCH2_PRESSURE_102C) / 2.0;
    bTMR_Clutch2Pres_A_Iso := FALSE; bTMR_Clutch2Pres_B_Iso := TRUE; bTMR_Clutch2Pres_C_Iso := FALSE;
ELSE
    tTMR_Clutch2Pres_Timer := tTMR_Clutch2Pres_Timer + rConst_SampleTimeTs;
    rVotedClutch2Pressure_bar := PT_CLUTCH2_PRESSURE_102B;
    IF tTMR_Clutch2Pres_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.3 PT_MAIN_LINE_HYDR_103: Hydraulic Main Line Supply Pressure [bar] *)
rDiffAB := ABS(PT_MAIN_LINE_HYDR_103A - PT_MAIN_LINE_HYDR_103B);
rDiffBC := ABS(PT_MAIN_LINE_HYDR_103B - PT_MAIN_LINE_HYDR_103C);
rDiffAC := ABS(PT_MAIN_LINE_HYDR_103A - PT_MAIN_LINE_HYDR_103C);
bMatchAB := (rDiffAB <= rTol_MainLineHydr_bar);
bMatchBC := (rDiffBC <= rTol_MainLineHydr_bar);
bMatchAC := (rDiffAC <= rTol_MainLineHydr_bar);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedMainLineHydr_bar := (PT_MAIN_LINE_HYDR_103A + PT_MAIN_LINE_HYDR_103B + PT_MAIN_LINE_HYDR_103C) / 3.0;
    bTMR_MainLineHydr_A_Iso := FALSE; bTMR_MainLineHydr_B_Iso := FALSE; bTMR_MainLineHydr_C_Iso := FALSE;
    tTMR_MainLineHydr_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedMainLineHydr_bar := (PT_MAIN_LINE_HYDR_103A + PT_MAIN_LINE_HYDR_103B) / 2.0;
    bTMR_MainLineHydr_A_Iso := FALSE; bTMR_MainLineHydr_B_Iso := FALSE; bTMR_MainLineHydr_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedMainLineHydr_bar := (PT_MAIN_LINE_HYDR_103B + PT_MAIN_LINE_HYDR_103C) / 2.0;
    bTMR_MainLineHydr_A_Iso := TRUE; bTMR_MainLineHydr_B_Iso := FALSE; bTMR_MainLineHydr_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedMainLineHydr_bar := (PT_MAIN_LINE_HYDR_103A + PT_MAIN_LINE_HYDR_103C) / 2.0;
    bTMR_MainLineHydr_A_Iso := FALSE; bTMR_MainLineHydr_B_Iso := TRUE; bTMR_MainLineHydr_C_Iso := FALSE;
ELSE
    tTMR_MainLineHydr_Timer := tTMR_MainLineHydr_Timer + rConst_SampleTimeTs;
    rVotedMainLineHydr_bar := PT_MAIN_LINE_HYDR_103B;
    IF tTMR_MainLineHydr_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.4 ST_ENGINE_CRANKSHAFT_201: Engine Flywheel / Crankshaft Speed [rpm] *)
rDiffAB := ABS(ST_ENGINE_CRANKSHAFT_201A - ST_ENGINE_CRANKSHAFT_201B);
rDiffBC := ABS(ST_ENGINE_CRANKSHAFT_201B - ST_ENGINE_CRANKSHAFT_201C);
rDiffAC := ABS(ST_ENGINE_CRANKSHAFT_201A - ST_ENGINE_CRANKSHAFT_201C);
bMatchAB := (rDiffAB <= rTol_ShaftSpeed_RPM);
bMatchBC := (rDiffBC <= rTol_ShaftSpeed_RPM);
bMatchAC := (rDiffAC <= rTol_ShaftSpeed_RPM);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedEngineSpeed_RPM := (ST_ENGINE_CRANKSHAFT_201A + ST_ENGINE_CRANKSHAFT_201B + ST_ENGINE_CRANKSHAFT_201C) / 3.0;
    bTMR_EngineSpeed_A_Iso := FALSE; bTMR_EngineSpeed_B_Iso := FALSE; bTMR_EngineSpeed_C_Iso := FALSE;
    tTMR_EngineSpeed_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedEngineSpeed_RPM := (ST_ENGINE_CRANKSHAFT_201A + ST_ENGINE_CRANKSHAFT_201B) / 2.0;
    bTMR_EngineSpeed_A_Iso := FALSE; bTMR_EngineSpeed_B_Iso := FALSE; bTMR_EngineSpeed_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedEngineSpeed_RPM := (ST_ENGINE_CRANKSHAFT_201B + ST_ENGINE_CRANKSHAFT_201C) / 2.0;
    bTMR_EngineSpeed_A_Iso := TRUE; bTMR_EngineSpeed_B_Iso := FALSE; bTMR_EngineSpeed_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedEngineSpeed_RPM := (ST_ENGINE_CRANKSHAFT_201A + ST_ENGINE_CRANKSHAFT_201C) / 2.0;
    bTMR_EngineSpeed_A_Iso := FALSE; bTMR_EngineSpeed_B_Iso := TRUE; bTMR_EngineSpeed_C_Iso := FALSE;
ELSE
    tTMR_EngineSpeed_Timer := tTMR_EngineSpeed_Timer + rConst_SampleTimeTs;
    rVotedEngineSpeed_RPM := ST_ENGINE_CRANKSHAFT_201B;
    IF tTMR_EngineSpeed_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.5 ST_INPUT_SHAFT1_202: Transmission Odd Gears Input Shaft Speed [rpm] *)
rDiffAB := ABS(ST_INPUT_SHAFT1_202A - ST_INPUT_SHAFT1_202B);
rDiffBC := ABS(ST_INPUT_SHAFT1_202B - ST_INPUT_SHAFT1_202C);
rDiffAC := ABS(ST_INPUT_SHAFT1_202A - ST_INPUT_SHAFT1_202C);
bMatchAB := (rDiffAB <= rTol_ShaftSpeed_RPM);
bMatchBC := (rDiffBC <= rTol_ShaftSpeed_RPM);
bMatchAC := (rDiffAC <= rTol_ShaftSpeed_RPM);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedInputShaft1Speed_RPM := (ST_INPUT_SHAFT1_202A + ST_INPUT_SHAFT1_202B + ST_INPUT_SHAFT1_202C) / 3.0;
    bTMR_InputShaft1_A_Iso := FALSE; bTMR_InputShaft1_B_Iso := FALSE; bTMR_InputShaft1_C_Iso := FALSE;
    tTMR_InputShaft1_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedInputShaft1Speed_RPM := (ST_INPUT_SHAFT1_202A + ST_INPUT_SHAFT1_202B) / 2.0;
    bTMR_InputShaft1_A_Iso := FALSE; bTMR_InputShaft1_B_Iso := FALSE; bTMR_InputShaft1_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedInputShaft1Speed_RPM := (ST_INPUT_SHAFT1_202B + ST_INPUT_SHAFT1_202C) / 2.0;
    bTMR_InputShaft1_A_Iso := TRUE; bTMR_InputShaft1_B_Iso := FALSE; bTMR_InputShaft1_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedInputShaft1Speed_RPM := (ST_INPUT_SHAFT1_202A + ST_INPUT_SHAFT1_202C) / 2.0;
    bTMR_InputShaft1_A_Iso := FALSE; bTMR_InputShaft1_B_Iso := TRUE; bTMR_InputShaft1_C_Iso := FALSE;
ELSE
    tTMR_InputShaft1_Timer := tTMR_InputShaft1_Timer + rConst_SampleTimeTs;
    rVotedInputShaft1Speed_RPM := ST_INPUT_SHAFT1_202B;
    IF tTMR_InputShaft1_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.6 ST_INPUT_SHAFT2_203: Transmission Even Gears Input Shaft Speed [rpm] *)
rDiffAB := ABS(ST_INPUT_SHAFT2_203A - ST_INPUT_SHAFT2_203B);
rDiffBC := ABS(ST_INPUT_SHAFT2_203B - ST_INPUT_SHAFT2_203C);
rDiffAC := ABS(ST_INPUT_SHAFT2_203A - ST_INPUT_SHAFT2_203C);
bMatchAB := (rDiffAB <= rTol_ShaftSpeed_RPM);
bMatchBC := (rDiffBC <= rTol_ShaftSpeed_RPM);
bMatchAC := (rDiffAC <= rTol_ShaftSpeed_RPM);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedInputShaft2Speed_RPM := (ST_INPUT_SHAFT2_203A + ST_INPUT_SHAFT2_203B + ST_INPUT_SHAFT2_203C) / 3.0;
    bTMR_InputShaft2_A_Iso := FALSE; bTMR_InputShaft2_B_Iso := FALSE; bTMR_InputShaft2_C_Iso := FALSE;
    tTMR_InputShaft2_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedInputShaft2Speed_RPM := (ST_INPUT_SHAFT2_203A + ST_INPUT_SHAFT2_203B) / 2.0;
    bTMR_InputShaft2_A_Iso := FALSE; bTMR_InputShaft2_B_Iso := FALSE; bTMR_InputShaft2_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedInputShaft2Speed_RPM := (ST_INPUT_SHAFT2_203B + ST_INPUT_SHAFT2_203C) / 2.0;
    bTMR_InputShaft2_A_Iso := TRUE; bTMR_InputShaft2_B_Iso := FALSE; bTMR_InputShaft2_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedInputShaft2Speed_RPM := (ST_INPUT_SHAFT2_203A + ST_INPUT_SHAFT2_203C) / 2.0;
    bTMR_InputShaft2_A_Iso := FALSE; bTMR_InputShaft2_B_Iso := TRUE; bTMR_InputShaft2_C_Iso := FALSE;
ELSE
    tTMR_InputShaft2_Timer := tTMR_InputShaft2_Timer + rConst_SampleTimeTs;
    rVotedInputShaft2Speed_RPM := ST_INPUT_SHAFT2_203B;
    IF tTMR_InputShaft2_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.7 ST_OUTPUT_PROP_SHAFT_204: Propeller Shaft Rotational Speed [rpm] *)
rDiffAB := ABS(ST_OUTPUT_PROP_SHAFT_204A - ST_OUTPUT_PROP_SHAFT_204B);
rDiffBC := ABS(ST_OUTPUT_PROP_SHAFT_204B - ST_OUTPUT_PROP_SHAFT_204C);
rDiffAC := ABS(ST_OUTPUT_PROP_SHAFT_204A - ST_OUTPUT_PROP_SHAFT_204C);
bMatchAB := (rDiffAB <= rTol_PropShaftSpeed_RPM);
bMatchBC := (rDiffBC <= rTol_PropShaftSpeed_RPM);
bMatchAC := (rDiffAC <= rTol_PropShaftSpeed_RPM);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedPropShaftSpeed_RPM := (ST_OUTPUT_PROP_SHAFT_204A + ST_OUTPUT_PROP_SHAFT_204B + ST_OUTPUT_PROP_SHAFT_204C) / 3.0;
    bTMR_PropShaft_A_Iso := FALSE; bTMR_PropShaft_B_Iso := FALSE; bTMR_PropShaft_C_Iso := FALSE;
    tTMR_PropShaft_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedPropShaftSpeed_RPM := (ST_OUTPUT_PROP_SHAFT_204A + ST_OUTPUT_PROP_SHAFT_204B) / 2.0;
    bTMR_PropShaft_A_Iso := FALSE; bTMR_PropShaft_B_Iso := FALSE; bTMR_PropShaft_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedPropShaftSpeed_RPM := (ST_OUTPUT_PROP_SHAFT_204B + ST_OUTPUT_PROP_SHAFT_204C) / 2.0;
    bTMR_PropShaft_A_Iso := TRUE; bTMR_PropShaft_B_Iso := FALSE; bTMR_PropShaft_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedPropShaftSpeed_RPM := (ST_OUTPUT_PROP_SHAFT_204A + ST_OUTPUT_PROP_SHAFT_204C) / 2.0;
    bTMR_PropShaft_A_Iso := FALSE; bTMR_PropShaft_B_Iso := TRUE; bTMR_PropShaft_C_Iso := FALSE;
ELSE
    tTMR_PropShaft_Timer := tTMR_PropShaft_Timer + rConst_SampleTimeTs;
    rVotedPropShaftSpeed_RPM := ST_OUTPUT_PROP_SHAFT_204B;
    IF tTMR_PropShaft_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.8 ZT_SHIFT_RAIL_POS_301: Shift Rail Synchronizer Sleeve Position [mm] *)
rDiffAB := ABS(ZT_SHIFT_RAIL_POS_301A - ZT_SHIFT_RAIL_POS_301B);
rDiffBC := ABS(ZT_SHIFT_RAIL_POS_301B - ZT_SHIFT_RAIL_POS_301C);
rDiffAC := ABS(ZT_SHIFT_RAIL_POS_301A - ZT_SHIFT_RAIL_POS_301C);
bMatchAB := (rDiffAB <= rTol_ShiftRailPos_mm);
bMatchBC := (rDiffBC <= rTol_ShiftRailPos_mm);
bMatchAC := (rDiffAC <= rTol_ShiftRailPos_mm);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedShiftRailPos_mm := (ZT_SHIFT_RAIL_POS_301A + ZT_SHIFT_RAIL_POS_301B + ZT_SHIFT_RAIL_POS_301C) / 3.0;
    bTMR_ShiftRail_A_Iso := FALSE; bTMR_ShiftRail_B_Iso := FALSE; bTMR_ShiftRail_C_Iso := FALSE;
    tTMR_ShiftRail_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedShiftRailPos_mm := (ZT_SHIFT_RAIL_POS_301A + ZT_SHIFT_RAIL_POS_301B) / 2.0;
    bTMR_ShiftRail_A_Iso := FALSE; bTMR_ShiftRail_B_Iso := FALSE; bTMR_ShiftRail_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedShiftRailPos_mm := (ZT_SHIFT_RAIL_POS_301B + ZT_SHIFT_RAIL_POS_301C) / 2.0;
    bTMR_ShiftRail_A_Iso := TRUE; bTMR_ShiftRail_B_Iso := FALSE; bTMR_ShiftRail_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedShiftRailPos_mm := (ZT_SHIFT_RAIL_POS_301A + ZT_SHIFT_RAIL_POS_301C) / 2.0;
    bTMR_ShiftRail_A_Iso := FALSE; bTMR_ShiftRail_B_Iso := TRUE; bTMR_ShiftRail_C_Iso := FALSE;
ELSE
    tTMR_ShiftRail_Timer := tTMR_ShiftRail_Timer + rConst_SampleTimeTs;
    rVotedShiftRailPos_mm := ZT_SHIFT_RAIL_POS_301B;
    IF tTMR_ShiftRail_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.9 TT_TRANSMISSION_OIL_401: Sump Lubrication Oil Temperature [deg C] *)
rDiffAB := ABS(TT_TRANSMISSION_OIL_401A - TT_TRANSMISSION_OIL_401B);
rDiffBC := ABS(TT_TRANSMISSION_OIL_401B - TT_TRANSMISSION_OIL_401C);
rDiffAC := ABS(TT_TRANSMISSION_OIL_401A - TT_TRANSMISSION_OIL_401C);
bMatchAB := (rDiffAB <= rTol_TransOilTemp_degC);
bMatchBC := (rDiffBC <= rTol_TransOilTemp_degC);
bMatchAC := (rDiffAC <= rTol_TransOilTemp_degC);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedTransOilTemp_degC := (TT_TRANSMISSION_OIL_401A + TT_TRANSMISSION_OIL_401B + TT_TRANSMISSION_OIL_401C) / 3.0;
    bTMR_TransOilTemp_A_Iso := FALSE; bTMR_TransOilTemp_B_Iso := FALSE; bTMR_TransOilTemp_C_Iso := FALSE;
    tTMR_TransOilTemp_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedTransOilTemp_degC := (TT_TRANSMISSION_OIL_401A + TT_TRANSMISSION_OIL_401B) / 2.0;
    bTMR_TransOilTemp_A_Iso := FALSE; bTMR_TransOilTemp_B_Iso := FALSE; bTMR_TransOilTemp_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedTransOilTemp_degC := (TT_TRANSMISSION_OIL_401B + TT_TRANSMISSION_OIL_401C) / 2.0;
    bTMR_TransOilTemp_A_Iso := TRUE; bTMR_TransOilTemp_B_Iso := FALSE; bTMR_TransOilTemp_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedTransOilTemp_degC := (TT_TRANSMISSION_OIL_401A + TT_TRANSMISSION_OIL_401C) / 2.0;
    bTMR_TransOilTemp_A_Iso := FALSE; bTMR_TransOilTemp_B_Iso := TRUE; bTMR_TransOilTemp_C_Iso := FALSE;
ELSE
    tTMR_TransOilTemp_Timer := tTMR_TransOilTemp_Timer + rConst_SampleTimeTs;
    rVotedTransOilTemp_degC := TT_TRANSMISSION_OIL_401B;
    IF tTMR_TransOilTemp_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.10 TT_CLUTCH_FRICTION_PLATE_402: Friction Plate Interface Temperature [deg C] *)
rDiffAB := ABS(TT_CLUTCH_FRICTION_PLATE_402A - TT_CLUTCH_FRICTION_PLATE_402B);
rDiffBC := ABS(TT_CLUTCH_FRICTION_PLATE_402B - TT_CLUTCH_FRICTION_PLATE_402C);
rDiffAC := ABS(TT_CLUTCH_FRICTION_PLATE_402A - TT_CLUTCH_FRICTION_PLATE_402C);
bMatchAB := (rDiffAB <= rTol_ClutchPlateTemp_degC);
bMatchBC := (rDiffBC <= rTol_ClutchPlateTemp_degC);
bMatchAC := (rDiffAC <= rTol_ClutchPlateTemp_degC);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedClutchPlateTemp_degC := (TT_CLUTCH_FRICTION_PLATE_402A + TT_CLUTCH_FRICTION_PLATE_402B + TT_CLUTCH_FRICTION_PLATE_402C) / 3.0;
    bTMR_ClutchPlateTemp_A_Iso := FALSE; bTMR_ClutchPlateTemp_B_Iso := FALSE; bTMR_ClutchPlateTemp_C_Iso := FALSE;
    tTMR_ClutchPlateTemp_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedClutchPlateTemp_degC := (TT_CLUTCH_FRICTION_PLATE_402A + TT_CLUTCH_FRICTION_PLATE_402B) / 2.0;
    bTMR_ClutchPlateTemp_A_Iso := FALSE; bTMR_ClutchPlateTemp_B_Iso := FALSE; bTMR_ClutchPlateTemp_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedClutchPlateTemp_degC := (TT_CLUTCH_FRICTION_PLATE_402B + TT_CLUTCH_FRICTION_PLATE_402C) / 2.0;
    bTMR_ClutchPlateTemp_A_Iso := TRUE; bTMR_ClutchPlateTemp_B_Iso := FALSE; bTMR_ClutchPlateTemp_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedClutchPlateTemp_degC := (TT_CLUTCH_FRICTION_PLATE_402A + TT_CLUTCH_FRICTION_PLATE_402C) / 2.0;
    bTMR_ClutchPlateTemp_A_Iso := FALSE; bTMR_ClutchPlateTemp_B_Iso := TRUE; bTMR_ClutchPlateTemp_C_Iso := FALSE;
ELSE
    tTMR_ClutchPlateTemp_Timer := tTMR_ClutchPlateTemp_Timer + rConst_SampleTimeTs;
    rVotedClutchPlateTemp_degC := TT_CLUTCH_FRICTION_PLATE_402B;
    IF tTMR_ClutchPlateTemp_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;

(* 1.11 AT_CHASSIS_INCLINOMETER_501: Road Grade Chassis Inclinometer [%] *)
rDiffAB := ABS(AT_CHASSIS_INCLINOMETER_501A - AT_CHASSIS_INCLINOMETER_501B);
rDiffBC := ABS(AT_CHASSIS_INCLINOMETER_501B - AT_CHASSIS_INCLINOMETER_501C);
rDiffAC := ABS(AT_CHASSIS_INCLINOMETER_501A - AT_CHASSIS_INCLINOMETER_501C);
bMatchAB := (rDiffAB <= rTol_RoadGrade_Pct);
bMatchBC := (rDiffBC <= rTol_RoadGrade_Pct);
bMatchAC := (rDiffAC <= rTol_RoadGrade_Pct);

IF bMatchAB AND bMatchBC AND bMatchAC THEN
    rVotedRoadGrade_Pct := (AT_CHASSIS_INCLINOMETER_501A + AT_CHASSIS_INCLINOMETER_501B + AT_CHASSIS_INCLINOMETER_501C) / 3.0;
    bTMR_RoadGrade_A_Iso := FALSE; bTMR_RoadGrade_B_Iso := FALSE; bTMR_RoadGrade_C_Iso := FALSE;
    tTMR_RoadGrade_Timer := 0.0;
ELSIF bMatchAB THEN
    rVotedRoadGrade_Pct := (AT_CHASSIS_INCLINOMETER_501A + AT_CHASSIS_INCLINOMETER_501B) / 2.0;
    bTMR_RoadGrade_A_Iso := FALSE; bTMR_RoadGrade_B_Iso := FALSE; bTMR_RoadGrade_C_Iso := TRUE;
ELSIF bMatchBC THEN
    rVotedRoadGrade_Pct := (AT_CHASSIS_INCLINOMETER_501B + AT_CHASSIS_INCLINOMETER_501C) / 2.0;
    bTMR_RoadGrade_A_Iso := TRUE; bTMR_RoadGrade_B_Iso := FALSE; bTMR_RoadGrade_C_Iso := FALSE;
ELSIF bMatchAC THEN
    rVotedRoadGrade_Pct := (AT_CHASSIS_INCLINOMETER_501A + AT_CHASSIS_INCLINOMETER_501C) / 2.0;
    bTMR_RoadGrade_A_Iso := FALSE; bTMR_RoadGrade_B_Iso := TRUE; bTMR_RoadGrade_C_Iso := FALSE;
ELSE
    tTMR_RoadGrade_Timer := tTMR_RoadGrade_Timer + rConst_SampleTimeTs;
    rVotedRoadGrade_Pct := AT_CHASSIS_INCLINOMETER_501B;
    IF tTMR_RoadGrade_Timer >= rTmrPersistenceTimeout_s THEN
        bAlarm_TMR_Degraded := TRUE;
    END_IF;
END_IF;"""
    parts.append(phase1)

    # =========================================================================
    # 7. PHASE 2: CYBER-PHYSICAL PHYSICS & STATE PROPAGATION
    # =========================================================================
    phase2 = """(* ===================================================================================================================
 * PHASE 2: CYBER-PHYSICAL STATE PROPAGATION & THERMAL FRICTION OBSERVER
 * =================================================================================================================== *)

(* 2.1 Angular Slip Velocities & Stribeck Friction Dynamics *)
rClutch1_SlipSpeedRadS := (rVotedEngineSpeed_RPM - rVotedInputShaft1Speed_RPM) * (2.0 * rConst_Pi / 60.0);
rClutch2_SlipSpeedRadS := (rVotedEngineSpeed_RPM - rVotedInputShaft2Speed_RPM) * (2.0 * rConst_Pi / 60.0);

(* Stribeck Friction Coefficients for Clutch 1 & Clutch 2 *)
rTempSum := ABS(rClutch1_SlipSpeedRadS) / rConst_StribeckVelocityWs;
IF rTempSum > 20.0 THEN
    rTempSum := 20.0;
END_IF;
(* Stribeck exponential decay: mu(w) = mu_c + (mu_s - mu_c)*exp(-x^delta) + sigma_v*|w| *)
rTempSum := rConst_StribeckMuCoulomb + (rConst_StribeckMuStatic - rConst_StribeckMuCoulomb)
            * EXP(-EXPT(rTempSum, rConst_StribeckExponentDelta))
            + rConst_StribeckViscousCoeff * ABS(rClutch1_SlipSpeedRadS);

(* Net Clamping Normal Force on Clutch 1 [N] *)
IF rVotedClutch1Pressure_bar > rConst_ClutchReturnSpringP THEN
    rDiffAB := (rVotedClutch1Pressure_bar - rConst_ClutchReturnSpringP) * 1.0E5 * rConst_ClutchPistonArea;
ELSE
    rDiffAB := 0.0;
END_IF;
(* Transmitted Friction Torque on Clutch 1 [Nm] *)
rObservedClutch1Torque_Nm := (2.0 / 3.0) * INT_TO_REAL(nConst_ClutchFrictionFaces) * rConst_ClutchMeanRadius * rDiffAB * rTempSum;

(* Stribeck Friction for Clutch 2 *)
rTempSum := ABS(rClutch2_SlipSpeedRadS) / rConst_StribeckVelocityWs;
IF rTempSum > 20.0 THEN
    rTempSum := 20.0;
END_IF;
rTempSum := rConst_StribeckMuCoulomb + (rConst_StribeckMuStatic - rConst_StribeckMuCoulomb)
            * EXP(-EXPT(rTempSum, rConst_StribeckExponentDelta))
            + rConst_StribeckViscousCoeff * ABS(rClutch2_SlipSpeedRadS);

IF rVotedClutch2Pressure_bar > rConst_ClutchReturnSpringP THEN
    rDiffBC := (rVotedClutch2Pressure_bar - rConst_ClutchReturnSpringP) * 1.0E5 * rConst_ClutchPistonArea;
ELSE
    rDiffBC := 0.0;
END_IF;
rObservedClutch2Torque_Nm := (2.0 / 3.0) * INT_TO_REAL(nConst_ClutchFrictionFaces) * rConst_ClutchMeanRadius * rDiffBC * rTempSum;

(* Directional torque signing based on slip direction *)
IF rClutch1_SlipSpeedRadS < 0.0 THEN
    rObservedClutch1Torque_Nm := -rObservedClutch1Torque_Nm;
END_IF;
IF rClutch2_SlipSpeedRadS < 0.0 THEN
    rObservedClutch2Torque_Nm := -rObservedClutch2Torque_Nm;
END_IF;

(* 2.2 Wet Clutch Thermal Dissipation Lumped Model *)
rClutch1_FricPowerWatts := ABS(rObservedClutch1Torque_Nm * rClutch1_SlipSpeedRadS);
rClutch2_FricPowerWatts := ABS(rObservedClutch2Torque_Nm * rClutch2_SlipSpeedRadS);

(* Integrated Thermal Energy Dissipation [kJ] *)
rClutch1ThermalEnergy_kJ := rClutch1ThermalEnergy_kJ + (rClutch1_FricPowerWatts * rConst_SampleTimeTs / 1000.0);
rClutch2ThermalEnergy_kJ := rClutch2ThermalEnergy_kJ + (rClutch2_FricPowerWatts * rConst_SampleTimeTs / 1000.0);

(* Bulk Steel Plate Thermal State Observer d(T)/dt = (P_fric - h*A*(T - T_oil)) / (m*cp) *)
rClutch1_BulkTempObserved := rClutch1_BulkTempObserved + rConst_SampleTimeTs * (
    (rClutch1_FricPowerWatts - rConst_ConvectiveCoolingHA * (rClutch1_BulkTempObserved - rVotedTransOilTemp_degC))
    / (rConst_ClutchPlatePackMass * rConst_SteelSpecificHeat)
);
rClutch2_BulkTempObserved := rClutch2_BulkTempObserved + rConst_SampleTimeTs * (
    (rClutch2_FricPowerWatts - rConst_ConvectiveCoolingHA * (rClutch2_BulkTempObserved - rVotedTransOilTemp_degC))
    / (rConst_ClutchPlatePackMass * rConst_SteelSpecificHeat)
);

(* 2.3 Drive Axle Half-Shaft Torsional Torque & Vehicle Longitudinal Kinematics *)
rDrivelineTorsionalTorque_Nm := rConst_HalfShaftStiffness * arrState_x[5]
                              + rConst_HalfShaftDamping * (
                                  (rVotedPropShaftSpeed_RPM * (2.0 * rConst_Pi / 60.0) / rConst_FinalDriveAxleRatio)
                                  - (arrState_x[6] / rConst_TireRadiusDyn)
                              );

(* Resisting Road Forces *)
rDiffAB := rConst_RollingResistCoeff * rConst_MaxGrossTruckMass * rConst_Gravity * COS(rVotedRoadGrade_Pct * 0.01);
rDiffBC := 0.5 * rConst_AirDensity * rConst_TruckDragCoeff * rConst_TruckFrontalArea * EXPT(arrState_x[6], 2.0);
rDiffAC := rConst_MaxGrossTruckMass * rConst_Gravity * SIN(rVotedRoadGrade_Pct * 0.01);

(* Net Acceleration & Jerk *)
rVehicleLongitudinalAcc_mps2 := ((rDrivelineTorsionalTorque_Nm / rConst_TireRadiusDyn) - rDiffAB - rDiffBC - rDiffAC) / rConst_MaxGrossTruckMass;
rLongitudinalJerk_mps3 := (rVehicleLongitudinalAcc_mps2 - rPrevVehicleAcc) / rConst_SampleTimeTs;
rPrevVehicleAcc := rVehicleLongitudinalAcc_mps2;

(* Adaptive Gross Vehicle Weight (GVW) Recursive Estimation *)
IF (ABS(rVehicleLongitudinalAcc_mps2) > 0.15) AND (bServiceBrakeApplied = FALSE) THEN
    rEstimatedGVW_Tons := ((rDrivelineTorsionalTorque_Nm / rConst_TireRadiusDyn) - rDiffBC)
                          / (1000.0 * (rVehicleLongitudinalAcc_mps2 + rConst_Gravity * (SIN(rVotedRoadGrade_Pct * 0.01) + rConst_RollingResistCoeff)));
    IF rEstimatedGVW_Tons < (rConst_EmptyTruckMass / 1000.0) THEN
        rEstimatedGVW_Tons := rConst_EmptyTruckMass / 1000.0;
    ELSIF rEstimatedGVW_Tons > (rConst_MaxGrossTruckMass / 1000.0) THEN
        rEstimatedGVW_Tons := rConst_MaxGrossTruckMass / 1000.0;
    END_IF;
END_IF;

(* 2.4 Discrete 8x8 State-Space Time Propagation (x[k+1] = A*x[k] + B*u[k]) *)
FOR iIdx := 1 TO 8 DO
    rTempSum := 0.0;
    FOR jIdx := 1 TO 8 DO
        rTempSum := rTempSum + arrA[iIdx, jIdx] * arrState_x[jIdx];
    END_FOR;
    FOR kIdx := 1 TO 4 DO
        rTempSum := rTempSum + arrB[iIdx, kIdx] * arrControl_u[kIdx];
    END_FOR;
    arrState_x_next[iIdx] := rTempSum;
END_FOR;

(* State update for next sample *)
FOR iIdx := 1 TO 8 DO
    arrState_x[iIdx] := arrState_x_next[iIdx];
END_FOR;"""
    parts.append(phase2)

    # =========================================================================
    # 8. PHASE 3: RECEDING-HORIZON MPC & ANTI-JERK FILTER
    # =========================================================================
    phase3 = """(* ===================================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & ANTI-JERK ACTIVE DAMPING
 * =================================================================================================================== *)

(* 3.1 Driveline Torsional Anti-Jerk Active Damping Filter *)
(* Isolates 3.5 to 5.5 Hz driveline torsional resonant shuffle *)
rDiffAB := (rVotedPropShaftSpeed_RPM * (2.0 * rConst_Pi / 60.0) / rConst_FinalDriveAxleRatio) - (arrState_x[6] / rConst_TireRadiusDyn);
rAntiJerk_FilterState1 := rAntiJerk_FilterState1 + rConst_SampleTimeTs * (rDiffAB - 25.0 * rAntiJerk_FilterState1 - 950.0 * rAntiJerk_FilterState2);
rAntiJerk_FilterState2 := rAntiJerk_FilterState2 + rConst_SampleTimeTs * rAntiJerk_FilterState1;

rAntiJerkDampingTorque_Nm := - (rAntiJerk_Kp * rAntiJerk_FilterState1 + rAntiJerk_Kd * (rDiffAB - rAntiJerk_PrevError) / rConst_SampleTimeTs);
rAntiJerk_PrevError := rDiffAB;

(* Schedulable clamping of anti-jerk counter-torque *)
IF rAntiJerkDampingTorque_Nm > rAntiJerk_TorqueLimitNm THEN
    rAntiJerkDampingTorque_Nm := rAntiJerk_TorqueLimitNm;
ELSIF rAntiJerkDampingTorque_Nm < -rAntiJerk_TorqueLimitNm THEN
    rAntiJerkDampingTorque_Nm := -rAntiJerk_TorqueLimitNm;
END_IF;

(* 3.2 Receding-Horizon MPC Quadratic Cost Evaluation & Gradient Descent *)
(* Reference State Vector Setup *)
arrStateReference[1] := rVotedEngineSpeed_RPM * (2.0 * rConst_Pi / 60.0);
arrStateReference[2] := rVotedPropShaftSpeed_RPM * arrGearRatios[MAX(1, nActiveGear)] * (2.0 * rConst_Pi / 60.0) / rConst_FinalDriveAxleRatio;
arrStateReference[3] := rVotedPropShaftSpeed_RPM * arrGearRatios[MAX(1, nPreSelectedGear)] * (2.0 * rConst_Pi / 60.0) / rConst_FinalDriveAxleRatio;
arrStateReference[4] := rVotedPropShaftSpeed_RPM * (2.0 * rConst_Pi / 60.0);
arrStateReference[5] := 0.0; (* Zero torsional twist desired during steady state *)
arrStateReference[6] := (rDriverThrottlePedal_Pct / 100.0) * 25.0; (* Target cruise velocity [m/s] *)
arrStateReference[7] := rTouchPointPressure_bar;
arrStateReference[8] := rTouchPointPressure_bar;

(* Compute Current Scalar Quadratic Cost J *)
rMpcObjectiveValue := 0.0;
FOR iIdx := 1 TO 8 DO
    rMpcObjectiveValue := rMpcObjectiveValue + arrQ_Cost[iIdx] * EXPT(arrState_x[iIdx] - arrStateReference[iIdx], 2.0);
END_FOR;
FOR kIdx := 1 TO 4 DO
    rMpcObjectiveValue := rMpcObjectiveValue + arrR_Cost[kIdx] * EXPT(arrControl_u[kIdx], 2.0);
    rMpcObjectiveValue := rMpcObjectiveValue + arrS_Cost[kIdx] * EXPT(arrControl_u[kIdx] - arrControl_u_prev[kIdx], 2.0);
END_FOR;
rMPC_QuadraticCost := rMpcObjectiveValue;

(* Projected Gradient Descent Solver (nMpcIterations = 4) *)
FOR mIdx := 1 TO nMpcIterations DO
    (* Compute Analytical Gradient nabla_J = B^T * Q * (A*x + B*u - x_ref) + R*u + S*(u - u_prev) *)
    FOR kIdx := 1 TO 4 DO
        rTempSum := 0.0;
        FOR iIdx := 1 TO 8 DO
            rDiffAB := 0.0;
            FOR jIdx := 1 TO 8 DO
                rDiffAB := rDiffAB + arrA[iIdx, jIdx] * arrState_x[jIdx];
            END_FOR;
            FOR jIdx := 1 TO 4 DO
                rDiffAB := rDiffAB + arrB[iIdx, jIdx] * arrControl_u[jIdx];
            END_FOR;
            rTempSum := rTempSum + arrB[iIdx, kIdx] * arrQ_Cost[iIdx] * (rDiffAB - arrStateReference[iIdx]);
        END_FOR;
        arrMpcGradient[kIdx] := rTempSum + arrR_Cost[kIdx] * arrControl_u[kIdx] + arrS_Cost[kIdx] * (arrControl_u[kIdx] - arrControl_u_prev[kIdx]);
    END_FOR;

    (* Actuator Descent Step & Constraint Clamping *)
    FOR kIdx := 1 TO 4 DO
        arrControl_u[kIdx] := arrControl_u[kIdx] - rMpcStepAlpha * arrMpcGradient[kIdx];

        (* Hard Saturation Constraints *)
        IF arrControl_u[kIdx] < arrU_Min[kIdx] THEN
            arrControl_u[kIdx] := arrU_Min[kIdx];
        ELSIF arrControl_u[kIdx] > arrU_Max[kIdx] THEN
            arrControl_u[kIdx] := arrU_Max[kIdx];
        END_IF;

        (* Slew Rate Clamping *)
        arrControl_u_delta[kIdx] := arrControl_u[kIdx] - arrControl_u_prev[kIdx];
        IF arrControl_u_delta[kIdx] > arrDeltaU_Max[kIdx] THEN
            arrControl_u[kIdx] := arrControl_u_prev[kIdx] + arrDeltaU_Max[kIdx];
        ELSIF arrControl_u_delta[kIdx] < -arrDeltaU_Max[kIdx] THEN
            arrControl_u[kIdx] := arrControl_u_prev[kIdx] - arrDeltaU_Max[kIdx];
        END_IF;
    END_FOR;
END_FOR;

(* Store control vector for slew calculation in next scan *)
FOR kIdx := 1 TO 4 DO
    arrControl_u_prev[kIdx] := arrControl_u[kIdx];
END_FOR;"""
    parts.append(phase3)

    # =========================================================================
    # 9. PHASE 4: SYNCHRONIZER SLEEVE SPEED MATCHING
    # =========================================================================
    phase4 = """(* ===================================================================================================================
 * PHASE 4: SYNCHRONIZER SLEEVE & DOG CLUTCH SPEED MATCHING ENGINE
 * =================================================================================================================== *)

(* Calculate Target Input Shaft Speed for Pre-Selected Gear *)
IF nPreSelectedGear >= 1 AND nPreSelectedGear <= 12 THEN
    rSynchro_TargetShaftSpeed_RPM := (rVotedPropShaftSpeed_RPM * arrGearRatios[nPreSelectedGear]) / rConst_FinalDriveAxleRatio;
ELSE
    rSynchro_TargetShaftSpeed_RPM := 0.0;
END_IF;

(* Evaluate Synchronizer Speed Matching Error *)
IF (nPreSelectedGear MOD 2) = 1 THEN
    (* Odd Gear: Target Shaft is Input Shaft 1 *)
    rSynchro_SpeedDiff_RPM := ABS(rSynchro_TargetShaftSpeed_RPM - rVotedInputShaft1Speed_RPM);
ELSE
    (* Even Gear: Target Shaft is Input Shaft 2 *)
    rSynchro_SpeedDiff_RPM := ABS(rSynchro_TargetShaftSpeed_RPM - rVotedInputShaft2Speed_RPM);
END_IF;

(* Shift Rail Mechanical Jam Detection *)
rShiftRail_PosError_mm := ABS(rShiftRail_TargetPos_mm - rVotedShiftRailPos_mm);
IF (rShiftRail_PosError_mm > rConst_ShiftRailJamTol_mm) AND (ABS(rShiftRail_PneumaticForceCmd_N) > 100.0) THEN
    tShiftRail_JamTimer := tShiftRail_JamTimer + rConst_SampleTimeTs;
    IF tShiftRail_JamTimer >= rConst_ShiftRailJamTimeout THEN
        bShiftRailJamFault := TRUE;
    END_IF;
ELSE
    tShiftRail_JamTimer := 0.0;
END_IF;

(* Closed-Loop Pneumatic Shift Rail Force Modulation *)
IF bShiftRailJamFault = FALSE THEN
    rShiftRail_PneumaticForceCmd_N := 250.0 * (rShiftRail_TargetPos_mm - rVotedShiftRailPos_mm);
    IF rShiftRail_PneumaticForceCmd_N > 1200.0 THEN
        rShiftRail_PneumaticForceCmd_N := 1200.0;
    ELSIF rShiftRail_PneumaticForceCmd_N < -1200.0 THEN
        rShiftRail_PneumaticForceCmd_N := -1200.0;
    END_IF;
ELSE
    rShiftRail_PneumaticForceCmd_N := 0.0;
END_IF;"""
    parts.append(phase4)

    # =========================================================================
    # 10. PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # =========================================================================
    phase5 = """(* ===================================================================================================================
 * PHASE 5: MULTI-STAGE CASE FINITE STATE MACHINE (12 STATES)
 * =================================================================================================================== *)
tStateDwellTimer := tStateDwellTimer + rConst_SampleTimeTs;

CASE nFSM_State OF

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 1: TRANSMISSION BOOT & SENSOR ZERO CALIBRATION                                      *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_BOOT_CALIBRATION:
        wFSM_CurrentState := 16#0001;
        bTransmissionReady := FALSE;
        bShiftInProgress := FALSE;
        bEmergencyNeutralValveCmd := FALSE;
        rClutch1_PropPressureCmd_bar := 0.0;
        rClutch2_PropPressureCmd_bar := 0.0;
        rEngineTorqueRequest_Nm := 0.0;
        rShiftRail_TargetPos_mm := 0.0; (* Center neutral *)

        IF bMasterEnable AND bEStopChainOK_NC AND (rVotedMainLineHydr_bar >= rAlarmMainHydr_L) THEN
            IF tStateDwellTimer >= 0.250 THEN
                bTransmissionReady := TRUE;
                nFSM_NextState := c_STATE_NEUTRAL_IDLE;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 2: NEUTRAL IDLE WITH BOTH CLUTCHES FULLY DISENGAGED                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_NEUTRAL_IDLE:
        wFSM_CurrentState := 16#0002;
        bShiftInProgress := FALSE;
        rClutch1_PropPressureCmd_bar := 0.0;
        rClutch2_PropPressureCmd_bar := 0.0;
        rShiftRail_TargetPos_mm := 0.0;
        nActiveGear := 0;
        nPreSelectedGear := 0;
        rEngineTorqueRequest_Nm := 0.0;

        IF bDriverShiftRequest AND (nDriverTargetGear = 1) THEN
            nFSM_NextState := c_STATE_FIRST_PRE_SELECT;
        ELSIF bAlarm_ClutchPlateTemp_HH OR (bEStopChainOK_NC = FALSE) THEN
            nFSM_NextState := c_STATE_EMERGENCY_NEUTRAL;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 3: FIRST GEAR PRE-SELECT & STANDBY SHAFT ENGAGEMENT                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_FIRST_PRE_SELECT:
        wFSM_CurrentState := 16#0003;
        bShiftInProgress := TRUE;
        nPreSelectedGear := 1; (* Gear 1 is on Odd Shaft -> Clutch 1 *)
        rShiftRail_TargetPos_mm := 14.0; (* Position for Gear 1 dog clutch engagement *)

        (* Ballistic Fast-Fill pulse to prepare Clutch 1 *)
        IF bStateFirstScan THEN
            tFastFillTimer1 := 0.0;
            bClutch1_FastFillPulse := TRUE;
        END_IF;
        tFastFillTimer1 := tFastFillTimer1 + rConst_SampleTimeTs;
        IF tFastFillTimer1 < rFastFillPulseDuration THEN
            rClutch1_PropPressureCmd_bar := rFastFillPressure_bar;
        ELSE
            bClutch1_FastFillPulse := FALSE;
            rClutch1_PropPressureCmd_bar := rTouchPointPressure_bar; (* Hold at kiss point *)
        END_IF;
        rClutch2_PropPressureCmd_bar := 0.0;

        (* Check sleeve position confirmation *)
        IF (ABS(rVotedShiftRailPos_mm - 14.0) < 0.50) AND (tStateDwellTimer >= 0.120) THEN
            nActiveGear := 1;
            nFSM_NextState := c_STATE_LAUNCH_CLUTCH_SLIP;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 4: VEHICLE LAUNCH CONTROL MODULATED CLUTCH SLIP                                     *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_LAUNCH_CLUTCH_SLIP:
        wFSM_CurrentState := 16#0004;
        bShiftInProgress := FALSE;
        (* Launch torque modulated via throttle pedal demand *)
        rDiffAB := (rDriverThrottlePedal_Pct / 100.0) * 1650.0;
        rEngineTorqueRequest_Nm := rDiffAB + rAntiJerkDampingTorque_Nm;

        (* Ramp Clutch 1 pressure proportionally with slip velocity control *)
        rClutch1_PropPressureCmd_bar := rTouchPointPressure_bar + (rDriverThrottlePedal_Pct / 100.0) * 12.0;
        rClutch2_PropPressureCmd_bar := 0.0;

        (* Pre-select Gear 2 on Standby Even Shaft *)
        nPreSelectedGear := 2;

        (* Lockup detection: slip speed < 15 RPM for 20 ms *)
        IF ABS(rVotedEngineSpeed_RPM - rVotedInputShaft1Speed_RPM) < rSynchro_SpeedMatchTolerance THEN
            IF tStateDwellTimer >= 0.350 THEN
                nFSM_NextState := c_STATE_LOCKUP_CRUISE;
            END_IF;
        END_IF;

        (* Thermal safeguard: if launch slip exceeds 4.0 seconds, force limp mode *)
        IF tStateDwellTimer > 4.0 THEN
            nFSM_NextState := c_STATE_OVERHEAT_LIMP;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 5: DUAL WET CLUTCH TORQUE TRANSFER CROSS-FADING                                     *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_TORQUE_CROSSFADE:
        wFSM_CurrentState := 16#0005;
        bShiftInProgress := TRUE;
        tCrossFadeTimer := tCrossFadeTimer + rConst_SampleTimeTs;
        rCrossFadeAlpha := tCrossFadeTimer / rCrossFadeDuration_s;
        IF rCrossFadeAlpha > 1.0 THEN
            rCrossFadeAlpha := 1.0;
        END_IF;

        (* Dynamic Cross-Fading Pressure Commands: Off-going vs On-coming *)
        IF (nActiveGear MOD 2) = 1 THEN
            (* Upshift: Off-going is Clutch 1, On-coming is Clutch 2 *)
            rClutch1_PropPressureCmd_bar := rTouchPointPressure_bar + (18.0 - rTouchPointPressure_bar) * (1.0 - rCrossFadeAlpha);
            rClutch2_PropPressureCmd_bar := rTouchPointPressure_bar + (18.0 - rTouchPointPressure_bar) * rCrossFadeAlpha;
        ELSE
            (* Upshift: Off-going is Clutch 2, On-coming is Clutch 1 *)
            rClutch2_PropPressureCmd_bar := rTouchPointPressure_bar + (18.0 - rTouchPointPressure_bar) * (1.0 - rCrossFadeAlpha);
            rClutch1_PropPressureCmd_bar := rTouchPointPressure_bar + (18.0 - rTouchPointPressure_bar) * rCrossFadeAlpha;
        END_IF;

        rEngineTorqueRequest_Nm := (rDriverThrottlePedal_Pct / 100.0) * 2100.0 + rAntiJerkDampingTorque_Nm;

        IF tCrossFadeTimer >= rCrossFadeDuration_s THEN
            nFSM_NextState := c_STATE_INERTIA_SYNC;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 6: INERTIA PHASE SPEED SYNCHRONIZATION                                              *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_INERTIA_SYNC:
        wFSM_CurrentState := 16#0006;
        bShiftInProgress := TRUE;
        tInertiaPhaseTimer := tInertiaPhaseTimer + rConst_SampleTimeTs;

        (* Hold on-coming clutch clamped while off-going is fully vented *)
        IF (nActiveGear MOD 2) = 1 THEN
            rClutch1_PropPressureCmd_bar := 0.0;
            rClutch2_PropPressureCmd_bar := 19.5;
            rDiffAB := ABS(rVotedEngineSpeed_RPM - rVotedInputShaft2Speed_RPM);
        ELSE
            rClutch2_PropPressureCmd_bar := 0.0;
            rClutch1_PropPressureCmd_bar := 19.5;
            rDiffAB := ABS(rVotedEngineSpeed_RPM - rVotedInputShaft1Speed_RPM);
        END_IF;

        (* Engine torque trim pulls crankshaft speed to match target shaft *)
        rEngineTorqueRequest_Nm := (rDriverThrottlePedal_Pct / 100.0) * 1200.0;

        (* Sub-10 ms synchronization lockup window confirmation *)
        IF (rDiffAB < rSynchro_SpeedMatchTolerance) OR (tInertiaPhaseTimer >= 0.180) THEN
            nActiveGear := nPreSelectedGear;
            nShiftCycleCount := nShiftCycleCount + 1;
            nFSM_NextState := c_STATE_LOCKUP_CRUISE;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 7: LOCKED-UP STEADY-STATE CRUISE EFFICIENCY                                         *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_LOCKUP_CRUISE:
        wFSM_CurrentState := 16#0007;
        bShiftInProgress := FALSE;

        (* Active clutch fully pressurized to 21.0 bar to guarantee zero continuous slip *)
        IF (nActiveGear MOD 2) = 1 THEN
            rClutch1_PropPressureCmd_bar := 21.0;
            rClutch2_PropPressureCmd_bar := 0.0;
            (* Standby pre-select next even gear *)
            IF nActiveGear < 12 THEN
                nPreSelectedGear := nActiveGear + 1;
            END_IF;
        ELSE
            rClutch2_PropPressureCmd_bar := 21.0;
            rClutch1_PropPressureCmd_bar := 0.0;
            (* Standby pre-select next odd gear *)
            IF nActiveGear < 12 THEN
                nPreSelectedGear := nActiveGear + 1;
            END_IF;
        END_IF;

        rEngineTorqueRequest_Nm := (rDriverThrottlePedal_Pct / 100.0) * 2400.0 + rAntiJerkDampingTorque_Nm;

        (* Upshift trigger condition *)
        IF (rVotedEngineSpeed_RPM > 1850.0) AND (nActiveGear < 12) AND (bDriverShiftRequest OR (rDriverThrottlePedal_Pct > 20.0)) THEN
            tCrossFadeTimer := 0.0;
            nFSM_NextState := c_STATE_TORQUE_CROSSFADE;
        (* Downhill grade condition *)
        ELSIF rVotedRoadGrade_Pct < -3.5 THEN
            nFSM_NextState := c_STATE_GRADE_RETARDER;
        (* Severe braking skip shift trigger *)
        ELSIF rDriverBrakePedal_Pct > 45.0 THEN
            nFSM_NextState := c_STATE_SKIP_SHIFT_DECEL;
        (* Thermal overload protection *)
        ELSIF (rVotedClutchPlateTemp_degC >= rAlarmClutchTemp_H) OR (rClutch1_BulkTempObserved >= rAlarmClutchTemp_H) THEN
            nFSM_NextState := c_STATE_OVERHEAT_LIMP;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 8: MULTI-GEAR SKIP SHIFT DECELERATION                                               *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_SKIP_SHIFT_DECEL:
        wFSM_CurrentState := 16#0008;
        bShiftInProgress := TRUE;

        (* Calculate block downshift skip (e.g., Gear 10 -> Gear 7) *)
        IF nActiveGear > 2 THEN
            nPreSelectedGear := nActiveGear - 2;
        ELSE
            nPreSelectedGear := 1;
        END_IF;

        (* Disengage active clutch, match revs *)
        rClutch1_PropPressureCmd_bar := 0.0;
        rClutch2_PropPressureCmd_bar := 0.0;
        rEngineTorqueRequest_Nm := 200.0; (* Rev matching blip *)

        IF tStateDwellTimer >= 0.160 THEN
            nActiveGear := nPreSelectedGear;
            nFSM_NextState := c_STATE_LOCKUP_CRUISE;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 9: DOWNHILL GRADE & ENGINE RETARDER COORDINATION                                    *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_GRADE_RETARDER:
        wFSM_CurrentState := 16#0009;
        bShiftInProgress := FALSE;
        (* Downhill engine braking mode *)
        rEngineTorqueRequest_Nm := 0.0;
        rRetarderBrakeTorqueCmd_Nm := 1450.0 * (ABS(rVotedRoadGrade_Pct) / 10.0);
        IF rRetarderBrakeTorqueCmd_Nm > 2200.0 THEN
            rRetarderBrakeTorqueCmd_Nm := 2200.0;
        END_IF;

        (* Maintain solid lockup to transfer retarding torque to driveline *)
        IF (nActiveGear MOD 2) = 1 THEN
            rClutch1_PropPressureCmd_bar := 22.0;
            rClutch2_PropPressureCmd_bar := 0.0;
        ELSE
            rClutch2_PropPressureCmd_bar := 22.0;
            rClutch1_PropPressureCmd_bar := 0.0;
        END_IF;

        IF rVotedRoadGrade_Pct >= -1.0 THEN
            rRetarderBrakeTorqueCmd_Nm := 0.0;
            nFSM_NextState := c_STATE_LOCKUP_CRUISE;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: CLUTCH OVERHEAT LIMP-HOME PROTECTION                                            *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_OVERHEAT_LIMP:
        wFSM_CurrentState := 16#000A;
        bClutchOverheatWarning := TRUE;
        (* Limit engine power strictly to 40% to reduce frictional thermal generation *)
        rEngineTorqueRequest_Nm := (rDriverThrottlePedal_Pct / 100.0) * 800.0;
        rEngineSpeedLimit_RPM := 1400.0;

        (* Force full clutch clamp to eliminate sliding dissipation *)
        IF (nActiveGear MOD 2) = 1 THEN
            rClutch1_PropPressureCmd_bar := 22.0;
            rClutch2_PropPressureCmd_bar := 0.0;
        ELSE
            rClutch2_PropPressureCmd_bar := 22.0;
            rClutch1_PropPressureCmd_bar := 0.0;
        END_IF;

        IF (rVotedClutchPlateTemp_degC < (rAlarmClutchTemp_H - rAlarmClutchTemp_Deadband))
           AND (rClutch1_BulkTempObserved < (rAlarmClutchTemp_H - rAlarmClutchTemp_Deadband)) THEN
            bClutchOverheatWarning := FALSE;
            rEngineSpeedLimit_RPM := 2200.0;
            nFSM_NextState := c_STATE_LOCKUP_CRUISE;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 11: SHIFT RAIL FAULT SAFE LOCK MODE                                                 *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_RAIL_FAULT_LOCK:
        wFSM_CurrentState := 16#000B;
        bShiftRailJamFault := TRUE;
        bShiftRail_LockPawlEngaged := TRUE;
        rShiftRail_PneumaticForceCmd_N := 0.0;
        (* Inhibit any further gear shifting, keep current gear locked *)
        rEngineTorqueRequest_Nm := (rDriverThrottlePedal_Pct / 100.0) * 1100.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 12: EMERGENCY NEUTRAL HIGH-SPEED HYDRAULIC DUMP                                     *)
    (* ----------------------------------------------------------------------------------------- *)
    c_STATE_EMERGENCY_NEUTRAL:
        wFSM_CurrentState := 16#000C;
        bEmergencyNeutralValveCmd := TRUE;
        rClutch1_PropPressureCmd_bar := 0.0;
        rClutch2_PropPressureCmd_bar := 0.0;
        rEngineTorqueRequest_Nm := 0.0;
        rShiftRail_TargetPos_mm := 0.0;
        bShiftInProgress := FALSE;
        nActiveGear := 0;

        IF bEStopChainOK_NC AND bMasterEnable AND (bAlarm_ClutchPlateTemp_HH = FALSE) THEN
            IF tStateDwellTimer >= 1.0 THEN
                bEmergencyNeutralValveCmd := FALSE;
                nFSM_NextState := c_STATE_BOOT_CALIBRATION;
            END_IF;
        END_IF;

ELSE
    nFSM_State := c_STATE_BOOT_CALIBRATION;
END_CASE;

(* FSM State Transition Execution *)
IF nFSM_NextState <> nFSM_State THEN
    nFSM_State := nFSM_NextState;
    tStateDwellTimer := 0.0;
    bStateFirstScan := TRUE;
ELSE
    bStateFirstScan := FALSE;
END_IF;"""
    parts.append(phase5)

    # =========================================================================
    # 11. PHASE 6: ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING
    # =========================================================================
    phase6 = """(* ===================================================================================================================
 * PHASE 6: ISA-18.2 PROCESS ALARMS & DIAGNOSTIC WORD PACKING
 * =================================================================================================================== *)

(* 6.1 Rate-of-Change (ROC) Calculations *)
rROC_ClutchPlateTemp := (rVotedClutchPlateTemp_degC - rPrevClutchPlateTemp) / rConst_SampleTimeTs;
rPrevClutchPlateTemp := rVotedClutchPlateTemp_degC;

rROC_MainHydrPressure := (rVotedMainLineHydr_bar - rPrevMainHydrPressure) / rConst_SampleTimeTs;
rPrevMainHydrPressure := rVotedMainLineHydr_bar;

(* 6.2 Wet Clutch Multi-Plate Temperature Alarms *)
IF rVotedClutchPlateTemp_degC >= rAlarmClutchTemp_HH THEN
    bAlarm_ClutchPlateTemp_HH := TRUE;
ELSIF rVotedClutchPlateTemp_degC < (rAlarmClutchTemp_HH - rAlarmClutchTemp_Deadband) THEN
    bAlarm_ClutchPlateTemp_HH := FALSE;
END_IF;

IF rVotedClutchPlateTemp_degC >= rAlarmClutchTemp_H THEN
    bAlarm_ClutchPlateTemp_H := TRUE;
ELSIF rVotedClutchPlateTemp_degC < (rAlarmClutchTemp_H - rAlarmClutchTemp_Deadband) THEN
    bAlarm_ClutchPlateTemp_H := FALSE;
END_IF;

IF rROC_ClutchPlateTemp >= rAlarmClutchTemp_MaxROC THEN
    bAlarm_ClutchPlateTemp_ROC := TRUE;
ELSE
    bAlarm_ClutchPlateTemp_ROC := FALSE;
END_IF;

(* 6.3 Main Hydraulic Supply Pressure Alarms *)
IF rVotedMainLineHydr_bar <= rAlarmMainHydr_LL THEN
    bAlarm_MainHydr_LL := TRUE;
ELSIF rVotedMainLineHydr_bar > (rAlarmMainHydr_LL + rAlarmMainHydr_Deadband) THEN
    bAlarm_MainHydr_LL := FALSE;
END_IF;

IF rVotedMainLineHydr_bar <= rAlarmMainHydr_L THEN
    bAlarm_MainHydr_L := TRUE;
ELSIF rVotedMainLineHydr_bar > (rAlarmMainHydr_L + rAlarmMainHydr_Deadband) THEN
    bAlarm_MainHydr_L := FALSE;
END_IF;

(* 6.4 Clutch Pressure Deviation Alarms *)
IF ABS(rClutch1_PropPressureCmd_bar - rVotedClutch1Pressure_bar) >= rAlarmClutchDev_HH THEN
    bAlarm_ClutchDev1_HH := TRUE;
ELSE
    bAlarm_ClutchDev1_HH := FALSE;
END_IF;

IF ABS(rClutch2_PropPressureCmd_bar - rVotedClutch2Pressure_bar) >= rAlarmClutchDev_HH THEN
    bAlarm_ClutchDev2_HH := TRUE;
ELSE
    bAlarm_ClutchDev2_HH := FALSE;
END_IF;

(* 6.5 Longitudinal Jerk Comfort Exceedance *)
IF ABS(rLongitudinalJerk_mps3) > rAlarmLongJerk_Max THEN
    bAlarm_LongJerkExceeded := TRUE;
ELSE
    bAlarm_LongJerkExceeded := FALSE;
END_IF;

(* Automatic Emergency Transition on Critical Trips *)
IF bAlarm_ClutchPlateTemp_HH OR bAlarm_MainHydr_LL OR (bEStopChainOK_NC = FALSE) THEN
    nFSM_State := c_STATE_EMERGENCY_NEUTRAL;
END_IF;

(* Shift Rail Mechanical Jam Trip Transition *)
IF bShiftRailJamFault THEN
    nFSM_State := c_STATE_RAIL_FAULT_LOCK;
END_IF;

(* 6.6 Diagnostic Word Packing *)
(* dwDiagnosticWord01_FSM: Operational & Mechatronic Status *)
dwDiagnosticWord01_FSM := 16#00000000;
IF bTransmissionReady THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000001; END_IF;
IF bShiftInProgress THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000002; END_IF;
IF bClutch1_FastFillPulse THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000004; END_IF;
IF bClutch2_FastFillPulse THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000008; END_IF;
IF bShiftRail_LockPawlEngaged THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000010; END_IF;
IF bEmergencyNeutralValveCmd THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000020; END_IF;
IF bEngineRetarderEnable THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000040; END_IF;
IF bTrailerConnected THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000080; END_IF;
IF bServiceBrakeApplied THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000100; END_IF;
IF bParkingBrakeReleased THEN dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR 16#00000200; END_IF;
dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR SHL(INT_TO_DWORD(nActiveGear), 12);
dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR SHL(INT_TO_DWORD(nPreSelectedGear), 16);
dwDiagnosticWord01_FSM := dwDiagnosticWord01_FSM OR SHL(INT_TO_DWORD(nFSM_State), 20);

(* dwDiagnosticWord02_TMR: 2oo3 Sensor Channel Health *)
dwDiagnosticWord02_TMR := 16#00000000;
IF bTMR_Clutch1Pres_A_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000001; END_IF;
IF bTMR_Clutch1Pres_B_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000002; END_IF;
IF bTMR_Clutch1Pres_C_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000004; END_IF;
IF bTMR_Clutch2Pres_A_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000008; END_IF;
IF bTMR_Clutch2Pres_B_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000010; END_IF;
IF bTMR_Clutch2Pres_C_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000020; END_IF;
IF bTMR_MainLineHydr_A_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000040; END_IF;
IF bTMR_MainLineHydr_B_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000080; END_IF;
IF bTMR_MainLineHydr_C_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000100; END_IF;
IF bTMR_EngineSpeed_A_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000200; END_IF;
IF bTMR_EngineSpeed_B_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000400; END_IF;
IF bTMR_EngineSpeed_C_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00000800; END_IF;
IF bTMR_InputShaft1_A_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00001000; END_IF;
IF bTMR_InputShaft1_B_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00002000; END_IF;
IF bTMR_InputShaft1_C_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00004000; END_IF;
IF bTMR_ShiftRail_A_Iso THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00008000; END_IF;
IF bAlarm_TMR_Degraded THEN dwDiagnosticWord02_TMR := dwDiagnosticWord02_TMR OR 16#00010000; END_IF;

(* dwAlarmWord_Priority1_Trip: Emergency Shutdown & Hardware Lock *)
dwAlarmWord_Priority1_Trip := 16#00000000;
IF (bEStopChainOK_NC = FALSE) THEN dwAlarmWord_Priority1_Trip := dwAlarmWord_Priority1_Trip OR 16#00000001; END_IF;
IF bAlarm_ClutchPlateTemp_HH THEN dwAlarmWord_Priority1_Trip := dwAlarmWord_Priority1_Trip OR 16#00000002; END_IF;
IF bAlarm_MainHydr_LL THEN dwAlarmWord_Priority1_Trip := dwAlarmWord_Priority1_Trip OR 16#00000004; END_IF;
IF bShiftRailJamFault THEN dwAlarmWord_Priority1_Trip := dwAlarmWord_Priority1_Trip OR 16#00000008; END_IF;
IF bAlarm_ClutchDev1_HH THEN dwAlarmWord_Priority1_Trip := dwAlarmWord_Priority1_Trip OR 16#00000010; END_IF;
IF bAlarm_ClutchDev2_HH THEN dwAlarmWord_Priority1_Trip := dwAlarmWord_Priority1_Trip OR 16#00000020; END_IF;

(* dwAlarmWord_Priority2_Severe: Process Abort & Clutch Disengage *)
dwAlarmWord_Priority2_Severe := 16#00000000;
IF bAlarm_ClutchPlateTemp_H THEN dwAlarmWord_Priority2_Severe := dwAlarmWord_Priority2_Severe OR 16#00000001; END_IF;
IF bAlarm_MainHydr_L THEN dwAlarmWord_Priority2_Severe := dwAlarmWord_Priority2_Severe OR 16#00000002; END_IF;
IF bClutchOverheatWarning THEN dwAlarmWord_Priority2_Severe := dwAlarmWord_Priority2_Severe OR 16#00000004; END_IF;
IF bAlarm_ClutchPlateTemp_ROC THEN dwAlarmWord_Priority2_Severe := dwAlarmWord_Priority2_Severe OR 16#00000008; END_IF;

(* dwAlarmWord_Priority3_Warning: Advisory & Comfort Warnings *)
dwAlarmWord_Priority3_Warning := 16#00000000;
IF bAlarm_LongJerkExceeded THEN dwAlarmWord_Priority3_Warning := dwAlarmWord_Priority3_Warning OR 16#00000001; END_IF;
IF bAlarm_TMR_Degraded THEN dwAlarmWord_Priority3_Warning := dwAlarmWord_Priority3_Warning OR 16#00000002; END_IF;
IF (rEstimatedGVW_Tons > 42.0) THEN dwAlarmWord_Priority3_Warning := dwAlarmWord_Priority3_Warning OR 16#00000004; END_IF;
IF (rVotedRoadGrade_Pct > 8.0) THEN dwAlarmWord_Priority3_Warning := dwAlarmWord_Priority3_Warning OR 16#00000008; END_IF;
IF (rVotedRoadGrade_Pct < -6.0) THEN dwAlarmWord_Priority3_Warning := dwAlarmWord_Priority3_Warning OR 16#00000010; END_IF;"""
    parts.append(phase6)

    # =========================================================================
    # 12. FOOTER
    # =========================================================================
    footer = """END_FUNCTION_BLOCK"""
    parts.append(footer)

    full_st_code = "\n\n".join(parts) + "\n"
    return full_st_code

if __name__ == "__main__":
    code = build_code()
    print(f"Generated Structured Text raw characters: {len(code)}")
