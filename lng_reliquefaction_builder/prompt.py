# lng_reliquefaction_builder/prompt.py

def get_prompt():
    return """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Commercial Marine & Clean Energy Shipping (174,000 m3 LNG Carrier Boil-Off Gas Re-Liquefaction & Cryogenic Fuel Gas Handling System)**

**Function Block Name**: `FB_Marine_LNG_BoilOffGas_Reliquefaction_Cascade`

**Engineering Context & Operational Architecture**:
1. 174,000 m3 Membrane-Type (GTT Mark III Flex / NO96) LNG Carrier Cargo Boil-Off Dynamics:
   - Total cargo capacity 174,000 m3 distributed across 4 prismatic membrane tanks.
   - Design Natural Boil-Off Rate (NBOR): 0.085% volume per day laden voyage (approx. 4,200 kg/h methane vapor generated from ambient heat leak through reinforced polyurethane insulation).
   - Cargo tank ullage pressure operating envelope: 104.0 kPa to 125.0 kPa absolute (4.0 kPa to 25.0 kPa gauge).
   - Sloshing surge dynamics under severe sea state (Beaufort 7-9, significant wave height Hs > 6 m) inducing severe hydrodynamic pressure peaks and rapid ullage gas volume compression.
2. Nitrogen Reverse Brayton Cycle Cryogenic Subcooler Re-Liquefaction Plant:
   - Closed-loop Nitrogen refrigeration circuit operating between 12.0 bar and 45.0 bar.
   - High-speed Nitrogen compander (centrifugal compressor and cryogenic radial inflow expander coupled on common magnetic bearing shaft operating at up to 48,000 rpm).
   - Vacuum-brazed aluminum plate-fin heat exchanger (Cold Box) subcooling boil-off gas from -130.0 °C to -162.0 °C at 5.5 bar gauge, converting methane vapor back to saturated subcooled cryogenic liquid condensate.
   - Subcooled LNG condensate return header routing reliquefied liquid back to the bottom of Cargo Tanks 1 and 4 via submerged spray headers to minimize tank pressure regrowth.
3. Multi-Stage Centrifugal Boil-Off Gas (BOG) Compressor & Fuel Gas Handling (FGSS):
   - Two-stage variable speed centrifugal BOG compressor driven by 3.5 MW electric motor with active magnetic bearings.
   - Coordinated dual-mode dispatch: sendout to Low-Pressure Dual-Fuel 2-Stroke Main Propulsion Engines (WinGD X-DF / MAN ME-GA at 16.0 bar or 5.5 bar gauge) and Auxiliary Dual-Fuel Gensets, or 100% full reliquefaction back to cargo tanks during ballast/idle voyage.
   - Dynamic anti-surge control loop with fast-acting electro-pneumatic recycle valves (< 800 ms full stroke) and dynamic surge line decoupling.
   - Auxiliary thermal disposal: Gas Combustion Unit (GCU) / Methane Thermal Oxidizer capacity 5,000 kg/h for excess boil-off gas incineration during port congestion or canal transit where reliquefaction or engine consumption is restricted.
4. First-Principles 8-State Cyber-Physical Discrete State-Space Model (Ts = 20 ms = 0.020 s):
   - States:
     x1 = LNG Cargo Tank 1 Ullage Vapor Pressure [kPa gauge]
     x2 = LNG Cargo Tank 4 Ullage Vapor Pressure [kPa gauge]
     x3 = BOG Compressor Stage 1 Suction Temperature [deg C]
     x4 = BOG Compressor Stage 2 Discharge Pressure [kPa gauge]
     x5 = Nitrogen Compander Expander Outlet Temperature [deg C]
     x6 = Cold Box Subcooled LNG Condensate Temperature [deg C]
     x7 = Subcooled LNG Return Header Flow Rate [kg/h]
     x8 = Nitrogen Cycle Loop Mass Inventory [kg]
   - Control Actuators u (6 inputs):
     u1 = BOG Compressor Stage 1 Anti-Surge Bypass Valve [0..100%]
     u2 = BOG Compressor Stage 2 Anti-Surge Bypass Valve [0..100%]
     u3 = Nitrogen Compander Variable Inlet Guide Vanes (IGV) [0..100%]
     u4 = Subcooled LNG Condensate Return Control Valve [0..100%]
     u5 = Gas Combustion Unit (GCU) Fast-Dump Throttle Valve [0..100%]
     u6 = BOG Compressor Variable Frequency Drive (VFD) Speed [0..100%]
   - Full non-zero system matrices A (8x8), B (8x6), C (6x8), D (6x6).
   - Luenberger / steady-state Kalman innovation gain matrix L (8x6).
5. Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent:
   - Prediction horizon Np = 5 steps, 6 unrolled iterations of PGD.
   - Quadratic state tracking penalties Q, actuator effort penalties R, terminal cost P.
   - Surge margin avoidance penalty guaranteeing S_margin >= 1.15 across both compression stages.
   - Asymmetric slew rate limits on all actuators.
6. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting:
   - Tank 1 & 4 Ullage Vapor Pressure Transmitters: PT_ULLAGE_101A/B/C [kPa]
   - BOG Compressor Suction Pressure Transmitters: PT_SUCTION_201A/B/C [kPa]
   - BOG Compressor Discharge Differential Pressure: PDT_DISCH_301A/B/C [kPa]
   - Cryogenic Nitrogen Cold Box Temperature Sensors: TT_COLD_401A/B/C [deg C]
   - Subcooled LNG Condensate Coriolis Flowmeters: FT_COND_501A/B/C [kg/h]
   - Pairwise difference tolerance, 250 ms discrepancy timers, channel degradation (3oo3 -> 2oo3 -> 1oo2 -> trip).
7. Deterministic 14-Stage Production Finite State Machine (FSM):
   - Stage 0: PORT_STANDBY_AND_WARM_NITROGEN_INERT
   - Stage 1: REFRIGERATION_COLD_BOX_NITROGEN_DRY_RUN
   - Stage 2: BOG_COMPRESSOR_LUBE_OIL_AND_SEAL_GAS_LOCK
   - Stage 3: CARGO_TANK_PRESSURE_EQUILIBRIUM_CHECK
   - Stage 4: BOG_COMPRESSOR_STAGE1_SPINUP
   - Stage 5: BOG_COMPRESSOR_STAGE2_AND_ANTI_SURGE_LOCK
   - Stage 6: NITROGEN_COMPANDER_EXPANSION_CHILLDOWN (-160 deg C)
   - Stage 7: FULL_CONDENSATE_RELIQUEFACTION_OPTIMAL_MPC
   - Stage 8: DUAL_FUEL_ENGINE_FUEL_GAS_SENDOUT_COORDINATION
   - Stage 9: GCU_EXCESS_BOG_THERMAL_BURNING_MODE
   - Stage 10: ROUGH_SEA_SLOSHING_PRESSURE_SURGE_DAMPING
   - Stage 11: REFRIGERATION_LOOP_HOT_STANDBY_RECYCLE
   - Stage 12: EMERGENCY_CARGO_MAST_VENT_ISOLATION
   - Stage 13: SIL-3_QUICK_CLOSING_SAFETY_SHUTDOWN (ESD-1/2)
8. ISA-18.2 Process Alarms & 32-Bit Bit-Packed Telemetry:
   - Multi-tier alarms (HH, H, L, LL) with deadband hysteresis.
   - Emergency cargo mast venting interlock and GCU automatic light-off.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Marine_LNG_BoilOffGas_Reliquefaction_Cascade` with zero placeholders, complete state-space matrices, unrolled MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""
