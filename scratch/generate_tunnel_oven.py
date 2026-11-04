# Generator script for FB_Bakery_ContinuousTunnelOven_MultiZone_Humidity
# LUMINA SWARM V7 MAX-PERSONA PROTOCOL

import json
import uuid
import os
import sys
import re

def generate_tunnel_oven_code():
    # We will build the entire Function Block string here.
    code_parts = []
    
    # -------------------------------------------------------------
    # 1. FUNCTION_BLOCK DECLARATION & COMPREHENSIVE HEADER COMMENT
    # -------------------------------------------------------------
    header = """FUNCTION_BLOCK FB_Bakery_ContinuousTunnelOven_MultiZone_Humidity
(*
 ==========================================================================================
  PROJECT:       INDUSTRIAL CYBER-PHYSICAL MANUFACTURING SYSTEMS (CPS-CMS)
  FACILITY:      HIGH-THROUGHPUT COMMERCIAL BAKERY PRODUCTION LINE
  EQUIPMENT:     6-ZONE CONTINUOUS BAKERY TUNNEL OVEN (60 METERS, 5,000 KG/H THROUGHPUT)
  DISCIPLINE:    MULTIVARIABLE THERMAL & MOISTURE MODEL PREDICTIVE CONTROL (MPC)
                 2oo3 TRIPLE MODULAR REDUNDANT (TMR) COMBUSTION SAFETY & SENSOR FUSION
                 ACTIVE PNEUMATIC WIRE-MESH BELT TRACKING & EDGE TENSION CENTERING
  IEC STANDARD:  IEC 61131-3 DETERMINISTIC STRUCTURED TEXT (3RD EDITION)
  SAFETY CODES:  NFPA 86 (STANDARD FOR OVENS AND FURNACES), EN 746-2, ISO 13849-1 (PL e)
 ==========================================================================================
  THEORETICAL ARCHITECTURE & CYBER-PHYSICAL FORMULATIONS:
  ------------------------------------------------------------------------------------------
  1. TUNNEL OVEN GEOMETRY & THERMODYNAMIC OVERVIEW:
     The continuous baking tunnel oven comprises six (6) distinct, independently modulated
     thermal zones distributed along a total active baking length L = 60.0 m with a useful
     baking hearth width W = 3.0 m, conveying a compound balanced weave high-temperature
     carbon-steel wire mesh belt. The nominal production throughput is 5,000 kg/h of dough,
     corresponding to approximately 6,250 standard 800-gram pan bread dough pieces per hour,
     with a typical residence time between 18.0 and 28.0 minutes (conveyor speed 2.14 to 3.33 m/min).

     The 6 thermal zones operate along a dedicated temperature and relative humidity gradient:
       - ZONE 1 (Steam Deposition & Oven Spring, L = 10.0 m):
         Atmosphere setpoint: 180.0 to 210.0 deg C. Chamber relative humidity: 65% to 75% RH.
         Direct saturated steam pulse injection (3.0 to 5.0 bar saturated steam) creates a
         condensing vapor blanket on cold incoming dough pieces (24 to 28 deg C). Condensation
         transfers high latent heat (h_fg = 2,120 kJ/kg), rapidly heating the outer dough layer,
         initiating starch gelatinization (55 to 65 deg C) which forms a glossy, elastic film.
         Crucially, the condensation prevents premature crust skinning, allowing the internal
         carbon dioxide (CO2), ethanol, and water vapor expansion to achieve maximum "oven spring"
         volume increase (+35% to +50% height) without surface rupture or cracking.
       - ZONE 2 (Crumb Gelatinization & Expansion, L = 10.0 m):
         Atmosphere setpoint: 210.0 to 230.0 deg C. Chamber relative humidity: 55% to 65% RH.
         Upper radiant heating and lower convection hearth heating drive heat transfer through
         the mesh belt into the dough base. Gluten protein coagulation occurs at 70 to 85 deg C,
         freezing the crumb cellular matrix structure.
       - ZONE 3 (Crumb Setting & Initial Drying, L = 10.0 m):
         Atmosphere setpoint: 220.0 to 240.0 deg C. Chamber relative humidity: 45% to 55% RH.
         Enzyme inactivation (alpha-amylase ceases at 85 to 90 deg C) and cellular pore stabilization.
         Moisture evaporation initiates internal vapor pressure gradient driving core-to-surface diffusion.
       - ZONE 4 (Moisture Extraction & Crust Hardening, L = 10.0 m):
         Atmosphere setpoint: 230.0 to 250.0 deg C. Chamber relative humidity: 40% to 45% RH.
         Modulated exhaust dampers extract evaporated water vapor. Surface drying lowers crust water
         activity below a_w = 0.70, elevating surface temperature above 100 deg C.
       - ZONE 5 (Browning & Maillard Reaction Kinetics, L = 10.0 m):
         Atmosphere setpoint: 240.0 to 260.0 deg C. Chamber relative humidity: 35% to 40% RH.
         High radiative heat transfer initiates non-enzymatic browning (Maillard condensation between
         reducing sugars and amino acids) and caramelization of sucrose, developing characteristic
         golden-brown crust pigments (melanoidins) and volatile aroma compounds.
       - ZONE 6 (Final Crust Crispness & Core Moisture Equalization, L = 10.0 m):
         Atmosphere setpoint: 200.0 to 220.0 deg C. Chamber relative humidity: 35% to 40% RH.
         Mild thermal soaking brings internal loaf crumb core temperature to target 96.0 to 98.0 deg C,
         completing bake-out while preventing excessive crust carbonization or moisture loss.

  2. CONJUGATE HEAT TRANSFER & MULTI-NODE THERMAL OBSERVER:
     The Function Block computes multi-modal heat flux into each dough loaf:
       a) Radiative Heat Flux (Upper Burner / Radiant Ceramic Tiles):
          q_rad,i = sigma * epsilon_eff * F_bd * (T_upper,i^4 - T_dough_surf^4)
          where sigma = 5.67037e-8 W/(m2.K4), epsilon_eff = 0.90, F_bd is the view factor (~0.85).
       b) Convective Heat Flux (Recirculating Combustion Flue Gas & Air):
          q_conv,i = h_c,i * (T_air,i - T_dough_surf)
          where h_c,i = Nu_i * k_air / D_h is dynamically evaluated from forced circulation blower speed.
       c) Conductive Heat Flux (Wire-Mesh Belt Contact to Loaf Base):
          q_cond,i = (k_eff / delta_mesh) * (T_belt,i - T_dough_base)
          accounting for wire-mesh thermal capacitance and contact resistance.
       d) Dough Multi-Node Internal Heat Conduction:
          A 3-node transient observer evaluates:
            - Crust surface temperature (T_dough_surf) subject to radiative/convective flux and evaporative heat loss.
            - Mid-crumb temperature (T_dough_mid) governing starch gelatinization and protein denaturation.
            - Loaf geometric core temperature (T_dough_core) determining internal bake completion.
          Evaporative cooling flux: q_evap = m_dot_evap * h_fg, where evaporation rate depends on
          the vapor pressure deficit: Delta_P_vapor = P_sat(T_dough_surf) - P_ambient_vapor.

  3. 8-STATE DISCRETE STATE-SPACE MODEL & KALMAN FILTER PREDICTION:
     The global oven dynamics are represented in discrete state-space form:
       x[k+1] = A * x[k] + B * u[k]
       y[k]   = C * x[k] + D * u[k]
     Sample period: Ts = 0.50 s.
     State vector x in R^8:
       x[1] = Zone 1-2 lumped upper radiation chamber temperature [deg C]
       x[2] = Zone 1-2 lumped lower convection hearth temperature [deg C]
       x[3] = Zone 3-4 intermediate zone temperature [deg C]
       x[4] = Zone 5-6 browning & finish zone temperature [deg C]
       x[5] = Chamber relative humidity state [% RH]
       x[6] = Wire-mesh conveyor belt dynamic thermal energy absorption [deg C]
       x[7] = Dough internal crumb core temperature observer state [deg C]
       x[8] = Flue exhaust draft negative pressure differential [mbar]

     Control input vector u in R^6:
       u[1] = Upper burner modulating fuel gas demand [%]
       u[2] = Lower burner modulating fuel gas demand [%]
       u[3] = Combustion air blower modulating airflow [%]
       u[4] = Zone 1 steam pulse injection valve command [%]
       u[5] = Flue exhaust moisture extraction damper position [%]
       u[6] = Wire-mesh conveyor belt speed setpoint [m/min]

  4. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC):
     The controller solves a discrete receding-horizon quadratic optimization problem:
       min J = sum_{i=1..Np} (x[k+i] - x_ref)^T * Q * (x[k+i] - x_ref)
             + sum_{j=0..Nu-1} delta_u[k+j]^T * R * delta_u[k+j]
             + (x[k+Np] - x_ref)^T * P * (x[k+Np] - x_ref)
     subject to:
       - Firing rate constraints: 0.0% <= u_gas <= 100.0%
       - Gas valve rate slew limits: |d(u_gas)/dt| <= 5.0 %/s
       - Stoichiometric combustion cross-limiting: Air flow must LEAD gas on load increase,
         and gas must LEAD air on load decrease, maintaining excess air ratio lambda >= 1.08.
       - Crumb core temperature error penalty heavily weighted in Q matrix to ensure
         exact 96.0 - 98.0 deg C exit temperature regardless of throughput fluctuations.

  5. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR FUSION & NFPA 86 SAFETY:
     All mission-critical measurements employ 2oo3 voting with discrepancy monitoring:
       - Zone 1 to 6 Upper Thermocouples: Triads A, B, C (Type K duplex mineral insulated).
       - Zone 1 to 6 Lower Thermocouples: Triads A, B, C.
       - High-Temperature Zirconia Humidity Probes: Triads A, B, C.
       - Flue Draft Pressure Transmitters: Triads A, B, C.
       - Wire-Mesh Conveyor Speed Encoders: Triads A, B, C.
       - Optical UV/IR Flame Scanners: Triads A, B, C per burner assembly.
     Voting Engine executes median calculation, detects drifting channels (> 8.0 deg C, > 5.0% RH),
     increments discrepancy timers, and enables seamless bumpless degradation (2oo3 -> 1oo2 -> 1oo1).
     Combustion safety interlocks enforce NFPA 86 compliance with double block-and-bleed fuel slam-shut
     in < 1.0 s upon flame failure, combustion air pressure loss, or exhaust draft failure.

  6. ACTIVE PNEUMATIC BELT TRACKING & EDGE TENSION CENTERING:
     The 60-meter wire mesh belt is vulnerable to lateral drift and camber runout.
     Dual proportional pneumatic steering cylinders apply lateral angular tilt to the idler shaft.
     Laser/optical edge sensors measure belt deviation (target: 0.0 mm +/- 2.0 mm).
     A dedicated closed-loop PI centering algorithm dynamically modulates left and right tracking
     pressures while load cells monitor catenary tension to prevent fatigue breakage or mesh distortion.
 ==========================================================================================
*)
"""
    code_parts.append(header)
    
    # -------------------------------------------------------------
    # 2. VAR_INPUT DECLARATION BLOCK
    # -------------------------------------------------------------
    var_input = """
VAR_INPUT
    (* ===================================================================================== *)
    (* 1. SYSTEM SUPERVISORY COMMANDS & SAFETY PERMISSIVES                                   *)
    (* ===================================================================================== *)
    bEnableSystem                   : BOOL;     (* Master oven system enable command permissive *)
    bEmergencyStop                  : BOOL;     (* SIL-3 hardwired E-stop safety circuit (Active High = Healthy) *)
    bResetFaults                    : BOOL;     (* Master alarm unlatch and safety fault acknowledgement *)
    bAutoBakeEnable                 : BOOL;     (* Master autonomous baking closed-loop governor permissive *)
    bSteamZone1Enable               : BOOL;     (* Permissive for Zone 1 saturated steam injection system *)
    bRecipeChangeoverReq            : BOOL;     (* Supervisory request for dynamic recipe changeover *)
    bMaintenanceManualOverride     : BOOL;     (* Maintenance manual actuator jog and test permissive *)
    bPurgeExhaustDamperOpenPerm     : BOOL;     (* Permissive confirmation from damper end-switches *)

    (* ===================================================================================== *)
    (* 2. SUPERVISORY PRODUCTION RECIPE SETPOINTS                                            *)
    (* ===================================================================================== *)
    rRecipe_Throughput_kgh          : REAL;     (* Target production mass throughput setpoint [kg/h] *)
    rRecipe_BakeTime_min            : REAL;     (* Recipe nominal total baking dwell time [min] *)
    rRecipe_BeltSpeedSP_mpm         : REAL;     (* Calculated nominal wire-mesh conveyor speed [m/min] *)
    rRecipe_ZoneTempSP_Upper_degC   : ARRAY[1..6] OF REAL; (* Zone 1-6 upper chamber temperature setpoints [deg C] *)
    rRecipe_ZoneTempSP_Lower_degC   : ARRAY[1..6] OF REAL; (* Zone 1-6 lower hearth temperature setpoints [deg C] *)
    rRecipe_ZoneRH_SP_pct           : ARRAY[1..6] OF REAL; (* Zone 1-6 chamber relative humidity setpoints [%] *)
    rRecipe_SteamPulseDuty_pct      : REAL;     (* Zone 1 steam pulse injection solenoid duty cycle [%] *)
    rRecipe_FlueDraftSP_mbar        : REAL;     (* Master flue negative draft pressure setpoint [mbar] *)
    rRecipe_TargetCrumbCoreTemp_degC: REAL;     (* Final exit bread loaf crumb core temperature target [deg C] *)

    (* ===================================================================================== *)
    (* 3. 2oo3 TMR ZONE 1-6 UPPER RADIANT TEMPERATURE SENSOR TRIADS [deg C]                  *)
    (* ===================================================================================== *)
    rZoneTemp_Upper_A_degC          : ARRAY[1..6] OF REAL; (* Upper thermocouple Channel A reading [deg C] *)
    rZoneTemp_Upper_B_degC          : ARRAY[1..6] OF REAL; (* Upper thermocouple Channel B reading [deg C] *)
    rZoneTemp_Upper_C_degC          : ARRAY[1..6] OF REAL; (* Upper thermocouple Channel C reading [deg C] *)

    (* ===================================================================================== *)
    (* 4. 2oo3 TMR ZONE 1-6 LOWER HEARTH TEMPERATURE SENSOR TRIADS [deg C]                   *)
    (* ===================================================================================== *)
    rZoneTemp_Lower_A_degC          : ARRAY[1..6] OF REAL; (* Lower thermocouple Channel A reading [deg C] *)
    rZoneTemp_Lower_B_degC          : ARRAY[1..6] OF REAL; (* Lower thermocouple Channel B reading [deg C] *)
    rZoneTemp_Lower_C_degC          : ARRAY[1..6] OF REAL; (* Lower thermocouple Channel C reading [deg C] *)

    (* ===================================================================================== *)
    (* 5. 2oo3 TMR HIGH-TEMP ZIRCONIA CHAMBER HUMIDITY SENSOR TRIADS [% RH]                  *)
    (* ===================================================================================== *)
    rChamberRH_A_pct                : ARRAY[1..6] OF REAL; (* Zirconia moisture sensor Channel A [%] *)
    rChamberRH_B_pct                : ARRAY[1..6] OF REAL; (* Zirconia moisture sensor Channel B [%] *)
    rChamberRH_C_pct                : ARRAY[1..6] OF REAL; (* Zirconia moisture sensor Channel C [%] *)

    (* ===================================================================================== *)
    (* 6. 2oo3 TMR COMBUSTION FLUE DRAFT PRESSURE SENSORS [mbar]                             *)
    (* ===================================================================================== *)
    rFlueDraftPress_A_mbar          : REAL;     (* Exhaust flue differential pressure Channel A [mbar] *)
    rFlueDraftPress_B_mbar          : REAL;     (* Exhaust flue differential pressure Channel B [mbar] *)
    rFlueDraftPress_C_mbar          : REAL;     (* Exhaust flue differential pressure Channel C [mbar] *)

    (* ===================================================================================== *)
    (* 7. 2oo3 TMR OPTICAL UV/IR FLAME SCANNERS (UPPER & LOWER BURNERS)                      *)
    (* ===================================================================================== *)
    bFlameScanner_Upper_A           : ARRAY[1..6] OF BOOL; (* Upper burner optical flame detector Channel A *)
    bFlameScanner_Upper_B           : ARRAY[1..6] OF BOOL; (* Upper burner optical flame detector Channel B *)
    bFlameScanner_Upper_C           : ARRAY[1..6] OF BOOL; (* Upper burner optical flame detector Channel C *)
    bFlameScanner_Lower_A           : ARRAY[1..6] OF BOOL; (* Lower burner optical flame detector Channel A *)
    bFlameScanner_Lower_B           : ARRAY[1..6] OF BOOL; (* Lower burner optical flame detector Channel B *)
    bFlameScanner_Lower_C           : ARRAY[1..6] OF BOOL; (* Lower burner optical flame detector Channel C *)

    (* ===================================================================================== *)
    (* 8. COMBUSTION GAS & AIR SUPPLY UTILITY TELEMETRY                                      *)
    (* ===================================================================================== *)
    rMainGasSupplyPress_bar         : REAL;     (* Natural gas main manifold supply pressure [bar] *)
    rCombAirHeaderPress_mbar        : REAL;     (* Combustion air supply header static pressure [mbar] *)
    rCombAirFlow_Upper_m3h          : ARRAY[1..6] OF REAL; (* Upper burner combustion airflow rate [m3/h] *)
    rCombAirFlow_Lower_m3h          : ARRAY[1..6] OF REAL; (* Lower burner combustion airflow rate [m3/h] *)
    rFuelGasFlow_Upper_m3h          : ARRAY[1..6] OF REAL; (* Upper burner natural gas fuel flow rate [m3/h] *)
    rFuelGasFlow_Lower_m3h          : ARRAY[1..6] OF REAL; (* Lower burner natural gas fuel flow rate [m3/h] *)
    bGasProofOfClosure_Upper        : ARRAY[1..6] OF BOOL; (* Upper burner double safety shutoff valve POC switch *)
    bGasProofOfClosure_Lower        : ARRAY[1..6] OF BOOL; (* Lower burner double safety shutoff valve POC switch *)

    (* ===================================================================================== *)
    (* 9. ZONE 1 SATURATED STEAM UTILITY TELEMETRY                                           *)
    (* ===================================================================================== *)
    rSteamSupplyPress_bar           : REAL;     (* Saturated steam header supply pressure [bar] *)
    rSteamSupplyTemp_degC           : REAL;     (* Saturated steam header temperature [deg C] *)
    rSteamFlowRate_kgh              : REAL;     (* Zone 1 steam mass flow transmitter [kg/h] *)
    bSteamCondensateTrapOK          : BOOL;     (* Thermodynamic condensate trap float high-level OK switch *)

    (* ===================================================================================== *)
    (* 10. WIRE-MESH CONVEYOR BELT DRIVE & ACTIVE PNEUMATIC TRACKING FEEDBACK                *)
    (* ===================================================================================== *)
    rBeltSpeed_EncA_mpm             : REAL;     (* Conveyor drive shaft speed rotary encoder Channel A [m/min] *)
    rBeltSpeed_EncB_mpm             : REAL;     (* Conveyor drive shaft speed rotary encoder Channel B [m/min] *)
    rBeltSpeed_EncC_mpm             : REAL;     (* Conveyor drive shaft speed rotary encoder Channel C [m/min] *)
    rBeltMotorTorque_Nm             : REAL;     (* Main conveyor planetary gearmotor feedback torque [Nm] *)
    rBeltMotorCurrent_A             : REAL;     (* Main conveyor VFD motor phase current [A] *)
    rBeltTension_Left_kN            : REAL;     (* Left tension take-up bearing load cell [kN] *)
    rBeltTension_Right_kN           : REAL;     (* Right tension take-up bearing load cell [kN] *)
    rBeltEdgePos_Left_mm            : REAL;     (* Left optical laser belt edge position sensor [mm] *)
    rBeltEdgePos_Right_mm           : REAL;     (* Right optical laser belt edge position sensor [mm] *)

    (* ===================================================================================== *)
    (* 11. INFEED / OUTFEED DOUGH PRODUCT TELEMETRY                                          *)
    (* ===================================================================================== *)
    bDoughInfeedPresent             : BOOL;     (* Optical beam sensor confirming dough loaf presence at infeed *)
    rDoughInfeedRate_kgh            : REAL;     (* Dynamic weigh conveyor measured dough mass rate [kg/h] *)
    rDoughInfeedTemp_degC           : REAL;     (* Proofer discharge dough internal temperature [deg C] *)
    rBakedLoafExitTemp_degC         : REAL;     (* Oven discharge infrared pyrometer crumb temperature [deg C] *)
END_VAR
"""
    code_parts.append(var_input)

    # -------------------------------------------------------------
    # 3. VAR_OUTPUT DECLARATION BLOCK
    # -------------------------------------------------------------
    var_output = """
VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1. SYSTEM SUPERVISORY & FSM OPERATION STATUS WORDS                                   *)
    (* ===================================================================================== *)
    bSystemReady                    : BOOL;     (* Tunnel oven fully ready for automated production *)
    bSystemRunning                  : BOOL;     (* Active automated thermal control and baking execution *)
    bSystemTripped                  : BOOL;     (* Master NFPA 86 emergency safety fuel slam-shut tripped *)
    bPrePurgeActive                 : BOOL;     (* NFPA 86 forced draft combustion chamber pre-purge in progress *)
    bPrePurgeCompleted              : BOOL;     (* Pre-purge cycle successfully certified *)
    bPilotsEstablished              : BOOL;     (* All zone pilot burner flames confirmed established *)
    bSteamChamberReady              : BOOL;     (* Zone 1 steam deposition chamber primed at target humidity *)
    bContinuousBakeActive           : BOOL;     (* Continuous steady-state baking closed-loop active *)
    bRecipeTransitionActive         : BOOL;     (* Dynamic recipe thermal inertia transition in progress *)

    (* ===================================================================================== *)
    (* 2. ZONE 1-6 MODULATING BURNER ACTUATOR COMMANDS                                       *)
    (* ===================================================================================== *)
    rGasValveCmd_Upper_pct          : ARRAY[1..6] OF REAL; (* Upper burner fuel gas modulating valve [0.0-100.0%] *)
    rGasValveCmd_Lower_pct          : ARRAY[1..6] OF REAL; (* Lower burner fuel gas modulating valve [0.0-100.0%] *)
    rCombAirBlowerCmd_Upper_pct     : ARRAY[1..6] OF REAL; (* Upper combustion air variable blower speed [0.0-100.0%] *)
    rCombAirBlowerCmd_Lower_pct     : ARRAY[1..6] OF REAL; (* Lower combustion air variable blower speed [0.0-100.0%] *)
    bSafetyShutoffValve_Upper       : ARRAY[1..6] OF BOOL; (* Upper burner double block-and-bleed gas valves command *)
    bSafetyShutoffValve_Lower       : ARRAY[1..6] OF BOOL; (* Lower burner double block-and-bleed gas valves command *)
    bSparkIgniter_Upper             : ARRAY[1..6] OF BOOL; (* Upper burner high-voltage ignition transformer spark *)
    bSparkIgniter_Lower             : ARRAY[1..6] OF BOOL; (* Lower burner high-voltage ignition transformer spark *)

    (* ===================================================================================== *)
    (* 3. ZONE 1 STEAM DEPOSITION & EXHAUST DAMPER ACTUATORS                                 *)
    (* ===================================================================================== *)
    rSteamModulatingValveCmd_pct    : REAL;     (* Zone 1 saturated steam proportional control valve [0.0-100.0%] *)
    bSteamPulseSolenoidCmd          : BOOL;     (* Zone 1 saturated steam high-speed pulse manifold solenoid *)
    rExhaustDamperCmd_pct           : ARRAY[1..6] OF REAL; (* Zone 1-6 modulating exhaust moisture damper [0.0-100.0%] *)
    rMainExhaustFanSpeedCmd_pct     : REAL;     (* Main flue chimney draft variable speed exhaust fan [0.0-100.0%] *)

    (* ===================================================================================== *)
    (* 4. WIRE-MESH CONVEYOR DRIVE & ACTIVE PNEUMATIC TRACKING ACTUATORS                     *)
    (* ===================================================================================== *)
    rConveyorVfdSpeedCmd_mpm        : REAL;     (* Main wire-mesh conveyor VFD speed reference [m/min] *)
    rPneumaticTrackPress_Left_bar   : REAL;     (* Left pneumatic steering cylinder proportional pressure [bar] *)
    rPneumaticTrackPress_Right_bar  : REAL;     (* Right pneumatic steering cylinder proportional pressure [bar] *)
    rBeltTensionCylinderCmd_bar     : REAL;     (* Active catenary take-up tension pneumatic pressure [bar] *)

    (* ===================================================================================== *)
    (* 5. CYBER-PHYSICAL OBSERVER & PROCESS ANALYTICS                                        *)
    (* ===================================================================================== *)
    rVotedZoneTemp_Upper_degC       : ARRAY[1..6] OF REAL; (* Voted 2oo3 upper chamber temperature [deg C] *)
    rVotedZoneTemp_Lower_degC       : ARRAY[1..6] OF REAL; (* Voted 2oo3 lower hearth temperature [deg C] *)
    rVotedChamberRH_pct             : ARRAY[1..6] OF REAL; (* Voted 2oo3 chamber relative humidity [%] *)
    rVotedFlueDraft_mbar            : REAL;     (* Voted 2oo3 flue negative draft pressure [mbar] *)
    rVotedBeltSpeed_mpm             : REAL;     (* Voted 2oo3 conveyor belt speed [m/min] *)
    rEstCrumbCoreTemp_degC          : REAL;     (* Observer estimated internal bread loaf crumb core temp [deg C] *)
    rEstCrustSurfaceTemp_degC       : REAL;     (* Observer estimated loaf outer crust surface temp [deg C] *)
    rEstCrustBrowningIndex          : REAL;     (* Maillard non-enzymatic browning optical index [0.0 to 100.0] *)
    rEstDoughMoistureLoss_pct       : REAL;     (* Estimated cumulative dough moisture evaporation loss [%] *)
    rTotalGasFlow_m3h               : REAL;     (* Instantaneous total natural gas consumption [m3/h] *)
    rTotalThermalPower_kW           : REAL;     (* Total instantaneous oven thermal power release [kW] *)
    rOvenThermalEfficiency_pct      : REAL;     (* Overall cyber-physical thermal energy efficiency [%] *)

    (* ===================================================================================== *)
    (* 6. COMPREHENSIVE ISA-18.2 BIT-PACKED STATUS & ALARM WORDS                             *)
    (* ===================================================================================== *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed FSM operational state word *)
    dwAlarmWord1                    : DWORD;    (* Bit-packed critical safety trips (SIL-3, flame, draft, gas press) *)
    dwAlarmWord2                    : DWORD;    (* Bit-packed process trips (overtemp, belt drift, steam failure) *)
    dwWarningWord                   : DWORD;    (* Bit-packed advisory warnings (humidity dev, belt tension, air flow) *)
    dwDegradationWord               : DWORD;    (* Bit-packed sensor 2oo3 channel discrepancy & degradation *)
END_VAR
"""
    code_parts.append(var_output)

    # -------------------------------------------------------------
    # 4. VAR INTERNAL DECLARATIONS BLOCK
    # -------------------------------------------------------------
    var_internal = """
VAR
    (* ===================================================================================== *)
    (* FINITE STATE MACHINE (FSM) STEP REGISTERS & DETERMINISTIC TIMERS                      *)
    (* ===================================================================================== *)
    iState                          : INT := 0; (* Supervisory operational state index *)
    iPrevState                      : INT := 0; (* Previous scan cycle state history *)
    iSubState                       : INT := 0; (* Execution substep progress register *)
    bFirstScan                      : BOOL := TRUE; (* Cold-start initialization flag *)

    tStateDwellTimer                : TON;      (* Primary state dwell timer *)
    tPrePurgeTimer                  : TON;      (* NFPA 86 4-volume ventilation pre-purge timer *)
    tPilotIgnitionTimer             : TON;      (* Pilot spark trial-for-ignition timer *)
    tFlameStabilizeTimer            : TON;      (* Main flame establishment stabilization timer *)
    tSteamChamberPrimeTimer         : TON;      (* Zone 1 steam condensation priming timer *)
    tBakeSteadySyncTimer            : TON;      (* Dough infeed synchronization timer *)
    tRecipeTransitionTimer          : TON;      (* Thermal inertia transition timer *)
    tRunoutBakeoutTimer             : TON;      (* Empty oven bake-out runout timer *)
    tCooldownTimer                  : TON;      (* Controlled refractory cool-down timer *)
    tFlameFailureDebounce           : TON;      (* Flame failure trip debounce timer *)
    tBeltDriftTripTimer             : TON;      (* Excessive belt edge runout trip timer *)
    tDraftLossTripTimer             : TON;      (* Flue draft loss trip timer *)

    (* ===================================================================================== *)
    (* PHYSICAL & THERMODYNAMIC CONSTANTS                                                    *)
    (* ===================================================================================== *)
    rStefanBoltzmann_sigma          : REAL := 5.67037E-8; (* Stefan-Boltzmann constant [W/(m2.K4)] *)
    rOvenTunnelLength_m             : REAL := 60.0;       (* Total continuous baking tunnel length [m] *)
    rOvenZoneLength_m               : REAL := 10.0;       (* Individual thermal zone length [m] *)
    rOvenHearthWidth_m              : REAL := 3.0;        (* Usable wire-mesh hearth width [m] *)
    rOvenChamberVolume_m3           : REAL := 270.0;      (* Total internal combustion oven volume [m3] *)
    rWireMeshArealMass_kgm2         : REAL := 14.5;       (* Carbon-steel wire mesh mass per unit area [kg/m2] *)
    rWireMeshSpecHeat_kJkgK         : REAL := 0.490;      (* Specific heat capacity of steel mesh [kJ/(kg.K)] *)
    rDoughSpecificHeat_kJkgK        : REAL := 2.850;      (* Specific heat capacity of unbaked dough [kJ/(kg.K)] *)
    rBreadSpecificHeat_kJkgK        : REAL := 2.300;      (* Specific heat capacity of baked bread [kJ/(kg.K)] *)
    rWaterHeatVaporization_kJkg     : REAL := 2120.0;     (* Latent heat of saturated steam vaporization [kJ/kg] *)
    rGasNetCalorificValue_kWhm3     : REAL := 9.970;      (* Natural gas lower heating value (LHV) [kWh/m3] *)
    rStoichiometricAirGasRatio      : REAL := 9.520;      (* Theoretical stoichiometric air-to-fuel ratio *)
    rTargetExcessAirLambda          : REAL := 1.120;      (* Target combustion excess air ratio *)
    rSampleTime_Ts_s                : REAL := 0.500;      (* Task execution period (500 ms) [s] *)

    (* ===================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING INTERNALS                          *)
    (* ===================================================================================== *)
    (* Discrepancy tolerances *)
    rTempDiscrepancyLimit_degC      : REAL := 8.0;   (* Maximum allowable spread between redundant thermocouples *)
    rRHDiscrepancyLimit_pct         : REAL := 6.0;   (* Maximum allowable spread between redundant RH sensors *)
    rDraftDiscrepancyLimit_mbar     : REAL := 0.15;  (* Maximum allowable spread between draft sensors *)
    rSpeedDiscrepancyLimit_mpm      : REAL := 0.15;  (* Maximum allowable spread between belt encoders *)

    (* Health tracking flags *)
    bUpperTempHealth_A              : ARRAY[1..6] OF BOOL;
    bUpperTempHealth_B              : ARRAY[1..6] OF BOOL;
    bUpperTempHealth_C              : ARRAY[1..6] OF BOOL;
    bLowerTempHealth_A              : ARRAY[1..6] OF BOOL;
    bLowerTempHealth_B              : ARRAY[1..6] OF BOOL;
    bLowerTempHealth_C              : ARRAY[1..6] OF BOOL;
    bRHHealth_A                     : ARRAY[1..6] OF BOOL;
    bRHHealth_B                     : ARRAY[1..6] OF BOOL;
    bRHHealth_C                     : ARRAY[1..6] OF BOOL;

    bDraftHealth_A                  : BOOL := TRUE;
    bDraftHealth_B                  : BOOL := TRUE;
    bDraftHealth_C                  : BOOL := TRUE;
    bSpeedHealth_A                  : BOOL := TRUE;
    bSpeedHealth_B                  : BOOL := TRUE;
    bSpeedHealth_C                  : BOOL := TRUE;

    bUpperFlameVoted                : ARRAY[1..6] OF BOOL;
    bLowerFlameVoted                : ARRAY[1..6] OF BOOL;

    (* Discrepancy accumulators & timers *)
    rUpperTempDiscrepancy           : ARRAY[1..6] OF REAL;
    rLowerTempDiscrepancy           : ARRAY[1..6] OF REAL;
    rRHDiscrepancy                  : ARRAY[1..6] OF REAL;
    rDraftDiscrepancy               : REAL;
    rSpeedDiscrepancy               : REAL;

    tUpperTempDiscTimer             : ARRAY[1..6] OF TON;
    tLowerTempDiscTimer             : ARRAY[1..6] OF TON;
    tRHDiscTimer                    : ARRAY[1..6] OF TON;
    tDraftDiscTimer                 : TON;
    tSpeedDiscTimer                 : TON;

    (* ===================================================================================== *)
    (* 8-STATE DISCRETE STATE-SPACE MODEL MATRICES & VECTORS                                 *)
    (* States x[1..8]:                                                                       *)
    (*   x[1]=Zone 1-2 Upper Temp, x[2]=Zone 1-2 Lower Temp, x[3]=Zone 3-4 Temp,            *)
    (*   x[4]=Zone 5-6 Temp,       x[5]=Chamber Moisture,    x[6]=Belt Energy Temp,          *)
    (*   x[7]=Crumb Core Temp,     x[8]=Flue Draft Pressure                              *)
    (* Inputs u[1..6]:                                                                       *)
    (*   u[1]=Gas Upper, u[2]=Gas Lower, u[3]=Comb Air,                                      *)
    (*   u[4]=Steam Pulse, u[5]=Exhaust Damper, u[6]=Belt Speed                              *)
    (* ===================================================================================== *)
    bMatricesInitialized            : BOOL := FALSE;
    A_mat                           : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Transition Matrix *)
    B_mat                           : ARRAY[1..8, 1..6] OF REAL; (* Discrete Input Coupling Matrix *)
    C_mat                           : ARRAY[1..6, 1..8] OF REAL; (* Measurement Output Matrix *)
    D_mat                           : ARRAY[1..6, 1..6] OF REAL; (* Feedthrough Transmission Matrix *)

    x_state                         : ARRAY[1..8] OF REAL;       (* Dynamic discrete state vector *)
    x_next                          : ARRAY[1..8] OF REAL;       (* One-step predicted state vector *)
    x_ref                           : ARRAY[1..8] OF REAL;       (* Reference trajectory state vector *)
    u_control                       : ARRAY[1..6] OF REAL;       (* Plant control input vector *)
    u_prev                          : ARRAY[1..6] OF REAL;       (* Previous cycle control vector *)
    y_observed                      : ARRAY[1..6] OF REAL;       (* Computed plant output vector *)
    y_measured                      : ARRAY[1..6] OF REAL;       (* Actual sensory feedback vector *)
    L_observer                      : ARRAY[1..8, 1..6] OF REAL; (* Luenberger state observer gain matrix *)

    (* ===================================================================================== *)
    (* RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) VARIABLES                             *)
    (* ===================================================================================== *)
    Q_diag                          : ARRAY[1..8] OF REAL;       (* State tracking error penalty weights *)
    R_diag                          : ARRAY[1..6] OF REAL;       (* Actuator rate effort penalty weights *)
    P_diag                          : ARRAY[1..8] OF REAL;       (* Terminal state error penalty weights *)
    H_diag                          : ARRAY[1..6] OF REAL;       (* Hessian diagonal approximation *)
    grad_J                          : ARRAY[1..6] OF REAL;       (* Cost function gradient vector *)
    delta_u                         : ARRAY[1..6] OF REAL;       (* Optimal control slew rate increment *)

    rCostFunction_J                 : REAL;                      (* Instantaneous MPC quadratic cost *)
    rStepAlpha                      : REAL := 0.080;             (* Projected gradient descent step size *)
    iMpcIter                        : INT := 1;
    iStateIdx                       : INT := 1;
    iInputIdx                       : INT := 1;
    iOutIdx                         : INT := 1;
    iZoneIdx                        : INT := 1;

    (* Actuator rate and boundary constraints *)
    rMaxGasSlewRate_pcts            : REAL := 5.0;               (* Gas valve maximum slew rate [5 %/s] *)
    rMaxAirSlewRate_pcts            : REAL := 8.0;               (* Air blower maximum slew rate [8 %/s] *)
    rMaxDamperSlewRate_pcts         : REAL := 6.0;               (* Exhaust damper maximum slew rate [6 %/s] *)
    rMaxBeltAcc_mpms                : REAL := 0.050;             (* Conveyor acceleration limit [0.05 m/min/s] *)

    (* Cross-limiting combustion control variables *)
    rTargetGasFiring_Upper          : ARRAY[1..6] OF REAL;
    rTargetGasFiring_Lower          : ARRAY[1..6] OF REAL;
    rAirLeadGas_Upper               : ARRAY[1..6] OF REAL;
    rAirLeadGas_Lower               : ARRAY[1..6] OF REAL;
    rGasLeadAir_Upper               : ARRAY[1..6] OF REAL;
    rGasLeadAir_Lower               : ARRAY[1..6] OF REAL;

    (* ===================================================================================== *)
    (* CYBER-PHYSICAL 1D DOUGH HEAT CONDUCTION & QUALITY OBSERVER                            *)
    (* ===================================================================================== *)
    rDoughLoafMass_kg               : REAL := 0.800;             (* Standard loaf dough wet mass [kg] *)
    rDoughLoafRadius_m              : REAL := 0.060;             (* Effective half-thickness loaf radius [m] *)
    rThermalDiffusivityDough        : REAL := 1.35E-7;           (* Thermal diffusivity alpha [m2/s] *)
    rThermalConductivityDough       : REAL := 0.280;             (* Thermal conductivity k [W/(m.K)] *)
    rDoughSurfaceTemp_degC          : REAL := 25.0;              (* Loaf crust surface temperature [deg C] *)
    rDoughMidTemp_degC              : REAL := 25.0;              (* Loaf intermediate crumb temperature [deg C] *)
    rDoughCoreTemp_degC             : REAL := 25.0;              (* Loaf geometric center temperature [deg C] *)
    rCumulativeMoistureLoss_kg      : REAL := 0.0;
    rCrustMaillardRate              : REAL := 0.0;
    rCrustBrowningAccumulator       : REAL := 0.0;
    rZoneResidenceTime_s            : REAL := 240.0;

    (* Stefan-Boltzmann temperature powers *)
    rT_upper_K                      : REAL;
    rT_lower_K                      : REAL;
    rT_dough_K                      : REAL;
    rRadFluxUpper_Wm2               : REAL;
    rConvFluxUpper_Wm2              : REAL;
    rCondFluxLower_Wm2              : REAL;
    rEvapCoolingFlux_Wm2            : REAL;

    (* ===================================================================================== *)
    (* ZONE 1 SATURATED STEAM PULSE INJECTION PULSER                                         *)
    (* ===================================================================================== *)
    rSteamPulseTimer_s              : REAL := 0.0;
    rSteamPulsePeriod_s             : REAL := 10.0;              (* Pulse repetition cycle period [s] *)
    rSteamPulseDuration_s           : REAL := 4.0;               (* Steam injection open duration [s] *)
    bSteamPulseOutput               : BOOL := FALSE;

    (* ===================================================================================== *)
    (* ACTIVE PNEUMATIC BELT TRACKING & EDGE TENSION CENTERING                               *)
    (* ===================================================================================== *)
    rBeltTrackingError_mm           : REAL := 0.0;               (* Differential belt lateral displacement [mm] *)
    rBeltTrackingIntegral_mm        : REAL := 0.0;               (* PI tracking centering integral [mm.s] *)
    rBeltTrackingDiffPressure_bar   : REAL := 0.0;               (* Differential steering cylinder pressure [bar] *)
    rTrackKp                        : REAL := 0.045;             (* Proportional steering gain [bar/mm] *)
    rTrackKi                        : REAL := 0.003;             (* Integral steering gain [bar/(mm.s)] *)
    rNominalTrackingPressure_bar    : REAL := 3.50;              (* Base pneumatic tracking pressure [bar] *)
    rTargetBeltTension_kN           : REAL := 18.50;             (* Target total wire-mesh catenary tension [kN] *)
    rTensionError_kN                : REAL := 0.0;
    rTensionKp                      : REAL := 0.200;             (* Proportional tension gain [bar/kN] *)
    rNominalTensionPressure_bar     : REAL := 4.20;              (* Base tension cylinder pressure [bar] *)

    (* ===================================================================================== *)
    (* COMBUSTION AIR-TO-FUEL RATIO & FLOW AGGREGATORS                                       *)
    (* ===================================================================================== *)
    rTotalGasConsumption_Accum     : REAL := 0.0;
    rTotalThermalEnergy_kWh         : REAL := 0.0;
    rZonePowerUpper_kW              : ARRAY[1..6] OF REAL;
    rZonePowerLower_kW              : ARRAY[1..6] OF REAL;

    (* ===================================================================================== *)
    (* ISA-18.2 ALARM ENGINE TRIP POINTS & HYSTERESIS DEADBANDS                              *)
    (* ===================================================================================== *)
    rAlarmTempHH_degC               : REAL := 285.0;             (* High-High emergency flame slam-shut [deg C] *)
    rAlarmTempH_degC                : REAL := 270.0;             (* High temperature warning [deg C] *)
    rAlarmTempL_degC                : REAL := 150.0;             (* Low temperature warning [deg C] *)
    rAlarmTempLL_degC               : REAL := 120.0;             (* Low-Low temperature flame lockout [deg C] *)
    rTempDeadband_degC              : REAL := 3.0;               (* Alarm clear deadband hysteresis [deg C] *)

    rAlarmDraftHH_mbar              : REAL := 0.05;              (* Flue draft positive pressure trip [mbar] *)
    rAlarmDraftLL_mbar              : REAL := -1.50;             (* Flue draft excessive negative pressure [mbar] *)
    rAlarmDraftL_mbar               : REAL := -0.10;             (* Flue draft low warning [mbar] *)

    rAlarmBeltDriftTrip_mm          : REAL := 35.0;              (* Belt runout emergency stop limit [mm] *)
    rAlarmBeltDriftWarn_mm          : REAL := 18.0;              (* Belt runout advisory warning limit [mm] *)

    rAlarmGasPressHH_bar            : REAL := 3.20;              (* Gas main overpressure trip [bar] *)
    rAlarmGasPressLL_bar            : REAL := 1.80;              (* Gas main underpressure trip [bar] *)

    bAlarmTripped_FlameFailure      : BOOL := FALSE;
    bAlarmTripped_OverTempHH        : BOOL := FALSE;
    bAlarmTripped_DraftLoss         : BOOL := FALSE;
    bAlarmTripped_GasPressure       : BOOL := FALSE;
    bAlarmTripped_BeltDrift         : BOOL := FALSE;
    bWarning_TempHigh               : BOOL := FALSE;
    bWarning_TempLow                : BOOL := FALSE;
    bWarning_HumidityDeviation      : BOOL := FALSE;
    bWarning_BeltTensionLow         : BOOL := FALSE;
END_VAR
"""
    code_parts.append(var_internal)

    # -------------------------------------------------------------
    # 5. INITIALIZATION & SAFETY SHUTDOWN LOGIC (PHASE 1)
    # -------------------------------------------------------------
    phase1 = """
(* ========================================================================================= *)
(* =================================== MAIN LOGIC EXECUTION ================================ *)
(* ========================================================================================= *)

(* ========================================================================================= *)
(* PHASE 1: SIL-3 EMERGENCY SAFETY SHUTDOWN & NFPA 86 COMBUSTION SAFETY INTERLOCKS           *)
(* ========================================================================================= *)
IF NOT bEmergencyStop OR NOT bEnableSystem THEN
    bSystemTripped := TRUE;
    bSystemRunning := FALSE;
    bSystemReady := FALSE;
    bPrePurgeActive := FALSE;
    bContinuousBakeActive := FALSE;
    bRecipeTransitionActive := FALSE;

    (* Pack SIL-3 Hardwired Emergency Stop trip into Alarm Word 1 (Bit 0) *)
    IF NOT bEmergencyStop THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* Bit 0: Hardware SIL-3 Hardwired Safety Circuit Broken *)
    END_IF;

    IF NOT bEnableSystem THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Bit 1: System Master Enable Permissive Lost *)
    END_IF;

    (* NFPA 86 MANDATORY IMMEDIATE SLAM-SHUT (< 1.0 s) ON ALL DOUBLE BLOCK-AND-BLEED VALVES *)
    FOR iZoneIdx := 1 TO 6 DO
        bSafetyShutoffValve_Upper[iZoneIdx] := FALSE;
        bSafetyShutoffValve_Lower[iZoneIdx] := FALSE;
        rGasValveCmd_Upper_pct[iZoneIdx] := 0.0;
        rGasValveCmd_Lower_pct[iZoneIdx] := 0.0;
        bSparkIgniter_Upper[iZoneIdx] := FALSE;
        bSparkIgniter_Lower[iZoneIdx] := FALSE;
        (* Maintain minimum combustion air purge to clear unburned hydrocarbons *)
        rCombAirBlowerCmd_Upper_pct[iZoneIdx] := 35.0;
        rCombAirBlowerCmd_Lower_pct[iZoneIdx] := 35.0;
        rExhaustDamperCmd_pct[iZoneIdx] := 100.0; (* Fully open dampers to evacuate combustible gases *)
    END_FOR;

    (* Shut off saturated steam injection *)
    rSteamModulatingValveCmd_pct := 0.0;
    bSteamPulseSolenoidCmd := FALSE;

    (* Decelerate wire-mesh conveyor to controlled stop *)
    rConveyorVfdSpeedCmd_mpm := 0.0;

    (* Set main chimney exhaust fan to safe post-ventilation *)
    rMainExhaustFanSpeedCmd_pct := 50.0;

    iState := 10; (* Transition directly to STATE_EMERGENCY_SLAM_SHUT *)
    RETURN;
END_IF;

(* Master safety fault unlatch logic upon valid reset request *)
IF bResetFaults THEN
    IF bEmergencyStop AND bEnableSystem AND (rMainGasSupplyPress_bar >= rAlarmGasPressLL_bar) 
       AND (rMainGasSupplyPress_bar <= rAlarmGasPressHH_bar) THEN
        dwAlarmWord1 := 16#0000_0000;
        dwAlarmWord2 := 16#0000_0000;
        dwWarningWord := 16#0000_0000;
        bSystemTripped := FALSE;
        bAlarmTripped_FlameFailure := FALSE;
        bAlarmTripped_OverTempHH := FALSE;
        bAlarmTripped_DraftLoss := FALSE;
        bAlarmTripped_GasPressure := FALSE;
        bAlarmTripped_BeltDrift := FALSE;
    END_IF;
END_IF;
"""
    code_parts.append(phase1)

    # -------------------------------------------------------------
    # 6. SENSOR VOTING & TMR ENGINE (PHASE 2)
    # -------------------------------------------------------------
    phase2 = """
(* ========================================================================================= *)
(* PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINE                        *)
(* ========================================================================================= *)
dwDegradationWord := 16#0000_0000;

(* --- 2.1 Zone 1 to 6 Upper Radiant Chamber Thermocouple Triad Voting (2oo3) --- *)
FOR iZoneIdx := 1 TO 6 DO
    (* Calculate channel-to-channel absolute differences *)
    rUpperTempDiscrepancy[iZoneIdx] := MAX(
        ABS(rZoneTemp_Upper_A_degC[iZoneIdx] - rZoneTemp_Upper_B_degC[iZoneIdx]),
        MAX(ABS(rZoneTemp_Upper_B_degC[iZoneIdx] - rZoneTemp_Upper_C_degC[iZoneIdx]),
            ABS(rZoneTemp_Upper_C_degC[iZoneIdx] - rZoneTemp_Upper_A_degC[iZoneIdx]))
    );

    (* Boundary plausibility checks [0.0 to 350.0 deg C] *)
    bUpperTempHealth_A[iZoneIdx] := (rZoneTemp_Upper_A_degC[iZoneIdx] >= 0.0) AND (rZoneTemp_Upper_A_degC[iZoneIdx] <= 350.0);
    bUpperTempHealth_B[iZoneIdx] := (rZoneTemp_Upper_B_degC[iZoneIdx] >= 0.0) AND (rZoneTemp_Upper_B_degC[iZoneIdx] <= 350.0);
    bUpperTempHealth_C[iZoneIdx] := (rZoneTemp_Upper_C_degC[iZoneIdx] >= 0.0) AND (rZoneTemp_Upper_C_degC[iZoneIdx] <= 350.0);

    (* Median Voting Implementation *)
    IF bUpperTempHealth_A[iZoneIdx] AND bUpperTempHealth_B[iZoneIdx] AND bUpperTempHealth_C[iZoneIdx] THEN
        (* All three channels healthy: take true mathematical median *)
        IF ((rZoneTemp_Upper_A_degC[iZoneIdx] >= rZoneTemp_Upper_B_degC[iZoneIdx]) AND (rZoneTemp_Upper_A_degC[iZoneIdx] <= rZoneTemp_Upper_C_degC[iZoneIdx])) OR
           ((rZoneTemp_Upper_A_degC[iZoneIdx] <= rZoneTemp_Upper_B_degC[iZoneIdx]) AND (rZoneTemp_Upper_A_degC[iZoneIdx] >= rZoneTemp_Upper_C_degC[iZoneIdx])) THEN
            rVotedZoneTemp_Upper_degC[iZoneIdx] := rZoneTemp_Upper_A_degC[iZoneIdx];
        ELSIF ((rZoneTemp_Upper_B_degC[iZoneIdx] >= rZoneTemp_Upper_A_degC[iZoneIdx]) AND (rZoneTemp_Upper_B_degC[iZoneIdx] <= rZoneTemp_Upper_C_degC[iZoneIdx])) OR
              ((rZoneTemp_Upper_B_degC[iZoneIdx] <= rZoneTemp_Upper_A_degC[iZoneIdx]) AND (rZoneTemp_Upper_B_degC[iZoneIdx] >= rZoneTemp_Upper_C_degC[iZoneIdx])) THEN
            rVotedZoneTemp_Upper_degC[iZoneIdx] := rZoneTemp_Upper_B_degC[iZoneIdx];
        ELSE
            rVotedZoneTemp_Upper_degC[iZoneIdx] := rZoneTemp_Upper_C_degC[iZoneIdx];
        END_IF;
    ELSIF bUpperTempHealth_A[iZoneIdx] AND bUpperTempHealth_B[iZoneIdx] THEN
        rVotedZoneTemp_Upper_degC[iZoneIdx] := 0.5 * (rZoneTemp_Upper_A_degC[iZoneIdx] + rZoneTemp_Upper_B_degC[iZoneIdx]);
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0001, iZoneIdx - 1);
    ELSIF bUpperTempHealth_B[iZoneIdx] AND bUpperTempHealth_C[iZoneIdx] THEN
        rVotedZoneTemp_Upper_degC[iZoneIdx] := 0.5 * (rZoneTemp_Upper_B_degC[iZoneIdx] + rZoneTemp_Upper_C_degC[iZoneIdx]);
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0001, iZoneIdx - 1);
    ELSIF bUpperTempHealth_A[iZoneIdx] AND bUpperTempHealth_C[iZoneIdx] THEN
        rVotedZoneTemp_Upper_degC[iZoneIdx] := 0.5 * (rZoneTemp_Upper_A_degC[iZoneIdx] + rZoneTemp_Upper_C_degC[iZoneIdx]);
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0001, iZoneIdx - 1);
    ELSIF bUpperTempHealth_A[iZoneIdx] THEN
        rVotedZoneTemp_Upper_degC[iZoneIdx] := rZoneTemp_Upper_A_degC[iZoneIdx];
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0040, iZoneIdx - 1);
    ELSIF bUpperTempHealth_B[iZoneIdx] THEN
        rVotedZoneTemp_Upper_degC[iZoneIdx] := rZoneTemp_Upper_B_degC[iZoneIdx];
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0040, iZoneIdx - 1);
    ELSIF bUpperTempHealth_C[iZoneIdx] THEN
        rVotedZoneTemp_Upper_degC[iZoneIdx] := rZoneTemp_Upper_C_degC[iZoneIdx];
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0040, iZoneIdx - 1);
    ELSE
        (* Total sensor loss in zone upper chamber *)
        rVotedZoneTemp_Upper_degC[iZoneIdx] := rRecipe_ZoneTempSP_Upper_degC[iZoneIdx];
        dwAlarmWord2 := dwAlarmWord2 OR SHL(16#0000_0001, iZoneIdx - 1);
    END_IF;

    (* Discrepancy Debounce Timer Evaluation *)
    tUpperTempDiscTimer[iZoneIdx](IN := (rUpperTempDiscrepancy[iZoneIdx] > rTempDiscrepancyLimit_degC), PT := T#5S);
    IF tUpperTempDiscTimer[iZoneIdx].Q THEN
        dwWarningWord := dwWarningWord OR SHL(16#0000_0001, iZoneIdx - 1);
    END_IF;
END_FOR;

(* --- 2.2 Zone 1 to 6 Lower Hearth Thermocouple Triad Voting (2oo3) --- *)
FOR iZoneIdx := 1 TO 6 DO
    rLowerTempDiscrepancy[iZoneIdx] := MAX(
        ABS(rZoneTemp_Lower_A_degC[iZoneIdx] - rZoneTemp_Lower_B_degC[iZoneIdx]),
        MAX(ABS(rZoneTemp_Lower_B_degC[iZoneIdx] - rZoneTemp_Lower_C_degC[iZoneIdx]),
            ABS(rZoneTemp_Lower_C_degC[iZoneIdx] - rZoneTemp_Lower_A_degC[iZoneIdx]))
    );

    bLowerTempHealth_A[iZoneIdx] := (rZoneTemp_Lower_A_degC[iZoneIdx] >= 0.0) AND (rZoneTemp_Lower_A_degC[iZoneIdx] <= 350.0);
    bLowerTempHealth_B[iZoneIdx] := (rZoneTemp_Lower_B_degC[iZoneIdx] >= 0.0) AND (rZoneTemp_Lower_B_degC[iZoneIdx] <= 350.0);
    bLowerTempHealth_C[iZoneIdx] := (rZoneTemp_Lower_C_degC[iZoneIdx] >= 0.0) AND (rZoneTemp_Lower_C_degC[iZoneIdx] <= 350.0);

    IF bLowerTempHealth_A[iZoneIdx] AND bLowerTempHealth_B[iZoneIdx] AND bLowerTempHealth_C[iZoneIdx] THEN
        IF ((rZoneTemp_Lower_A_degC[iZoneIdx] >= rZoneTemp_Lower_B_degC[iZoneIdx]) AND (rZoneTemp_Lower_A_degC[iZoneIdx] <= rZoneTemp_Lower_C_degC[iZoneIdx])) OR
           ((rZoneTemp_Lower_A_degC[iZoneIdx] <= rZoneTemp_Lower_B_degC[iZoneIdx]) AND (rZoneTemp_Lower_A_degC[iZoneIdx] >= rZoneTemp_Lower_C_degC[iZoneIdx])) THEN
            rVotedZoneTemp_Lower_degC[iZoneIdx] := rZoneTemp_Lower_A_degC[iZoneIdx];
        ELSIF ((rZoneTemp_Lower_B_degC[iZoneIdx] >= rZoneTemp_Lower_A_degC[iZoneIdx]) AND (rZoneTemp_Lower_B_degC[iZoneIdx] <= rZoneTemp_Lower_C_degC[iZoneIdx])) OR
              ((rZoneTemp_Lower_B_degC[iZoneIdx] <= rZoneTemp_Lower_A_degC[iZoneIdx]) AND (rZoneTemp_Lower_B_degC[iZoneIdx] >= rZoneTemp_Lower_C_degC[iZoneIdx])) THEN
            rVotedZoneTemp_Lower_degC[iZoneIdx] := rZoneTemp_Lower_B_degC[iZoneIdx];
        ELSE
            rVotedZoneTemp_Lower_degC[iZoneIdx] := rZoneTemp_Lower_C_degC[iZoneIdx];
        END_IF;
    ELSIF bLowerTempHealth_A[iZoneIdx] AND bLowerTempHealth_B[iZoneIdx] THEN
        rVotedZoneTemp_Lower_degC[iZoneIdx] := 0.5 * (rZoneTemp_Lower_A_degC[iZoneIdx] + rZoneTemp_Lower_B_degC[iZoneIdx]);
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0100, iZoneIdx - 1);
    ELSIF bLowerTempHealth_B[iZoneIdx] AND bLowerTempHealth_C[iZoneIdx] THEN
        rVotedZoneTemp_Lower_degC[iZoneIdx] := 0.5 * (rZoneTemp_Lower_B_degC[iZoneIdx] + rZoneTemp_Lower_C_degC[iZoneIdx]);
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0100, iZoneIdx - 1);
    ELSIF bLowerTempHealth_A[iZoneIdx] AND bLowerTempHealth_C[iZoneIdx] THEN
        rVotedZoneTemp_Lower_degC[iZoneIdx] := 0.5 * (rZoneTemp_Lower_A_degC[iZoneIdx] + rZoneTemp_Lower_C_degC[iZoneIdx]);
        dwDegradationWord := dwDegradationWord OR SHL(16#0000_0100, iZoneIdx - 1);
    ELSIF bLowerTempHealth_A[iZoneIdx] THEN
        rVotedZoneTemp_Lower_degC[iZoneIdx] := rZoneTemp_Lower_A_degC[iZoneIdx];
    ELSIF bLowerTempHealth_B[iZoneIdx] THEN
        rVotedZoneTemp_Lower_degC[iZoneIdx] := rZoneTemp_Lower_B_degC[iZoneIdx];
    ELSIF bLowerTempHealth_C[iZoneIdx] THEN
        rVotedZoneTemp_Lower_degC[iZoneIdx] := rZoneTemp_Lower_C_degC[iZoneIdx];
    ELSE
        rVotedZoneTemp_Lower_degC[iZoneIdx] := rRecipe_ZoneTempSP_Lower_degC[iZoneIdx];
        dwAlarmWord2 := dwAlarmWord2 OR SHL(16#0000_0100, iZoneIdx - 1);
    END_IF;

    tLowerTempDiscTimer[iZoneIdx](IN := (rLowerTempDiscrepancy[iZoneIdx] > rTempDiscrepancyLimit_degC), PT := T#5S);
END_FOR;

(* --- 2.3 Zone 1 to 6 High-Temperature Zirconia Humidity Sensor Voting (2oo3) --- *)
FOR iZoneIdx := 1 TO 6 DO
    rRHDiscrepancy[iZoneIdx] := MAX(
        ABS(rChamberRH_A_pct[iZoneIdx] - rChamberRH_B_pct[iZoneIdx]),
        MAX(ABS(rChamberRH_B_pct[iZoneIdx] - rChamberRH_C_pct[iZoneIdx]),
            ABS(rChamberRH_C_pct[iZoneIdx] - rChamberRH_A_pct[iZoneIdx]))
    );

    bRHHealth_A[iZoneIdx] := (rChamberRH_A_pct[iZoneIdx] >= 0.0) AND (rChamberRH_A_pct[iZoneIdx] <= 100.0);
    bRHHealth_B[iZoneIdx] := (rChamberRH_B_pct[iZoneIdx] >= 0.0) AND (rChamberRH_B_pct[iZoneIdx] <= 100.0);
    bRHHealth_C[iZoneIdx] := (rChamberRH_C_pct[iZoneIdx] >= 0.0) AND (rChamberRH_C_pct[iZoneIdx] <= 100.0);

    IF bRHHealth_A[iZoneIdx] AND bRHHealth_B[iZoneIdx] AND bRHHealth_C[iZoneIdx] THEN
        IF ((rChamberRH_A_pct[iZoneIdx] >= rChamberRH_B_pct[iZoneIdx]) AND (rChamberRH_A_pct[iZoneIdx] <= rChamberRH_C_pct[iZoneIdx])) OR
           ((rChamberRH_A_pct[iZoneIdx] <= rChamberRH_B_pct[iZoneIdx]) AND (rChamberRH_A_pct[iZoneIdx] >= rChamberRH_C_pct[iZoneIdx])) THEN
            rVotedChamberRH_pct[iZoneIdx] := rChamberRH_A_pct[iZoneIdx];
        ELSIF ((rChamberRH_B_pct[iZoneIdx] >= rChamberRH_A_pct[iZoneIdx]) AND (rChamberRH_B_pct[iZoneIdx] <= rChamberRH_C_pct[iZoneIdx])) OR
              ((rChamberRH_B_pct[iZoneIdx] <= rChamberRH_A_pct[iZoneIdx]) AND (rChamberRH_B_pct[iZoneIdx] >= rChamberRH_C_pct[iZoneIdx])) THEN
            rVotedChamberRH_pct[iZoneIdx] := rChamberRH_B_pct[iZoneIdx];
        ELSE
            rVotedChamberRH_pct[iZoneIdx] := rChamberRH_C_pct[iZoneIdx];
        END_IF;
    ELSIF bRHHealth_A[iZoneIdx] AND bRHHealth_B[iZoneIdx] THEN
        rVotedChamberRH_pct[iZoneIdx] := 0.5 * (rChamberRH_A_pct[iZoneIdx] + rChamberRH_B_pct[iZoneIdx]);
    ELSIF bRHHealth_B[iZoneIdx] AND bRHHealth_C[iZoneIdx] THEN
        rVotedChamberRH_pct[iZoneIdx] := 0.5 * (rChamberRH_B_pct[iZoneIdx] + rChamberRH_C_pct[iZoneIdx]);
    ELSIF bRHHealth_A[iZoneIdx] AND bRHHealth_C[iZoneIdx] THEN
        rVotedChamberRH_pct[iZoneIdx] := 0.5 * (rChamberRH_A_pct[iZoneIdx] + rChamberRH_C_pct[iZoneIdx]);
    ELSIF bRHHealth_A[iZoneIdx] THEN
        rVotedChamberRH_pct[iZoneIdx] := rChamberRH_A_pct[iZoneIdx];
    ELSIF bRHHealth_B[iZoneIdx] THEN
        rVotedChamberRH_pct[iZoneIdx] := rChamberRH_B_pct[iZoneIdx];
    ELSIF bRHHealth_C[iZoneIdx] THEN
        rVotedChamberRH_pct[iZoneIdx] := rChamberRH_C_pct[iZoneIdx];
    ELSE
        rVotedChamberRH_pct[iZoneIdx] := rRecipe_ZoneRH_SP_pct[iZoneIdx];
        dwDegradationWord := dwDegradationWord OR SHL(16#0001_0000, iZoneIdx - 1);
    END_IF;

    tRHDiscTimer[iZoneIdx](IN := (rRHDiscrepancy[iZoneIdx] > rRHDiscrepancyLimit_pct), PT := T#10S);
END_FOR;

(* --- 2.4 Flue Draft Pressure Differential Sensor Voting (2oo3) --- *)
rDraftDiscrepancy := MAX(
    ABS(rFlueDraftPress_A_mbar - rFlueDraftPress_B_mbar),
    MAX(ABS(rFlueDraftPress_B_mbar - rFlueDraftPress_C_mbar),
        ABS(rFlueDraftPress_C_mbar - rFlueDraftPress_A_mbar))
);

bDraftHealth_A := (rFlueDraftPress_A_mbar >= -5.0) AND (rFlueDraftPress_A_mbar <= 5.0);
bDraftHealth_B := (rFlueDraftPress_B_mbar >= -5.0) AND (rFlueDraftPress_B_mbar <= 5.0);
bDraftHealth_C := (rFlueDraftPress_C_mbar >= -5.0) AND (rFlueDraftPress_C_mbar <= 5.0);

IF bDraftHealth_A AND bDraftHealth_B AND bDraftHealth_C THEN
    IF ((rFlueDraftPress_A_mbar >= rFlueDraftPress_B_mbar) AND (rFlueDraftPress_A_mbar <= rFlueDraftPress_C_mbar)) OR
       ((rFlueDraftPress_A_mbar <= rFlueDraftPress_B_mbar) AND (rFlueDraftPress_A_mbar >= rFlueDraftPress_C_mbar)) THEN
        rVotedFlueDraft_mbar := rFlueDraftPress_A_mbar;
    ELSIF ((rFlueDraftPress_B_mbar >= rFlueDraftPress_A_mbar) AND (rFlueDraftPress_B_mbar <= rFlueDraftPress_C_mbar)) OR
          ((rFlueDraftPress_B_mbar <= rFlueDraftPress_A_mbar) AND (rFlueDraftPress_B_mbar >= rFlueDraftPress_C_mbar)) THEN
        rVotedFlueDraft_mbar := rFlueDraftPress_B_mbar;
    ELSE
        rVotedFlueDraft_mbar := rFlueDraftPress_C_mbar;
    END_IF;
ELSIF bDraftHealth_A AND bDraftHealth_B THEN
    rVotedFlueDraft_mbar := 0.5 * (rFlueDraftPress_A_mbar + rFlueDraftPress_B_mbar);
ELSIF bDraftHealth_B AND bDraftHealth_C THEN
    rVotedFlueDraft_mbar := 0.5 * (rFlueDraftPress_B_mbar + rFlueDraftPress_C_mbar);
ELSIF bDraftHealth_A AND bDraftHealth_C THEN
    rVotedFlueDraft_mbar := 0.5 * (rFlueDraftPress_A_mbar + rFlueDraftPress_C_mbar);
ELSE
    rVotedFlueDraft_mbar := rRecipe_FlueDraftSP_mbar;
    dwDegradationWord := dwDegradationWord OR 16#0010_0000;
END_IF;

tDraftDiscTimer(IN := (rDraftDiscrepancy > rDraftDiscrepancyLimit_mbar), PT := T#3S);

(* --- 2.5 Wire-Mesh Conveyor Speed Encoder Voting (2oo3) --- *)
rSpeedDiscrepancy := MAX(
    ABS(rBeltSpeed_EncA_mpm - rBeltSpeed_EncB_mpm),
    MAX(ABS(rBeltSpeed_EncB_mpm - rBeltSpeed_EncC_mpm),
        ABS(rBeltSpeed_EncC_mpm - rBeltSpeed_EncA_mpm))
);

bSpeedHealth_A := (rBeltSpeed_EncA_mpm >= 0.0) AND (rBeltSpeed_EncA_mpm <= 10.0);
bSpeedHealth_B := (rBeltSpeed_EncB_mpm >= 0.0) AND (rBeltSpeed_EncB_mpm <= 10.0);
bSpeedHealth_C := (rBeltSpeed_EncC_mpm >= 0.0) AND (rBeltSpeed_EncC_mpm <= 10.0);

IF bSpeedHealth_A AND bSpeedHealth_B AND bSpeedHealth_C THEN
    IF ((rBeltSpeed_EncA_mpm >= rBeltSpeed_EncB_mpm) AND (rBeltSpeed_EncA_mpm <= rBeltSpeed_EncC_mpm)) OR
       ((rBeltSpeed_EncA_mpm <= rBeltSpeed_EncB_mpm) AND (rBeltSpeed_EncA_mpm >= rBeltSpeed_EncC_mpm)) THEN
        rVotedBeltSpeed_mpm := rBeltSpeed_EncA_mpm;
    ELSIF ((rBeltSpeed_EncB_mpm >= rBeltSpeed_EncA_mpm) AND (rBeltSpeed_EncB_mpm <= rBeltSpeed_EncC_mpm)) OR
          ((rBeltSpeed_EncB_mpm <= rBeltSpeed_EncA_mpm) AND (rBeltSpeed_EncB_mpm >= rBeltSpeed_EncC_mpm)) THEN
        rVotedBeltSpeed_mpm := rBeltSpeed_EncB_mpm;
    ELSE
        rVotedBeltSpeed_mpm := rBeltSpeed_EncC_mpm;
    END_IF;
ELSIF bSpeedHealth_A AND bSpeedHealth_B THEN
    rVotedBeltSpeed_mpm := 0.5 * (rBeltSpeed_EncA_mpm + rBeltSpeed_EncB_mpm);
ELSIF bSpeedHealth_B AND bSpeedHealth_C THEN
    rVotedBeltSpeed_mpm := 0.5 * (rBeltSpeed_EncB_mpm + rBeltSpeed_EncC_mpm);
ELSIF bSpeedHealth_A AND bSpeedHealth_C THEN
    rVotedBeltSpeed_mpm := 0.5 * (rBeltSpeed_EncA_mpm + rBeltSpeed_EncC_mpm);
ELSE
    rVotedBeltSpeed_mpm := rRecipe_BeltSpeedSP_mpm;
    dwDegradationWord := dwDegradationWord OR 16#0020_0000;
END_IF;

tSpeedDiscTimer(IN := (rSpeedDiscrepancy > rSpeedDiscrepancyLimit_mpm), PT := T#2S);

(* --- 2.6 Optical UV/IR Flame Scanners 2oo3 Voting Per Burner Assembly --- *)
FOR iZoneIdx := 1 TO 6 DO
    (* 2-out-of-3 logic: At least 2 channels must detect flame *)
    bUpperFlameVoted[iZoneIdx] := (bFlameScanner_Upper_A[iZoneIdx] AND bFlameScanner_Upper_B[iZoneIdx]) OR
                                  (bFlameScanner_Upper_B[iZoneIdx] AND bFlameScanner_Upper_C[iZoneIdx]) OR
                                  (bFlameScanner_Upper_C[iZoneIdx] AND bFlameScanner_Upper_A[iZoneIdx]);

    bLowerFlameVoted[iZoneIdx] := (bFlameScanner_Lower_A[iZoneIdx] AND bFlameScanner_Lower_B[iZoneIdx]) OR
                                  (bFlameScanner_Lower_B[iZoneIdx] AND bFlameScanner_Lower_C[iZoneIdx]) OR
                                  (bFlameScanner_Lower_C[iZoneIdx] AND bFlameScanner_Lower_A[iZoneIdx]);
END_FOR;
"""
    code_parts.append(phase2)

    # -------------------------------------------------------------
    # 7. CYBER-PHYSICAL HEAT TRANSFER & DOUGH OBSERVER (PHASE 3)
    # -------------------------------------------------------------
    phase3 = """
(* ========================================================================================= *)
(* PHASE 3: CYBER-PHYSICAL CONJUGATE HEAT TRANSFER & DOUGH BAKING OBSERVER                   *)
(* ========================================================================================= *)
(* Convert Temperatures to Kelvin for Radiative Stefan-Boltzmann Formulations *)
rT_upper_K := rVotedZoneTemp_Upper_degC[1] + 273.15;
rT_lower_K := rVotedZoneTemp_Lower_degC[1] + 273.15;
rT_dough_K := rDoughSurfaceTemp_degC + 273.15;

(* Stefan-Boltzmann Fourth-Power Radiative Flux from Overhead Ceramic Radiant Elements *)
rRadFluxUpper_Wm2 := rStefanBoltzmann_sigma * 0.90 * 0.85 * (EXPT(rT_upper_K, 4.0) - EXPT(rT_dough_K, 4.0));
IF rRadFluxUpper_Wm2 < 0.0 THEN
    rRadFluxUpper_Wm2 := 0.0;
END_IF;

(* Forced Convective Heat Flux from Recirculating Combustion Air Blower Jets *)
rConvFluxUpper_Wm2 := (22.5 + 0.35 * rCombAirBlowerCmd_Upper_pct[1]) * (rVotedZoneTemp_Upper_degC[1] - rDoughSurfaceTemp_degC);
IF rConvFluxUpper_Wm2 < 0.0 THEN
    rConvFluxUpper_Wm2 := 0.0;
END_IF;

(* Conductive Heat Flux from Carbon-Steel Wire-Mesh Conveyor Belt into Dough Base *)
rCondFluxLower_Wm2 := (45.0) * (rVotedZoneTemp_Lower_degC[1] - rDoughSurfaceTemp_degC);
IF rCondFluxLower_Wm2 < 0.0 THEN
    rCondFluxLower_Wm2 := 0.0;
END_IF;

(* Evaporative Mass Loss & Latent Cooling Flux *)
IF rDoughSurfaceTemp_degC >= 60.0 THEN
    rEvapCoolingFlux_Wm2 := (0.015 * (rDoughSurfaceTemp_degC - 55.0)) * (1.0 - (rVotedChamberRH_pct[1] / 100.0)) * rWaterHeatVaporization_kJkg;
ELSE
    rEvapCoolingFlux_Wm2 := 0.0;
END_IF;

(* Multi-Node 1D Transient Radial Conduction Observer for 800-gram Pan Bread Loaf *)
(* Surface node differential equation: q_net = q_rad + q_conv - q_evap *)
rDoughSurfaceTemp_degC := rDoughSurfaceTemp_degC + rSampleTime_Ts_s * (
    (rRadFluxUpper_Wm2 + rConvFluxUpper_Wm2 - rEvapCoolingFlux_Wm2) / (rDoughSpecificHeat_kJkgK * 1000.0 * 2.5)
    - (rThermalConductivityDough / (rDoughLoafRadius_m * 0.5)) * (rDoughSurfaceTemp_degC - rDoughMidTemp_degC)
);

(* Mid-crumb node differential equation (Gelatinization domain 55 to 85 deg C) *)
rDoughMidTemp_degC := rDoughMidTemp_degC + rSampleTime_Ts_s * (
    (rThermalConductivityDough / (rDoughLoafRadius_m * 0.5)) * (rDoughSurfaceTemp_degC - 2.0 * rDoughMidTemp_degC + rDoughCoreTemp_degC)
);

(* Loaf core node differential equation *)
rDoughCoreTemp_degC := rDoughCoreTemp_degC + rSampleTime_Ts_s * (
    (rThermalConductivityDough / (rDoughLoafRadius_m * 0.5)) * (rDoughMidTemp_degC - rDoughCoreTemp_degC)
);

(* Saturation and Clamping of Observers *)
IF rDoughSurfaceTemp_degC > 210.0 THEN rDoughSurfaceTemp_degC := 210.0; END_IF;
IF rDoughMidTemp_degC > 105.0 THEN rDoughMidTemp_degC := 105.0; END_IF;
IF rDoughCoreTemp_degC > 100.0 THEN rDoughCoreTemp_degC := 100.0; END_IF;

rEstCrumbCoreTemp_degC := rDoughCoreTemp_degC;
rEstCrustSurfaceTemp_degC := rDoughSurfaceTemp_degC;

(* Maillard Reaction Non-Enzymatic Crust Browning Kinetics *)
IF rDoughSurfaceTemp_degC >= 135.0 THEN
    rCrustMaillardRate := 0.00085 * (rDoughSurfaceTemp_degC - 130.0) * (1.0 - (rVotedChamberRH_pct[5] / 100.0));
    rCrustBrowningAccumulator := rCrustBrowningAccumulator + rCrustMaillardRate * rSampleTime_Ts_s;
END_IF;

IF rCrustBrowningAccumulator > 100.0 THEN
    rCrustBrowningAccumulator := 100.0;
END_IF;
rEstCrustBrowningIndex := rCrustBrowningAccumulator;

(* Cumulative Evaporation Moisture Loss Observer *)
IF rDoughSurfaceTemp_degC >= 75.0 THEN
    rCumulativeMoistureLoss_kg := rCumulativeMoistureLoss_kg + (0.000045 * (rDoughSurfaceTemp_degC - 70.0)) * rSampleTime_Ts_s;
END_IF;
rEstDoughMoistureLoss_pct := (rCumulativeMoistureLoss_kg / rDoughLoafMass_kg) * 100.0;
IF rEstDoughMoistureLoss_pct > 14.5 THEN
    rEstDoughMoistureLoss_pct := 14.5; (* Typ. 10-12% moisture loss during industrial baking *)
END_IF;

(* Instantaneous Thermal Power & Gas Flow Aggregation *)
rTotalGasFlow_m3h := 0.0;
FOR iZoneIdx := 1 TO 6 DO
    rZonePowerUpper_kW[iZoneIdx] := (rCombAirFlow_Upper_m3h[iZoneIdx] / rStoichiometricAirGasRatio) * rGasNetCalorificValue_kWhm3;
    rZonePowerLower_kW[iZoneIdx] := (rCombAirFlow_Lower_m3h[iZoneIdx] / rStoichiometricAirGasRatio) * rGasNetCalorificValue_kWhm3;
    rTotalGasFlow_m3h := rTotalGasFlow_m3h + rFuelGasFlow_Upper_m3h[iZoneIdx] + rFuelGasFlow_Lower_m3h[iZoneIdx];
END_FOR;
rTotalThermalPower_kW := rTotalGasFlow_m3h * rGasNetCalorificValue_kWhm3;

(* Energy efficiency calculation: useful heat into dough vs gross gas calorific energy *)
IF rTotalThermalPower_kW > 50.0 THEN
    rOvenThermalEfficiency_pct := ((rRecipe_Throughput_kgh * rBreadSpecificHeat_kJkgK * (rEstCrumbCoreTemp_degC - rDoughInfeedTemp_degC) / 3600.0)
                                  + (rRecipe_Throughput_kgh * (rEstDoughMoistureLoss_pct / 100.0) * rWaterHeatVaporization_kJkg / 3600.0))
                                  / rTotalThermalPower_kW * 100.0;
ELSE
    rOvenThermalEfficiency_pct := 0.0;
END_IF;
"""
    code_parts.append(phase3)

    # -------------------------------------------------------------
    # 8. DISCRETE 8-STATE STATE-SPACE MODEL (PHASE 4)
    # -------------------------------------------------------------
    phase4 = """
(* ========================================================================================= *)
(* PHASE 4: DISCRETE 8-STATE STATE-SPACE PROPAGATION (x[k+1] = A*x[k] + B*u[k])              *)
(* ========================================================================================= *)
IF NOT bMatricesInitialized THEN
    (* 8x8 System Transition Matrix A (Discretized at Ts = 0.50 s) *)
    A_mat[1,1] := 0.9850; A_mat[1,2] := 0.0080; A_mat[1,3] := 0.0020; A_mat[1,4] := 0.0000; A_mat[1,5] := -0.0050; A_mat[1,6] := 0.0030; A_mat[1,7] := 0.0000; A_mat[1,8] := 0.0010;
    A_mat[2,1] := 0.0075; A_mat[2,2] := 0.9820; A_mat[2,3] := 0.0035; A_mat[2,4] := 0.0000; A_mat[2,5] := -0.0030; A_mat[2,6] := 0.0120; A_mat[2,7] := 0.0000; A_mat[2,8] := 0.0005;
    A_mat[3,1] := 0.0040; A_mat[3,2] := 0.0030; A_mat[3,3] := 0.9840; A_mat[3,4] := 0.0050; A_mat[3,5] := -0.0040; A_mat[3,6] := 0.0060; A_mat[3,7] := 0.0000; A_mat[3,8] := 0.0008;
    A_mat[4,1] := 0.0000; A_mat[4,2] := 0.0000; A_mat[4,3] := 0.0065; A_mat[4,4] := 0.9860; A_mat[4,5] := -0.0020; A_mat[4,6] := 0.0050; A_mat[4,7] := 0.0000; A_mat[4,8] := 0.0012;
    A_mat[5,1] := 0.0020; A_mat[5,2] := 0.0020; A_mat[5,3] := 0.0015; A_mat[5,4] := 0.0010; A_mat[5,5] := 0.9650;  A_mat[5,6] := 0.0000; A_mat[5,7] := 0.0000; A_mat[5,8] := -0.0250;
    A_mat[6,1] := 0.0080; A_mat[6,2] := 0.0250; A_mat[6,3] := 0.0100; A_mat[6,4] := 0.0080; A_mat[6,5] := 0.0000;  A_mat[6,6] := 0.9600; A_mat[6,7] := -0.0050; A_mat[6,8] := 0.0000;
    A_mat[7,1] := 0.0010; A_mat[7,2] := 0.0015; A_mat[7,3] := 0.0025; A_mat[7,4] := 0.0030; A_mat[7,5] := 0.0005;  A_mat[7,6] := 0.0045; A_mat[7,7] := 0.9880; A_mat[7,8] := 0.0000;
    A_mat[8,1] := 0.0005; A_mat[8,2] := 0.0005; A_mat[8,3] := 0.0005; A_mat[8,4] := 0.0005; A_mat[8,5] := 0.0000;  A_mat[8,6] := 0.0000; A_mat[8,7] := 0.0000; A_mat[8,8] := 0.9100;

    (* 8x6 Input Coupling Matrix B *)
    B_mat[1,1] := 0.1250; B_mat[1,2] := 0.0100; B_mat[1,3] := -0.0150; B_mat[1,4] := 0.0050; B_mat[1,5] := -0.0080; B_mat[1,6] := -0.0200;
    B_mat[2,1] := 0.0080; B_mat[2,2] := 0.1450; B_mat[2,3] := -0.0120; B_mat[2,4] := 0.0020; B_mat[2,5] := -0.0050; B_mat[2,6] := -0.0250;
    B_mat[3,1] := 0.0350; B_mat[3,2] := 0.0400; B_mat[3,3] := -0.0100; B_mat[3,4] := 0.0000; B_mat[3,5] := -0.0120; B_mat[3,6] := -0.0180;
    B_mat[4,1] := 0.0150; B_mat[4,2] := 0.0200; B_mat[4,3] := -0.0080; B_mat[4,4] := 0.0000; B_mat[4,5] := -0.0150; B_mat[4,6] := -0.0150;
    B_mat[5,1] := 0.0050; B_mat[5,2] := 0.0050; B_mat[5,3] := -0.0020; B_mat[5,4] := 0.2800; B_mat[5,5] := -0.3200; B_mat[5,6] := 0.0450;
    B_mat[6,1] := 0.0150; B_mat[6,2] := 0.0350; B_mat[6,3] := -0.0050; B_mat[6,4] := 0.0000; B_mat[6,5] := -0.0020; B_mat[6,6] := -0.0500;
    B_mat[7,1] := 0.0005; B_mat[7,2] := 0.0010; B_mat[7,3] := 0.0000;  B_mat[7,4] := 0.0020; B_mat[7,5] := 0.0000;  B_mat[7,6] := -0.0850;
    B_mat[8,1] := 0.0020; B_mat[8,2] := 0.0020; B_mat[8,3] := 0.0150;  B_mat[8,4] := 0.0010; B_mat[8,5] := 0.0450;  B_mat[8,6] := 0.0000;

    (* 6x8 Output Observation Matrix C *)
    FOR iOutIdx := 1 TO 6 DO
        FOR iStateIdx := 1 TO 8 DO
            C_mat[iOutIdx, iStateIdx] := 0.0;
        END_FOR;
    END_FOR;
    C_mat[1,1] := 1.0; (* y[1] = Zone 1-2 Upper Temp *)
    C_mat[2,2] := 1.0; (* y[2] = Zone 1-2 Lower Temp *)
    C_mat[3,3] := 1.0; (* y[3] = Zone 3-4 Temp *)
    C_mat[4,4] := 1.0; (* y[4] = Zone 5-6 Temp *)
    C_mat[5,5] := 1.0; (* y[5] = Chamber RH *)
    C_mat[6,8] := 1.0; (* y[6] = Flue Draft *)

    (* MPC Quadratic Weights Initialization *)
    Q_diag[1] := 2.50;  (* Zone 1-2 upper temp penalty *)
    Q_diag[2] := 2.20;  (* Zone 1-2 lower temp penalty *)
    Q_diag[3] := 3.00;  (* Zone 3-4 temp penalty *)
    Q_diag[4] := 4.50;  (* Zone 5-6 browning temp penalty *)
    Q_diag[5] := 3.80;  (* Chamber humidity penalty *)
    Q_diag[6] := 1.20;  (* Belt energy penalty *)
    Q_diag[7] := 15.00; (* CRITICAL: Crumb core temperature tracking penalty *)
    Q_diag[8] := 5.00;  (* Flue draft negative pressure penalty *)

    R_diag[1] := 0.85;  (* Upper gas valve rate effort penalty *)
    R_diag[2] := 0.85;  (* Lower gas valve rate effort penalty *)
    R_diag[3] := 0.40;  (* Combustion air blower effort penalty *)
    R_diag[4] := 1.10;  (* Steam pulse valve overshoot penalty *)
    R_diag[5] := 0.60;  (* Exhaust damper movement penalty *)
    R_diag[6] := 2.50;  (* Conveyor belt speed hunting penalty *)

    P_diag[1] := 5.0; P_diag[2] := 5.0; P_diag[3] := 6.0; P_diag[4] := 8.0;
    P_diag[5] := 7.0; P_diag[6] := 2.0; P_diag[7] := 35.0; P_diag[8] := 10.0;

    bMatricesInitialized := TRUE;
END_IF;

(* Assemble Sensory Measurement Feedback Vector y_measured *)
y_measured[1] := 0.5 * (rVotedZoneTemp_Upper_degC[1] + rVotedZoneTemp_Upper_degC[2]);
y_measured[2] := 0.5 * (rVotedZoneTemp_Lower_degC[1] + rVotedZoneTemp_Lower_degC[2]);
y_measured[3] := 0.5 * (rVotedZoneTemp_Upper_degC[3] + rVotedZoneTemp_Upper_degC[4]);
y_measured[4] := 0.5 * (rVotedZoneTemp_Upper_degC[5] + rVotedZoneTemp_Upper_degC[6]);
y_measured[5] := rVotedChamberRH_pct[1];
y_measured[6] := rVotedFlueDraft_mbar;

(* State Estimation & Observer Residual Update *)
FOR iOutIdx := 1 TO 6 DO
    y_observed[iOutIdx] := 0.0;
    FOR iStateIdx := 1 TO 8 DO
        y_observed[iOutIdx] := y_observed[iOutIdx] + C_mat[iOutIdx, iStateIdx] * x_state[iStateIdx];
    END_FOR;
END_FOR;

(* Luenberger State Correction: x_state = x_state + L * (y_measured - y_observed) *)
x_state[1] := x_state[1] + 0.15 * (y_measured[1] - y_observed[1]);
x_state[2] := x_state[2] + 0.15 * (y_measured[2] - y_observed[2]);
x_state[3] := x_state[3] + 0.15 * (y_measured[3] - y_observed[3]);
x_state[4] := x_state[4] + 0.15 * (y_measured[4] - y_observed[4]);
x_state[5] := x_state[5] + 0.20 * (y_measured[5] - y_observed[5]);
x_state[6] := x_state[6] + 0.10 * (y_measured[2] - y_observed[2]);
x_state[7] := x_state[7] + 0.05 * (rEstCrumbCoreTemp_degC - x_state[7]);
x_state[8] := x_state[8] + 0.30 * (y_measured[6] - y_observed[6]);

(* Pack Current Control Inputs for Forward Simulation *)
u_control[1] := rGasValveCmd_Upper_pct[1];
u_control[2] := rGasValveCmd_Lower_pct[1];
u_control[3] := rCombAirBlowerCmd_Upper_pct[1];
u_control[4] := rRecipe_SteamPulseDuty_pct;
u_control[5] := rExhaustDamperCmd_pct[1];
u_control[6] := rVotedBeltSpeed_mpm;

(* State-Space Time Propagation: x_next = A * x_state + B * u_control *)
FOR iStateIdx := 1 TO 8 DO
    x_next[iStateIdx] := 0.0;
    FOR iInputIdx := 1 TO 8 DO
        x_next[iStateIdx] := x_next[iStateIdx] + A_mat[iStateIdx, iInputIdx] * x_state[iInputIdx];
    END_FOR;
    FOR iInputIdx := 1 TO 6 DO
        x_next[iStateIdx] := x_next[iStateIdx] + B_mat[iStateIdx, iInputIdx] * u_control[iInputIdx];
    END_FOR;
END_FOR;

(* Update state registers for next cycle *)
FOR iStateIdx := 1 TO 8 DO
    x_state[iStateIdx] := x_next[iStateIdx];
END_FOR;
"""
    code_parts.append(phase4)

    # -------------------------------------------------------------
    # 9. RECEDING-HORIZON MPC OPTIMIZER (PHASE 5)
    # -------------------------------------------------------------
    phase5 = """
(* ========================================================================================= *)
(* PHASE 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZER                        *)
(* ========================================================================================= *)
(* Define Reference Trajectory x_ref *)
x_ref[1] := 0.5 * (rRecipe_ZoneTempSP_Upper_degC[1] + rRecipe_ZoneTempSP_Upper_degC[2]);
x_ref[2] := 0.5 * (rRecipe_ZoneTempSP_Lower_degC[1] + rRecipe_ZoneTempSP_Lower_degC[2]);
x_ref[3] := 0.5 * (rRecipe_ZoneTempSP_Upper_degC[3] + rRecipe_ZoneTempSP_Upper_degC[4]);
x_ref[4] := 0.5 * (rRecipe_ZoneTempSP_Upper_degC[5] + rRecipe_ZoneTempSP_Upper_degC[6]);
x_ref[5] := rRecipe_ZoneRH_SP_pct[1];
x_ref[6] := x_ref[2] * 0.92; (* Belt reference temperature tracking lower hearth *)
x_ref[7] := rRecipe_TargetCrumbCoreTemp_degC; (* Target crumb core: 96.0 - 98.0 deg C *)
x_ref[8] := rRecipe_FlueDraftSP_mbar;

(* Evaluate Cost Function J *)
rCostFunction_J := 0.0;
FOR iStateIdx := 1 TO 8 DO
    rCostFunction_J := rCostFunction_J + Q_diag[iStateIdx] * EXPT(x_state[iStateIdx] - x_ref[iStateIdx], 2.0);
END_FOR;
FOR iInputIdx := 1 TO 6 DO
    rCostFunction_J := rCostFunction_J + R_diag[iInputIdx] * EXPT(u_control[iInputIdx] - u_prev[iInputIdx], 2.0);
END_FOR;

(* Gradient-Descent Optimization Iteration to derive Delta_u *)
FOR iInputIdx := 1 TO 6 DO
    grad_J[iInputIdx] := 0.0;
    FOR iStateIdx := 1 TO 8 DO
        grad_J[iInputIdx] := grad_J[iInputIdx] + 2.0 * B_mat[iStateIdx, iInputIdx] * Q_diag[iStateIdx] * (x_state[iStateIdx] - x_ref[iStateIdx]);
    END_FOR;
    grad_J[iInputIdx] := grad_J[iInputIdx] + 2.0 * R_diag[iInputIdx] * (u_control[iInputIdx] - u_prev[iInputIdx]);

    (* Hessian diagonal element approximation *)
    H_diag[iInputIdx] := 2.0 * R_diag[iInputIdx] + 0.15;

    (* Slew rate correction increment *)
    delta_u[iInputIdx] := - rStepAlpha * (grad_J[iInputIdx] / H_diag[iInputIdx]);
END_FOR;

(* Apply MPC Increments with Actuator Rate Saturation Limits *)
(* Control 1: Upper Gas Valve Firing *)
IF delta_u[1] > (rMaxGasSlewRate_pcts * rSampleTime_Ts_s) THEN delta_u[1] := rMaxGasSlewRate_pcts * rSampleTime_Ts_s; END_IF;
IF delta_u[1] < (-rMaxGasSlewRate_pcts * rSampleTime_Ts_s) THEN delta_u[1] := -rMaxGasSlewRate_pcts * rSampleTime_Ts_s; END_IF;

(* Control 2: Lower Gas Valve Firing *)
IF delta_u[2] > (rMaxGasSlewRate_pcts * rSampleTime_Ts_s) THEN delta_u[2] := rMaxGasSlewRate_pcts * rSampleTime_Ts_s; END_IF;
IF delta_u[2] < (-rMaxGasSlewRate_pcts * rSampleTime_Ts_s) THEN delta_u[2] := -rMaxGasSlewRate_pcts * rSampleTime_Ts_s; END_IF;

(* Control 3: Combustion Air Blower *)
IF delta_u[3] > (rMaxAirSlewRate_pcts * rSampleTime_Ts_s) THEN delta_u[3] := rMaxAirSlewRate_pcts * rSampleTime_Ts_s; END_IF;
IF delta_u[3] < (-rMaxAirSlewRate_pcts * rSampleTime_Ts_s) THEN delta_u[3] := -rMaxAirSlewRate_pcts * rSampleTime_Ts_s; END_IF;

(* Control 4: Zone 1 Steam Pulse Duty *)
IF delta_u[4] > 5.0 THEN delta_u[4] := 5.0; END_IF;
IF delta_u[4] < -5.0 THEN delta_u[4] := -5.0; END_IF;

(* Control 5: Exhaust Moisture Damper *)
IF delta_u[5] > (rMaxDamperSlewRate_pcts * rSampleTime_Ts_s) THEN delta_u[5] := rMaxDamperSlewRate_pcts * rSampleTime_Ts_s; END_IF;
IF delta_u[5] < (-rMaxDamperSlewRate_pcts * rSampleTime_Ts_s) THEN delta_u[5] := -rMaxDamperSlewRate_pcts * rSampleTime_Ts_s; END_IF;

(* Control 6: Conveyor Belt Speed *)
IF delta_u[6] > (rMaxBeltAcc_mpms * rSampleTime_Ts_s) THEN delta_u[6] := rMaxBeltAcc_mpms * rSampleTime_Ts_s; END_IF;
IF delta_u[6] < (-rMaxBeltAcc_mpms * rSampleTime_Ts_s) THEN delta_u[6] := -rMaxBeltAcc_mpms * rSampleTime_Ts_s; END_IF;

(* STOICHIOMETRIC CROSS-LIMITING AIR-TO-FUEL COMBUSTION CONTROL *)
(* Principle: Air leads gas on firing increase; Gas leads air on firing decrease *)
FOR iZoneIdx := 1 TO 6 DO
    rTargetGasFiring_Upper[iZoneIdx] := LIMIT(15.0, rGasValveCmd_Upper_pct[iZoneIdx] + delta_u[1], 100.0);
    rTargetGasFiring_Lower[iZoneIdx] := LIMIT(15.0, rGasValveCmd_Lower_pct[iZoneIdx] + delta_u[2], 100.0);

    (* Cross-limiting Upper Burners *)
    IF rTargetGasFiring_Upper[iZoneIdx] > rGasValveCmd_Upper_pct[iZoneIdx] THEN
        (* Firing increasing: Boost combustion air first *)
        rCombAirBlowerCmd_Upper_pct[iZoneIdx] := LIMIT(20.0, rTargetGasFiring_Upper[iZoneIdx] * rTargetExcessAirLambda, 100.0);
        rGasValveCmd_Upper_pct[iZoneIdx] := MIN(rTargetGasFiring_Upper[iZoneIdx], rCombAirBlowerCmd_Upper_pct[iZoneIdx] / rTargetExcessAirLambda);
    ELSE
        (* Firing decreasing: Lower fuel gas first *)
        rGasValveCmd_Upper_pct[iZoneIdx] := rTargetGasFiring_Upper[iZoneIdx];
        rCombAirBlowerCmd_Upper_pct[iZoneIdx] := LIMIT(20.0, rGasValveCmd_Upper_pct[iZoneIdx] * rTargetExcessAirLambda, 100.0);
    END_IF;

    (* Cross-limiting Lower Burners *)
    IF rTargetGasFiring_Lower[iZoneIdx] > rGasValveCmd_Lower_pct[iZoneIdx] THEN
        rCombAirBlowerCmd_Lower_pct[iZoneIdx] := LIMIT(20.0, rTargetGasFiring_Lower[iZoneIdx] * rTargetExcessAirLambda, 100.0);
        rGasValveCmd_Lower_pct[iZoneIdx] := MIN(rTargetGasFiring_Lower[iZoneIdx], rCombAirBlowerCmd_Lower_pct[iZoneIdx] / rTargetExcessAirLambda);
    ELSE
        rGasValveCmd_Lower_pct[iZoneIdx] := rTargetGasFiring_Lower[iZoneIdx];
        rCombAirBlowerCmd_Lower_pct[iZoneIdx] := LIMIT(20.0, rGasValveCmd_Lower_pct[iZoneIdx] * rTargetExcessAirLambda, 100.0);
    END_IF;

    (* Exhaust Damper Modulation to Maintain Chamber Moisture and Flue Draft *)
    rExhaustDamperCmd_pct[iZoneIdx] := LIMIT(10.0, rExhaustDamperCmd_pct[iZoneIdx] + delta_u[5] + 0.15 * (rVotedChamberRH_pct[iZoneIdx] - rRecipe_ZoneRH_SP_pct[iZoneIdx]), 100.0);
END_FOR;

(* Save prior control inputs *)
FOR iInputIdx := 1 TO 6 DO
    u_prev[iInputIdx] := u_control[iInputIdx];
END_FOR;
"""
    code_parts.append(phase5)

    # -------------------------------------------------------------
    # 10. ACTIVE PNEUMATIC BELT TRACKING & EDGE CENTERING (PHASE 6)
    # -------------------------------------------------------------
    phase6 = """
(* ========================================================================================= *)
(* PHASE 6: ACTIVE PNEUMATIC WIRE-MESH BELT TRACKING & EDGE TENSION CENTERING               *)
(* ========================================================================================= *)
(* Differential Lateral Edge Runout Calculation *)
rBeltTrackingError_mm := (rBeltEdgePos_Left_mm - rBeltEdgePos_Right_mm) * 0.50;

(* Deadband filter to prevent continuous actuator hunting (+/- 1.5 mm) *)
IF ABS(rBeltTrackingError_mm) <= 1.5 THEN
    rBeltTrackingError_mm := 0.0;
END_IF;

(* Proportional-Integral (PI) Centering Governor *)
rBeltTrackingIntegral_mm := rBeltTrackingIntegral_mm + rBeltTrackingError_mm * rSampleTime_Ts_s;
IF rBeltTrackingIntegral_mm > 50.0 THEN rBeltTrackingIntegral_mm := 50.0; END_IF;
IF rBeltTrackingIntegral_mm < -50.0 THEN rBeltTrackingIntegral_mm := -50.0; END_IF;

rBeltTrackingDiffPressure_bar := (rTrackKp * rBeltTrackingError_mm) + (rTrackKi * rBeltTrackingIntegral_mm);
rBeltTrackingDiffPressure_bar := LIMIT(-1.80, rBeltTrackingDiffPressure_bar, 1.80);

(* Apply differential steering to left and right pneumatic idler cylinders *)
rPneumaticTrackPress_Left_bar := LIMIT(1.5, rNominalTrackingPressure_bar - rBeltTrackingDiffPressure_bar, 5.5);
rPneumaticTrackPress_Right_bar := LIMIT(1.5, rNominalTrackingPressure_bar + rBeltTrackingDiffPressure_bar, 5.5);

(* Active Catenary Belt Tension Regulation *)
rTensionError_kN := rTargetBeltTension_kN - (rBeltTension_Left_kN + rBeltTension_Right_kN);
rBeltTensionCylinderCmd_bar := LIMIT(2.0, rNominalTensionPressure_bar + (rTensionKp * rTensionError_kN), 6.5);

(* Belt runout emergency alarm evaluation *)
tBeltDriftTripTimer(IN := (ABS(rBeltEdgePos_Left_mm) > rAlarmBeltDriftTrip_mm) OR (ABS(rBeltEdgePos_Right_mm) > rAlarmBeltDriftTrip_mm), PT := T#3S);
IF tBeltDriftTripTimer.Q THEN
    bAlarmTripped_BeltDrift := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; (* Bit 2: Conveyor Belt Lateral Drift Emergency Runout *)
END_IF;
"""
    code_parts.append(phase6)

    # -------------------------------------------------------------
    # 11. ZONE 1 SATURATED STEAM PULSE INJECTION (PHASE 7)
    # -------------------------------------------------------------
    phase7 = """
(* ========================================================================================= *)
(* PHASE 7: ZONE 1 SATURATED STEAM DEPOSITION CHAMBER PULSE INJECTION                        *)
(* ========================================================================================= *)
IF bSteamZone1Enable AND bSteamCondensateTrapOK AND (rSteamSupplyPress_bar >= 2.5) THEN
    (* Saturated steam modulating control valve tracks zone setpoint *)
    rSteamModulatingValveCmd_pct := LIMIT(0.0, 50.0 + 1.2 * (rRecipe_ZoneRH_SP_pct[1] - rVotedChamberRH_pct[1]), 100.0);

    (* High-Velocity Pulse Steam Injection Solenoid Logic *)
    rSteamPulseTimer_s := rSteamPulseTimer_s + rSampleTime_Ts_s;
    IF rSteamPulseTimer_s >= rSteamPulsePeriod_s THEN
        rSteamPulseTimer_s := 0.0;
    END_IF;

    rSteamPulseDuration_s := (rRecipe_SteamPulseDuty_pct / 100.0) * rSteamPulsePeriod_s;
    IF (rSteamPulseTimer_s <= rSteamPulseDuration_s) AND (rVotedChamberRH_pct[1] < (rRecipe_ZoneRH_SP_pct[1] + 5.0)) THEN
        bSteamPulseSolenoidCmd := TRUE;
    ELSE
        bSteamPulseSolenoidCmd := FALSE;
    END_IF;
ELSE
    rSteamModulatingValveCmd_pct := 0.0;
    bSteamPulseSolenoidCmd := FALSE;
    IF NOT bSteamCondensateTrapOK THEN
        dwWarningWord := dwWarningWord OR 16#0000_0400; (* Steam condensate trap high liquid level warning *)
    END_IF;
END_IF;
"""
    code_parts.append(phase7)

    # -------------------------------------------------------------
    # 12. 12-STAGE FINITE STATE MACHINE (PHASE 8)
    # -------------------------------------------------------------
    phase8 = """
(* ========================================================================================= *)
(* PHASE 8: 12-STAGE FINITE STATE MACHINE (FSM) SUPERVISORY CONTROL                          *)
(* ========================================================================================= *)
CASE iState OF
    (* ------------------------------------------------------------------------------------- *)
    (* STATE 0: IDLE / SYSTEM READY & INITIAL COLD STANDBY                                  *)
    (* ------------------------------------------------------------------------------------- *)
    0:
        bSystemReady := TRUE;
        bSystemRunning := FALSE;
        bPrePurgeActive := FALSE;
        bPrePurgeCompleted := FALSE;
        bContinuousBakeActive := FALSE;
        bRecipeTransitionActive := FALSE;

        (* Ensure all gas valves are confirmed closed via POC limit switches *)
        FOR iZoneIdx := 1 TO 6 DO
            bSafetyShutoffValve_Upper[iZoneIdx] := FALSE;
            bSafetyShutoffValve_Lower[iZoneIdx] := FALSE;
            rGasValveCmd_Upper_pct[iZoneIdx] := 0.0;
            rGasValveCmd_Lower_pct[iZoneIdx] := 0.0;
            bSparkIgniter_Upper[iZoneIdx] := FALSE;
            bSparkIgniter_Lower[iZoneIdx] := FALSE;
            rCombAirBlowerCmd_Upper_pct[iZoneIdx] := 0.0;
            rCombAirBlowerCmd_Lower_pct[iZoneIdx] := 0.0;
        END_FOR;

        rConveyorVfdSpeedCmd_mpm := 0.0;
        rMainExhaustFanSpeedCmd_pct := 15.0;

        IF bEnableSystem AND bEmergencyStop AND NOT bSystemTripped THEN
            iState := 1; (* Proceed to NFPA 86 Forced Ventilation Pre-Purge *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 1: PRE_PURGE (NFPA 86 MANDATORY 4-VOLUME AIR CHANGE PURGE)                     *)
    (* ------------------------------------------------------------------------------------- *)
    1:
        bPrePurgeActive := TRUE;
        bSystemReady := FALSE;
        bSystemRunning := TRUE;

        (* Open all exhaust dampers 100% and run combustion air blowers at >= 70% *)
        FOR iZoneIdx := 1 TO 6 DO
            rExhaustDamperCmd_pct[iZoneIdx] := 100.0;
            rCombAirBlowerCmd_Upper_pct[iZoneIdx] := 75.0;
            rCombAirBlowerCmd_Lower_pct[iZoneIdx] := 75.0;
        END_FOR;
        rMainExhaustFanSpeedCmd_pct := 85.0;

        (* Conveyor runs at low ventilation speed *)
        rConveyorVfdSpeedCmd_mpm := 1.0;

        (* Purge timer: minimum 300 seconds (5 minutes) for 4 chamber volume exchanges *)
        tPrePurgeTimer(IN := (rCombAirHeaderPress_mbar >= 12.0) AND (rVotedFlueDraft_mbar <= -0.15), PT := T#300S);

        IF tPrePurgeTimer.Q THEN
            bPrePurgeCompleted := TRUE;
            bPrePurgeActive := FALSE;
            iState := 2; (* Proceed to Pilot Ignition *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 2: PILOT_IGNITION & FLAME ESTABLISHMENT                                         *)
    (* ------------------------------------------------------------------------------------- *)
    2:
        (* Throttle combustion air to pilot ignition light-off rate (25%) *)
        FOR iZoneIdx := 1 TO 6 DO
            rCombAirBlowerCmd_Upper_pct[iZoneIdx] := 25.0;
            rCombAirBlowerCmd_Lower_pct[iZoneIdx] := 25.0;
        END_FOR;

        (* Energize spark igniters and open pilot gas valves *)
        FOR iZoneIdx := 1 TO 6 DO
            bSparkIgniter_Upper[iZoneIdx] := TRUE;
            bSparkIgniter_Lower[iZoneIdx] := TRUE;
            bSafetyShutoffValve_Upper[iZoneIdx] := TRUE;
            bSafetyShutoffValve_Lower[iZoneIdx] := TRUE;
            rGasValveCmd_Upper_pct[iZoneIdx] := 18.0;
            rGasValveCmd_Lower_pct[iZoneIdx] := 18.0;
        END_FOR;

        tPilotIgnitionTimer(IN := TRUE, PT := T#10S);

        (* Check flame scanner confirmation via 2oo3 voted flame signals *)
        bPilotsEstablished := TRUE;
        FOR iZoneIdx := 1 TO 6 DO
            IF NOT bUpperFlameVoted[iZoneIdx] OR NOT bLowerFlameVoted[iZoneIdx] THEN
                bPilotsEstablished := FALSE;
            END_IF;
        END_FOR;

        IF bPilotsEstablished AND (tPilotIgnitionTimer.ET >= T#4S) THEN
            (* De-energize spark transformers once flame is confirmed *)
            FOR iZoneIdx := 1 TO 6 DO
                bSparkIgniter_Upper[iZoneIdx] := FALSE;
                bSparkIgniter_Lower[iZoneIdx] := FALSE;
            END_FOR;
            iState := 3; (* Proceed to Zone Temperature Ramp Preheat *)
            iSubState := 0;
        ELSIF tPilotIgnitionTimer.Q AND NOT bPilotsEstablished THEN
            (* Pilot ignition trial period expired without flame confirmation *)
            bAlarmTripped_FlameFailure := TRUE;
            dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* Bit 2: Pilot Flame Establishment Failure *)
            iState := 10; (* Emergency Fuel Slam-Shut *)
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 3: ZONE_RAMP_PREHEAT (CONTROLLED REFRACTORY WARMUP)                             *)
    (* ------------------------------------------------------------------------------------- *)
    3:
        (* Controlled ramp: Gas firing modulated to not exceed 3.5 deg C / min thermal rise *)
        FOR iZoneIdx := 1 TO 6 DO
            IF rVotedZoneTemp_Upper_degC[iZoneIdx] < (rRecipe_ZoneTempSP_Upper_degC[iZoneIdx] - 5.0) THEN
                rGasValveCmd_Upper_pct[iZoneIdx] := LIMIT(20.0, rGasValveCmd_Upper_pct[iZoneIdx] + 0.10, 85.0);
            ELSE
                rGasValveCmd_Upper_pct[iZoneIdx] := LIMIT(20.0, rGasValveCmd_Upper_pct[iZoneIdx] - 0.10, 85.0);
            END_IF;

            IF rVotedZoneTemp_Lower_degC[iZoneIdx] < (rRecipe_ZoneTempSP_Lower_degC[iZoneIdx] - 5.0) THEN
                rGasValveCmd_Lower_pct[iZoneIdx] := LIMIT(20.0, rGasValveCmd_Lower_pct[iZoneIdx] + 0.10, 85.0);
            ELSE
                rGasValveCmd_Lower_pct[iZoneIdx] := LIMIT(20.0, rGasValveCmd_Lower_pct[iZoneIdx] - 0.10, 85.0);
            END_IF;
        END_FOR;

        (* Run wire mesh belt at preheat circulation speed to prevent localized thermal warping *)
        rConveyorVfdSpeedCmd_mpm := 1.5;

        (* Verify when all zones reach within +/- 8.0 deg C of target recipe setpoints *)
        iSubState := 1;
        FOR iZoneIdx := 1 TO 6 DO
            IF (ABS(rVotedZoneTemp_Upper_degC[iZoneIdx] - rRecipe_ZoneTempSP_Upper_degC[iZoneIdx]) > 8.0) OR
               (ABS(rVotedZoneTemp_Lower_degC[iZoneIdx] - rRecipe_ZoneTempSP_Lower_degC[iZoneIdx]) > 8.0) THEN
                iSubState := 0;
            END_IF;
        END_FOR;

        IF iSubState = 1 THEN
            iState := 4; (* Proceed to Steam Chamber Priming *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 4: STEAM_CHAMBER_PRIME (ZONE 1 MOISTURE SATURATION)                            *)
    (* ------------------------------------------------------------------------------------- *)
    4:
        (* Open Zone 1 steam header and pulse manifolds to establish initial 70% RH vapor blanket *)
        rSteamModulatingValveCmd_pct := 80.0;
        bSteamPulseSolenoidCmd := TRUE;
        rExhaustDamperCmd_pct[1] := 15.0; (* Throttle Zone 1 exhaust damper to retain saturated steam *)

        tSteamChamberPrimeTimer(IN := (rVotedChamberRH_pct[1] >= 65.0), PT := T#60S);

        IF tSteamChamberPrimeTimer.Q THEN
            bSteamChamberReady := TRUE;
            iState := 5; (* Proceed to Dough Infeed Loading Synchronization *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 5: DOUGH_LOADING_SYNC (PROOFER DISCHARGE SYNCHRONIZATION)                      *)
    (* ------------------------------------------------------------------------------------- *)
    5:
        (* Accelerate conveyor to recipe nominal speed *)
        rConveyorVfdSpeedCmd_mpm := rRecipe_BeltSpeedSP_mpm;

        tBakeSteadySyncTimer(IN := bDoughInfeedPresent AND (rDoughInfeedRate_kgh >= (rRecipe_Throughput_kgh * 0.75)), PT := T#45S);

        IF tBakeSteadySyncTimer.Q AND bAutoBakeEnable THEN
            bContinuousBakeActive := TRUE;
            iState := 6; (* Enter Continuous Steady-State Baking *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 6: CONTINUOUS_STEADY_STATE_BAKING (FULL CLOSED-LOOP MPC GOVERNOR)              *)
    (* ------------------------------------------------------------------------------------- *)
    6:
        bContinuousBakeActive := TRUE;
        rConveyorVfdSpeedCmd_mpm := rRecipe_BeltSpeedSP_mpm + delta_u[6];

        (* Handle dynamic recipe changeover request *)
        IF bRecipeChangeoverReq THEN
            iState := 7; (* Transition to Dynamic Recipe Changeover *)
            iSubState := 0;
        END_IF;

        (* Check if dough infeed has ceased for empty runout *)
        IF NOT bDoughInfeedPresent AND (rDoughInfeedRate_kgh < 100.0) THEN
            iState := 8; (* Enter Runout Empty Bakeout *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 7: DYNAMIC_RECIPE_CHANGEOVER (THERMAL INERTIA TRANSITION)                      *)
    (* ------------------------------------------------------------------------------------- *)
    7:
        bRecipeTransitionActive := TRUE;
        tRecipeTransitionTimer(IN := TRUE, PT := T#180S);

        (* Adjust conveyor speed temporarily to compensate for thermal ramp lag *)
        rConveyorVfdSpeedCmd_mpm := rRecipe_BeltSpeedSP_mpm * 0.95;

        IF tRecipeTransitionTimer.Q THEN
            bRecipeTransitionActive := FALSE;
            iState := 6; (* Return to Continuous Steady-State Baking with new recipe *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 8: RUNOUT_EMPTY_BAKEOUT (DOUGH TRAILING EDGE PURGE)                            *)
    (* ------------------------------------------------------------------------------------- *)
    8:
        bContinuousBakeActive := FALSE;
        (* Maintain steady baking speed until trailing loaves clear Zone 6 *)
        rConveyorVfdSpeedCmd_mpm := rRecipe_BeltSpeedSP_mpm;

        (* Dwell timer: full tunnel residence time (~22 minutes = 1320 s) *)
        tRunoutBakeoutTimer(IN := TRUE, PT := T#1320S);

        IF tRunoutBakeoutTimer.Q THEN
            iState := 9; (* Proceed to Controlled Zone Cooldown *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 9: CONTROLLED_ZONE_COOLDOWN (STAGED REFRACTORY COOLING)                        *)
    (* ------------------------------------------------------------------------------------- *)
    9:
        (* De-energize all main gas burners *)
        FOR iZoneIdx := 1 TO 6 DO
            bSafetyShutoffValve_Upper[iZoneIdx] := FALSE;
            bSafetyShutoffValve_Lower[iZoneIdx] := FALSE;
            rGasValveCmd_Upper_pct[iZoneIdx] := 0.0;
            rGasValveCmd_Lower_pct[iZoneIdx] := 0.0;
            rCombAirBlowerCmd_Upper_pct[iZoneIdx] := 40.0; (* Moderate cooling airflow *)
            rCombAirBlowerCmd_Lower_pct[iZoneIdx] := 40.0;
            rExhaustDamperCmd_pct[iZoneIdx] := 80.0;
        END_FOR;

        (* Run wire mesh belt at creep speed (0.6 m/min) until all zones drop below 80 deg C *)
        rConveyorVfdSpeedCmd_mpm := 0.6;

        iSubState := 1;
        FOR iZoneIdx := 1 TO 6 DO
            IF (rVotedZoneTemp_Upper_degC[iZoneIdx] > 80.0) OR (rVotedZoneTemp_Lower_degC[iZoneIdx] > 80.0) THEN
                iSubState := 0;
            END_IF;
        END_FOR;

        IF iSubState = 1 THEN
            rConveyorVfdSpeedCmd_mpm := 0.0;
            FOR iZoneIdx := 1 TO 6 DO
                rCombAirBlowerCmd_Upper_pct[iZoneIdx] := 0.0;
                rCombAirBlowerCmd_Lower_pct[iZoneIdx] := 0.0;
            END_FOR;
            iState := 0; (* Return to Cold Standby / Idle *)
            iSubState := 0;
        END_IF;

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 10: EMERGENCY_FUEL_SLAM_SHUT (NFPA 86 SAFETY SHUTDOWN)                         *)
    (* ------------------------------------------------------------------------------------- *)
    10:
        bSystemTripped := TRUE;
        bSystemRunning := FALSE;
        bContinuousBakeActive := FALSE;

        (* INSTANTANEOUS DOUBLE BLOCK-AND-BLEED TRIP *)
        FOR iZoneIdx := 1 TO 6 DO
            bSafetyShutoffValve_Upper[iZoneIdx] := FALSE;
            bSafetyShutoffValve_Lower[iZoneIdx] := FALSE;
            rGasValveCmd_Upper_pct[iZoneIdx] := 0.0;
            rGasValveCmd_Lower_pct[iZoneIdx] := 0.0;
            bSparkIgniter_Upper[iZoneIdx] := FALSE;
            bSparkIgniter_Lower[iZoneIdx] := FALSE;
            rExhaustDamperCmd_pct[iZoneIdx] := 100.0;
            rCombAirBlowerCmd_Upper_pct[iZoneIdx] := 50.0;
            rCombAirBlowerCmd_Lower_pct[iZoneIdx] := 50.0;
        END_FOR;

        rSteamModulatingValveCmd_pct := 0.0;
        bSteamPulseSolenoidCmd := FALSE;
        rConveyorVfdSpeedCmd_mpm := 0.0;

        iState := 11; (* Transition to Safety Lockout Diagnostic *)

    (* ------------------------------------------------------------------------------------- *)
    (* STATE 11: FAULT_LOCKOUT_DIAGNOSTIC (MANUAL SAFETY RESET REQUIRED)                    *)
    (* ------------------------------------------------------------------------------------- *)
    11:
        bSystemTripped := TRUE;
        bSystemRunning := FALSE;

        (* Requires operator intervention and bResetFaults unlatch *)
        IF bResetFaults AND NOT bAlarmTripped_FlameFailure AND NOT bAlarmTripped_OverTempHH 
           AND NOT bAlarmTripped_DraftLoss AND NOT bAlarmTripped_GasPressure THEN
            bSystemTripped := FALSE;
            iState := 0; (* Reset to Idle *)
            iSubState := 0;
        END_IF;

ELSE
    iState := 10; (* Unrecognized state trap: force emergency shutdown *)
END_CASE;
"""
    code_parts.append(phase8)

    # -------------------------------------------------------------
    # 13. ISA-18.2 ALARMS & BIT-PACKING (PHASE 9)
    # -------------------------------------------------------------
    phase9 = """
(* ========================================================================================= *)
(* PHASE 9: ISA-18.2 MULTI-TIERED ALARM ENGINE & DIAGNOSTIC WORD BIT-PACKING                 *)
(* ========================================================================================= *)
(* --- 9.1 High-High & Low-Low Critical Safety Limit Evaluations --- *)
FOR iZoneIdx := 1 TO 6 DO
    (* High-High Temperature Flame Slam-Shut Trip *)
    IF (rVotedZoneTemp_Upper_degC[iZoneIdx] >= rAlarmTempHH_degC) OR (rVotedZoneTemp_Lower_degC[iZoneIdx] >= rAlarmTempHH_degC) THEN
        bAlarmTripped_OverTempHH := TRUE;
        dwAlarmWord1 := dwAlarmWord1 OR SHL(16#0000_0010, iZoneIdx - 1);
    END_IF;

    (* Flame Failure Trip in Active Firing States *)
    IF (iState >= 3) AND (iState <= 7) THEN
        IF NOT bUpperFlameVoted[iZoneIdx] OR NOT bLowerFlameVoted[iZoneIdx] THEN
            bAlarmTripped_FlameFailure := TRUE;
            dwAlarmWord1 := dwAlarmWord1 OR SHL(16#0000_0400, iZoneIdx - 1);
        END_IF;
    END_IF;
END_FOR;

(* Gas Supply Main Manifold Pressure Safety Trip *)
IF (rMainGasSupplyPress_bar < rAlarmGasPressLL_bar) OR (rMainGasSupplyPress_bar > rAlarmGasPressHH_bar) THEN
    bAlarmTripped_GasPressure := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Bit 3: Gas Header Supply Pressure Trip *)
END_IF;

(* Exhaust Chimney Draft Loss Trip *)
tDraftLossTripTimer(IN := (rVotedFlueDraft_mbar > rAlarmDraftHH_mbar) OR (rVotedFlueDraft_mbar < rAlarmDraftLL_mbar), PT := T#2S);
IF tDraftLossTripTimer.Q THEN
    bAlarmTripped_DraftLoss := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_4000; (* Bit 14: Flue Draft Failure Trip *)
END_IF;

(* Trip Initiation Interlock *)
IF bAlarmTripped_OverTempHH OR bAlarmTripped_FlameFailure OR bAlarmTripped_GasPressure OR bAlarmTripped_DraftLoss THEN
    bSystemTripped := TRUE;
    IF (iState <> 10) AND (iState <> 11) THEN
        iState := 10; (* Instantaneous NFPA 86 Slam-Shut *)
    END_IF;
END_IF;

(* --- 9.2 Process Warning Evaluations --- *)
FOR iZoneIdx := 1 TO 6 DO
    IF (rVotedZoneTemp_Upper_degC[iZoneIdx] > rAlarmTempH_degC) OR (rVotedZoneTemp_Lower_degC[iZoneIdx] > rAlarmTempH_degC) THEN
        dwWarningWord := dwWarningWord OR SHL(16#0000_0001, iZoneIdx - 1);
    END_IF;

    IF (ABS(rVotedChamberRH_pct[iZoneIdx] - rRecipe_ZoneRH_SP_pct[iZoneIdx]) > 12.0) THEN
        dwWarningWord := dwWarningWord OR SHL(16#0000_0040, iZoneIdx - 1);
    END_IF;
END_FOR;

IF (rBeltTension_Left_kN < 10.0) OR (rBeltTension_Right_kN < 10.0) THEN
    dwWarningWord := dwWarningWord OR 16#0000_1000; (* Bit 12: Wire-mesh belt catenary tension low *)
END_IF;

(* --- 9.3 System Operational Status Word Bit-Packing (dwSystemStatusWord) --- *)
dwSystemStatusWord := 16#0000_0000;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bSystemTripped THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bPrePurgeActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bPrePurgeCompleted THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bPilotsEstablished THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF bSteamChamberReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;
IF bContinuousBakeActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; END_IF;
IF bRecipeTransitionActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; END_IF;
dwSystemStatusWord := dwSystemStatusWord OR SHL(INT_TO_DWORD(iState), 16); (* Store current state index in upper word *)

END_FUNCTION_BLOCK
"""
    code_parts.append(phase9)

    full_st_code = "".join(code_parts)
    return full_st_code

if __name__ == "__main__":
    st_code = generate_tunnel_oven_code()
    print(f"Generated ST code length: {len(st_code)} characters")
