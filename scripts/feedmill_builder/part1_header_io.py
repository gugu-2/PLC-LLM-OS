# scripts/feedmill_builder/part1_header_io.py
# -*- coding: utf-8 -*-

def get_header_and_io():
    return """FUNCTION_BLOCK FB_FeedMill_Conditioner_PelletPress_Cooler
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA SPECIFICATION
  CORE SECTOR    : AGRICULTURE & ANIMAL FEED PROCESSING MACHINERY
  APPLICATION    : HIGH-CAPACITY COMMERCIAL ANIMAL FEED PELLETING COMPLEX (30 METRIC TONS/HOUR MASH THROUGHPUT)
  MACHINE TRAIN  : 1. DUAL-SHAFT HIGH-RETENTION CONDITIONING CYLINDER (DDC / HRTC) WITH CULINARY DRY STEAM INJECTION
                   2. 400 kW RING-DIE PELLET PRESS WITH INDEPENDENT HYDRAULIC GAP ADJUSTMENT & SHEAR PIN BYPASS
                   3. COUNTERFLOW AMBIENT AIR PELLET COOLER WITH ROTARY LEVEL SENSOR GRID DISCHARGE
                   4. HIGH-PRECISION VACUUM FAT & POST-PELLET LIQUID ENZYME COATING SYSTEM
  FUNCTION BLOCK : FB_FeedMill_Conditioner_PelletPress_Cooler
  P&ID TAGGING   : ISA-5.1 COMPLIANT INSTRUMENTATION DESIGNATION (TE, PT, JT, LT, WT, ST, ZT SERIES 100-400)
  REDUNDANCY     : 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ON CRITICAL PROCESS MEASUREMENT TRIPLETS
  CYBER-PHYSICS  : 8x8 MULTIVARIABLE DISCRETE STATE-SPACE MODEL (Ts = 50 ms) WITH RECEDING-HORIZON MPC
  THERMODYNAMICS : DRY SATURATED CULINARY STEAM MASS/ENTHALPY BALANCE & CHUNG-PFOST EMC COOLING ISOTHERMS
  KINETICS       : MODIFIED ARRHENIUS DYNAMIC STARCH GELATINIZATION OBSERVER WITH WATER ACTIVITY CORRELATION
  TRIBOLOGY      : PELLET DIE COMPRESSION FRICTION WEDGE, ROLLER TRACTION SLIP & SEC ENERGY CONSUMPTION
  SAFETY NORMS   : EN ISO 13849-1 (CAT 3, PL d), IEC 61508 (SIL 2), EN 60204-1, ISA-18.2 ALARM ENGINE
  FSM TOPOLOGY   : 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
========================================================================================================================

  THEORETICAL AND MATHEMATICAL FOUNDATION:

  1. DUAL-SHAFT HIGH-RETENTION CONDITIONER (DDC / HRTC) STEAM MASS & ENTHALPY BALANCE:
     Conditioning raw mash meal (corn, wheat, soybean meal, DDGS) is required to hydrolyze starch, activate natural
     adhesives, plasticize proteins, and kill pathogenic bacteriological micro-flora (e.g., Salmonella enterica at 85-90 deg C).
     Dry saturated culinary steam at supply pressure P_steam = 2.5 bar(g) (3.5 bar absolute, Tsat = 138.88 deg C)
     is injected into the dual counter-rotating paddle shafts.
     
     Thermodynamic properties of dry saturated steam at 2.5 bar(g):
         Specific enthalpy of saturated vapor:  h_g  = 2,732.4 kJ/kg
         Specific enthalpy of saturated liquid: h_f  =   584.3 kJ/kg
         Latent heat of vaporization:          h_fg = 2,148.1 kJ/kg
         Specific volume of saturated vapor:    v_g  =   0.524 m3/kg

     Dynamic mass balance of moisture in conditioner cylinder:
         d(M_mash * w_mash) / dt = m_dot_feed * w_inlet + m_dot_steam_cond - m_dot_discharge * w_mash
     Where:
         M_mash              = Instantaneous mash holdup mass in conditioner cylinder [kg]
         m_dot_feed          = Raw meal gravimetric inlet mass flow rate [kg/s]
         w_inlet             = Raw meal incoming moisture fraction [% w/w]
         w_mash              = Conditioned mash exit moisture fraction [% w/w]
         m_dot_steam_cond    = Mass flow rate of condensing culinary steam [kg/s]
         m_dot_discharge     = Mash mass discharge rate into pellet press feed chute [kg/s]

     Dynamic thermal energy enthalpy balance:
         M_mash * c_p_mash * (dT_mash / dt) = m_dot_feed * c_p_mash * (T_inlet - T_mash)
                                             + m_dot_steam * [h_g - c_p_water * T_mash]
                                             - U_loss * A_shell * (T_mash - T_ambient)
                                             + P_shaft_mech * eta_shaft
     Where:
         c_p_mash            = Specific heat capacity of poultry/swine mash = 1.88 kJ/(kg*K)
         c_p_water           = Specific heat capacity of liquid water = 4.184 kJ/(kg*K)
         U_loss * A_shell    = Overall thermal heat dissipation conductance of insulated barrel [kW/K]
         P_shaft_mech        = Mechanical shaft agitation power transferred as frictional heat [kW]
         eta_shaft           = Electromechanical conversion efficiency of paddle shaft drive (~0.88)

  2. STARCH GELATINIZATION REACTION KINETICS (MODIFIED ARRHENIUS DYNAMICS):
     Starch gelatinization index alpha_gel in [0.0, 1.0] quantifies the irreversible disruption of the crystalline
     amylose/amylopectin lamellae within grain endosperm granules under hydrothermal shear.
     The reaction rate is governed by an empirical multi-factor Arrhenius equation:
         d(alpha_gel) / dt = k_0 * exp( -E_a / (R_gas * (T_mash + 273.15)) )
                           * [MAX(0.0, (w_mash - w_crit) / w_ref)]^beta_w
                           * (1.0 + gamma_shear * N_shaft)
                           * (1.0 - alpha_gel)^n_order
     Where:
         k_0         = Pre-exponential kinetic frequency constant = 1.25E7 s^-1
         E_a         = Apparent thermal activation energy = 68.50 kJ/mol = 68,500 J/mol
         R_gas       = Universal ideal gas constant = 8.314 J/(mol*K)
         w_crit      = Critical moisture threshold below which gelatinization cannot occur = 11.8% w/w
         w_ref       = Reference moisture scaling parameter = 5.0% w/w
         beta_w      = Non-linear moisture plasticization exponent = 1.45
         N_shaft     = Rotational speed of conditioner dual paddle shafts [rpm]
         gamma_shear = Hydrodynamic shear augmentation coefficient = 0.0028 rpm^-1
         n_order     = Apparent reaction order of starch crystal melting = 1.20
     High gelatinization (alpha_gel >= 0.55) significantly enhances Pellet Durability Index (PDI > 96.5%),
     lowers pellet mill motor Specific Energy Consumption (SEC), and eliminates pathogenic bacteria.

  3. 400 kW RING-DIE PELLET PRESS TRIBOLOGY & DYNAMIC HYDRAULIC ROLLER GAP MECHANICS:
     The pellet press forces conditioned plasticized mash through radial cylindrical holes in a rotating ring die
     using two cylindrical press rollers (Roll #1 and Roll #2).
     
     A. Mechanical Power, Torque, and Specific Energy Consumption (SEC):
        For a 400 kW, 400 V, 50 Hz 3-phase induction motor:
            Full-Load Continuous Current: I_FLC = 715.0 A
            Active Electrical Power:      P_act_kW = sqrt(3) * V_LL * I_RMS * cos_phi * eta_motor / 1000.0
            Motor Shaft Torque:           M_torque_Nm = (P_act_kW * 1000.0) / (2.0 * PI * (N_motor_rpm / 60.0))
            Die Rotational Speed:         N_die_rpm = N_motor_rpm / i_gearbox
            Specific Mechanical Energy:   SEC_kWh_ton = P_act_kW / MAX(1.0, m_dot_feed_tph)
        Target SEC for 30 t/h broilers/finisher feed: 9.0 to 12.5 kWh/ton.
        Excessive SEC (> 14.5 kWh/ton) signals die hole scouring, low steam conditioning, or excessive roller pinch.

     B. Dynamic Hydraulic Roller Gap Control:
        Each roller is positioned by high-pressure double-acting hydraulic cylinders with integrated LVDT transducers.
        Operating gap g_roller range: 0.20 mm to 2.50 mm (nominal target 0.50 mm to 0.75 mm).
        Dynamic mash extrusion wedge pressure:
            P_wedge(g) = P_comp_0 * exp( (g_ref - g_roller) / delta_gap )
        Opposing hydraulic ram force balance:
            M_roller * (d2 g_roller / dt2) + c_damping * (dg_roller / dt) = F_hyd - F_extrusion_radial
        Ring die thermal expansion dynamic compensation:
            Delta_g_thermal = alpha_die_steel * D_die_nominal * (T_die_surface - T_die_ambient)
        Where:
            alpha_die_steel = 1.25E-5 K^-1 (AISI 420 chrome-moly stainless die steel)
            D_die_nominal   = 900.0 mm (internal working track diameter)
        As the die heats up from 25 deg C to 105 deg C, the die ring expands radially by:
            Delta_g = 1.25E-5 * 900.0 * 80.0 = 0.90 mm
        The dynamic hydraulic gap controller must automatically retract the rollers by 0.90 mm to maintain
        constant effective mechanical clearance, preventing metal-to-metal die-roller scuffing and catastrophic die failure.

     C. Dynamic Roller Traction Slip Observer:
        Roller slip occurs when the friction coefficient between incoming mash and roller surface breaks down,
        causing mash build-up, motor stall, and instant die choking (plugging).
        Linear peripheral speeds:
            v_die    = PI * D_die_internal * (N_die_rpm / 60.0)
            v_roller = PI * D_roller_outer * (N_roller_rpm / 60.0)
        Dynamic Slip Ratio S_slip in [0.0, 1.0]:
            S_slip = ABS(v_die - v_roller) / MAX(0.01, v_die)
        Normal operation: S_slip <= 0.05 (5% micro-slip).
        Warning threshold: S_slip >= 0.15 (15% slip - impending choke; trigger emergency steam & gap trim).
        Trip threshold:    S_slip >= 0.35 (35% slip - immediate die overload bypass flap diversion).

     D. Overload Shear Pin Protection & Pneumatic Die Bypass Flap:
        The main shaft driving the ring die is mechanically safeguarded by dual calibrated shear pins.
        If motor current exceeds 760 A for > 500 ms, or if shear pin limit switches (DI207) open:
        Instantaneous safety interlock diverts incoming mash to the bypass chute within 150 ms,
        relieving extrusion pressure and stopping main drive coasting.

  4. COUNTERFLOW AMBIENT AIR PELLET COOLER THERMODYNAMICS:
     Hot extruded pellets exit the die at 82-90 deg C with 15.5-16.5% moisture.
     Pellets must be cooled to within +3 deg C of ambient temperature and dried to <= 12.5% moisture (a_w < 0.65)
     for safe silo storage without mold spore propagation.
     
     A. Mass and Bed Residence Time Dynamics:
        Counterflow cooler active cross-sectional area: A_cooler = 6.25 m2 (2.5 m x 2.5 m square bed).
        Pellet bulk density: rho_bulk = 650.0 kg/m3.
        Bed height: h_bed in [300 mm, 1400 mm] (nominal 950 mm).
        Instantaneous pellet bed holdup mass:
            M_bed = A_cooler * (h_bed / 1000.0) * rho_bulk [kg]
        Bed residence retention time:
            tau_cool = M_bed / (m_dot_feed_tph * 1000.0 / 60.0) [minutes]
        At 30 t/h and 950 mm bed depth: M_bed = 6.25 * 0.95 * 650 = 3,859 kg.
        tau_cool = 3,859 / 500 = 7.72 minutes.

     B. Psychrometric Evaporative Cooling and Chung-Pfost Equilibrium Moisture Content (EMC):
        Ambient air is drawn upwards through the descending pellet bed via a 55 kW variable-pitch centrifugal fan.
        Evaporative cooling carries away latent heat:
            Q_dot_latent = m_dot_evap * h_fg_water
        Sensible cooling transfers heat to counterflowing air:
            Q_dot_sensible = m_dot_air * c_p_air * (T_air_exhaust - T_air_inlet)
        Equilibrium Moisture Content (EMC) of grain pellets is calculated via the Chung-Pfost equation:
            EMC_pct = (1.0 / -C_cp_1) * LN( - (R_gas * (T_air_inlet + C_cp_2) * LN(RH_ambient / 100.0)) / C_cp_3 )
        Where for balanced poultry feed: C_cp_1 = 0.165, C_cp_2 = 35.80, C_cp_3 = 452.0.
        The discharge grid stroke frequency is modulated to hold bed level at 950 mm while ensuring
        residence time >= 7.5 minutes to achieve targeted core pellet moisture of 12.2%.

  5. BATCH VACUUM FAT & POST-PELLET LIQUID ENZYME COATING SYSTEM:
     Post-pellet coating applies liquid poultry fat / soybean oil (3% to 8% inclusion) and thermo-sensitive
     enzymes/vitamins (phytase, xylanase, beta-glucanase) without thermal degradation.
     Cyclic batch operation (500 kg per batch):
         Step 1: Charge 500 kg cooled screened pellets into pressurized vacuum chamber.
         Step 2: Evacuate chamber to P_vac = -0.85 bar(g) (150 mbar absolute) in < 18 seconds.
                 Under high vacuum, air trapped inside pellet capillary micropores is completely extracted.
         Step 3: Atomize heated liquid fat (at 55 deg C) through multi-nozzle high-pressure spray manifold
                 into the fluidized tumbling pellet bed.
         Step 4: Spray liquid enzyme aqueous solution in calibrated micro-doses (50 to 500 ppm).
         Step 5: Atmospheric Break / Controlled Vacuum Venting: Atmospheric air is admitted over 10 seconds.
                 The sudden atmospheric pressure differential drives the surface fat deep into the evacuated
                 pellet core pores, producing a dry, non-greasy exterior with zero fat leaching and PDI > 97.5%.
         Step 6: Rapid slide gate discharge into finished feed distribution hopper.

  6. CYBER-PHYSICAL 8x8 DISCRETE STATE-SPACE MODEL (Ts = 50 ms):
     State vector x(k) in R^8:
         x1: Conditioned mash exit temperature T_mash [deg C] (Target: 90.0 deg C)
         x2: Conditioned mash exit moisture w_mash [% w/w] (Target: 16.0%)
         x3: Starch gelatinization extent index alpha_gel [0.0..1.0] (Target: 0.58)
         x4: Pellet mill 400 kW main drive motor current I_mill [A] (Target: 580.0 A)
         x5: Ring die friction surface temperature T_die [deg C] (Target: 98.0 deg C)
         x6: Twin roller hydraulic dynamic gap g_roller [mm] (Target: 0.65 mm)
         x7: Counterflow cooler bed depth h_bed [mm] (Target: 950.0 mm)
         x8: Cooled pellet core moisture equilibrium w_pellet [% w/w] (Target: 12.2%)

     Manipulated variable vector u(k) in R^6:
         u1: Feeder screw rotational speed command N_feeder [RPM] (0 to 180 RPM, scales 0 to 30 t/h)
         u2: Saturated culinary steam modulating globe valve position Y_steam [%] (0 to 100%)
         u3: Conditioner paddle shaft variable frequency drive N_shaft [RPM] (150 to 450 RPM)
         u4: Twin roller hydraulic servo proportional valve command Y_gap_hyd [%] (0 to 100%)
         u5: Counterflow cooler reciprocating discharge grid speed Y_grid [%] (0 to 100%)
         u6: Cooler exhaust centrifugal fan VFD speed command N_fan [%] (30 to 100%)

     Unmeasured/Measured Disturbance vector d(k) in R^3:
         d1: Raw mash incoming inlet temperature T_inlet [deg C] (Ambient 5 to 35 deg C)
         d2: Raw mash incoming inlet moisture w_inlet [% w/w] (10.5% to 13.5%)
         d3: Saturated steam header supply pressure P_steam_hdr [bar] (2.2 to 2.8 bar)

     Discrete state propagation equation:
         x(k+1) = A * x(k) + B * u(k) + E * d(k)
         y(k)   = C * x(k) + D * u(k)

  7. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) FORMULATION:
     Quadratic objective cost function over prediction horizon N_p = 3:
         J = SUM(k=1..3) [ (x_hat(k) - x_sp)^T * Q * (x_hat(k) - x_sp) ]
           + SUM(m=1..6) [ Delta_u(m)^T * R * Delta_u(m) ]
           + [ (x_hat(3) - x_sp)^T * P_term * (x_hat(3) - x_sp) ]
     Where:
         Q      = Diagonal state tracking penalty matrix:
                  Q = diag([4.5, 8.0, 25.0, 18.0, 2.0, 12.0, 5.0, 15.0])
                  Prioritizes starch gelatinization (25.0) and motor current avoidance (18.0).
         R      = Diagonal actuator slew rate penalty matrix:
                  R = diag([3.0, 6.0, 1.5, 8.0, 2.5, 2.0])
                  Penalizes excessive hunting of hydraulic gap servo (8.0) and steam valve (6.0).
         P_term = Terminal state weight matrix:
                  P_term = diag([9.0, 16.0, 50.0, 75.0, 4.0, 24.0, 10.0, 30.0])
                  Harsh penalty (75.0) on terminal motor current to guarantee absolute safety margin below FLC.
*)

VAR_INPUT
    (* Master System Commands & Operating Modes *)
    bEnable                         : BOOL;     (* Master Automation System Enable Command [BOOL] *)
    bReset                          : BOOL;     (* Master System Alarm and Trip Reset Pushbutton [BOOL] *)
    bAutoMode                       : BOOL;     (* Automatic Supervisory Pelleting Mode Active [BOOL] *)
    bFeederStartCmd                 : BOOL;     (* Operator Feeder Screw Start Permissive [BOOL] *)
    bPelletMillStartCmd             : BOOL;     (* Operator 400 kW Pellet Mill Start Command [BOOL] *)
    bCoolerAutoDischargeCmd         : BOOL;     (* Cooler Automatic Level Discharge Enable [BOOL] *)
    bCoaterCycleStartCmd            : BOOL;     (* Vacuum Fat Coater Automatic Batch Enable [BOOL] *)

    (* Production Setpoints & Recipe Parameters *)
    rFeedRate_SP_tph                : REAL;     (* Target Raw Meal Production Feed Throughput [t/h] *)
    rTargetMashTemp_SP_degC         : REAL;     (* Conditioner Target Pasteurization Mash Temperature [deg C] *)
    rTargetMashMoist_SP_pct         : REAL;     (* Conditioner Conditioned Mash Target Moisture Setpoint [%] *)
    rTargetRollerGap_SP_mm          : REAL;     (* Ring Die Dynamic Hydraulic Roller Target Gap [mm] *)
    rTargetGelatinization_SP        : REAL;     (* Target Starch Hydrothermal Gelatinization Index [0.0..1.0] *)
    rTargetCoolerBed_SP_mm          : REAL;     (* Counterflow Pellet Cooler Regulated Bed Depth [mm] *)
    rTargetFinalMoist_SP_pct        : REAL;     (* Final Storage Pellets Moisture Setpoint [%] *)
    rFatInclusion_SP_pct            : REAL;     (* Vacuum Coater Liquid Fat Addition Setpoint [%] *)
    rEnzymeInclusion_SP_ppm         : REAL;     (* Post-Pellet Vacuum Liquid Enzyme Dose Setpoint [ppm] *)

    (* Raw Material & Steam Header Physical Disturbances *)
    rRawMashTemp_Inlet_degC         : REAL;     (* Incoming Raw Meal Mash Ambient Temperature [deg C] *)
    rRawMashMoist_Inlet_pct         : REAL;     (* Incoming Raw Meal Mash Moisture Content [%] *)
    rSteamHdrPress_Supply_bar       : REAL;     (* Culinary Saturated Steam Supply Header Pressure [bar] *)
    rSteamHdrTemp_Supply_degC       : REAL;     (* Culinary Saturated Steam Supply Header Temperature [deg C] *)

    (* 2oo3 TMR Triple Modular Redundancy Sensor Inputs - Conditioner Mash Temperature *)
    rCondTemp_TE101A_degC           : REAL;     (* Conditioner Discharge Mash Temp Sensor Triplet A [deg C] *)
    rCondTemp_TE101B_degC           : REAL;     (* Conditioner Discharge Mash Temp Sensor Triplet B [deg C] *)
    rCondTemp_TE101C_degC           : REAL;     (* Conditioner Discharge Mash Temp Sensor Triplet C [deg C] *)

    (* 2oo3 TMR Triple Modular Redundancy Sensor Inputs - Pellet Press 400 kW Motor Current *)
    rPressMotorCurrent_JT201A_A     : REAL;     (* Pellet Press Main Motor Phase A Current Transducer [A] *)
    rPressMotorCurrent_JT201B_A     : REAL;     (* Pellet Press Main Motor Phase B Current Transducer [A] *)
    rPressMotorCurrent_JT201C_A     : REAL;     (* Pellet Press Main Motor Phase C Current Transducer [A] *)

    (* 2oo3 TMR Triple Modular Redundancy Sensor Inputs - Dynamic Roller Gap Hydraulic Pressure *)
    rHydGapPress_PT202A_bar         : REAL;     (* Roller Dynamic Hydraulic Gap Pressure Transducer A [bar] *)
    rHydGapPress_PT202B_bar         : REAL;     (* Roller Dynamic Hydraulic Gap Pressure Transducer B [bar] *)
    rHydGapPress_PT202C_bar         : REAL;     (* Roller Dynamic Hydraulic Gap Pressure Transducer C [bar] *)

    (* 2oo3 TMR Triple Modular Redundancy Sensor Inputs - Counterflow Cooler Bed Level Probes *)
    rCoolerBedLevel_LT301A_mm       : REAL;     (* Counterflow Cooler Microwave Bed Level Sensor A [mm] *)
    rCoolerBedLevel_LT301B_mm       : REAL;     (* Counterflow Cooler Microwave Bed Level Sensor B [mm] *)
    rCoolerBedLevel_LT301C_mm       : REAL;     (* Counterflow Cooler Microwave Bed Level Sensor C [mm] *)

    (* Pellet Press Tribological & Kinematic Sensors *)
    rPressMotorVoltage_VT201_V      : REAL;     (* Pellet Press Motor Bus Line-to-Line Operating Voltage [V] *)
    rPressMotorCosPhi_JT202         : REAL;     (* Pellet Press Motor Power Factor Transducer [cos phi] *)
    rDieSurfaceTemp_TE203_degC      : REAL;     (* Ring Die Face Optical Infrared Pyrometer Temperature [deg C] *)
    rRoller1_RPM_ST204_rpm          : REAL;     (* Roller #1 Inductive Proximity Rotation Speed Sensor [rpm] *)
    rRoller2_RPM_ST205_rpm          : REAL;     (* Roller #2 Inductive Proximity Rotation Speed Sensor [rpm] *)
    rDieRing_RPM_ST206_rpm          : REAL;     (* Main Ring Die Heavy-Duty Magnetic Speed Pick-up [rpm] *)
    rRollerGapLVDT_Left_mm          : REAL;     (* Roller #1 Dynamic Linear Displacement LVDT Position [mm] *)
    rRollerGapLVDT_Right_mm         : REAL;     (* Roller #2 Dynamic Linear Displacement LVDT Position [mm] *)

    (* Counterflow Cooler Ambient Air Sensors *)
    rCoolerAirInletTemp_TE302_degC  : REAL;     (* Cooler Intake Ambient Cooling Air Temperature [deg C] *)
    rCoolerAirInletRH_ME302_pct     : REAL;     (* Cooler Intake Ambient Relative Humidity [%] *)
    rCoolerDischargePelletTemp_degC : REAL;     (* Cooled Pellets Discharge Gravity Chute Temperature [deg C] *)

    (* Vacuum Fat / Liquid Enzyme Coater Batch Sensors *)
    rCoaterVesselPress_PT401_bar    : REAL;     (* Vacuum Coater Chamber Pressure Transducer [bar] *)
    rCoaterBatchWeight_WT401_kg     : REAL;     (* Vacuum Coater Chamber Precision Load Cell Batch Weight [kg] *)

    (* Hardwired Discrete Safety Interlocks & Limit Switches *)
    bShearPin_Intact_DI207          : BOOL;     (* Main Shaft Mechanical Shear Pin Limit Switch (NC) [BOOL] *)
    bDieDoor_Closed_DI208           : BOOL;     (* Pellet Mill Heavy Cast Die Access Door Limit Switch [BOOL] *)
    bEmergStop_Circuit_OK           : BOOL;     (* Dual-Channel Hardwired Emergency Stop Safety Circuit [BOOL] *)
    bAckAlarms                      : BOOL;     (* Operator Alarm Acknowledge Pushbutton Signal [BOOL] *)
END_VAR

VAR_OUTPUT
    (* Primary Complex Status & Interlock Indicators *)
    bSysRunning                     : BOOL;     (* Complex Master Integrated Pelleting Plant Running [BOOL] *)
    bSysFault                       : BOOL;     (* Complex Critical Tripped Shutdown Active [BOOL] *)
    nFsmState_Active                : INT;      (* Active Operational FSM Stage Number 0-11 [INT] *)
    bEmergencyBypassActive          : BOOL;     (* High-Speed Die Overload Bypass Flap Gate Open [BOOL] *)

    (* Modulating Actuator Commands & Drive Speed References *)
    rCmdFeederSpeed_RPM             : REAL;     (* Variable Speed Feeder Screw Rotational Speed [RPM] *)
    rCmdSteamValve_pct              : REAL;     (* Saturated Culinary Steam Modulating Globe Valve Position [%] *)
    rCmdShaftSpeed_RPM              : REAL;     (* Dual-Shaft High-Retention Conditioner Paddle Drive [RPM] *)
    rCmdMillMotor_kW                : REAL;     (* Pellet Mill 400 kW Main Drive Electric Power Load [kW] *)
    rCmdGapHydServo_pct             : REAL;     (* Roller Dynamic Hydraulic Proportional Servo Position [%] *)
    bCmdBypassFlap_Divert           : BOOL;     (* Electro-Pneumatic Mash Reject / Die Bypass Flap Gate [BOOL] *)
    rCmdCoolerDischarge_pct         : REAL;     (* Counterflow Cooler Swivel Grid Discharge Hydraulic Speed [%] *)
    rCmdCoolerFan_pct               : REAL;     (* Counterflow Cooler Centrifugal Exhaust Fan VFD Speed [%] *)

    (* Vacuum Fat / Enzyme Batch Coater Discrete & Proportional Outputs *)
    bCmdCoaterVacuumPump            : BOOL;     (* Vacuum Coater Rotary Vane Evacuation Pump Run Command [BOOL] *)
    bCmdCoaterFatSprayValve         : BOOL;     (* Heated Liquid Fat High-Pressure Injection Valve [BOOL] *)
    bCmdCoaterEnzymeValve           : BOOL;     (* Liquid Micro-Enzyme High-Precision Metering Valve [BOOL] *)
    bCmdCoaterVentValve             : BOOL;     (* Atmospheric Vacuum Break Controlled Diffusive Vent Valve [BOOL] *)
    bCmdCoaterDischargeGate         : BOOL;     (* Coater Bottom Pneumatic Slide Discharge Gate Command [BOOL] *)

    (* Real-Time Cyber-Physical Observers & Predictive Properties *)
    rVoted_CondMashTemp_degC        : REAL;     (* 2oo3 TMR Validated Conditioner Mash Temperature [deg C] *)
    rVoted_PressMotorCurrent_A      : REAL;     (* 2oo3 TMR Validated Pellet Press Motor Phase Current [A] *)
    rVoted_HydGapPress_bar          : REAL;     (* 2oo3 TMR Validated Roller Dynamic Hydraulic Pressure [bar] *)
    rVoted_CoolerBedLevel_mm        : REAL;     (* 2oo3 TMR Validated Cooler Pellet Bed Height [mm] *)
    rEst_GelatinizationIndex        : REAL;     (* Dynamic Starch Hydrothermal Gelatinization Index [0.0..1.0] *)
    rEst_PelletDurabilityIndex_PDI  : REAL;     (* Real-time Holmen Pellet Durability Index PDI [%] *)
    rEst_SpecificEnergy_kWh_ton     : REAL;     (* Ring Die Specific Mechanical Energy Consumption [kWh/t] *)
    rEst_RollerSlipRatio            : REAL;     (* Pellet Mill Ring Die vs Roller Traction Slip Factor [0.0..1.0] *)
    rEst_CoolerRetentionTime_min    : REAL;     (* Counterflow Cooler Active Bed Residence Retention Time [min] *)
    rEst_PelletDischargeMoist_pct   : REAL;     (* Cooled Pellet Equilibrium Core Moisture Content [%] *)

    (* Packed ISA-18.2 Diagnostic & Alarm Status Words *)
    dwAlarms_Critical_HH            : DWORD;    (* ISA-18.2 Emergency Priority 1 Critical Trip Word [DWORD] *)
    dwAlarms_Warning_H_L            : DWORD;    (* ISA-18.2 Priority 2 Process Warning & Alert Word [DWORD] *)
    dwSensorHealth_Status           : DWORD;    (* 2oo3 TMR Sensor Triplets Health & Discrepancy Diagnostics [DWORD] *)
    dwFSM_Diagnostic_Word           : DWORD;    (* Operational Finite State Machine Diagnostics [DWORD] *)
    dwActuatorStatus_Word           : DWORD;    (* Electro-Hydraulic & Pneumatic Actuators Status Word [DWORD] *)
END_VAR
"""
