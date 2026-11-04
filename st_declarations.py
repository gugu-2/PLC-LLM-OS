# st_declarations.py
# Contains header, VAR_INPUT, VAR_OUTPUT, and VAR for FB_Hydrogen_PEM_Electrolyzer_100MW_StackPowerBalance

def get_declarations():
    return """```iec-st
FUNCTION_BLOCK FB_Hydrogen_PEM_Electrolyzer_100MW_StackPowerBalance
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Green Hydrogen Infrastructure & Industrial Water Electrolysis
 * SYSTEM                       : 100 MW Multi-Stack Proton Exchange Membrane (PEM) Electrolysis Green Hydrogen Facility
 * DESIGN ARCHITECTURE          : 20 x 5 MW PEM Stacks Dynamic Power Splitting & Renewable Wind/Solar Fast Fluctuation Tracking
 * INTEGRATED PROCESS LOOPS     : - Anode Deionized Water Circulating Loop & O2 Degasser Differential Pressure Regulation
 *                                - Cathode H2-in-O2 Gas Permeation Cross-Over Safety Observer (LFL Margin < 1.5% H2 in O2)
 *                                - 20-Stack Heat Exchanger Thermal Balancing (70.0 deg C +- 0.5 deg C)
 *                                - TSA Deoxo / Dual-Bed Swing Desorption Regeneration Pacing
 *                                - 8x8 Multivariable Discrete State-Space Cyber-Physical Dynamics (5.0 ms Task Cycle)
 *                                - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent
 *                                - Electrochemical Butler-Volmer & Nernst Reversible Thermodynamic Voltage Engine
 *                                - Nafion 117 Temperature-Dependent Proton Conductivity & Ohmic Area Resistance
 *                                - Fick's Law Diffusive Gas Crossover & Faradaic Efficiency Observer
 *                                - 2oo3 Triple Modular Redundant (TMR) Sensor Voting with Bumpless Channel Isolation
 *                                - ISA-18.2 5-Tier Alarm Management Hierarchy & 4-Word Bit-Packed Diagnostic Telemetry
 *                                - 12-Stage Deterministic Production Finite State Machine (FSM)
 * =====================================================================================================================
 * CYBER-PHYSICAL ELECTROCHEMICAL & THERMODYNAMIC FORMULATIONS:
 * 1. 100 MW Multi-Stack PEM Electrolyzer Architecture:
 *    The green hydrogen facility aggregates twenty (20) 5.0 MW modular PEM electrolyzer stacks supplied by dedicated 12-pulse
 *    thyristor rectifiers with dynamic active harmonic filtration. Each 5 MW stack contains 500 series-connected cells with
 *    an active membrane electrode assembly (MEA) area of 2,500 cm2 (0.25 m2). Total nominal facility current reaches
 *    100,000 A at 1,000 V DC bus, producing approximately 18,000 Nm3/h (~1,620 kg/h) of ultra-pure green hydrogen.
 *
 * 2. Reversible Thermodynamic Voltage & Nernst Equilibrium:
 *    The reversible thermodynamic potential E_rev(T, P) for liquid water decomposition into gaseous H2 and O2 is governed by:
 *      E_0(T) = 1.229 - 0.00085 * (T - 298.15) [V]
 *      E_rev(T, P) = E_0(T) + (R * T / (2 * F)) * LN( (a_H2 * a_O2^0.5) / a_H2O ) [V]
 *    where R = 8.31446 J/(mol*K), F = 96485.33 C/mol, a_H2 = P_cathode / P_ref, a_O2 = P_anode / P_ref, a_H2O ~= 1.0.
 *    Operating at 30.0 bar cathode and anode separator pressure and 70.0 deg C (343.15 K) yields E_rev ~= 1.252 V.
 *
 * 3. Electrochemical Butler-Volmer Overpotentials:
 *    Total single cell polarization is given by:
 *      V_cell = E_rev(T, P) + eta_act,a + eta_act,c + eta_ohm + eta_conc
 *    The sluggish anode Oxygen Evolution Reaction (OER) overpotential eta_act,a is calculated from the inverted Butler-Volmer:
 *      eta_act,a = (R * T / (alpha_a * F)) * LN( i_dens / i_0,a )
 *    where alpha_a = 0.50, and anode exchange current density i_0,a = 1.20e-7 A/cm2.
 *    The cathode Hydrogen Evolution Reaction (HER) overpotential eta_act,c is calculated from:
 *      eta_act,c = (R * T / (alpha_c * F)) * LN( i_dens / i_0,c )
 *    where alpha_c = 0.50, and cathode exchange current density i_0,c = 1.50e-3 A/cm2.
 *
 * 4. Nafion 117 Proton Conductivity & Ohmic Resistance:
 *    Membrane ionic conductivity sigma_PEM [S/cm] depends non-linearly on water uptake lambda and local temperature T [K]:
 *      sigma_PEM = (0.005139 * lambda - 0.00326) * EXP( 1268.0 * (1.0 / 303.15 - 1.0 / T) )
 *    For fully liquid-hydrated Nafion 117 (lambda = 14.0, thickness t_mem = 0.0175 cm) at 70.0 deg C (343.15 K),
 *    sigma_PEM ~= 0.118 S/cm. Area-specific resistance r_PEM = t_mem / sigma_PEM ~= 0.148 Ohm*cm2.
 *    Membrane ohmic overpotential: eta_ohm = i_dens * r_PEM.
 *
 * 5. Fick's Law Diffusive Gas Crossover & Low-Load Explosion Safety Limit:
 *    Hydrogen gas permeation across the polymer electrolyte membrane into the oxygen-rich anode separator occurs via
 *    Fickian molecular diffusion and pressure-driven convective permeation:
 *      N_H2,cross = K_perm,H2(T) * (P_cathode - P_anode) / t_mem + K_diff,H2(T) * P_cathode / t_mem [mol/(cm2*s)]
 *    where K_diff,H2(T) = K_0,H2 * EXP( -E_a,H2 / (R * T) ).
 *    Simultaneously, oxygen production at the anode is proportional to current via Faraday's Law:
 *      N_O2,prod = (I_stack * eta_F) / (4.0 * F * A_cell) [mol/(cm2*s)]
 *    The volumetric fraction of hydrogen in the anode oxygen separator gas phase is:
 *      Phi_H2_in_O2 = N_H2,cross / (2.0 * N_O2,prod + N_H2,cross) * 100.0 [% vol]
 *    CRITICAL HAZARD: At low turndown (< 5% nominal load), N_O2,prod plummets while N_H2,cross remains constant due to
 *    the 30 bar pressure gradient. Phi_H2_in_O2 can rapidly exceed the 4.0% Lower Flammability Limit (LFL). The system
 *    enforces a 1.5% maximum allowable safety derate threshold, initiating stack load holds and nitrogen purging.
 *
 * 6. Lumped Stack Thermal Capacitance & Energy Efficiency:
 *    The thermal energy balance for each 5 MW stack accounts for Joule heating and electrochemical enthalpy:
 *      C_th * dT_stack/dt = P_elec - P_H2,chem - Q_cooling - Q_ambient_loss
 *    where P_elec = V_stack * I_stack, and P_H2,chem = n_dot_H2 * Delta_H_LHV (Delta_H_LHV = 241.82 kJ/mol).
 *    Facility electrical-to-chemical efficiency on Lower Heating Value:
 *      eta_LHV = (n_dot_H2_total * Delta_H_LHV) / P_facility_total * 100.0 [%]
 * =====================================================================================================================
 *)

VAR_INPUT
    (* ========================================================================================= *)
    (* 1. MASTER SUPERVISORY PERMISSIVES & SAFETY INTERLOCKS                                    *)
    (* ========================================================================================= *)
    bEnableMaster                       : BOOL := FALSE;    (* Master Facility Automation Enable Permissive [BOOL] *)
    bEmergencyStop_NC                   : BOOL := TRUE;     (* Dual-Channel Hardware Safety Circuit Active Low [BOOL] *)
    bFaultReset                         : BOOL := FALSE;    (* Master Pushbutton Acknowledge & Fault Latch Reset [BOOL] *)
    bAutoRenewableTrackingEnable        : BOOL := FALSE;    (* Enable Fast Dynamic Wind/Solar Fluctuation Following [BOOL] *)
    bGridFrequencySupportEnable         : BOOL := FALSE;    (* Enable Primary Frequency Regulation Droop Fast Modulation [BOOL] *)
    bTSA_RegenAutoSequenceEnable        : BOOL := FALSE;    (* Enable Automatic TSA Dual-Bed Thermal Swing Desorption [BOOL] *)
    bCathodeBleedPermissive             : BOOL := FALSE;    (* Safety Flare Permissive for Cathode Gas Venting [BOOL] *)
    bN2_PurgeHeaderAvailable            : BOOL := TRUE;     (* High-Pressure Inert Nitrogen Header Supply Ready [BOOL] *)

    (* ========================================================================================= *)
    (* 2. RENEWABLE GENERATION & POWER GRID TELEMETRY                                           *)
    (* ========================================================================================= *)
    rGridTargetTotalPower_MW            : REAL := 50.0;     (* Grid / Dispatch Commanded Total Facility Active Power [MW] *)
    rGridPowerRampRate_MW_per_s         : REAL := 5.0;      (* Allowable Power Trajectory Ramp Rate Limit [MW/s] *)
    rWindFarmOutput_MW                  : REAL := 45.0;     (* Colocated Wind Turbine Generation Farm Active Output [MW] *)
    rSolarPVOutput_MW                   : REAL := 30.0;     (* Colocated Solar Photovoltaic Farm Active Output [MW] *)
    rGridFrequency_Hz                   : REAL := 50.00;    (* Transmission Grid High-Voltage Frequency Telemetry [Hz] *)
    rGridFrequencyDroopGain_MW_per_Hz   : REAL := 25.0;     (* Primary Frequency Response Droop Characteristic [MW/Hz] *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANT (TMR) INSTRUMENTATION TRANSMITTERS                      *)
    (* ========================================================================================= *)
    (* IT_STACK_DC_CURRENT_101: Facility Master Total DC Current Transducers [A] *)
    IT_STACK_DC_CURRENT_101A            : REAL := 50000.0;  (* Hall Effect DC Current Transducer Channel A [A] *)
    IT_STACK_DC_CURRENT_101B            : REAL := 50020.0;  (* Hall Effect DC Current Transducer Channel B [A] *)
    IT_STACK_DC_CURRENT_101C            : REAL := 49985.0;  (* Hall Effect DC Current Transducer Channel C [A] *)

    (* VT_STACK_DC_VOLTAGE_102: Master DC Bus Terminal Voltage Transducers [V] *)
    VT_STACK_DC_VOLTAGE_102A            : REAL := 985.4;    (* Calibrated Resistive Voltage Divider Channel A [V] *)
    VT_STACK_DC_VOLTAGE_102B            : REAL := 984.9;    (* Calibrated Resistive Voltage Divider Channel B [V] *)
    VT_STACK_DC_VOLTAGE_102C            : REAL := 985.8;    (* Calibrated Resistive Voltage Divider Channel C [V] *)

    (* PT_ANODE_O2_SEPARATOR_201: Anode Oxygen Gas-Liquid Separator Dome Pressure [bar] *)
    PT_ANODE_O2_SEPARATOR_201A          : REAL := 30.02;    (* Piezoresistive Pressure Transmitter Channel A [bar] *)
    PT_ANODE_O2_SEPARATOR_201B          : REAL := 30.00;    (* Piezoresistive Pressure Transmitter Channel B [bar] *)
    PT_ANODE_O2_SEPARATOR_201C          : REAL := 30.04;    (* Piezoresistive Pressure Transmitter Channel C [bar] *)

    (* PT_CATHODE_H2_SEPARATOR_202: Cathode Hydrogen Gas-Liquid Separator Dome Pressure [bar] *)
    PT_CATHODE_H2_SEPARATOR_202A        : REAL := 30.05;    (* Piezoresistive Pressure Transmitter Channel A [bar] *)
    PT_CATHODE_H2_SEPARATOR_202B        : REAL := 30.03;    (* Piezoresistive Pressure Transmitter Channel B [bar] *)
    PT_CATHODE_H2_SEPARATOR_202C        : REAL := 30.06;    (* Piezoresistive Pressure Transmitter Channel C [bar] *)

    (* DP_MEMBRANE_DIFF_PRESS_203: Cell Membrane Differential Pressure (P_Cathode - P_Anode) [bar] *)
    DP_MEMBRANE_DIFF_PRESS_203A         : REAL := 0.030;    (* Resonant Silicon DP Transmitter Channel A [bar] *)
    DP_MEMBRANE_DIFF_PRESS_203B         : REAL := 0.028;    (* Resonant Silicon DP Transmitter Channel B [bar] *)
    DP_MEMBRANE_DIFF_PRESS_203C         : REAL := 0.032;    (* Resonant Silicon DP Transmitter Channel C [bar] *)

    (* AIT_H2_IN_O2_CROSSOVER_301: Anode O2 Degasser Gas Phase H2 Crossover Concentration [% vol] *)
    AIT_H2_IN_O2_CROSSOVER_301A         : REAL := 0.42;     (* Thermal Conductivity / Catalytic Bead Sensor Channel A [% vol] *)
    AIT_H2_IN_O2_CROSSOVER_301B         : REAL := 0.41;     (* Thermal Conductivity / Catalytic Bead Sensor Channel B [% vol] *)
    AIT_H2_IN_O2_CROSSOVER_301C         : REAL := 0.43;     (* Thermal Conductivity / Catalytic Bead Sensor Channel C [% vol] *)

    (* AIT_O2_IN_H2_CROSSOVER_302: Cathode H2 Product Gas O2 Contamination [% vol] *)
    AIT_O2_IN_H2_CROSSOVER_302A         : REAL := 0.045;    (* Paramagnetic / Electrochemical Trace O2 Channel A [% vol] *)
    AIT_O2_IN_H2_CROSSOVER_302B         : REAL := 0.044;    (* Paramagnetic / Electrochemical Trace O2 Channel B [% vol] *)
    AIT_O2_IN_H2_CROSSOVER_302C         : REAL := 0.046;    (* Paramagnetic / Electrochemical Trace O2 Channel C [% vol] *)

    (* TT_STACK_COOLING_INLET_401: Secondary Cooling Loop Inlet Temperature [deg C] *)
    TT_STACK_COOLING_INLET_401A         : REAL := 64.8;     (* 4-Wire Class A Pt100 RTD Channel A [deg C] *)
    TT_STACK_COOLING_INLET_401B         : REAL := 65.0;     (* 4-Wire Class A Pt100 RTD Channel B [deg C] *)
    TT_STACK_COOLING_INLET_401C         : REAL := 64.9;     (* 4-Wire Class A Pt100 RTD Channel C [deg C] *)

    (* TT_STACK_COOLING_OUTLET_402: Secondary Cooling Loop Outlet Temperature [deg C] *)
    TT_STACK_COOLING_OUTLET_402A        : REAL := 70.1;     (* 4-Wire Class A Pt100 RTD Channel A [deg C] *)
    TT_STACK_COOLING_OUTLET_402B        : REAL := 69.9;     (* 4-Wire Class A Pt100 RTD Channel B [deg C] *)
    TT_STACK_COOLING_OUTLET_402C        : REAL := 70.2;     (* 4-Wire Class A Pt100 RTD Channel C [deg C] *)

    (* FT_DI_WATER_FEED_501: Demineralized Deionized Water Make-Up Coriolis Mass Flow [m3/h] *)
    FT_DI_WATER_FEED_501A               : REAL := 15.2;     (* High-Accuracy Coriolis Mass Flowmeter Channel A [m3/h] *)
    FT_DI_WATER_FEED_501B               : REAL := 15.1;     (* High-Accuracy Coriolis Mass Flowmeter Channel B [m3/h] *)
    FT_DI_WATER_FEED_501C               : REAL := 15.3;     (* High-Accuracy Coriolis Mass Flowmeter Channel C [m3/h] *)

    (* AIT_DI_WATER_CONDUCTIVITY_502: Anode Circulating DI Water Quality Conductivity [uS/cm] *)
    AIT_DI_WATER_CONDUCTIVITY_502A      : REAL := 0.042;    (* Ultra-Pure 4-Electrode Conductivity Sensor Channel A [uS/cm] *)
    AIT_DI_WATER_CONDUCTIVITY_502B      : REAL := 0.041;    (* Ultra-Pure 4-Electrode Conductivity Sensor Channel B [uS/cm] *)
    AIT_DI_WATER_CONDUCTIVITY_502C      : REAL := 0.043;    (* Ultra-Pure 4-Electrode Conductivity Sensor Channel C [uS/cm] *)

    (* PT_TSA_DRYER_BED1_601: TSA Deoxo / Dryer Adsorption Bed 1 Vessel Pressure [bar] *)
    PT_TSA_DRYER_BED1_601A              : REAL := 29.8;     (* Thick-Film Ceramic Pressure Sensor Channel A [bar] *)
    PT_TSA_DRYER_BED1_601B              : REAL := 29.7;     (* Thick-Film Ceramic Pressure Sensor Channel B [bar] *)
    PT_TSA_DRYER_BED1_601C              : REAL := 29.9;     (* Thick-Film Ceramic Pressure Sensor Channel C [bar] *)

    (* PT_TSA_DRYER_BED2_602: TSA Deoxo / Dryer Adsorption Bed 2 Vessel Pressure [bar] *)
    PT_TSA_DRYER_BED2_602A              : REAL := 1.25;     (* Thick-Film Ceramic Pressure Sensor Channel A [bar] *)
    PT_TSA_DRYER_BED2_602B              : REAL := 1.23;     (* Thick-Film Ceramic Pressure Sensor Channel B [bar] *)
    PT_TSA_DRYER_BED2_602C              : REAL := 1.27;     (* Thick-Film Ceramic Pressure Sensor Channel C [bar] *)

    (* TT_TSA_BED1_TEMP_603: TSA Bed 1 Multi-Point Thermal Desorption Temperature [deg C] *)
    TT_TSA_BED1_TEMP_603A               : REAL := 42.5;     (* Duplex Mineral-Insulated Thermocouple Channel A [deg C] *)
    TT_TSA_BED1_TEMP_603B               : REAL := 42.2;     (* Duplex Mineral-Insulated Thermocouple Channel B [deg C] *)
    TT_TSA_BED1_TEMP_603C               : REAL := 42.8;     (* Duplex Mineral-Insulated Thermocouple Channel C [deg C] *)

    (* TT_TSA_BED2_TEMP_604: TSA Bed 2 Multi-Point Thermal Desorption Temperature [deg C] *)
    TT_TSA_BED2_TEMP_604A               : REAL := 178.5;    (* Duplex Mineral-Insulated Thermocouple Channel A [deg C] *)
    TT_TSA_BED2_TEMP_604B               : REAL := 178.1;    (* Duplex Mineral-Insulated Thermocouple Channel B [deg C] *)
    TT_TSA_BED2_TEMP_604C               : REAL := 178.9;    (* Duplex Mineral-Insulated Thermocouple Channel C [deg C] *)

    (* AIT_PRODUCT_H2_DEWPOINT_701: Final Product Hydrogen Moisture Dew Point [deg C] *)
    AIT_PRODUCT_H2_DEWPOINT_701A        : REAL := -76.5;    (* Precision Optical Chilled-Mirror Hygrometer Channel A [deg C] *)
    AIT_PRODUCT_H2_DEWPOINT_701B        : REAL := -76.8;    (* Precision Optical Chilled-Mirror Hygrometer Channel B [deg C] *)
    AIT_PRODUCT_H2_DEWPOINT_701C        : REAL := -76.2;    (* Precision Optical Chilled-Mirror Hygrometer Channel C [deg C] *)

    (* ========================================================================================= *)
    (* 4. 20-STACK INDIVIDUAL TELEMETRY & STATUS ARRAYS                                         *)
    (* ========================================================================================= *)
    aStackVoltage_Actual                : ARRAY[1..20] OF REAL; (* Actual Stack DC Terminal Voltage [V] *)
    aStackCurrent_Actual                : ARRAY[1..20] OF REAL; (* Actual Stack DC Operating Current [A] *)
    aStackTemp_Actual                   : ARRAY[1..20] OF REAL; (* Actual Stack Internal Core Operating Temperature [deg C] *)
    aStackCoolingFlow_Actual            : ARRAY[1..20] OF REAL; (* Actual Secondary Coolant Volumetric Flow Rate [m3/h] *)
    aStackDegradationFactor             : ARRAY[1..20] OF REAL; (* Health Degradation Aging Factor (1.0 = new, 1.30 = aged) [p.u.] *)
    aStackInhibited                     : ARRAY[1..20] OF BOOL; (* Stack Manual Maintenance Lockout or Offline Flag [BOOL] *)
END_VAR

VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. PRIMARY SYSTEM OPERATION & INTERLOCK STATUS WORDS                                     *)
    (* ========================================================================================= *)
    bSystemReady                        : BOOL := FALSE;    (* Master Facility Automation Ready Permissive [BOOL] *)
    bSystemRunning                      : BOOL := FALSE;    (* Facility Active Green Hydrogen Production State [BOOL] *)
    bSystemTripped                      : BOOL := FALSE;    (* Master Critical Safety Shutdown Latched Trip [BOOL] *)
    bPowerTrackingActive                : BOOL := FALSE;    (* Fast Dynamic Wind/Solar Fluctuation Tracking Active [BOOL] *)
    bCrossoverDerateActive              : BOOL := FALSE;    (* H2-in-O2 Gas Permeation Safety Derate Hold Active [BOOL] *)
    bFastPurgeActive                    : BOOL := FALSE;    (* Emergency Nitrogen Inert Gas Purge Blast Active [BOOL] *)
    nActiveFSM_State                    : INT := 10;        (* Active Operational Finite State Machine State Index [10..120] *)

    (* ========================================================================================= *)
    (* 2. FACILITY PRODUCTION & THERMODYNAMIC EFFICIENCY METRICS                                *)
    (* ========================================================================================= *)
    rFacilityTotalPower_MW              : REAL := 0.0;      (* Aggregate Total Electrical Power Consumed by 20 Stacks [MW] *)
    rFacilityEfficiency_LHV_pct         : REAL := 0.0;      (* Real-Time Overall System Efficiency on LHV Basis [%] *)
    rTotalH2ProductionRate_Nm3h         : REAL := 0.0;      (* Total Facility Green Hydrogen Generation Rate [Nm3/h] *)
    rTotalO2ProductionRate_Nm3h         : REAL := 0.0;      (* Total By-Product Oxygen Generation Rate [Nm3/h] *)
    rSpecificEnergyConsumption_kWh_Nm3  : REAL := 0.0;      (* Specific Power Consumption per Normal m3 H2 [kWh/Nm3] *)

    (* ========================================================================================= *)
    (* 3. 20-STACK INDIVIDUAL RECTIFIER & BREAKER DISPATCH COMMANDS                             *)
    (* ========================================================================================= *)
    aStackCurrentCmd_A                  : ARRAY[1..20] OF REAL; (* Dispatched Thyristor Rectifier DC Current Setpoints [A] *)
    aStackPowerCmd_MW                   : ARRAY[1..20] OF REAL; (* Dispatched Active Electrical Power per Stack [MW] *)
    aStackBreakerTripCmd                : ARRAY[1..20] OF BOOL; (* High-Speed DC Vacuum Contactor Fast Trip (< 10 ms) [BOOL] *)
    aStackCoolingValveCmd_pct           : ARRAY[1..20] OF REAL; (* Individual Stack Coolant Modulating Valve Setpoints [%] *)

    (* ========================================================================================= *)
    (* 4. PRIMARY PROCESS LOOP ACTUATOR COMMANDS                                                *)
    (* ========================================================================================= *)
    rValveCmd_CathodeBackpress_pct      : REAL := 50.0;     (* Cathode H2 Separator Dome Backpressure Control Valve CV-202 [%] *)
    rValveCmd_AnodeBackpress_pct        : REAL := 50.0;     (* Anode O2 Separator Dome Backpressure Control Valve CV-201 [%] *)
    rValveCmd_MembraneDiffPressure_pct  : REAL := 0.0;      (* High-Speed Cell Membrane Differential Bypass Trim Valve CV-203 [%] *)
    rPumpCmd_DI_WaterCirculation_pct    : REAL := 65.0;     (* Anode Loop DI Water Circulating Pump P-501 VFD Command [%] *)
    rValveCmd_DI_WaterMakeUp_pct        : REAL := 35.0;     (* Fresh DI Water Make-Up Supply Regulating Valve CV-501 [%] *)
    rPumpCmd_MainCoolingLoop_pct        : REAL := 70.0;     (* Secondary Cooling Loop Main Pump P-401 VFD Command [%] *)
    rValveCmd_CoolingTowerBypass_pct    : REAL := 25.0;     (* Secondary Cooling Loop Thermal Bypass Modulating Valve CV-401 [%] *)

    (* ========================================================================================= *)
    (* 5. TSA DEOXO / DUAL-BED SWING DRYER ACTUATOR COMMANDS                                    *)
    (* ========================================================================================= *)
    bValveCmd_TSA_Bed1_Adsorption       : BOOL := TRUE;     (* TSA Bed 1 Process Gas Inlet Solenoid Valve XV-601A [BOOL] *)
    bValveCmd_TSA_Bed1_Desorption       : BOOL := FALSE;    (* TSA Bed 1 Hot Regeneration Purge Solenoid Valve XV-601B [BOOL] *)
    bValveCmd_TSA_Bed1_Depress          : BOOL := FALSE;    (* TSA Bed 1 Depressurization & Venting Solenoid Valve XV-601C [BOOL] *)
    bValveCmd_TSA_Bed2_Adsorption       : BOOL := FALSE;    (* TSA Bed 2 Process Gas Inlet Solenoid Valve XV-602A [BOOL] *)
    bValveCmd_TSA_Bed2_Desorption       : BOOL := TRUE;     (* TSA Bed 2 Hot Regeneration Purge Solenoid Valve XV-602B [BOOL] *)
    bValveCmd_TSA_Bed2_Depress          : BOOL := FALSE;    (* TSA Bed 2 Depressurization & Venting Solenoid Valve XV-602C [BOOL] *)
    rHeaterCmd_TSA_RegenHeater_pct      : REAL := 85.0;     (* TSA Regeneration Gas Electric Circulation Heater E-601 [%] *)
    bValveCmd_H2_ProductOffSpecVent     : BOOL := FALSE;    (* Moisture / O2 Off-Spec Hydrogen Flare Divert Valve XV-701 [BOOL] *)
    bValveCmd_N2_PurgeSupplyMain        : BOOL := FALSE;    (* Master High-Pressure Inert Nitrogen Purge Safety Valve XV-901 [BOOL] *)

    (* ========================================================================================= *)
    (* 6. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTED TELEMETRY OUTPUTS                          *)
    (* ========================================================================================= *)
    rVoted_MembraneDiffPressure_bar     : REAL := 0.030;    (* 2oo3 Voted Membrane Differential Pressure [bar] *)
    rVoted_H2_in_O2_Crossover_pct       : REAL := 0.42;     (* 2oo3 Voted H2 in O2 Gas Permeation Concentration [% vol] *)
    rVoted_O2_in_H2_Crossover_pct       : REAL := 0.045;    (* 2oo3 Voted O2 in H2 Product Gas Contamination [% vol] *)
    rVoted_AnodePressure_bar            : REAL := 30.02;    (* 2oo3 Voted Anode O2 Separator Dome Pressure [bar] *)
    rVoted_CathodePressure_bar          : REAL := 30.05;    (* 2oo3 Voted Cathode H2 Separator Dome Pressure [bar] *)
    rVoted_CoolingInletTemp_degC        : REAL := 64.9;     (* 2oo3 Voted Cooling Water Inlet Temperature [deg C] *)
    rVoted_CoolingOutletTemp_degC       : REAL := 70.1;     (* 2oo3 Voted Cooling Water Outlet Temperature [deg C] *)
    rVoted_DI_WaterFeedFlow_m3h         : REAL := 15.2;     (* 2oo3 Voted Fresh DI Water Supply Flow [m3/h] *)
    rVoted_DI_WaterConductivity_uScm    : REAL := 0.042;    (* 2oo3 Voted Anode Water Electrical Conductivity [uS/cm] *)
    rVoted_TSA_Bed1_Pressure_bar        : REAL := 29.8;     (* 2oo3 Voted TSA Bed 1 Adsorption Pressure [bar] *)
    rVoted_TSA_Bed2_Pressure_bar        : REAL := 1.25;     (* 2oo3 Voted TSA Bed 2 Adsorption Pressure [bar] *)
    rVoted_ProductH2_Dewpoint_degC      : REAL := -76.5;    (* 2oo3 Voted Final Product Hydrogen Moisture Dew Point [deg C] *)

    (* ========================================================================================= *)
    (* 7. ISA-18.2 BIT-PACKED DIAGNOSTIC & ALARM STATUS WORDS                                   *)
    (* ========================================================================================= *)
    dwSystemStatusWord                  : DWORD := 16#0000_0000; (* Bit-Packed Operational State & Permissive Telemetry *)
    dwSensorDegradationWord             : DWORD := 16#0000_0000; (* Bit-Packed 2oo3 TMR Sensor Health & Isolation Flags *)
    dwProcessAlarmWord                  : DWORD := 16#0000_0000; (* Bit-Packed ISA-18.2 Process Alarms (HI, LO, ROC) *)
    dwCriticalSafetyTripWord            : DWORD := 16#0000_0000; (* Bit-Packed SIL-3 Critical Trips (HI_HI, LO_LO, E-Stop) *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* 1. DISCRETE TASK CYCLE & PHYSICAL / ELECTROCHEMICAL CONSTANTS                             *)
    (* ========================================================================================= *)
    c_rTs                               : REAL := 0.005;    (* Deterministic PLC Execution Task Cycle (5.0 ms) [s] *)
    c_rFaradayConst                     : REAL := 96485.33; (* Faraday Electrochemical Constant [C/mol] *)
    c_rGasConstR                        : REAL := 8.31446;  (* Universal Gas Constant R [J/(mol*K)] *)
    c_rLHV_H2_kJ_mol                    : REAL := 241.82;   (* Lower Heating Value of Hydrogen [kJ/mol] *)
    c_rHHV_H2_kJ_mol                    : REAL := 285.83;   (* Higher Heating Value of Hydrogen [kJ/mol] *)
    c_rMolarMassH2_kg_mol               : REAL := 0.002016; (* Molecular Mass of Diatomic Hydrogen [kg/mol] *)
    c_rMolarVolumeH2_Nm3_mol            : REAL := 0.022414; (* Normal Molar Volume of Ideal Gas at 0 C, 1 atm [Nm3/mol] *)
    c_rStandardAtmPressure_bar          : REAL := 1.01325;  (* Reference Standard Atmospheric Pressure [bar] *)
    c_rThermoNeutralVoltage             : REAL := 1.481;    (* Enthalpic Thermoneutral Cell Potential [V] *)
    c_nCellsPerStack                    : INT := 500;       (* Number of Series-Connected PEM Cells per 5 MW Stack *)
    c_rCellActiveArea_cm2               : REAL := 2500.0;   (* Active MEA Electrode Area per Cell [cm2] *)
    c_rMembraneThickness_cm             : REAL := 0.0175;   (* Nafion 117 Polymer Membrane Thickness (175 um) [cm] *)
    c_rMembraneHydrationLambda          : REAL := 14.0;     (* Liquid Water Hydration Uptake Number lambda [H2O/SO3-] *)

    (* Butler-Volmer & Exchange Current Parameters *)
    c_rAlphaAnode                       : REAL := 0.50;     (* Anode Oxygen Evolution Reaction (OER) Transfer Coefficient *)
    c_rAlphaCathode                     : REAL := 0.50;     (* Cathode Hydrogen Evolution Reaction (HER) Transfer Coefficient *)
    c_rExchangeCurrentDensity_OER       : REAL := 0.00000012; (* Anode Exchange Current Density i_0,a [A/cm2] *)
    c_rExchangeCurrentDensity_HER       : REAL := 0.00150;  (* Cathode Exchange Current Density i_0,c [A/cm2] *)

    (* Gas Permeation Crossover Activation Parameters (Arrhenius Model) *)
    c_rPreExpCrossoverH2                : REAL := 0.0000000045; (* Pre-Exponential Hydrogen Permeation Factor [mol/(cm*s*bar)] *)
    c_rActivationEnergyH2_over_R        : REAL := 2450.0;   (* Arrhenius Activation Constant E_a / R [K] *)

    (* ========================================================================================= *)
    (* 2. 8x8 MULTIVARIABLE STATE-SPACE DYNAMICS MATRICES (5.0 ms CYCLE)                         *)
    (* States x[1..8]:                                                                           *)
    (*   x[1]: Cell Active Overpotential Deviation Delta_eta_act [V]                            *)
    (*   x[2]: Membrane Differential Pressure Deviation Delta_DP_mem [bar]                       *)
    (*   x[3]: H2-in-O2 Gas Crossover Permeation Deviation Delta_Phi_cross [% vol]               *)
    (*   x[4]: Stack Core Thermal Temperature Deviation Delta_T_stack [deg C]                    *)
    (*   x[5]: Anode O2 Separator Dome Pressure Deviation Delta_P_anode [bar]                    *)
    (*   x[6]: Cathode H2 Separator Dome Pressure Deviation Delta_P_cathode [bar]                *)
    (*   x[7]: Anode DI Water Circulating Loop Flow Deviation Delta_F_DI [m3/h]                  *)
    (*   x[8]: TSA Adsorber Product Moisture Deviation Delta_C_H2O [ppmv]                        *)
    (* Controls u[1..4]:                                                                         *)
    (*   u[1]: Aggregate Thyristor Rectifier Power Command Trim Delta_P_rect [MW]                *)
    (*   u[2]: Membrane Differential Backpressure Valve Modulation Delta_theta_DP [%]            *)
    (*   u[3]: Anode DI Water Circulating Pump Speed Trim Delta_omega_pump [%]                   *)
    (*   u[4]: Secondary Cooling Heat Exchanger Bypass Valve Trim Delta_theta_cool [%]           *)
    (* ========================================================================================= *)
    bMatricesInitialized                : BOOL := FALSE;
    aA                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Transition Matrix A *)
    aB                                  : ARRAY[1..8, 1..4] OF REAL; (* Discrete Input Coupling Matrix B *)
    aC                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete Output Observation Matrix C *)
    aD                                  : ARRAY[1..8, 1..4] OF REAL; (* Discrete Feedthrough Matrix D *)
    ax_state                            : ARRAY[1..8] OF REAL;       (* Current Dynamic State Vector x[k] *)
    ax_next                             : ARRAY[1..8] OF REAL;       (* Projected Next State Vector x[k+1] *)
    ax_ref                              : ARRAY[1..8] OF REAL;       (* Target Equilibrium Reference State Vector x_ref *)
    au_control                          : ARRAY[1..4] OF REAL;       (* Optimal Control Actuator Input Vector u[k] *)
    au_prev                             : ARRAY[1..4] OF REAL;       (* Previous Cycle Control Vector u[k-1] *)
    au_delta                            : ARRAY[1..4] OF REAL;       (* Slew Increment Vector Delta_u[k] *)

    (* Model Predictive Control (MPC) Penalty Weights & Bounds *)
    aQ_Weight                           : ARRAY[1..8] OF REAL;       (* State Tracking Error Penalty Matrix Diag(Q) *)
    aR_Weight                           : ARRAY[1..4] OF REAL;       (* Actuator Control Effort Penalty Matrix Diag(R) *)
    aS_Weight                           : ARRAY[1..4] OF REAL;       (* Actuator Slew Rate Penalty Matrix Diag(S) *)
    aP_TerminalWeight                   : ARRAY[1..8] OF REAL;       (* Terminal Predictive Cost Matrix Diag(P) *)
    au_min                              : ARRAY[1..4] OF REAL;       (* Hard Lower Actuator Saturation Bounds *)
    au_max                              : ARRAY[1..4] OF REAL;       (* Hard Upper Actuator Saturation Bounds *)
    adelta_u_max                        : ARRAY[1..4] OF REAL;       (* Maximum Allowable Slew per 5 ms Sample *)
    aGrad_u                             : ARRAY[1..4] OF REAL;       (* Analytical Gradient Vector dJ/du *)
    aPredictedState                     : ARRAY[1..8] OF REAL;       (* 1-Step Horizon State Projection *)
    c_rPGD_Alpha                        : REAL := 0.00035;           (* Projected Gradient Descent Step Size *)
    rMPC_QuadraticCost                  : REAL := 0.0;               (* Objective Functional Value J *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY TIMERS & FLAGS                        *)
    (* ========================================================================================= *)
    c_rDP_DiscrepancyThreshold_bar      : REAL := 0.040;    (* Membrane DP Discrepancy Tolerance [bar] *)
    c_rH2Cross_DiscrepancyThreshold     : REAL := 0.100;    (* H2-in-O2 Analyzer Discrepancy Tolerance [% vol] *)
    c_rO2Cross_DiscrepancyThreshold     : REAL := 0.050;    (* O2-in-H2 Analyzer Discrepancy Tolerance [% vol] *)
    c_rAnodePress_Discrepancy_bar       : REAL := 0.500;    (* Anode Separator Pressure Tolerance [bar] *)
    c_rCathodePress_Discrepancy_bar     : REAL := 0.500;    (* Cathode Separator Pressure Tolerance [bar] *)
    c_rCoolingTemp_Discrepancy_degC     : REAL := 1.500;    (* Cooling Water RTD Discrepancy Tolerance [deg C] *)
    c_rDI_Flow_Discrepancy_m3h          : REAL := 1.000;    (* DI Water Feed Flow Discrepancy Tolerance [m3/h] *)
    c_rConductivity_Discrepancy_uScm    : REAL := 0.020;    (* Water Conductivity Discrepancy Tolerance [uS/cm] *)
    c_rTSA_Press_Discrepancy_bar        : REAL := 0.800;    (* TSA Bed Vessel Pressure Tolerance [bar] *)
    c_rTSA_Temp_Discrepancy_degC        : REAL := 3.500;    (* TSA Thermal Desorption Temperature Tolerance [deg C] *)
    c_rDewpoint_Discrepancy_degC        : REAL := 2.500;    (* Chilled Mirror Dew Point Tolerance [deg C] *)
    c_rCurrent_Discrepancy_A            : REAL := 150.0;    (* Master DC Current Sensor Tolerance [A] *)
    c_rVoltage_Discrepancy_V            : REAL := 15.0;     (* Master DC Voltage Sensor Tolerance [V] *)
    c_rTMR_PersistencyTimeout_s         : REAL := 0.050;    (* Discrepancy Persistency Latch Time (50 ms) [s] *)

    (* Timers for Persistent Sensor Faults *)
    rDP_DiscrepancyTimer_s              : REAL := 0.0;
    rH2Cross_DiscrepancyTimer_s         : REAL := 0.0;
    rO2Cross_DiscrepancyTimer_s         : REAL := 0.0;
    rAnodePress_DiscrepancyTimer_s      : REAL := 0.0;
    rCathodePress_DiscrepancyTimer_s    : REAL := 0.0;
    rCoolingInlet_DiscrepancyTimer_s    : REAL := 0.0;
    rCoolingOutlet_DiscrepancyTimer_s   : REAL := 0.0;
    rDI_Flow_DiscrepancyTimer_s         : REAL := 0.0;
    rConductivity_DiscrepancyTimer_s    : REAL := 0.0;
    rTSA_Bed1_DiscrepancyTimer_s        : REAL := 0.0;
    rTSA_Bed2_DiscrepancyTimer_s        : REAL := 0.0;
    rDewpoint_DiscrepancyTimer_s        : REAL := 0.0;
    rCurrent_DiscrepancyTimer_s         : REAL := 0.0;
    rVoltage_DiscrepancyTimer_s         : REAL := 0.0;

    (* Channel Health Isolation Booleans *)
    bDP_ChA_Isolated                    : BOOL := FALSE;
    bDP_ChB_Isolated                    : BOOL := FALSE;
    bDP_ChC_Isolated                    : BOOL := FALSE;
    bH2Cross_ChA_Isolated               : BOOL := FALSE;
    bH2Cross_ChB_Isolated               : BOOL := FALSE;
    bH2Cross_ChC_Isolated               : BOOL := FALSE;
    bO2Cross_ChA_Isolated               : BOOL := FALSE;
    bO2Cross_ChB_Isolated               : BOOL := FALSE;
    bO2Cross_ChC_Isolated               : BOOL := FALSE;
    bAnodePress_ChA_Isolated            : BOOL := FALSE;
    bAnodePress_ChB_Isolated            : BOOL := FALSE;
    bAnodePress_ChC_Isolated            : BOOL := FALSE;
    bCathodePress_ChA_Isolated          : BOOL := FALSE;
    bCathodePress_ChB_Isolated          : BOOL := FALSE;
    bCathodePress_ChC_Isolated          : BOOL := FALSE;
    bCoolingInlet_ChA_Isolated          : BOOL := FALSE;
    bCoolingInlet_ChB_Isolated          : BOOL := FALSE;
    bCoolingInlet_ChC_Isolated          : BOOL := FALSE;
    bCoolingOutlet_ChA_Isolated         : BOOL := FALSE;
    bCoolingOutlet_ChB_Isolated         : BOOL := FALSE;
    bCoolingOutlet_ChC_Isolated         : BOOL := FALSE;
    bDI_Flow_ChA_Isolated               : BOOL := FALSE;
    bDI_Flow_ChB_Isolated               : BOOL := FALSE;
    bDI_Flow_ChC_Isolated               : BOOL := FALSE;
    bConductivity_ChA_Isolated          : BOOL := FALSE;
    bConductivity_ChB_Isolated          : BOOL := FALSE;
    bConductivity_ChC_Isolated          : BOOL := FALSE;
    bTSA_Bed1_ChA_Isolated              : BOOL := FALSE;
    bTSA_Bed1_ChB_Isolated              : BOOL := FALSE;
    bTSA_Bed1_ChC_Isolated              : BOOL := FALSE;
    bTSA_Bed2_ChA_Isolated              : BOOL := FALSE;
    bTSA_Bed2_ChB_Isolated              : BOOL := FALSE;
    bTSA_Bed2_ChC_Isolated              : BOOL := FALSE;
    bDewpoint_ChA_Isolated              : BOOL := FALSE;
    bDewpoint_ChB_Isolated              : BOOL := FALSE;
    bDewpoint_ChC_Isolated              : BOOL := FALSE;

    (* ========================================================================================= *)
    (* 4. ELECTROCHEMICAL & OBSERVER INTERNAL REGISTERS                                          *)
    (* ========================================================================================= *)
    rCalc_AbsoluteTemp_K                : REAL := 343.15;   (* Absolute Core Electrolyzer Temperature [K] *)
    rCalc_NernstPotential_V             : REAL := 1.252;    (* Thermodynamic Reversible Nernst Voltage [V] *)
    rCalc_AnodeOverpotential_V          : REAL := 0.350;    (* Anode Oxygen Evolution Reaction Overpotential [V] *)
    rCalc_CathodeOverpotential_V        : REAL := 0.085;    (* Cathode Hydrogen Evolution Reaction Overpotential [V] *)
    rCalc_ProtonConductivity_S_cm       : REAL := 0.118;    (* Nafion 117 Specific Ionic Conductivity [S/cm] *)
    rCalc_MembraneAreaResistance_Ohmcm2 : REAL := 0.148;    (* Area-Specific Ohmic Resistance [Ohm*cm2] *)
    rCalc_OhmicOverpotential_V          : REAL := 0.296;    (* Total Ohmic Drop Across Polymer Membrane [V] *)
    rCalc_SingleCellVoltage_V           : REAL := 1.983;    (* Computed Polarization Cell Voltage [V] *)
    rCalc_FaradaicEfficiency            : REAL := 0.985;    (* Current Utilization Faradaic Efficiency [0..1] *)
    rCalc_H2CrossoverFlux_mol_cm2_s     : REAL := 0.0;      (* Fickian Diffusive Hydrogen Flux [mol/(cm2*s)] *)
    rCalc_O2ProductionFlux_mol_cm2_s    : REAL := 0.0;      (* Faradaic Anode Oxygen Generation Flux [mol/(cm2*s)] *)
    rCalc_H2inO2_Predicted_pct          : REAL := 0.42;     (* Observer Predicted Hydrogen-in-Oxygen Concentration [% vol] *)
    rCalc_LumpedHeatGeneration_kW       : REAL := 0.0;      (* Total Exothermic Waste Heat Generation [kW] *)

    (* ========================================================================================= *)
    (* 5. 20-STACK POWER SPLITTING & RENEWABLE TRACKING INTERNALS                               *)
    (* ========================================================================================= *)
    rFilteredTargetPower_MW             : REAL := 50.0;     (* Slew-Rate Limited Renewable Power Reference [MW] *)
    rActiveStacksCount                  : REAL := 20.0;     (* Number of Uninhibited Online Stacks *)
    rTotalDispatchWeight                : REAL := 20.0;     (* Sum of Individual Health Dispatch Weights *)
    aStackDispatchWeight                : ARRAY[1..20] OF REAL; (* Health, Temperature & Degradation Dispatch Weights *)
    aStackCurrentDensity_A_cm2          : ARRAY[1..20] OF REAL; (* Actual Operating Current Density per Stack [A/cm2] *)
    aStackCellVoltage_Calc              : ARRAY[1..20] OF REAL; (* Model Estimated Single Cell Voltage per Stack [V] *)
    aStackWasteHeat_kW                  : ARRAY[1..20] OF REAL; (* Individual Stack Thermal Dissipation [kW] *)
    rMinStackTurndownPower_MW           : REAL := 0.250;    (* 5.0% Minimum Load Turndown Limit per 5 MW Stack [MW] *)

    (* ========================================================================================= *)
    (* 6. FINITE STATE MACHINE (FSM) SEQUENCE REGISTERS & TIMERS                                 *)
    (* ========================================================================================= *)
    iFSM_State                          : INT := 10;        (* Primary Operational State Index [10..120] *)
    iNextFSM_State                      : INT := 10;        (* State Transition Target Register *)
    iPrevFSM_State                      : INT := 10;        (* Prior Cycle State History *)
    rStateTimer_s                       : REAL := 0.0;      (* Active State Dwell Execution Timer [s] *)
    rTotalOperatingTimer_h              : REAL := 0.0;      (* Cumulative Facility Operating Lifetime [h] *)

    (* State Specific Timers *)
    rFillCirculationTimer_s             : REAL := 0.0;      (* DI Water Fill and Degas Stabilization Timer [s] *)
    rHydrationSoakTimer_s               : REAL := 0.0;      (* Membrane Polymer Soak & Warm-Up Timer [s] *)
    rPressurizeRampTimer_s              : REAL := 0.0;      (* Dual-Header Equalization Ramp Timer [s] *)
    rMinLoadStartTimer_s                : REAL := 0.0;      (* 5% Turndown Polarization Ignition Timer [s] *)
    rDeenergizationRampTimer_s          : REAL := 0.0;      (* Controlled Shutdown Ramp Timer [s] *)
    rN2FlushStandbyTimer_s              : REAL := 0.0;      (* Inert Nitrogen Blanket Flush Timer [s] *)
    rEStopVentTimer_s                   : REAL := 0.0;      (* Emergency Fast Depressurization Hold Timer [s] *)
    rCrossoverDerateTimer_s             : REAL := 0.0;      (* Crossover Gas Safety Derate Hold Timer [s] *)

    (* ========================================================================================= *)
    (* 7. TSA DEOXO / DUAL-BED SWING REGENERATION INTERNAL REGISTERS                             *)
    (* ========================================================================================= *)
    iTSA_Step                           : INT := 1;         (* 1=Bed1 Adsorb / Bed2 Regen, 2=Switchover, 3=Bed2 Adsorb / Bed1 Regen *)
    rTSA_CycleTimer_s                   : REAL := 0.0;      (* Active Half-Cycle Swing Timer [s] *)
    c_rTSA_HalfCycleDuration_s          : REAL := 14400.0;  (* 4.0-Hour Adsorption Dwell Half-Cycle [s] *)
    c_rTSA_DesorptionHeatingTime_s      : REAL := 7200.0;   (* 2.0-Hour Electric Thermal Desorption Phase [s] *)
    c_rTSA_CoolingPurgeTime_s           : REAL := 5400.0;   (* 1.5-Hour Dry Product Slip Cooling Phase [s] *)
    c_rTSA_RepressurizeTime_s           : REAL := 1800.0;   (* 0.5-Hour Controlled Re-Pressurization Phase [s] *)

    (* ========================================================================================= *)
    (* 8. ISA-18.2 PROCESS ALARM THRESHOLDS, DEADBANDS & RATE-OF-CHANGE REGISTERS               *)
    (* ========================================================================================= *)
    (* Gas Permeation Cross-Over Limits *)
    c_rH2Cross_Trip_HI_HI               : REAL := 2.00;     (* Critical Catastrophic LFL Safety Trip [% vol] *)
    c_rH2Cross_Alarm_HI                 : REAL := 1.50;     (* Mandatory Power Derate Hold Warning [% vol] *)
    c_rH2Cross_Deadband                 : REAL := 0.08;     (* Hysteresis Clearance Band [% vol] *)
    c_rH2Cross_Max_ROC                  : REAL := 0.25;     (* Rate-of-Change Trip Limit 0.25 %/s [% vol/s] *)

    (* Membrane Differential Pressure Limits *)
    c_rDP_Trip_HI_HI                    : REAL := 0.250;    (* Critical Membrane Burst Overpressure Trip [bar] *)
    c_rDP_Alarm_HI                      : REAL := 0.050;    (* Cell Differential High Alarm [bar] *)
    c_rDP_Alarm_LO                      : REAL := -0.050;   (* Cell Differential Low Alarm [bar] *)
    c_rDP_Trip_LO_LO                    : REAL := -0.250;   (* Critical Reverse Differential Pressure Trip [bar] *)
    c_rDP_Deadband                      : REAL := 0.010;    (* Differential Pressure Hysteresis [bar] *)

    (* Stack Operating Core Temperature Limits *)
    c_rStackTemp_Trip_HI_HI             : REAL := 85.0;     (* Membrane Polymer Thermal Degradation Trip [deg C] *)
    c_rStackTemp_Alarm_HI               : REAL := 75.0;     (* High Temperature Cooling Demand Warning [deg C] *)
    c_rStackTemp_Alarm_LO               : REAL := 55.0;     (* Low Operating Temperature Efficiency Warning [deg C] *)
    c_rStackTemp_Trip_LO_LO             : REAL := 40.0;     (* Cold Stack Polarization Freeze Trip [deg C] *)
    c_rStackTemp_Deadband               : REAL := 1.0;      (* Temperature Clearance Hysteresis [deg C] *)

    (* Anode DI Water Quality Electrical Conductivity Limits *)
    c_rConductivity_Trip_HI_HI          : REAL := 0.200;    (* MEA Catalyst Poisoning Fast Trip [uS/cm] *)
    c_rConductivity_Alarm_HI            : REAL := 0.100;    (* Mixed-Bed Demineralizer Exhaustion Warning [uS/cm] *)
    c_rConductivity_Deadband            : REAL := 0.015;    (* Conductivity Hysteresis [uS/cm] *)

    (* Rate-of-Change Prior Registers *)
    rPrev_H2Cross                       : REAL := 0.42;
    rPrev_DP                            : REAL := 0.030;
    rPrev_StackTemp                     : REAL := 70.0;
    rROC_H2Cross                        : REAL := 0.0;
    rROC_DP                             : REAL := 0.0;
    rROC_StackTemp                      : REAL := 0.0;

    (* Latched Alarm Booleans *)
    bAlarm_H2Cross_HI_HI                : BOOL := FALSE;
    bAlarm_H2Cross_HI                   : BOOL := FALSE;
    bAlarm_H2Cross_ROC                  : BOOL := FALSE;
    bAlarm_DP_HI_HI                     : BOOL := FALSE;
    bAlarm_DP_HI                        : BOOL := FALSE;
    bAlarm_DP_LO                        : BOOL := FALSE;
    bAlarm_DP_LO_LO                     : BOOL := FALSE;
    bAlarm_StackTemp_HI_HI              : BOOL := FALSE;
    bAlarm_StackTemp_HI                 : BOOL := FALSE;
    bAlarm_StackTemp_LO                 : BOOL := FALSE;
    bAlarm_StackTemp_LO_LO              : BOOL := FALSE;
    bAlarm_Conductivity_HI_HI           : BOOL := FALSE;
    bAlarm_Conductivity_HI              : BOOL := FALSE;
    bAlarm_Dewpoint_HI                  : BOOL := FALSE;
    bAlarm_TMR_Degraded                 : BOOL := FALSE;

    (* ========================================================================================= *)
    (* 9. TEMPORARY SCRATCHPAD ITERATORS & CALCULATION VARIABLES                                 *)
    (* ========================================================================================= *)
    iIdx                                : INT := 1;
    jIdx                                : INT := 1;
    kIdx                                : INT := 1;
    rDiff12                             : REAL := 0.0;
    rDiff23                             : REAL := 0.0;
    rDiff13                             : REAL := 0.0;
    bAgree12                            : BOOL := FALSE;
    bAgree23                            : BOOL := FALSE;
    bAgree13                            : BOOL := FALSE;
    rTempSum                            : REAL := 0.0;
    rDeltaPowerDemand                   : REAL := 0.0;
    rAllocatedStackPower                : REAL := 0.0;
    rSpecificStackCurrent               : REAL := 0.0;
END_VAR
"""
