# Comprehensive builder for FB_Chemical_CryoASU_DoubleColumn_AntiSurge
import json, uuid, re, os, sys

def get_header_and_vars():
    return """FUNCTION_BLOCK FB_Chemical_CryoASU_DoubleColumn_AntiSurge
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * V7 PERSONA                  : 75+ Years Principal Automation Fellow & Cyber-Physical Systems Chair
 * COMMERCIAL INDUSTRIAL SECTOR: Heavy Industrial Gases & Cryogenic Air Separation
 * SYSTEM                      : World-Scale 5,000 MTD Cryogenic Air Separation Unit (ASU)
 * CORE INTEGRATED SUBSYSTEMS  :
 *   1. Medium Pressure Column (HP / MP Column: 6.0 bar at -175.2 deg C, 72 Sieve Trays)
 *   2. Low Pressure Column (LP Column: 1.4 bar at -194.1 deg C, 110 Structured Packing Stages)
 *   3. Main Condenser-Reboiler Core Bath with Thermosiphon Two-Phase Boiling Loop
 *   4. Hydrocarbon & Acetylene (C2H2 < 0.10 ppm) Accumulation Anti-Detonation Continuous Purge Control
 *   5. 45 MW Centrifugal Main Air Compressor (MAC) 4-Stage High-Speed Dynamic Anti-Surge & Decoupled IGV
 *   6. Crude Argon Rectification Column Side-Draw Ratio Dynamic Decoupling & N2 Breakthrough Prevention
 *   7. High-Speed 85,000 RPM Cryogenic Turbo-Expander Active Magnetic Bearings & Joule-Thomson Balancing
 *   8. 8x8 Multivariable Discrete State-Space Model at 20 ms Cycle Time (x[k+1] = A*x[k] + B*u[k])
 *   9. Receding-Horizon Model Predictive Control (MPC) with 3-Iteration Projected Gradient Descent (PGD)
 *  10. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting across 16 Process Transmitter Triplets (48 Ch)
 *  11. ISA-18.2 5-Tier Process Alarm Hierarchy (HI_HI, HI, LO, LO_LO, ROC) & Bit-Packed Diagnostics
 *  12. 12-Stage Deterministic Plant Operational Finite State Machine (FSM)
 * =====================================================================================================================
 * DETAILED CYBER-PHYSICAL PROCESS THERMODYNAMICS & ENGINEERING THEORY:
 *
 * 1. Double-Column Air Rectification Thermodynamics:
 *    Atmospheric ambient air is compressed to 6.2 bar by the 45 MW Main Air Compressor (MAC), precooled by chilling
 *    water, and purified through twin-bed 13X molecular sieve adsorbers (PPU) removing water vapor (< 0.1 ppm) and
 *    CO2 (< 0.1 ppm) to prevent cryogenic dry ice and hydrate blockages in downstream brazed aluminum plate-fin heat
 *    exchangers (BAHX). Clean air enters the bottom of the Medium Pressure (HP) column at -172 deg C.
 *    The HP column operates at 5.8 to 6.2 bar, separating air into pure gaseous nitrogen (GAN) top distillate (99.999% N2)
 *    and oxygen-enriched 'kettle liquid' bottom bottoms (36-40% O2).
 *    Pure nitrogen vapor from the HP column top is routed to the condensing pass of the Main Condenser-Reboiler,
 *    where it condenses at -176.5 deg C (6.0 bar) against boiling liquid oxygen (LOX) in the LP column bottom boiling
 *    at -183.0 deg C (1.4 bar). The temperature driving force delta-T across the reboiler core is strictly maintained
 *    between 1.4 K and 1.8 K to guarantee vigorous thermosiphon two-phase circulation without film-boiling dry-out.
 *
 * 2. Acetylene & Hydrocarbon Precipitation Detonation Hazard:
 *    Atmospheric air contains trace hydrocarbons (methane, ethane, ethylene, acetylene, propane, butane). While lighter
 *    alkanes possess high solubility in LOX, acetylene (C2H2) exhibits a critical solubility limit of only ~5.0 ppm in LOX
 *    at -183 deg C. Because acetylene has a boiling point of -84 deg C, it is practically non-volatile at -183 deg C and
 *    remains completely partitioned in the liquid phase as liquid oxygen continuously vaporizes into pure GOX product.
 *    Without continuous liquid purging, acetylene concentrates monotonically. Once the local concentration exceeds 5 ppm,
 *    microscopic solid acetylene crystals precipitate out of solution onto reboiler boiling surfaces. Solid acetylene in
 *    the presence of pure liquid oxygen is an explosive contact primary capable of violent detonation triggered by static
 *    electricity, thermal shock, or mechanical vibration. Under international safety standards (EIGA / CGA), acetylene
 *    concentration in the reboiler bath must be maintained below 0.10 ppm, with an alarm threshold at 0.05 ppm, and an
 *    emergency automatic LOX bath dump initiated if concentration exceeds 0.20 ppm.
 *
 * 3. 45 MW Centrifugal Main Air Compressor Dynamic Anti-Surge Control:
 *    The compressor operates in non-dimensional coordinates (reduced head Psi vs reduced flow Phi). Surge occurs when
 *    aerodynamic stall induces massive flow reversal, cyclic pressure oscillation, and destructive shaft deflection.
 *    The Surge Limit Line (SLL) is characterized by: Delta_P_mac = K_sll * Delta_P_venturi.
 *    The controller calculates an instantaneous surge safety margin:
 *        SurgeMargin = [(Delta_P_venturi / Delta_P_mac) - (Delta_P_venturi_sll / Delta_P_mac)] / (Delta_P_venturi / Delta_P_mac)
 *    A minimum 12.0% safety margin is enforced by modulating the high-speed pneumatic anti-surge recycle valve (< 200 ms
 *    full-stroke latency) and decoupling inlet guide vanes (IGV) via an aerodynamic feedforward decoupling gain matrix.
 *
 * 4. Crude Argon Rectification Column Side-Draw Dynamic Ratio Optimization:
 *    Argon (boiling point -185.8 deg C) possesses a volatility intermediate between nitrogen (-195.8 deg C) and oxygen
 *    (-183.0 deg C). Inside the LP column, an 'argon belly' develops with peak argon concentration (9.0 to 12.5% Ar,
 *    balance O2, < 0.05% N2) located approximately 30 to 35 trays above the reboiler. Vapor is drawn off and directed to
 *    the Crude Argon Column. Precise ratio control of the side-draw rate relative to MAC feed air is imperative:
 *    drawing too rapidly pulls nitrogen down into the draw, poisoning the argon condenser and causing total argon column
 *    collapse; drawing too slowly dumps argon into the pure GOX product, degrading oxygen purity below commercial 99.6%.
 *
 * 5. High-Speed Turbo-Expander (85,000 RPM) Active Magnetic Bearing Control:
 *    Refrigeration for cold-box liquefaction is produced by isentropic gas expansion across an ultra-high-speed radial
 *    inflow turbine rotating at 85,000 RPM supported by 5-axis active magnetic bearings (AMB). Isentropic expansion
 *    efficiency eta_isen = (T_in - T_out) / [T_in * (1 - (P_out/P_in)^((gamma-1)/gamma))].
 *    Shaft speed is controlled by an aerodynamic brake compressor and variable inlet guide nozzles (VIGV).
 * =====================================================================================================================
 *)
VAR_INPUT
    (* --- Master Plant Automation Supervisory Permissives & Pushbuttons --- *)
    bEnable                             : BOOL := FALSE;    (* Master Plant Automation Execution Permissive [BOOL] *)
    bResetFault                         : BOOL := FALSE;    (* Operator Fault Acknowledge / Reset Pushbutton [BOOL] *)
    bEmergencyStop_NC                   : BOOL := TRUE;     (* Dual-Channel Hardwired Safety Instrumented System Loop (Active Low) [BOOL] *)
    bAutoMode                           : BOOL := TRUE;     (* 1=Full Closed-Loop MPC Automation, 0=Manual Engineering Mode [BOOL] *)
    bAcknowledgeAlarms                  : BOOL := FALSE;    (* ISA-18.2 Process Alarm Silence / Acknowledge Strobe [BOOL] *)
    bColdBoxWarmPurgePermissive         : BOOL := TRUE;     (* Ambient Dry Nitrogen Warm Purge Permissive Confirmed [BOOL] *)
    bMolSieveDryingPermissive           : BOOL := TRUE;     (* Molecular Sieve Adsorber Regeneration & Dewpoint Confirmed [BOOL] *)
    bCompressorStartPermissive          : BOOL := TRUE;     (* 45 MW MAC Auxiliary Lube Oil, Cooling Water & Seal Permissives [BOOL] *)
    bExpanderStartPermissive            : BOOL := TRUE;     (* Cryo Turbo-Expander Magnetic Bearing Levitation & Seal Gas OK [BOOL] *)
    bArgonDrawPermissive                : BOOL := TRUE;     (* Crude Argon Rectification Column Ready Permissive [BOOL] *)
    bEmergencyDepressCommand            : BOOL := FALSE;    (* Operator Manual Cold-Box Fast Depressurization Trip [BOOL] *)

    (* --- Process Operational Target Setpoints --- *)
    rTarget_MAC_DischargePress_bar      : REAL := 6.20;     (* MAC 4th Stage Final Discharge Pressure Setpoint [bar] *)
    rTarget_MAC_InletAirFlow_m3h        : REAL := 185000.0; (* MAC Suction Volumetric Air Flow Rate Setpoint [m3/h] *)
    rTarget_HP_ColumnPress_bar          : REAL := 5.95;     (* Medium/High Pressure Column Top Operating Pressure [bar] *)
    rTarget_LP_ColumnPress_bar          : REAL := 1.42;     (* Low Pressure Column Top Operating Pressure [bar] *)
    rTarget_CondenserTemp_degC          : REAL := -181.8;   (* Main Condenser-Reboiler Bath Equilibrium Temperature [deg C] *)
    rTarget_LOX_Level_pct               : REAL := 65.0;     (* Main Reboiler Liquid Oxygen Bath Level Setpoint [%] *)
    rTarget_ArgonPurity_O2_pct          : REAL := 1.50;     (* Crude Argon Overhead Product Residual Oxygen Target [%] *)
    rTarget_AntiSurgeMargin_pct         : REAL := 12.0;     (* Minimum Permissible Aerodynamic Surge Margin Safety Bias [%] *)
    rTarget_ExpanderSpeed_RPM           : REAL := 82500.0;  (* High-Speed Cryogenic Turbo-Expander Target Speed [RPM] *)
    rTarget_GOX_Flow_Nm3h               : REAL := 65000.0;  (* High-Purity Gaseous Oxygen Pipeline Delivery Flow Setpoint [Nm3/h] *)
    rTarget_GAN_Flow_Nm3h               : REAL := 125000.0; (* Gaseous Pure Nitrogen Pipeline Delivery Flow Setpoint [Nm3/h] *)
    rMaxSafeAcetylene_ppm               : REAL := 0.050;    (* Critical Acetylene Safety Alert Concentration Limit [ppm] *)
    rCycleTime_s                        : REAL := 0.020;    (* Deterministic PLC Execution Task Period (20 ms) [s] *)

    (* ==================================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) ANALYTICAL & PHYSICAL INSTRUMENTATION INPUTS                     *)
    (* ==================================================================================================== *)
    (* Channel 1: PT_MAC_DISCHARGE_101 [bar] - Main Air Compressor Discharge Pressure *)
    PT_MAC_DISCHARGE_101A               : REAL := 6.21;     (* MAC Discharge Pressure Channel A [bar] *)
    PT_MAC_DISCHARGE_101B               : REAL := 6.19;     (* MAC Discharge Pressure Channel B [bar] *)
    PT_MAC_DISCHARGE_101C               : REAL := 6.20;     (* MAC Discharge Pressure Channel C [bar] *)

    (* Channel 2: FT_MAC_INLET_AIR_102 [m3/h] - Main Air Compressor Suction Volumetric Flow *)
    FT_MAC_INLET_AIR_102A               : REAL := 185120.0; (* MAC Suction Flow Channel A [m3/h] *)
    FT_MAC_INLET_AIR_102B               : REAL := 184950.0; (* MAC Suction Flow Channel B [m3/h] *)
    FT_MAC_INLET_AIR_102C               : REAL := 185040.0; (* MAC Suction Flow Channel C [m3/h] *)

    (* Channel 3: PT_HP_COLUMN_TOP_201 [bar] - Medium Pressure Column Overhead Vapor Pressure *)
    PT_HP_COLUMN_TOP_201A               : REAL := 5.96;     (* HP Column Top Pressure Channel A [bar] *)
    PT_HP_COLUMN_TOP_201B               : REAL := 5.94;     (* HP Column Top Pressure Channel B [bar] *)
    PT_HP_COLUMN_TOP_201C               : REAL := 5.95;     (* HP Column Top Pressure Channel C [bar] *)

    (* Channel 4: PT_LP_COLUMN_TOP_202 [bar] - Low Pressure Column Overhead Waste Nitrogen Pressure *)
    PT_LP_COLUMN_TOP_202A               : REAL := 1.42;     (* LP Column Top Pressure Channel A [bar] *)
    PT_LP_COLUMN_TOP_202B               : REAL := 1.41;     (* LP Column Top Pressure Channel B [bar] *)
    PT_LP_COLUMN_TOP_202C               : REAL := 1.43;     (* LP Column Top Pressure Channel C [bar] *)

    (* Channel 5: TT_CONDENSER_BATH_301 [deg C] - Main Condenser-Reboiler Core Bath RTD *)
    TT_CONDENSER_BATH_301A              : REAL := -181.8;   (* Condenser Bath Temp Channel A [deg C] *)
    TT_CONDENSER_BATH_301B              : REAL := -181.7;   (* Condenser Bath Temp Channel B [deg C] *)
    TT_CONDENSER_BATH_301C              : REAL := -181.9;   (* Condenser Bath Temp Channel C [deg C] *)

    (* Channel 6: LT_REBOILER_LOX_LEVEL_302 [%] - Main Reboiler Liquid Oxygen Bath Level *)
    LT_REBOILER_LOX_LEVEL_302A          : REAL := 65.2;     (* Reboiler LOX Level Channel A [%] *)
    LT_REBOILER_LOX_LEVEL_302B          : REAL := 64.9;     (* Reboiler LOX Level Channel B [%] *)
    LT_REBOILER_LOX_LEVEL_302C          : REAL := 65.1;     (* Reboiler LOX Level Channel C [%] *)

    (* Channel 7: AIT_LOX_ACETYLENE_PPM_401 [ppm] - Reboiler LOX Hydrocarbon Acetylene Analyzer *)
    AIT_LOX_ACETYLENE_PPM_401A          : REAL := 0.024;    (* LOX Acetylene Analyzer Channel A [ppm] *)
    AIT_LOX_ACETYLENE_PPM_401B          : REAL := 0.025;    (* LOX Acetylene Analyzer Channel B [ppm] *)
    AIT_LOX_ACETYLENE_PPM_401C          : REAL := 0.023;    (* LOX Acetylene Analyzer Channel C [ppm] *)

    (* Channel 8: AIT_ARGON_PURITY_O2_402 [%] - Crude Argon Side-Draw Oxygen Content Analyzer *)
    AIT_ARGON_PURITY_O2_402A            : REAL := 1.52;     (* Crude Argon O2 Purity Channel A [%] *)
    AIT_ARGON_PURITY_O2_402B            : REAL := 1.48;     (* Crude Argon O2 Purity Channel B [%] *)
    AIT_ARGON_PURITY_O2_402C            : REAL := 1.50;     (* Crude Argon O2 Purity Channel C [%] *)

    (* Channel 9: ST_EXPANDER_RPM_501 [RPM] - Turbo-Expander Shaft Eddy-Current Speed Transducer *)
    ST_EXPANDER_RPM_501A                : REAL := 82510.0;  (* Expander Rotor Speed Channel A [RPM] *)
    ST_EXPANDER_RPM_501B                : REAL := 82480.0;  (* Expander Rotor Speed Channel B [RPM] *)
    ST_EXPANDER_RPM_501C                : REAL := 82500.0;  (* Expander Rotor Speed Channel C [RPM] *)

    (* Channel 10: ZT_EXPANDER_NOZZLE_POS_502 [%] - Expander Variable Inlet Guide Vanes Position *)
    ZT_EXPANDER_NOZZLE_POS_502A         : REAL := 54.8;     (* Expander Nozzle Position Feedback A [%] *)
    ZT_EXPANDER_NOZZLE_POS_502B         : REAL := 55.1;     (* Expander Nozzle Position Feedback B [%] *)
    ZT_EXPANDER_NOZZLE_POS_502C         : REAL := 55.0;     (* Expander Nozzle Position Feedback C [%] *)

    (* Channel 11: FT_GOX_PRODUCT_601 [Nm3/h] - Pure Gaseous Oxygen Product Coriolis Flow *)
    FT_GOX_PRODUCT_601A                 : REAL := 65050.0;  (* GOX Product Flow Channel A [Nm3/h] *)
    FT_GOX_PRODUCT_601B                 : REAL := 64970.0;  (* GOX Product Flow Channel B [Nm3/h] *)
    FT_GOX_PRODUCT_601C                 : REAL := 65010.0;  (* GOX Product Flow Channel C [Nm3/h] *)

    (* Channel 12: FT_GAN_PRODUCT_602 [Nm3/h] - Pure Gaseous Nitrogen Product Flow Meter *)
    FT_GAN_PRODUCT_602A                 : REAL := 125100.0; (* GAN Product Flow Channel A [Nm3/h] *)
    FT_GAN_PRODUCT_602B                 : REAL := 124920.0; (* GAN Product Flow Channel B [Nm3/h] *)
    FT_GAN_PRODUCT_602C                 : REAL := 125040.0; (* GAN Product Flow Channel C [Nm3/h] *)

    (* Channel 13: DP_MAC_INLET_VENTURI_103 [mbar] - MAC Inlet Venturi Differential Pressure *)
    DP_MAC_INLET_VENTURI_103A           : REAL := 48.5;     (* MAC Inlet Venturi DP Channel A [mbar] *)
    DP_MAC_INLET_VENTURI_103B           : REAL := 48.2;     (* MAC Inlet Venturi DP Channel B [mbar] *)
    DP_MAC_INLET_VENTURI_103C           : REAL := 48.4;     (* MAC Inlet Venturi DP Channel C [mbar] *)

    (* Channel 14: TT_MAC_DISCHARGE_104 [deg C] - MAC Final Discharge Temperature RTD *)
    TT_MAC_DISCHARGE_104A               : REAL := 92.4;     (* MAC Discharge Temp Channel A [deg C] *)
    TT_MAC_DISCHARGE_104B               : REAL := 92.8;     (* MAC Discharge Temp Channel B [deg C] *)
    TT_MAC_DISCHARGE_104C               : REAL := 92.5;     (* MAC Discharge Temp Channel C [deg C] *)

    (* Channel 15: LT_HP_SUMP_LEVEL_203 [%] - HP Column Bottom Rich Liquid Air Sump Level *)
    LT_HP_SUMP_LEVEL_203A               : REAL := 52.3;     (* HP Sump Level Channel A [%] *)
    LT_HP_SUMP_LEVEL_203B               : REAL := 51.9;     (* HP Sump Level Channel B [%] *)
    LT_HP_SUMP_LEVEL_203C               : REAL := 52.1;     (* HP Sump Level Channel C [%] *)

    (* Channel 16: AIT_TOTAL_HYDROCARBON_403 [ppm] - Total Hydrocarbon Flame Ionization Analyzer *)
    AIT_TOTAL_HYDROCARBON_403A          : REAL := 0.42;     (* Total Hydrocarbons Channel A [ppm] *)
    AIT_TOTAL_HYDROCARBON_403B          : REAL := 0.45;     (* Total Hydrocarbons Channel B [ppm] *)
    AIT_TOTAL_HYDROCARBON_403C          : REAL := 0.43;     (* Total Hydrocarbons Channel C [ppm] *)
END_VAR

VAR_OUTPUT
    (* --- Overall Cryogenic Plant Operational Indicators --- *)
    bReady                              : BOOL := FALSE;    (* Cryogenic ASU Automation System Ready Permissive [BOOL] *)
    bBusy                               : BOOL := FALSE;    (* ASU Plant Startup / Sequence Progression Active [BOOL] *)
    bUnitInSteadyState                  : BOOL := FALSE;    (* ASU Operating in Nominal Commercial Production Equilibrium [BOOL] *)
    bAntiSurgeActive                    : BOOL := FALSE;    (* MAC Dynamic Anti-Surge Control Action Actively Modulating [BOOL] *)
    bCompressorSurgeTrip                : BOOL := FALSE;    (* MAC Emergency Surge Protection Fast Recycle Trip Latched [BOOL] *)
    bHydrocarbonExplosionHazardTrip     : BOOL := FALSE;    (* Acetylene Over-Concentration Bath Dump Interlock Latched [BOOL] *)
    bEmergencyDepressActive             : BOOL := FALSE;    (* Cold-Box Fast Depressurization Emergency Sequence Active [BOOL] *)
    bDegradedSensorModeActive           : BOOL := FALSE;    (* Warning: 2oo3 Sensing Degraded to 1oo2 or 1oo1 Analytical Fallback [BOOL] *)
    bExpanderOverspeedTrip              : BOOL := FALSE;    (* Cryo Turbo-Expander Redline Overspeed Trip Latched (>95,000 RPM) [BOOL] *)
    nActiveFSM_State                    : INT := 1;         (* Operational Finite State Machine Active State [1..12] *)

    (* --- ISA-18.2 Diagnostic & Status Bit-Packed Words --- *)
    wDiagnosticWord01                   : WORD := 16#0000;  (* FSM Sequencer State, Sub-Step & Mode Flags [WORD] *)
    wDiagnosticWord02                   : WORD := 16#0000;  (* 2oo3 TMR Sensor Health, Discrepancy & Isolation Vector [WORD] *)
    wDiagnosticWord03                   : WORD := 16#0000;  (* ISA-18.2 Process Warning Alarms (HI / LO / ROC Alerts) [WORD] *)
    wDiagnosticWord04                   : WORD := 16#0000;  (* ISA-18.2 Critical Trips & SIS Redline Shutdown Bits [WORD] *)

    (* --- Primary Process Actuator Commands & Valve Positions --- *)
    rCmd_MAC_AntiSurgeValve_pct         : REAL := 0.0;      (* 45 MW MAC Fast Pneumatic Anti-Surge Recycle Valve Command [0..100 %] *)
    rCmd_MAC_IGV_Position_pct           : REAL := 0.0;      (* MAC Suction Variable Inlet Guide Vanes (IGV) Command [0..100 %] *)
    rCmd_Expander_Nozzle_pct            : REAL := 0.0;      (* Turbo-Expander Inlet Variable Guide Vanes Command [0..100 %] *)
    rCmd_Expander_BrakeBlower_pct       : REAL := 0.0;      (* Turbo-Expander Aerodynamic Brake Dissipation Valve [0..100 %] *)
    rCmd_LOX_ContinuousPurge_pct        : REAL := 0.0;      (* Main Reboiler Liquid Oxygen Continuous Purge Valve [0..100 %] *)
    bCmd_LOX_EmergencyDumpValve         : BOOL := FALSE;    (* Fail-Open Cryogenic Solenoid to Emergency LOX Vaporizer Trench [BOOL] *)
    rCmd_ArgonSideDrawValve_pct         : REAL := 0.0;      (* LP Column Crude Argon Vapor Side-Draw Modulation Valve [0..100 %] *)
    rCmd_RichLiquidAirFeedValve_pct     : REAL := 0.0;      (* HP Sump Rich Liquid Expansion Joule-Thomson Valve to LP Column [0..100 %] *)
    rCmd_PureLiquidN2RefluxValve_pct    : REAL := 0.0;      (* HP Top Pure Liquid Nitrogen Reflux Subcooled Expansion Valve [0..100 %] *)
    rCmd_GOX_DeliveryValve_pct          : REAL := 0.0;      (* Pipeline Gaseous Oxygen Product Backpressure Valve [0..100 %] *)
    rCmd_GAN_DeliveryValve_pct          : REAL := 0.0;      (* Pipeline Gaseous Pure Nitrogen Product Delivery Valve [0..100 %] *)
    bCmd_ColdBoxWarmPurgeVent           : BOOL := FALSE;    (* Cold-Box Insulation Casing Dry N2 Warm Purge Vent Solenoid [BOOL] *)
    bCmd_MolecularSieveSwitchover       : BOOL := FALSE;    (* Twin Molecular Sieve Adsorber Vessel Switchover Strobe [BOOL] *)
    bCmd_FastRecycleOpenTrip            : BOOL := FALSE;    (* Emergency MAC Full Recycle Blow-Off Solenoid Trip (< 200 ms) [BOOL] *)
    bCmd_CryoSubcoolerBypassValve       : BOOL := FALSE;    (* Plate-Fin Heat Exchanger Cryogenic Subcooler Bypass Valve [BOOL] *)

    (* --- Cyber-Physical 2oo3 Voted & Process Evaluated Quantities --- *)
    rVoted_MAC_DischargePress_bar       : REAL := 0.0;      (* 2oo3 Voted MAC Discharge Stagnation Pressure [bar] *)
    rVoted_MAC_Flow_m3h                 : REAL := 0.0;      (* 2oo3 Voted MAC Suction Volumetric Flow Rate [m3/h] *)
    rVoted_HP_Pressure_bar              : REAL := 0.0;      (* 2oo3 Voted Medium Pressure Column Overhead Pressure [bar] *)
    rVoted_LP_Pressure_bar              : REAL := 0.0;      (* 2oo3 Voted Low Pressure Column Overhead Pressure [bar] *)
    rVoted_CondenserTemp_degC           : REAL := 0.0;      (* 2oo3 Voted Main Condenser-Reboiler Core Bath Temp [deg C] *)
    rVoted_LOX_Level_pct                : REAL := 0.0;      (* 2oo3 Voted Reboiler Liquid Oxygen Bath Level [%] *)
    rVoted_Acetylene_ppm                : REAL := 0.0;      (* 2oo3 Voted LOX Reboiler Acetylene Impurity [ppm] *)
    rVoted_Argon_O2_pct                 : REAL := 0.0;      (* 2oo3 Voted Crude Argon Draw Residual Oxygen Content [%] *)
    rVoted_Expander_RPM                 : REAL := 0.0;      (* 2oo3 Voted Cryo Turbo-Expander Rotational Shaft Speed [RPM] *)
    rVoted_Expander_Nozzle_pct          : REAL := 0.0;      (* 2oo3 Voted Turbo-Expander Guide Vanes Feedback [%] *)
    rVoted_GOX_Flow_Nm3h                : REAL := 0.0;      (* 2oo3 Voted Gaseous Oxygen Product Delivery Flow [Nm3/h] *)
    rVoted_GAN_Flow_Nm3h                : REAL := 0.0;      (* 2oo3 Voted Gaseous Nitrogen Product Delivery Flow [Nm3/h] *)
    rVoted_MAC_VenturiDP_mbar           : REAL := 0.0;      (* 2oo3 Voted MAC Suction Venturi Differential Pressure [mbar] *)
    rVoted_MAC_DischargeTemp_degC       : REAL := 0.0;      (* 2oo3 Voted MAC Final Stage Discharge Temperature [deg C] *)
    rVoted_HP_SumpLevel_pct             : REAL := 0.0;      (* 2oo3 Voted HP Column Bottom Kettle Liquid Level [%] *)
    rVoted_TotalHydrocarbon_ppm         : REAL := 0.0;      (* 2oo3 Voted Reboiler Total Hydrocarbon Concentration [ppm] *)

    (* --- Advanced Cyber-Physical Thermomechanical Telemetry --- *)
    rCalculated_SurgeMargin_pct         : REAL := 0.0;      (* Real-Time Dynamic Distance to Aerodynamic Surge Line [%] *)
    rCalculated_SpecificPower_kWh_Nm3O2 : REAL := 0.0;      (* Specific Energy Consumption per Normal Cubic Meter O2 [kWh/Nm3] *)
    rCalculated_ExpanderEfficiency_pct  : REAL := 0.0;      (* Cryo Turbo-Expander Real-Time Isentropic Expansion Efficiency [%] *)
    rCalculated_LOX_EvaporationRate_kgh : REAL := 0.0;      (* Reboiler Core Natural Circulation LOX Boil-Off Mass Rate [kg/h] *)
    rCalculated_PengRobinson_K_N2       : REAL := 0.0;      (* Cryogenic Nitrogen Vapor-Liquid Equilibrium Ratio K_N2 [-] *)
    rCalculated_PengRobinson_K_Ar       : REAL := 0.0;      (* Cryogenic Argon Vapor-Liquid Equilibrium Ratio K_Ar [-] *)
    rCalculated_PengRobinson_K_O2       : REAL := 0.0;      (* Cryogenic Oxygen Vapor-Liquid Equilibrium Ratio K_O2 [-] *)
    rCalculated_ThermosiphonFlowRate_m3h: REAL := 0.0;      (* Two-Phase Natural Thermosiphon Recirculation Rate [m3/h] *)
    rCalculated_AcetyleneAccumulationRate_ppmh: REAL := 0.0;(* Modeled Rate of Change of Acetylene in Reboiler [ppm/h] *)
    rMPC_ObjectiveCost_J                : REAL := 0.0;      (* Receding-Horizon Optimal Quadratic Objective Cost J [REAL] *)
END_VAR

VAR
    (* --- Execution Scan Cycle & Time Integration Variables --- *)
    c_rTs                               : REAL := 0.020;    (* Deterministic Control Period 20.0 milliseconds [s] *)
    c_rPi                               : REAL := 3.141592653589793; (* Constant Pi *)
    c_rR_GasConstant                    : REAL := 8.314462; (* Universal Gas Constant R [J/(mol*K)] *)
    rStateTimer_s                       : REAL := 0.0;      (* Accumulated Active FSM State Dwell Timer [s] *)
    rTotalPlantUptime_s                 : REAL := 0.0;      (* Continuous Plant Run Clock [s] *)
    bFirstScan                          : BOOL := TRUE;     (* Block First Scan Cold Initialization Flag *)

    (* --- Pure Component Physical Constants & Cryogenic Parameters --- *)
    c_rMW_N2                            : REAL := 28.0134;  (* Molecular Weight of Molecular Nitrogen N2 [kg/kmol] *)
    c_rMW_Ar                            : REAL := 39.9480;  (* Molecular Weight of Argon Ar [kg/kmol] *)
    c_rMW_O2                            : REAL := 31.9988;  (* Molecular Weight of Molecular Oxygen O2 [kg/kmol] *)
    c_rMW_C2H2                          : REAL := 26.0380;  (* Molecular Weight of Acetylene C2H2 [kg/kmol] *)
    c_rTc_N2_K                          : REAL := 126.19;   (* Nitrogen Critical Temperature [K] *)
    c_rPc_N2_bar                        : REAL := 33.958;   (* Nitrogen Critical Pressure [bar] *)
    c_rOmega_N2                         : REAL := 0.0377;   (* Nitrogen Pitzer Acentric Factor omega [-] *)
    c_rTc_Ar_K                          : REAL := 150.86;   (* Argon Critical Temperature [K] *)
    c_rPc_Ar_bar                        : REAL := 48.980;   (* Argon Critical Pressure [bar] *)
    c_rOmega_Ar                         : REAL := -0.0020;  (* Argon Pitzer Acentric Factor omega [-] *)
    c_rTc_O2_K                          : REAL := 154.58;   (* Oxygen Critical Temperature [K] *)
    c_rPc_O2_bar                        : REAL := 50.430;   (* Oxygen Critical Pressure [bar] *)
    c_rOmega_O2                         : REAL := 0.0222;   (* Oxygen Pitzer Acentric Factor omega [-] *)
    c_rLatentHeatO2_kJ_kg               : REAL := 213.0;    (* Latent Heat of Vaporization of LOX at 1.4 bar [kJ/kg] *)
    c_rDensityLOX_kg_m3                 : REAL := 1141.0;   (* Density of Saturated Liquid Oxygen [kg/m3] *)
    c_rDensityLIN_kg_m3                 : REAL := 808.0;    (* Density of Saturated Liquid Nitrogen [kg/m3] *)

    (* --- 45 MW Centrifugal MAC Aerodynamic Compressor Constants --- *)
    c_rMAC_ImpellerDiameter_m           : REAL := 1.450;    (* 4th Stage Shrouded Impeller Diameter D_imp [m] *)
    c_rMAC_RatedSpeed_RPM               : REAL := 4250.0;   (* MAC Synchronous Electric Drive Shaft Speed [RPM] *)
    c_rMAC_SurgeSlope_Ksll              : REAL := 0.0485;   (* Surge Limit Line Aerodynamic Gradient K_sll [bar/mbar] *)
    c_rMAC_SurgeOffset_b0               : REAL := 0.350;    (* Surge Limit Line Aerodynamic Pressure Intercept [bar] *)
    c_rMAC_PolytropicEfficiency         : REAL := 0.865;    (* MAC Compressor Stage Polytropic Efficiency eta_poly *)
    c_rMAC_MotorPowerNominal_kW         : REAL := 45000.0;  (* 45 MW Synchronous High-Voltage Electric Motor Power [kW] *)

    (* --- Cryogenic Turbo-Expander (85,000 RPM) Dynamic Constants --- *)
    c_rExpander_RotorInertia_kg_m2      : REAL := 0.00425;  (* High-Speed Turbine Rotor Polar Mass Moment of Inertia [kg*m2] *)
    c_rExpander_MaxOverspeed_RPM        : REAL := 95000.0;  (* Hard Trip Redline Overspeed Threshold [RPM] *)
    c_rExpander_DesignEfficiency        : REAL := 0.885;    (* Peak Design Isentropic Expansion Efficiency [-] *)
    c_rExpander_NozzleFlowCoeff         : REAL := 125.0;    (* Variable Guide Vane Effective Flow Coefficient *)

    (* --- Main Condenser-Reboiler Core Geometry & Heat Transfer Parameters --- *)
    c_rReboiler_CoreArea_m2             : REAL := 18500.0;  (* Total Brazed Aluminum Plate-Fin Wetted Heat Exchange Area [m2] *)
    c_rReboiler_CoreHeight_m            : REAL := 4.20;     (* Active Fin Matrix Immersion Height [m] *)
    c_rReboiler_HeatTransferU_W_m2K     : REAL := 1450.0;   (* Overall Boiling Heat Transfer Coefficient U [W/(m2*K)] *)
    c_rReboiler_LOX_SumpVolume_m3       : REAL := 32.5;     (* Reboiler Bottom Sump Liquid Inventory Volume [m3] *)

    (* ==================================================================================================== *)
    (* 8x8 MULTIVARIABLE DISCRETE STATE-SPACE CYBER-PHYSICAL MODEL (Ts = 20 ms)                             *)
    (* x[k+1] = matA * x[k] + matB * u[k],  y[k] = matC * x[k] + matD * u[k]                                *)
    (* States x[1..8]:                                                                                      *)
    (*   x[1]: MAC Discharge Pressure Error Delta_P_mac [bar]                                               *)
    (*   x[2]: MAC Suction Volumetric Flow Error Delta_Q_mac [m3/h]                                         *)
    (*   x[3]: HP Column Top Pressure Error Delta_P_hp [bar]                                                *)
    (*   x[4]: LP Column Top Pressure Error Delta_P_lp [bar]                                                *)
    (*   x[5]: Main Reboiler LOX Level Error Delta_L_lox [%]                                                *)
    (*   x[6]: Reboiler LOX Acetylene Concentration Error Delta_C_c2h2 [ppm]                                *)
    (*   x[7]: Crude Argon Side-Draw Oxygen Content Error Delta_y_o2 [%]                                    *)
    (*   x[8]: Cryo Turbo-Expander Shaft Speed Error Delta_N_exp [RPM]                                      *)
    (* Control Inputs u[1..5]:                                                                              *)
    (*   u[1]: MAC Fast Anti-Surge Recycle Valve Delta_u_asv [%]                                            *)
    (*   u[2]: MAC Suction Inlet Guide Vanes (IGV) Delta_u_igv [%]                                          *)
    (*   u[3]: Turbo-Expander Inlet Variable Guide Vanes Delta_u_exp [%]                                    *)
    (*   u[4]: Main Reboiler Continuous LOX Purge Flow Delta_u_purge [%]                                    *)
    (*   u[5]: LP Column Crude Argon Side-Draw Flow Delta_u_ar [%]                                          *)
    (* ==================================================================================================== *)
    matA                                : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Matrix A *)
    matB                                : ARRAY[1..8, 1..5] OF REAL; (* Discrete Input Coupling Matrix B *)
    matC                                : ARRAY[1..8, 1..8] OF REAL; (* Discrete Output Measurement Matrix C *)
    matD                                : ARRAY[1..8, 1..5] OF REAL; (* Discrete Direct Feedthrough Matrix D *)
    vecX                                : ARRAY[1..8] OF REAL;      (* Current System State Vector x[k] *)
    vecX_next                           : ARRAY[1..8] OF REAL;      (* Projected System State Vector x[k+1] *)
    vecX_ref                            : ARRAY[1..8] OF REAL;      (* Equilibrium Reference Vector x_ref *)
    vecU                                : ARRAY[1..5] OF REAL;      (* Active Control Command Vector u[k] *)
    vecU_prev                           : ARRAY[1..5] OF REAL;      (* Prior Control Command Vector u[k-1] *)
    vecDeltaU                           : ARRAY[1..5] OF REAL;      (* Control Action Slew Vector Delta_u[k] *)
    vecY                                : ARRAY[1..8] OF REAL;      (* Synthetic Sensor Output Vector y[k] *)
    vecGradU                            : ARRAY[1..5] OF REAL;      (* Real-Time Quadratic Cost Gradient Vector dJ/du *)

    (* --- Model Predictive Control (MPC) Cost Weighting Matrices & Constraints --- *)
    arrQ_Weight                         : ARRAY[1..8] OF REAL;      (* State Deviation Penalty Diag(Q) *)
    arrR_Weight                         : ARRAY[1..5] OF REAL;      (* Control Magnitude Penalty Diag(R) *)
    arrS_Weight                         : ARRAY[1..5] OF REAL;      (* Actuator Slew Rate Penalty Diag(S) *)
    arrP_TerminalWeight                 : ARRAY[1..8] OF REAL;      (* Terminal Prediction State Penalty Diag(P) *)
    arrU_Min                            : ARRAY[1..5] OF REAL;      (* Actuator Lower Bounds u_min *)
    arrU_Max                            : ARRAY[1..5] OF REAL;      (* Actuator Upper Bounds u_max *)
    arrDeltaU_Max                       : ARRAY[1..5] OF REAL;      (* Actuator Slew Rate Bounds per 20 ms *)
    c_rPGD_StepSize                     : REAL := 0.00045;          (* Projected Gradient Descent Learning Rate *)

    (* ==================================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY TIMERS & CHANNEL ISOLATION FLAGS                    *)
    (* ==================================================================================================== *)
    c_rTol_Press_MAC_bar                : REAL := 0.120;    (* MAC Discharge Pressure Discrepancy Tolerance [bar] *)
    c_rTol_Flow_MAC_m3h                 : REAL := 3500.0;   (* MAC Inlet Volumetric Flow Tolerance [m3/h] *)
    c_rTol_Press_HP_bar                 : REAL := 0.080;    (* HP Column Top Pressure Discrepancy Tolerance [bar] *)
    c_rTol_Press_LP_bar                 : REAL := 0.035;    (* LP Column Top Pressure Discrepancy Tolerance [bar] *)
    c_rTol_Temp_Bath_degC               : REAL := 0.350;    (* Main Condenser Bath RTD Tolerance [deg C] *)
    c_rTol_Level_LOX_pct                : REAL := 1.800;    (* Reboiler LOX Level Discrepancy Tolerance [%] *)
    c_rTol_Acetylene_ppm                : REAL := 0.020;    (* Reboiler LOX Acetylene Discrepancy Tolerance [ppm] *)
    c_rTol_Argon_O2_pct                 : REAL := 0.250;    (* Crude Argon Oxygen Content Tolerance [%] *)
    c_rTol_Expander_RPM                 : REAL := 450.0;    (* Turbo-Expander Speed Transducer Tolerance [RPM] *)
    c_rTol_Expander_Nozzle_pct          : REAL := 1.500;    (* Expander VIGV Position Feedback Tolerance [%] *)
    c_rTol_Flow_GOX_Nm3h                : REAL := 1200.0;   (* GOX Product Delivery Flow Tolerance [Nm3/h] *)
    c_rTol_Flow_GAN_Nm3h                : REAL := 2500.0;   (* GAN Product Delivery Flow Tolerance [Nm3/h] *)
    c_rTol_Venturi_DP_mbar              : REAL := 1.200;    (* MAC Inlet Venturi DP Tolerance [mbar] *)
    c_rTol_Temp_Discharge_degC          : REAL := 2.500;    (* MAC Discharge Temperature Tolerance [deg C] *)
    c_rTol_Level_HPSump_pct             : REAL := 2.000;    (* HP Sump Level Discrepancy Tolerance [%] *)
    c_rTol_TotalHydrocarbon_ppm         : REAL := 0.080;    (* Reboiler Total Hydrocarbon Tolerance [ppm] *)
    c_rTMR_Timeout_s                    : REAL := 0.500;    (* Discrepancy Confirmation Persistence Timeout (500 ms) [s] *)

    (* Discrepancy Timers for 16 Triplets [s] *)
    rTimer_TMR_Press_MAC_s              : REAL := 0.0;
    rTimer_TMR_Flow_MAC_s               : REAL := 0.0;
    rTimer_TMR_Press_HP_s               : REAL := 0.0;
    rTimer_TMR_Press_LP_s               : REAL := 0.0;
    rTimer_TMR_Temp_Bath_s              : REAL := 0.0;
    rTimer_TMR_Level_LOX_s              : REAL := 0.0;
    rTimer_TMR_Acetylene_s              : REAL := 0.0;
    rTimer_TMR_Argon_O2_s               : REAL := 0.0;
    rTimer_TMR_Expander_RPM_s           : REAL := 0.0;
    rTimer_TMR_Expander_Nozzle_s        : REAL := 0.0;
    rTimer_TMR_Flow_GOX_s               : REAL := 0.0;
    rTimer_TMR_Flow_GAN_s               : REAL := 0.0;
    rTimer_TMR_Venturi_DP_s             : REAL := 0.0;
    rTimer_TMR_Temp_Discharge_s         : REAL := 0.0;
    rTimer_TMR_Level_HPSump_s           : REAL := 0.0;
    rTimer_TMR_TotalHydrocarbon_s       : REAL := 0.0;

    (* Channel Health Flags (TRUE = Isolated / Divergent) *)
    bIso_Press_MAC_A                    : BOOL := FALSE; bIso_Press_MAC_B : BOOL := FALSE; bIso_Press_MAC_C : BOOL := FALSE;
    bIso_Flow_MAC_A                     : BOOL := FALSE; bIso_Flow_MAC_B  : BOOL := FALSE; bIso_Flow_MAC_C  : BOOL := FALSE;
    bIso_Press_HP_A                     : BOOL := FALSE; bIso_Press_HP_B  : BOOL := FALSE; bIso_Press_HP_C  : BOOL := FALSE;
    bIso_Press_LP_A                     : BOOL := FALSE; bIso_Press_LP_B  : BOOL := FALSE; bIso_Press_LP_C  : BOOL := FALSE;
    bIso_Temp_Bath_A                    : BOOL := FALSE; bIso_Temp_Bath_B : BOOL := FALSE; bIso_Temp_Bath_C : BOOL := FALSE;
    bIso_Level_LOX_A                    : BOOL := FALSE; bIso_Level_LOX_B : BOOL := FALSE; bIso_Level_LOX_C : BOOL := FALSE;
    bIso_Acetylene_A                    : BOOL := FALSE; bIso_Acetylene_B : BOOL := FALSE; bIso_Acetylene_C : BOOL := FALSE;
    bIso_Argon_O2_A                     : BOOL := FALSE; bIso_Argon_O2_B  : BOOL := FALSE; bIso_Argon_O2_C  : BOOL := FALSE;
    bIso_Expander_RPM_A                 : BOOL := FALSE; bIso_Expander_RPM_B:BOOL := FALSE; bIso_Expander_RPM_C:BOOL := FALSE;
    bIso_Expander_Nozzle_A              : BOOL := FALSE; bIso_Expander_Nozzle_B:BOOL := FALSE; bIso_Expander_Nozzle_C:BOOL := FALSE;
    bIso_Flow_GOX_A                     : BOOL := FALSE; bIso_Flow_GOX_B  : BOOL := FALSE; bIso_Flow_GOX_C  : BOOL := FALSE;
    bIso_Flow_GAN_A                     : BOOL := FALSE; bIso_Flow_GAN_B  : BOOL := FALSE; bIso_Flow_GAN_C  : BOOL := FALSE;
    bIso_Venturi_DP_A                   : BOOL := FALSE; bIso_Venturi_DP_B: BOOL := FALSE; bIso_Venturi_DP_C: BOOL := FALSE;
    bIso_Temp_Discharge_A               : BOOL := FALSE; bIso_Temp_Discharge_B:BOOL := FALSE; bIso_Temp_Discharge_C:BOOL := FALSE;
    bIso_Level_HPSump_A                 : BOOL := FALSE; bIso_Level_HPSump_B:BOOL := FALSE; bIso_Level_HPSump_C:BOOL := FALSE;
    bIso_TotalHydrocarbon_A             : BOOL := FALSE; bIso_TotalHydrocarbon_B:BOOL := FALSE; bIso_TotalHydrocarbon_C:BOOL := FALSE;

    (* ==================================================================================================== *)
    (* ISA-18.2 MULTI-TIER PROCESS ALARM THRESHOLDS & STATUS FLAGS                                          *)
    (* ==================================================================================================== *)
    (* Main Air Compressor Discharge Pressure Limits [bar] *)
    c_rMAC_Press_Trip_HI_HI             : REAL := 6.95;     (* MAC Casing Overpressure Fast Mechanical Blow-Off Trip [bar] *)
    c_rMAC_Press_Alarm_HI               : REAL := 6.60;     (* MAC High Discharge Advisory [bar] *)
    c_rMAC_Press_Alarm_LO               : REAL := 5.40;     (* MAC Low Discharge Pressure Alert [bar] *)
    c_rMAC_Press_Trip_LO_LO             : REAL := 4.80;     (* MAC Severe Loss of Header Pressure Trip [bar] *)
    c_rMAC_Press_Deadband               : REAL := 0.08;     (* Pressure Alarm Clearance Hysteresis [bar] *)

    (* MAC Aerodynamic Surge Margin Limits [%] *)
    c_rSurge_Trip_LO_LO                 : REAL := 3.0;      (* Critical Aerodynamic Surge Line Violation Fast Trip [%] *)
    c_rSurge_Alarm_LO                   : REAL := 8.0;      (* Low Surge Safety Margin Alarm [%] *)
    c_rSurge_ROC_Limit                  : REAL := -4.0;     (* Rapid Approach Rate-of-Change Limit [- %/s] *)
    c_rSurge_Deadband                   : REAL := 1.0;      (* Surge Clearance Hysteresis [%] *)

    (* Main Condenser LOX Acetylene Concentration Limits [ppm] *)
    c_rAcetylene_Trip_HI_HI             : REAL := 0.150;    (* Critical Acetylene Solid Precipitation Explosion Dump Redline [ppm] *)
    c_rAcetylene_Alarm_HI               : REAL := 0.065;    (* Elevated Hydrocarbon Alert [ppm] *)
    c_rAcetylene_Deadband               : REAL := 0.008;    (* Acetylene Clearance Hysteresis [ppm] *)

    (* Main Reboiler LOX Level Limits [%] *)
    c_rLOX_Level_Trip_HI_HI             : REAL := 92.0;     (* Core Flooding / Liquid Entrainment Carryover Redline [%] *)
    c_rLOX_Level_Alarm_HI               : REAL := 82.0;     (* High LOX Level Warning [%] *)
    c_rLOX_Level_Alarm_LO               : REAL := 42.0;     (* Low LOX Bath Level Warning [%] *)
    c_rLOX_Level_Trip_LO_LO             : REAL := 25.0;     (* Reboiler Core Uncovery Dry-Boiling Explosion Redline [%] *)
    c_rLOX_Level_Deadband               : REAL := 1.5;      (* Level Clearance Hysteresis [%] *)

    (* Turbo-Expander Rotational Speed Limits [RPM] *)
    c_rExpander_Trip_HI_HI              : REAL := 95000.0;  (* Turbine Wheel Burst Magnetic Bearing Overspeed Trip [RPM] *)
    c_rExpander_Alarm_HI                : REAL := 89000.0;  (* High Expander Speed Advisory [RPM] *)
    c_rExpander_Alarm_LO                : REAL := 45000.0;  (* Low Refrigeration Speed Alert [RPM] *)
    c_rExpander_Deadband                : REAL := 500.0;    (* Speed Alarm Clearance Hysteresis [RPM] *)

    (* Internal ISA-18.2 Latched Alarm Booleans *)
    bAlarm_MAC_Press_HI_HI              : BOOL := FALSE;
    bAlarm_MAC_Press_HI                 : BOOL := FALSE;
    bAlarm_MAC_Press_LO                 : BOOL := FALSE;
    bAlarm_MAC_Press_LO_LO              : BOOL := FALSE;
    bAlarm_SurgeMargin_LO_LO            : BOOL := FALSE;
    bAlarm_SurgeMargin_LO               : BOOL := FALSE;
    bAlarm_SurgeMargin_ROC              : BOOL := FALSE;
    bAlarm_Acetylene_HI_HI              : BOOL := FALSE;
    bAlarm_Acetylene_HI                 : BOOL := FALSE;
    bAlarm_LOX_Level_HI_HI              : BOOL := FALSE;
    bAlarm_LOX_Level_HI                 : BOOL := FALSE;
    bAlarm_LOX_Level_LO                 : BOOL := FALSE;
    bAlarm_LOX_Level_LO_LO              : BOOL := FALSE;
    bAlarm_Expander_Speed_HI_HI         : BOOL := FALSE;
    bAlarm_Expander_Speed_HI            : BOOL := FALSE;
    bAlarm_TotalHydrocarbon_HI          : BOOL := FALSE;
    bAlarm_TMR_ChannelDivergent         : BOOL := FALSE;

    (* Previous Scan Stored Values for ROC Calculation *)
    rPrev_SurgeMargin_pct               : REAL := 12.0;
    rROC_SurgeMargin_pct_s              : REAL := 0.0;
    rPrev_MAC_DischargePress_bar        : REAL := 6.20;
    rROC_MAC_DischargePress_bar_s       : REAL := 0.0;

    (* --- Deterministic Plant Operational Finite State Machine (12 States) --- *)
    iFSM_State                          : INT := 1;         (* Primary FSM State Register [1..12] *)
    iNextFSM_State                      : INT := 1;         (* Targeted Next State Pointer *)
    rWarmPurgeTimer_s                   : REAL := 0.0;      (* Dwell Counter for Casing Warm Purge *)
    rMolSieveDryTimer_s                 : REAL := 0.0;      (* Dwell Counter for 13X Bed Dewpoint Stabilization *)
    rMAC_SpinupTimer_s                  : REAL := 0.0;      (* Dwell Counter for 45 MW Motor Accelerating Time *)
    rExpanderChilldownTimer_s           : REAL := 0.0;      (* Dwell Counter for Cold Gas Turbine Rotor Pre-Chill *)
    rLiquefactionTimer_s                : REAL := 0.0;      (* Dwell Counter for Liquid Pooling Phase *)
    rColumnPressurizeTimer_s            : REAL := 0.0;      (* Dwell Counter for Double-Column DP Ramping *)
    rThermosiphonPrimeTimer_s           : REAL := 0.0;      (* Dwell Counter for Two-Phase Flow Establishment *)
    rArgonCommissionTimer_s             : REAL := 0.0;      (* Dwell Counter for Side-Draw Fractionation *)
    rLOX_PurgeRampTimer_s               : REAL := 0.0;      (* Dwell Counter for Acetylene Cleansing Flush *)
    rDrainTimer_s                       : REAL := 0.0;      (* Dwell Counter for Controlled De-Inventorying *)
    rEmergencyDepressTimer_s            : REAL := 0.0;      (* Fast Abort Time Accumulator *)

    (* --- Scratch Variables for Internal Iterative Computation --- *)
    iLoop                               : INT := 0;
    jLoop                               : INT := 0;
    kLoop                               : INT := 0;
    iPGD_Iter                           : INT := 0;
    rDiffAB                             : REAL := 0.0;
    rDiffBC                             : REAL := 0.0;
    rDiffCA                             : REAL := 0.0;
    rTempVoted                          : REAL := 0.0;
    rTempSum                            : REAL := 0.0;
    rReducedTemp                        : REAL := 0.0;
    rAlphaPR                            : REAL := 0.0;
    rParamA                             : REAL := 0.0;
    rParamB                             : REAL := 0.0;
    rAntoinePvap                        : REAL := 0.0;
    rDeltaH_Reboiler_kW                 : REAL := 0.0;
    rGasHeadVenturi_bar                 : REAL := 0.0;
    rSurgeLimitDP_bar                   : REAL := 0.0;
    rSurgeControlDP_bar                 : REAL := 0.0;
    rTheoreticalDeltaT_Expander         : REAL := 0.0;
    rActualDeltaT_Expander              : REAL := 0.0;
    rThermalPowerExpander_kW            : REAL := 0.0;
    rCompressorWork_kW                  : REAL := 0.0;
    rNetProductOxygen_Nm3h              : REAL := 0.0;
    rGradientElement                    : REAL := 0.0;
    rActuatorCandidate                  : REAL := 0.0;
END_VAR
"""

print("Vars defined.")
