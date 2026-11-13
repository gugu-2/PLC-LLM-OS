# cz_silicon_builder/mod_header_io.py
# -*- coding: utf-8 -*-

def generate_header_io():
    return """FUNCTION_BLOCK FB_Semiconductor_Czochralski_SiliconIngot_MeltThermal_Puller
(*
  ==========================================================================================
  PROJECT:       300 mm HIGH-PURITY SINGLE-CRYSTAL SILICON CZOCHRALSKI (CZ) PULLER FURNACE
  SUBSYSTEM:     MULTI-ZONE THERMAL, ELECTROMAGNETIC CUSP FIELD & OPTICAL MENISCUS PULL CONTROL
  DISCIPLINE:    ADVANCED CYBER-PHYSICAL SEMICONDUCTOR CRYSTAL GROWTH & RECESSED MPC AUTOMATION
  STANDARDS:     IEC 61131-3 3RD EDITION, SEMI E10, SEMI E30 (GEM), ISA-18.2 ALARM LIFECYCLE
  AUTHOR:        LUMINA AI INDUSTRIAL AUTOMATION ARCHITECT - PRINCIPAL CPS FELLOW (V7 MAX PERSONA)
  TARGET CHIP:   SUB-3nm NODE COMPLIANT DISLOCATION-FREE ULTRA-FLAT SILICON WAFER SUBSTRATE
  
  PHYSICAL SYSTEM SPECIFICATIONS & CONSTRAINTS:
  - Nominal Wafer Substrate Diameter: 300.0 mm (+/- 0.25 mm tight optical tolerance band)
  - Max Ingot Length Capacity:        1,800.0 mm to 2,000.0 mm (Excluding Neck, Crown, and Tail)
  - Polysilicon Crucible Charge:      350.0 kg Electronic Grade Polysilicon (EG-Si 11N Purity)
  - Synthetic Quartz Crucible Size:   32.0 inch (812.8 mm O.D.) mounted in Isostatic Graphite Susceptor
  - Solidification Melting Point:    1,414.0 deg C (1,687.15 K)
  - High-Vacuum Base Pressure:       < 5.0e-3 mbar prior to backfill
  - Controlled Process Pressure:     15.0 mbar to 30.0 mbar under continuous high-purity Argon purge
  - Argon Purge Flow Rate:           80.0 to 140.0 slpm downward laminar purge for SiO gas removal
  
  CORE CYBER-PHYSICAL GOVERNING PHENOMENA:
  1. STEFAN PHASE BOUNDARY SOLID-LIQUID SOLIDIFICATION:
     Governed by the two-phase Stefan energy balance at the crystallization interface:
       k_s * (dT_s / dz) - k_l * (dT_l / dz) = rho_s * L_f * v_growth
     where:
       k_s   = 22.0 W/(m*K) (Solid silicon thermal conductivity near melting point)
       k_l   = 64.0 W/(m*K) (Liquid silicon thermal conductivity)
       rho_s = 2,330.0 kg/m3 (Solid silicon mass density)
       rho_l = 2,570.0 kg/m3 (Molten liquid silicon density)
       L_f   = 1.80e6 J/kg   (Latent heat of crystallization fusion)
       v_growth = Instantaneous vertical crystal growth rate [m/s]
     Dynamic modulation of pull speed v_pull directly shifts the latent heat generation rate,
     cooling or heating the local tri-junction contact line and expanding or shrinking diameter.

  2. CAPILLARY MENISCUS DYNAMICS & OPTICAL PYROMETRY TRIANGULATION:
     The solid-liquid-gas tri-junction forms a supported liquid meniscus governed by Laplace-Young:
       h_m = SQRT( 2.0 * gamma_m / (rho_l * g) * (1.0 - SIN(theta_c)) )
     where:
       gamma_m = 0.720 N/m (Molten silicon surface tension at 1,414 deg C)
       theta_c = Dynamic growth contact angle.
                 For cylindrical body growth (dR/dt = 0), theta_c = 11.0 deg.
                 For crown expansion (dR/dt > 0), theta_c > 11.0 deg.
                 For tail-off tapering (dR/dt < 0), theta_c < 11.0 deg.
     Optical high-speed pyrometer and CCD cameras detect the specular reflection ring of the
     meniscus to establish true crystal diameter and tri-junction interface temperature.

  3. CUSP ELECTROMAGNETIC FIELD CONVECTION SUPPRESSION (LORENTZ BRAKING):
     Opposing Helmholtz/cusp electromagnetic coils positioned above and below the melt surface
     generate a radial magnetic field across the melt surface and axial field near the bottom.
     Molten silicon is a metallic conductor (electrical conductivity sigma_e = 1.25e6 S/m).
     The induced Lorentz force:
       F_Lorentz = J x B = sigma_e * (v_melt x B) x B
     powerfully damps chaotic Rayleigh-Benard thermal buoyancy and Marangoni surface tension
     driven convection cells, suppressing temperature fluctuations from +/- 18 deg C down to < +/- 0.5 deg C.

  4. VORONKOV DEFECT MANAGEMENT CRITERION (v / G_0):
     To eliminate vacancy clustering (Crystal-Originated Pits, COPs) and interstitial dislocation
     loops (A-swirl and B-defects), the ratio of pull rate v to axial thermal gradient G_0
     is constrained within a strict defect-free boundary:
       xi = v_pull / G_0
       xi_crit = 0.220 mm2 / (min * K)
       Defect-Free Neutral Window: 0.200 <= xi <= 0.240 mm2 / (min * K)

  5. CONTINUOUS MASS CONTINUITY & CRUCIBLE LIFT KINEMATICS:
     As solid crystal mass is pulled from the crucible, the melt level drops:
       v_drop = v_pull * (rho_s / rho_l) * (R_crystal^2 / (R_crucible^2 - R_crystal^2))
     The bottom crucible lift drive dynamically tracks v_drop plus a closed-loop optical
     level correction to hold the melt surface locked at the focal plane of the heat shield.
  ==========================================================================================
*)
VAR_INPUT
    bEnable : BOOL; (* [bool] Master control enable request *)
    bAutoMode : BOOL; (* [bool] Automatic supervisory sequence enable *)
    bResetAlarm : BOOL; (* [bool] Master alarm acknowledge and trip reset *)
    bEmergencyStop : BOOL; (* [bool] Hardwired safety category 4 emergency trip *)
    rPyrometer_Meniscus_ChA : REAL; (* [deg C] Meniscus optical pyrometer channel A reading *)
    rPyrometer_Meniscus_ChB : REAL; (* [deg C] Meniscus optical pyrometer channel B reading *)
    rPyrometer_Meniscus_ChC : REAL; (* [deg C] Meniscus optical pyrometer channel C reading *)
    rCCD_Diameter_ChA : REAL; (* [mm] High-speed CCD optical diameter channel A *)
    rCCD_Diameter_ChB : REAL; (* [mm] High-speed CCD optical diameter channel B *)
    rCCD_Diameter_ChC : REAL; (* [mm] High-speed CCD optical diameter channel C *)
    rLoadCell_Weight_ChA : REAL; (* [kg] Seed suspension load cell channel A *)
    rLoadCell_Weight_ChB : REAL; (* [kg] Seed suspension load cell channel B *)
    rLoadCell_Weight_ChC : REAL; (* [kg] Seed suspension load cell channel C *)
    rHeater_TC_ChA : REAL; (* [deg C] Main graphite heater thermocouple channel A *)
    rHeater_TC_ChB : REAL; (* [deg C] Main graphite heater thermocouple channel B *)
    rHeater_TC_ChC : REAL; (* [deg C] Main graphite heater thermocouple channel C *)
    rChamberVacuumPressure : REAL; (* [mbar] Furnace chamber vacuum pressure *)
    rArgonPurgeMassFlow : REAL; (* [slpm] Argon inert gas mass flow rate *)
    rBottomCrucibleTC : REAL; (* [deg C] Crucible bottom susceptor thermocouple *)
    rCuspCoilCurrentActual : REAL; (* [A] Cusp magnetic field coil actual feedback current *)
    rCrystalPullSpeedActual : REAL; (* [mm/min] Crystal lift servo encoder speed feedback *)
    rCrucibleLiftSpeedActual : REAL; (* [mm/min] Crucible lift servo encoder speed feedback *)
    rSeedRotationSpeedActual : REAL; (* [RPM] Seed crystal rotation speed feedback *)
    rCrucibleRotationSpeedActual : REAL; (* [RPM] Crucible rotation speed feedback *)
    rCoolingWaterFlowPrimary : REAL; (* [L/min] Furnace chamber cooling water jacket flow *)
    rCoolingWaterTempPrimary : REAL; (* [deg C] Cooling water jacket inlet temperature *)
    rTargetIngotDiameter : REAL; (* [mm] Target single crystal ingot body diameter, nominal 300.0 mm *)
    rTargetGrowthLength : REAL; (* [mm] Target ingot total cylinder length, nominal 1800.0 mm *)
    rInitialSiliconChargeMass : REAL; (* [kg] Initial virgin polysilicon load mass in crucible, nominal 350.0 kg *)
    tCycleTime : TIME; (* [s] Deterministic task execution cycle time, nominal T#100MS *)
END_VAR
VAR_OUTPUT
    bSystemReady : BOOL; (* [bool] Ingot puller system ready for sequence start *)
    bSequenceActive : BOOL; (* [bool] Crystal growth sequence in active state *)
    bDislocationFreeStructure : BOOL; (* [bool] Zero dislocation status confirmed optically *)
    bVoronkovCriterionSatisfied : BOOL; (* [bool] V/G ratio within vacancy-interstitial neutral boundary *)
    iCurrentFSMState : INT; (* [state] Active FSM operating state index 0-13 *)
    rCrystalPullSpeedCmd : REAL; (* [mm/min] Crystal lift servo motor speed command *)
    rMainHeaterPowerCmd : REAL; (* [kW] Main graphite resistance heater thyristor power setpoint *)
    rCrucibleLiftSpeedCmd : REAL; (* [mm/min] Crucible vertical lift servo motor speed command *)
    rCuspCoilCurrentCmd : REAL; (* [A] Electromagnetic cusp coil DC current setpoint *)
    rSeedRotationCmd : REAL; (* [RPM] Crystal seed rotation motor speed command *)
    rCrucibleRotationCmd : REAL; (* [RPM] Crucible rotation motor speed command *)
    rArgonMFCFlowCmd : REAL; (* [slpm] Argon mass flow controller flow setpoint *)
    rVacuumThrottleValveCmd : REAL; (* [%] Vacuum throttle butterfly valve position setpoint *)
    rVotedMeniscusTemp : REAL; (* [deg C] 2oo3 voted meniscus tri-junction temperature *)
    rVotedIngotDiameter : REAL; (* [mm] 2oo3 voted crystal optical diameter *)
    rVotedCrystalWeight : REAL; (* [kg] 2oo3 voted crystal suspended weight *)
    rVotedHeaterTemp : REAL; (* [deg C] 2oo3 voted graphite heater temperature *)
    rEstimatedGrowthRate : REAL; (* [mm/min] Instantaneous Stefan boundary crystal solidification rate *)
    rCurrentVoronkovRatio : REAL; (* [mm2/(min*K)] Instantaneous V/G ratio *)
    rAccumulatedIngotLength : REAL; (* [mm] Total solidified crystal length *)
    rResidualMeltMass : REAL; (* [kg] Remaining molten silicon mass in crucible *)
    dwStatusWord1 : DWORD; (* [bitfield] Primary operational telemetry status word *)
    dwStatusWord2 : DWORD; (* [bitfield] Secondary process and crystallization status word *)
    dwAlarmWord1 : DWORD; (* [bitfield] Critical safety and hardware trip alarms *)
    dwAlarmWord2 : DWORD; (* [bitfield] Operational warning and degradation alarms *)
    dwFirstOutWord : DWORD; (* [bitfield] Root-cause first-out trip identifier *)
END_VAR"""
