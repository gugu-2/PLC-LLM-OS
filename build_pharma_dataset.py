import os
import sys
import json
import uuid

# Define the user prompt exactly as specified
USER_PROMPT = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Pharmaceutical Lyophilization & Sterile Freeze Drying (Tier 1 Priority Sector): Commercial Production Lyophilizer (150,000 Vials / 50 m2 Shelf Area) with 2-Stage Cascade Screw Compressor Refrigeration Skid (-55 °C to +60 °C), Heated Capacitance Manometer vs Pirani Sublimation Endpoint Detection, Manometric Temperature Measurement (MTM) & Cake Collapse Margin (Tc - Tp), and Hydraulic Shelf Stoppering Compression Load Cell Control (0 to 250 kN).**

**Function Block Name**: `FB_Pharma_Lyophilizer_FreezeDrying_VacuumEndpoint`

**Engineering Context & Operational Architecture**:
1. Thermal Fluid Circulation Skid & 2-Stage Refrigeration Cascade:
   - 50 m2 usable shelf area (10 to 14 stacked hollow stainless steel shelves, 316L, mirror polished Ra < 0.4 um).
   - Silicone oil thermal fluid (Syltherm XLT / Dowfrost) circulated at 120 m3/h with variable speed magnetic drive pumps.
   - 2-stage economized screw refrigeration compressor package operating on ultra-low GWP refrigerant (R449A/R507/CO2) delivering shelf temperatures from -55 °C to +60 °C with +/- 0.5 °C spatial uniformity across all shelves.
   - Plate heat exchangers with modulating electric trim heaters (120 kW) and refrigeration expansion valves for tight ramp rate control (+/- 0.1 °C/min to +/- 2.0 °C/min).
2. Deep Vacuum Pumping Skid & Dual-Transducer Endpoint Detection:
   - Dry claw / screw backing vacuum pumps backed by Roots booster blower achieving ultimate blank-off pressure < 0.005 mbar.
   - Dual-transducer vacuum instrumentation: Heated Capacitance Manometers (MKS Baratron 100 °C sensor head, 0.001 to 10 mbar absolute, gas-independent) and Pirani thermal conductivity vacuum gauges (Pirani reads ~1.6x higher than true pressure in 100% water vapor due to higher thermal conductivity of H2O vs N2).
   - Ratio P_Pirani / P_Baratron provides continuous sublimation front monitoring, converging from ~1.60 down to 1.00 +/- 0.02 as primary drying terminates and chamber gas transitions from pure water vapor to sterile nitrogen.
3. Manometric Temperature Measurement (MTM) & Pressure Rise Analysis (PRA):
   - High-speed main chamber isolation spool valve (DN500 butterfly valve closing in < 0.8 s) enables periodic 15-30 second pressure rise tests during primary drying.
   - Non-linear least squares fit of pressure rise curve P(t) = P_eq - (P_eq - P0) * exp(-t/tau) + C_leak * t to determine ice interface temperature Ti, cake dry layer mass transfer resistance Rp, and cake collapse safety margin Delta_T_collapse = T_collapse - Ti.
   - Dynamic shelf heating temperature clamp preventing product cake melting or amorphous collapse (micro-collapse threshold Tc = -28.5 °C to -32.0 °C for typical monoclonal antibodies / vaccine formulations).
4. Hydraulic Shelf Compression & Stoppering Force Uniformity:
   - Central hydraulic cylinder with proportional directional servo valve, position linear transducer (0-1500 mm), and triple modular redundant (2oo3 TMR) compression load cells (0-250 kN).
   - Uniform vial stoppering under partial vacuum (800 mbar N2 backfill) to seat 150,000 rubber stoppers into 2R/10R glass vials with controlled compression ramp (0 to 180 kN) and mechanical force equalization preventing vial neck breakage.
5. 8-State Cyber-Physical Discrete State-Space Model (x_{k+1} = A x_k + B u_k + E d_k):
   - 8 states:
     x1: Mean shelf silicone oil circulating temperature [deg C]
     x2: Sublimation ice interface / product cake temperature [deg C]
     x3: Lyophilization chamber absolute pressure (Capacitance Manometer) [mbar]
     x4: Condenser coil ice surface accretion thickness [mm]
     x5: Primary drying sublimation water vapor mass flow rate [kg/h]
     x6: Secondary drying residual product cake moisture content [%]
     x7: Hydraulic shelf stoppering compression force [kN]
     x8: Sterile nitrogen chamber leak-rate / micro-bleed flow rate [m3/h]
   - 8 control inputs:
     u1: Silicone oil electric heater modulating duty [%]
     u2: Refrigeration cascade expansion valve modulating duty [%]
     u3: Vacuum Roots booster VFD frequency [%]
     u4: Sterile nitrogen micro-bleed dosing piezo valve command [%]
     u5: Chamber main isolation valve command [0/1]
     u6: Hydraulic stoppering proportional servo pressure command [%]
     u7: Condenser refrigeration expansion valve duty [%]
     u8: Chamber sterile aeration break valve command [%]
6. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) balancing shelf temperature trajectory tracking, chamber pressure stability, sublimation rate maximization, cake collapse temperature margin, and smooth actuator slew.
   - Fast Projected Gradient Descent (PGD) solver with physical box saturation [0, 100%] and slew rate clamping.
7. Deterministic 14-Stage Production Finite State Machine (FSM):
   - Stage 0: Standby / System Purge
   - Stage 1: Clean-In-Place / Steam-In-Place (CIP/SIP, 121.1 °C, 2.1 bar steam soak, WFI wash)
   - Stage 2: Aseptic Vial Loading (Isolator interface, shelf hold at +5.0 °C, spacing 70 mm)
   - Stage 3: Atmospheric Freezing (-45.0 °C soak at -0.5 °C/min ramp, ice nucleation annealing)
   - Stage 4: Condenser Chill-Down (Condenser coil to -75.0 °C, isolation valve closed)
   - Stage 5: Primary Drying Vacuum Pull-Down (Roughing + booster down to 0.100 mbar)
   - Stage 6: Primary Drying Sublimation Ramp (Shelf to -15.0 °C, N2 micro-bleed at 0.080-0.120 mbar)
   - Stage 7: Manometric Endpoint Verification (MTM valve pulse, Baratron/Pirani ratio check < 1.03)
   - Stage 8: Secondary Desorption Heating Ramp (Shelf ramp to +25.0 °C at +0.2 °C/min)
   - Stage 9: Secondary Drying Isothermal Soak (+25.0 °C hold, < 0.015 mbar, moisture < 1.0%)
   - Stage 10: Sterile Nitrogen Backfill (Controlled backfill to 800 mbar with 0.22 um filtered N2)
   - Stage 11: Hydraulic Stoppering Compaction (0 to 180 kN ramp, uniform vial stoppering)
   - Stage 12: Aeration Vacuum Break (Vent to 1013 mbar atmospheric with sterile air/N2)
   - Stage 13: Aseptic Vial Unload (Sub-door open, shelf expansion to 110 mm, auto-unloader push)
   - Stage 14: Emergency Abort Defrost & Safe Vent (Refrigeration safe shutdown, steam defrost)
8. ISA-18.2 Multi-Tiered Alarms & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low, and Rate-of-Change trips with clearance hysteresis and 32-bit status/diagnostic words.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Pharma_Lyophilizer_FreezeDrying_VacuumEndpoint` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

print("User prompt prepared. Size:", len(USER_PROMPT))

def generate_st_code():
    parts = []

    # 1. Opening FUNCTION_BLOCK declaration & Engineering Treatise Header
    header = """FUNCTION_BLOCK FB_Pharma_Lyophilizer_FreezeDrying_VacuumEndpoint
(*
========================================================================================================================
  LUMINA AI CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  CRITICAL PHARMACEUTICAL MANUFACTURING REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION : COMMERCIAL PRODUCTION FREEZE DRYER (LYOPHILIZER) WITH SUBLIMATION ENDPOINT DETECTION
  APPARATUS GEOMETRY : 50.0 M2 TOTAL USABLE SHELF SURFACE AREA (10 TO 14 HOLLOW STAINLESS STEEL SHELVES, 316L)
  BATCH CAPACITY     : UP TO 150,000 STERILE INJECTABLE VIALS (2R / 10R DIN GLASS VIALS, LIQUID FILL 1.0 TO 5.0 ML)
  REFRIGERATION SKID : 2-STAGE SCREW COMPRESSOR CASCADE PACKAGE WITH ECONOMIZER (-55.0 DEG C TO +60.0 DEG C)
  THERMAL FLUID      : SYLTHERM XLT / POLYSILOXANE HEAT TRANSFER OIL CIRCULATED AT 120.0 M3/H VIA DUAL VFD PUMPS
  VACUUM INSTRUMENT  : HEATED CAPACITANCE MANOMETER (MKS BARATRON 100 DEG C) VS PIRANI THERMAL GAUGES (2oo3 TMR)
  PROCESS ANALYTICAL : MANOMETRIC TEMPERATURE MEASUREMENT (MTM) & PRESSURE RISE ANALYSIS (PRA) SUBLIMATION ENDPOINT
  STOPPERING SYSTEM  : HYDRAULIC SHELF COMPACTION CROSSHEAD (0 TO 250 KN) WITH LOAD CELL EQUALIZATION CONTROL
  APPLICABLE NORMS   : FDA 21 CFR PART 11 (ELECTRONIC RECORDS/SIGNATURES), EU GMP ANNEX 1 (STERILE MEDICINAL PRODUCTS),
                       ASME BPE-2022 (BIOPROCESSING EQUIPMENT), GAMP 5 REVISION 2 (VALIDATION OF AUTOMATED SYSTEMS),
                       ISA-18.2 / IEC 62682 (MANAGEMENT OF ALARM SYSTEMS), IEC 61508 / IEC 61511 (SIL-2 INTEGRITY),
                       DIN EN 285 (STEAM STERILIZATION), ISO 13408-3 (ASEPTIC PROCESSING - FREEZE-DRYING).
  AUTHOR             : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL & CYBER-PHYSICAL THERMODYNAMIC FOUNDATIONS:
  ----------------------------------------------------------------------------------------------------------------------
  1. HEAT AND MASS TRANSFER DYNAMICS IN LYOPHILIZATION (PRIMARY DRYING SUBLIMATION):
     - Lyophilization is a non-equilibrium transient sublimative separation process wherein frozen solvent (typically water)
       sublimates directly from the solid ice state to the vapor phase under deep vacuum, avoiding liquid-phase meniscus
       surface tension forces that would otherwise collapse delicate protein tertiary/quaternary structures.
     - Heat flux q [W/m2] transferred from the heat transfer fluid inside the hollow shelf plate into the vial base
       and upward across the frozen ice core to the sublimating front is governed by conjugate heat transfer modes:
           q_in = K_v * (T_shelf - T_vial_base) = (k_ice / delta_ice) * (T_vial_base - T_i) = Delta_H_sub * m_dot_sub
       where:
           K_v         = Overall vial heat transfer coefficient [W/(m2 * K)]
           k_ice       = Thermal conductivity of frozen amorphous/crystalline ice matrix (~2.21 W/(m * K) at -30 deg C)
           delta_ice   = Thickness of remaining frozen product core [m]
           T_shelf     = Circulating silicone oil bulk shelf temperature [deg C]
           T_vial_base = Exterior glass bottom surface temperature of the DIN injection vial [deg C]
           T_i         = Sublimation ice-front interface temperature [deg C]
           Delta_H_sub = Latent heat of ice sublimation (~2.84e6 J/kg at -25 deg C)
           m_dot_sub   = Area-normalized sublimation mass flux rate [kg/(m2 * s)]

     - In the low-pressure rarefied gas regime (0.040 to 0.500 mbar), the Knudsen number Kn = lambda_mfp / l_gap
       spans the transitional flow regime (0.1 < Kn < 10). The effective heat transfer coefficient K_v exhibits
       a strong non-linear dependence on chamber absolute pressure P_ch:
           K_v(P_ch) = K_contact + (alpha_acc * Lambda_0 * P_ch) / (1 + alpha_acc * Lambda_0 * P_ch * (l_gap / k_gas)) + K_rad
       where:
           K_contact = Direct solid-to-solid conduction between shelf surface asperities and vial glass bottom rim (~5-10 W/m2-K)
           Lambda_0  = Free molecular gas heat conductivity factor (~1.19 W/(m2 * K * mbar) for dry nitrogen)
           alpha_acc = Thermal accommodation coefficient of nitrogen on 316L mirror polish stainless steel (~0.85)
           l_gap     = Effective concave bottom curvature standoff gap of standard 2R/10R tubing vials (~0.05 to 0.20 mm)
           K_rad     = Radiative exchange coefficient sigma_SB * epsilon_v * (T_sh^2 + T_v^2) * (T_sh + T_v) (~2-5 W/m2-K)

  2. VAPOR MASS TRANSPORT & PRODUCT CAKE DRY LAYER HYDRAULIC RESISTANCE (R_p):
     - Water vapor molecules sublimating from the receding ice front must diffuse through the porous tortuous channels
       of the dried product cake matrix before entering the chamber headspace.
     - The mass flow rate m_dot_sub [kg/s] per vial is modeled by Darcy's law modified for rarefied gas diffusion:
           m_dot_sub = (A_vial / R_p) * (P_i(T_i) - P_ch)
       where:
           A_vial = Cross-sectional area of vial product cake [m2]
           P_ch   = Lyophilization chamber absolute total pressure measured by Baratron capacitance manometer [mbar]
           P_i    = Saturated equilibrium vapor pressure of pure ice at sublimation front interface temperature T_i [mbar]
                    P_i(T_i) = 10^(10.5553 - (2667.0 / (T_i + 273.15)))  [Clausius-Clapeyron equation for ice]
           R_p    = Hydraulic resistance of the dried product cake layer [mbar * m2 * s / kg]
     - As sublimation progresses, the dried cake layer thickness L_dry increases from 0 to total fill depth L_total,
       causing product dry layer resistance R_p to increase dynamically:
           R_p(L_dry) = R_p0 + (A_res1 * L_dry) / (1.0 + A_res2 * L_dry)
       where R_p0 is the initial micro-porous crust resistance and A_res1, A_res2 capture structure tortuosity.

  3. CRITICAL CAKE COLLAPSE MARGIN (T_collapse - T_i) & PRODUCT INTEGRITY:
     - Biologics, monoclonal antibodies (mAbs), mRNA lipid nanoparticles, and vaccine formulations contain amorphous
       lyoprotectants (e.g. sucrose, trehalose, mannitol).
     - If the sublimation interface temperature T_i exceeds the formulation critical collapse threshold T_collapse
       (or glass transition temperature of maximally freeze-concentrated solution Tg'):
           T_i > T_collapse
       the product cake suffers catastrophic microscopic structural collapse. Collapse results in:
       * Loss of porous cake specific surface area (crumbling into a dense vitreous glassy mass)
       * Exponential spike in dried cake resistance R_p (choking sublimation vapor flow)
       * Retarded secondary drying rate, high residual moisture (> 3%), and irreversible protein denaturation/aggregation.
     - Therefore, the advanced Model Predictive Control (MPC) algorithm enforces a strict dynamic state constraint:
           Delta_T_collapse_margin = T_collapse - T_i >= +2.50 deg C  (Safety Margin Clamp)

  4. DUAL-TRANSDUCER SUBLIMATION ENDPOINT DETECTION (BARATRON VS PIRANI RATIO):
     - Capacitance Manometers (MKS Baratron) measure true absolute mechanical pressure (P_true = Force / Area)
       independently of gas molecular composition or chemical species via diaphragm elastic deflection.
     - Thermal Pirani Vacuum Gauges infer pressure from thermal heat dissipation across an electrically heated wire filament.
     - In the primary drying phase, chamber gas consists of ~99.5% pure sublimated water vapor (H2O, molecular weight 18 g/mol).
       Because the thermal conductivity of low-pressure water vapor is ~1.6 times higher than that of nitrogen (N2, 28 g/mol),
       a Pirani gauge calibrated for dry nitrogen reports an apparent pressure approximately 60% higher than true pressure:
           P_Pirani / P_Baratron ~= 1.55 to 1.65  (Active Sublimation Regime)
     - As the sublimating ice front recedes to the bottom of all 150,000 vials, the water vapor flux drops sharply to zero.
       The chamber gas composition shifts smoothly from 100% water vapor to 100% sterile nitrogen carrier gas:
           lim_{m_dot_sub -> 0} (P_Pirani / P_Baratron) = 1.000 +/- 0.025  (Sublimation Endpoint Crossover)
     - This physical crossover ratio provides a continuous, non-invasive, batch-wide sublimation front endpoint indicator.

  5. MANOMETRIC TEMPERATURE MEASUREMENT (MTM) & PRESSURE RISE ANALYSIS (PRA):
     - To verify the exact product temperature T_i without invasive thermocouples in every vial, the DN500 main isolation
       spool valve connecting chamber to condenser is rapidly closed for 25.0 seconds.
     - The instantaneous rate of pressure rise P_ch(t) during the first 25 seconds of isolation follows:
           P_ch(t) = P_eq - (P_eq - P_0) * exp(-t / tau_mtm) + C_leak * t
       where:
           P_0     = Chamber pressure at t = 0 s (valve shut instant) [mbar]
           P_eq    = Equilibrium vapor pressure of ice at sublimation front [mbar]
           tau_mtm = Time constant of pressure rise governing vapor saturation in chamber headspace [s]
           C_leak  = Steady-state background leak rate of the hermetic chamber envelope [mbar / s]
     - By inverting Clausius-Clapeyron equation using fitted P_eq:
           T_i_MTM = 2667.0 / (10.5553 - log10(P_eq)) - 273.15  [deg C]
     - This gives the exact, spatially averaged sublimation interface temperature across all 150,000 production vials!

  6. HYDRAULIC SHELF COMPACTION & STOPPERING LOAD DISTRIBUTION:
     - Following secondary drying and sterile N2 backfill to 800 mbar, the hydraulic shelf compression cylinder
       drives the shelf stack downward to compress and seat 150,000 bromobutyl rubber stoppers into the vial necks.
     - Required total hydraulic stoppering force F_stop [kN]:
           F_stop = (N_vials * F_stopper_seal) + F_shelf_deadweight + F_bellows_resistance
       where:
           N_vials            = 150,000 vials
           F_stopper_seal     = Seating force per stopper (~1.0 to 1.5 N per 13/20 mm vial stopper)
           F_shelf_deadweight = Cumulative weight of 12 stainless steel shelf assemblies (~45 kN)
           F_total_target     = 150 kN to 220 kN controlled compaction profile.
     - Uniformity across 50 m2 is paramount: uneven force breaks glass vial necks or yields unseated stoppers,
       breaching container closure integrity (CCI) per USP <1207>.
*)
"""
    parts.append(header)

    # 2. VAR_INPUT block
    var_input = """VAR_INPUT
    (* ========================================================================================================= *)
    (* PRIMARY THERMAL FLUID SKID & SILICONE OIL TEMPERATURE TRANSDUCERS (2oo3 TMR Pt100 RTD SENSORS)            *)
    (* ========================================================================================================= *)
    rShelf_Oil_Inlet_Temp_RTD_A           : REAL; (* Silicone oil circulating header inlet temperature RTD channel A [deg C] *)
    rShelf_Oil_Inlet_Temp_RTD_B           : REAL; (* Silicone oil circulating header inlet temperature RTD channel B [deg C] *)
    rShelf_Oil_Inlet_Temp_RTD_C           : REAL; (* Silicone oil circulating header inlet temperature RTD channel C [deg C] *)
    rShelf_Oil_Outlet_Temp_RTD_A          : REAL; (* Silicone oil circulating header return temperature RTD channel A [deg C] *)
    rShelf_Oil_Outlet_Temp_RTD_B          : REAL; (* Silicone oil circulating header return temperature RTD channel B [deg C] *)
    rShelf_Oil_Outlet_Temp_RTD_C          : REAL; (* Silicone oil circulating header return temperature RTD channel C [deg C] *)

    (* ========================================================================================================= *)
    (* REPRESENTATIVE PRODUCT VIAL SUBLIMATION THERMOCOUPLES (2oo3 TMR THIN-WIRE T-TYPE / Pt100 SENSORS)         *)
    (* ========================================================================================================= *)
    rProduct_Vial_Temp_TC_A               : REAL; (* Center shelf monitored vial product ice core temperature channel A [deg C] *)
    rProduct_Vial_Temp_TC_B               : REAL; (* Edge shelf monitored vial product ice core temperature channel B [deg C] *)
    rProduct_Vial_Temp_TC_C               : REAL; (* Corner shelf monitored vial product ice core temperature channel C [deg C] *)

    (* ========================================================================================================= *)
    (* LYOPHILIZATION CHAMBER VACUUM INSTRUMENTATION (2oo3 TMR HEATED CAPACITANCE MANOMETERS & PIRANI GAUGES)    *)
    (* ========================================================================================================= *)
    rChamber_Baratron_Press_A             : REAL; (* MKS Baratron 100 deg C heated capacitance manometer pressure channel A [mbar] *)
    rChamber_Baratron_Press_B             : REAL; (* MKS Baratron 100 deg C heated capacitance manometer pressure channel B [mbar] *)
    rChamber_Baratron_Press_C             : REAL; (* MKS Baratron 100 deg C heated capacitance manometer pressure channel C [mbar] *)
    rChamber_Pirani_Press_A               : REAL; (* Wide-range thermal conductivity Pirani vacuum gauge channel A [mbar] *)
    rChamber_Pirani_Press_B               : REAL; (* Wide-range thermal conductivity Pirani vacuum gauge channel B [mbar] *)
    rChamber_Pirani_Press_C               : REAL; (* Wide-range thermal conductivity Pirani vacuum gauge channel C [mbar] *)

    (* ========================================================================================================= *)
    (* ICE CONDENSER SKID & REFRIGERATION COIL TRANSDUCERS (2oo3 TMR SURFACE RTDS & VACUUM TRANSDUCER)          *)
    (* ========================================================================================================= *)
    rCondenser_Coil_Temp_RTD_A            : REAL; (* Refrigeration condenser serpentine tube surface temperature RTD channel A [deg C] *)
    rCondenser_Coil_Temp_RTD_B            : REAL; (* Refrigeration condenser serpentine tube surface temperature RTD channel B [deg C] *)
    rCondenser_Coil_Temp_RTD_C            : REAL; (* Refrigeration condenser serpentine tube surface temperature RTD channel C [deg C] *)
    rCondenser_Chamber_Press              : REAL; (* Condenser chamber spool independent wide-range vacuum transducer [mbar] *)

    (* ========================================================================================================= *)
    (* HYDRAULIC SHELF COMPACTION & STOPPERING SENSORS (2oo3 TMR CROSSHEAD COMPRESSION LOAD CELLS & LVDT)        *)
    (* ========================================================================================================= *)
    rStoppering_Load_Cell_Force_A         : REAL; (* Hydraulic crosshead compression load cell sensor channel A [kN] *)
    rStoppering_Load_Cell_Force_B         : REAL; (* Hydraulic crosshead compression load cell sensor channel B [kN] *)
    rStoppering_Load_Cell_Force_C         : REAL; (* Hydraulic crosshead compression load cell sensor channel C [kN] *)
    rShelf_Hydraulic_Position_LVDT        : REAL; (* Hydraulic cylinder linear displacement position transducer [mm] *)

    (* ========================================================================================================= *)
    (* UTILITY SUPPLIES, PUMP HYDRAULICS, AND STERILE BOUNDARY PROCESS PRESSURES                                  *)
    (* ========================================================================================================= *)
    rSilicone_Oil_Circ_Flow               : REAL; (* Silicone oil circulating skid electromagnetic flowmeter [m3/h] *)
    rSilicone_Oil_Pump_Press              : REAL; (* Silicone oil circulation pump delivery differential pressure [bar] *)
    rNitrogen_Supply_Header_Press         : REAL; (* High-purity sterile gaseous nitrogen (N2) supply header pressure [bar] *)
    rClean_Steam_Supply_Press             : REAL; (* Clean steam generator SIP sanitization header supply pressure [bar] *)
    rWFI_Supply_Press                     : REAL; (* Water-for-Injection CIP spray distribution header pressure [bar] *)
    rRefrig_LowStage_Suction_Press        : REAL; (* Refrigeration cascade low-stage screw booster compressor suction pressure [bar] *)
    rRefrig_HighStage_Disch_Press         : REAL; (* Refrigeration cascade high-stage screw compressor discharge pressure [bar] *)

    (* ========================================================================================================= *)
    (* RECIPE OPERATIONAL TARGET SETPOINTS & PRODUCT CRITICAL QUALITY ATTRIBUTE (CQA) LIMITS                     *)
    (* ========================================================================================================= *)
    rRecipe_Collapse_Temp_Limit           : REAL; (* Critical formulation product cake collapse threshold temperature Tc [deg C] *)
    rRecipe_Freezing_Shelf_Target         : REAL; (* Target shelf temperature setpoint during atmospheric freezing soak [deg C] *)
    rRecipe_Primary_Shelf_Target          : REAL; (* Target shelf temperature setpoint during primary sublimation ramp [deg C] *)
    rRecipe_Primary_Chamber_Press_SP      : REAL; (* Target chamber vacuum setpoint during primary drying sublimation [mbar] *)
    rRecipe_Secondary_Shelf_Target        : REAL; (* Target shelf temperature setpoint during secondary desorption drying [deg C] *)
    rRecipe_Stoppering_Target_Force       : REAL; (* Target total hydraulic shelf stoppering compaction force for 150,000 vials [kN] *)
    rRecipe_Backfill_Target_Press         : REAL; (* Target chamber nitrogen backfill pressure prior to stoppering compression [mbar] *)
    rRecipe_Shelf_Ramp_Rate_Limit         : REAL; (* Maximum allowable shelf thermal ramp rate limit [deg C/min] *)

    (* ========================================================================================================= *)
    (* DISCRETE SAMPLING CLOCK & OPERATOR SUPERVISORY COMMAND SIGNALS                                            *)
    (* ========================================================================================================= *)
    tCycle_Sample_Time_Ts                 : TIME; (* Discrete deterministic scan execution sample interval [s] *)
    bCmd_Cycle_Start                      : BOOL; (* Supervisory batch cycle start trigger command strobe *)
    bCmd_Cycle_Pause                      : BOOL; (* Supervisory cycle pause / hold active state command toggle *)
    bCmd_Cycle_Abort                      : BOOL; (* Operator emergency cycle abort strobe *)
    bCmd_Alarm_Reset                      : BOOL; (* Operator ISA-18.2 alarm acknowledge and trip reset strobe *)
    bCmd_Manual_MTM_Trigger               : BOOL; (* Engineering manual trigger for Pressure Rise Analysis (PRA) pulse *)
    bIsolator_Interlock_Healthy           : BOOL; (* Aseptic containment isolator / RABS barrier door closed and sterile boundary healthy *)
END_VAR
"""
    parts.append(var_input)

    # 3. VAR_OUTPUT block
    var_output = """VAR_OUTPUT
    (* ========================================================================================================= *)
    (* MODULATING ACTUATOR COMMANDS & SYSTEM VALVE POSITIONERS                                                   *)
    (* ========================================================================================================= *)
    rShelf_Electric_Heater_PWM_Duty        : REAL; (* Silicone oil electric trim heater thyristor modulating command [%] *)
    rShelf_Refrig_Expansion_Valve_Duty    : REAL; (* Silicone oil refrigeration plate heat exchanger expansion valve [%] *)
    rCondenser_Refrig_Expansion_Valve_Duty: REAL; (* Condenser coil cascade refrigeration expansion valve command [%] *)
    rVacuum_Roughing_Screw_VFD_Speed      : REAL; (* Dry screw backing vacuum pump variable frequency drive speed [%] *)
    rVacuum_Booster_Roots_VFD_Speed       : REAL; (* Roots booster blower variable frequency drive speed command [%] *)
    bChamber_Isolation_Spool_Valve_Open   : BOOL; (* Main DN500 pneumatic high-vacuum chamber isolation spool valve open command *)
    rNitrogen_MicroBleed_Piezo_Valve_Duty : REAL; (* Sterile nitrogen dosing piezo valve duty for chamber pressure control [%] *)
    bNitrogen_Fast_Backfill_Valve_Open    : BOOL; (* Sterile nitrogen fast backfill pneumatic angle seat valve command *)
    rSterile_Aeration_Break_Valve_Duty    : REAL; (* Chamber sterile atmospheric aeration break modulating valve [%] *)
    rHydraulic_Stoppering_Servo_Valve     : REAL; (* Hydraulic shelf compression proportional servo directional valve command [%] *)
    bHydraulic_Power_Pack_Pump_Run        : BOOL; (* Hydraulic power unit motor starter enable command *)
    rCIP_SIP_Steam_Modulating_Valve       : REAL; (* Clean steam modulating diaphragm control valve command [%] *)
    bCondenser_Defrost_Water_Valve_Open   : BOOL; (* Hot water / steam condenser ice defrost supply valve command *)

    (* ========================================================================================================= *)
    (* VOTED PROCESS VARIABLES & OBSERVER RECONSTRUCTED CYBER-PHYSICAL STATES                                    *)
    (* ========================================================================================================= *)
    rVoted_Shelf_Mean_Temp                : REAL; (* 2oo3 TMR voted bulk shelf silicone oil mean temperature [deg C] *)
    rVoted_Product_Cake_Temp              : REAL; (* 2oo3 TMR voted product vial sublimation ice/cake interface temperature [deg C] *)
    rVoted_Chamber_Baratron_Press         : REAL; (* 2oo3 TMR voted capacitance manometer true absolute chamber pressure [mbar] *)
    rVoted_Chamber_Pirani_Press           : REAL; (* 2oo3 TMR voted thermal Pirani apparent vacuum pressure [mbar] *)
    rVoted_Condenser_Coil_Temp            : REAL; (* 2oo3 TMR voted condenser refrigeration coil surface temperature [deg C] *)
    rVoted_Stoppering_Actual_Force        : REAL; (* 2oo3 TMR voted total hydraulic stoppering compression force [kN] *)
    rSublimation_Endpoint_Pirani_Ratio    : REAL; (* Dual-transducer sublimation ratio Pirani / Baratron [-] *)
    rSublimation_Interface_Temp_MTM       : REAL; (* Manometric temperature measurement estimated ice-front temperature Ti [deg C] *)
    rCake_Collapse_Safety_Margin          : REAL; (* Real-time cake collapse safety margin Tc - Ti [deg C] *)
    rEstimated_Sublimation_Flux           : REAL; (* Estimated instantaneous water vapor sublimation mass flow rate [kg/h] *)
    rEstimated_Ice_Cake_Thickness         : REAL; (* Estimated remaining frozen ice core depth per vial [mm] *)
    rEstimated_Residual_Moisture          : REAL; (* Secondary drying estimated residual cake moisture content [%] *)

    (* ========================================================================================================= *)
    (* FSM CYCLE SEQUENCING, ENDPOINT FLAGS, AND HIGH-INTEGRITY ISA-18.2 ALARMS                                   *)
    (* ========================================================================================================= *)
    iActive_FSM_State_ID                  : INT;  (* Deterministic operational finite state machine active stage identifier *)
    bSublimation_Primary_Endpoint_Active  : BOOL; (* Sublimation front primary drying completion endpoint verified *)
    bBatch_Lyophilization_Complete        : BOOL; (* Overall sterile lyophilization recipe cycle successfully completed *)
    bAlarm_ISA18_Warning_Active           : BOOL; (* ISA-18.2 Priority 2 Process Warning alarm active *)
    bAlarm_ISA18_Critical_Active          : BOOL; (* ISA-18.2 Priority 1 Critical Process alarm active *)
    bAlarm_ISA18_Emergency_Trip           : BOOL; (* ISA-18.2 Priority 0 Safety Emergency Trip active *)
    dwStatus_Word_Subsystems              : DWORD;(* Bit-packed 32-bit status register: Subsystems operational health *)
    dwStatus_Word_TMR_Health              : DWORD;(* Bit-packed 32-bit status register: 2oo3 TMR channel health and degradation *)
    dwAlarm_Word_Process_Trips            : DWORD;(* Bit-packed 32-bit alarm register: Process parameters out of tolerance *)
    dwAlarm_Word_Interlocks               : DWORD;(* Bit-packed 32-bit alarm register: Equipment and sterile boundary interlocks *)
END_VAR
"""
    parts.append(var_output)

    # 4. VAR internal block (Matrices, MPC variables, TMR structures, FSM variables, Alarms)
    var_internal = """VAR
    (* ========================================================================================================= *)
    (* DISCRETE 8-STATE CYBER-PHYSICAL STATE-SPACE MATRICES (Ts = 0.020 s)                                       *)
    (* x[k+1] = A * x[k] + B * u[k] + L * innov[k], y[k] = C * x[k] + D * u[k]                                    *)
    (* x1: Shelf silicone oil temp [deg C]                                                                       *)
    (* x2: Sublimation ice interface temp [deg C]                                                                *)
    (* x3: Lyophilization chamber pressure [mbar]                                                                *)
    (* x4: Condenser coil ice thickness [mm]                                                                     *)
    (* x5: Sublimation mass flux rate [kg/h]                                                                     *)
    (* x6: Secondary residual cake moisture [%]                                                                  *)
    (* x7: Hydraulic shelf stoppering force [kN]                                                                 *)
    (* x8: Chamber sterile nitrogen leak/bleed rate [m3/h]                                                       *)
    (* ========================================================================================================= *)
    mA_Matrix : ARRAY[1..8, 1..8] OF REAL := [
        0.998420,  0.000150, -0.000025,  0.000000, -0.000310,  0.000000,  0.000000,  0.000000,
        0.001250,  0.996800,  0.000840, -0.000015, -0.004200,  0.000000,  0.000000,  0.000000,
       -0.000085,  0.000420,  0.985200, -0.000120,  0.015200,  0.000000,  0.000000,  0.024500,
        0.000000,  0.000018,  0.000045,  0.999980,  0.000082,  0.000000,  0.000000,  0.000000,
        0.000850,  0.002400, -0.006800, -0.000040,  0.982500,  0.000000,  0.000000,  0.000000,
        0.000042,  0.000000,  0.000000,  0.000000,  0.000000,  0.999450,  0.000000,  0.000000,
        0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.992000,  0.000000,
        0.000000,  0.000000,  0.000210,  0.000000,  0.000000,  0.000000,  0.000000,  0.988000
    ];

    mB_Matrix : ARRAY[1..8, 1..8] OF REAL := [
        0.001850, -0.001620,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,
        0.000045, -0.000038,  0.000000,  0.000015,  0.000000,  0.000000,  0.000000,  0.000000,
        0.000000,  0.000000, -0.002450,  0.004120, -0.008500,  0.000000, -0.000450,  0.012500,
        0.000000,  0.000000,  0.000000,  0.000000,  0.000035,  0.000000,  0.000012,  0.000000,
        0.000120, -0.000085, -0.000340,  0.000180,  0.001450,  0.000000,  0.000000,  0.000000,
       -0.000015,  0.000000, -0.000045,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,
        0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.085000,  0.000000,  0.000000,
        0.000000,  0.000000,  0.000000,  0.002850,  0.000000,  0.000000,  0.000000,  0.000000
    ];

    mC_Matrix : ARRAY[1..8, 1..8] OF REAL := [
        1.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,
        0.000000,  1.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,
        0.000000,  0.000000,  1.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,
        0.000000,  0.000000,  0.000000,  1.000000,  0.000000,  0.000000,  0.000000,  0.000000,
        0.000000,  0.000000,  0.000000,  0.000000,  1.000000,  0.000000,  0.000000,  0.000000,
        0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  1.000000,  0.000000,  0.000000,
        0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  1.000000,  0.000000,
        0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  0.000000,  1.000000
    ];

    mD_Matrix : ARRAY[1..8, 1..8] OF REAL := [
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ];

    mL_KalmanGain : ARRAY[1..8, 1..8] OF REAL := [
        0.1850, 0.0012, -0.0004, 0.0000, 0.0002, 0.0000, 0.0000, 0.0000,
        0.0015, 0.2450,  0.0085, 0.0000, 0.0045, 0.0000, 0.0000, 0.0000,
       -0.0008, 0.0062,  0.3120, 0.0000, 0.0185, 0.0000, 0.0000, 0.0145,
        0.0000, 0.0001,  0.0002, 0.0540, 0.0001, 0.0000, 0.0000, 0.0000,
        0.0004, 0.0052, -0.0142, 0.0000, 0.2850, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000,  0.0000, 0.0000, 0.0000, 0.0850, 0.0000, 0.0000,
        0.0000, 0.0000,  0.0000, 0.0000, 0.0000, 0.0000, 0.4500, 0.0000,
        0.0000, 0.0000,  0.0018, 0.0000, 0.0000, 0.0000, 0.0000, 0.1250
    ];

    (* State vectors *)
    rState_Vector_x_k                     : ARRAY[1..8] OF REAL;
    rState_Vector_x_kplus1                : ARRAY[1..8] OF REAL;
    rState_Vector_x_est                   : ARRAY[1..8] OF REAL;
    rControl_Vector_u_k                   : ARRAY[1..8] OF REAL;
    rControl_Vector_u_prev                : ARRAY[1..8] OF REAL;
    rMeas_Vector_y_k                      : ARRAY[1..8] OF REAL;
    rEst_Output_Vector_y_k                : ARRAY[1..8] OF REAL;
    rInnov_Vector                         : ARRAY[1..8] OF REAL;
    rTarget_State_Ref                     : ARRAY[1..8] OF REAL;

    (* ========================================================================================================= *)
    (* RECEDING-HORIZON MPC COST FUNCTION WEIGHTS, CONSTRAINTS & OPTIMIZER BUFFERS                               *)
    (* ========================================================================================================= *)
    rMPC_Q_Weights : ARRAY[1..8] OF REAL := [12.0, 18.0, 25.0, 0.5, 8.0, 15.0, 6.0, 2.0];
    rMPC_R_Weights : ARRAY[1..8] OF REAL := [0.85, 0.95, 1.20, 2.50, 5.00, 0.65, 1.10, 3.00];
    rMPC_S_SlewWeights : ARRAY[1..8] OF REAL := [2.50, 2.80, 3.50, 6.00, 12.00, 1.80, 3.20, 8.00];
    rMPC_P_TerminalWeights : ARRAY[1..8] OF REAL := [24.0, 36.0, 50.0, 1.0, 16.0, 30.0, 12.0, 4.0];

    rActuator_Min_Bounds : ARRAY[1..8] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, -100.0, 0.0, 0.0];
    rActuator_Max_Bounds : ARRAY[1..8] OF REAL := [100.0, 100.0, 100.0, 100.0, 1.0, 100.0, 100.0, 100.0];
    rActuator_Slew_Limits : ARRAY[1..8] OF REAL := [2.5, 3.0, 4.0, 8.0, 1.0, 5.0, 3.5, 10.0];

    rMPC_Pred_States : ARRAY[0..5, 1..8] OF REAL;
    rMPC_Pred_Controls : ARRAY[0..4, 1..8] OF REAL;
    rMPC_Gradient_u : ARRAY[0..4, 1..8] OF REAL;
    rMPC_Cost_J : REAL;
    rMPC_Cost_J_Best : REAL;
    rMPC_Alpha_Step : REAL := 0.0185;

    (* ========================================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING STRUCTURES ACROSS 7 CRITICAL SENSING CHANNELS                 *)
    (* ========================================================================================================= *)
    (* Channel 1: Shelf Inlet RTD *)
    bTMR_Ch1_A_Healthy : BOOL := TRUE;
    bTMR_Ch1_B_Healthy : BOOL := TRUE;
    bTMR_Ch1_C_Healthy : BOOL := TRUE;
    tTMR_Ch1_DiscTimer_AB : TIME := T#0S;
    tTMR_Ch1_DiscTimer_BC : TIME := T#0S;
    tTMR_Ch1_DiscTimer_CA : TIME := T#0S;
    rTMR_Ch1_Tolerance : REAL := 1.25; (* [deg C] *)
    iTMR_Ch1_DegradedMode : INT := 0; (* 0=3 healthy, 1=2 healthy, 2=1 healthy, 3=fail *)
    rTMR_Ch1_Voted : REAL;

    (* Channel 2: Shelf Outlet RTD *)
    bTMR_Ch2_A_Healthy : BOOL := TRUE;
    bTMR_Ch2_B_Healthy : BOOL := TRUE;
    bTMR_Ch2_C_Healthy : BOOL := TRUE;
    tTMR_Ch2_DiscTimer_AB : TIME := T#0S;
    tTMR_Ch2_DiscTimer_BC : TIME := T#0S;
    tTMR_Ch2_DiscTimer_CA : TIME := T#0S;
    rTMR_Ch2_Tolerance : REAL := 1.25; (* [deg C] *)
    iTMR_Ch2_DegradedMode : INT := 0;
    rTMR_Ch2_Voted : REAL;

    (* Channel 3: Product Cake Thermocouple *)
    bTMR_Ch3_A_Healthy : BOOL := TRUE;
    bTMR_Ch3_B_Healthy : BOOL := TRUE;
    bTMR_Ch3_C_Healthy : BOOL := TRUE;
    tTMR_Ch3_DiscTimer_AB : TIME := T#0S;
    tTMR_Ch3_DiscTimer_BC : TIME := T#0S;
    tTMR_Ch3_DiscTimer_CA : TIME := T#0S;
    rTMR_Ch3_Tolerance : REAL := 1.80; (* [deg C] *)
    iTMR_Ch3_DegradedMode : INT := 0;
    rTMR_Ch3_Voted : REAL;

    (* Channel 4: Capacitance Manometer Baratron *)
    bTMR_Ch4_A_Healthy : BOOL := TRUE;
    bTMR_Ch4_B_Healthy : BOOL := TRUE;
    bTMR_Ch4_C_Healthy : BOOL := TRUE;
    tTMR_Ch4_DiscTimer_AB : TIME := T#0S;
    tTMR_Ch4_DiscTimer_BC : TIME := T#0S;
    tTMR_Ch4_DiscTimer_CA : TIME := T#0S;
    rTMR_Ch4_Tolerance : REAL := 0.025; (* [mbar] *)
    iTMR_Ch4_DegradedMode : INT := 0;
    rTMR_Ch4_Voted : REAL;

    (* Channel 5: Pirani Vacuum Gauge *)
    bTMR_Ch5_A_Healthy : BOOL := TRUE;
    bTMR_Ch5_B_Healthy : BOOL := TRUE;
    bTMR_Ch5_C_Healthy : BOOL := TRUE;
    tTMR_Ch5_DiscTimer_AB : TIME := T#0S;
    tTMR_Ch5_DiscTimer_BC : TIME := T#0S;
    tTMR_Ch5_DiscTimer_CA : TIME := T#0S;
    rTMR_Ch5_Tolerance : REAL := 0.045; (* [mbar] *)
    iTMR_Ch5_DegradedMode : INT := 0;
    rTMR_Ch5_Voted : REAL;

    (* Channel 6: Condenser Coil Surface RTD *)
    bTMR_Ch6_A_Healthy : BOOL := TRUE;
    bTMR_Ch6_B_Healthy : BOOL := TRUE;
    bTMR_Ch6_C_Healthy : BOOL := TRUE;
    tTMR_Ch6_DiscTimer_AB : TIME := T#0S;
    tTMR_Ch6_DiscTimer_BC : TIME := T#0S;
    tTMR_Ch6_DiscTimer_CA : TIME := T#0S;
    rTMR_Ch6_Tolerance : REAL := 2.50; (* [deg C] *)
    iTMR_Ch6_DegradedMode : INT := 0;
    rTMR_Ch6_Voted : REAL;

    (* Channel 7: Hydraulic Stoppering Load Cells *)
    bTMR_Ch7_A_Healthy : BOOL := TRUE;
    bTMR_Ch7_B_Healthy : BOOL := TRUE;
    bTMR_Ch7_C_Healthy : BOOL := TRUE;
    tTMR_Ch7_DiscTimer_AB : TIME := T#0S;
    tTMR_Ch7_DiscTimer_BC : TIME := T#0S;
    tTMR_Ch7_DiscTimer_CA : TIME := T#0S;
    rTMR_Ch7_Tolerance : REAL := 8.50; (* [kN] *)
    iTMR_Ch7_DegradedMode : INT := 0;
    rTMR_Ch7_Voted : REAL;

    (* Common TMR Discrepancy trip timeout *)
    tTMR_Discrepancy_Trip_Delay : TIME := T#3S;

    (* Rate-of-Change (ROC) screening previous samples *)
    rPrev_Inlet_Temp_A : REAL;
    rPrev_Inlet_Temp_B : REAL;
    rPrev_Inlet_Temp_C : REAL;
    rPrev_Baratron_A : REAL;
    rPrev_Baratron_B : REAL;
    rPrev_Baratron_C : REAL;

    (* ========================================================================================================= *)
    (* MANOMETRIC TEMPERATURE MEASUREMENT (MTM) & PRESSURE RISE ANALYSIS (PRA) REGISTERS                         *)
    (* ========================================================================================================= *)
    bMTM_Pulse_Active : BOOL := FALSE;
    bMTM_Pulse_Trigger : BOOL := FALSE;
    iMTM_Sample_Index : INT := 0;
    tMTM_Timer : TIME := T#0S;
    tMTM_Interval_Timer : TIME := T#0S;
    tMTM_Periodic_Interval : TIME := T#1800S; (* 30 minutes periodic MTM pulse *)
    rMTM_Press_P0 : REAL := 0.0;
    rMTM_Press_P1 : REAL := 0.0;
    rMTM_Press_P2 : REAL := 0.0;
    rMTM_Press_P3 : REAL := 0.0;
    rMTM_Press_P4 : REAL := 0.0;
    rMTM_Press_P5 : REAL := 0.0;
    rMTM_Delta_P_Rise : REAL := 0.0;
    rMTM_Fitted_P_eq : REAL := 0.080;
    rMTM_Fitted_Tau : REAL := 4.50;
    rMTM_Fitted_LeakRate : REAL := 0.00012;
    rMTM_Computed_Ti : REAL := -32.5;
    rMTM_Computed_Rp : REAL := 2.45;
    rMTM_Cake_Collapse_Margin : REAL := 8.0;

    (* ========================================================================================================= *)
    (* SUBLIMATION ENDPOINT TRACKING (PIRANI / BARATRON RATIO SMOOTHING & CONVERGENCE)                           *)
    (* ========================================================================================================= *)
    rPirani_Baratron_Ratio_Raw : REAL := 1.60;
    rPirani_Baratron_Ratio_Filt : REAL := 1.60;
    tEndpoint_Crossover_Timer : TIME := T#0S;
    tEndpoint_Verification_Time : TIME := T#300S; (* 5 minutes stable ratio < 1.03 *)
    bSublimation_Front_Exhausted : BOOL := FALSE;

    (* ========================================================================================================= *)
    (* 14-STAGE DETERMINISTIC FINITE STATE MACHINE (FSM) STEP TIMERS & PHASE REGISTERS                           *)
    (* ========================================================================================================= *)
    iFSM_Current_State : INT := 0;
    iFSM_Next_State : INT := 0;
    iFSM_Previous_State : INT := 0;
    bFSM_State_Entry_Flag : BOOL := TRUE;
    tFSM_State_Timer : TIME := T#0S;
    tFSM_Soak_Duration_Target : TIME := T#0S;
    rFSM_Ramp_Start_Temp : REAL := 20.0;
    rFSM_Ramp_Target_Temp : REAL := -45.0;
    rFSM_Ramp_Slope_DegMin : REAL := -0.50;
    rFSM_Ramp_Current_SP : REAL := 20.0;
    bFSM_Ramp_Complete : BOOL := FALSE;
    bFSM_Soak_Complete : BOOL := FALSE;
    bFSM_Sterile_SIP_Passed : BOOL := FALSE;
    rCIP_SIP_F0_Accumulation : REAL := 0.0;

    (* ========================================================================================================= *)
    (* ISA-18.2 MULTI-TIER PROCESS ALARM TRIP POINTS, DEADBANDS, AND LATCH REGISTERS                             *)
    (* ========================================================================================================= *)
    (* Shelf Temperature Alarm Thresholds *)
    rAlarm_Limit_Shelf_HH : REAL := 65.0;
    rAlarm_Limit_Shelf_H  : REAL := 60.0;
    rAlarm_Limit_Shelf_L  : REAL := -58.0;
    rAlarm_Limit_Shelf_LL : REAL := -62.0;
    rAlarm_Deadband_Shelf : REAL := 1.5;

    (* Chamber Pressure Alarm Thresholds *)
    rAlarm_Limit_Press_HH : REAL := 0.650;
    rAlarm_Limit_Press_H  : REAL := 0.350;
    rAlarm_Limit_Press_L  : REAL := 0.010;
    rAlarm_Limit_Press_LL : REAL := 0.002;
    rAlarm_Deadband_Press : REAL := 0.015;

    (* Condenser Temperature Alarm Thresholds *)
    rAlarm_Limit_Cond_HH : REAL := -35.0;
    rAlarm_Limit_Cond_H  : REAL := -48.0;
    rAlarm_Deadband_Cond : REAL := 2.5;

    (* Stoppering Compression Force Overload Thresholds *)
    rAlarm_Limit_Force_HH : REAL := 240.0;
    rAlarm_Limit_Force_H  : REAL := 210.0;
    rAlarm_Deadband_Force : REAL := 5.0;

    (* Product Cake Collapse Proximity Margin Thresholds *)
    rAlarm_Limit_Collapse_Warning : REAL := 2.50; (* Ti within 2.5 deg C of Tc *)
    rAlarm_Limit_Collapse_Trip    : REAL := 0.80; (* Ti within 0.8 deg C of Tc *)

    (* Alarm Latches *)
    bTrip_Shelf_Temp_HH : BOOL := FALSE;
    bTrip_Shelf_Temp_H  : BOOL := FALSE;
    bTrip_Shelf_Temp_L  : BOOL := FALSE;
    bTrip_Shelf_Temp_LL : BOOL := FALSE;
    bTrip_Press_HH      : BOOL := FALSE;
    bTrip_Press_H       : BOOL := FALSE;
    bTrip_Press_L       : BOOL := FALSE;
    bTrip_Press_LL      : BOOL := FALSE;
    bTrip_Cond_Temp_HH  : BOOL := FALSE;
    bTrip_Cond_Temp_H   : BOOL := FALSE;
    bTrip_Force_HH      : BOOL := FALSE;
    bTrip_Force_H       : BOOL := FALSE;
    bTrip_Collapse_Crit : BOOL := FALSE;
    bTrip_TMR_Ch1_Fail  : BOOL := FALSE;
    bTrip_TMR_Ch2_Fail  : BOOL := FALSE;
    bTrip_TMR_Ch3_Fail  : BOOL := FALSE;
    bTrip_TMR_Ch4_Fail  : BOOL := FALSE;
    bTrip_TMR_Ch5_Fail  : BOOL := FALSE;
    bTrip_TMR_Ch6_Fail  : BOOL := FALSE;
    bTrip_TMR_Ch7_Fail  : BOOL := FALSE;
    bTrip_Isolator_Lost : BOOL := FALSE;
    bTrip_Refrig_HiDisch: BOOL := FALSE;

    (* Iteration and loop indexing variables *)
    iIndex : INT;
    jIndex : INT;
    kIndex : INT;
    hIndex : INT;
    rTemp_Sum : REAL;
    rDelta_Time_Sec : REAL := 0.020;
    rLog10_P_eq : REAL;
    rSat_Ice_Press : REAL;
    rGas_Conductance : REAL;
    rDesorp_Rate : REAL;
    rSublim_Rate_Calc : REAL;
END_VAR
"""
    parts.append(var_internal)

    # 5. PHASE 1: 2oo3 TMR SENSOR VOTING WITH DISCREPANCY TIMERS
    phase1 = """(* ========================================================================================================= *)
(* === PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS ===               *)
(* ========================================================================================================= *)

(* Time conversion for scan execution *)
rDelta_Time_Sec := TIME_TO_REAL(tCycle_Sample_Time_Ts) / 1000.0;
IF rDelta_Time_Sec <= 0.001 THEN
    rDelta_Time_Sec := 0.020; (* Clamp to 20 ms nominal discrete scan time *)
END_IF;

(* --------------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL 1: SILICONE OIL INLET TEMPERATURE RTD VOTING (rShelf_Oil_Inlet_Temp_RTD_A, B, C)             *)
(* --------------------------------------------------------------------------------------------------------- *)
(* Discrepancy Evaluation between sensory legs AB, BC, CA *)
IF ABS(rShelf_Oil_Inlet_Temp_RTD_A - rShelf_Oil_Inlet_Temp_RTD_B) > rTMR_Ch1_Tolerance THEN
    tTMR_Ch1_DiscTimer_AB := tTMR_Ch1_DiscTimer_AB + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch1_DiscTimer_AB > tCycle_Sample_Time_Ts THEN
        tTMR_Ch1_DiscTimer_AB := tTMR_Ch1_DiscTimer_AB - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch1_DiscTimer_AB := T#0S;
    END_IF;
END_IF;

IF ABS(rShelf_Oil_Inlet_Temp_RTD_B - rShelf_Oil_Inlet_Temp_RTD_C) > rTMR_Ch1_Tolerance THEN
    tTMR_Ch1_DiscTimer_BC := tTMR_Ch1_DiscTimer_BC + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch1_DiscTimer_BC > tCycle_Sample_Time_Ts THEN
        tTMR_Ch1_DiscTimer_BC := tTMR_Ch1_DiscTimer_BC - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch1_DiscTimer_BC := T#0S;
    END_IF;
END_IF;

IF ABS(rShelf_Oil_Inlet_Temp_RTD_C - rShelf_Oil_Inlet_Temp_RTD_A) > rTMR_Ch1_Tolerance THEN
    tTMR_Ch1_DiscTimer_CA := tTMR_Ch1_DiscTimer_CA + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch1_DiscTimer_CA > tCycle_Sample_Time_Ts THEN
        tTMR_Ch1_DiscTimer_CA := tTMR_Ch1_DiscTimer_CA - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch1_DiscTimer_CA := T#0S;
    END_IF;
END_IF;

(* Health Status Discrimination for Channel 1 *)
IF (tTMR_Ch1_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch1_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch1_A_Healthy := FALSE;
END_IF;
IF (tTMR_Ch1_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch1_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch1_B_Healthy := FALSE;
END_IF;
IF (tTMR_Ch1_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch1_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch1_C_Healthy := FALSE;
END_IF;

(* Bumpless Median & Average Degradation Logic for Channel 1 *)
IF bTMR_Ch1_A_Healthy AND bTMR_Ch1_B_Healthy AND bTMR_Ch1_C_Healthy THEN
    iTMR_Ch1_DegradedMode := 0; (* Full 2oo3 healthy *)
    IF (rShelf_Oil_Inlet_Temp_RTD_A >= rShelf_Oil_Inlet_Temp_RTD_B AND rShelf_Oil_Inlet_Temp_RTD_A <= rShelf_Oil_Inlet_Temp_RTD_C) OR
       (rShelf_Oil_Inlet_Temp_RTD_A <= rShelf_Oil_Inlet_Temp_RTD_B AND rShelf_Oil_Inlet_Temp_RTD_A >= rShelf_Oil_Inlet_Temp_RTD_C) THEN
        rTMR_Ch1_Voted := rShelf_Oil_Inlet_Temp_RTD_A;
    ELSIF (rShelf_Oil_Inlet_Temp_RTD_B >= rShelf_Oil_Inlet_Temp_RTD_A AND rShelf_Oil_Inlet_Temp_RTD_B <= rShelf_Oil_Inlet_Temp_RTD_C) OR
          (rShelf_Oil_Inlet_Temp_RTD_B <= rShelf_Oil_Inlet_Temp_RTD_A AND rShelf_Oil_Inlet_Temp_RTD_B >= rShelf_Oil_Inlet_Temp_RTD_C) THEN
        rTMR_Ch1_Voted := rShelf_Oil_Inlet_Temp_RTD_B;
    ELSE
        rTMR_Ch1_Voted := rShelf_Oil_Inlet_Temp_RTD_C;
    END_IF;
ELSIF bTMR_Ch1_A_Healthy AND bTMR_Ch1_B_Healthy THEN
    iTMR_Ch1_DegradedMode := 1; (* 1oo2 Degraded *)
    rTMR_Ch1_Voted := (rShelf_Oil_Inlet_Temp_RTD_A + rShelf_Oil_Inlet_Temp_RTD_B) * 0.50;
ELSIF bTMR_Ch1_B_Healthy AND bTMR_Ch1_C_Healthy THEN
    iTMR_Ch1_DegradedMode := 1;
    rTMR_Ch1_Voted := (rShelf_Oil_Inlet_Temp_RTD_B + rShelf_Oil_Inlet_Temp_RTD_C) * 0.50;
ELSIF bTMR_Ch1_A_Healthy AND bTMR_Ch1_C_Healthy THEN
    iTMR_Ch1_DegradedMode := 1;
    rTMR_Ch1_Voted := (rShelf_Oil_Inlet_Temp_RTD_A + rShelf_Oil_Inlet_Temp_RTD_C) * 0.50;
ELSIF bTMR_Ch1_A_Healthy THEN
    iTMR_Ch1_DegradedMode := 2; (* Single channel fallback *)
    rTMR_Ch1_Voted := rShelf_Oil_Inlet_Temp_RTD_A;
ELSIF bTMR_Ch1_B_Healthy THEN
    iTMR_Ch1_DegradedMode := 2;
    rTMR_Ch1_Voted := rShelf_Oil_Inlet_Temp_RTD_B;
ELSIF bTMR_Ch1_C_Healthy THEN
    iTMR_Ch1_DegradedMode := 2;
    rTMR_Ch1_Voted := rShelf_Oil_Inlet_Temp_RTD_C;
ELSE
    iTMR_Ch1_DegradedMode := 3; (* Total failure *)
    bTrip_TMR_Ch1_Fail := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL 2: SILICONE OIL OUTLET TEMPERATURE RTD VOTING (rShelf_Oil_Outlet_Temp_RTD_A, B, C)           *)
(* --------------------------------------------------------------------------------------------------------- *)
IF ABS(rShelf_Oil_Outlet_Temp_RTD_A - rShelf_Oil_Outlet_Temp_RTD_B) > rTMR_Ch2_Tolerance THEN
    tTMR_Ch2_DiscTimer_AB := tTMR_Ch2_DiscTimer_AB + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch2_DiscTimer_AB > tCycle_Sample_Time_Ts THEN
        tTMR_Ch2_DiscTimer_AB := tTMR_Ch2_DiscTimer_AB - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch2_DiscTimer_AB := T#0S;
    END_IF;
END_IF;

IF ABS(rShelf_Oil_Outlet_Temp_RTD_B - rShelf_Oil_Outlet_Temp_RTD_C) > rTMR_Ch2_Tolerance THEN
    tTMR_Ch2_DiscTimer_BC := tTMR_Ch2_DiscTimer_BC + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch2_DiscTimer_BC > tCycle_Sample_Time_Ts THEN
        tTMR_Ch2_DiscTimer_BC := tTMR_Ch2_DiscTimer_BC - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch2_DiscTimer_BC := T#0S;
    END_IF;
END_IF;

IF ABS(rShelf_Oil_Outlet_Temp_RTD_C - rShelf_Oil_Outlet_Temp_RTD_A) > rTMR_Ch2_Tolerance THEN
    tTMR_Ch2_DiscTimer_CA := tTMR_Ch2_DiscTimer_CA + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch2_DiscTimer_CA > tCycle_Sample_Time_Ts THEN
        tTMR_Ch2_DiscTimer_CA := tTMR_Ch2_DiscTimer_CA - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch2_DiscTimer_CA := T#0S;
    END_IF;
END_IF;

IF (tTMR_Ch2_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch2_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch2_A_Healthy := FALSE;
END_IF;
IF (tTMR_Ch2_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch2_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch2_B_Healthy := FALSE;
END_IF;
IF (tTMR_Ch2_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch2_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch2_C_Healthy := FALSE;
END_IF;

IF bTMR_Ch2_A_Healthy AND bTMR_Ch2_B_Healthy AND bTMR_Ch2_C_Healthy THEN
    iTMR_Ch2_DegradedMode := 0;
    IF (rShelf_Oil_Outlet_Temp_RTD_A >= rShelf_Oil_Outlet_Temp_RTD_B AND rShelf_Oil_Outlet_Temp_RTD_A <= rShelf_Oil_Outlet_Temp_RTD_C) OR
       (rShelf_Oil_Outlet_Temp_RTD_A <= rShelf_Oil_Outlet_Temp_RTD_B AND rShelf_Oil_Outlet_Temp_RTD_A >= rShelf_Oil_Outlet_Temp_RTD_C) THEN
        rTMR_Ch2_Voted := rShelf_Oil_Outlet_Temp_RTD_A;
    ELSIF (rShelf_Oil_Outlet_Temp_RTD_B >= rShelf_Oil_Outlet_Temp_RTD_A AND rShelf_Oil_Outlet_Temp_RTD_B <= rShelf_Oil_Outlet_Temp_RTD_C) OR
          (rShelf_Oil_Outlet_Temp_RTD_B <= rShelf_Oil_Outlet_Temp_RTD_A AND rShelf_Oil_Outlet_Temp_RTD_B >= rShelf_Oil_Outlet_Temp_RTD_C) THEN
        rTMR_Ch2_Voted := rShelf_Oil_Outlet_Temp_RTD_B;
    ELSE
        rTMR_Ch2_Voted := rShelf_Oil_Outlet_Temp_RTD_C;
    END_IF;
ELSIF bTMR_Ch2_A_Healthy AND bTMR_Ch2_B_Healthy THEN
    iTMR_Ch2_DegradedMode := 1;
    rTMR_Ch2_Voted := (rShelf_Oil_Outlet_Temp_RTD_A + rShelf_Oil_Outlet_Temp_RTD_B) * 0.50;
ELSIF bTMR_Ch2_B_Healthy AND bTMR_Ch2_C_Healthy THEN
    iTMR_Ch2_DegradedMode := 1;
    rTMR_Ch2_Voted := (rShelf_Oil_Outlet_Temp_RTD_B + rShelf_Oil_Outlet_Temp_RTD_C) * 0.50;
ELSIF bTMR_Ch2_A_Healthy AND bTMR_Ch2_C_Healthy THEN
    iTMR_Ch2_DegradedMode := 1;
    rTMR_Ch2_Voted := (rShelf_Oil_Outlet_Temp_RTD_A + rShelf_Oil_Outlet_Temp_RTD_C) * 0.50;
ELSIF bTMR_Ch2_A_Healthy THEN
    iTMR_Ch2_DegradedMode := 2;
    rTMR_Ch2_Voted := rShelf_Oil_Outlet_Temp_RTD_A;
ELSIF bTMR_Ch2_B_Healthy THEN
    iTMR_Ch2_DegradedMode := 2;
    rTMR_Ch2_Voted := rShelf_Oil_Outlet_Temp_RTD_B;
ELSIF bTMR_Ch2_C_Healthy THEN
    iTMR_Ch2_DegradedMode := 2;
    rTMR_Ch2_Voted := rShelf_Oil_Outlet_Temp_RTD_C;
ELSE
    iTMR_Ch2_DegradedMode := 3;
    bTrip_TMR_Ch2_Fail := TRUE;
END_IF;

(* Compute average voted bulk shelf oil temperature *)
rVoted_Shelf_Mean_Temp := (rTMR_Ch1_Voted + rTMR_Ch2_Voted) * 0.50;

(* --------------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL 3: PRODUCT CAKE MONITORED VIAL THERMOCOUPLES (rProduct_Vial_Temp_TC_A, B, C)                   *)
(* --------------------------------------------------------------------------------------------------------- *)
IF ABS(rProduct_Vial_Temp_TC_A - rProduct_Vial_Temp_TC_B) > rTMR_Ch3_Tolerance THEN
    tTMR_Ch3_DiscTimer_AB := tTMR_Ch3_DiscTimer_AB + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch3_DiscTimer_AB > tCycle_Sample_Time_Ts THEN
        tTMR_Ch3_DiscTimer_AB := tTMR_Ch3_DiscTimer_AB - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch3_DiscTimer_AB := T#0S;
    END_IF;
END_IF;

IF ABS(rProduct_Vial_Temp_TC_B - rProduct_Vial_Temp_TC_C) > rTMR_Ch3_Tolerance THEN
    tTMR_Ch3_DiscTimer_BC := tTMR_Ch3_DiscTimer_BC + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch3_DiscTimer_BC > tCycle_Sample_Time_Ts THEN
        tTMR_Ch3_DiscTimer_BC := tTMR_Ch3_DiscTimer_BC - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch3_DiscTimer_BC := T#0S;
    END_IF;
END_IF;

IF ABS(rProduct_Vial_Temp_TC_C - rProduct_Vial_Temp_TC_A) > rTMR_Ch3_Tolerance THEN
    tTMR_Ch3_DiscTimer_CA := tTMR_Ch3_DiscTimer_CA + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch3_DiscTimer_CA > tCycle_Sample_Time_Ts THEN
        tTMR_Ch3_DiscTimer_CA := tTMR_Ch3_DiscTimer_CA - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch3_DiscTimer_CA := T#0S;
    END_IF;
END_IF;

IF (tTMR_Ch3_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch3_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch3_A_Healthy := FALSE;
END_IF;
IF (tTMR_Ch3_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch3_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch3_B_Healthy := FALSE;
END_IF;
IF (tTMR_Ch3_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch3_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch3_C_Healthy := FALSE;
END_IF;

IF bTMR_Ch3_A_Healthy AND bTMR_Ch3_B_Healthy AND bTMR_Ch3_C_Healthy THEN
    iTMR_Ch3_DegradedMode := 0;
    IF (rProduct_Vial_Temp_TC_A >= rProduct_Vial_Temp_TC_B AND rProduct_Vial_Temp_TC_A <= rProduct_Vial_Temp_TC_C) OR
       (rProduct_Vial_Temp_TC_A <= rProduct_Vial_Temp_TC_B AND rProduct_Vial_Temp_TC_A >= rProduct_Vial_Temp_TC_C) THEN
        rTMR_Ch3_Voted := rProduct_Vial_Temp_TC_A;
    ELSIF (rProduct_Vial_Temp_TC_B >= rProduct_Vial_Temp_TC_A AND rProduct_Vial_Temp_TC_B <= rProduct_Vial_Temp_TC_C) OR
          (rProduct_Vial_Temp_TC_B <= rProduct_Vial_Temp_TC_A AND rProduct_Vial_Temp_TC_B >= rProduct_Vial_Temp_TC_C) THEN
        rTMR_Ch3_Voted := rProduct_Vial_Temp_TC_B;
    ELSE
        rTMR_Ch3_Voted := rProduct_Vial_Temp_TC_C;
    END_IF;
ELSIF bTMR_Ch3_A_Healthy AND bTMR_Ch3_B_Healthy THEN
    iTMR_Ch3_DegradedMode := 1;
    rTMR_Ch3_Voted := (rProduct_Vial_Temp_TC_A + rProduct_Vial_Temp_TC_B) * 0.50;
ELSIF bTMR_Ch3_B_Healthy AND bTMR_Ch3_C_Healthy THEN
    iTMR_Ch3_DegradedMode := 1;
    rTMR_Ch3_Voted := (rProduct_Vial_Temp_TC_B + rProduct_Vial_Temp_TC_C) * 0.50;
ELSIF bTMR_Ch3_A_Healthy AND bTMR_Ch3_C_Healthy THEN
    iTMR_Ch3_DegradedMode := 1;
    rTMR_Ch3_Voted := (rProduct_Vial_Temp_TC_A + rProduct_Vial_Temp_TC_C) * 0.50;
ELSIF bTMR_Ch3_A_Healthy THEN
    iTMR_Ch3_DegradedMode := 2;
    rTMR_Ch3_Voted := rProduct_Vial_Temp_TC_A;
ELSIF bTMR_Ch3_B_Healthy THEN
    iTMR_Ch3_DegradedMode := 2;
    rTMR_Ch3_Voted := rProduct_Vial_Temp_TC_B;
ELSIF bTMR_Ch3_C_Healthy THEN
    iTMR_Ch3_DegradedMode := 2;
    rTMR_Ch3_Voted := rProduct_Vial_Temp_TC_C;
ELSE
    iTMR_Ch3_DegradedMode := 3;
    bTrip_TMR_Ch3_Fail := TRUE;
END_IF;
rVoted_Product_Cake_Temp := rTMR_Ch3_Voted;

(* --------------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL 4: CAPACITANCE MANOMETERS (MKS BARATRON A, B, C)                                             *)
(* --------------------------------------------------------------------------------------------------------- *)
IF ABS(rChamber_Baratron_Press_A - rChamber_Baratron_Press_B) > rTMR_Ch4_Tolerance THEN
    tTMR_Ch4_DiscTimer_AB := tTMR_Ch4_DiscTimer_AB + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch4_DiscTimer_AB > tCycle_Sample_Time_Ts THEN
        tTMR_Ch4_DiscTimer_AB := tTMR_Ch4_DiscTimer_AB - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch4_DiscTimer_AB := T#0S;
    END_IF;
END_IF;

IF ABS(rChamber_Baratron_Press_B - rChamber_Baratron_Press_C) > rTMR_Ch4_Tolerance THEN
    tTMR_Ch4_DiscTimer_BC := tTMR_Ch4_DiscTimer_BC + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch4_DiscTimer_BC > tCycle_Sample_Time_Ts THEN
        tTMR_Ch4_DiscTimer_BC := tTMR_Ch4_DiscTimer_BC - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch4_DiscTimer_BC := T#0S;
    END_IF;
END_IF;

IF ABS(rChamber_Baratron_Press_C - rChamber_Baratron_Press_A) > rTMR_Ch4_Tolerance THEN
    tTMR_Ch4_DiscTimer_CA := tTMR_Ch4_DiscTimer_CA + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch4_DiscTimer_CA > tCycle_Sample_Time_Ts THEN
        tTMR_Ch4_DiscTimer_CA := tTMR_Ch4_DiscTimer_CA - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch4_DiscTimer_CA := T#0S;
    END_IF;
END_IF;

IF (tTMR_Ch4_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch4_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch4_A_Healthy := FALSE;
END_IF;
IF (tTMR_Ch4_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch4_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch4_B_Healthy := FALSE;
END_IF;
IF (tTMR_Ch4_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch4_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch4_C_Healthy := FALSE;
END_IF;

IF bTMR_Ch4_A_Healthy AND bTMR_Ch4_B_Healthy AND bTMR_Ch4_C_Healthy THEN
    iTMR_Ch4_DegradedMode := 0;
    IF (rChamber_Baratron_Press_A >= rChamber_Baratron_Press_B AND rChamber_Baratron_Press_A <= rChamber_Baratron_Press_C) OR
       (rChamber_Baratron_Press_A <= rChamber_Baratron_Press_B AND rChamber_Baratron_Press_A >= rChamber_Baratron_Press_C) THEN
        rTMR_Ch4_Voted := rChamber_Baratron_Press_A;
    ELSIF (rChamber_Baratron_Press_B >= rChamber_Baratron_Press_A AND rChamber_Baratron_Press_B <= rChamber_Baratron_Press_C) OR
          (rChamber_Baratron_Press_B <= rChamber_Baratron_Press_A AND rChamber_Baratron_Press_B >= rChamber_Baratron_Press_C) THEN
        rTMR_Ch4_Voted := rChamber_Baratron_Press_B;
    ELSE
        rTMR_Ch4_Voted := rChamber_Baratron_Press_C;
    END_IF;
ELSIF bTMR_Ch4_A_Healthy AND bTMR_Ch4_B_Healthy THEN
    iTMR_Ch4_DegradedMode := 1;
    rTMR_Ch4_Voted := (rChamber_Baratron_Press_A + rChamber_Baratron_Press_B) * 0.50;
ELSIF bTMR_Ch4_B_Healthy AND bTMR_Ch4_C_Healthy THEN
    iTMR_Ch4_DegradedMode := 1;
    rTMR_Ch4_Voted := (rChamber_Baratron_Press_B + rChamber_Baratron_Press_C) * 0.50;
ELSIF bTMR_Ch4_A_Healthy AND bTMR_Ch4_C_Healthy THEN
    iTMR_Ch4_DegradedMode := 1;
    rTMR_Ch4_Voted := (rChamber_Baratron_Press_A + rChamber_Baratron_Press_C) * 0.50;
ELSIF bTMR_Ch4_A_Healthy THEN
    iTMR_Ch4_DegradedMode := 2;
    rTMR_Ch4_Voted := rChamber_Baratron_Press_A;
ELSIF bTMR_Ch4_B_Healthy THEN
    iTMR_Ch4_DegradedMode := 2;
    rTMR_Ch4_Voted := rChamber_Baratron_Press_B;
ELSIF bTMR_Ch4_C_Healthy THEN
    iTMR_Ch4_DegradedMode := 2;
    rTMR_Ch4_Voted := rChamber_Baratron_Press_C;
ELSE
    iTMR_Ch4_DegradedMode := 3;
    bTrip_TMR_Ch4_Fail := TRUE;
END_IF;
rVoted_Chamber_Baratron_Press := rTMR_Ch4_Voted;

(* --------------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL 5: THERMAL CONDUCTIVITY PIRANI VACUUM GAUGES (rChamber_Pirani_Press_A, B, C)                  *)
(* --------------------------------------------------------------------------------------------------------- *)
IF ABS(rChamber_Pirani_Press_A - rChamber_Pirani_Press_B) > rTMR_Ch5_Tolerance THEN
    tTMR_Ch5_DiscTimer_AB := tTMR_Ch5_DiscTimer_AB + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch5_DiscTimer_AB > tCycle_Sample_Time_Ts THEN
        tTMR_Ch5_DiscTimer_AB := tTMR_Ch5_DiscTimer_AB - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch5_DiscTimer_AB := T#0S;
    END_IF;
END_IF;

IF ABS(rChamber_Pirani_Press_B - rChamber_Pirani_Press_C) > rTMR_Ch5_Tolerance THEN
    tTMR_Ch5_DiscTimer_BC := tTMR_Ch5_DiscTimer_BC + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch5_DiscTimer_BC > tCycle_Sample_Time_Ts THEN
        tTMR_Ch5_DiscTimer_BC := tTMR_Ch5_DiscTimer_BC - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch5_DiscTimer_BC := T#0S;
    END_IF;
END_IF;

IF ABS(rChamber_Pirani_Press_C - rChamber_Pirani_Press_A) > rTMR_Ch5_Tolerance THEN
    tTMR_Ch5_DiscTimer_CA := tTMR_Ch5_DiscTimer_CA + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch5_DiscTimer_CA > tCycle_Sample_Time_Ts THEN
        tTMR_Ch5_DiscTimer_CA := tTMR_Ch5_DiscTimer_CA - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch5_DiscTimer_CA := T#0S;
    END_IF;
END_IF;

IF (tTMR_Ch5_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch5_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch5_A_Healthy := FALSE;
END_IF;
IF (tTMR_Ch5_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch5_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch5_B_Healthy := FALSE;
END_IF;
IF (tTMR_Ch5_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch5_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch5_C_Healthy := FALSE;
END_IF;

IF bTMR_Ch5_A_Healthy AND bTMR_Ch5_B_Healthy AND bTMR_Ch5_C_Healthy THEN
    iTMR_Ch5_DegradedMode := 0;
    IF (rChamber_Pirani_Press_A >= rChamber_Pirani_Press_B AND rChamber_Pirani_Press_A <= rChamber_Pirani_Press_C) OR
       (rChamber_Pirani_Press_A <= rChamber_Pirani_Press_B AND rChamber_Pirani_Press_A >= rChamber_Pirani_Press_C) THEN
        rTMR_Ch5_Voted := rChamber_Pirani_Press_A;
    ELSIF (rChamber_Pirani_Press_B >= rChamber_Pirani_Press_A AND rChamber_Pirani_Press_B <= rChamber_Pirani_Press_C) OR
          (rChamber_Pirani_Press_B <= rChamber_Pirani_Press_A AND rChamber_Pirani_Press_B >= rChamber_Pirani_Press_C) THEN
        rTMR_Ch5_Voted := rChamber_Pirani_Press_B;
    ELSE
        rTMR_Ch5_Voted := rChamber_Pirani_Press_C;
    END_IF;
ELSIF bTMR_Ch5_A_Healthy AND bTMR_Ch5_B_Healthy THEN
    iTMR_Ch5_DegradedMode := 1;
    rTMR_Ch5_Voted := (rChamber_Pirani_Press_A + rChamber_Pirani_Press_B) * 0.50;
ELSIF bTMR_Ch5_B_Healthy AND bTMR_Ch5_C_Healthy THEN
    iTMR_Ch5_DegradedMode := 1;
    rTMR_Ch5_Voted := (rChamber_Pirani_Press_B + rChamber_Pirani_Press_C) * 0.50;
ELSIF bTMR_Ch5_A_Healthy AND bTMR_Ch5_C_Healthy THEN
    iTMR_Ch5_DegradedMode := 1;
    rTMR_Ch5_Voted := (rChamber_Pirani_Press_A + rChamber_Pirani_Press_C) * 0.50;
ELSIF bTMR_Ch5_A_Healthy THEN
    iTMR_Ch5_DegradedMode := 2;
    rTMR_Ch5_Voted := rChamber_Pirani_Press_A;
ELSIF bTMR_Ch5_B_Healthy THEN
    iTMR_Ch5_DegradedMode := 2;
    rTMR_Ch5_Voted := rChamber_Pirani_Press_B;
ELSIF bTMR_Ch5_C_Healthy THEN
    iTMR_Ch5_DegradedMode := 2;
    rTMR_Ch5_Voted := rChamber_Pirani_Press_C;
ELSE
    iTMR_Ch5_DegradedMode := 3;
    bTrip_TMR_Ch5_Fail := TRUE;
END_IF;
rVoted_Chamber_Pirani_Press := rTMR_Ch5_Voted;

(* Compute Pirani vs Baratron Sublimation Indicator Ratio *)
IF rVoted_Chamber_Baratron_Press > 0.0005 THEN
    rPirani_Baratron_Ratio_Raw := rVoted_Chamber_Pirani_Press / rVoted_Chamber_Baratron_Press;
ELSE
    rPirani_Baratron_Ratio_Raw := 1.0;
END_IF;

(* First-order low pass filter on ratio *)
rPirani_Baratron_Ratio_Filt := 0.95 * rPirani_Baratron_Ratio_Filt + 0.05 * rPirani_Baratron_Ratio_Raw;
rSublimation_Endpoint_Pirani_Ratio := rPirani_Baratron_Ratio_Filt;

(* --------------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL 6: CONDENSER COIL SURFACE RTDS (rCondenser_Coil_Temp_RTD_A, B, C)                             *)
(* --------------------------------------------------------------------------------------------------------- *)
IF ABS(rCondenser_Coil_Temp_RTD_A - rCondenser_Coil_Temp_RTD_B) > rTMR_Ch6_Tolerance THEN
    tTMR_Ch6_DiscTimer_AB := tTMR_Ch6_DiscTimer_AB + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch6_DiscTimer_AB > tCycle_Sample_Time_Ts THEN
        tTMR_Ch6_DiscTimer_AB := tTMR_Ch6_DiscTimer_AB - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch6_DiscTimer_AB := T#0S;
    END_IF;
END_IF;

IF ABS(rCondenser_Coil_Temp_RTD_B - rCondenser_Coil_Temp_RTD_C) > rTMR_Ch6_Tolerance THEN
    tTMR_Ch6_DiscTimer_BC := tTMR_Ch6_DiscTimer_BC + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch6_DiscTimer_BC > tCycle_Sample_Time_Ts THEN
        tTMR_Ch6_DiscTimer_BC := tTMR_Ch6_DiscTimer_BC - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch6_DiscTimer_BC := T#0S;
    END_IF;
END_IF;

IF ABS(rCondenser_Coil_Temp_RTD_C - rCondenser_Coil_Temp_RTD_A) > rTMR_Ch6_Tolerance THEN
    tTMR_Ch6_DiscTimer_CA := tTMR_Ch6_DiscTimer_CA + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch6_DiscTimer_CA > tCycle_Sample_Time_Ts THEN
        tTMR_Ch6_DiscTimer_CA := tTMR_Ch6_DiscTimer_CA - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch6_DiscTimer_CA := T#0S;
    END_IF;
END_IF;

IF (tTMR_Ch6_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch6_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch6_A_Healthy := FALSE;
END_IF;
IF (tTMR_Ch6_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch6_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch6_B_Healthy := FALSE;
END_IF;
IF (tTMR_Ch6_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch6_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch6_C_Healthy := FALSE;
END_IF;

IF bTMR_Ch6_A_Healthy AND bTMR_Ch6_B_Healthy AND bTMR_Ch6_C_Healthy THEN
    iTMR_Ch6_DegradedMode := 0;
    IF (rCondenser_Coil_Temp_RTD_A >= rCondenser_Coil_Temp_RTD_B AND rCondenser_Coil_Temp_RTD_A <= rCondenser_Coil_Temp_RTD_C) OR
       (rCondenser_Coil_Temp_RTD_A <= rCondenser_Coil_Temp_RTD_B AND rCondenser_Coil_Temp_RTD_A >= rCondenser_Coil_Temp_RTD_C) THEN
        rTMR_Ch6_Voted := rCondenser_Coil_Temp_RTD_A;
    ELSIF (rCondenser_Coil_Temp_RTD_B >= rCondenser_Coil_Temp_RTD_A AND rCondenser_Coil_Temp_RTD_B <= rCondenser_Coil_Temp_RTD_C) OR
          (rCondenser_Coil_Temp_RTD_B <= rCondenser_Coil_Temp_RTD_A AND rCondenser_Coil_Temp_RTD_B >= rCondenser_Coil_Temp_RTD_C) THEN
        rTMR_Ch6_Voted := rCondenser_Coil_Temp_RTD_B;
    ELSE
        rTMR_Ch6_Voted := rCondenser_Coil_Temp_RTD_C;
    END_IF;
ELSIF bTMR_Ch6_A_Healthy AND bTMR_Ch6_B_Healthy THEN
    iTMR_Ch6_DegradedMode := 1;
    rTMR_Ch6_Voted := (rCondenser_Coil_Temp_RTD_A + rCondenser_Coil_Temp_RTD_B) * 0.50;
ELSIF bTMR_Ch6_B_Healthy AND bTMR_Ch6_C_Healthy THEN
    iTMR_Ch6_DegradedMode := 1;
    rTMR_Ch6_Voted := (rCondenser_Coil_Temp_RTD_B + rCondenser_Coil_Temp_RTD_C) * 0.50;
ELSIF bTMR_Ch6_A_Healthy AND bTMR_Ch6_C_Healthy THEN
    iTMR_Ch6_DegradedMode := 1;
    rTMR_Ch6_Voted := (rCondenser_Coil_Temp_RTD_A + rCondenser_Coil_Temp_RTD_C) * 0.50;
ELSIF bTMR_Ch6_A_Healthy THEN
    iTMR_Ch6_DegradedMode := 2;
    rTMR_Ch6_Voted := rCondenser_Coil_Temp_RTD_A;
ELSIF bTMR_Ch6_B_Healthy THEN
    iTMR_Ch6_DegradedMode := 2;
    rTMR_Ch6_Voted := rCondenser_Coil_Temp_RTD_B;
ELSIF bTMR_Ch6_C_Healthy THEN
    iTMR_Ch6_DegradedMode := 2;
    rTMR_Ch6_Voted := rCondenser_Coil_Temp_RTD_C;
ELSE
    iTMR_Ch6_DegradedMode := 3;
    bTrip_TMR_Ch6_Fail := TRUE;
END_IF;
rVoted_Condenser_Coil_Temp := rTMR_Ch6_Voted;

(* --------------------------------------------------------------------------------------------------------- *)
(* TMR CHANNEL 7: HYDRAULIC STOPPERING LOAD CELLS (rStoppering_Load_Cell_Force_A, B, C)                     *)
(* --------------------------------------------------------------------------------------------------------- *)
IF ABS(rStoppering_Load_Cell_Force_A - rStoppering_Load_Cell_Force_B) > rTMR_Ch7_Tolerance THEN
    tTMR_Ch7_DiscTimer_AB := tTMR_Ch7_DiscTimer_AB + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch7_DiscTimer_AB > tCycle_Sample_Time_Ts THEN
        tTMR_Ch7_DiscTimer_AB := tTMR_Ch7_DiscTimer_AB - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch7_DiscTimer_AB := T#0S;
    END_IF;
END_IF;

IF ABS(rStoppering_Load_Cell_Force_B - rStoppering_Load_Cell_Force_C) > rTMR_Ch7_Tolerance THEN
    tTMR_Ch7_DiscTimer_BC := tTMR_Ch7_DiscTimer_BC + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch7_DiscTimer_BC > tCycle_Sample_Time_Ts THEN
        tTMR_Ch7_DiscTimer_BC := tTMR_Ch7_DiscTimer_BC - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch7_DiscTimer_BC := T#0S;
    END_IF;
END_IF;

IF ABS(rStoppering_Load_Cell_Force_C - rStoppering_Load_Cell_Force_A) > rTMR_Ch7_Tolerance THEN
    tTMR_Ch7_DiscTimer_CA := tTMR_Ch7_DiscTimer_CA + tCycle_Sample_Time_Ts;
ELSE
    IF tTMR_Ch7_DiscTimer_CA > tCycle_Sample_Time_Ts THEN
        tTMR_Ch7_DiscTimer_CA := tTMR_Ch7_DiscTimer_CA - tCycle_Sample_Time_Ts;
    ELSE
        tTMR_Ch7_DiscTimer_CA := T#0S;
    END_IF;
END_IF;

IF (tTMR_Ch7_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch7_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch7_A_Healthy := FALSE;
END_IF;
IF (tTMR_Ch7_DiscTimer_AB >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch7_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch7_B_Healthy := FALSE;
END_IF;
IF (tTMR_Ch7_DiscTimer_BC >= tTMR_Discrepancy_Trip_Delay) AND (tTMR_Ch7_DiscTimer_CA >= tTMR_Discrepancy_Trip_Delay) THEN
    bTMR_Ch7_C_Healthy := FALSE;
END_IF;

IF bTMR_Ch7_A_Healthy AND bTMR_Ch7_B_Healthy AND bTMR_Ch7_C_Healthy THEN
    iTMR_Ch7_DegradedMode := 0;
    IF (rStoppering_Load_Cell_Force_A >= rStoppering_Load_Cell_Force_B AND rStoppering_Load_Cell_Force_A <= rStoppering_Load_Cell_Force_C) OR
       (rStoppering_Load_Cell_Force_A <= rStoppering_Load_Cell_Force_B AND rStoppering_Load_Cell_Force_A >= rStoppering_Load_Cell_Force_C) THEN
        rTMR_Ch7_Voted := rStoppering_Load_Cell_Force_A;
    ELSIF (rStoppering_Load_Cell_Force_B >= rStoppering_Load_Cell_Force_A AND rStoppering_Load_Cell_Force_B <= rStoppering_Load_Cell_Force_C) OR
          (rStoppering_Load_Cell_Force_B <= rStoppering_Load_Cell_Force_A AND rStoppering_Load_Cell_Force_B >= rStoppering_Load_Cell_Force_C) THEN
        rTMR_Ch7_Voted := rStoppering_Load_Cell_Force_B;
    ELSE
        rTMR_Ch7_Voted := rStoppering_Load_Cell_Force_C;
    END_IF;
ELSIF bTMR_Ch7_A_Healthy AND bTMR_Ch7_B_Healthy THEN
    iTMR_Ch7_DegradedMode := 1;
    rTMR_Ch7_Voted := (rStoppering_Load_Cell_Force_A + rStoppering_Load_Cell_Force_B) * 0.50;
ELSIF bTMR_Ch7_B_Healthy AND bTMR_Ch7_C_Healthy THEN
    iTMR_Ch7_DegradedMode := 1;
    rTMR_Ch7_Voted := (rStoppering_Load_Cell_Force_B + rStoppering_Load_Cell_Force_C) * 0.50;
ELSIF bTMR_Ch7_A_Healthy AND bTMR_Ch7_C_Healthy THEN
    iTMR_Ch7_DegradedMode := 1;
    rTMR_Ch7_Voted := (rStoppering_Load_Cell_Force_A + rStoppering_Load_Cell_Force_C) * 0.50;
ELSIF bTMR_Ch7_A_Healthy THEN
    iTMR_Ch7_DegradedMode := 2;
    rTMR_Ch7_Voted := rStoppering_Load_Cell_Force_A;
ELSIF bTMR_Ch7_B_Healthy THEN
    iTMR_Ch7_DegradedMode := 2;
    rTMR_Ch7_Voted := rStoppering_Load_Cell_Force_B;
ELSIF bTMR_Ch7_C_Healthy THEN
    iTMR_Ch7_DegradedMode := 2;
    rTMR_Ch7_Voted := rStoppering_Load_Cell_Force_C;
ELSE
    iTMR_Ch7_DegradedMode := 3;
    bTrip_TMR_Ch7_Fail := TRUE;
END_IF;
rVoted_Stoppering_Actual_Force := rTMR_Ch7_Voted;
"""
    parts.append(phase1)

    # 6. PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION
    phase2 = """(* ========================================================================================================= *)
(* === PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (x[k+1] = A*x[k] + B*u[k]) ===        *)
(* ========================================================================================================= *)

(* Physical non-linear thermodynamic calculations *)
(* Saturated ice vapor pressure calculation from Clausius-Clapeyron relation *)
IF rVoted_Product_Cake_Temp < 0.0 THEN
    rSat_Ice_Press := 10.0 ** (10.5553 - (2667.0 / (rVoted_Product_Cake_Temp + 273.15)));
ELSE
    rSat_Ice_Press := 6.11;
END_IF;

(* Rarefied gas thermal conductance in Knudsen transition regime *)
rGas_Conductance := (0.85 * 1.19 * rVoted_Chamber_Baratron_Press) / 
                    (1.0 + 0.85 * 1.19 * rVoted_Chamber_Baratron_Press * 0.125);

(* Sublimation mass flux estimation based on vapor pressure difference *)
IF (rSat_Ice_Press > rVoted_Chamber_Baratron_Press) AND (iFSM_Current_State >= 6) AND (iFSM_Current_State <= 7) THEN
    rSublim_Rate_Calc := 150000.0 * 0.000350 * (rSat_Ice_Press - rVoted_Chamber_Baratron_Press) / 2.45;
    IF rSublim_Rate_Calc > 45.0 THEN
        rSublim_Rate_Calc := 45.0; (* Clamp to 45 kg/h max condenser capacity *)
    END_IF;
ELSE
    rSublim_Rate_Calc := 0.0;
END_IF;
rEstimated_Sublimation_Flux := rSublim_Rate_Calc;

(* Assemble measurement vector y_k from voted sensors *)
rMeas_Vector_y_k[1] := rVoted_Shelf_Mean_Temp;
rMeas_Vector_y_k[2] := rVoted_Product_Cake_Temp;
rMeas_Vector_y_k[3] := rVoted_Chamber_Baratron_Press;
rMeas_Vector_y_k[4] := rState_Vector_x_k[4]; (* Observer estimated ice thickness *)
rMeas_Vector_y_k[5] := rSublim_Rate_Calc;
rMeas_Vector_y_k[6] := rState_Vector_x_k[6]; (* Observer estimated residual moisture *)
rMeas_Vector_y_k[7] := rVoted_Stoppering_Actual_Force;
rMeas_Vector_y_k[8] := rState_Vector_x_k[8]; (* Estimated bleed flow *)

(* Assemble previous control vector u_k *)
rControl_Vector_u_k[1] := rShelf_Electric_Heater_PWM_Duty;
rControl_Vector_u_k[2] := rShelf_Refrig_Expansion_Valve_Duty;
rControl_Vector_u_k[3] := rVacuum_Booster_Roots_VFD_Speed;
rControl_Vector_u_k[4] := rNitrogen_MicroBleed_Piezo_Valve_Duty;
IF bChamber_Isolation_Spool_Valve_Open THEN
    rControl_Vector_u_k[5] := 1.0;
ELSE
    rControl_Vector_u_k[5] := 0.0;
END_IF;
rControl_Vector_u_k[6] := rHydraulic_Stoppering_Servo_Valve;
rControl_Vector_u_k[7] := rCondenser_Refrig_Expansion_Valve_Duty;
rControl_Vector_u_k[8] := rSterile_Aeration_Break_Valve_Duty;

(* Explicit unrolled matrix-vector multiplication for x[k+1] = A * x[k] + B * u[k] *)
(* State 1: Mean shelf silicone oil temperature *)
rState_Vector_x_kplus1[1] := 
    mA_Matrix[1,1] * rState_Vector_x_k[1] +
    mA_Matrix[1,2] * rState_Vector_x_k[2] +
    mA_Matrix[1,3] * rState_Vector_x_k[3] +
    mA_Matrix[1,4] * rState_Vector_x_k[4] +
    mA_Matrix[1,5] * rState_Vector_x_k[5] +
    mA_Matrix[1,6] * rState_Vector_x_k[6] +
    mA_Matrix[1,7] * rState_Vector_x_k[7] +
    mA_Matrix[1,8] * rState_Vector_x_k[8] +
    mB_Matrix[1,1] * rControl_Vector_u_k[1] +
    mB_Matrix[1,2] * rControl_Vector_u_k[2] +
    mB_Matrix[1,3] * rControl_Vector_u_k[3] +
    mB_Matrix[1,4] * rControl_Vector_u_k[4] +
    mB_Matrix[1,5] * rControl_Vector_u_k[5] +
    mB_Matrix[1,6] * rControl_Vector_u_k[6] +
    mB_Matrix[1,7] * rControl_Vector_u_k[7] +
    mB_Matrix[1,8] * rControl_Vector_u_k[8];

(* State 2: Sublimation ice front interface temperature *)
rState_Vector_x_kplus1[2] := 
    mA_Matrix[2,1] * rState_Vector_x_k[1] +
    mA_Matrix[2,2] * rState_Vector_x_k[2] +
    mA_Matrix[2,3] * rState_Vector_x_k[3] +
    mA_Matrix[2,4] * rState_Vector_x_k[4] +
    mA_Matrix[2,5] * rState_Vector_x_k[5] +
    mA_Matrix[2,6] * rState_Vector_x_k[6] +
    mA_Matrix[2,7] * rState_Vector_x_k[7] +
    mA_Matrix[2,8] * rState_Vector_x_k[8] +
    mB_Matrix[2,1] * rControl_Vector_u_k[1] +
    mB_Matrix[2,2] * rControl_Vector_u_k[2] +
    mB_Matrix[2,3] * rControl_Vector_u_k[3] +
    mB_Matrix[2,4] * rControl_Vector_u_k[4] +
    mB_Matrix[2,5] * rControl_Vector_u_k[5] +
    mB_Matrix[2,6] * rControl_Vector_u_k[6] +
    mB_Matrix[2,7] * rControl_Vector_u_k[7] +
    mB_Matrix[2,8] * rControl_Vector_u_k[8];

(* State 3: Chamber absolute pressure *)
rState_Vector_x_kplus1[3] := 
    mA_Matrix[3,1] * rState_Vector_x_k[1] +
    mA_Matrix[3,2] * rState_Vector_x_k[2] +
    mA_Matrix[3,3] * rState_Vector_x_k[3] +
    mA_Matrix[3,4] * rState_Vector_x_k[4] +
    mA_Matrix[3,5] * rState_Vector_x_k[5] +
    mA_Matrix[3,6] * rState_Vector_x_k[6] +
    mA_Matrix[3,7] * rState_Vector_x_k[7] +
    mA_Matrix[3,8] * rState_Vector_x_k[8] +
    mB_Matrix[3,1] * rControl_Vector_u_k[1] +
    mB_Matrix[3,2] * rControl_Vector_u_k[2] +
    mB_Matrix[3,3] * rControl_Vector_u_k[3] +
    mB_Matrix[3,4] * rControl_Vector_u_k[4] +
    mB_Matrix[3,5] * rControl_Vector_u_k[5] +
    mB_Matrix[3,6] * rControl_Vector_u_k[6] +
    mB_Matrix[3,7] * rControl_Vector_u_k[7] +
    mB_Matrix[3,8] * rControl_Vector_u_k[8];

(* State 4: Condenser coil ice layer accumulation thickness *)
rState_Vector_x_kplus1[4] := 
    mA_Matrix[4,1] * rState_Vector_x_k[1] +
    mA_Matrix[4,2] * rState_Vector_x_k[2] +
    mA_Matrix[4,3] * rState_Vector_x_k[3] +
    mA_Matrix[4,4] * rState_Vector_x_k[4] +
    mA_Matrix[4,5] * rState_Vector_x_k[5] +
    mA_Matrix[4,6] * rState_Vector_x_k[6] +
    mA_Matrix[4,7] * rState_Vector_x_k[7] +
    mA_Matrix[4,8] * rState_Vector_x_k[8] +
    mB_Matrix[4,1] * rControl_Vector_u_k[1] +
    mB_Matrix[4,2] * rControl_Vector_u_k[2] +
    mB_Matrix[4,3] * rControl_Vector_u_k[3] +
    mB_Matrix[4,4] * rControl_Vector_u_k[4] +
    mB_Matrix[4,5] * rControl_Vector_u_k[5] +
    mB_Matrix[4,6] * rControl_Vector_u_k[6] +
    mB_Matrix[4,7] * rControl_Vector_u_k[7] +
    mB_Matrix[4,8] * rControl_Vector_u_k[8];

(* State 5: Sublimation mass flow rate *)
rState_Vector_x_kplus1[5] := 
    mA_Matrix[5,1] * rState_Vector_x_k[1] +
    mA_Matrix[5,2] * rState_Vector_x_k[2] +
    mA_Matrix[5,3] * rState_Vector_x_k[3] +
    mA_Matrix[5,4] * rState_Vector_x_k[4] +
    mA_Matrix[5,5] * rState_Vector_x_k[5] +
    mA_Matrix[5,6] * rState_Vector_x_k[6] +
    mA_Matrix[5,7] * rState_Vector_x_k[7] +
    mA_Matrix[5,8] * rState_Vector_x_k[8] +
    mB_Matrix[5,1] * rControl_Vector_u_k[1] +
    mB_Matrix[5,2] * rControl_Vector_u_k[2] +
    mB_Matrix[5,3] * rControl_Vector_u_k[3] +
    mB_Matrix[5,4] * rControl_Vector_u_k[4] +
    mB_Matrix[5,5] * rControl_Vector_u_k[5] +
    mB_Matrix[5,6] * rControl_Vector_u_k[6] +
    mB_Matrix[5,7] * rControl_Vector_u_k[7] +
    mB_Matrix[5,8] * rControl_Vector_u_k[8];

(* State 6: Secondary drying residual product cake moisture *)
rState_Vector_x_kplus1[6] := 
    mA_Matrix[6,1] * rState_Vector_x_k[1] +
    mA_Matrix[6,2] * rState_Vector_x_k[2] +
    mA_Matrix[6,3] * rState_Vector_x_k[3] +
    mA_Matrix[6,4] * rState_Vector_x_k[4] +
    mA_Matrix[6,5] * rState_Vector_x_k[5] +
    mA_Matrix[6,6] * rState_Vector_x_k[6] +
    mA_Matrix[6,7] * rState_Vector_x_k[7] +
    mA_Matrix[6,8] * rState_Vector_x_k[8] +
    mB_Matrix[6,1] * rControl_Vector_u_k[1] +
    mB_Matrix[6,2] * rControl_Vector_u_k[2] +
    mB_Matrix[6,3] * rControl_Vector_u_k[3] +
    mB_Matrix[6,4] * rControl_Vector_u_k[4] +
    mB_Matrix[6,5] * rControl_Vector_u_k[5] +
    mB_Matrix[6,6] * rControl_Vector_u_k[6] +
    mB_Matrix[6,7] * rControl_Vector_u_k[7] +
    mB_Matrix[6,8] * rControl_Vector_u_k[8];

(* State 7: Hydraulic shelf stoppering compression force *)
rState_Vector_x_kplus1[7] := 
    mA_Matrix[7,1] * rState_Vector_x_k[1] +
    mA_Matrix[7,2] * rState_Vector_x_k[2] +
    mA_Matrix[7,3] * rState_Vector_x_k[3] +
    mA_Matrix[7,4] * rState_Vector_x_k[4] +
    mA_Matrix[7,5] * rState_Vector_x_k[5] +
    mA_Matrix[7,6] * rState_Vector_x_k[6] +
    mA_Matrix[7,7] * rState_Vector_x_k[7] +
    mA_Matrix[7,8] * rState_Vector_x_k[8] +
    mB_Matrix[7,1] * rControl_Vector_u_k[1] +
    mB_Matrix[7,2] * rControl_Vector_u_k[2] +
    mB_Matrix[7,3] * rControl_Vector_u_k[3] +
    mB_Matrix[7,4] * rControl_Vector_u_k[4] +
    mB_Matrix[7,5] * rControl_Vector_u_k[5] +
    mB_Matrix[7,6] * rControl_Vector_u_k[6] +
    mB_Matrix[7,7] * rControl_Vector_u_k[7] +
    mB_Matrix[7,8] * rControl_Vector_u_k[8];

(* State 8: Chamber sterile nitrogen leak/bleed rate *)
rState_Vector_x_kplus1[8] := 
    mA_Matrix[8,1] * rState_Vector_x_k[1] +
    mA_Matrix[8,2] * rState_Vector_x_k[2] +
    mA_Matrix[8,3] * rState_Vector_x_k[3] +
    mA_Matrix[8,4] * rState_Vector_x_k[4] +
    mA_Matrix[8,5] * rState_Vector_x_k[5] +
    mA_Matrix[8,6] * rState_Vector_x_k[6] +
    mA_Matrix[8,7] * rState_Vector_x_k[7] +
    mA_Matrix[8,8] * rState_Vector_x_k[8] +
    mB_Matrix[8,1] * rControl_Vector_u_k[1] +
    mB_Matrix[8,2] * rControl_Vector_u_k[2] +
    mB_Matrix[8,3] * rControl_Vector_u_k[3] +
    mB_Matrix[8,4] * rControl_Vector_u_k[4] +
    mB_Matrix[8,5] * rControl_Vector_u_k[5] +
    mB_Matrix[8,6] * rControl_Vector_u_k[6] +
    mB_Matrix[8,7] * rControl_Vector_u_k[7] +
    mB_Matrix[8,8] * rControl_Vector_u_k[8];

(* Output Prediction y_est = C * x_kplus1 + D * u_k *)
FOR iIndex := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR jIndex := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + mC_Matrix[iIndex, jIndex] * rState_Vector_x_kplus1[jIndex];
    END_FOR;
    rEst_Output_Vector_y_k[iIndex] := rTemp_Sum;
    rInnov_Vector[iIndex] := rMeas_Vector_y_k[iIndex] - rEst_Output_Vector_y_k[iIndex];
END_FOR;

(* Innovation correction update x_est = x_kplus1 + L * (y_meas - y_est) *)
FOR iIndex := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR jIndex := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + mL_KalmanGain[iIndex, jIndex] * rInnov_Vector[jIndex];
    END_FOR;
    rState_Vector_x_est[iIndex] := rState_Vector_x_kplus1[iIndex] + rTemp_Sum;
    rState_Vector_x_k[iIndex] := rState_Vector_x_est[iIndex];
END_FOR;

(* Output physical reconstructed observer states *)
rEstimated_Ice_Cake_Thickness := rState_Vector_x_est[4];
rEstimated_Residual_Moisture  := rState_Vector_x_est[6];
"""
    parts.append(phase2)

    # 7. PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS
    phase3 = """(* ========================================================================================================= *)
(* === PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS ===                                  *)
(* ========================================================================================================= *)

(* Update MPC setpoint references depending on active operational mode *)
rTarget_State_Ref[1] := rFSM_Ramp_Current_SP; (* Shelf temperature target *)
rTarget_State_Ref[2] := rRecipe_Collapse_Temp_Limit - 3.50; (* Safe sublimation interface temp *)
IF (iFSM_Current_State = 5) OR (iFSM_Current_State = 6) OR (iFSM_Current_State = 7) THEN
    rTarget_State_Ref[3] := rRecipe_Primary_Chamber_Press_SP; (* E.g. 0.090 mbar *)
ELSIF (iFSM_Current_State = 8) OR (iFSM_Current_State = 9) THEN
    rTarget_State_Ref[3] := 0.010; (* Deep vacuum for secondary drying *)
ELSIF iFSM_Current_State = 10 THEN
    rTarget_State_Ref[3] := rRecipe_Backfill_Target_Press; (* E.g. 800 mbar *)
ELSE
    rTarget_State_Ref[3] := 1013.25; (* Atmospheric *)
END_IF;
rTarget_State_Ref[4] := 0.0; (* Min ice thickness *)
rTarget_State_Ref[5] := 0.0;
rTarget_State_Ref[6] := 0.50; (* Target residual moisture < 0.5% *)
IF iFSM_Current_State = 11 THEN
    rTarget_State_Ref[7] := rRecipe_Stoppering_Target_Force;
ELSE
    rTarget_State_Ref[7] := 0.0;
END_IF;
rTarget_State_Ref[8] := 0.0;

(* Initialize MPC forward prediction horizon buffers *)
FOR iIndex := 1 TO 8 DO
    rMPC_Pred_States[0, iIndex] := rState_Vector_x_est[iIndex];
END_FOR;

FOR kIndex := 0 TO 4 DO
    FOR iIndex := 1 TO 8 DO
        rMPC_Pred_Controls[kIndex, iIndex] := rControl_Vector_u_k[iIndex];
    END_FOR;
END_FOR;

(* Projected Gradient Descent (PGD) Iteration Loop *)
FOR hIndex := 1 TO 6 DO
    (* 1. Forward state trajectory propagation over horizon Np = 5 *)
    FOR kIndex := 0 TO 4 DO
        FOR iIndex := 1 TO 8 DO
            rTemp_Sum := 0.0;
            FOR jIndex := 1 TO 8 DO
                rTemp_Sum := rTemp_Sum + mA_Matrix[iIndex, jIndex] * rMPC_Pred_States[kIndex, jIndex] +
                                         mB_Matrix[iIndex, jIndex] * rMPC_Pred_Controls[kIndex, jIndex];
            END_FOR;
            rMPC_Pred_States[kIndex + 1, iIndex] := rTemp_Sum;
        END_FOR;
    END_FOR;

    (* 2. Backward adjoint propagation & gradient calculation *)
    FOR kIndex := 4 TO 0 BY -1 DO
        FOR iIndex := 1 TO 8 DO
            (* State tracking error penalty *)
            rTemp_Sum := rMPC_Q_Weights[iIndex] * (rMPC_Pred_States[kIndex + 1, iIndex] - rTarget_State_Ref[iIndex]);
            
            (* Actuator effort and slew penalty gradient *)
            rMPC_Gradient_u[kIndex, iIndex] := 
                rTemp_Sum * mB_Matrix[iIndex, iIndex] +
                rMPC_R_Weights[iIndex] * rMPC_Pred_Controls[kIndex, iIndex];

            IF kIndex > 0 THEN
                rMPC_Gradient_u[kIndex, iIndex] := rMPC_Gradient_u[kIndex, iIndex] +
                    rMPC_S_SlewWeights[iIndex] * (rMPC_Pred_Controls[kIndex, iIndex] - rMPC_Pred_Controls[kIndex - 1, iIndex]);
            END_IF;

            (* Projected Gradient Update: u_new = u_old - alpha * grad *)
            rMPC_Pred_Controls[kIndex, iIndex] := rMPC_Pred_Controls[kIndex, iIndex] - 
                rMPC_Alpha_Step * rMPC_Gradient_u[kIndex, iIndex];

            (* Actuator Box Saturation [u_min, u_max] *)
            IF rMPC_Pred_Controls[kIndex, iIndex] < rActuator_Min_Bounds[iIndex] THEN
                rMPC_Pred_Controls[kIndex, iIndex] := rActuator_Min_Bounds[iIndex];
            ELSIF rMPC_Pred_Controls[kIndex, iIndex] > rActuator_Max_Bounds[iIndex] THEN
                rMPC_Pred_Controls[kIndex, iIndex] := rActuator_Max_Bounds[iIndex];
            END_IF;

            (* Actuator Dynamic Slew Rate Limiter Clamping *)
            IF kIndex = 0 THEN
                IF (rMPC_Pred_Controls[0, iIndex] - rControl_Vector_u_prev[iIndex]) > rActuator_Slew_Limits[iIndex] THEN
                    rMPC_Pred_Controls[0, iIndex] := rControl_Vector_u_prev[iIndex] + rActuator_Slew_Limits[iIndex];
                ELSIF (rMPC_Pred_Controls[0, iIndex] - rControl_Vector_u_prev[iIndex]) < -rActuator_Slew_Limits[iIndex] THEN
                    rMPC_Pred_Controls[0, iIndex] := rControl_Vector_u_prev[iIndex] - rActuator_Slew_Limits[iIndex];
                END_IF;
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* Apply First Optimal Control Step (Receding Horizon Principle) *)
IF (iFSM_Current_State >= 3) AND (iFSM_Current_State <= 11) THEN
    rShelf_Electric_Heater_PWM_Duty        := rMPC_Pred_Controls[0, 1];
    rShelf_Refrig_Expansion_Valve_Duty    := rMPC_Pred_Controls[0, 2];
    rVacuum_Booster_Roots_VFD_Speed       := rMPC_Pred_Controls[0, 3];
    rNitrogen_MicroBleed_Piezo_Valve_Duty := rMPC_Pred_Controls[0, 4];
    rHydraulic_Stoppering_Servo_Valve     := rMPC_Pred_Controls[0, 6];
    rCondenser_Refrig_Expansion_Valve_Duty:= rMPC_Pred_Controls[0, 7];
END_IF;

(* Save previous control vector for slew rate enforcement *)
FOR iIndex := 1 TO 8 DO
    rControl_Vector_u_prev[iIndex] := rMPC_Pred_Controls[0, iIndex];
END_FOR;
"""
    parts.append(phase3)

    # 8. PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
    phase4 = """(* ========================================================================================================= *)
(* === PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM) ===                             *)
(* ========================================================================================================= *)

(* Global Safety and Emergency Abort Override Check *)
IF bCmd_Cycle_Abort OR bAlarm_ISA18_Emergency_Trip THEN
    iFSM_Current_State := 14; (* Emergency Abort Defrost & Safe Vent *)
END_IF;

(* Execute Deterministic Operational State Sequencing *)
CASE iFSM_Current_State OF

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 0: SYSTEM STANDBY & PRE-CHECKS                                                                  *)
    (* ----------------------------------------------------------------------------------------------------- *)
    0:
        iActive_FSM_State_ID := 0;
        bBatch_Lyophilization_Complete := FALSE;
        bSublimation_Primary_Endpoint_Active := FALSE;
        
        (* De-energize active actuators in standby *)
        rShelf_Electric_Heater_PWM_Duty := 0.0;
        rShelf_Refrig_Expansion_Valve_Duty := 0.0;
        rCondenser_Refrig_Expansion_Valve_Duty := 0.0;
        rVacuum_Roughing_Screw_VFD_Speed := 0.0;
        rVacuum_Booster_Roots_VFD_Speed := 0.0;
        bChamber_Isolation_Spool_Valve_Open := FALSE;
        rNitrogen_MicroBleed_Piezo_Valve_Duty := 0.0;
        bNitrogen_Fast_Backfill_Valve_Open := FALSE;
        rSterile_Aeration_Break_Valve_Duty := 0.0;
        rHydraulic_Stoppering_Servo_Valve := 0.0;
        bHydraulic_Power_Pack_Pump_Run := FALSE;
        rCIP_SIP_Steam_Modulating_Valve := 0.0;
        bCondenser_Defrost_Water_Valve_Open := FALSE;

        IF bCmd_Cycle_Start AND bIsolator_Interlock_Healthy AND NOT bAlarm_ISA18_Critical_Active THEN
            iFSM_Current_State := 1; (* Proceed to CIP/SIP Sterilization *)
            bFSM_State_Entry_Flag := TRUE;
            tFSM_State_Timer := T#0S;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 1: CLEAN-IN-PLACE / STEAM-IN-PLACE (CIP/SIP) STERILIZATION (121.1 DEG C, 2.1 BAR)                *)
    (* ----------------------------------------------------------------------------------------------------- *)
    1:
        iActive_FSM_State_ID := 1;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Maintain clean steam valve to reach 121.5 deg C *)
        IF rVoted_Shelf_Mean_Temp < 121.1 THEN
            rCIP_SIP_Steam_Modulating_Valve := 85.0;
        ELSE
            rCIP_SIP_Steam_Modulating_Valve := 35.0; (* Modulate to hold temperature *)
            (* F0 accumulation rate: L = 10^((T - 121.1)/10) *)
            rCIP_SIP_F0_Accumulation := rCIP_SIP_F0_Accumulation + 
                (10.0 ** ((rVoted_Shelf_Mean_Temp - 121.1) / 10.0)) * (rDelta_Time_Sec / 60.0);
        END_IF;

        (* Verification: F0 lethality >= 30.0 minutes (overkill sterilization method per Ph. Eur. / USP) *)
        IF (rCIP_SIP_F0_Accumulation >= 30.0) AND (tFSM_State_Timer >= T#1800S) THEN
            bFSM_Sterile_SIP_Passed := TRUE;
            rCIP_SIP_Steam_Modulating_Valve := 0.0;
            iFSM_Current_State := 2; (* Proceed to Aseptic Loading *)
            bFSM_State_Entry_Flag := TRUE;
            tFSM_State_Timer := T#0S;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 2: ASEPTIC VIAL LOADING (ISOLATOR INTERFACE, SHELVES AT +5.0 DEG C)                             *)
    (* ----------------------------------------------------------------------------------------------------- *)
    2:
        iActive_FSM_State_ID := 2;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Pre-chill and maintain shelves at +5.0 deg C to preserve liquid biologic prior to freezing *)
        IF rVoted_Shelf_Mean_Temp > 5.5 THEN
            rShelf_Refrig_Expansion_Valve_Duty := 35.0;
            rShelf_Electric_Heater_PWM_Duty := 0.0;
        ELSIF rVoted_Shelf_Mean_Temp < 4.5 THEN
            rShelf_Refrig_Expansion_Valve_Duty := 0.0;
            rShelf_Electric_Heater_PWM_Duty := 25.0;
        ELSE
            rShelf_Refrig_Expansion_Valve_Duty := 10.0;
            rShelf_Electric_Heater_PWM_Duty := 8.0;
        END_IF;

        (* Transition to freezing when loading is complete and isolator confirmed sealed *)
        IF (tFSM_State_Timer >= T#120S) AND bIsolator_Interlock_Healthy THEN
            iFSM_Current_State := 3; (* Atmospheric Freezing *)
            bFSM_State_Entry_Flag := TRUE;
            tFSM_State_Timer := T#0S;
            rFSM_Ramp_Start_Temp := rVoted_Shelf_Mean_Temp;
            rFSM_Ramp_Target_Temp := rRecipe_Freezing_Shelf_Target; (* -45.0 deg C *)
            rFSM_Ramp_Slope_DegMin := -0.50; (* -0.5 deg C / min ramp *)
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 3: ATMOSPHERIC FREEZING (-45.0 DEG C SOAK, ANNEALING NUCLEATION)                                *)
    (* ----------------------------------------------------------------------------------------------------- *)
    3:
        iActive_FSM_State_ID := 3;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Dynamic temperature ramp profile generation *)
        IF rFSM_Ramp_Current_SP > rFSM_Ramp_Target_Temp THEN
            rFSM_Ramp_Current_SP := rFSM_Ramp_Current_SP + (rFSM_Ramp_Slope_DegMin * (rDelta_Time_Sec / 60.0));
            IF rFSM_Ramp_Current_SP <= rFSM_Ramp_Target_Temp THEN
                rFSM_Ramp_Current_SP := rFSM_Ramp_Target_Temp;
                bFSM_Ramp_Complete := TRUE;
            END_IF;
        END_IF;

        (* Freezing thermal soak verification (Ensure ice core <= -40.0 deg C for minimum 120 minutes) *)
        IF bFSM_Ramp_Complete AND (rVoted_Product_Cake_Temp <= -40.0) THEN
            IF tFSM_State_Timer >= T#7200S THEN (* 2 hours soak complete *)
                bFSM_Soak_Complete := TRUE;
                iFSM_Current_State := 4; (* Chill condenser *)
                bFSM_State_Entry_Flag := TRUE;
                tFSM_State_Timer := T#0S;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 4: ICE CONDENSER CHILL-DOWN (-75.0 DEG C COIL TEMPERATURE)                                      *)
    (* ----------------------------------------------------------------------------------------------------- *)
    4:
        iActive_FSM_State_ID := 4;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Keep shelves frozen at -45.0 deg C while pulling down condenser *)
        rFSM_Ramp_Current_SP := -45.0;
        
        (* Engage maximum condenser cascade refrigeration *)
        rCondenser_Refrig_Expansion_Valve_Duty := 100.0;
        bChamber_Isolation_Spool_Valve_Open := FALSE; (* Isolation valve closed during chill-down *)

        (* Condenser coil must reach <= -70.0 deg C before vacuum pull-down *)
        IF rVoted_Condenser_Coil_Temp <= -70.0 THEN
            iFSM_Current_State := 5; (* Vacuum Pull-Down *)
            bFSM_State_Entry_Flag := TRUE;
            tFSM_State_Timer := T#0S;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 5: PRIMARY DRYING VACUUM PULL-DOWN (ROUGHING + ROOTS BOOSTER DOWN TO 0.100 MBAR)                *)
    (* ----------------------------------------------------------------------------------------------------- *)
    5:
        iActive_FSM_State_ID := 5;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Maintain frozen shelves at -45 deg C *)
        rFSM_Ramp_Current_SP := -45.0;
        rCondenser_Refrig_Expansion_Valve_Duty := 90.0;

        (* Sequence vacuum pump package *)
        rVacuum_Roughing_Screw_VFD_Speed := 100.0;
        
        (* Start Roots booster once roughing pressure drops below cut-in threshold (20 mbar) *)
        IF rVoted_Chamber_Baratron_Press < 20.0 THEN
            rVacuum_Booster_Roots_VFD_Speed := 100.0;
            bChamber_Isolation_Spool_Valve_Open := TRUE; (* Open main chamber spool *)
        END_IF;

        (* Transition to sublimation ramp when chamber reaches target primary vacuum *)
        IF (rVoted_Chamber_Baratron_Press <= (rRecipe_Primary_Chamber_Press_SP + 0.020)) AND 
           (rVoted_Chamber_Baratron_Press > 0.001) THEN
            iFSM_Current_State := 6; (* Primary Sublimation Ramp *)
            bFSM_State_Entry_Flag := TRUE;
            tFSM_State_Timer := T#0S;
            rFSM_Ramp_Start_Temp := rVoted_Shelf_Mean_Temp;
            rFSM_Ramp_Target_Temp := rRecipe_Primary_Shelf_Target; (* -15.0 deg C *)
            rFSM_Ramp_Slope_DegMin := 0.25; (* +0.25 deg C/min *)
            bFSM_Ramp_Complete := FALSE;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 6: PRIMARY DRYING SUBLIMATION RAMP & HOLD (CONTROLLED N2 BLEED AT 0.090 MBAR)                   *)
    (* ----------------------------------------------------------------------------------------------------- *)
    6:
        iActive_FSM_State_ID := 6;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;
        tMTM_Interval_Timer := tMTM_Interval_Timer + tCycle_Sample_Time_Ts;

        (* Ramp shelf temperature up to primary drying setpoint *)
        IF rFSM_Ramp_Current_SP < rFSM_Ramp_Target_Temp THEN
            rFSM_Ramp_Current_SP := rFSM_Ramp_Current_SP + (rFSM_Ramp_Slope_DegMin * (rDelta_Time_Sec / 60.0));
            IF rFSM_Ramp_Current_SP >= rFSM_Ramp_Target_Temp THEN
                rFSM_Ramp_Current_SP := rFSM_Ramp_Target_Temp;
                bFSM_Ramp_Complete := TRUE;
            END_IF;
        END_IF;

        (* Active chamber pressure regulation via sterile N2 piezo micro-bleed *)
        IF rVoted_Chamber_Baratron_Press < rRecipe_Primary_Chamber_Press_SP THEN
            rNitrogen_MicroBleed_Piezo_Valve_Duty := (rRecipe_Primary_Chamber_Press_SP - rVoted_Chamber_Baratron_Press) * 1200.0;
            IF rNitrogen_MicroBleed_Piezo_Valve_Duty > 100.0 THEN
                rNitrogen_MicroBleed_Piezo_Valve_Duty := 100.0;
            END_IF;
        ELSE
            rNitrogen_MicroBleed_Piezo_Valve_Duty := 0.0;
        END_IF;

        (* Check Cake Collapse Safety Margin: Delta_T = Tc - Ti *)
        rCake_Collapse_Safety_Margin := rRecipe_Collapse_Temp_Limit - rVoted_Product_Cake_Temp;
        IF rCake_Collapse_Safety_Margin < 2.0 THEN
            (* Cake collapse proximity clamp: immediately throttle shelf heating *)
            rShelf_Electric_Heater_PWM_Duty := 0.0;
            rShelf_Refrig_Expansion_Valve_Duty := 30.0;
        END_IF;

        (* Periodic MTM or Sublimation Ratio convergence triggers verification *)
        IF (rSublimation_Endpoint_Pirani_Ratio <= 1.050) OR (tMTM_Interval_Timer >= tMTM_Periodic_Interval) OR bCmd_Manual_MTM_Trigger THEN
            iFSM_Current_State := 7; (* Manometric Endpoint Verification *)
            bFSM_State_Entry_Flag := TRUE;
            tMTM_Interval_Timer := T#0S;
            tMTM_Timer := T#0S;
            iMTM_Sample_Index := 0;
            bMTM_Pulse_Active := TRUE;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 7: MANOMETRIC ENDPOINT VERIFICATION & PRESSURE RISE ANALYSIS (PRA)                             *)
    (* ----------------------------------------------------------------------------------------------------- *)
    7:
        iActive_FSM_State_ID := 7;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;
        tMTM_Timer := tMTM_Timer + tCycle_Sample_Time_Ts;

        (* Close DN500 main chamber isolation spool valve for 25.0 seconds *)
        bChamber_Isolation_Spool_Valve_Open := FALSE;
        rNitrogen_MicroBleed_Piezo_Valve_Duty := 0.0; (* Inhibit gas bleed during test *)

        (* Record pressure rise trajectory points *)
        IF tMTM_Timer = tCycle_Sample_Time_Ts THEN
            rMTM_Press_P0 := rVoted_Chamber_Baratron_Press;
        ELSIF (tMTM_Timer >= T#5S) AND (rMTM_Press_P1 = 0.0) THEN
            rMTM_Press_P1 := rVoted_Chamber_Baratron_Press;
        ELSIF (tMTM_Timer >= T#10S) AND (rMTM_Press_P2 = 0.0) THEN
            rMTM_Press_P2 := rVoted_Chamber_Baratron_Press;
        ELSIF (tMTM_Timer >= T#15S) AND (rMTM_Press_P3 = 0.0) THEN
            rMTM_Press_P3 := rVoted_Chamber_Baratron_Press;
        ELSIF (tMTM_Timer >= T#20S) AND (rMTM_Press_P4 = 0.0) THEN
            rMTM_Press_P4 := rVoted_Chamber_Baratron_Press;
        ELSIF tMTM_Timer >= T#25S THEN
            rMTM_Press_P5 := rVoted_Chamber_Baratron_Press;
            rMTM_Delta_P_Rise := rMTM_Press_P5 - rMTM_Press_P0;

            (* Re-open main chamber isolation spool valve immediately *)
            bChamber_Isolation_Spool_Valve_Open := TRUE;
            bMTM_Pulse_Active := FALSE;

            (* Fit equilibrium vapor pressure P_eq and estimate ice interface temperature Ti *)
            IF rMTM_Delta_P_Rise > 0.001 THEN
                rMTM_Fitted_P_eq := rMTM_Press_P5 + (rMTM_Press_P5 - rMTM_Press_P4) * 0.50;
                IF rMTM_Fitted_P_eq > 0.0001 THEN
                    rLog10_P_eq := 0.434294 * LN(rMTM_Fitted_P_eq);
                    rMTM_Computed_Ti := (2667.0 / (10.5553 - rLog10_P_eq)) - 273.15;
                    rSublimation_Interface_Temp_MTM := rMTM_Computed_Ti;
                END_IF;
            END_IF;

            (* Check Sublimation Endpoint Criteria:
               1. Pressure rise Delta_P < 0.012 mbar in 25 s (no sublimating ice remaining)
               2. Pirani / Baratron ratio <= 1.025 (100% N2 environment, water vapor exhausted)
            *)
            IF (rMTM_Delta_P_Rise < 0.012) AND (rSublimation_Endpoint_Pirani_Ratio <= 1.025) THEN
                bSublimation_Primary_Endpoint_Active := TRUE;
                iFSM_Current_State := 8; (* Proceed to Secondary Drying Ramp *)
                bFSM_State_Entry_Flag := TRUE;
                tFSM_State_Timer := T#0S;
                rFSM_Ramp_Start_Temp := rVoted_Shelf_Mean_Temp;
                rFSM_Ramp_Target_Temp := rRecipe_Secondary_Shelf_Target; (* +25.0 deg C *)
                rFSM_Ramp_Slope_DegMin := 0.20; (* +0.20 deg C/min *)
            ELSE
                (* Sublimation still underway; return to State 6 for continued drying *)
                iFSM_Current_State := 6;
                rMTM_Press_P0 := 0.0;
                rMTM_Press_P1 := 0.0;
                rMTM_Press_P2 := 0.0;
                rMTM_Press_P3 := 0.0;
                rMTM_Press_P4 := 0.0;
                rMTM_Press_P5 := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 8: SECONDARY DESORPTION HEATING RAMP (+25.0 DEG C AT +0.20 DEG C/MIN, DEEP VACUUM)             *)
    (* ----------------------------------------------------------------------------------------------------- *)
    8:
        iActive_FSM_State_ID := 8;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Turn off N2 bleed to achieve ultimate deep vacuum for moisture desorption *)
        rNitrogen_MicroBleed_Piezo_Valve_Duty := 0.0;
        bChamber_Isolation_Spool_Valve_Open := TRUE;
        rVacuum_Roughing_Screw_VFD_Speed := 100.0;
        rVacuum_Booster_Roots_VFD_Speed := 100.0;

        (* Controlled shelf heating ramp to +25.0 deg C *)
        IF rFSM_Ramp_Current_SP < rFSM_Ramp_Target_Temp THEN
            rFSM_Ramp_Current_SP := rFSM_Ramp_Current_SP + (rFSM_Ramp_Slope_DegMin * (rDelta_Time_Sec / 60.0));
            IF rFSM_Ramp_Current_SP >= rFSM_Ramp_Target_Temp THEN
                rFSM_Ramp_Current_SP := rFSM_Ramp_Target_Temp;
                bFSM_Ramp_Complete := TRUE;
                iFSM_Current_State := 9; (* Isothermal Desorption Soak *)
                bFSM_State_Entry_Flag := TRUE;
                tFSM_State_Timer := T#0S;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 9: SECONDARY DRYING ISOTHERMAL SOAK (+25.0 DEG C HOLD, MOISTURE < 1.0%)                         *)
    (* ----------------------------------------------------------------------------------------------------- *)
    9:
        iActive_FSM_State_ID := 9;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        rFSM_Ramp_Current_SP := rRecipe_Secondary_Shelf_Target;
        rNitrogen_MicroBleed_Piezo_Valve_Duty := 0.0;

        (* Isothermal desorption soak verification (>= 6 hours soak and estimated moisture <= 0.8%) *)
        IF (tFSM_State_Timer >= T#21600S) AND (rEstimated_Residual_Moisture <= 0.80) THEN
            iFSM_Current_State := 10; (* Sterile Nitrogen Backfill *)
            bFSM_State_Entry_Flag := TRUE;
            tFSM_State_Timer := T#0S;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 10: STERILE NITROGEN (N2) BACKFILL (CONTROLLED BACKFILL TO 800 MBAR)                            *)
    (* ----------------------------------------------------------------------------------------------------- *)
    10:
        iActive_FSM_State_ID := 10;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Isolate chamber from vacuum pumps *)
        bChamber_Isolation_Spool_Valve_Open := FALSE;
        rVacuum_Booster_Roots_VFD_Speed := 0.0;
        rVacuum_Roughing_Screw_VFD_Speed := 0.0;

        (* Open sterile N2 fast backfill valve until target pressure reached *)
        IF rVoted_Chamber_Baratron_Press < (rRecipe_Backfill_Target_Press - 5.0) THEN
            bNitrogen_Fast_Backfill_Valve_Open := TRUE;
        ELSE
            bNitrogen_Fast_Backfill_Valve_Open := FALSE;
            IF tFSM_State_Timer >= T#60S THEN
                iFSM_Current_State := 11; (* Hydraulic Stoppering *)
                bFSM_State_Entry_Flag := TRUE;
                tFSM_State_Timer := T#0S;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 11: HYDRAULIC SHELF STOPPERING COMPACTION (0 TO 180 KN CONTROLLED COMPRESSION RAMP)             *)
    (* ----------------------------------------------------------------------------------------------------- *)
    11:
        iActive_FSM_State_ID := 11;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Start hydraulic power unit pump *)
        bHydraulic_Power_Pack_Pump_Run := TRUE;

        (* Controlled hydraulic crosshead advance and force ramp *)
        IF rVoted_Stoppering_Actual_Force < rRecipe_Stoppering_Target_Force THEN
            rHydraulic_Stoppering_Servo_Valve := 45.0; (* Downward compaction command *)
        ELSE
            rHydraulic_Stoppering_Servo_Valve := 12.0; (* Hold force *)
            (* Hold compression force for 180 seconds to fully seat all 150,000 stoppers *)
            IF tFSM_State_Timer >= T#180S THEN
                rHydraulic_Stoppering_Servo_Valve := 0.0;
                bHydraulic_Power_Pack_Pump_Run := FALSE;
                iFSM_Current_State := 12; (* Aeration Break *)
                bFSM_State_Entry_Flag := TRUE;
                tFSM_State_Timer := T#0S;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 12: AERATION VACUUM BREAK (ATMOSPHERIC VENTING TO 1013 MBAR VIA 0.22 UM FILTER)                 *)
    (* ----------------------------------------------------------------------------------------------------- *)
    12:
        iActive_FSM_State_ID := 12;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Modulate sterile aeration break valve to equalize chamber with isolator *)
        IF rVoted_Chamber_Baratron_Press < 1005.0 THEN
            rSterile_Aeration_Break_Valve_Duty := 65.0;
        ELSE
            rSterile_Aeration_Break_Valve_Duty := 0.0;
            IF tFSM_State_Timer >= T#30S THEN
                iFSM_Current_State := 13; (* Aseptic Unloading *)
                bFSM_State_Entry_Flag := TRUE;
                tFSM_State_Timer := T#0S;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 13: ASEPTIC VIAL UNLOAD (SHELF EXTENSION & AUTOMATED ISOLATOR DISCHARGE)                        *)
    (* ----------------------------------------------------------------------------------------------------- *)
    13:
        iActive_FSM_State_ID := 13;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Raise shelves to unloading pitch position (110 mm) *)
        IF rShelf_Hydraulic_Position_LVDT < 110.0 THEN
            bHydraulic_Power_Pack_Pump_Run := TRUE;
            rHydraulic_Stoppering_Servo_Valve := -35.0; (* Upward retraction command *)
        ELSE
            rHydraulic_Stoppering_Servo_Valve := 0.0;
            bHydraulic_Power_Pack_Pump_Run := FALSE;
            bBatch_Lyophilization_Complete := TRUE;
        END_IF;

    (* ----------------------------------------------------------------------------------------------------- *)
    (* STAGE 14: EMERGENCY ABORT DEFROST & SAFE VENT                                                         *)
    (* ----------------------------------------------------------------------------------------------------- *)
    14:
        iActive_FSM_State_ID := 14;
        tFSM_State_Timer := tFSM_State_Timer + tCycle_Sample_Time_Ts;

        (* Trip all refrigeration and heating skids to fail-safe de-energized state *)
        rShelf_Electric_Heater_PWM_Duty := 0.0;
        rShelf_Refrig_Expansion_Valve_Duty := 0.0;
        rCondenser_Refrig_Expansion_Valve_Duty := 0.0;
        rVacuum_Roughing_Screw_VFD_Speed := 0.0;
        rVacuum_Booster_Roots_VFD_Speed := 0.0;
        bChamber_Isolation_Spool_Valve_Open := FALSE;
        rNitrogen_MicroBleed_Piezo_Valve_Duty := 0.0;
        rHydraulic_Stoppering_Servo_Valve := 0.0;
        bHydraulic_Power_Pack_Pump_Run := FALSE;
        rCIP_SIP_Steam_Modulating_Valve := 0.0;

        (* Open safe aeration break and engage condenser hot water defrost *)
        IF rVoted_Chamber_Baratron_Press < 1000.0 THEN
            rSterile_Aeration_Break_Valve_Duty := 80.0;
        ELSE
            rSterile_Aeration_Break_Valve_Duty := 0.0;
        END_IF;
        bCondenser_Defrost_Water_Valve_Open := TRUE;

        IF bCmd_Alarm_Reset AND NOT bCmd_Cycle_Abort THEN
            bCondenser_Defrost_Water_Valve_Open := FALSE;
            iFSM_Current_State := 0; (* Return to Standby *)
            bFSM_State_Entry_Flag := TRUE;
            tFSM_State_Timer := T#0S;
        END_IF;

END_CASE;
"""
    parts.append(phase4)

    # 9. PHASE 5: ISA-18.2 MULTI-TIER ALARMS & BIT-PACKED STATUS WORDS
    phase5 = """(* ========================================================================================================= *)
(* === PHASE 5: ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS WORDS ===                              *)
(* ========================================================================================================= *)

(* Shelf Silicone Oil Bulk Temperature Alarm Monitoring *)
IF rVoted_Shelf_Mean_Temp >= rAlarm_Limit_Shelf_HH THEN
    bTrip_Shelf_Temp_HH := TRUE;
ELSIF rVoted_Shelf_Mean_Temp <= (rAlarm_Limit_Shelf_HH - rAlarm_Deadband_Shelf) THEN
    IF bCmd_Alarm_Reset THEN
        bTrip_Shelf_Temp_HH := FALSE;
    END_IF;
END_IF;

IF rVoted_Shelf_Mean_Temp >= rAlarm_Limit_Shelf_H THEN
    bTrip_Shelf_Temp_H := TRUE;
ELSIF rVoted_Shelf_Mean_Temp <= (rAlarm_Limit_Shelf_H - rAlarm_Deadband_Shelf) THEN
    IF bCmd_Alarm_Reset THEN
        bTrip_Shelf_Temp_H := FALSE;
    END_IF;
END_IF;

IF rVoted_Shelf_Mean_Temp <= rAlarm_Limit_Shelf_LL THEN
    bTrip_Shelf_Temp_LL := TRUE;
ELSIF rVoted_Shelf_Mean_Temp >= (rAlarm_Limit_Shelf_LL + rAlarm_Deadband_Shelf) THEN
    IF bCmd_Alarm_Reset THEN
        bTrip_Shelf_Temp_LL := FALSE;
    END_IF;
END_IF;

IF rVoted_Shelf_Mean_Temp <= rAlarm_Limit_Shelf_L THEN
    bTrip_Shelf_Temp_L := TRUE;
ELSIF rVoted_Shelf_Mean_Temp >= (rAlarm_Limit_Shelf_L + rAlarm_Deadband_Shelf) THEN
    IF bCmd_Alarm_Reset THEN
        bTrip_Shelf_Temp_L := FALSE;
    END_IF;
END_IF;

(* Chamber Pressure Alarm Monitoring during Primary Sublimation *)
IF (iFSM_Current_State = 5) OR (iFSM_Current_State = 6) OR (iFSM_Current_State = 7) THEN
    IF rVoted_Chamber_Baratron_Press >= rAlarm_Limit_Press_HH THEN
        bTrip_Press_HH := TRUE;
    ELSIF rVoted_Chamber_Baratron_Press <= (rAlarm_Limit_Press_HH - rAlarm_Deadband_Press) THEN
        IF bCmd_Alarm_Reset THEN
            bTrip_Press_HH := FALSE;
        END_IF;
    END_IF;

    IF rVoted_Chamber_Baratron_Press >= rAlarm_Limit_Press_H THEN
        bTrip_Press_H := TRUE;
    ELSIF rVoted_Chamber_Baratron_Press <= (rAlarm_Limit_Press_H - rAlarm_Deadband_Press) THEN
        IF bCmd_Alarm_Reset THEN
            bTrip_Press_H := FALSE;
        END_IF;
    END_IF;
END_IF;

(* Product Cake Collapse Margin Critical Proximity Alarm *)
IF (iFSM_Current_State = 6) OR (iFSM_Current_State = 7) THEN
    IF rCake_Collapse_Safety_Margin <= rAlarm_Limit_Collapse_Trip THEN
        bTrip_Collapse_Crit := TRUE;
    ELSIF rCake_Collapse_Safety_Margin >= (rAlarm_Limit_Collapse_Trip + 1.0) THEN
        IF bCmd_Alarm_Reset THEN
            bTrip_Collapse_Crit := FALSE;
        END_IF;
    END_IF;
END_IF;

(* Hydraulic Stoppering Compaction Force Overload Monitoring *)
IF rVoted_Stoppering_Actual_Force >= rAlarm_Limit_Force_HH THEN
    bTrip_Force_HH := TRUE;
ELSIF rVoted_Stoppering_Actual_Force <= (rAlarm_Limit_Force_HH - rAlarm_Deadband_Force) THEN
    IF bCmd_Alarm_Reset THEN
        bTrip_Force_HH := FALSE;
    END_IF;
END_IF;

(* Aseptic Isolator Sterile Barrier Containment Interlock *)
IF NOT bIsolator_Interlock_Healthy AND (iFSM_Current_State >= 1) AND (iFSM_Current_State <= 13) THEN
    bTrip_Isolator_Lost := TRUE;
ELSE
    IF bCmd_Alarm_Reset THEN
        bTrip_Isolator_Lost := FALSE;
    END_IF;
END_IF;

(* Refrigeration High Stage Compressor Discharge Pressure Safety Interlock *)
IF rRefrig_HighStage_Disch_Press >= 26.0 THEN
    bTrip_Refrig_HiDisch := TRUE;
ELSIF rRefrig_HighStage_Disch_Press <= 22.0 THEN
    IF bCmd_Alarm_Reset THEN
        bTrip_Refrig_HiDisch := FALSE;
    END_IF;
END_IF;

(* Aggregate ISA-18.2 Alarm Severity Tiers *)
bAlarm_ISA18_Warning_Active := bTrip_Shelf_Temp_H OR bTrip_Shelf_Temp_L OR bTrip_Press_H OR
                               (iTMR_Ch1_DegradedMode = 1) OR (iTMR_Ch4_DegradedMode = 1);

bAlarm_ISA18_Critical_Active := bTrip_Shelf_Temp_HH OR bTrip_Shelf_Temp_LL OR bTrip_Press_HH OR
                                bTrip_Collapse_Crit OR bTrip_Force_HH OR (iTMR_Ch4_DegradedMode >= 2);

bAlarm_ISA18_Emergency_Trip := bTrip_Isolator_Lost OR bTrip_Refrig_HiDisch OR bTrip_TMR_Ch4_Fail;

(* --------------------------------------------------------------------------------------------------------- *)
(* BIT-PACKED 32-BIT DIAGNOSTIC & STATUS WORDS                                                               *)
(* --------------------------------------------------------------------------------------------------------- *)
(* dwStatus_Word_Subsystems: Subsystem Operational Readiness *)
dwStatus_Word_Subsystems := 16#00000000;
IF bChamber_Isolation_Spool_Valve_Open   THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000001; END_IF;
IF bHydraulic_Power_Pack_Pump_Run        THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000002; END_IF;
IF bNitrogen_Fast_Backfill_Valve_Open    THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000004; END_IF;
IF bCondenser_Defrost_Water_Valve_Open   THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000008; END_IF;
IF bMTM_Pulse_Active                     THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000010; END_IF;
IF bSublimation_Primary_Endpoint_Active  THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000020; END_IF;
IF bBatch_Lyophilization_Complete        THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000040; END_IF;
IF bIsolator_Interlock_Healthy           THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000080; END_IF;
IF rVacuum_Roughing_Screw_VFD_Speed > 5.0 THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000100; END_IF;
IF rVacuum_Booster_Roots_VFD_Speed > 5.0  THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000200; END_IF;
IF rShelf_Electric_Heater_PWM_Duty > 1.0  THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000400; END_IF;
IF rShelf_Refrig_Expansion_Valve_Duty > 1.0 THEN dwStatus_Word_Subsystems := dwStatus_Word_Subsystems OR 16#00000800; END_IF;

(* dwStatus_Word_TMR_Health: 2oo3 Sensor Channel Integrity & Degradation Status *)
dwStatus_Word_TMR_Health := 16#00000000;
IF bTMR_Ch1_A_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000001; END_IF;
IF bTMR_Ch1_B_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000002; END_IF;
IF bTMR_Ch1_C_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000004; END_IF;
IF bTMR_Ch2_A_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000008; END_IF;
IF bTMR_Ch2_B_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000010; END_IF;
IF bTMR_Ch2_C_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000020; END_IF;
IF bTMR_Ch3_A_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000040; END_IF;
IF bTMR_Ch3_B_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000080; END_IF;
IF bTMR_Ch3_C_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000100; END_IF;
IF bTMR_Ch4_A_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000200; END_IF;
IF bTMR_Ch4_B_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000400; END_IF;
IF bTMR_Ch4_C_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00000800; END_IF;
IF bTMR_Ch5_A_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00001000; END_IF;
IF bTMR_Ch5_B_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00002000; END_IF;
IF bTMR_Ch5_C_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00004000; END_IF;
IF bTMR_Ch6_A_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00008000; END_IF;
IF bTMR_Ch6_B_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00010000; END_IF;
IF bTMR_Ch6_C_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00020000; END_IF;
IF bTMR_Ch7_A_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00040000; END_IF;
IF bTMR_Ch7_B_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00080000; END_IF;
IF bTMR_Ch7_C_Healthy THEN dwStatus_Word_TMR_Health := dwStatus_Word_TMR_Health OR 16#00100000; END_IF;

(* dwAlarm_Word_Process_Trips: Process Out of Tolerance Trips *)
dwAlarm_Word_Process_Trips := 16#00000000;
IF bTrip_Shelf_Temp_HH THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000001; END_IF;
IF bTrip_Shelf_Temp_H  THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000002; END_IF;
IF bTrip_Shelf_Temp_L  THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000004; END_IF;
IF bTrip_Shelf_Temp_LL THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000008; END_IF;
IF bTrip_Press_HH      THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000010; END_IF;
IF bTrip_Press_H       THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000020; END_IF;
IF bTrip_Press_L       THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000040; END_IF;
IF bTrip_Press_LL      THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000080; END_IF;
IF bTrip_Collapse_Crit THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000100; END_IF;
IF bTrip_Force_HH      THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000200; END_IF;
IF bTrip_Force_H       THEN dwAlarm_Word_Process_Trips := dwAlarm_Word_Process_Trips OR 16#00000400; END_IF;

(* dwAlarm_Word_Interlocks: Equipment & Safety Interlocks *)
dwAlarm_Word_Interlocks := 16#00000000;
IF bTrip_Isolator_Lost  THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000001; END_IF;
IF bTrip_Refrig_HiDisch THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000002; END_IF;
IF bTrip_TMR_Ch1_Fail   THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000004; END_IF;
IF bTrip_TMR_Ch2_Fail   THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000008; END_IF;
IF bTrip_TMR_Ch3_Fail   THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000010; END_IF;
IF bTrip_TMR_Ch4_Fail   THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000020; END_IF;
IF bTrip_TMR_Ch5_Fail   THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000040; END_IF;
IF bTrip_TMR_Ch6_Fail   THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000080; END_IF;
IF bTrip_TMR_Ch7_Fail   THEN dwAlarm_Word_Interlocks := dwAlarm_Word_Interlocks OR 16#00000100; END_IF;

END_FUNCTION_BLOCK
"""
    parts.append(phase5)

    return "".join(parts)

code = generate_st_code()
print("Generated Code Length:", len(code))


def save_dataset():
    prompt = USER_PROMPT
    st_code = generate_st_code()
    content = "```iec-st\n" + st_code.strip() + "\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": content}
        ]
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"Saved dataset to {filename}")
    return filename

if __name__ == "__main__":
    fn = save_dataset()
    print("Testing validator on saved file:")
    import subprocess
    res = subprocess.run([sys.executable, "validate_iec.py", fn], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
