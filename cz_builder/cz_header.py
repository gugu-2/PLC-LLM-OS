# cz_builder/cz_header.py

def get_header():
    return """FUNCTION_BLOCK FB_Semiconductor_Czochralski_IngotPuller_Furnace
(*
  ==========================================================================================
  PROJECT:       300 mm HIGH-PURITY SILICON SINGLE-CRYSTAL CZOCHRALSKI (CZ) INGOT PULLER FURNACE
  SUBSYSTEM:     MULTI-ZONE INDUCTION/RESISTANCE HEATING & OPTICAL MENISCUS CLOSED-LOOP CONTROL
  DISCIPLINE:    HIGH-TEMPERATURE VACUUM / SEMICONDUCTOR CRYSTAL GROWTH / STEFAN MULTIPHYSICS / MPC
  IEC STANDARD:  IEC 61131-3 3RD EDITION (DETERMINISTIC EMBEDDED REAL-TIME CONTROL)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  OPERATING RANGE: 1,414.0 DEG C (MELT INTERFACE) | VACUUM: 15.0 TO 30.0 mbar (ARGON PURGE)
  INGOT CAPACITY:  300 mm DIAMETER (+/- 0.3 mm) x 1,800 mm BODY LENGTH | 350 kg INITIAL CHARGE
  CRUCIBLE SIZE:   32 INCH (812.8 mm O.D.) SYNTHETIC QUARTZ (SiO2) IN GRAPHITE SUSCEPTOR
  PULL MECHANISM:  SUB-MICRON PRECISION WIRE-CABLE SERVO LIFT WITH LOAD CELL TARE COMPENSATION

  PROCESS CYBER-PHYSICAL GOVERNING PRINCIPLES:

  1. HIGH-TEMPERATURE VACUUM THERMAL ENVIRONMENT & MULTI-ZONE HEATING:
     The crystal growth furnace operates under a high-purity inert Argon atmosphere maintained at
     15.0 to 30.0 mbar by a closed-loop vacuum throttle valve and mass flow controller (MFC).
     Continuous Ar downward purge (80 to 120 slpm) sweeps away volatile silicon monoxide (SiO)
     gas formed by the endothermic reaction between the molten silicon and the quartz crucible:
         SiO2(s) + Si(l) <===> 2 SiO(g)
     If SiO gas condenses on cooler graphite surfaces or the seed crystal, solid SiO particles
     fall back into the melt, causing catastrophic crystal polycrystallization (loss of structure).
     The thermal field is driven by multi-zone graphite heaters:
       - Upper Side Heater (SCR phase-angle power control, nominal 90 - 130 kW)
       - Lower Side Heater (SCR phase-angle power control, nominal 70 - 110 kW)
       - Bottom Resistance/Induction Heater (SCR power control, nominal 35 - 65 kW)
     These zones establish precise axial and radial temperature gradients in the 350 kg melt
     to maintain the solid-liquid crystallization isotherm at exactly 1,414.0 deg C.

  2. STEFAN SOLID-LIQUID PHASE BOUNDARY & LATENT HEAT REJECTION:
     At the crystallization boundary where single-crystal silicon solidifies from the molten pool,
     the phase change releases an immense latent heat of fusion:
         L_f = 1.80 x 10^6 J/kg  (rho_solid = 2,330 kg/m3, rho_liquid = 2,570 kg/m3)
     The local energy conservation is governed by the two-phase Stefan condition:
         k_s * (dT_s / dz) - k_l * (dT_l / dz) = rho_s * L_f * v_growth
     where k_s = 22.0 W/(m*K) (solid silicon conductivity at melting point),
           k_l = 64.0 W/(m*K) (molten silicon thermal conductivity),
           v_growth is the instantaneous vertical crystallization growth velocity.
     Any increase in seed pull velocity v_pull increases the latent heat generation rate,
     which warms the local interface and retards radial crystal expansion. Conversely,
     slowing down the pull rate allows conduction into the ingot body to dominate, accelerating
     solidification and expanding the crystal radius.

  3. CAPILLARY MENISCUS OPTICAL SENSING & LAPLACE-YOUNG GEOMETRY:
     A bright meniscus ring forms around the tri-junction where the liquid melt climbs the solid
     crystal cylinder due to capillary surface tension (sigma_Si = 0.720 N/m at 1,414 deg C).
     The meniscus acts as an optical reflector, reflecting radiation from the hot crucible wall
     into an overhead optical CCD camera and laser triangulation pyrometer.
     The Laplace-Young capillary equation governs the meniscus profile height:
         h_m = SQRT( 2 * a^2 * SIN^2(phi_L / 2) )
     where a = SQRT( 2 * sigma_Si / (rho_l * g) ) = 7.56 mm is the capillary constant,
     and phi_L is the dynamic growth contact angle.
     - For steady cylindrical growth of silicon (<100> or <111> orientation):
           phi_L = theta_L = 11.0 deg (Zero radial growth: dR_c / dt = 0)
     - If phi_L > 11.0 deg, the crystal radius is expanding (dR_c / dt > 0, shoulder expansion)
     - If phi_L < 11.0 deg, the crystal radius is contracting (dR_c / dt < 0, tail-off tapering)
     The closed-loop optical vision system processes the bright ring image to extract:
       a) Solid crystal diameter D_c [mm]
       b) Meniscus height h_m [mm]
       c) Contact growth angle phi_L [deg]
       d) Solid-liquid interface vertical position z_int [mm]

  4. DASH NECKING & DISLOCATION SUPPRESSION DYNAMICS:
     Upon dipping the seed crystal into the molten silicon at 1,420 deg C, severe thermal shock
     generates dense dislocation networks (slip lines) propagating along the {111} crystallographic
     planes. To eliminate dislocations before initiating the large 300 mm body, the Dash Necking
     procedure is executed:
       - The pull speed is accelerated rapidly to 4.5 - 6.0 mm/min.
       - The diameter is squeezed down to 3.0 - 4.0 mm.
       - The neck is pulled over a length of 200 to 300 mm.
     Under this high growth velocity and narrow geometry, dislocations glide at an angle to the
     growth axis and terminate at the free crystal surface, leaving the growing crystal core
     100% dislocation-free (confirmed optically by the sharp development of 4 crystal habit lines).

  5. VORONKOV DEFECT CRITERION (v/G) POINT DEFECT MANAGEMENT:
     In ultra-pure 300 mm silicon for sub-3nm semiconductor fabrication, microscopic point defect
     clusters (vacancies vs self-interstitials) must be completely suppressed across the entire wafer.
     Voronkov's theory dictates that the point defect incorporation is governed by the ratio:
         xi = v_growth / G_0   [mm2 / (min * K)]
     where G_0 = |dT/dz|_interface is the axial thermal gradient at the solid-liquid interface.
       - Critical Voronkov Ratio: xi_crit = 0.22 mm2 / (min * K)
       - If xi > xi_crit: Vacancy-dominant regime -> Agglomerated Crystal-Originated Pits (COPs)
       - If xi < xi_crit: Interstitial-dominant regime -> A-swirl dislocation loops / B-defects
       - Pure Defect-Free Window: 0.20 <= xi <= 0.24 mm2 / (min * K)
     The Function Block dynamically coordinates pull speed v_pull and multi-zone heater balance
     to constrain xi within the defect-free window across the entire 1,800 mm ingot length.

  6. CRUCIBLE LIFT KINEMATICS & MASS CONTINUITY:
     As solid silicon is extracted from the melt, the liquid surface in the quartz crucible drops.
     To maintain the melt surface at the exact focal plane of the optical cameras and heat shield,
     the quartz crucible must be lifted upward by the crucible servo drive.
     Mass conservation across the crucible and crystal:
         v_drop = v_pull * (rho_s / rho_l) * (R_crystal^2 / (R_crucible^2 - R_crystal^2))
     Crucible lift velocity setpoint:
         v_crucible = v_drop + K_level * (z_target - z_measured)
     Simultaneously, crucible counter-rotation (3 to 10 rpm) and seed rotation (10 to 22 rpm)
     suppress Marangoni thermocapillary vortices, ensuring radial oxygen and dopant homogeneity.

  7. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC):
     A discrete 12-state, 8-input state-space formulation models the coupled thermo-mechanical
     interactions. A real-time unrolled Projected Gradient Descent quadratic program optimizes:
       - Seed pull speed [mm/min]
       - Crucible lift speed [mm/min]
       - Upper, Lower, and Bottom heater powers [kW]
       - Seed and Crucible rotation speeds [rpm]
       - Argon purge flow rate [slpm]
     subject to hard actuator bounds, thermal slew limits, and Voronkov defect envelope constraints.

  8. TRIPLE MODULAR REDUNDANCY (2oo3) & ISA-18.2 ALARMS:
     Triple redundant optical pyrometers, CCD cameras, capacitance vacuum manometers, laser level
     sensors, and Type B thermocouples execute median selection and pair-wise deviation voting.
     A 12-stage Finite State Machine and bit-packed telemetry words enforce SIL-3 plant protection.
  ==========================================================================================
*)
"""
