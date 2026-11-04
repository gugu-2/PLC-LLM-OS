# -*- coding: utf-8 -*-
"""
Declarations module for FB_DataCenter_LiquidCooling_CDU_DirectToChip
Contains: Header, VAR_INPUT, VAR_OUTPUT, VAR (internal)
"""

def get_header():
    return """FUNCTION_BLOCK FB_DataCenter_LiquidCooling_CDU_DirectToChip
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
MISSION-CRITICAL INFRASTRUCTURE DIVISION - HYPERSCALER AI DATA CENTER SYSTEMS
========================================================================================================================
SYSTEM SPECIFICATION:
  - Facility Thermal Dissipation Rating: 40.0 MW Continuous Heat Dissipation (Direct-to-Chip Warm Water Cooling)
  - Coolant Media: 25% Industrial Propylene Glycol Aqueous Solution (PG25) with Organic Acid Technology (OAT) Inhibitors
  - Secondary Technology Cooling System (TCS):
      * W32 Temperature Regime: Supply Coolant at 32.0 deg C (+/- 0.2 deg C setpoint), Return Coolant at 44.0 deg C nominal
      * Volumetric Delivery: 4,000.0 L/min (240.0 m3/h) nominal total design circulation across 64 high-density AI server racks
      * Differential Pressure Target: 1.80 bar (+/- 0.05 bar) decoupled loop differential pressure at IT manifold headers
  - Dual Redundant Coolant Distribution Units (CDUs):
      * 2x 100% Canned Motor Inverter Pumps (Pump 1 Lead / Pump 2 Lag, 45.0 kW IE5 SynRM, 0-3500 rpm)
      * Bumpless Lead-Lag Automatic Failover within 250 ms upon cavitation, thermal overload, or VFD fault
  - Heat Exchanger Infrastructure:
      * 2x Primary Plate-and-Frame Heat Exchangers (PHE) with Titanium Plates (42.0 MW combined capacity)
      * Primary Facility Water Supply/Return (FWS/FWR) modulating two-way equal percentage control valve
      * Secondary TCS 3-way fast thermostatic mixing and bypass valve for rapid dynamic supply temperature stabilization
  - Distributed Cyber-Physical Leak & Corrosion Containment:
      * Distributed coaxial/fiber impedance sensing rope matrix across 64 server rack troughs (< 100 ms fast isolation)
      * Motorized fail-safe spring-return fast ball valves for sub-100 ms zone hydraulic containment
      * Continuous Dissolved Oxygen (DO optical luminescence < 20 ppb) and PG concentration refractometry
  - Emergency Thermal Ride-Through Buffer:
      * 120,000 Liter stratified cold thermal storage reservoir providing 120 seconds of continuous 40 MW heat absorption
      * Fast automatic pneumatic switchover upon facility chiller plant power outage or loss of chilled water flow
  - Mathematical & Control Rigor:
      * 2oo3 Triple Modular Redundancy (TMR) across 16 critical physical measurement triplets with discrepancy timers
      * High-Fidelity 8x8 Discrete State-Space Model (x[k+1] = A*x[k] + B*u[k] + Bw*w[k]) executed at Ts = 50 ms
      * Receding-Horizon Model Predictive Control (MPC) optimizing VFD speeds and PHE valve to slash pumping power > 25%
      * Real-Time Thermodynamic & Transport Property Polynomial Evaluators for PG25 (rho, cp, mu, k)
      * Plate Heat Exchanger epsilon-NTU micro-fouling conductance observer (UA tracking)
      * AI Server Cold-Plate micro-channel thermal resistance and peak GPU silicon junction temperature observer
      * ISA-18.2 Compliant Multi-Tiered Alarm Hierarchy (HH, H, L, LL, ROC) with emergency IT compute throttling trigger
========================================================================================================================
*)
"""

def get_var_input():
    return """VAR_INPUT
    (* ========================================================================= *)
    (* SECTION 1: 2oo3 TRIPLE MODULAR REDUNDANT FIELD TRANSMITTER TRIPLET INPUTS *)
    (* ========================================================================= *)
    (* 1. Technology Cooling System (TCS) Supply Flow Rate [L/min] *)
    FT_TCS_SUPPLY_FLOW_101A               : REAL; (* [L/min] TCS Supply Coolant Flow Rate Transmitter Channel A *)
    FT_TCS_SUPPLY_FLOW_101B               : REAL; (* [L/min] TCS Supply Coolant Flow Rate Transmitter Channel B *)
    FT_TCS_SUPPLY_FLOW_101C               : REAL; (* [L/min] TCS Supply Coolant Flow Rate Transmitter Channel C *)

    (* 2. TCS Pump Discharge Header Static Pressure [bar] *)
    PT_TCS_SUPPLY_PRESS_102A              : REAL; (* [bar] TCS Pump Discharge Header Static Pressure Channel A *)
    PT_TCS_SUPPLY_PRESS_102B              : REAL; (* [bar] TCS Pump Discharge Header Static Pressure Channel B *)
    PT_TCS_SUPPLY_PRESS_102C              : REAL; (* [bar] TCS Pump Discharge Header Static Pressure Channel C *)

    (* 3. TCS IT Rack Return Header Static Pressure [bar] *)
    PT_TCS_RETURN_PRESS_103A              : REAL; (* [bar] TCS IT Rack Return Header Static Pressure Channel A *)
    PT_TCS_RETURN_PRESS_103B              : REAL; (* [bar] TCS IT Rack Return Header Static Pressure Channel B *)
    PT_TCS_RETURN_PRESS_103C              : REAL; (* [bar] TCS IT Rack Return Header Static Pressure Channel C *)

    (* 4. TCS Decoupled Manifold Differential Pressure [bar] *)
    DPS_TCS_LOOP_DIFF_PRESS_104A          : REAL; (* [bar] TCS Decoupled Rack Differential Pressure Channel A *)
    DPS_TCS_LOOP_DIFF_PRESS_104B          : REAL; (* [bar] TCS Decoupled Rack Differential Pressure Channel B *)
    DPS_TCS_LOOP_DIFF_PRESS_104C          : REAL; (* [bar] TCS Decoupled Rack Differential Pressure Channel C *)

    (* 5. TCS Supply Coolant Temperature to Server Racks [deg C] *)
    TT_TCS_SUPPLY_TEMP_105A               : REAL; (* [deg C] TCS Supply Coolant Temperature Channel A (Target 32.0 C) *)
    TT_TCS_SUPPLY_TEMP_105B               : REAL; (* [deg C] TCS Supply Coolant Temperature Channel B (Target 32.0 C) *)
    TT_TCS_SUPPLY_TEMP_105C               : REAL; (* [deg C] TCS Supply Coolant Temperature Channel C (Target 32.0 C) *)

    (* 6. TCS Return Coolant Temperature from Server Racks [deg C] *)
    TT_TCS_RETURN_TEMP_106A               : REAL; (* [deg C] TCS Return Coolant Temperature Channel A *)
    TT_TCS_RETURN_TEMP_106B               : REAL; (* [deg C] TCS Return Coolant Temperature Channel B *)
    TT_TCS_RETURN_TEMP_106C               : REAL; (* [deg C] TCS Return Coolant Temperature Channel C *)

    (* 7. Primary Facility Chilled Water Supply Flow Rate [m3/h] *)
    FT_FWS_FACILITY_FLOW_201A             : REAL; (* [m3/h] Facility Chilled Water Primary Flow Channel A *)
    FT_FWS_FACILITY_FLOW_201B             : REAL; (* [m3/h] Facility Chilled Water Primary Flow Channel B *)
    FT_FWS_FACILITY_FLOW_201C             : REAL; (* [m3/h] Facility Chilled Water Primary Flow Channel C *)

    (* 8. Facility Chilled Water Supply Temperature [deg C] *)
    TT_FWS_FACILITY_SUPPLY_202A           : REAL; (* [deg C] Facility Chilled Water Supply Temp Channel A *)
    TT_FWS_FACILITY_SUPPLY_202B           : REAL; (* [deg C] Facility Chilled Water Supply Temp Channel B *)
    TT_FWS_FACILITY_SUPPLY_202C           : REAL; (* [deg C] Facility Chilled Water Supply Temp Channel C *)

    (* 9. Facility Chilled Water Return Temperature [deg C] *)
    TT_FWR_FACILITY_RETURN_203A           : REAL; (* [deg C] Facility Chilled Water Return Temp Channel A *)
    TT_FWR_FACILITY_RETURN_203B           : REAL; (* [deg C] Facility Chilled Water Return Temp Channel B *)
    TT_FWR_FACILITY_RETURN_203C           : REAL; (* [deg C] Facility Chilled Water Return Temp Channel C *)

    (* 10. CDU Pump 1 Shaft Speed Tachometer Feedback [rpm] *)
    ZT_CDU_PUMP1_VFD_RPM_301A             : REAL; (* [rpm] CDU Inverter Pump 1 Shaft Speed Feedback Channel A *)
    ZT_CDU_PUMP1_VFD_RPM_301B             : REAL; (* [rpm] CDU Inverter Pump 1 Shaft Speed Feedback Channel B *)
    ZT_CDU_PUMP1_VFD_RPM_301C             : REAL; (* [rpm] CDU Inverter Pump 1 Shaft Speed Feedback Channel C *)

    (* 11. CDU Pump 2 Shaft Speed Tachometer Feedback [rpm] *)
    ZT_CDU_PUMP2_VFD_RPM_302A             : REAL; (* [rpm] CDU Inverter Pump 2 Shaft Speed Feedback Channel A *)
    ZT_CDU_PUMP2_VFD_RPM_302B             : REAL; (* [rpm] CDU Inverter Pump 2 Shaft Speed Feedback Channel B *)
    ZT_CDU_PUMP2_VFD_RPM_302C             : REAL; (* [rpm] CDU Inverter Pump 2 Shaft Speed Feedback Channel C *)

    (* 12. Primary PHE Modulating Control Valve Position Feedback [%] *)
    ZT_PHE_CONTROL_VALVE_POS_303A         : REAL; (* [%] Primary Heat Exchanger Modulating Valve Position Feedback Channel A *)
    ZT_PHE_CONTROL_VALVE_POS_303B         : REAL; (* [%] Primary Heat Exchanger Modulating Valve Position Feedback Channel B *)
    ZT_PHE_CONTROL_VALVE_POS_303C         : REAL; (* [%] Primary Heat Exchanger Modulating Valve Position Feedback Channel C *)

    (* 13. Propylene Glycol Concentration Refractometer [%] *)
    AIT_GLYCOL_CONCENTRATION_401A         : REAL; (* [%] Coolant Propylene Glycol Concentration Channel A (Nominal 25%) *)
    AIT_GLYCOL_CONCENTRATION_401B         : REAL; (* [%] Coolant Propylene Glycol Concentration Channel B (Nominal 25%) *)
    AIT_GLYCOL_CONCENTRATION_401C         : REAL; (* [%] Coolant Propylene Glycol Concentration Channel C (Nominal 25%) *)

    (* 14. Coolant Dissolved Oxygen / Corrosion Sensor [ppb] *)
    AIT_CORROSION_ORP_DO_402A             : REAL; (* [ppb] Dissolved Oxygen Optical Sensor Channel A (<20 ppb) *)
    AIT_CORROSION_ORP_DO_402B             : REAL; (* [ppb] Dissolved Oxygen Optical Sensor Channel B (<20 ppb) *)
    AIT_CORROSION_ORP_DO_402C             : REAL; (* [ppb] Dissolved Oxygen Optical Sensor Channel C (<20 ppb) *)

    (* 15. Distributed Optical/Polymer Leak Sensing Rope Resistance [Ohm] *)
    OPT_LEAK_ROPE_RESISTANCE_501A         : REAL; (* [Ohm] Distributed Floor Leak Rope Resistance Channel A (Trip < 150 Ohm) *)
    OPT_LEAK_ROPE_RESISTANCE_501B         : REAL; (* [Ohm] Distributed Floor Leak Rope Resistance Channel B (Trip < 150 Ohm) *)
    OPT_LEAK_ROPE_RESISTANCE_501C         : REAL; (* [Ohm] Distributed Floor Leak Rope Resistance Channel C (Trip < 150 Ohm) *)

    (* 16. Emergency Coolant Thermal Storage Reservoir Level [%] *)
    LT_THERMAL_BUFFER_TANK_601A           : REAL; (* [%] Thermal Storage Buffer Tank Level Channel A *)
    LT_THERMAL_BUFFER_TANK_601B           : REAL; (* [%] Thermal Storage Buffer Tank Level Channel B *)
    LT_THERMAL_BUFFER_TANK_601C           : REAL; (* [%] Thermal Storage Buffer Tank Level Channel C *)

    (* ========================================================================= *)
    (* SECTION 2: AI WORKLOAD, TELEMETRY & SUPERVISORY CONTROL COMMANDS          *)
    (* ========================================================================= *)
    rIT_Cluster_Thermal_Load_MW           : REAL; (* [MW] Real-Time Hyperscale AI Accelerator Cluster Total Thermal Power *)
    rAI_Server_Rack_Hotspot_Max_Temp_C    : REAL; (* [deg C] Worst-Case Compute Blade Silicon Hotspot Temperature *)
    rGPU_Compute_Node_Average_Power_kW    : REAL; (* [kW] Average Compute Blade Power Dissipation per Chassis *)
    rFacility_Chilled_Water_DP_bar        : REAL; (* [bar] Facility Supply-Return Differential Pressure *)
    rThermal_Buffer_Tank_Core_Temp_C      : REAL; (* [deg C] Stratified Core Coolant Temperature in Storage Vessel *)
    bCDU_System_Enable                    : BOOL; (* Master CDU Automation Enable Command *)
    bMaster_Alarm_Reset                   : BOOL; (* ISA-18.2 Manual Alarm Acknowledge and Fault Reset Pushbutton *)
    bLead_Pump_Select_1_2                 : BOOL; (* Lead Pump Select: FALSE=Pump 1 Lead, TRUE=Pump 2 Lead *)
    bAuto_Thermal_Buffer_Enable           : BOOL; (* Permissive for Automatic Chiller Outage Ride-Through Deployment *)
    bEmergencyStop_Circuit_NC             : BOOL; (* Dual-Channel Hardware E-Stop Safety Relay (Normally Closed) *)
    tScanTime_DeltaT                      : TIME; (* Discrete Loop Cycle Execution Delta Time (Nominal T#50ms) *)
END_VAR
"""

def get_var_output():
    return """VAR_OUTPUT
    (* ========================================================================= *)
    (* SECTION 1: ACTUATOR DRIVE COMMANDS & FAST SAFETY INTERLOCKS               *)
    (* ========================================================================= *)
    rCDU_Pump1_VFD_Speed_Cmd_RPM          : REAL; (* [rpm] CDU Inverter Pump 1 Speed Reference (0 - 3500 rpm) *)
    rCDU_Pump2_VFD_Speed_Cmd_RPM          : REAL; (* [rpm] CDU Inverter Pump 2 Speed Reference (0 - 3500 rpm) *)
    rPHE_Facility_Modulating_Valve_Cmd_Pct: REAL; (* [%] Primary Facility Chilled Water Equal-Pct Valve Position (0-100%) *)
    rPHE_Bypass_3Way_Valve_Cmd_Pct        : REAL; (* [%] Secondary TCS 3-Way Dynamic Temperature Mixing Valve (0-100%) *)
    bTCS_Fast_Isolation_Valve_Trip        : BOOL; (* Fast Catastrophic Leak Isolation Shutoff Solenoid Command (<100ms) *)
    bThermal_Buffer_Discharge_Valve_Cmd   : BOOL; (* Fast Pneumatic Actuator Command for Ride-Through Discharge Coupling *)
    bThermal_Buffer_Charging_Valve_Cmd    : BOOL; (* Motorized Recirculation Valve for Thermal Buffer Chilled Charging *)
    bChemical_Dosing_Pump_Cmd             : BOOL; (* Digital Dosing Pump Stroke Command for Corrosion Inhibitor Top-Up *)
    bDeaerator_Vacuum_Vent_Solenoid       : BOOL; (* Continuous Cyclonic Deaeration Vacuum Exhaust Solenoid Valve *)
    bAI_Cluster_Emergency_Thermal_Throttling_Req: BOOL; (* Fast Hardware Throttling Interlock Signal to Data Center BMS *)

    (* ========================================================================= *)
    (* SECTION 2: 2oo3 VOTED PROCESS VARIABLES                                   *)
    (* ========================================================================= *)
    rVoted_TCS_Supply_Flow_Lpm            : REAL; (* [L/min] Voted TCS Coolant Supply Flow Rate *)
    rVoted_TCS_Supply_Pressure_bar        : REAL; (* [bar] Voted TCS Supply Manifold Pressure *)
    rVoted_TCS_Return_Pressure_bar        : REAL; (* [bar] Voted TCS Return Manifold Pressure *)
    rVoted_TCS_Loop_Diff_Pressure_bar     : REAL; (* [bar] Voted TCS Manifold Differential Pressure (Target 1.80 bar) *)
    rVoted_TCS_Supply_Temp_C              : REAL; (* [deg C] Voted TCS Supply Coolant Temperature (Target 32.0 deg C) *)
    rVoted_TCS_Return_Temp_C              : REAL; (* [deg C] Voted TCS Return Coolant Temperature *)
    rVoted_FWS_Facility_Flow_m3h          : REAL; (* [m3/h] Voted Primary Facility Chilled Water Flow Rate *)
    rVoted_FWS_Facility_Supply_Temp_C     : REAL; (* [deg C] Voted Facility Chilled Water Supply Temperature *)
    rVoted_FWR_Facility_Return_Temp_C     : REAL; (* [deg C] Voted Facility Chilled Water Return Temperature *)
    rVoted_Glycol_Concentration_Pct       : REAL; (* [%] Voted Coolant Propylene Glycol Concentration (PG25 nominal) *)
    rVoted_Dissolved_Oxygen_ppb           : REAL; (* [ppb] Voted Coolant Dissolved Oxygen Level (<20 ppb) *)
    rVoted_Leak_Rope_Resistance_Ohm       : REAL; (* [Ohm] Voted Floor Distributed Leak Rope Impedance *)
    rVoted_Buffer_Tank_Level_Pct          : REAL; (* [%] Voted Thermal Ride-Through Reservoir Coolant Level *)

    (* ========================================================================= *)
    (* SECTION 3: CYBER-PHYSICAL OBSERVERS, ENERGETICS & RELIABILITY KPIS        *)
    (* ========================================================================= *)
    rPHE_Thermal_Duty_MW                  : REAL; (* [MW] Heat Exchanger Instantaneous Transferred Thermal Duty *)
    rPHE_Overall_Heat_Transfer_UA_kW_K    : REAL; (* [kW/K] Dynamic Overall Heat Transfer Conductance UA *)
    rPHE_Fouling_Resistance_m2K_kW        : REAL; (* [m2*K/kW] Estimated Plate Micro-Fouling Resistance Factor *)
    rObserved_GPU_Junction_Temp_C         : REAL; (* [deg C] Real-Time Predicted Peak AI Chip Silicon Junction Temp *)
    rObserved_ColdPlate_Rth_K_per_W       : REAL; (* [K/W] Dynamic Micro-Channel Cold Plate Convective Thermal Resistance *)
    rThermal_Buffer_RideThrough_Sec_Remaining: REAL; (* [s] Dynamic Thermal Buffer Autonomy Seconds at Present MW Load *)
    rFluid_Density_kg_m3                  : REAL; (* [kg/m3] Evaluated PG25 Coolant Density *)
    rFluid_Specific_Heat_J_kgK            : REAL; (* [J/(kg*K)] Evaluated PG25 Coolant Specific Heat Capacity *)
    rFluid_Viscosity_cP                   : REAL; (* [cP] Evaluated PG25 Coolant Dynamic Viscosity *)
    rFluid_Thermal_Conductivity_W_mK      : REAL; (* [W/(m*K)] Evaluated PG25 Coolant Thermal Conductivity *)
    rLeak_Zone_Estimated_Distance_m       : REAL; (* [m] Estimated Distance to Liquid Breach from Optical/TDR Reflector *)
    rTotal_CDU_Pumping_Electric_Power_kW  : REAL; (* [kW] Total Electrical Input Power to Both VFD Inverter Pumps *)
    rEnergy_Pumping_Efficiency_COP        : REAL; (* Dynamic Coefficient of Performance (Thermal kW / Electric kW) *)

    (* ========================================================================= *)
    (* SECTION 4: FINITE STATE MACHINE & ISA-18.2 DIAGNOSTIC WORDS               *)
    (* ========================================================================= *)
    wCDU_FSM_Current_State                : WORD; (* Current Operational Finite State Machine State Code (0..11) *)
    wCDU_FSM_Previous_State               : WORD; (* Previous State Code for Bump-Free State Transitions *)
    dwISA_Alarm_Word_1_Critical           : DWORD; (* ISA-18.2 Priority 1 Catastrophic & Safety Alarms *)
    dwISA_Alarm_Word_2_Warning            : DWORD; (* ISA-18.2 Priority 2 Warning & Operating Alarms *)
    dwTMR_Discrepancy_Word                : DWORD; (* 2oo3 Sensor Voting Channel Fault & Discrepancy Bitmask *)
    wAutomationStatusWord                 : WORD; (* Global Automation & Permissive Bitfield *)
END_VAR
"""

def get_var_internal():
    return """VAR
    (* ========================================================================= *)
    (* DISCRETE 8x8 STATE-SPACE MATRICES & VECTORS (Ts = 50 ms)                  *)
    (* States x:                                                                 *)
    (*   x[1]: TCS Supply Temperature Deviation [deg C] (Target: 32.0 C)         *)
    (*   x[2]: TCS Return Temperature Deviation [deg C] (Target: 44.0 C)         *)
    (*   x[3]: TCS Manifold Differential Pressure Deviation [bar] (Target: 1.80) *)
    (*   x[4]: TCS Volumetric Flow Deviation [L/min] (Target: 4000.0 L/min)      *)
    (*   x[5]: PHE Titanium Plate Core Temperature [deg C]                       *)
    (*   x[6]: Primary Facility Return Temperature Deviation [deg C]             *)
    (*   x[7]: Lead Pump Impeller Fluid Dynamic Angular Momentum [rad/s]         *)
    (*   x[8]: Thermal Storage Stratified Buffer Core Temperature [deg C]        *)
    (* Controls u:                                                               *)
    (*   u[1]: Lead Pump VFD Speed Cmd [rpm] (0 - 3500)                          *)
    (*   u[2]: Lag Pump VFD Speed Cmd [rpm] (0 - 3500)                           *)
    (*   u[3]: Facility PHE Modulating Valve [0 - 100%]                          *)
    (*   u[4]: Secondary TCS 3-Way Bypass Valve [0 - 100%]                       *)
    (* Disturbances w:                                                           *)
    (*   w[1]: AI Cluster Total Power Surge [MW] (0 - 45 MW)                     *)
    (*   w[2]: Facility Supply Water Temperature Disturbance [deg C]             *)
    (* ========================================================================= *)
    mA_Matrix                             : ARRAY[1..8, 1..8] OF REAL;
    mB_Matrix                             : ARRAY[1..8, 1..4] OF REAL;
    mBw_Matrix                            : ARRAY[1..8, 1..2] OF REAL;
    mC_Matrix                             : ARRAY[1..4, 1..8] OF REAL;
    mD_Matrix                             : ARRAY[1..4, 1..4] OF REAL;

    aState_x                              : ARRAY[1..8] OF REAL;
    aState_x_next                         : ARRAY[1..8] OF REAL;
    aState_x_hat                          : ARRAY[1..8] OF REAL;
    aState_x_err                          : ARRAY[1..8] OF REAL;
    aControl_u                            : ARRAY[1..4] OF REAL;
    aControl_u_opt                        : ARRAY[1..4] OF REAL;
    aControl_u_prev                       : ARRAY[1..4] OF REAL;
    aDisturb_w                            : ARRAY[1..2] OF REAL;
    aOutput_y                             : ARRAY[1..4] OF REAL;
    aOutput_y_sp                          : ARRAY[1..4] OF REAL;

    (* ========================================================================= *)
    (* RECEDING-HORIZON MPC COST MATRICES & OPTIMIZER WORK REGISTERS             *)
    (* ========================================================================= *)
    mQ_cost                               : ARRAY[1..8, 1..8] OF REAL; (* State tracking error penalty matrix *)
    mR_cost                               : ARRAY[1..4, 1..4] OF REAL; (* Actuator control effort penalty matrix *)
    mP_term                               : ARRAY[1..8, 1..8] OF REAL; (* Discrete algebraic Riccati terminal cost matrix *)
    mH_hessian                            : ARRAY[1..4, 1..4] OF REAL; (* Hessian matrix approximation *)
    aGrad_g                               : ARRAY[1..4] OF REAL;       (* Quadratic gradient vector *)
    aDelta_u                              : ARRAY[1..4] OF REAL;       (* Control step gradient update *)

    (* ========================================================================= *)
    (* 2oo3 TMR VOTING INTERMEDIATES, DELTAS, TIMERS & HEALTH MASKS              *)
    (* ========================================================================= *)
    (* 1. TCS Supply Flow *)
    rDiff_Flow_AB                         : REAL;
    rDiff_Flow_BC                         : REAL;
    rDiff_Flow_AC                         : REAL;
    tTMR_Timer_Flow                       : REAL;
    bFlow_ChA_Healthy                     : BOOL;
    bFlow_ChB_Healthy                     : BOOL;
    bFlow_ChC_Healthy                     : BOOL;

    (* 2. TCS Supply Pressure *)
    rDiff_SupplyP_AB                      : REAL;
    rDiff_SupplyP_BC                      : REAL;
    rDiff_SupplyP_AC                      : REAL;
    tTMR_Timer_SupplyP                    : REAL;
    bSupplyP_ChA_Healthy                  : BOOL;
    bSupplyP_ChB_Healthy                  : BOOL;
    bSupplyP_ChC_Healthy                  : BOOL;

    (* 3. TCS Return Pressure *)
    rDiff_ReturnP_AB                      : REAL;
    rDiff_ReturnP_BC                      : REAL;
    rDiff_ReturnP_AC                      : REAL;
    tTMR_Timer_ReturnP                    : REAL;
    bReturnP_ChA_Healthy                  : BOOL;
    bReturnP_ChB_Healthy                  : BOOL;
    bReturnP_ChC_Healthy                  : BOOL;

    (* 4. TCS Differential Pressure *)
    rDiff_DP_AB                           : REAL;
    rDiff_DP_BC                           : REAL;
    rDiff_DP_AC                           : REAL;
    tTMR_Timer_DP                         : REAL;
    bDP_ChA_Healthy                       : BOOL;
    bDP_ChB_Healthy                       : BOOL;
    bDP_ChC_Healthy                       : BOOL;

    (* 5. TCS Supply Temperature *)
    rDiff_SupplyT_AB                      : REAL;
    rDiff_SupplyT_BC                      : REAL;
    rDiff_SupplyT_AC                      : REAL;
    tTMR_Timer_SupplyT                    : REAL;
    bSupplyT_ChA_Healthy                  : BOOL;
    bSupplyT_ChB_Healthy                  : BOOL;
    bSupplyT_ChC_Healthy                  : BOOL;

    (* 6. TCS Return Temperature *)
    rDiff_ReturnT_AB                      : REAL;
    rDiff_ReturnT_BC                      : REAL;
    rDiff_ReturnT_AC                      : REAL;
    tTMR_Timer_ReturnT                    : REAL;
    bReturnT_ChA_Healthy                  : BOOL;
    bReturnT_ChB_Healthy                  : BOOL;
    bReturnT_ChC_Healthy                  : BOOL;

    (* 7. Facility Water Flow *)
    rDiff_FacFlow_AB                      : REAL;
    rDiff_FacFlow_BC                      : REAL;
    rDiff_FacFlow_AC                      : REAL;
    tTMR_Timer_FacFlow                    : REAL;
    bFacFlow_ChA_Healthy                  : BOOL;
    bFacFlow_ChB_Healthy                  : BOOL;
    bFacFlow_ChC_Healthy                  : BOOL;

    (* 8. Facility Supply Temperature *)
    rDiff_FacSupplyT_AB                   : REAL;
    rDiff_FacSupplyT_BC                   : REAL;
    rDiff_FacSupplyT_AC                   : REAL;
    tTMR_Timer_FacSupplyT                 : REAL;
    bFacSupplyT_ChA_Healthy               : BOOL;
    bFacSupplyT_ChB_Healthy               : BOOL;
    bFacSupplyT_ChC_Healthy               : BOOL;

    (* 9. Facility Return Temperature *)
    rDiff_FacReturnT_AB                   : REAL;
    rDiff_FacReturnT_BC                   : REAL;
    rDiff_FacReturnT_AC                   : REAL;
    tTMR_Timer_FacReturnT                 : REAL;
    bFacReturnT_ChA_Healthy               : BOOL;
    bFacReturnT_ChB_Healthy               : BOOL;
    bFacReturnT_ChC_Healthy               : BOOL;

    (* 10. Pump 1 RPM Feedback *)
    rDiff_Pump1RPM_AB                     : REAL;
    rDiff_Pump1RPM_BC                     : REAL;
    rDiff_Pump1RPM_AC                     : REAL;
    tTMR_Timer_Pump1RPM                   : REAL;
    bPump1RPM_ChA_Healthy                 : BOOL;
    bPump1RPM_ChB_Healthy                 : BOOL;
    bPump1RPM_ChC_Healthy                 : BOOL;

    (* 11. Pump 2 RPM Feedback *)
    rDiff_Pump2RPM_AB                     : REAL;
    rDiff_Pump2RPM_BC                     : REAL;
    rDiff_Pump2RPM_AC                     : REAL;
    tTMR_Timer_Pump2RPM                   : REAL;
    bPump2RPM_ChA_Healthy                 : BOOL;
    bPump2RPM_ChB_Healthy                 : BOOL;
    bPump2RPM_ChC_Healthy                 : BOOL;

    (* 12. PHE Valve Position Feedback *)
    rDiff_PHEValve_AB                     : REAL;
    rDiff_PHEValve_BC                     : REAL;
    rDiff_PHEValve_AC                     : REAL;
    tTMR_Timer_PHEValve                   : REAL;
    bPHEValve_ChA_Healthy                 : BOOL;
    bPHEValve_ChB_Healthy                 : BOOL;
    bPHEValve_ChC_Healthy                 : BOOL;

    (* 13. Glycol Concentration *)
    rDiff_Glycol_AB                       : REAL;
    rDiff_Glycol_BC                       : REAL;
    rDiff_Glycol_AC                       : REAL;
    tTMR_Timer_Glycol                     : REAL;
    bGlycol_ChA_Healthy                   : BOOL;
    bGlycol_ChB_Healthy                   : BOOL;
    bGlycol_ChC_Healthy                   : BOOL;

    (* 14. Dissolved Oxygen *)
    rDiff_DO_AB                           : REAL;
    rDiff_DO_BC                           : REAL;
    rDiff_DO_AC                           : REAL;
    tTMR_Timer_DO                         : REAL;
    bDO_ChA_Healthy                       : BOOL;
    bDO_ChB_Healthy                       : BOOL;
    bDO_ChC_Healthy                       : BOOL;

    (* 15. Leak Rope Resistance *)
    rDiff_Leak_AB                         : REAL;
    rDiff_Leak_BC                         : REAL;
    rDiff_Leak_AC                         : REAL;
    tTMR_Timer_Leak                       : REAL;
    bLeak_ChA_Healthy                     : BOOL;
    bLeak_ChB_Healthy                     : BOOL;
    bLeak_ChC_Healthy                     : BOOL;

    (* 16. Buffer Tank Level *)
    rDiff_BufferLvl_AB                    : REAL;
    rDiff_BufferLvl_BC                    : REAL;
    rDiff_BufferLvl_AC                    : REAL;
    tTMR_Timer_BufferLvl                  : REAL;
    bBufferLvl_ChA_Healthy                : BOOL;
    bBufferLvl_ChB_Healthy                : BOOL;
    bBufferLvl_ChC_Healthy                : BOOL;

    (* ========================================================================= *)
    (* THERMO-PHYSICAL MODELING & CYBER-PHYSICAL OBSERVER INTERNAL REGISTERS     *)
    (* ========================================================================= *)
    (* PG25 Polynomial constants *)
    rPG_Poly_A0                           : REAL;
    rPG_Poly_A1                           : REAL;
    rPG_Poly_A2                           : REAL;
    rPG_Poly_A3                           : REAL;
    rPG_Poly_B0                           : REAL;
    rPG_Poly_B1                           : REAL;
    rPG_Poly_B2                           : REAL;
    rPG_Poly_C0                           : REAL;
    rPG_Poly_C1                           : REAL;
    rPG_Poly_C2                           : REAL;
    rPG_Poly_D0                           : REAL;
    rPG_Poly_D1                           : REAL;

    (* Heat Exchanger Log Mean Temp Difference & UA *)
    rLMTD_DeltaT1                         : REAL;
    rLMTD_DeltaT2                         : REAL;
    rLMTD_Calculated                      : REAL;
    rPHE_MassFlow_Primary_kg_s            : REAL;
    rPHE_MassFlow_Secondary_kg_s          : REAL;
    rPHE_Clean_Conductance_UA             : REAL;

    (* Direct-to-Chip Cold Plate Hydraulics & Thermal Resistance *)
    rRack_Coolant_Velocity_m_s            : REAL;
    rMicroChannel_Hydraulic_Diameter_m    : REAL;
    rMicroChannel_Reynolds_Number         : REAL;
    rMicroChannel_Prandtl_Number          : REAL;
    rMicroChannel_Nusselt_Number          : REAL;
    rConvective_Heat_Transfer_Coeff_h     : REAL;
    rColdPlate_Conduction_Resistance_K_W  : REAL;
    rColdPlate_Convective_Resistance_K_W  : REAL;
    rFluid_Caloric_Temperature_Rise_K     : REAL;

    (* Leak Localization Acoustic/TDR Wave Parameters *)
    rLeak_Loop_Characteristic_Impedance   : REAL;
    rLeak_Signal_Propagation_Velocity_m_us: REAL;
    rLeak_Measured_Reflectance_Ratio      : REAL;

    (* Thermal Storage Reservoir Energy Tracking *)
    rBuffer_Total_Fluid_Mass_kg           : REAL;
    rBuffer_Stored_Thermal_Capacity_MJ    : REAL;
    rBuffer_Available_Enthalpy_Delta_MJ   : REAL;

    (* ========================================================================= *)
    (* ISA-18.2 ALARM ENGINE REGISTERS & RATE-OF-CHANGE TRACKING                 *)
    (* ========================================================================= *)
    rPrev_Voted_DP                        : REAL;
    rPrev_Voted_SupplyTemp                : REAL;
    rPrev_Voted_Flow                      : REAL;
    rPrev_Voted_LeakResistance            : REAL;
    rROC_DP_bar_per_s                     : REAL;
    rROC_SupplyTemp_degC_per_s            : REAL;
    rROC_LeakResistance_Ohm_per_s         : REAL;

    rDP_Deadband_High                     : REAL;
    rDP_Deadband_Low                      : REAL;
    rSupplyTemp_Deadband_High             : REAL;
    rSupplyTemp_Deadband_Low              : REAL;

    (* Fast trip debounce counters *)
    tLeak_Trip_Debounce_Time              : REAL;
    tCavitation_Debounce_Time             : REAL;
    bLeak_Fast_Trip_Latched               : BOOL;
    bCavitation_Trip_Latched              : BOOL;

    (* ========================================================================= *)
    (* MULTI-STAGE FINITE STATE MACHINE INTERNAL COUNTERS & RUNTIME LOGS         *)
    (* ========================================================================= *)
    nFSM_State                            : INT;
    nFSM_NextState                        : INT;
    nFSM_PreviousState                    : INT;
    tState_Dwell_Timer_Sec                : REAL;
    tDeaeration_Cycle_Sec                 : REAL;
    tChemical_Dosing_Pulse_Sec            : REAL;
    rPump1_RunHours                       : REAL;
    rPump2_RunHours                       : REAL;
    bLeadPump_Active                      : INT; (* 1=Pump 1 Lead, 2=Pump 2 Lead *)
    bFailover_In_Progress                 : BOOL;
    tFailover_Ramp_Timer_Sec              : REAL;
    rRamp_Rate_RPM_per_Sec                : REAL;
    rTarget_Lead_RPM                      : REAL;
    rTarget_Lag_RPM                       : REAL;
    rTarget_Valve_Pct                     : REAL;
    rTarget_Bypass_Pct                    : REAL;

    (* General loop counters *)
    iIndex_i                              : INT;
    iIndex_j                              : INT;
    iIndex_k                              : INT;
    bMatrices_Initialized                 : BOOL;
END_VAR
"""

print("Declarations module configured.")
