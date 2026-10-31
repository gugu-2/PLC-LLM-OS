# -*- coding: utf-8 -*-
"""
Generator for FB_CommercialVehicle_AMT_DualClutch_KissPointCalibration
Target File: data/swarm_raw/agent_3f820b17.json
"""
import json
import os
import re

def generate_iec_st():
    parts = []
    
    # Header
    parts.append('''FUNCTION_BLOCK FB_CommercialVehicle_AMT_DualClutch_KissPointCalibration
(*
====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - SYNTHETIC IEC 61131-3 DATASET ENGINE
  SYSTEM DESIGNATION: CPS-AUTO-POWERTRAIN-AMT-DUALCLUTCH-V7
  DOMAIN ASSIGNMENT: Automotive & Heavy Commercial Vehicles: 12-Speed Automated Manual Transmission
                     (AMT) Dual Wet Clutch Electrohydraulic Kiss-Point Adaptive Calibration & Shift
                     Rail Servo Pacing
  STANDARDS COMPLIANCE:
    - IEC 61131-3 3rd Edition (Deterministic Industrial Automation Structured Text)
    - ISO 26262-5 / ISO 26262-6:2018 (Road Vehicles - Functional Safety ASIL-D Transmission Control)
    - SAE J1939-71 / SAE J1939-21 (Commercial Vehicle CAN Driveline Communication Application Layer)
    - ISO 14229-1:2020 (Road Vehicles - Unified Diagnostic Services UDS Protocol)
    - ISO 6336 / DIN 3990 (Calculation of Load Capacity of Spur and Helical Gears)
    - DIN 740 / ISO 281 (Transmission Gear Mesh & Rolling Element Bearing Dynamic Life)
    - ISA-18.2 / EEMUA 191 (Management of Alarm Systems for the Process Industries)
    - IEC 61508 / IEC 61511 (Functional Safety SIL-3 Safety Instrumented Functions)
  PERSONA:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Powertrain Tenure)
====================================================================================================
  MATHEMATICAL & CYBER-PHYSICAL POWERTRAIN SYSTEM SPECIFICATION:

  1. HEAVY-DUTY COMMERCIAL VEHICLE 12-SPEED DUAL-CLUTCH TRANSMISSION KINEMATICS:
     Heavy-duty commercial freight tractors (Class 8, Gross Combination Weight GCW up to 44,000 kg)
     demand ultra-high torque transmission capability (up to 3,500 Nm peak engine torque at 1,000 -
     1,400 RPM, redline 2,500 RPM) while eliminating tractive torque interruption during gear
     transitions on steep highway inclines.
     The driveline utilizes a dual-clutch transmission (DCT) architecture comprising two concentric
     transmission input shafts:
       - Clutch 1 (C1 - Outer Pack): Powers solid inner transmission input shaft 1 (J_in1 = 0.0850 kg*m^2),
         governing Odd forward gear mesh ratios:
           Gear 1:  i_1  = 14.940
           Gear 3:  i_3  =  8.860
           Gear 5:  i_5  =  5.420
           Gear 7:  i_7  =  3.360
           Gear 9:  i_9  =  2.090
           Gear 11: i_11 =  1.280
       - Clutch 2 (C2 - Inner Pack): Powers hollow outer transmission input shaft 2 (J_in2 = 0.0920 kg*m^2),
         governing Even forward gear mesh ratios and Reverse gears:
           Gear 2:  i_2  = 11.520
           Gear 4:  i_4  =  6.840
           Gear 6:  i_6  =  4.180
           Gear 8:  i_8  =  2.590
           Gear 10: i_10 =  1.610
           Gear 12: i_12 =  1.000 (Direct Drive / High Cruise)
           Reverse 1: i_R1 = 13.820
           Reverse 2: i_R2 = 10.650
     Final drive differential ratio: i_diff = 3.420; Drive axle wheel rolling radius: r_whl = 0.512 m.
     Equivalent vehicle inertia reflected to transmission output shaft:
       J_veh_ref = (M_veh * r_whl^2) / (i_diff^2)
     For a 40-tonne commercial tractor-trailer:
       J_veh_ref = (40000.0 * 0.512^2) / (3.420^2) = 10485.76 / 11.6964 = 896.49 kg*m^2.

  2. DUAL MULTI-PLATE WET CLUTCH ELECTROHYDRAULICS & TRIBOLOGY:
     Each wet clutch pack incorporates alternating steel separator plates and sintered-bronze/carbon
     composite friction plates submerged in circulating automatic transmission fluid (ATF).
     Clutch Pack Dimensions & Mechanical Parameters:
       - Number of active friction interfaces: z_interfaces = 12 (6 dual-sided friction discs)
       - Outer plate friction radius: r_outer = 0.142 m
       - Inner plate friction radius: r_inner = 0.108 m
       - Mean effective friction radius:
           r_mean = (2.0 / 3.0) * (r_outer^3 - r_inner^3) / (r_outer^2 - r_inner^2) = 0.1256 m
       - Net hydraulic apply piston cross-sectional area: A_piston = 0.01850 m^2
       - Piston return diaphragm spring preload: F_preload = 1450.0 N
       - Piston return spring stiffness: k_spring = 85000.0 N/m
       - Piston cushion travel distance to pack clearance take-up: x_cushion = 0.0018 m (1.80 mm)
     Hydraulic Clamping Force Balance:
       F_net(P_c) = max( 0.0, P_c * A_piston - F_preload - k_spring * x_cushion )
     Dynamic Transmitted Friction Torque:
       T_clutch = z_interfaces * mu_effective(v_slip, T_oil, wear) * F_net * r_mean * sgn(omega_e - omega_in)
     where:
       v_slip = |omega_e - omega_in| * r_mean [m/s]
     The boundary-to-hydrodynamic friction coefficient mu_effective is modeled via the extended
     Stribeck curve incorporating oil film thermal thinning:
       mu_effective = (mu_Coulomb + (mu_Static - mu_Coulomb) * exp(-(v_slip / v_Stribeck)^gamma_stribeck)
                      + sigma_visc * v_slip) * f_temp(T_oil) * f_wear(W_cum)

  3. DYNAMIC ADAPTIVE KISS-POINT CALIBRATION & THERMAL COMPENSATION:
     The kiss-point (touch-point / bite-point) P_kiss defines the critical electrohydraulic apply
     pressure at which the clutch piston completely traverses cushion clearance, overcomes spring
     counter-forces, and establishes initial frictional contact transmitting micro-torque:
       T_clutch >= 15.0 Nm.
     Micro-touch point detection criteria during active vehicle calibration routines:
       Condition 1: Engine closed-loop idle speed droop: Delta_omega_e = omega_e_idle - omega_e >= 25.0 RPM
       Condition 2: Engine ECU internal fuel injection torque reaction: Delta_T_e >= 18.5 Nm
       Condition 3: Transmission input shaft rotational acceleration: d(omega_in)/dt >= 50.0 rad/s^2
     ATF Hydraulic Oil Viscosity Temperature Compensation:
     ATF dynamic viscosity varies nonlinearly with oil temperature T_oil in [-20.0, 120.0] deg C
     according to the Vogel-Eyring formulation:
       eta_oil(T_oil) = eta_0 * exp( B_vogel / (T_oil + C_vogel) )
     Because hydraulic valve spool discharge flow, seal lip friction, and return spring steel modulus
     shift with bulk oil temperature, the calibrated kiss-point pressure requires dynamic compensation:
       P_kiss_comp(T_oil) = P_kiss_base + k_temp1 * (T_oil - T_ref) + k_temp2 * (T_oil - T_ref)^2
     where T_ref = 80.0 deg C, k_temp1 = -0.0125 bar/deg C, k_temp2 = 0.000085 bar/(deg C)^2.
     Clutch Plate Friction Degradation & Wear Adaptation:
     Cumulative frictional slip dissipation energy:
       W_cum = Integral_{0}^{t} ( T_clutch(tau) * |omega_e(tau) - omega_in(tau)| ) dtau  [MJ]
     Degradation tracking updates the base kiss-point through a recursive exponential smoothing filter:
       P_kiss_base[k] = P_kiss_base[k-1] + alpha_adapt * (P_detected - P_kiss_base[k-1])
     Subject to hard safety adaptation bounds: |P_kiss_base[k] - P_kiss_nominal| <= 2.50 bar.

  4. SYNCHRONOUS SHIFT RAIL ELECTROHYDRAULIC SERVO PACING:
     Mechanical gear engagement is commanded across 4 independent dual-acting hydraulic shift rails:
       - Shift Rail 1: Gears 1 and 3 (Inner Shaft 1)
       - Shift Rail 2: Gears 5 and 7 (Inner Shaft 1)
       - Shift Rail 3: Gears 2, 4 and Reverse (Outer Shaft 2)
       - Shift Rail 4: Gears 6, 8, 10 and 12 (Outer Shaft 2)
     Each shift rail is equipped with a high-resolution linear LVDT position sensor:
       Stroke range: -25.00 mm to +25.00 mm (+/- 0.05 mm accuracy).
       Neutral position: 0.00 mm (+/- 0.25 mm deadband detent).
       Positive engagement (Gear A): +18.00 mm (+/- 0.35 mm detent lock).
       Negative engagement (Gear B): -18.00 mm (+/- 0.35 mm detent lock).
     Electrohydraulic Servo Pacing operates across a 4-phase kinematic trajectory:
       Phase 1 (Rapid Free-Travel Pre-Stroke): Slew rate commanded at max hydraulic flow (up to 120 mm/s)
               from 0.00 mm to synchronizer baulk cone touch position (+/- 12.20 mm).
       Phase 2 (Baulk Cone Synchronization): Controlled proportional force (F_sync = 1,850 N to 2,400 N)
               applied to synchronizer cone friction surfaces until speed differential across dog sleeve
               decays to zero: |omega_sync - omega_gear| <= 20.0 RPM.
       Phase 3 (Tooth Chamfer Unblocking Dip): Force reduced dynamically to 650 N for 35 ms to permit
               dog teeth to smoothly index through baulk ring chamfer gaps without acoustic clashing.
       Phase 4 (Positive Detent Engagement): Full hydraulic stroke driven to +/- 18.00 mm, locking
               the spring-loaded mechanical ball detent into the rail detent notch.

  5. POWER-SHIFT OVERLAPPING CROSS-FILL TORQUE HANDOFF:
     During an automated powershift transition (e.g. Gear 3 Odd -> Gear 4 Even), uninterrupted
     tractive torque delivery is sustained by dynamically cross-filling clutch hydraulic pressures:
       T_driveline(t) = i_offgoing * T_c_off(t) + i_oncoming * T_c_on(t)
     Four-stage overlapping hydraulic cross-fill sequence:
       Stage A (Oncoming Pre-Fill & Cushion Prime): Oncoming clutch pre-charged at P_boost = 3.50 bar
               for 65 ms to purge air and stroke piston, then reduced to hold at (P_kiss - 0.20 bar).
       Stage B (Torque Phase Handoff): Offgoing clutch pressure ramps down while oncoming clutch
               pressure ramps up linearly over duration t_torque = 110 ms:
                 T_c_off(t) = T_demand * (1.0 - t / t_torque)
                 T_c_on(t)  = T_demand * (t / t_torque) * (i_offgoing / i_oncoming)
       Stage C (Inertia Phase Speed Pull-Down): With oncoming clutch carrying full engine torque,
               engine ECU intervenes via J1939 CAN TSC1 to retard fueling while oncoming clutch pressure
               is elevated to pull engine speed down to synchronous gear speed:
                 d(omega_e)/dt = (T_engine - T_c_on) / J_engine
       Stage D (Lockup & Exhaust): Once slip speed |omega_e - omega_in_target| <= 15.0 RPM for 30 ms,
               oncoming clutch pressure is driven to full line lockup (P_lock = 18.5 bar, safety factor 1.45x),
               offgoing clutch is vented to 0.0 bar, and offgoing shift rail is retracted to Neutral.
       Total shift duration is strictly constrained: t_shift <= 0.350 s.

  6. ACTIVE DRIVELINE ANTI-JERK TORSIONAL COMPLIANCE DAMPING:
     Long-wheelbase commercial vehicle drivelines exhibit high torsional compliance in the prop-shaft
     and drive axle half-shafts (equivalent torsional stiffness k_prop = 8,500 Nm/rad, damping
     c_prop = 48.0 Nms/rad). Sudden torque handoffs excite driveline resonance (chassis shuffle at
     f_res = 2.50 to 3.80 Hz), inducing harsh cab pitching and driveline fatigue.
     An active anti-jerk state observer estimates driveline twist angle Delta_theta_d and generates
     dynamic damping torque intervention via high-speed J1939 engine CAN torque modulation:
       Delta_T_anti_jerk = -K_prop_aj * (omega_trans_out - omega_whl * i_diff)
                          - K_deriv_aj * d(omega_trans_out - omega_whl * i_diff)/dt

  7. 16x16 CYBER-PHYSICAL DISCRETE STATE-SPACE MODEL:
     Discrete-time state equations: x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k].
     State Vector x in R^16:
       x[1]:  omega_e        - Engine crankshaft rotational speed [rad/s]
       x[2]:  omega_in1      - Transmission input shaft 1 speed (Odd gears) [rad/s]
       x[3]:  omega_in2      - Transmission input shaft 2 speed (Even gears) [rad/s]
       x[4]:  omega_lay      - Countershaft / layshaft rotational speed [rad/s]
       x[5]:  omega_out      - Transmission output shaft rotational speed [rad/s]
       x[6]:  Delta_theta_d  - Prop-shaft torsional compliance twist angle [rad]
       x[7]:  omega_whl      - Drive axle road wheel rotational speed [rad/s]
       x[8]:  v_veh          - Vehicle forward longitudinal velocity [m/s]
       x[9]:  P_c1           - Clutch 1 hydraulic apply chamber pressure [bar]
       x[10]: P_c2           - Clutch 2 hydraulic apply chamber pressure [bar]
       x[11]: x_spool1       - Clutch 1 proportional valve spool position [mm]
       x[12]: x_spool2       - Clutch 2 proportional valve spool position [mm]
       x[13]: y_rail_odd     - Active Odd shift rail LVDT position stroke [mm]
       x[14]: y_rail_even    - Active Even shift rail LVDT position stroke [mm]
       x[15]: T_clutch1      - Clutch 1 multi-plate pack bulk temperature [deg C]
       x[16]: T_clutch2      - Clutch 2 multi-plate pack bulk temperature [deg C]
     Control Input Vector u in R^8:
       u[1]:  I_sol1         - Clutch 1 proportional pressure valve current demand [mA]
       u[2]:  I_sol2         - Clutch 2 proportional pressure valve current demand [mA]
       u[3]:  u_rail_odd     - Odd shift rail directional servo valve command [%]
       u[4]:  u_rail_even    - Even shift rail directional servo valve command [%]
       u[5]:  T_e_req        - Engine CAN J1939 torque intervention command [Nm]
       u[6]:  Q_cool_cmd     - Wet clutch lubricating and cooling oil flow valve [%]
       u[7]:  D_line_pmp     - Main hydraulic line pressure pump duty cycle [%]
       u[8]:  T_anti_jerk    - Active driveline anti-jerk damping torque correction [Nm]

  8. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) FORMULATION:
     Unrolled quadratic objective minimization over receding prediction horizon:
       min_u J = 0.5 * sum_{i=1..16} Q_cost[i] * (x[i] - x_ref[i])^2
               + 0.5 * sum_{j=1..8}  R_cost[j] * (u[j])^2
               + 0.5 * sum_{j=1..8}  Rd_cost[j] * (u[j] - u_prev[j])^2
               + 0.5 * sum_{i=1..16} P_term[i] * (x_next[i] - x_ref[i])^2
               + J_barrier_thermal + J_barrier_shift_time
     Projected Gradient Descent (PGD) enforces hard actuator current limits (0 to 1,500 mA),
     maximum pressure slew rates (<= 65 bar/s), and rail velocity constraints.

  9. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE:
     Mission-critical powertrain sensory channels operate triplicated transducers:
       - Engine Speed: CAN J1939 EEC1 (Ch A), Crank Variable Reluctance (Ch B), Flywheel Hall (Ch C)
       - Input Shaft 1 Speed: Hall Pickups Ch A, Ch B, Ch C
       - Input Shaft 2 Speed: Hall Pickups Ch A, Ch B, Ch C
       - Main Line Hydraulic Pressure: Piezoresistive Transducers Ch A, Ch B, Ch C
     Voting Engine executes median sorting across healthy channels, applies discrepancy qualification
     timers (tau_discrep = 0.25 s), degrades bumplessly to 2-channel average, and latches alarms.

  10. 12-STAGE COMPREHENSIVE POWERTRAIN OPERATIONAL FINITE STATE MACHINE:
      State 0:  Transmission Power-On Self-Test (POST & Hardware Health Diagnostics)
      State 1:  Hydraulic Pressure Accumulator Charging & Main Line Priming
      State 2:  Static Kiss-Point Self-Learn Routine (Active Micro-Slip Calibration)
      State 3:  Pre-Select 1st Gear Shift Rail Engagement & Dog Detent Lock
      State 4:  Launch Clutch Modulated Engagement & Dynamic Vehicle Creep
      State 5:  Steady-State In-Gear Cruise & Efficiency Optimization
      State 6:  Shift Pre-Select Next Target Gear & Synchronizer Baulk Pacing
      State 7:  Overlapping Cross-Fill Power-Shift Torque Handoff
      State 8:  Off-Going Shift Rail Neutral Release & Verification
      State 9:  Dynamic Friction Adaption & Flash Memory Storage
      State 10: Hill-Hold Anti-Rollback Standstill Brake Coordination
      State 11: Emergency Neutral Dump & Hydraulic Clutch Vent Trip
====================================================================================================
*)
''')
    
    # VAR_INPUT
    parts.append('''VAR_INPUT
    (* ========================================================================================= *)
    (* 1. SYSTEM CONTROL, PERMISSIVES & DRIVER CABIN COMMANDS                                    *)
    (* ========================================================================================= *)
    bMasterAutomationEnable         : BOOL;         (* Master transmission control unit permissive [active HIGH] *)
    bEStopEmergencyTrip             : BOOL;         (* SIL-3 hardwired emergency safety circuit [active LOW: FALSE=Trip] *)
    bOperatorDrivePermissive        : BOOL;         (* Cabin shift selector in D (Drive) permissive *)
    bBrakePedalDepressed            : BOOL;         (* Foundation service brake active brake pedal switch *)
    bParkBrakeReleased              : BOOL;         (* Pneumatic parking emergency spring brake released *)
    bHillHoldRequest                : BOOL;         (* Electronic braking system (EBS) hill-start assist request *)
    bManualOverrideEnable           : BOOL;         (* Diagnostic manual calibration routine permissive *)
    bAlarmAcknowledgeReset          : BOOL;         (* ISA-18.2 master alarm acknowledge and trip reset push button *)

    (* ========================================================================================= *)
    (* 2. TRIPLE MODULAR REDUNDANT (2oo3 TMR) PRIMARY POWERTRAIN SENSORS                         *)
    (* ========================================================================================= *)
    (* Engine Crankshaft Rotational Speed Transducers [rpm] *)
    rEngineSpeed_ChA                : REAL;         (* Engine crankshaft speed from J1939 EEC1 CAN broadcast [rpm] *)
    rEngineSpeed_ChB                : REAL;         (* Engine crankshaft variable reluctance hardware sensor [rpm] *)
    rEngineSpeed_ChC                : REAL;         (* Engine flywheel ring gear magnetic hall sensor [rpm] *)

    (* Transmission Input Shaft 1 Speed Transducers (Odd Gears) [rpm] *)
    rInputShaft1Speed_ChA           : REAL;         (* Input shaft 1 solid inner shaft hall sensor A [rpm] *)
    rInputShaft1Speed_ChB           : REAL;         (* Input shaft 1 solid inner shaft hall sensor B [rpm] *)
    rInputShaft1Speed_ChC           : REAL;         (* Input shaft 1 solid inner shaft hall sensor C [rpm] *)

    (* Transmission Input Shaft 2 Speed Transducers (Even Gears) [rpm] *)
    rInputShaft2Speed_ChA           : REAL;         (* Input shaft 2 hollow outer shaft hall sensor A [rpm] *)
    rInputShaft2Speed_ChB           : REAL;         (* Input shaft 2 hollow outer shaft hall sensor B [rpm] *)
    rInputShaft2Speed_ChC           : REAL;         (* Input shaft 2 hollow outer shaft hall sensor C [rpm] *)

    (* Electrohydraulic Main Line Pressure Transducers [bar] *)
    rMainLinePressure_ChA           : REAL;         (* Hydraulic line pressure piezoresistive transducer A [bar] *)
    rMainLinePressure_ChB           : REAL;         (* Hydraulic line pressure piezoresistive transducer B [bar] *)
    rMainLinePressure_ChC           : REAL;         (* Hydraulic line pressure piezoresistive transducer C [bar] *)

    (* ========================================================================================= *)
    (* 3. AUXILIARY THERMODYNAMIC, HYDRAULIC & POWERTRAIN SENSORS                                *)
    (* ========================================================================================= *)
    rClutch1ChamberPressure         : REAL;         (* Clutch 1 odd wet pack apply cylinder pressure [bar] *)
    rClutch2ChamberPressure         : REAL;         (* Clutch 2 even wet pack apply cylinder pressure [bar] *)
    rClutchOilSumpTemp              : REAL;         (* Transmission hydraulic oil sump bulk temperature [deg C] *)
    rClutch1PlateTemp               : REAL;         (* Clutch 1 embedded thermistor multi-plate pack temperature [deg C] *)
    rClutch2PlateTemp               : REAL;         (* Clutch 2 embedded thermistor multi-plate pack temperature [deg C] *)
    rEngineTorqueActual             : REAL;         (* Actual indicated flywheel engine torque from EEC1 CAN [Nm] *)
    rAcceleratorPedalPos            : REAL;         (* Driver accelerator throttle pedal demand percentage [%] *)
    rVehicleSpeedKmh                : REAL;         (* Tachograph output drive axle vehicle speed [km/h] *)
    rRoadGradientGrade              : REAL;         (* Inclinometer chassis longitudinal road slope grade [%] *)

    (* ========================================================================================= *)
    (* 4. SHIFT RAIL LINEAR DISPLACEMENT SENSORS (LVDT / HALL) [mm]                              *)
    (* ========================================================================================= *)
    rShiftRail1Pos_LVDT             : REAL;         (* Shift Rail 1 (1st/3rd gears) linear displacement stroke [mm] *)
    rShiftRail2Pos_LVDT             : REAL;         (* Shift Rail 2 (5th/7th gears) linear displacement stroke [mm] *)
    rShiftRail3Pos_LVDT             : REAL;         (* Shift Rail 3 (2nd/4th/Rev gears) linear displacement stroke [mm] *)
    rShiftRail4Pos_LVDT             : REAL;         (* Shift Rail 4 (6th/8th/10th/12th gears) linear stroke [mm] *)
    nTargetGearRequest              : INT;          (* Transmission supervisory controller requested target gear [-] *)
END_VAR
''')
    
    # VAR_OUTPUT
    parts.append('''VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. ELECTROHYDRAULIC CLUTCH & SHIFT RAIL ACTUATOR COMMANDS                                 *)
    (* ========================================================================================= *)
    rClutch1CurrentCommand_mA       : REAL;         (* Clutch 1 proportional pressure valve solenoid current [mA] *)
    rClutch2CurrentCommand_mA       : REAL;         (* Clutch 2 proportional pressure valve solenoid current [mA] *)
    rClutch1PressureSetpoint_bar    : REAL;         (* Clutch 1 target hydraulic apply pressure [bar] *)
    rClutch2PressureSetpoint_bar    : REAL;         (* Clutch 2 target hydraulic apply pressure [bar] *)
    rShiftRail1ServoCmd_Pct         : REAL;         (* Shift Rail 1 proportional directional valve servo output [%] *)
    rShiftRail2ServoCmd_Pct         : REAL;         (* Shift Rail 2 proportional directional valve servo output [%] *)
    rShiftRail3ServoCmd_Pct         : REAL;         (* Shift Rail 3 proportional directional valve servo output [%] *)
    rShiftRail4ServoCmd_Pct         : REAL;         (* Shift Rail 4 proportional directional valve servo output [%] *)
    rEngineTorqueOverride_Nm        : REAL;         (* CAN TSC1 engine torque limit intervention demand [Nm] *)
    rAntiJerkDampingTorque_Nm       : REAL;         (* Active driveline shuffle anti-jerk correction torque [Nm] *)
    rClutchCoolingValveCmd_Pct      : REAL;         (* Wet clutch lubricating and cooling oil flow valve [%] *)
    rLinePressurePumpCmd_Pct        : REAL;         (* Hydraulic accumulator charging pump duty cycle [%] *)
    bClutch1VentValveOpen           : BOOL;         (* Fast-acting safety dump solenoid valve Clutch 1 [active HIGH] *)
    bClutch2VentValveOpen           : BOOL;         (* Fast-acting safety dump solenoid valve Clutch 2 [active HIGH] *)

    (* ========================================================================================= *)
    (* 2. POWERTRAIN STATUS & CYBER-PHYSICAL STATE ESTIMATES                                     *)
    (* ========================================================================================= *)
    bTransmissionInGear             : BOOL;         (* Positive mechanical gear engagement locked in detent *)
    bPowerShiftActive               : BOOL;         (* Dual clutch overlapping cross-fill power shift actively executing *)
    bKissPointCalibrated            : BOOL;         (* Dual wet clutch kiss point calibration valid and active *)
    bEmergencyNeutralActive         : BOOL;         (* Transmission forced into safe neutral disengaged state *)
    nCurrentActiveGear              : INT;          (* Currently engaged and locked mechanical gear index [-] *)
    nPreselectedTargetGear          : INT;          (* Pre-synchronized pending oncoming gear index [-] *)
    rCalibratedKissPressure_C1      : REAL;         (* Current adapted kiss point pressure for Clutch 1 [bar] *)
    rCalibratedKissPressure_C2      : REAL;         (* Current adapted kiss point pressure for Clutch 2 [bar] *)
    rCumulativeWearEnergy_C1_MJ     : REAL;         (* Cumulative frictional thermal dissipation energy Clutch 1 [MJ] *)
    rCumulativeWearEnergy_C2_MJ     : REAL;         (* Cumulative frictional thermal dissipation energy Clutch 2 [MJ] *)
    rClutch1EstimatedTorque_Nm      : REAL;         (* Dynamic observer estimated torque transmitted by Clutch 1 [Nm] *)
    rClutch2EstimatedTorque_Nm      : REAL;         (* Dynamic observer estimated torque transmitted by Clutch 2 [Nm] *)
    rDrivelineTorsionAngle_mrad     : REAL;         (* Observer estimated driveshaft torsional compliance twist [mrad] *)

    (* ========================================================================================= *)
    (* 3. ISA-88 RECIPE / ISA-18.2 ALARM & DIAGNOSTIC STATUS WORDS                               *)
    (* ========================================================================================= *)
    wTransmissionFSMState           : WORD;         (* 16-bit packed operational finite state machine status word *)
    dwAlarmWord_Trips               : DWORD;        (* ISA-18.2 Priority 1 Bit-packed Critical Emergency Trips *)
    dwAlarmWord_Severe              : DWORD;        (* ISA-18.2 Priority 2 Bit-packed Process Deviation Alarms *)
    dwAlarmWord_Warning             : DWORD;        (* ISA-18.2 Priority 3 Bit-packed Advisory & Discrepancy Warnings *)
    wTMR_DiscrepancyStatus          : WORD;         (* 2oo3 voting discrepancy and degradation status word *)
    wShiftRailStatusWord            : WORD;         (* Bit-packed mechanical dog clutch and shift rail position word *)
END_VAR
''')
    
    # VAR
    parts.append('''VAR
    (* ========================================================================================= *)
    (* 1. THERMODYNAMIC, KINEMATIC & ELECTROHYDRAULIC PHYSICAL CONSTANTS                         *)
    (* ========================================================================================= *)
    rConst_ScanDeltaTime            : REAL := 0.010;        (* Periodic cyclic execution scan time dt = 10 ms [s] *)
    rConst_EngineInertia            : REAL := 3.8500;       (* Diesel engine crankshaft rotational inertia [kg*m^2] *)
    rConst_InputShaft1Inertia       : REAL := 0.0850;       (* Solid inner transmission shaft 1 inertia [kg*m^2] *)
    rConst_InputShaft2Inertia       : REAL := 0.0920;       (* Hollow outer transmission shaft 2 inertia [kg*m^2] *)
    rConst_LayshaftInertia          : REAL := 0.1450;       (* Countershaft rotational inertia [kg*m^2] *)
    rConst_OutputShaftInertia       : REAL := 0.2200;       (* Output mainshaft rotational inertia [kg*m^2] *)
    rConst_VehicleMassKG            : REAL := 40000.0;      (* Nominal commercial vehicle gross combination weight [kg] *)
    rConst_WheelRadiusM             : REAL := 0.5120;       (* Drive axle tire loaded dynamic rolling radius [m] *)
    rConst_FinalDriveRatio          : REAL := 3.4200;       (* Drive axle differential crown-wheel-pinion gear ratio *)
    rConst_DrivelineStiffness       : REAL := 8500.0;       (* Prop-shaft equivalent torsional spring stiffness [Nm/rad] *)
    rConst_DrivelineDamping         : REAL := 48.00;        (* Prop-shaft equivalent torsional viscous damping [Nms/rad] *)
    rConst_ClutchPistonArea         : REAL := 0.01850;      (* Hydraulic apply piston cross-sectional area [m^2] *)
    rConst_ClutchMeanRadius         : REAL := 0.1256;       (* Wet multi-plate effective mean friction radius [m] *)
    rConst_ClutchFrictionPlates     : REAL := 12.0;         (* Total active friction interfaces per clutch pack *)
    rConst_ReturnSpringPreload      : REAL := 1450.0;       (* Piston return diaphragm spring preload force [N] *)
    rConst_ReturnSpringRate         : REAL := 85000.0;      (* Piston return diaphragm spring linear rate [N/m] *)
    rConst_PistonCushionTravel      : REAL := 0.00180;      (* Piston air gap cushion clearance stroke [m] *)
    rConst_BaseFrictionCoeff        : REAL := 0.1380;       (* Sintered bronze/carbon wet friction baseline coefficient *)
    rConst_OilRefTempDegC           : REAL := 80.0;         (* Reference ATF calibration oil temperature [deg C] *)
    rConst_TempCoeffAlpha1          : REAL := -0.01250;     (* First-order kiss-point temperature compensation [bar/C] *)
    rConst_TempCoeffAlpha2          : REAL := 0.000085;     (* Second-order kiss-point temperature compensation [bar/C^2] *)
    rConst_WearDegradationFactor    : REAL := 0.000045;     (* Frictional wear coefficient per megajoule slip [1/MJ] *)

    (* 12 Forward Transmission Gear Ratios & 2 Reverse Ratios *)
    arrGearRatios                   : ARRAY[1..14] OF REAL := [
        14.940, 11.520,  8.860,  6.840,  5.420,  4.180,
         3.360,  2.590,  2.090,  1.610,  1.280,  1.000,
        13.820, 10.650
    ];

    (* ========================================================================================= *)
    (* 2. DISCRETE STATE-SPACE MATRICES (16x16 SYSTEM: x[k+1] = A*x[k] + B*u[k])                 *)
    (* States x[1..16]:                                                                          *)
    (*   x[1]:  omega_e       - Engine crankshaft speed [rad/s]                                  *)
    (*   x[2]:  omega_in1     - Inner input shaft 1 speed [rad/s]                                *)
    (*   x[3]:  omega_in2     - Outer input shaft 2 speed [rad/s]                                *)
    (*   x[4]:  omega_lay     - Countershaft speed [rad/s]                                       *)
    (*   x[5]:  omega_out     - Transmission output shaft speed [rad/s]                          *)
    (*   x[6]:  Delta_theta_d - Prop-shaft torsional twist angle [rad]                           *)
    (*   x[7]:  omega_whl     - Road wheel speed [rad/s]                                         *)
    (*   x[8]:  v_veh         - Vehicle forward longitudinal velocity [m/s]                      *)
    (*   x[9]:  P_c1          - Clutch 1 apply hydraulic pressure [bar]                          *)
    (*   x[10]: P_c2          - Clutch 2 apply hydraulic pressure [bar]                          *)
    (*   x[11]: x_spool1      - Clutch 1 valve spool position [mm]                               *)
    (*   x[12]: x_spool2      - Clutch 2 valve spool position [mm]                               *)
    (*   x[13]: y_rail_odd    - Active Odd shift rail stroke [mm]                                *)
    (*   x[14]: y_rail_even   - Active Even shift rail stroke [mm]                               *)
    (*   x[15]: T_clutch1     - Clutch 1 multi-plate bulk temperature [deg C]                    *)
    (*   x[16]: T_clutch2     - Clutch 2 multi-plate bulk temperature [deg C]                    *)
    (* Inputs u[1..8]:                                                                           *)
    (*   u[1]:  I_sol1        - Clutch 1 solenoid current [mA]                                   *)
    (*   u[2]:  I_sol2        - Clutch 2 solenoid current [mA]                                   *)
    (*   u[3]:  u_rail_odd    - Odd shift rail servo command [%]                                 *)
    (*   u[4]:  u_rail_even   - Even shift rail servo command [%]                                *)
    (*   u[5]:  T_e_req       - Engine CAN torque intervention [Nm]                              *)
    (*   u[6]:  Q_cool_cmd    - Clutch cooling oil flow valve [%]                                *)
    (*   u[7]:  D_line_pmp    - Main line pump duty cycle [%]                                    *)
    (*   u[8]:  T_anti_jerk   - Active anti-jerk damping torque [Nm]                             *)
    (* ========================================================================================= *)
    matA                            : ARRAY[1..16, 1..16] OF REAL; (* Discrete state transition matrix A *)
    matB                            : ARRAY[1..16, 1..8] OF REAL;  (* Discrete input coupling matrix B *)
    matC                            : ARRAY[1..16, 1..16] OF REAL; (* Discrete measurement observation matrix C *)
    matD                            : ARRAY[1..16, 1..8] OF REAL;  (* Direct feedthrough matrix D *)
    matL                            : ARRAY[1..16, 1..16] OF REAL; (* Steady-state observer Luenberger gain L *)

    vecState_x                      : ARRAY[1..16] OF REAL;        (* Current estimated state vector x[k] *)
    vecState_x_next                 : ARRAY[1..16] OF REAL;        (* Predicted state vector x[k+1] *)
    vecStateRef                     : ARRAY[1..16] OF REAL;        (* Reference trajectory state setpoints *)
    vecControl_u                    : ARRAY[1..8] OF REAL;         (* Active control command vector u[k] *)
    vecControl_u_prev               : ARRAY[1..8] OF REAL;         (* Preceding scan control command u[k-1] *)
    vecMeasurement_z                : ARRAY[1..16] OF REAL;        (* Sensor feedback measurement vector z[k] *)
    vecInnovation_e                 : ARRAY[1..16] OF REAL;        (* Observer innovation residual e[k] *)

    (* ========================================================================================= *)
    (* 3. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION                           *)
    (* ========================================================================================= *)
    vecQ_Cost                       : ARRAY[1..16] OF REAL;        (* State error quadratic penalty weights Q *)
    vecR_Cost                       : ARRAY[1..8] OF REAL;         (* Actuator effort quadratic weights R *)
    vecRd_Cost                      : ARRAY[1..8] OF REAL;         (* Actuator slew rate penalty weights Rd *)
    vecP_Cost                       : ARRAY[1..16] OF REAL;        (* Terminal state penalty weights P *)
    vecMpcGradient                  : ARRAY[1..8] OF REAL;         (* Cost function gradient vector *)
    vecDeltaU                       : ARRAY[1..8] OF REAL;         (* Actuator optimal increment per scan *)
    vecU_Min                        : ARRAY[1..8] OF REAL;         (* Lower saturation bounds *)
    vecU_Max                        : ARRAY[1..8] OF REAL;         (* Upper saturation bounds *)
    vecDeltaU_Max                   : ARRAY[1..8] OF REAL;         (* Maximum allowable rate of change per scan *)
    rMpcStepSize                    : REAL := 0.00185;             (* Projected gradient descent learning step *)
    iMpcInnerLoops                  : INT := 8;                    (* Unrolled solver iteration count *)

    (* ========================================================================================= *)
    (* 4. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING CHANNELS & FAULT ACCUMULATORS              *)
    (* ========================================================================================= *)
    (* Engine Crankshaft Speed Transducers (A, B, C) *)
    rEngineSpeed_Voted              : REAL := 600.0;               (* Consolidated 2oo3 engine speed [rpm] *)
    bEngineSpeed_ChA_Healthy        : BOOL := TRUE;
    bEngineSpeed_ChB_Healthy        : BOOL := TRUE;
    bEngineSpeed_ChC_Healthy        : BOOL := TRUE;
    tEngineSpeed_ChA_FaultTimer     : REAL := 0.0;
    tEngineSpeed_ChB_FaultTimer     : REAL := 0.0;
    tEngineSpeed_ChC_FaultTimer     : REAL := 0.0;
    rEngineSpeed_TmrThresh          : REAL := 75.0;                (* Maximum allowable deviation [rpm] *)

    (* Input Shaft 1 Speed Transducers (A, B, C) *)
    rShaft1Speed_Voted              : REAL := 0.0;                 (* Consolidated 2oo3 shaft 1 speed [rpm] *)
    bShaft1Speed_ChA_Healthy        : BOOL := TRUE;
    bShaft1Speed_ChB_Healthy        : BOOL := TRUE;
    bShaft1Speed_ChC_Healthy        : BOOL := TRUE;
    tShaft1Speed_ChA_FaultTimer     : REAL := 0.0;
    tShaft1Speed_ChB_FaultTimer     : REAL := 0.0;
    tShaft1Speed_ChC_FaultTimer     : REAL := 0.0;
    rShaft1Speed_TmrThresh          : REAL := 60.0;                (* Maximum allowable deviation [rpm] *)

    (* Input Shaft 2 Speed Transducers (A, B, C) *)
    rShaft2Speed_Voted              : REAL := 0.0;                 (* Consolidated 2oo3 shaft 2 speed [rpm] *)
    bShaft2Speed_ChA_Healthy        : BOOL := TRUE;
    bShaft2Speed_ChB_Healthy        : BOOL := TRUE;
    bShaft2Speed_ChC_Healthy        : BOOL := TRUE;
    tShaft2Speed_ChA_FaultTimer     : REAL := 0.0;
    tShaft2Speed_ChB_FaultTimer     : REAL := 0.0;
    tShaft2Speed_ChC_FaultTimer     : REAL := 0.0;
    rShaft2Speed_TmrThresh          : REAL := 60.0;                (* Maximum allowable deviation [rpm] *)

    (* Main Hydraulic Line Pressure Transducers (A, B, C) *)
    rMainLinePressure_Voted         : REAL := 45.0;                (* Consolidated 2oo3 line pressure [bar] *)
    bLinePress_ChA_Healthy          : BOOL := TRUE;
    bLinePress_ChB_Healthy          : BOOL := TRUE;
    bLinePress_ChC_Healthy          : BOOL := TRUE;
    tLinePress_ChA_FaultTimer       : REAL := 0.0;
    tLinePress_ChB_FaultTimer       : REAL := 0.0;
    tLinePress_ChC_FaultTimer       : REAL := 0.0;
    rLinePress_TmrThresh            : REAL := 3.50;                (* Maximum allowable deviation [bar] *)

    rTmrPersistenceLimit            : REAL := 0.250;               (* Discrepancy qualification debounce [s] *)

    (* ========================================================================================= *)
    (* 5. DYNAMIC ADAPTIVE KISS-POINT CALIBRATION REGISTERS                                      *)
    (* ========================================================================================= *)
    rKissPointPressure_C1_Base      : REAL := 4.250;               (* Base learned kiss-point Clutch 1 at 80C [bar] *)
    rKissPointPressure_C2_Base      : REAL := 4.280;               (* Base learned kiss-point Clutch 2 at 80C [bar] *)
    rKissPointPressure_C1_Comp      : REAL := 4.250;               (* Temperature-compensated kiss-point C1 [bar] *)
    rKissPointPressure_C2_Comp      : REAL := 4.280;               (* Temperature-compensated kiss-point C2 [bar] *)
    rKissPointCurrent_C1_mA         : REAL := 425.0;               (* Learned solenoid current C1 [mA] *)
    rKissPointCurrent_C2_mA         : REAL := 428.0;               (* Learned solenoid current C2 [mA] *)
    rAdaptationGainAlpha            : REAL := 0.0850;              (* Recursive exponential smoothing gain *)
    rMicroTouchDroopThreshold_RPM   : REAL := 25.0;                (* Engine droop threshold for bite point [rpm] *)
    rMicroTouchTorqueThresh_Nm      : REAL := 18.50;               (* Engine reaction torque threshold [Nm] *)
    rInputShaftAccelThresh_RadS2    : REAL := 50.00;               (* Shaft acceleration bite threshold [rad/s^2] *)
    bCalibrationInProgress          : BOOL := FALSE;               (* Kiss-point calibration cycle active *)
    bCalibrationComplete_C1         : BOOL := FALSE;               (* Clutch 1 kiss point calibrated *)
    bCalibrationComplete_C2         : BOOL := FALSE;               (* Clutch 2 kiss point calibrated *)
    rCalibrationRampRate_BarS       : REAL := 0.750;               (* Pressure ramp speed during learning [bar/s] *)
    rCalibratedRampPressure         : REAL := 0.0;                 (* Current sweep pressure register [bar] *)
    tCalibrationDwellTimer          : REAL := 0.0;                 (* Calibration step timer [s] *)

    (* ========================================================================================= *)
    (* 6. SYNCHRONOUS SHIFT RAIL SERVO PACING REGISTERS                                          *)
    (* ========================================================================================= *)
    arrRailPosition_Actual          : ARRAY[1..4] OF REAL;         (* Measured rail positions 1..4 [mm] *)
    arrRailPosition_Target          : ARRAY[1..4] OF REAL;         (* Target commanded rail positions [mm] *)
    arrRailVelocity_Actual          : ARRAY[1..4] OF REAL;         (* Differentiated rail velocities [mm/s] *)
    arrRailServoOutput              : ARRAY[1..4] OF REAL;         (* Proportional servo valve commands [%] *)
    arrRailInDetentLock             : ARRAY[1..4] OF BOOL;         (* Ball detent positive lock confirmed *)
    rRailKp                         : REAL := 8.50;                (* Rail position servo proportional gain *)
    rRailKd                         : REAL := 0.45;                (* Rail position servo derivative gain *)
    rRailKi                         : REAL := 0.02;                (* Rail position servo integral gain *)
    arrRailIntegralError            : ARRAY[1..4] OF REAL;         (* Rail position integral accumulator *)
    rBaulkSyncForceN                : REAL := 1850.0;              (* Synchronizer baulk cone clamping force [N] *)
    rToothChamferDipForceN          : REAL := 650.0;               (* Unblocking chamfer dip force [N] *)
    tChamferDipTimer                : REAL := 0.0;                 (* Unblocking phase duration timer [s] *)
    iActivePacingPhase              : INT := 0;                    (* Active 4-phase pacing index (1..4) *)

    (* ========================================================================================= *)
    (* 7. ACTIVE DRIVELINE ANTI-JERK DAMPING COMPENSATOR                                         *)
    (* ========================================================================================= *)
    rAntiJerkDampingGainProp        : REAL := 125.0;               (* Proportional damping gain [Nm/(rad/s)] *)
    rAntiJerkDampingGainDeriv       : REAL := 8.50;                (* Derivative damping gain [Nm/(rad/s^2)] *)
    rDrivelineSpeedDeltaFiltered    : REAL := 0.0;                 (* Filtered relative slip speed [rad/s] *)
    rDrivelineSpeedDeltaPrev        : REAL := 0.0;                 (* Preceding scan relative slip [rad/s] *)
    rAntiJerkMaxTorqueClip          : REAL := 350.0;               (* Hard saturation limit on damping torque [Nm] *)

    (* ========================================================================================= *)
    (* 8. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) STEP REGISTERS                         *)
    (* ========================================================================================= *)
    eCurrentState                   : INT := 0;                    (* Active 12-stage FSM step index *)
    eNextState                      : INT := 0;                    (* Next pending sequence step index *)
    tStateDwellTimer                : REAL := 0.0;                 (* Elapsed duration in current state [s] *)
    bStateFirstScan                 : BOOL := TRUE;                (* State transition entry trigger *)
    tPowershiftTimer                : REAL := 0.0;                 (* Power-shift execution stopwatch [s] *)
    tTorquePhaseTimer               : REAL := 0.0;                 (* Cross-fill torque handoff timer [s] *)
    tInertiaPhaseTimer              : REAL := 0.0;                 (* Speed pull-down inertia phase timer [s] *)
    tAccumulatorChargeTimer         : REAL := 0.0;                 (* Line pressure charge timer [s] *)
    tHillHoldTimer                  : REAL := 0.0;                 (* Hill-hold standstill brake timer [s] *)
    tStandstillTimeout              : REAL := 0.0;                 (* Idle timeout in neutral [s] *)
    nTotalPowershiftsCompleted      : DINT := 0;                   (* Lifetime successfully executed power shifts *)

    (* Preset Stage Dwell Thresholds [s] *)
    rTargetDuration_TorquePhase     : REAL := 0.110;               (* Target cross-fill torque phase [s] *)
    rTargetDuration_InertiaPhase    : REAL := 0.180;               (* Target speed matching inertia phase [s] *)
    rTargetDuration_ShiftMax        : REAL := 0.350;               (* Hard maximum shift duration limit [s] *)
    rTargetDuration_Post            : REAL := 0.500;               (* Power-on self-test timeout [s] *)
    rTargetDuration_Charge          : REAL := 2.500;               (* Accumulator initial charge timeout [s] *)

    (* ========================================================================================= *)
    (* 9. ISA-18.2 MULTI-TIER ALARM TRIP POINTS, LIMITS & DEADBANDS                              *)
    (* ========================================================================================= *)
    (* Clutch Plate Bulk Temperature Alarms [deg C] *)
    rAlarmClutchTemp_HH             : REAL := 220.0;               (* Critical clutch overheat emergency trip [deg C] *)
    rAlarmClutchTemp_H              : REAL := 175.0;               (* High clutch temperature warning [deg C] *)
    rDeadband_ClutchTemp            : REAL := 5.0;                 (* Temperature reset hysteresis [deg C] *)

    (* Main Hydraulic Line Pressure Alarms [bar] *)
    rAlarmLinePress_HH              : REAL := 62.0;                (* High-High line overpressure relief trip [bar] *)
    rAlarmLinePress_H               : REAL := 55.0;                (* High line pressure regulation warning [bar] *)
    rAlarmLinePress_L               : REAL := 24.0;                (* Low line pressure warning [bar] *)
    rAlarmLinePress_LL              : REAL := 16.0;                (* Critical line pressure loss trip [bar] *)
    rDeadband_LinePress             : REAL := 1.50;                (* Line pressure reset deadband [bar] *)

    (* Shift Rail Position & Timing Alarms *)
    rAlarmShiftRailTimeoutSec       : REAL := 0.450;               (* Shift rail engagement timeout limit [s] *)
    rAlarmKissPointDriftMaxBar      : REAL := 2.50;                (* Maximum allowable kiss-point drift [bar] *)
    rAlarmMaxSlipDurationSec        : REAL := 1.200;               (* Continuous clutch slip duration limit [s] *)
    tActiveClutchSlipTimer          : REAL := 0.0;                 (* Slip duration accumulator [s] *)

    (* Internal Flags, Iterators & Scratchpad Variables *)
    bMasterFirstScanDone            : BOOL := FALSE;               (* Cold boot memory parameterization flag *)
    nIdx_i                          : INT := 1;                    (* Matrix row index *)
    nIdx_j                          : INT := 1;                    (* Matrix column index *)
    nIdx_k                          : INT := 1;                    (* Matrix inner product index *)
    nMpcLoop                        : INT := 1;                    (* MPC gradient solver loop index *)
    rScratch1                       : REAL := 0.0;                 (* General scratchpad 1 *)
    rScratch2                       : REAL := 0.0;                 (* General scratchpad 2 *)
    rScratch3                       : REAL := 0.0;                 (* General scratchpad 3 *)
    rScratch4                       : REAL := 0.0;                 (* General scratchpad 4 *)
    rScratch5                       : REAL := 0.0;                 (* General scratchpad 5 *)
    rScratch6                       : REAL := 0.0;                 (* General scratchpad 6 *)
    rScratch7                       : REAL := 0.0;                 (* General scratchpad 7 *)
    rScratch8                       : REAL := 0.0;                 (* General scratchpad 8 *)
    rScratch9                       : REAL := 0.0;                 (* General scratchpad 9 *)
    rScratch10                      : REAL := 0.0;                 (* General scratchpad 10 *)
    rMedianBuffer                   : ARRAY[1..3] OF REAL;         (* 2oo3 median sorting buffer *)
    rSwapTemp                       : REAL := 0.0;                 (* Bubble sort swap variable *)
    rEngineSpeedRadS                : REAL := 62.83;               (* Engine speed converted to rad/s *)
    rShaft1SpeedRadS                : REAL := 0.0;                 (* Shaft 1 speed converted to rad/s *)
    rShaft2SpeedRadS                : REAL := 0.0;                 (* Shaft 2 speed converted to rad/s *)
    rActiveSlipSpeedRadS            : REAL := 0.0;                 (* Active clutch relative slip speed [rad/s] *)
    rActiveClutchNormalForce        : REAL := 0.0;                 (* Net hydraulic clamping normal force [N] *)
    rActiveFrictionCoeff            : REAL := 0.138;               (* Instantaneous friction coefficient *)
    rTargetGearRatio                : REAL := 14.94;               (* Ratio of currently engaged gear *)
END_VAR
''')

    # Cyclic Execution Modules
    # Module 1 & Module 2
    parts.append('''(*
====================================================================================================
  CYCLIC EXECUTION MODULE 1: SIL-3 SAFETY PERMISSIVES, WATCHDOG & COLD BOOT INITIALIZATION
====================================================================================================
*)
(* Master Cold-Start Parameterization *)
IF NOT bMasterFirstScanDone THEN
    (* Initialize 16x16 State Transition Matrix matA with discrete-time powertrain dynamics *)
    FOR nIdx_i := 1 TO 16 DO
        FOR nIdx_j := 1 TO 16 DO
            IF nIdx_i = nIdx_j THEN
                matA[nIdx_i, nIdx_j] := 0.9850;
            ELSE
                matA[nIdx_i, nIdx_j] := 0.0000;
            END_IF;
        END_FOR;
    END_FOR;

    (* Kinematic cross-coupling between engine, clutches, shafts, and vehicle inertia *)
    matA[1, 1]  := 0.9650;  matA[1, 2]  := 0.0185;  matA[1, 3]  := 0.0165;  matA[1, 9]  := -0.0450;
    matA[2, 1]  := 0.0240;  matA[2, 2]  := 0.9450;  matA[2, 4]  := 0.0310;  matA[2, 9]  :=  0.0820;
    matA[3, 1]  := 0.0220;  matA[3, 3]  := 0.9420;  matA[3, 4]  := 0.0350;  matA[3, 10] :=  0.0780;
    matA[4, 2]  := 0.0450;  matA[4, 3]  := 0.0480;  matA[4, 4]  := 0.9150;  matA[4, 5]  := -0.0520;
    matA[5, 4]  := 0.0650;  matA[5, 5]  := 0.8950;  matA[5, 6]  := -0.0850; matA[5, 7]  :=  0.0250;
    matA[6, 5]  := 0.0100;  matA[6, 6]  := 0.9950;  matA[6, 7]  := -0.0100;
    matA[7, 6]  := 0.0550;  matA[7, 7]  := 0.9250;  matA[7, 8]  := 0.0450;
    matA[8, 7]  := 0.0195;  matA[8, 8]  := 0.9850;
    matA[9, 9]  := 0.8250;  matA[9, 11] := 0.1450;
    matA[10, 10]:= 0.8250;  matA[10, 12]:= 0.1450;
    matA[11, 11]:= 0.7850;
    matA[12, 12]:= 0.7850;
    matA[13, 13]:= 0.8650;
    matA[14, 14]:= 0.8650;
    matA[15, 9] := 0.0125;  matA[15, 15]:= 0.9920;
    matA[16, 10]:= 0.0125;  matA[16, 16]:= 0.9920;

    (* Initialize 16x8 Input Coupling Matrix matB *)
    FOR nIdx_i := 1 TO 16 DO
        FOR nIdx_j := 1 TO 8 DO
            matB[nIdx_i, nIdx_j] := 0.0000;
        END_FOR;
    END_FOR;
    matB[1, 5]  := 0.0285;  (* Engine torque intervention -> Engine speed *)
    matB[1, 8]  := 0.0120;  (* Anti-jerk torque -> Engine speed *)
    matB[9, 1]  := 0.0450;  (* Solenoid 1 current -> Clutch 1 pressure *)
    matB[10, 2] := 0.0450;  (* Solenoid 2 current -> Clutch 2 pressure *)
    matB[11, 1] := 0.0850;  (* Solenoid 1 current -> Spool 1 position *)
    matB[12, 2] := 0.0850;  (* Solenoid 2 current -> Spool 2 position *)
    matB[13, 3] := 0.1250;  (* Rail odd servo command -> Rail odd stroke *)
    matB[14, 4] := 0.1250;  (* Rail even servo command -> Rail even stroke *)
    matB[15, 6] := -0.0180; (* Cooling oil flow -> Clutch 1 temp *)
    matB[16, 6] := -0.0180; (* Cooling oil flow -> Clutch 2 temp *)

    (* Initialize 16x16 Measurement Observation Matrix matC as Identity *)
    FOR nIdx_i := 1 TO 16 DO
        FOR nIdx_j := 1 TO 16 DO
            IF nIdx_i = nIdx_j THEN
                matC[nIdx_i, nIdx_j] := 1.0000;
            ELSE
                matC[nIdx_i, nIdx_j] := 0.0000;
            END_IF;
        END_FOR;
    END_FOR;

    (* Initialize 16x8 Feedthrough Matrix matD as Zero *)
    FOR nIdx_i := 1 TO 16 DO
        FOR nIdx_j := 1 TO 8 DO
            matD[nIdx_i, nIdx_j] := 0.0000;
        END_FOR;
    END_FOR;

    (* Initialize 16x16 Observer Gain Matrix matL *)
    FOR nIdx_i := 1 TO 16 DO
        FOR nIdx_j := 1 TO 16 DO
            IF nIdx_i = nIdx_j THEN
                matL[nIdx_i, nIdx_j] := 0.2500;
            ELSE
                matL[nIdx_i, nIdx_j] := 0.0000;
            END_IF;
        END_FOR;
    END_FOR;
    matL[1, 1]   := 0.4500;
    matL[2, 2]   := 0.4200;
    matL[3, 3]   := 0.4200;
    matL[5, 5]   := 0.3800;
    matL[9, 9]   := 0.5200;
    matL[10, 10] := 0.5200;
    matL[13, 13] := 0.6500;
    matL[14, 14] := 0.6500;

    (* Initialize MPC Quadratic Cost Weights *)
    FOR nIdx_i := 1 TO 16 DO
        vecQ_Cost[nIdx_i] := 1.0000;
        vecP_Cost[nIdx_i] := 5.0000;
    END_FOR;
    vecQ_Cost[1]  := 15.0;  (* Engine speed tracking *)
    vecQ_Cost[2]  := 25.0;  (* Shaft 1 synchronization *)
    vecQ_Cost[3]  := 25.0;  (* Shaft 2 synchronization *)
    vecQ_Cost[6]  := 180.0; (* Driveline twist angle suppression *)
    vecQ_Cost[9]  := 12.0;  (* Clutch 1 pressure tracking *)
    vecQ_Cost[10] := 12.0;  (* Clutch 2 pressure tracking *)
    vecQ_Cost[13] := 45.0;  (* Shift Rail odd positioning *)
    vecQ_Cost[14] := 45.0;  (* Shift Rail even positioning *)

    vecR_Cost[1] := 0.050; vecR_Cost[2] := 0.050; (* Solenoid current effort *)
    vecR_Cost[3] := 0.120; vecR_Cost[4] := 0.120; (* Rail servo effort *)
    vecR_Cost[5] := 0.015; (* Engine torque intervention *)
    vecR_Cost[6] := 0.080; (* Cooling oil flow *)
    vecR_Cost[7] := 0.020; (* Line pump duty *)
    vecR_Cost[8] := 0.035; (* Anti-jerk torque *)

    vecRd_Cost[1] := 0.250; vecRd_Cost[2] := 0.250;
    vecRd_Cost[3] := 0.450; vecRd_Cost[4] := 0.450;
    vecRd_Cost[5] := 0.080; vecRd_Cost[6] := 0.150;
    vecRd_Cost[7] := 0.050; vecRd_Cost[8] := 0.180;

    (* Actuator hard bounds *)
    vecU_Min[1] := 0.0;    vecU_Max[1] := 1500.0; (* Clutch 1 current [mA] *)
    vecU_Min[2] := 0.0;    vecU_Max[2] := 1500.0; (* Clutch 2 current [mA] *)
    vecU_Min[3] := -100.0; vecU_Max[3] := 100.0;  (* Rail odd servo [%] *)
    vecU_Min[4] := -100.0; vecU_Max[4] := 100.0;  (* Rail even servo [%] *)
    vecU_Min[5] := -800.0; vecU_Max[5] := 500.0;  (* Engine torque offset [Nm] *)
    vecU_Min[6] := 0.0;    vecU_Max[6] := 100.0;  (* Cooling valve [%] *)
    vecU_Min[7] := 10.0;   vecU_Max[7] := 100.0;  (* Line pump duty [%] *)
    vecU_Min[8] := -350.0; vecU_Max[8] := 350.0;  (* Anti-jerk torque [Nm] *)

    vecDeltaU_Max[1] := 125.0; vecDeltaU_Max[2] := 125.0;
    vecDeltaU_Max[3] := 25.0;  vecDeltaU_Max[4] := 25.0;
    vecDeltaU_Max[5] := 150.0; vecDeltaU_Max[6] := 15.0;
    vecDeltaU_Max[7] := 10.0;  vecDeltaU_Max[8] := 85.0;

    (* Initial State Vector Seed *)
    vecState_x[1] := 62.83; (* 600 RPM engine idle *)
    vecState_x[7] := 0.0;
    vecState_x[8] := 0.0;
    vecState_x[9] := 0.0;
    vecState_x[10]:= 0.0;
    vecState_x[15]:= 45.0;
    vecState_x[16]:= 45.0;

    bMasterFirstScanDone := TRUE;
END_IF;

(* SIL-3 Hardwired Emergency Stop & Neutral Vent Interlock *)
IF NOT bEStopEmergencyTrip THEN
    eCurrentState := 11; (* Force to Emergency Neutral Dump State *)
    bEmergencyNeutralActive := TRUE;
    bPowerShiftActive := FALSE;
    bTransmissionInGear := FALSE;
    dwAlarmWord_Trips.0 := TRUE; (* SIL-3 Emergency Neutral Vent Tripped *)

    rClutch1CurrentCommand_mA := 0.0;
    rClutch2CurrentCommand_mA := 0.0;
    rClutch1PressureSetpoint_bar := 0.0;
    rClutch2PressureSetpoint_bar := 0.0;
    bClutch1VentValveOpen := TRUE;
    bClutch2VentValveOpen := TRUE;
    rShiftRail1ServoCmd_Pct := 0.0;
    rShiftRail2ServoCmd_Pct := 0.0;
    rShiftRail3ServoCmd_Pct := 0.0;
    rShiftRail4ServoCmd_Pct := 0.0;
    rEngineTorqueOverride_Nm := 0.0;
    rAntiJerkDampingTorque_Nm := 0.0;
    wTransmissionFSMState := 16#F000;
    RETURN;
END_IF;

(* Master Alarm Acknowledge & Reset *)
IF bAlarmAcknowledgeReset THEN
    dwAlarmWord_Trips.0 := FALSE;
    dwAlarmWord_Trips.1 := FALSE;
    dwAlarmWord_Trips.2 := FALSE;
    dwAlarmWord_Trips.3 := FALSE;
    dwAlarmWord_Severe.0 := FALSE;
    dwAlarmWord_Severe.1 := FALSE;
    dwAlarmWord_Severe.2 := FALSE;
    dwAlarmWord_Severe.3 := FALSE;
    dwAlarmWord_Warning.0 := FALSE;
    dwAlarmWord_Warning.1 := FALSE;
    dwAlarmWord_Warning.2 := FALSE;
    dwAlarmWord_Warning.3 := FALSE;
    IF eCurrentState = 11 AND bEStopEmergencyTrip THEN
        eCurrentState := 0; (* Return to POST *)
        bEmergencyNeutralActive := FALSE;
    END_IF;
END_IF;

(*
====================================================================================================
  CYCLIC EXECUTION MODULE 2: TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING ENGINES
====================================================================================================
*)
(* --- 2A: ENGINE SPEED 2oo3 MEDIAN VOTING --- *)
rMedianBuffer[1] := rEngineSpeed_ChA;
rMedianBuffer[2] := rEngineSpeed_ChB;
rMedianBuffer[3] := rEngineSpeed_ChC;

FOR nIdx_i := 1 TO 2 DO
    FOR nIdx_j := 1 TO 3 - nIdx_i DO
        IF rMedianBuffer[nIdx_j] > rMedianBuffer[nIdx_j + 1] THEN
            rSwapTemp := rMedianBuffer[nIdx_j];
            rMedianBuffer[nIdx_j] := rMedianBuffer[nIdx_j + 1];
            rMedianBuffer[nIdx_j + 1] := rSwapTemp;
        END_IF;
    END_FOR;
END_FOR;

(* Channel Discrepancy Debounce *)
IF ABS(rEngineSpeed_ChA - rMedianBuffer[2]) > rEngineSpeed_TmrThresh THEN
    tEngineSpeed_ChA_FaultTimer := tEngineSpeed_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tEngineSpeed_ChA_FaultTimer >= rTmrPersistenceLimit THEN
        bEngineSpeed_ChA_Healthy := FALSE;
    END_IF;
ELSE
    tEngineSpeed_ChA_FaultTimer := 0.0;
    bEngineSpeed_ChA_Healthy := TRUE;
END_IF;

IF ABS(rEngineSpeed_ChB - rMedianBuffer[2]) > rEngineSpeed_TmrThresh THEN
    tEngineSpeed_ChB_FaultTimer := tEngineSpeed_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tEngineSpeed_ChB_FaultTimer >= rTmrPersistenceLimit THEN
        bEngineSpeed_ChB_Healthy := FALSE;
    END_IF;
ELSE
    tEngineSpeed_ChB_FaultTimer := 0.0;
    bEngineSpeed_ChB_Healthy := TRUE;
END_IF;

IF ABS(rEngineSpeed_ChC - rMedianBuffer[2]) > rEngineSpeed_TmrThresh THEN
    tEngineSpeed_ChC_FaultTimer := tEngineSpeed_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tEngineSpeed_ChC_FaultTimer >= rTmrPersistenceLimit THEN
        bEngineSpeed_ChC_Healthy := FALSE;
    END_IF;
ELSE
    tEngineSpeed_ChC_FaultTimer := 0.0;
    bEngineSpeed_ChC_Healthy := TRUE;
END_IF;

(* Synthesis of Voted Engine Speed *)
IF bEngineSpeed_ChA_Healthy AND bEngineSpeed_ChB_Healthy AND bEngineSpeed_ChC_Healthy THEN
    rEngineSpeed_Voted := rMedianBuffer[2];
    wTMR_DiscrepancyStatus.0 := FALSE;
ELSIF bEngineSpeed_ChA_Healthy AND bEngineSpeed_ChB_Healthy THEN
    rEngineSpeed_Voted := 0.5 * (rEngineSpeed_ChA + rEngineSpeed_ChB);
    wTMR_DiscrepancyStatus.0 := TRUE;
ELSIF bEngineSpeed_ChA_Healthy AND bEngineSpeed_ChC_Healthy THEN
    rEngineSpeed_Voted := 0.5 * (rEngineSpeed_ChA + rEngineSpeed_ChC);
    wTMR_DiscrepancyStatus.0 := TRUE;
ELSIF bEngineSpeed_ChB_Healthy AND bEngineSpeed_ChC_Healthy THEN
    rEngineSpeed_Voted := 0.5 * (rEngineSpeed_ChB + rEngineSpeed_ChC);
    wTMR_DiscrepancyStatus.0 := TRUE;
ELSIF bEngineSpeed_ChA_Healthy THEN
    rEngineSpeed_Voted := rEngineSpeed_ChA;
    dwAlarmWord_Warning.0 := TRUE; (* Single Engine Speed Channel Active *)
ELSIF bEngineSpeed_ChB_Healthy THEN
    rEngineSpeed_Voted := rEngineSpeed_ChB;
    dwAlarmWord_Warning.0 := TRUE;
ELSIF bEngineSpeed_ChC_Healthy THEN
    rEngineSpeed_Voted := rEngineSpeed_ChC;
    dwAlarmWord_Warning.0 := TRUE;
ELSE
    rEngineSpeed_Voted := 600.0; (* Fallback Idle Default *)
    dwAlarmWord_Severe.0 := TRUE; (* All Engine Speed Channels Failed *)
END_IF;

(* --- 2B: INPUT SHAFT 1 SPEED 2oo3 MEDIAN VOTING --- *)
rMedianBuffer[1] := rInputShaft1Speed_ChA;
rMedianBuffer[2] := rInputShaft1Speed_ChB;
rMedianBuffer[3] := rInputShaft1Speed_ChC;

FOR nIdx_i := 1 TO 2 DO
    FOR nIdx_j := 1 TO 3 - nIdx_i DO
        IF rMedianBuffer[nIdx_j] > rMedianBuffer[nIdx_j + 1] THEN
            rSwapTemp := rMedianBuffer[nIdx_j];
            rMedianBuffer[nIdx_j] := rMedianBuffer[nIdx_j + 1];
            rMedianBuffer[nIdx_j + 1] := rSwapTemp;
        END_IF;
    END_FOR;
END_FOR;

IF ABS(rInputShaft1Speed_ChA - rMedianBuffer[2]) > rShaft1Speed_TmrThresh THEN
    tShaft1Speed_ChA_FaultTimer := tShaft1Speed_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tShaft1Speed_ChA_FaultTimer >= rTmrPersistenceLimit THEN
        bShaft1Speed_ChA_Healthy := FALSE;
    END_IF;
ELSE
    tShaft1Speed_ChA_FaultTimer := 0.0;
    bShaft1Speed_ChA_Healthy := TRUE;
END_IF;

IF ABS(rInputShaft1Speed_ChB - rMedianBuffer[2]) > rShaft1Speed_TmrThresh THEN
    tShaft1Speed_ChB_FaultTimer := tShaft1Speed_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tShaft1Speed_ChB_FaultTimer >= rTmrPersistenceLimit THEN
        bShaft1Speed_ChB_Healthy := FALSE;
    END_IF;
ELSE
    tShaft1Speed_ChB_FaultTimer := 0.0;
    bShaft1Speed_ChB_Healthy := TRUE;
END_IF;

IF ABS(rInputShaft1Speed_ChC - rMedianBuffer[2]) > rShaft1Speed_TmrThresh THEN
    tShaft1Speed_ChC_FaultTimer := tShaft1Speed_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tShaft1Speed_ChC_FaultTimer >= rTmrPersistenceLimit THEN
        bShaft1Speed_ChC_Healthy := FALSE;
    END_IF;
ELSE
    tShaft1Speed_ChC_FaultTimer := 0.0;
    bShaft1Speed_ChC_Healthy := TRUE;
END_IF;

IF bShaft1Speed_ChA_Healthy AND bShaft1Speed_ChB_Healthy AND bShaft1Speed_ChC_Healthy THEN
    rShaft1Speed_Voted := rMedianBuffer[2];
    wTMR_DiscrepancyStatus.1 := FALSE;
ELSIF bShaft1Speed_ChA_Healthy AND bShaft1Speed_ChB_Healthy THEN
    rShaft1Speed_Voted := 0.5 * (rInputShaft1Speed_ChA + rInputShaft1Speed_ChB);
    wTMR_DiscrepancyStatus.1 := TRUE;
ELSIF bShaft1Speed_ChA_Healthy AND bShaft1Speed_ChC_Healthy THEN
    rShaft1Speed_Voted := 0.5 * (rInputShaft1Speed_ChA + rInputShaft1Speed_ChC);
    wTMR_DiscrepancyStatus.1 := TRUE;
ELSIF bShaft1Speed_ChB_Healthy AND bShaft1Speed_ChC_Healthy THEN
    rShaft1Speed_Voted := 0.5 * (rInputShaft1Speed_ChB + rInputShaft1Speed_ChC);
    wTMR_DiscrepancyStatus.1 := TRUE;
ELSE
    rShaft1Speed_Voted := rMedianBuffer[2];
    dwAlarmWord_Warning.1 := TRUE;
END_IF;

(* --- 2C: INPUT SHAFT 2 SPEED 2oo3 MEDIAN VOTING --- *)
rMedianBuffer[1] := rInputShaft2Speed_ChA;
rMedianBuffer[2] := rInputShaft2Speed_ChB;
rMedianBuffer[3] := rInputShaft2Speed_ChC;

FOR nIdx_i := 1 TO 2 DO
    FOR nIdx_j := 1 TO 3 - nIdx_i DO
        IF rMedianBuffer[nIdx_j] > rMedianBuffer[nIdx_j + 1] THEN
            rSwapTemp := rMedianBuffer[nIdx_j];
            rMedianBuffer[nIdx_j] := rMedianBuffer[nIdx_j + 1];
            rMedianBuffer[nIdx_j + 1] := rSwapTemp;
        END_IF;
    END_FOR;
END_FOR;

IF ABS(rInputShaft2Speed_ChA - rMedianBuffer[2]) > rShaft2Speed_TmrThresh THEN
    tShaft2Speed_ChA_FaultTimer := tShaft2Speed_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tShaft2Speed_ChA_FaultTimer >= rTmrPersistenceLimit THEN
        bShaft2Speed_ChA_Healthy := FALSE;
    END_IF;
ELSE
    tShaft2Speed_ChA_FaultTimer := 0.0;
    bShaft2Speed_ChA_Healthy := TRUE;
END_IF;

IF ABS(rInputShaft2Speed_ChB - rMedianBuffer[2]) > rShaft2Speed_TmrThresh THEN
    tShaft2Speed_ChB_FaultTimer := tShaft2Speed_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tShaft2Speed_ChB_FaultTimer >= rTmrPersistenceLimit THEN
        bShaft2Speed_ChB_Healthy := FALSE;
    END_IF;
ELSE
    tShaft2Speed_ChB_FaultTimer := 0.0;
    bShaft2Speed_ChB_Healthy := TRUE;
END_IF;

IF ABS(rInputShaft2Speed_ChC - rMedianBuffer[2]) > rShaft2Speed_TmrThresh THEN
    tShaft2Speed_ChC_FaultTimer := tShaft2Speed_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tShaft2Speed_ChC_FaultTimer >= rTmrPersistenceLimit THEN
        bShaft2Speed_ChC_Healthy := FALSE;
    END_IF;
ELSE
    tShaft2Speed_ChC_FaultTimer := 0.0;
    bShaft2Speed_ChC_Healthy := TRUE;
END_IF;

IF bShaft2Speed_ChA_Healthy AND bShaft2Speed_ChB_Healthy AND bShaft2Speed_ChC_Healthy THEN
    rShaft2Speed_Voted := rMedianBuffer[2];
    wTMR_DiscrepancyStatus.2 := FALSE;
ELSIF bShaft2Speed_ChA_Healthy AND bShaft2Speed_ChB_Healthy THEN
    rShaft2Speed_Voted := 0.5 * (rInputShaft2Speed_ChA + rInputShaft2Speed_ChB);
    wTMR_DiscrepancyStatus.2 := TRUE;
ELSIF bShaft2Speed_ChA_Healthy AND bShaft2Speed_ChC_Healthy THEN
    rShaft2Speed_Voted := 0.5 * (rInputShaft2Speed_ChA + rInputShaft2Speed_ChC);
    wTMR_DiscrepancyStatus.2 := TRUE;
ELSIF bShaft2Speed_ChB_Healthy AND bShaft2Speed_ChC_Healthy THEN
    rShaft2Speed_Voted := 0.5 * (rInputShaft2Speed_ChB + rInputShaft2Speed_ChC);
    wTMR_DiscrepancyStatus.2 := TRUE;
ELSE
    rShaft2Speed_Voted := rMedianBuffer[2];
    dwAlarmWord_Warning.2 := TRUE;
END_IF;

(* --- 2D: MAIN HYDRAULIC LINE PRESSURE 2oo3 MEDIAN VOTING --- *)
rMedianBuffer[1] := rMainLinePressure_ChA;
rMedianBuffer[2] := rMainLinePressure_ChB;
rMedianBuffer[3] := rMainLinePressure_ChC;

FOR nIdx_i := 1 TO 2 DO
    FOR nIdx_j := 1 TO 3 - nIdx_i DO
        IF rMedianBuffer[nIdx_j] > rMedianBuffer[nIdx_j + 1] THEN
            rSwapTemp := rMedianBuffer[nIdx_j];
            rMedianBuffer[nIdx_j] := rMedianBuffer[nIdx_j + 1];
            rMedianBuffer[nIdx_j + 1] := rSwapTemp;
        END_IF;
    END_FOR;
END_FOR;

IF ABS(rMainLinePressure_ChA - rMedianBuffer[2]) > rLinePress_TmrThresh THEN
    tLinePress_ChA_FaultTimer := tLinePress_ChA_FaultTimer + rConst_ScanDeltaTime;
    IF tLinePress_ChA_FaultTimer >= rTmrPersistenceLimit THEN
        bLinePress_ChA_Healthy := FALSE;
    END_IF;
ELSE
    tLinePress_ChA_FaultTimer := 0.0;
    bLinePress_ChA_Healthy := TRUE;
END_IF;

IF ABS(rMainLinePressure_ChB - rMedianBuffer[2]) > rLinePress_TmrThresh THEN
    tLinePress_ChB_FaultTimer := tLinePress_ChB_FaultTimer + rConst_ScanDeltaTime;
    IF tLinePress_ChB_FaultTimer >= rTmrPersistenceLimit THEN
        bLinePress_ChB_Healthy := FALSE;
    END_IF;
ELSE
    tLinePress_ChB_FaultTimer := 0.0;
    bLinePress_ChB_Healthy := TRUE;
END_IF;

IF ABS(rMainLinePressure_ChC - rMedianBuffer[2]) > rLinePress_TmrThresh THEN
    tLinePress_ChC_FaultTimer := tLinePress_ChC_FaultTimer + rConst_ScanDeltaTime;
    IF tLinePress_ChC_FaultTimer >= rTmrPersistenceLimit THEN
        bLinePress_ChC_Healthy := FALSE;
    END_IF;
ELSE
    tLinePress_ChC_FaultTimer := 0.0;
    bLinePress_ChC_Healthy := TRUE;
END_IF;

IF bLinePress_ChA_Healthy AND bLinePress_ChB_Healthy AND bLinePress_ChC_Healthy THEN
    rMainLinePressure_Voted := rMedianBuffer[2];
    wTMR_DiscrepancyStatus.3 := FALSE;
ELSIF bLinePress_ChA_Healthy AND bLinePress_ChB_Healthy THEN
    rMainLinePressure_Voted := 0.5 * (rMainLinePressure_ChA + rMainLinePressure_ChB);
    wTMR_DiscrepancyStatus.3 := TRUE;
ELSIF bLinePress_ChA_Healthy AND bLinePress_ChC_Healthy THEN
    rMainLinePressure_Voted := 0.5 * (rMainLinePressure_ChA + rMainLinePressure_ChC);
    wTMR_DiscrepancyStatus.3 := TRUE;
ELSIF bLinePress_ChB_Healthy AND bLinePress_ChC_Healthy THEN
    rMainLinePressure_Voted := 0.5 * (rMainLinePressure_ChB + rMainLinePressure_ChC);
    wTMR_DiscrepancyStatus.3 := TRUE;
ELSE
    rMainLinePressure_Voted := rMedianBuffer[2];
    dwAlarmWord_Severe.1 := TRUE; (* Line Pressure Sensor Redundancy Depleted *)
END_IF;
''')

    # Module 3 & Module 4
    parts.append('''(*
====================================================================================================
  CYCLIC EXECUTION MODULE 3: DYNAMIC ADAPTIVE KISS-POINT CALIBRATION & FRICTION DEGRADATION
====================================================================================================
*)
(* Temperature Compensation Model for Wet Clutch Kiss-Point *)
rKissPointPressure_C1_Comp := rKissPointPressure_C1_Base
                            + rConst_TempCoeffAlpha1 * (rClutchOilSumpTemp - rConst_OilRefTempDegC)
                            + rConst_TempCoeffAlpha2 * (rClutchOilSumpTemp - rConst_OilRefTempDegC) * (rClutchOilSumpTemp - rConst_OilRefTempDegC);

rKissPointPressure_C2_Comp := rKissPointPressure_C2_Base
                            + rConst_TempCoeffAlpha1 * (rClutchOilSumpTemp - rConst_OilRefTempDegC)
                            + rConst_TempCoeffAlpha2 * (rClutchOilSumpTemp - rConst_OilRefTempDegC) * (rClutchOilSumpTemp - rConst_OilRefTempDegC);

(* Bound compensated kiss-points within physical hydraulic boundaries *)
IF rKissPointPressure_C1_Comp < 2.50 THEN
    rKissPointPressure_C1_Comp := 2.50;
ELSIF rKissPointPressure_C1_Comp > 6.50 THEN
    rKissPointPressure_C1_Comp := 6.50;
END_IF;

IF rKissPointPressure_C2_Comp < 2.50 THEN
    rKissPointPressure_C2_Comp := 2.50;
ELSIF rKissPointPressure_C2_Comp > 6.50 THEN
    rKissPointPressure_C2_Comp := 6.50;
END_IF;

rCalibratedKissPressure_C1 := rKissPointPressure_C1_Comp;
rCalibratedKissPressure_C2 := rKissPointPressure_C2_Comp;

(* Convert Rotational Speeds to Rad/Sec *)
rEngineSpeedRadS := rEngineSpeed_Voted * 0.104719755; (* 2 * PI / 60 *)
rShaft1SpeedRadS := rShaft1Speed_Voted * 0.104719755;
rShaft2SpeedRadS := rShaft2Speed_Voted * 0.104719755;

(* Clutch 1 Transmitted Torque Calculation & Slip Power *)
IF rClutch1ChamberPressure > (rConst_ReturnSpringPreload / (rConst_ClutchPistonArea * 1.0E5)) THEN
    rActiveClutchNormalForce := (rClutch1ChamberPressure * 1.0E5 * rConst_ClutchPistonArea)
                              - rConst_ReturnSpringPreload
                              - (rConst_ReturnSpringRate * rConst_PistonCushionTravel);
    IF rActiveClutchNormalForce < 0.0 THEN
        rActiveClutchNormalForce := 0.0;
    END_IF;
ELSE
    rActiveClutchNormalForce := 0.0;
END_IF;

rActiveSlipSpeedRadS := ABS(rEngineSpeedRadS - rShaft1SpeedRadS);
rActiveFrictionCoeff := rConst_BaseFrictionCoeff * (1.0 - rConst_WearDegradationFactor * rCumulativeWearEnergy_C1_MJ);
IF rActiveFrictionCoeff < 0.085 THEN
    rActiveFrictionCoeff := 0.085;
END_IF;

rClutch1EstimatedTorque_Nm := rConst_ClutchFrictionPlates * rActiveFrictionCoeff * rActiveClutchNormalForce * rConst_ClutchMeanRadius;
IF rClutch1EstimatedTorque_Nm > 3500.0 THEN
    rClutch1EstimatedTorque_Nm := 3500.0;
END_IF;

(* Accumulate Frictional Slip Dissipation Energy: E_slip = Integral( T_c * Delta_omega ) dt [MJ] *)
IF rActiveSlipSpeedRadS > 1.50 AND rClutch1EstimatedTorque_Nm > 5.0 THEN
    rCumulativeWearEnergy_C1_MJ := rCumulativeWearEnergy_C1_MJ + (rClutch1EstimatedTorque_Nm * rActiveSlipSpeedRadS * rConst_ScanDeltaTime * 1.0E-6);
END_IF;

(* Clutch 2 Transmitted Torque Calculation *)
IF rClutch2ChamberPressure > (rConst_ReturnSpringPreload / (rConst_ClutchPistonArea * 1.0E5)) THEN
    rScratch1 := (rClutch2ChamberPressure * 1.0E5 * rConst_ClutchPistonArea)
               - rConst_ReturnSpringPreload
               - (rConst_ReturnSpringRate * rConst_PistonCushionTravel);
    IF rScratch1 < 0.0 THEN
        rScratch1 := 0.0;
    END_IF;
ELSE
    rScratch1 := 0.0;
END_IF;

rScratch2 := ABS(rEngineSpeedRadS - rShaft2SpeedRadS);
rClutch2EstimatedTorque_Nm := rConst_ClutchFrictionPlates * rActiveFrictionCoeff * rScratch1 * rConst_ClutchMeanRadius;
IF rClutch2EstimatedTorque_Nm > 3500.0 THEN
    rClutch2EstimatedTorque_Nm := 3500.0;
END_IF;

IF rScratch2 > 1.50 AND rClutch2EstimatedTorque_Nm > 5.0 THEN
    rCumulativeWearEnergy_C2_MJ := rCumulativeWearEnergy_C2_MJ + (rClutch2EstimatedTorque_Nm * rScratch2 * rConst_ScanDeltaTime * 1.0E-6);
END_IF;

(*
====================================================================================================
  CYCLIC EXECUTION MODULE 4: SYNCHRONOUS SHIFT RAIL SERVO PACING & POSITIONING
====================================================================================================
*)
arrRailPosition_Actual[1] := rShiftRail1Pos_LVDT;
arrRailPosition_Actual[2] := rShiftRail2Pos_LVDT;
arrRailPosition_Actual[3] := rShiftRail3Pos_LVDT;
arrRailPosition_Actual[4] := rShiftRail4Pos_LVDT;

(* Evaluate Rail Detent Lock Flags (+/- 18.0 mm +/- 0.35 mm) *)
FOR nIdx_i := 1 TO 4 DO
    IF ABS(arrRailPosition_Actual[nIdx_i] - 18.0) <= 0.35 OR ABS(arrRailPosition_Actual[nIdx_i] - (-18.0)) <= 0.35 THEN
        arrRailInDetentLock[nIdx_i] := TRUE;
    ELSE
        arrRailInDetentLock[nIdx_i] := FALSE;
    END_IF;
END_FOR;

(* Shift Rail Proportional-Derivative (PD) Servo Pacing Loop *)
FOR nIdx_i := 1 TO 4 DO
    rScratch1 := arrRailPosition_Target[nIdx_i] - arrRailPosition_Actual[nIdx_i]; (* Position Error [mm] *)
    arrRailVelocity_Actual[nIdx_i] := (arrRailPosition_Actual[nIdx_i] - vecState_x[12 + nIdx_i]) / rConst_ScanDeltaTime;
    
    (* Servo control command [%] *)
    arrRailServoOutput[nIdx_i] := (rRailKp * rScratch1) - (rRailKd * arrRailVelocity_Actual[nIdx_i]);
    
    (* Anti-windup saturation clamping [-100% to +100%] *)
    IF arrRailServoOutput[nIdx_i] > 100.0 THEN
        arrRailServoOutput[nIdx_i] := 100.0;
    ELSIF arrRailServoOutput[nIdx_i] < -100.0 THEN
        arrRailServoOutput[nIdx_i] := -100.0;
    END_IF;
END_FOR;

rShiftRail1ServoCmd_Pct := arrRailServoOutput[1];
rShiftRail2ServoCmd_Pct := arrRailServoOutput[2];
rShiftRail3ServoCmd_Pct := arrRailServoOutput[3];
rShiftRail4ServoCmd_Pct := arrRailServoOutput[4];

(* Pack Mechanical Rail Position Status Word *)
wShiftRailStatusWord.0 := (ABS(arrRailPosition_Actual[1]) <= 0.25); (* Rail 1 Neutral *)
wShiftRailStatusWord.1 := (arrRailPosition_Actual[1] >= 17.65);     (* Gear 1 Engaged *)
wShiftRailStatusWord.2 := (arrRailPosition_Actual[1] <= -17.65);    (* Gear 3 Engaged *)
wShiftRailStatusWord.3 := (ABS(arrRailPosition_Actual[2]) <= 0.25); (* Rail 2 Neutral *)
wShiftRailStatusWord.4 := (arrRailPosition_Actual[2] >= 17.65);     (* Gear 5 Engaged *)
wShiftRailStatusWord.5 := (arrRailPosition_Actual[2] <= -17.65);    (* Gear 7 Engaged *)
wShiftRailStatusWord.6 := (ABS(arrRailPosition_Actual[3]) <= 0.25); (* Rail 3 Neutral *)
wShiftRailStatusWord.7 := (arrRailPosition_Actual[3] >= 17.65);     (* Gear 2 Engaged *)
wShiftRailStatusWord.8 := (arrRailPosition_Actual[3] <= -17.65);    (* Gear 4 / Rev Engaged *)
wShiftRailStatusWord.9 := (ABS(arrRailPosition_Actual[4]) <= 0.25); (* Rail 4 Neutral *)
wShiftRailStatusWord.10:= (arrRailPosition_Actual[4] >= 17.65);     (* Gear 6 Engaged *)
wShiftRailStatusWord.11:= (arrRailPosition_Actual[4] <= -17.65);    (* Gear 8/10/12 Engaged *)
''')

    # Module 5 & Module 6 & Module 7
    parts.append('''(*
====================================================================================================
  CYCLIC EXECUTION MODULE 5: ACTIVE DRIVELINE ANTI-JERK TORSIONAL DAMPING COMPENSATOR
====================================================================================================
*)
(* Relative slip across driveline torsional elasticity: Delta_omega_dl = omega_trans_out - omega_whl * i_diff *)
rScratch1 := vecState_x[5] - (vecState_x[7] * rConst_FinalDriveRatio);

(* 1st-order low-pass pre-filtering to reject sensor quantization ripple *)
rDrivelineSpeedDeltaFiltered := rDrivelineSpeedDeltaFiltered + 0.150 * (rScratch1 - rDrivelineSpeedDeltaFiltered);

(* Differentiated chassis shuffle acceleration *)
rScratch2 := (rDrivelineSpeedDeltaFiltered - rDrivelineSpeedDeltaPrev) / rConst_ScanDeltaTime;
rDrivelineSpeedDeltaPrev := rDrivelineSpeedDeltaFiltered;

(* Active Anti-Jerk Damping Correction Torque [Nm] *)
rAntiJerkDampingTorque_Nm := -(rAntiJerkDampingGainProp * rDrivelineSpeedDeltaFiltered) - (rAntiJerkDampingGainDeriv * rScratch2);

(* Saturation clipping within safe driveline boundaries *)
IF rAntiJerkDampingTorque_Nm > rAntiJerkMaxTorqueClip THEN
    rAntiJerkDampingTorque_Nm := rAntiJerkMaxTorqueClip;
ELSIF rAntiJerkDampingTorque_Nm < -rAntiJerkMaxTorqueClip THEN
    rAntiJerkDampingTorque_Nm := -rAntiJerkMaxTorqueClip;
END_IF;

(* Disable anti-jerk intervention at standstill to eliminate low-speed creep chatter *)
IF rVehicleSpeedKmh < 1.50 THEN
    rAntiJerkDampingTorque_Nm := 0.0;
END_IF;

(* Estimated prop-shaft twist angle Delta_theta_d in milliradians *)
rDrivelineTorsionAngle_mrad := vecState_x[6] * 1000.0;

(*
====================================================================================================
  CYCLIC EXECUTION MODULE 6: 16x16 DISCRETE STATE-SPACE OBSERVER & INNOVATION UPDATE
====================================================================================================
*)
(* Populate Sensor Feedback Vector vecMeasurement_z in R^16 *)
vecMeasurement_z[1]  := rEngineSpeedRadS;
vecMeasurement_z[2]  := rShaft1SpeedRadS;
vecMeasurement_z[3]  := rShaft2SpeedRadS;
vecMeasurement_z[4]  := (rShaft1SpeedRadS + rShaft2SpeedRadS) * 0.50; (* Layshaft estimate *)
vecMeasurement_z[5]  := (rVehicleSpeedKmh / 3.60) / rConst_WheelRadiusM * rConst_FinalDriveRatio;
vecMeasurement_z[6]  := vecState_x[6]; (* Torsional angle observer state *)
vecMeasurement_z[7]  := (rVehicleSpeedKmh / 3.60) / rConst_WheelRadiusM;
vecMeasurement_z[8]  := rVehicleSpeedKmh / 3.60;
vecMeasurement_z[9]  := rClutch1ChamberPressure;
vecMeasurement_z[10] := rClutch2ChamberPressure;
vecMeasurement_z[11] := vecControl_u[1] * 0.0012; (* Spool displacement estimate 1 *)
vecMeasurement_z[12] := vecControl_u[2] * 0.0012; (* Spool displacement estimate 2 *)
vecMeasurement_z[13] := arrRailPosition_Actual[1];
vecMeasurement_z[14] := arrRailPosition_Actual[3];
vecMeasurement_z[15] := rClutch1PlateTemp;
vecMeasurement_z[16] := rClutch2PlateTemp;

(* Compute Observer Innovation Residual: e[k] = z[k] - (C * x[k] + D * u[k]) *)
FOR nIdx_i := 1 TO 16 DO
    rScratch1 := 0.0;
    FOR nIdx_j := 1 TO 16 DO
        rScratch1 := rScratch1 + (matC[nIdx_i, nIdx_j] * vecState_x[nIdx_j]);
    END_FOR;
    FOR nIdx_j := 1 TO 8 DO
        rScratch1 := rScratch1 + (matD[nIdx_i, nIdx_j] * vecControl_u[nIdx_j]);
    END_FOR;
    vecInnovation_e[nIdx_i] := vecMeasurement_z[nIdx_i] - rScratch1;
END_FOR;

(* State Propagation: x_pred[k+1] = A * x[k] + B * u[k] *)
FOR nIdx_i := 1 TO 16 DO
    rScratch1 := 0.0;
    FOR nIdx_j := 1 TO 16 DO
        rScratch1 := rScratch1 + (matA[nIdx_i, nIdx_j] * vecState_x[nIdx_j]);
    END_FOR;
    FOR nIdx_j := 1 TO 8 DO
        rScratch1 := rScratch1 + (matB[nIdx_i, nIdx_j] * vecControl_u[nIdx_j]);
    END_FOR;
    vecState_x_next[nIdx_i] := rScratch1;
END_FOR;

(* Observer Correction: x[k] = x_pred + L * e[k] *)
FOR nIdx_i := 1 TO 16 DO
    rScratch1 := 0.0;
    FOR nIdx_j := 1 TO 16 DO
        rScratch1 := rScratch1 + (matL[nIdx_i, nIdx_j] * vecInnovation_e[nIdx_j]);
    END_FOR;
    vecState_x[nIdx_i] := vecState_x_next[nIdx_i] + rScratch1;
END_FOR;

(*
====================================================================================================
  CYCLIC EXECUTION MODULE 7: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZER
====================================================================================================
*)
(* Assemble Reference State Vector vecStateRef *)
vecStateRef[1]  := rEngineSpeedRadS;
vecStateRef[5]  := (rVehicleSpeedKmh / 3.60) / rConst_WheelRadiusM * rConst_FinalDriveRatio;
vecStateRef[6]  := 0.0; (* Zero torsional twist target *)
vecStateRef[7]  := (rVehicleSpeedKmh / 3.60) / rConst_WheelRadiusM;
vecStateRef[8]  := rVehicleSpeedKmh / 3.60;
vecStateRef[9]  := rClutch1PressureSetpoint_bar;
vecStateRef[10] := rClutch2PressureSetpoint_bar;
vecStateRef[15] := 85.0; (* Target clutch cooling temp *)
vecStateRef[16] := 85.0;

(* Iterative Projected Gradient Descent (PGD) *)
FOR nMpcLoop := 1 TO iMpcInnerLoops DO
    (* Gradient with respect to u[1] (Clutch 1 Current) *)
    vecMpcGradient[1] := (vecQ_Cost[9] * (vecState_x[9] - vecStateRef[9]) * matB[9, 1])
                       + (vecR_Cost[1] * vecControl_u[1])
                       + (vecRd_Cost[1] * (vecControl_u[1] - vecControl_u_prev[1]));

    (* Gradient with respect to u[2] (Clutch 2 Current) *)
    vecMpcGradient[2] := (vecQ_Cost[10] * (vecState_x[10] - vecStateRef[10]) * matB[10, 2])
                       + (vecR_Cost[2] * vecControl_u[2])
                       + (vecRd_Cost[2] * (vecControl_u[2] - vecControl_u_prev[2]));

    (* Gradient with respect to u[3] (Rail Odd Command) *)
    vecMpcGradient[3] := (vecQ_Cost[13] * (vecState_x[13] - vecStateRef[13]) * matB[13, 3])
                       + (vecR_Cost[3] * vecControl_u[3])
                       + (vecRd_Cost[3] * (vecControl_u[3] - vecControl_u_prev[3]));

    (* Gradient with respect to u[4] (Rail Even Command) *)
    vecMpcGradient[4] := (vecQ_Cost[14] * (vecState_x[14] - vecStateRef[14]) * matB[14, 4])
                       + (vecR_Cost[4] * vecControl_u[4])
                       + (vecRd_Cost[4] * (vecControl_u[4] - vecControl_u_prev[4]));

    (* Gradient with respect to u[5] (Engine Torque Override) *)
    vecMpcGradient[5] := (vecQ_Cost[1] * (vecState_x[1] - vecStateRef[1]) * matB[1, 5])
                       + (vecR_Cost[5] * vecControl_u[5])
                       + (vecRd_Cost[5] * (vecControl_u[5] - vecControl_u_prev[5]));

    (* Gradient with respect to u[6] (Cooling Oil Valve) *)
    vecMpcGradient[6] := (vecQ_Cost[15] * (vecState_x[15] - vecStateRef[15]) * matB[15, 6])
                       + (vecR_Cost[6] * vecControl_u[6])
                       + (vecRd_Cost[6] * (vecControl_u[6] - vecControl_u_prev[6]));

    (* Gradient with respect to u[7] (Main Line Pump Duty) *)
    vecMpcGradient[7] := (vecR_Cost[7] * vecControl_u[7])
                       + (vecRd_Cost[7] * (vecControl_u[7] - vecControl_u_prev[7]));

    (* Gradient with respect to u[8] (Anti-Jerk Damping Correction) *)
    vecMpcGradient[8] := (vecQ_Cost[6] * (vecState_x[6] - vecStateRef[6]) * matB[1, 8])
                       + (vecR_Cost[8] * vecControl_u[8])
                       + (vecRd_Cost[8] * (vecControl_u[8] - vecControl_u_prev[8]));

    (* Apply Gradient Step & Slew Rate Saturation *)
    FOR nIdx_j := 1 TO 8 DO
        vecDeltaU[nIdx_j] := -(rMpcStepSize * vecMpcGradient[nIdx_j]);
        IF vecDeltaU[nIdx_j] > vecDeltaU_Max[nIdx_j] THEN
            vecDeltaU[nIdx_j] := vecDeltaU_Max[nIdx_j];
        ELSIF vecDeltaU[nIdx_j] < -vecDeltaU_Max[nIdx_j] THEN
            vecDeltaU[nIdx_j] := -vecDeltaU_Max[nIdx_j];
        END_IF;
        vecControl_u[nIdx_j] := vecControl_u[nIdx_j] + vecDeltaU[nIdx_j];
        
        (* Hard Actuator Bound Clamping *)
        IF vecControl_u[nIdx_j] > vecU_Max[nIdx_j] THEN
            vecControl_u[nIdx_j] := vecU_Max[nIdx_j];
        ELSIF vecControl_u[nIdx_j] < vecU_Min[nIdx_j] THEN
            vecControl_u[nIdx_j] := vecU_Min[nIdx_j];
        END_IF;
    END_FOR;
END_FOR;

(* Store Preceding Control Scan Vector *)
FOR nIdx_j := 1 TO 8 DO
    vecControl_u_prev[nIdx_j] := vecControl_u[nIdx_j];
END_FOR;
''')

    # Module 8 (12-Stage FSM)
    parts.append('''(*
====================================================================================================
  CYCLIC EXECUTION MODULE 8: 12-STAGE COMPREHENSIVE POWERTRAIN FINITE STATE MACHINE (FSM)
====================================================================================================
*)
tStateDwellTimer := tStateDwellTimer + rConst_ScanDeltaTime;

CASE eCurrentState OF
    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 0: TRANSMISSION POWER-ON SELF-TEST (POST) & ACTUATOR PRE-ARMING                    *)
    (* ----------------------------------------------------------------------------------------- *)
    0:
        wTransmissionFSMState := 16#0000;
        bTransmissionInGear := FALSE;
        bPowerShiftActive := FALSE;
        bEmergencyNeutralActive := FALSE;
        bClutch1VentValveOpen := TRUE;
        bClutch2VentValveOpen := TRUE;
        rClutch1PressureSetpoint_bar := 0.0;
        rClutch2PressureSetpoint_bar := 0.0;
        rLinePressurePumpCmd_Pct := 35.0;

        IF tStateDwellTimer >= rTargetDuration_Post THEN
            IF bLinePress_ChA_Healthy OR bLinePress_ChB_Healthy OR bLinePress_ChC_Healthy THEN
                eCurrentState := 1; (* Advance to Accumulator Charge *)
                tStateDwellTimer := 0.0;
                bClutch1VentValveOpen := FALSE;
                bClutch2VentValveOpen := FALSE;
            ELSE
                dwAlarmWord_Severe.1 := TRUE; (* Line Pressure Sensor Loss in POST *)
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 1: HYDRAULIC PRESSURE ACCUMULATOR CHARGING & LINE PRESSURE PRIMING                 *)
    (* ----------------------------------------------------------------------------------------- *)
    1:
        wTransmissionFSMState := 16#0001;
        rLinePressurePumpCmd_Pct := 85.0; (* High pump displacement *)
        tAccumulatorChargeTimer := tAccumulatorChargeTimer + rConst_ScanDeltaTime;

        IF rMainLinePressure_Voted >= 38.0 THEN
            rLinePressurePumpCmd_Pct := 45.0; (* Modulate to standby maintenance duty *)
            IF NOT bKissPointCalibrated THEN
                eCurrentState := 2; (* Advance to Static Kiss-Point Self-Learn *)
            ELSE
                eCurrentState := 3; (* Pre-Select 1st Gear *)
            END_IF;
            tStateDwellTimer := 0.0;
            tAccumulatorChargeTimer := 0.0;
        ELSIF tAccumulatorChargeTimer > rTargetDuration_Charge THEN
            dwAlarmWord_Warning.3 := TRUE; (* Accumulator Charge Slow Advisory *)
            eCurrentState := 3; (* Proceed with caution *)
            tStateDwellTimer := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 2: STATIC KISS-POINT SELF-LEARN ROUTINE (ACTIVE MICRO-SLIP CALIBRATION)             *)
    (* ----------------------------------------------------------------------------------------- *)
    2:
        wTransmissionFSMState := 16#0002;
        bCalibrationInProgress := TRUE;

        (* Ensure shift rails are in verified neutral before applying calibration pressure *)
        arrRailPosition_Target[1] := 0.0;
        arrRailPosition_Target[2] := 0.0;
        arrRailPosition_Target[3] := 0.0;
        arrRailPosition_Target[4] := 0.0;

        IF NOT bCalibrationComplete_C1 THEN
            (* Ramp Clutch 1 Apply Pressure *)
            rCalibratedRampPressure := rCalibratedRampPressure + (rCalibrationRampRate_BarS * rConst_ScanDeltaTime);
            rClutch1PressureSetpoint_bar := rCalibratedRampPressure;
            rClutch1CurrentCommand_mA := (rCalibratedRampPressure / 20.0) * 1500.0;

            (* Micro-Touch Point Detection Criteria *)
            IF (rClutch1EstimatedTorque_Nm >= rMicroTouchTorqueThresh_Nm)
               OR (rEngineSpeed_Voted <= (600.0 - rMicroTouchDroopThreshold_RPM))
               OR (rShaft1Speed_Voted >= 45.0) THEN
                
                (* Update Base Kiss-Point via Exponential Smoothing Filter *)
                rKissPointPressure_C1_Base := rKissPointPressure_C1_Base
                                            + rAdaptationGainAlpha * (rCalibratedRampPressure - rKissPointPressure_C1_Base);
                bCalibrationComplete_C1 := TRUE;
                rCalibratedRampPressure := 0.0;
                rClutch1PressureSetpoint_bar := 0.0;
                rClutch1CurrentCommand_mA := 0.0;
            END_IF;
            
            (* Safeguard Abort Threshold *)
            IF rCalibratedRampPressure >= 7.50 THEN
                bCalibrationComplete_C1 := TRUE;
                rCalibratedRampPressure := 0.0;
                rClutch1PressureSetpoint_bar := 0.0;
                dwAlarmWord_Severe.2 := TRUE; (* Kiss-point out of range *)
            END_IF;
        ELSIF NOT bCalibrationComplete_C2 THEN
            (* Ramp Clutch 2 Apply Pressure *)
            rCalibratedRampPressure := rCalibratedRampPressure + (rCalibrationRampRate_BarS * rConst_ScanDeltaTime);
            rClutch2PressureSetpoint_bar := rCalibratedRampPressure;
            rClutch2CurrentCommand_mA := (rCalibratedRampPressure / 20.0) * 1500.0;

            IF (rClutch2EstimatedTorque_Nm >= rMicroTouchTorqueThresh_Nm)
               OR (rEngineSpeed_Voted <= (600.0 - rMicroTouchDroopThreshold_RPM))
               OR (rShaft2Speed_Voted >= 45.0) THEN
                
                rKissPointPressure_C2_Base := rKissPointPressure_C2_Base
                                            + rAdaptationGainAlpha * (rCalibratedRampPressure - rKissPointPressure_C2_Base);
                bCalibrationComplete_C2 := TRUE;
                rCalibratedRampPressure := 0.0;
                rClutch2PressureSetpoint_bar := 0.0;
                rClutch2CurrentCommand_mA := 0.0;
            END_IF;

            IF rCalibratedRampPressure >= 7.50 THEN
                bCalibrationComplete_C2 := TRUE;
                rCalibratedRampPressure := 0.0;
                rClutch2PressureSetpoint_bar := 0.0;
                dwAlarmWord_Severe.2 := TRUE;
            END_IF;
        ELSE
            bCalibrationInProgress := FALSE;
            bKissPointCalibrated := TRUE;
            eCurrentState := 3; (* Advance to Pre-Select 1st Gear *)
            tStateDwellTimer := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 3: PRE-SELECT 1ST GEAR SHIFT RAIL ENGAGEMENT & DOG DETENT LOCK                     *)
    (* ----------------------------------------------------------------------------------------- *)
    3:
        wTransmissionFSMState := 16#0003;
        nPreselectedTargetGear := 1;
        arrRailPosition_Target[1] := 18.0; (* Drive Rail 1 to +18.00 mm (1st Gear) *)

        IF arrRailInDetentLock[1] AND (arrRailPosition_Actual[1] >= 17.65) THEN
            bTransmissionInGear := TRUE;
            nCurrentActiveGear := 1;
            IF bOperatorDrivePermissive AND bParkBrakeReleased THEN
                eCurrentState := 4; (* Advance to Launch Clutch Modulation *)
                tStateDwellTimer := 0.0;
            END_IF;
        ELSIF tStateDwellTimer >= rAlarmShiftRailTimeoutSec THEN
            dwAlarmWord_Severe.3 := TRUE; (* Shift rail timeout *)
            eCurrentState := 0; (* Fallback to POST reset *)
            tStateDwellTimer := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 4: LAUNCH CLUTCH MODULATED ENGAGEMENT & VEHICLE CREEP CONTROL                      *)
    (* ----------------------------------------------------------------------------------------- *)
    4:
        wTransmissionFSMState := 16#0004;
        nCurrentActiveGear := 1;

        (* Check Hill-Hold Condition *)
        IF bHillHoldRequest AND (rRoadGradientGrade > 3.0) THEN
            eCurrentState := 10; (* Transfer to Hill-Hold Standstill *)
            tStateDwellTimer := 0.0;
        ELSE
            (* Modulate Clutch 1 Pressure proportional to driver throttle pedal *)
            rScratch1 := rKissPointPressure_C1_Comp + (rAcceleratorPedalPos / 100.0) * 12.0;
            IF rScratch1 > 18.5 THEN
                rScratch1 := 18.5;
            END_IF;
            rClutch1PressureSetpoint_bar := rScratch1;
            rClutch1CurrentCommand_mA := (rScratch1 / 20.0) * 1500.0;

            (* Pre-Synchronize Next Target Gear (Gear 2 Even on Rail 3) *)
            nPreselectedTargetGear := 2;
            arrRailPosition_Target[3] := 18.0; (* Rail 3 to +18.0 mm (2nd Gear) *)

            (* Check for Lockup Synchronization: Clutch 1 Slip < 25 RPM *)
            IF ABS(rEngineSpeed_Voted - rShaft1Speed_Voted) <= 25.0 AND (rVehicleSpeedKmh > 5.0) THEN
                rClutch1PressureSetpoint_bar := 18.5; (* Full Lockup Clamping *)
                rClutch1CurrentCommand_mA := 1420.0;
                eCurrentState := 5; (* Steady-State In-Gear Cruise *)
                tStateDwellTimer := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 5: STEADY-STATE IN-GEAR LOCKED CRUISE & EFFICIENCY MONITORING                      *)
    (* ----------------------------------------------------------------------------------------- *)
    5:
        wTransmissionFSMState := 16#0005;
        bPowerShiftActive := FALSE;
        bTransmissionInGear := TRUE;

        (* Maintain Lockup on Active Driving Clutch *)
        IF (nCurrentActiveGear MOD 2) = 1 THEN
            rClutch1PressureSetpoint_bar := 18.5; (* Odd gear locked on C1 *)
            rClutch1CurrentCommand_mA := 1420.0;
            rClutch2PressureSetpoint_bar := 0.0;
            rClutch2CurrentCommand_mA := 0.0;
        ELSE
            rClutch2PressureSetpoint_bar := 18.5; (* Even gear locked on C2 *)
            rClutch2CurrentCommand_mA := 1420.0;
            rClutch1PressureSetpoint_bar := 0.0;
            rClutch1CurrentCommand_mA := 0.0;
        END_IF;

        (* Check for Target Gear Shift Request from Powertrain Supervisory *)
        IF (nTargetGearRequest <> nCurrentActiveGear) AND (nTargetGearRequest >= 1) AND (nTargetGearRequest <= 12) THEN
            nPreselectedTargetGear := nTargetGearRequest;
            eCurrentState := 6; (* Advance to Shift Pre-Select *)
            tStateDwellTimer := 0.0;
        END_IF;

        (* Standstill Creep / Neutral Drop Check *)
        IF (rVehicleSpeedKmh < 0.5) AND bBrakePedalDepressed THEN
            tStandstillTimeout := tStandstillTimeout + rConst_ScanDeltaTime;
            IF tStandstillTimeout > 3.0 THEN
                rClutch1PressureSetpoint_bar := rKissPointPressure_C1_Comp - 0.50; (* Drop to Standby Cushion *)
                rClutch2PressureSetpoint_bar := rKissPointPressure_C2_Comp - 0.50;
            END_IF;
        ELSE
            tStandstillTimeout := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 6: SHIFT PRE-SELECT NEXT TARGET GEAR & BAULK CONE SYNCHRONIZATION                  *)
    (* ----------------------------------------------------------------------------------------- *)
    6:
        wTransmissionFSMState := 16#0006;
        
        (* Target shift rail selection and displacement positioning *)
        CASE nPreselectedTargetGear OF
            1: arrRailPosition_Target[1] := 18.0;
            2: arrRailPosition_Target[3] := 18.0;
            3: arrRailPosition_Target[1] := -18.0;
            4: arrRailPosition_Target[3] := -18.0;
            5: arrRailPosition_Target[2] := 18.0;
            6: arrRailPosition_Target[4] := 18.0;
            7: arrRailPosition_Target[2] := -18.0;
            8: arrRailPosition_Target[4] := -18.0;
            9: arrRailPosition_Target[1] := 18.0;
            10: arrRailPosition_Target[3] := 18.0;
            11: arrRailPosition_Target[1] := -18.0;
            12: arrRailPosition_Target[4] := -18.0;
        END_CASE;

        (* Pre-Fill Oncoming Clutch to Cushion Pressure (P_kiss - 0.20 bar) *)
        IF (nPreselectedTargetGear MOD 2) = 1 THEN
            rClutch1PressureSetpoint_bar := rKissPointPressure_C1_Comp - 0.20;
            rClutch1CurrentCommand_mA := ((rKissPointPressure_C1_Comp - 0.20) / 20.0) * 1500.0;
        ELSE
            rClutch2PressureSetpoint_bar := rKissPointPressure_C2_Comp - 0.20;
            rClutch2CurrentCommand_mA := ((rKissPointPressure_C2_Comp - 0.20) / 20.0) * 1500.0;
        END_IF;

        (* Verify Oncoming Shift Rail Reached Positive Detent *)
        IF tStateDwellTimer >= 0.085 THEN
            eCurrentState := 7; (* Initiate Cross-Fill Torque Handoff *)
            tStateDwellTimer := 0.0;
            tPowershiftTimer := 0.0;
            tTorquePhaseTimer := 0.0;
            bPowerShiftActive := TRUE;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 7: OVERLAPPING CROSS-FILL POWER-SHIFT TORQUE HANDOFF                               *)
    (* ----------------------------------------------------------------------------------------- *)
    7:
        wTransmissionFSMState := 16#0007;
        tPowershiftTimer := tPowershiftTimer + rConst_ScanDeltaTime;
        tTorquePhaseTimer := tTorquePhaseTimer + rConst_ScanDeltaTime;

        (* Linear Torque Cross-Fill Ratio Alpha in [0.0, 1.0] *)
        rScratch1 := tTorquePhaseTimer / rTargetDuration_TorquePhase;
        IF rScratch1 > 1.0 THEN
            rScratch1 := 1.0;
        END_IF;

        IF (nCurrentActiveGear MOD 2) = 1 THEN
            (* Odd (C1) to Even (C2) Powershift *)
            rClutch1PressureSetpoint_bar := (1.0 - rScratch1) * 18.5;
            rClutch2PressureSetpoint_bar := rKissPointPressure_C2_Comp + (rScratch1 * 12.5);
            rClutch1CurrentCommand_mA := (rClutch1PressureSetpoint_bar / 20.0) * 1500.0;
            rClutch2CurrentCommand_mA := (rClutch2PressureSetpoint_bar / 20.0) * 1500.0;
        ELSE
            (* Even (C2) to Odd (C1) Powershift *)
            rClutch2PressureSetpoint_bar := (1.0 - rScratch1) * 18.5;
            rClutch1PressureSetpoint_bar := rKissPointPressure_C1_Comp + (rScratch1 * 12.5);
            rClutch2CurrentCommand_mA := (rClutch2PressureSetpoint_bar / 20.0) * 1500.0;
            rClutch1CurrentCommand_mA := (rClutch1PressureSetpoint_bar / 20.0) * 1500.0;
        END_IF;

        (* Intervene Engine Torque via J1939 CAN TSC1 to Pull Down Engine Speed *)
        rEngineTorqueOverride_Nm := -250.0;

        IF tTorquePhaseTimer >= rTargetDuration_TorquePhase THEN
            eCurrentState := 8; (* Advance to Off-Going Rail Release *)
            tStateDwellTimer := 0.0;
            nCurrentActiveGear := nPreselectedTargetGear;
            nTotalPowershiftsCompleted := nTotalPowershiftsCompleted + 1;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 8: OFF-GOING SHIFT RAIL NEUTRAL RELEASE & GEAR CONSOLIDATION                       *)
    (* ----------------------------------------------------------------------------------------- *)
    8:
        wTransmissionFSMState := 16#0008;
        rEngineTorqueOverride_Nm := 0.0; (* Release Engine Torque Retard *)

        (* Fully vent off-going clutch *)
        IF (nCurrentActiveGear MOD 2) = 1 THEN
            rClutch2PressureSetpoint_bar := 0.0;
            rClutch2CurrentCommand_mA := 0.0;
            rClutch1PressureSetpoint_bar := 18.5; (* Lockup oncoming odd gear *)
            rClutch1CurrentCommand_mA := 1420.0;
            (* Retract Even Rails to Neutral *)
            arrRailPosition_Target[3] := 0.0;
            arrRailPosition_Target[4] := 0.0;
        ELSE
            rClutch1PressureSetpoint_bar := 0.0;
            rClutch1CurrentCommand_mA := 0.0;
            rClutch2PressureSetpoint_bar := 18.5; (* Lockup oncoming even gear *)
            rClutch2CurrentCommand_mA := 1420.0;
            (* Retract Odd Rails to Neutral *)
            arrRailPosition_Target[1] := 0.0;
            arrRailPosition_Target[2] := 0.0;
        END_IF;

        IF tStateDwellTimer >= 0.065 THEN
            eCurrentState := 9; (* Store Dynamic Adaptations *)
            tStateDwellTimer := 0.0;
            bPowerShiftActive := FALSE;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 9: DYNAMIC FRICTION ADAPTION STORAGE & NVRAM FLASH LATCH                           *)
    (* ----------------------------------------------------------------------------------------- *)
    9:
        wTransmissionFSMState := 16#0009;
        
        (* Evaluate shift quality and micro-adjust learned kiss-points *)
        IF tPowershiftTimer <= rTargetDuration_ShiftMax THEN
            (* Good shift duration -> gentle adaptation confirm *)
            rKissPointPressure_C1_Base := rKissPointPressure_C1_Base * 0.9995 + rCalibratedKissPressure_C1 * 0.0005;
            rKissPointPressure_C2_Base := rKissPointPressure_C2_Base * 0.9995 + rCalibratedKissPressure_C2 * 0.0005;
        END_IF;

        eCurrentState := 5; (* Return to Steady-State In-Gear Cruise *)
        tStateDwellTimer := 0.0;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 10: HILL-HOLD ANTI-ROLLBACK STANDSTILL BRAKE INTEGRATION                            *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        wTransmissionFSMState := 16#000A;
        tHillHoldTimer := tHillHoldTimer + rConst_ScanDeltaTime;

        (* Pre-load Clutch 1 to Bite Point to counter rollback torque before brake release *)
        rClutch1PressureSetpoint_bar := rKissPointPressure_C1_Comp + (rRoadGradientGrade * 0.35);
        IF rClutch1PressureSetpoint_bar > 12.0 THEN
            rClutch1PressureSetpoint_bar := 12.0;
        END_IF;
        rClutch1CurrentCommand_mA := (rClutch1PressureSetpoint_bar / 20.0) * 1500.0;

        IF (rAcceleratorPedalPos > 12.0) OR (NOT bHillHoldRequest) THEN
            eCurrentState := 4; (* Transition to Launch Modulation *)
            tStateDwellTimer := 0.0;
            tHillHoldTimer := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STATE 11: EMERGENCY NEUTRAL DUMP & HYDRAULIC CLUTCH VENT TRIP                            *)
    (* ----------------------------------------------------------------------------------------- *)
    11:
        wTransmissionFSMState := 16#000B;
        bEmergencyNeutralActive := TRUE;
        bPowerShiftActive := FALSE;
        bTransmissionInGear := FALSE;
        bClutch1VentValveOpen := TRUE;
        bClutch2VentValveOpen := TRUE;
        rClutch1PressureSetpoint_bar := 0.0;
        rClutch2PressureSetpoint_bar := 0.0;
        rClutch1CurrentCommand_mA := 0.0;
        rClutch2CurrentCommand_mA := 0.0;
        rEngineTorqueOverride_Nm := 0.0;
        rAntiJerkDampingTorque_Nm := 0.0;

        (* Slew all shift rails back to neutral position *)
        arrRailPosition_Target[1] := 0.0;
        arrRailPosition_Target[2] := 0.0;
        arrRailPosition_Target[3] := 0.0;
        arrRailPosition_Target[4] := 0.0;
END_CASE;
''')

    # Module 9 (ISA-18.2 Alarms)
    parts.append('''(*
====================================================================================================
  CYCLIC EXECUTION MODULE 9: ISA-18.2 MULTI-TIERED ALARM MATRIX & TELEMETRY BIT-PACKING
====================================================================================================
*)
(* Priority 1 Emergency Trips *)
IF rClutch1PlateTemp >= rAlarmClutchTemp_HH OR rClutch2PlateTemp >= rAlarmClutchTemp_HH THEN
    dwAlarmWord_Trips.1 := TRUE; (* Clutch Plate Overtemperature Trip HH (> 220 C) *)
    eCurrentState := 11;
END_IF;

IF rMainLinePressure_Voted <= rAlarmLinePress_LL THEN
    dwAlarmWord_Trips.2 := TRUE; (* Line Pressure Complete Loss Trip LL (< 16 bar) *)
    eCurrentState := 11;
END_IF;

(* Simultaneous Odd / Even Rail Engagement Interlock *)
IF (arrRailInDetentLock[1] AND arrRailInDetentLock[2]) OR (arrRailInDetentLock[3] AND arrRailInDetentLock[4]) THEN
    dwAlarmWord_Trips.3 := TRUE; (* Mechanical Dog Double Engagement Lockout Trip *)
    eCurrentState := 11;
END_IF;

(* Priority 2 Severe Process Deviations *)
IF ABS(rKissPointPressure_C1_Comp - rKissPointPressure_C1_Base) > rAlarmKissPointDriftMaxBar THEN
    dwAlarmWord_Severe.2 := TRUE; (* Kiss-point drift exceeded tolerance *)
END_IF;

(* Continuous Clutch Slip Duration Accumulator *)
IF (rActiveSlipSpeedRadS > 2.0) AND ((rClutch1PressureSetpoint_bar > 5.0) OR (rClutch2PressureSetpoint_bar > 5.0)) THEN
    tActiveClutchSlipTimer := tActiveClutchSlipTimer + rConst_ScanDeltaTime;
    IF tActiveClutchSlipTimer >= rAlarmMaxSlipDurationSec THEN
        dwAlarmWord_Severe.3 := TRUE; (* Continuous Slip Duration Exceeded *)
    END_IF;
ELSE
    tActiveClutchSlipTimer := 0.0;
END_IF;

(* Priority 3 Advisory Warnings *)
IF (rClutch1PlateTemp >= rAlarmClutchTemp_H) OR (rClutch2PlateTemp >= rAlarmClutchTemp_H) THEN
    dwAlarmWord_Warning.1 := TRUE; (* High Clutch Temperature Warning (> 175 C) *)
END_IF;

IF (rMainLinePressure_Voted >= rAlarmLinePress_HH) THEN
    dwAlarmWord_Warning.2 := TRUE; (* High Hydraulic Line Pressure Warning *)
END_IF;

(* Clutch Cooling Lubrication Flow Modulation *)
IF (rClutch1PlateTemp > 120.0) OR (rClutch2PlateTemp > 120.0) OR bPowerShiftActive THEN
    rClutchCoolingValveCmd_Pct := 100.0; (* Full cooling oil flood *)
ELSE
    rClutchCoolingValveCmd_Pct := 25.0;  (* Baseline circulation *)
END_IF;

END_FUNCTION_BLOCK
''')

    code_text = "".join(parts)
    return code_text

if __name__ == "__main__":
    code = generate_iec_st()
    print(f"Generated Code Character Count: {len(code)}")
