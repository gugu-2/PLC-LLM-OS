FUNCTION_BLOCK FB_Steel_BOF_Converter_DynamicLance_SublanceEndpoint_Offgas
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET ARCHITECTURE V7 MAX-PERSONA
  COMMERCIAL INDUSTRIAL SECTOR : Steel & Heavy Metallurgy / Primary Steelmaking Division
  SYSTEM CLASSIFICATION        : Commercial 300-Metric-Ton Basic Oxygen Furnace (BOF / LD Converter)
  PROCESS SCOPE                : Dynamic Supersonic Oxygen Top Lance Blowing (Mach 2.2 Multi-Hole Laval Nozzle, 900 Nm3/min),
                                 Dynamic In-Blow Sublance Immersion Carbon-Temperature Liquidus Arrest Endpoint Tracking,
                                 Continuous Real-Time Offgas Mass Spectrometer Analysis (CO, CO2, O2, N2, H2, Ar),
                                 Vessel Trunnion Piezoelectric Acoustic Accelerometer Slag Foaming & Slopping Prevention,
                                 Bottom-Stirring Inert Gas (Ar/N2) Porous Plug Energy Dissipation Coordination,
                                 and Suppressed-Combustion OG Electrostatic Precipitator (ESP) CO Gas Recovery Switchover.
  VESSEL SPECIFICATIONS        : 300 Metric Ton Nominal Liquid Steel Tapping Capacity, Magnesia-Carbon (MgO-C) Lining,
                                 450 m3 Bath Volume, 6 Bottom Porous Elements, Water-Cooled Movable Skirt Hood.
  AUTHOR                       : Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Experience)
========================================================================================================================

  METALLURGICAL THERMODYNAMICS & CYBER-PHYSICAL EQUATION FOUNDATIONS:
  ----------------------------------------------------------------------------------------------------------------------
  1. SUPERSONIC GAS DYNAMICS & LAVAL NOZZLE CAVITY PENETRATION:
     - Oxygen delivery occurs via a multi-hole copper Laval nozzle (typically 5 or 6 converging-diverging ports inclined
       at an angle theta_nozzle = 11.5 deg to 13.0 deg relative to lance centerline).
     - For an ideal diatomic gas (gamma = 1.40, molecular weight M_O2 = 32.0 kg/kmol), isentropic expansion produces Mach 2.2:
         M_exit = SQRT( (2 / (gamma - 1)) * [ (P_supply / P_ambient)^((gamma - 1) / gamma) - 1 ] )
       giving an exit gas velocity v_exit ~ 510 to 540 m/s.
     - Supersonic jet cavity penetration depth L_p [mm] into liquid iron (density rho_m = 6980 kg/m3) is given by Koria-Lange:
         L_p = 4.46e-3 * [ (P_O2 * d_throat^2 / (g * rho_m))^0.5 ] * (Q_O2 / Z_lance)^0.667 * EXP(-0.0014 * theta_nozzle)
       where P_O2 is header supply pressure [bar], d_throat is nozzle throat diameter [mm], Q_O2 is flow rate [Nm3/min],
       and Z_lance is lance tip distance above the quiescent liquid steel meniscus [mm].
     - Jet momentum force F_jet [N] creates the dynamic reaction cavity (fireclay/emulsion zone) where primary decarburization occurs:
         F_jet = rho_O2_exit * A_exit * v_exit^2 + (P_exit - P_vessel) * A_exit

  2. MULTIPHASE CHEMICAL REACTION KINETICS & THERMODYNAMICS:
     - Silicon Oxidation (Exothermic ignition & acid flux generation):
         [Si] + O2(g) -> (SiO2)                     Delta_H_298 = -910.9 kJ/mol
       Occurs preferentially in the first 3-5 minutes, releasing massive sensible heat to melt charged scrap.
     - Manganese Oxidation / Reduction:
         [Mn] + (FeO) <-> (MnO) + Fe(l)             Delta_G_0 = -124,500 + 58.2 * T [J/mol]
     - Carbon Decarburization Kinetics:
         High carbon regime (C_bath > C_crit ~ 0.25 wt% C): Decarburization rate is strictly gas-phase mass-transfer
         controlled by oxygen supply rate: dC/dt = -(24.0 / 22.414) * (Q_O2 / W_steel) * eta_O2_eff [%/min].
         Low carbon regime (C_bath < C_crit): Decarburization transitions to liquid-phase carbon diffusion boundary layer:
         dC/dt = -k_mass * A_interface * (C_bath - C_equilibrium) / V_bath
     - Slag Basicity & Dephosphorization Equilibrium:
         Binary Basicity: B_2 = (%CaO) / (%SiO2)               Target B_2 = 3.20 to 3.80
         Ternary Basicity: B_3 = (%CaO) / [(%SiO2) + (%Al2O3)] Target B_3 = 2.80 to 3.40
         Healy Dephosphorization Equilibrium Equation:
         log10((%P) / [%P]) = 22,350 / T_bath - 16.0 + 0.08 * (%CaO) + 2.5 * log10(%FeO_total)
       Phosphorus partition L_P is maximized at low bath temperatures (1540-1580 deg C), high basicity, and high slag FeO.

  3. DYNAMIC IN-BLOW SUBLANCE IMMERSION ENDPOINT PREDICTION:
     - At approximately 82% of planned total oxygen blow volume, a water-cooled secondary sublance descends into the vessel.
     - Disposable composite sensor (TSC: Temperature, Sample, Carbon liquidus arrest):
         Thermodynamic liquidus temperature T_liq [deg C] determines bath carbon via empirical Fe-C binary phase equilibrium:
           C_wt_pct = a_0 + a_1 * T_liq + a_2 * T_liq^2
         Direct thermocouple measurement records true bath bulk temperature T_bath [deg C].
     - In-situ dynamic model uses state-space feedback to re-project the exact remaining oxygen volume Delta_V_O2 [Nm3]
       and coolant/ore addition needed to hit target endpoint carbon (e.g. 0.045 wt%) and tap temperature (e.g. 1655 deg C).

  4. OFFGAS MASS SPECTROMETRY & TOTAL MASS BALANCE:
     - Real-time offgas analysis (CO, CO2, O2, N2, H2, Ar) with sampling delay compensation (tau_delay ~ 11.5 s):
     - Nitrogen tracer balance calculates instantaneous total dry offgas volumetric evacuation flow Q_offgas [Nm3/h]:
         Q_offgas = [ Q_bottom_N2 + Q_ingress_air * 0.7808 ] / (N2_vol_pct / 100.0)
     - Real-time bath decarburization rate dC/dt derived from offgas carbon mass emission:
         dC_dt_offgas = (12.011 / 22.414) * (Q_offgas / 100.0) * (CO_pct + CO2_pct) / (W_steel * 10.0) [%/min]
     - Post-Combustion Ratio (PCR) in converter mouth and waste heat boiler hood:
         PCR = CO2_pct / (CO_pct + CO2_pct) * 100.0 [%]
     - Dynamic slag oxygen accumulation (determining FeO buildup in slag):
         dO_slag/dt = O2_supply_flow - 0.5 * Q_offgas * (CO_pct + 2.0 * CO2_pct + 2.0 * O2_pct) - dO_Si/dt - dO_Mn/dt

  5. ACOUSTIC SLOPPING SURVEILLANCE & SUPPRESSION:
     - Two-phase gas-slag emulsion resonance is detected via piezoelectric trunnion accelerometers (0.1 to 10 kHz band).
     - Slag foaming height index H_foam [dB]: As liquid slag foams towards converter mouth, high-frequency acoustic attenuation
       muffles the supersonic jet impact noise. A sharp drop in acoustic transmission signal paired with boiler draft pressure
       instability indicates imminent slopping. Automatic closed-loop anti-slopping triggers lance height elevation,
       oxygen throttling, and lime/ore injection.

  6. BOTTOM-STIRRING INERT GAS THERMO-HYDRAULICS:
     - 6 bottom porous plugs inject Argon or Nitrogen to eliminate thermal and chemical stratification.
     - Specific stirring energy density epsilon_dot [W/t] (Sundberg / Nakanishi formulation):
         epsilon_dot = 28.5 * (Q_gas / W_steel) * T_bath * [ ln(1.0 + rho_m * g * H_bath / P_ambient) + (1.0 - T_gas0 / T_bath) ]
     - Nitrogen is blown in early stages; automatic bumpless switchover to Argon occurs at C < 0.40 wt% to avoid N-pickup.

  7. SUPPRESSED-COMBUSTION OG GAS RECOVERY CRITERIA:
     - Movable skirt lowers over vessel mouth to seal against atmospheric air ingress via nitrogen curtain.
     - Switchover to LD Gas Holder: Requires CO >= 35.0 vol% and O2 <= 1.0 vol% to ensure safe non-explosive calorific gas.
     - Immediate abort to flare stack if O2 exceeds 2.0 vol% or hood draft pressure deviates outside safe limits.
*)

VAR_INPUT
    (* ========================================================================= *)
    (* VESSEL KINEMATICS, CHARGING & CAMPAIGN DATA                               *)
    (* ========================================================================= *)
    rVesselTiltAngle_deg           : LREAL; (* Converter vessel tilt angle: 0.0=vertical, -55.0=scrap charge, +95.0=tap [deg] *)
    bVesselVerticalLock_Z          : BOOL;  (* Converter vessel mechanical vertical lock engaged at 0.0 deg [BOOL] *)
    rHotMetalChargeWeight_t        : LREAL; (* Charged liquid blast furnace hot metal mass [t] *)
    rScrapChargeWeight_t           : LREAL; (* Charged solid steel scrap mass [t] *)
    rHotMetalCarbon_pct            : LREAL; (* Hot metal incoming carbon content [wt% C] *)
    rHotMetalSilicon_pct           : LREAL; (* Hot metal incoming silicon content [wt% Si] *)
    rHotMetalPhosphorus_pct        : LREAL; (* Hot metal incoming phosphorus content [wt% P] *)
    rHotMetalManganese_pct         : LREAL; (* Hot metal incoming manganese content [wt% Mn] *)
    rHotMetalTemperature_degC      : LREAL; (* Hot metal ladle pre-pour temperature [deg C] *)
    rTargetTapCarbon_pct           : LREAL; (* Target tapping carbon endpoint specification [wt% C] *)
    rTargetTapTemperature_degC     : LREAL; (* Target tapping liquid steel temperature [deg C] *)
    rTargetTapPhosphorus_pct       : LREAL; (* Target tapping maximum phosphorus ceiling [wt% P] *)
    dCampaignHeatNumber            : DINT;  (* Cumulative heat count on current refractory lining [count] *)

    (* ========================================================================= *)
    (* 2oo3 REDUNDANT OXYGEN & LANCE WATER SENSORS                               *)
    (* ========================================================================= *)
    rO2_SupplyPressure_Ch1_bar     : LREAL; (* Main oxygen supply header pressure transmitter Channel 1 [bar] *)
    rO2_SupplyPressure_Ch2_bar     : LREAL; (* Main oxygen supply header pressure transmitter Channel 2 [bar] *)
    rO2_SupplyPressure_Ch3_bar     : LREAL; (* Main oxygen supply header pressure transmitter Channel 3 [bar] *)
    rO2_HeaderTemperature_degC     : LREAL; (* Main oxygen supply header gas temperature [deg C] *)
    rLanceWaterSupplyPress_bar     : LREAL; (* Lance high-pressure cooling water supply header pressure [bar] *)
    rLanceWaterSupplyFlow_m3h      : LREAL; (* Lance cooling water volumetric supply flow rate [m3/h] *)
    rLanceWaterDeltaT_Ch1_degC     : LREAL; (* Lance cooling water inlet-outlet differential RTD Channel 1 [deg C] *)
    rLanceWaterDeltaT_Ch2_degC     : LREAL; (* Lance cooling water inlet-outlet differential RTD Channel 2 [deg C] *)
    rLanceWaterDeltaT_Ch3_degC     : LREAL; (* Lance cooling water inlet-outlet differential RTD Channel 3 [deg C] *)
    rLanceWaterReturnPress_bar     : LREAL; (* Lance cooling water return discharge header pressure [bar] *)
    rLanceWaterLeakAcoustic_raw    : LREAL; (* Lance internal ultrasonic acoustic water leak sensor [mV] *)

    (* ========================================================================= *)
    (* LANCE POSITIONING, WINCH & SKIRT ENCODERS                                 *)
    (* ========================================================================= *)
    rLanceHeightActual_Z_mm        : LREAL; (* Lance nozzle tip elevation relative to static bath meniscus [mm] *)
    rLanceWinchActualSpeed_mms     : LREAL; (* Lance hoist winch actual vertical velocity [mm/s] *)
    bLanceUpperParkLimit_LS        : BOOL;  (* Lance mechanical hoist upper park limit switch [BOOL] *)
    bLanceLowerSafetyInterlock_LS  : BOOL;  (* Lance mechanical lower safety hard overtravel limit switch [BOOL] *)
    rSkirtPositionActual_mm        : LREAL; (* Waste heat boiler movable skirt elevation [mm] *)
    bSkirtFullyLowered_LS          : BOOL;  (* Waste heat boiler skirt fully seated seal limit switch [BOOL] *)

    (* ========================================================================= *)
    (* 2oo3 REDUNDANT VESSEL TRUNNION ACOUSTIC SENSORS (SLOPPING)                *)
    (* ========================================================================= *)
    rTrunnionAcoustic_Ch1_dB       : LREAL; (* Trunnion piezo accelerometer acoustic slopping Channel 1 [dB] *)
    rTrunnionAcoustic_Ch2_dB       : LREAL; (* Trunnion piezo accelerometer acoustic slopping Channel 2 [dB] *)
    rTrunnionAcoustic_Ch3_dB       : LREAL; (* Trunnion piezo accelerometer acoustic slopping Channel 3 [dB] *)
    rHoodDraftPressure_Pa          : LREAL; (* Waste heat boiler primary hood draft differential pressure [Pa] *)

    (* ========================================================================= *)
    (* 2oo3 REDUNDANT OFFGAS MASS SPECTROMETER READINGS                          *)
    (* ========================================================================= *)
    rOffgas_CO_Ch1_pct             : LREAL; (* Offgas mass spec CO concentration Channel 1 [% vol CO] *)
    rOffgas_CO_Ch2_pct             : LREAL; (* Offgas mass spec CO concentration Channel 2 [% vol CO] *)
    rOffgas_CO_Ch3_pct             : LREAL; (* Offgas mass spec CO concentration Channel 3 [% vol CO] *)
    rOffgas_CO2_Conc_pct           : LREAL; (* Offgas mass spec carbon dioxide concentration [% vol CO2] *)
    rOffgas_O2_Conc_pct            : LREAL; (* Offgas mass spec oxygen concentration [% vol O2] *)
    rOffgas_N2_Conc_pct            : LREAL; (* Offgas mass spec nitrogen concentration [% vol N2] *)
    rOffgas_H2_Conc_pct            : LREAL; (* Offgas mass spec hydrogen concentration [% vol H2] *)
    rOffgas_Ar_Conc_pct            : LREAL; (* Offgas mass spec argon concentration [% vol Ar] *)
    rOffgasTotalFlowRaw_Nm3h       : LREAL; (* Offgas pitot tube / differential primary flow transmitter [Nm3/h] *)

    (* ========================================================================= *)
    (* DYNAMIC SUBLANCE IN-BLOW MEASUREMENT SIGNALS                              *)
    (* ========================================================================= *)
    bSublanceProbeReady            : BOOL;  (* Sublance probe magazine ready & new probe loaded [BOOL] *)
    bSublanceBathContact_Sig       : BOOL;  (* Sublance probe electrical contact detected with molten bath [BOOL] *)
    rSublanceLiquidusTemp_degC     : LREAL; (* Sublance probe recorded solidification liquidus arrest temperature [deg C] *)
    rSublanceBathTemp_degC         : LREAL; (* Sublance probe direct liquid steel immersion temperature [deg C] *)
    rSublanceOxygenActivity_ppm    : LREAL; (* Sublance ZrO2 cell dissolved oxygen activity in steel bath [ppm] *)
    rSublanceActualDepth_mm        : LREAL; (* Sublance immersion elevation below bath meniscus [mm] *)

    (* ========================================================================= *)
    (* BOTTOM STIRRING & FLUX ADDITION SYSTEM SIGNALS                            *)
    (* ========================================================================= *)
    rBottomGasHeaderPress_bar      : LREAL; (* Bottom-stirring inert gas supply header pressure [bar] *)
    rBottomArgonFlowActual_Nm3min  : LREAL; (* Bottom porous plug actual Argon flow rate [Nm3/min] *)
    rBottomNitrogenFlowActual_Nm3min: LREAL; (* Bottom porous plug actual Nitrogen flow rate [Nm3/min] *)
    rLimeHopperWeight_kg           : LREAL; (* Overhead active calcined lime weigh hopper actual weight [kg] *)
    rDoloHopperWeight_kg           : LREAL; (* Overhead light-burned dolomitic lime weigh hopper actual weight [kg] *)
    rIronOreHopperWeight_kg        : LREAL; (* Overhead cooling iron ore / pellets weigh hopper actual weight [kg] *)

    (* ========================================================================= *)
    (* MASTER OPERATOR & SAFETY SUPERVISORY COMMANDS                             *)
    (* ========================================================================= *)
    bAutoSequenceStartCmd          : BOOL;  (* Master automatic heat sequence start push-button [BOOL] *)
    bSequenceHoldCmd               : BOOL;  (* Operator process hold / pause command [BOOL] *)
    bSequenceAbortCmd              : BOOL;  (* Operator controlled sequence abort / blow stop command [BOOL] *)
    bEmergencyTripCmd              : BOOL;  (* Hardwired Emergency Safety Stop (E-Stop) push-button [BOOL] *)
    bAlarmAcknowledgeCmd           : BOOL;  (* Master alarm acknowledge & silence command [BOOL] *)
    rCycleTime_dt_s                : LREAL; (* PLC deterministic scan cycle time [s] (e.g. 0.050 s) *)
END_VAR

VAR_OUTPUT
    (* ========================================================================= *)
    (* PRIMARY ACTUATOR COMMANDS (SUPERSONIC LANCE & BLOWING)                    *)
    (* ========================================================================= *)
    rO2_MainFlowControlValve_pct   : LREAL; (* Supersonic oxygen main flow control valve position command [%] *)
    rO2_FlowSetpoint_Nm3min        : LREAL; (* Supersonic oxygen mass flow setpoint command [Nm3/min] *)
    rLanceWinchSpeedCmd_mms        : LREAL; (* Lance hoist winch VFD vertical speed command [mm/s] *)
    iLanceWinchDirectionCmd        : INT;   (* Lance winch directional command: 0=Stop/Hold, +1=Lower, -1=Raise [INT] *)
    rLanceTargetElevation_mm       : LREAL; (* Lance dynamic target elevation above bath meniscus [mm] *)
    bO2_MainEmergencyShutoffValve  : BOOL;  (* Supersonic oxygen safety shutoff ball valve actuator command [BOOL] *)
    bLanceNitrogenPurgeValve       : BOOL;  (* Lance internal nitrogen purge valve actuator command [BOOL] *)

    (* ========================================================================= *)
    (* FLUX & ALLOY FEEDING ACTUATORS                                            *)
    (* ========================================================================= *)
    rLimeVibratoryFeederCmd_pct    : LREAL; (* Active lime vibratory feeder drive command [%] *)
    rDoloVibratoryFeederCmd_pct    : LREAL; (* Dolomite vibratory feeder drive command [%] *)
    rIronOreVibratoryFeederCmd_pct : LREAL; (* Iron ore cooling pellet vibratory feeder drive command [%] *)
    bFluxBatchDischargeGateOpen    : BOOL;  (* Overhead flux batching weigh hopper discharge gate command [BOOL] *)

    (* ========================================================================= *)
    (* BOTTOM STIRRING & HOOD GAS ACTUATORS                                      *)
    (* ========================================================================= *)
    iBottomGasTypeSelected         : INT;   (* Bottom gas active selection: 0=None, 1=Nitrogen, 2=Argon [INT] *)
    rBottomGasFlowCmd_Nm3min       : LREAL; (* Bottom-stirring inert gas total flow rate command [Nm3/min] *)
    rSkirtElevationCmd_mm          : LREAL; (* Movable skirt positioning cylinder command [mm] *)
    rPrimaryOffgasDamperCmd_pct    : LREAL; (* Primary waste heat boiler ID fan draft damper command [%] *)
    bGasRecoveryThreeWayValveCmd   : BOOL;  (* OG gas recovery switchover: FALSE=Flare Stack, TRUE=LD Gas Holder [BOOL] *)
    bNitrogenSealingCurtainCmd     : BOOL;  (* Skirt nitrogen sealing curtain purge valve command [BOOL] *)

    (* ========================================================================= *)
    (* SUBLANCE ACTUATION COMMANDS                                               *)
    (* ========================================================================= *)
    rSublanceWinchSpeedCmd_mms     : LREAL; (* Dynamic sublance hoist winch speed command [mm/s] *)
    iSublanceWinchDirectionCmd     : INT;   (* Sublance hoist direction: 0=Parked, +1=Immersion, -1=Retract [INT] *)
    bSublanceCycleInProgress       : BOOL;  (* Dynamic sublance immersion sampling cycle active [BOOL] *)
    bSublanceSampleValid           : BOOL;  (* Sublance probe data acquisition successful and verified [BOOL] *)

    (* ========================================================================= *)
    (* ESTIMATED CYBER-PHYSICAL STATE & METALLURGICAL TRACKING                   *)
    (* ========================================================================= *)
    rEstimatedBathCarbon_pct       : LREAL; (* Dynamic state-space estimated molten steel bath carbon [wt% C] *)
    rEstimatedBathTemp_degC        : LREAL; (* Dynamic state-space estimated molten steel bath temperature [deg C] *)
    rEstimatedSlagFeO_pct          : LREAL; (* Dynamic slag mass-balance estimated total FeO content [%] *)
    rCalculatedDecarbRate_pctmin   : LREAL; (* Real-time offgas mass-spectrometry decarburization rate dC/dt [%/min] *)
    rPostCombustionRatio_pct       : LREAL; (* Calculated waste heat hood post-combustion ratio PCR [%] *)
    rAcousticFoamIndex_dB          : LREAL; (* 2oo3 Voted trunnion acoustic accelerometer slag foaming index [dB] *)
    bAntiSloppingActive            : BOOL;  (* Closed-loop anti-slopping automatic suppression intervention active [BOOL] *)
    rStirringEnergyDensity_Wt      : LREAL; (* Calculated bottom gas specific stirring energy dissipation rate [W/t] *)
    rTotalOxygenBlown_Nm3          : LREAL; (* Cumulative oxygen volume consumed during current heat [Nm3] *)
    rTotalBlowDuration_s           : LREAL; (* Elapsed active oxygen blowing duration [s] *)

    (* ========================================================================= *)
    (* SYSTEM FSM STATE, DIAGNOSTICS & ALARM WORDS                               *)
    (* ========================================================================= *)
    iCurrentFsmState               : INT;   (* Current deterministic 14-stage FSM state index [0..13] [INT] *)
    rStateElapsedTime_s            : LREAL; (* Current FSM state elapsed active execution timer [s] *)
    dStatusWord1                   : DWORD; (* Primary bit-packed converter operational status word [DWORD] *)
    dStatusWord2                   : DWORD; (* Subsystem interlock & permissives bit-packed status word [DWORD] *)
    dAlarmWord1                    : DWORD; (* High-severity trip & interlock bit-packed alarm word [DWORD] *)
    dAlarmWord2                    : DWORD; (* Process deviation & warning bit-packed alarm word [DWORD] *)
    bEmergencyShutdownActive       : BOOL;  (* Master safety interlock fail-safe emergency shutdown active [BOOL] *)
    bHeatCompleteReadyToTap        : BOOL;  (* Heat blowing sequence successfully completed, ready for tap [BOOL] *)
END_VAR

VAR
    (* ========================================================================= *)
    (* FIRST SCAN & CONFIGURATION FLAGS                                          *)
    (* ========================================================================= *)
    bFirstScanDone                 : BOOL := FALSE; (* First scan cycle initialization completed flag *)
    bConfigInitialized             : BOOL := FALSE; (* Matrix and calibration parameters loaded flag *)

    (* ========================================================================= *)
    (* 2oo3 TMR VOTING DATA STRUCTURES & TIMERS                                  *)
    (* ========================================================================= *)
    (* Sensor Group 1: Main O2 Supply Pressure [bar] *)
    rO2_Press_Voted                : LREAL := 14.5; (* 2oo3 Voted O2 supply pressure [bar] *)
    bO2_Press_Ch1_Fail             : BOOL := FALSE; (* O2 Press Channel 1 failure detected *)
    bO2_Press_Ch2_Fail             : BOOL := FALSE; (* O2 Press Channel 2 failure detected *)
    bO2_Press_Ch3_Fail             : BOOL := FALSE; (* O2 Press Channel 3 failure detected *)
    rO2_Press_Ch1_DiscTimer_s      : LREAL := 0.0;  (* Discrepancy persistence timer Ch 1 [s] *)
    rO2_Press_Ch2_DiscTimer_s      : LREAL := 0.0;  (* Discrepancy persistence timer Ch 2 [s] *)
    rO2_Press_Ch3_DiscTimer_s      : LREAL := 0.0;  (* Discrepancy persistence timer Ch 3 [s] *)
    iO2_Press_HealthySensors       : INT := 3;      (* Count of operational O2 pressure channels [0..3] *)

    (* Sensor Group 2: Lance Cooling Water Delta T [deg C] *)
    rLanceDeltaT_Voted             : LREAL := 18.0; (* 2oo3 Voted lance cooling water delta-T [deg C] *)
    bLanceDeltaT_Ch1_Fail          : BOOL := FALSE; (* Lance Delta T Channel 1 failure detected *)
    bLanceDeltaT_Ch2_Fail          : BOOL := FALSE; (* Lance Delta T Channel 2 failure detected *)
    bLanceDeltaT_Ch3_Fail          : BOOL := FALSE; (* Lance Delta T Channel 3 failure detected *)
    rLanceDeltaT_Ch1_DiscTimer_s   : LREAL := 0.0;  (* Discrepancy persistence timer Ch 1 [s] *)
    rLanceDeltaT_Ch2_DiscTimer_s   : LREAL := 0.0;  (* Discrepancy persistence timer Ch 2 [s] *)
    rLanceDeltaT_Ch3_DiscTimer_s   : LREAL := 0.0;  (* Discrepancy persistence timer Ch 3 [s] *)
    iLanceDeltaT_HealthySensors    : INT := 3;      (* Count of operational Delta T channels [0..3] *)

    (* Sensor Group 3: Trunnion Acoustic Accelerometers [dB] *)
    rTrunnionAcoustic_Voted        : LREAL := 82.0; (* 2oo3 Voted trunnion acoustic accelerometer [dB] *)
    bTrunnionAcoustic_Ch1_Fail     : BOOL := FALSE; (* Trunnion Acoustic Channel 1 failure detected *)
    bTrunnionAcoustic_Ch2_Fail     : BOOL := FALSE; (* Trunnion Acoustic Channel 2 failure detected *)
    bTrunnionAcoustic_Ch3_Fail     : BOOL := FALSE; (* Trunnion Acoustic Channel 3 failure detected *)
    rTrunnionAcoustic_Ch1_DiscTimer_s: LREAL := 0.0; (* Discrepancy persistence timer Ch 1 [s] *)
    rTrunnionAcoustic_Ch2_DiscTimer_s: LREAL := 0.0; (* Discrepancy persistence timer Ch 2 [s] *)
    rTrunnionAcoustic_Ch3_DiscTimer_s: LREAL := 0.0; (* Discrepancy persistence timer Ch 3 [s] *)
    iTrunnionAcoustic_HealthySensors: INT := 3;     (* Count of operational Acoustic channels [0..3] *)

    (* Sensor Group 4: Offgas Mass Spec CO Concentration [% vol CO] *)
    rOffgas_CO_Voted               : LREAL := 0.0;  (* 2oo3 Voted offgas CO concentration [% vol CO] *)
    bOffgas_CO_Ch1_Fail            : BOOL := FALSE; (* Offgas CO Channel 1 failure detected *)
    bOffgas_CO_Ch2_Fail            : BOOL := FALSE; (* Offgas CO Channel 2 failure detected *)
    bOffgas_CO_Ch3_Fail            : BOOL := FALSE; (* Offgas CO Channel 3 failure detected *)
    rOffgas_CO_Ch1_DiscTimer_s     : LREAL := 0.0;  (* Discrepancy persistence timer Ch 1 [s] *)
    rOffgas_CO_Ch2_DiscTimer_s     : LREAL := 0.0;  (* Discrepancy persistence timer Ch 2 [s] *)
    rOffgas_CO_Ch3_DiscTimer_s     : LREAL := 0.0;  (* Discrepancy persistence timer Ch 3 [s] *)
    iOffgas_CO_HealthySensors      : INT := 3;      (* Count of operational Offgas CO channels [0..3] *)

    (* ========================================================================= *)
    (* 6-STATE CYBER-PHYSICAL DISCRETE STATE-SPACE MATRICES                      *)
    (* State Vector x[6]:                                                        *)
    (*   x[0] = C_bath [wt% C]       (Bath carbon concentration)                 *)
    (*   x[1] = T_bath [deg C]       (Bath bulk steel temperature)               *)
    (*   x[2] = dC_dt  [%/min]       (Instantaneous decarburization rate)        *)
    (*   x[3] = FeO    [%]           (Slag total FeO concentration)              *)
    (*   x[4] = H_foam [dB]          (Slag acoustic foaming attenuation index)   *)
    (*   x[5] = DP_hood [Pa]         (Boiler hood differential draft pressure)   *)
    (* Control Vector u[5]:                                                      *)
    (*   u[0] = Lance winch speed command trim v_lance [mm/s]                    *)
    (*   u[1] = Main O2 flow rate command trim Q_O2 [Nm3/min]                    *)
    (*   u[2] = Flux feeder gate command trim [lime/dolo %]                      *)
    (*   u[3] = Bottom inert gas stirring flow command trim Q_bottom [Nm3/min]   *)
    (*   u[4] = Primary offgas damper command trim [% open]                      *)
    (* ========================================================================= *)
    x_est                          : ARRAY[0..5] OF LREAL := [4.30, 1360.0, 0.0, 10.0, 85.0, -120.0];
    x_pred                         : ARRAY[0..5] OF LREAL := [4.30, 1360.0, 0.0, 10.0, 85.0, -120.0];
    x_ref                          : ARRAY[0..5] OF LREAL := [0.045, 1655.0, 0.05, 18.0, 78.0, -150.0];
    u_curr                         : ARRAY[0..4] OF LREAL := [0.0, 900.0, 0.0, 18.0, 45.0];
    u_prev                         : ARRAY[0..4] OF LREAL := [0.0, 900.0, 0.0, 18.0, 45.0];
    u_opt                          : ARRAY[0..4] OF LREAL := [0.0, 900.0, 0.0, 18.0, 45.0];
    y_meas                         : ARRAY[0..5] OF LREAL := [4.30, 1360.0, 0.0, 10.0, 85.0, -120.0];
    y_est                          : ARRAY[0..5] OF LREAL := [4.30, 1360.0, 0.0, 10.0, 85.0, -120.0];
    innov                          : ARRAY[0..5] OF LREAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

    (* State-Space System Matrices: Discrete Time Ts = 0.050 s *)
    A_mat                          : ARRAY[0..5, 0..5] OF LREAL;
    B_mat                          : ARRAY[0..5, 0..4] OF LREAL;
    C_mat                          : ARRAY[0..5, 0..5] OF LREAL;
    D_mat                          : ARRAY[0..5, 0..4] OF LREAL;
    L_obs                          : ARRAY[0..5, 0..5] OF LREAL; (* Observer Kalman / Luenberger gain *)

    (* ========================================================================= *)
    (* RECEDING-HORIZON MPC PENALTY MATRICES & TRAJECTORIES                      *)
    (* ========================================================================= *)
    Q_diag                         : ARRAY[0..5] OF LREAL := [12000.0, 85.0, 450.0, 320.0, 180.0, 45.0];
    R_diag                         : ARRAY[0..4] OF LREAL := [1.5, 0.8, 2.2, 3.5, 0.5];
    P_diag                         : ARRAY[0..5] OF LREAL := [24000.0, 180.0, 900.0, 650.0, 350.0, 90.0];
    R_delta_diag                   : ARRAY[0..4] OF LREAL := [4.0, 2.5, 5.0, 8.0, 1.2];

    (* MPC Horizon Arrays: Horizon N = 5 steps, 10 PGD iterations *)
    u_traj                         : ARRAY[0..4, 0..4] OF LREAL; (* u_traj[step 0..4, input 0..4] *)
    x_traj                         : ARRAY[0..5, 0..5] OF LREAL; (* x_traj[step 0..5, state 0..5] *)
    grad_u                         : ARRAY[0..4, 0..4] OF LREAL; (* Analytical cost gradient *)
    u_min                          : ARRAY[0..4] OF LREAL := [-45.0, 200.0, 0.0, 5.0, 10.0];
    u_max                          : ARRAY[0..4] OF LREAL := [45.0, 1050.0, 100.0, 35.0, 95.0];
    delta_u_max                    : ARRAY[0..4] OF LREAL := [8.0, 25.0, 15.0, 3.0, 5.0];
    rMpcStepSize_alpha             : LREAL := 0.0125;

    (* ========================================================================= *)
    (* METALLURGICAL & FIRST-PRINCIPLES PHYSICAL CALCULATION VARIABLES           *)
    (* ========================================================================= *)
    rTotalSteelMass_t              : LREAL := 300.0; (* Current total molten bath mass [t] *)
    rLavalMachNumber               : LREAL := 2.20;  (* Supersonic Laval nozzle Mach number *)
    rLavalExitVelocity_ms          : LREAL := 525.0; (* Laval nozzle oxygen exit velocity [m/s] *)
    rCavityPenetrationDepth_mm     : LREAL := 450.0; (* Dynamic supersonic jet cavity depth L_p [mm] *)
    rCavityDiameter_mm             : LREAL := 950.0; (* Dynamic supersonic jet cavity diameter [mm] *)
    rSlagBasicity_B2               : LREAL := 3.40;  (* Slag binary basicity CaO / SiO2 *)
    rSlagBasicity_B3               : LREAL := 3.10;  (* Slag ternary basicity CaO / (SiO2 + Al2O3) *)
    rDephosphorizationPartition_Lp : LREAL := 85.0;  (* Equilibrium phosphorus partition ratio (P) / [P] *)
    rInstantaneousDecarbRate_pctmin: LREAL := 0.0;   (* Offgas derived decarburization rate [%/min] *)
    rDynamicOxygenAccumulation_kg  : LREAL := 0.0;   (* Dynamic oxygen accumulated in slag [kg O2] *)
    rDynamicSlagMass_t             : LREAL := 28.0;  (* Dynamic total slag mass in furnace [t] *)
    rDynamicSlagFeO_pct            : LREAL := 16.5;  (* Dynamic slag FeO mass concentration [%] *)
    rDynamicSlagSiO2_pct           : LREAL := 14.2;  (* Dynamic slag SiO2 mass concentration [%] *)
    rDynamicSlagCaO_pct            : LREAL := 48.5;  (* Dynamic slag CaO mass concentration [%] *)
    rDynamicSlagMgO_pct            : LREAL := 8.5;   (* Dynamic slag MgO mass concentration [%] *)
    rDynamicBathCarbon_pct         : LREAL := 4.30;  (* Physical bath carbon content [wt% C] *)
    rDynamicBathTemp_degC          : LREAL := 1360.0;(* Physical bath temperature [deg C] *)
    rDynamicBathSilicon_pct        : LREAL := 0.45;  (* Physical bath silicon content [wt% Si] *)
    rDynamicBathManganese_pct      : LREAL := 0.35;  (* Physical bath manganese content [wt% Mn] *)
    rDynamicBathPhosphorus_pct     : LREAL := 0.065; (* Physical bath phosphorus content [wt% P] *)

    (* Gas Dynamic & Offgas Balance Variables *)
    rOffgasTotalFlowCalc_Nm3h      : LREAL := 185000.0; (* Calculated dry offgas evacuation rate [Nm3/h] *)
    rAirIngressFlow_Nm3h           : LREAL := 4200.0;   (* Air ingress around movable skirt [Nm3/h] *)
    rPostCombustionRatio_calc      : LREAL := 12.5;     (* Post combustion ratio PCR [%] *)
    rGasCalorificValue_MJNm3       : LREAL := 8.5;      (* Offgas lower heating value LHV [MJ/Nm3] *)
    bGasRecoveryPermissive         : BOOL := FALSE;     (* OG gas recovery switchover permissive flag *)
    rGasRecoveryEligibleTimer_s    : LREAL := 0.0;      (* Gas recovery continuous qualification timer [s] *)

    (* Sublance Process Variables *)
    rSublanceLiquidusCalculatedC_pct: LREAL := 0.0;   (* Bath carbon derived from liquidus arrest curve [% C] *)
    rSublanceImmersionTimer_s      : LREAL := 0.0;    (* Sublance in-bath residence timer [s] *)
    bSublanceTriggerDone           : BOOL := FALSE;   (* Sublance single immersion triggered flag *)
    bSublanceAcquisitionSuccessful : BOOL := FALSE;   (* Sublance data successfully latched flag *)
    rSublanceLatchedCarbon_pct     : LREAL := 0.0;    (* Latched sublance carbon measurement [% C] *)
    rSublanceLatchedTemp_degC      : LREAL := 0.0;    (* Latched sublance temperature measurement [deg C] *)
    rSublanceLatchedOxygen_ppm     : LREAL := 0.0;    (* Latched sublance dissolved oxygen [ppm] *)
    rRemainingBlowO2Volume_Nm3     : LREAL := 0.0;    (* Sublance recalculated remaining oxygen blow volume [Nm3] *)
    rTotalPlannedO2Volume_Nm3      : LREAL := 16500.0;(* Total planned oxygen blow volume for current heat [Nm3] *)

    (* Slag Slopping & Acoustic Resonance Variables *)
    rAcousticBaselineQuiet_dB      : LREAL := 92.0;   (* Baseline acoustic noise for shallow quiet slag [dB] *)
    rAcousticAttenuation_dB       : LREAL := 0.0;    (* Acoustic attenuation relative to quiet baseline [dB] *)
    rSloppingSeverityIndex         : LREAL := 0.0;    (* Slopping severity score [0.0..10.0] *)
    rAntiSloppingCooldownTimer_s   : LREAL := 0.0;    (* Anti-slopping intervention persistence timer [s] *)
    rSlagSplashingTimer_s          : LREAL := 0.0;    (* Slag splashing N2 blowing cycle timer [s] *)
    rSlagSplashingTargetTime_s     : LREAL := 180.0;  (* Slag splashing target duration (3 min) [s] *)

    (* Water Leak Protection Variables *)
    rWaterMassFlowDelta_kgh        : LREAL := 0.0;    (* Difference between supply and return water mass flow [kg/h] *)
    bCriticalWaterLeakDetected     : BOOL := FALSE;   (* Catastrophic lance water leak alarm trip *)
    rWaterLeakConfirmTimer_s       : LREAL := 0.0;    (* Water leak confirmation persistence timer [s] *)

    (* ========================================================================= *)
    (* 14-STAGE FINITE STATE MACHINE (FSM) INTERNAL REGISTERS                    *)
    (* ========================================================================= *)
    iFsmState                      : INT := 0;        (* Current active state index [0..13] *)
    iFsmPrevState                  : INT := 0;        (* Previous scan state index [0..13] *)
    rFsmStateTimer_s               : LREAL := 0.0;    (* Time elapsed in current FSM state [s] *)
    bFsmStateFirstScan             : BOOL := TRUE;    (* First scan of newly entered state flag *)
    rHeatTotalOxygenConsumed_Nm3   : LREAL := 0.0;    (* Integrated cumulative oxygen consumption [Nm3] *)
    rHeatTotalBlowTime_s           : LREAL := 0.0;    (* Integrated cumulative blowing duration [s] *)
    rTappingTimer_s                : LREAL := 0.0;    (* Liquid steel tapping duration timer [s] *)
    bTappingSlagDartDropped        : BOOL := FALSE;   (* Slag stopper dart deployed into taphole *)

    (* FSM State Constant Enumerations *)
    cSTATE_IDLE                    : INT := 0;        (* Vessel vertical, lance parked, awaiting charge *)
    cSTATE_SCRAP_HOTMETAL_CHARGE   : INT := 1;        (* Vessel tilted, scrap & hot metal charging *)
    cSTATE_VERTICAL_LOCK_HOOD_DOWN : INT := 2;        (* Vertical lock engaged, skirt lowered, seal purge *)
    cSTATE_LANCE_IGNITION_SOFT_BLOW: INT := 3;        (* High lance ignition blow, flame establishment *)
    cSTATE_SILICON_OXIDATION_FLUX  : INT := 4;        (* Si oxidation peak, lime/dolomite batch feeding *)
    cSTATE_MAIN_DECARB_DEEP_BLOW   : INT := 5;        (* Supersonic deep blowing, peak decarb rate dC/dt *)
    cSTATE_SLAG_FOAM_SLOP_SUPPRESS : INT := 6;        (* Active slopping suppression & acoustic control *)
    cSTATE_SUBLANCE_IMMERSION_DIP  : INT := 7;        (* Dynamic sublance immersion at ~82% blow *)
    cSTATE_ENDPOINT_FINE_TRIM_BLOW : INT := 8;        (* Fine O2 trim blow to hit target C and temp *)
    cSTATE_BOTTOM_STIR_RINSE       : INT := 9;        (* Pure Argon rinse stirring, O2 shutoff *)
    cSTATE_LANCE_RETRACT_VERIFY    : INT := 10;       (* Lance hoist to upper park, final TSC probe verify *)
    cSTATE_VESSEL_TILT_TAPPING     : INT := 11;       (* Converter tilt to +95 deg, tapping & ladle alloying *)
    cSTATE_SLAG_SPLASHING_COAT     : INT := 12;       (* High-pressure N2 slag splashing refractory coat *)
    cSTATE_EMERGENCY_LEAK_TRIP     : INT := 13;       (* Catastrophic lance leak or hood trip safe park *)

    (* ========================================================================= *)
    (* ISA-18.2 MULTI-TIERED ALARM ENGINE & STATUS WORD REGISTERS                *)
    (* ========================================================================= *)
    (* Alarm Trip Setpoints & Hysteresis *)
    rO2_Press_HH_bar               : LREAL := 19.5;   (* Main O2 pressure High-High trip [bar] *)
    rO2_Press_H_bar                : LREAL := 18.0;   (* Main O2 pressure High warning [bar] *)
    rO2_Press_L_bar                : LREAL := 11.5;   (* Main O2 pressure Low warning [bar] *)
    rO2_Press_LL_bar               : LREAL := 9.5;    (* Main O2 pressure Low-Low trip [bar] *)
    rO2_Press_Hyst_bar             : LREAL := 0.40;   (* Main O2 pressure deadband hysteresis [bar] *)

    rLanceDeltaT_HH_degC           : LREAL := 32.0;   (* Lance cooling water Delta-T High-High trip [deg C] *)
    rLanceDeltaT_H_degC            : LREAL := 26.0;   (* Lance cooling water Delta-T High warning [deg C] *)
    rLanceDeltaT_Hyst_degC         : LREAL := 1.0;    (* Lance Delta-T deadband hysteresis [deg C] *)

    rHoodDraft_HH_Pa               : LREAL := 50.0;   (* Hood draft pressure positive pressure trip [Pa] *)
    rHoodDraft_H_Pa                : LREAL := 0.0;    (* Hood draft pressure positive pressure warning [Pa] *)
    rHoodDraft_LL_Pa               : LREAL := -450.0; (* Hood draft excessive suction trip [Pa] *)
    rHoodDraft_Hyst_Pa             : LREAL := 15.0;   (* Hood draft deadband hysteresis [Pa] *)

    rOffgas_O2_HH_pct              : LREAL := 2.00;   (* Offgas O2 concentration High-High trip (explosion) [%] *)
    rOffgas_O2_H_pct               : LREAL := 1.20;   (* Offgas O2 concentration High warning [%] *)
    rOffgas_O2_Hyst_pct            : LREAL := 0.15;   (* Offgas O2 deadband hysteresis [%] *)

    rBathTemp_HH_degC              : LREAL := 1720.0; (* Molten steel bath temperature High-High trip [deg C] *)
    rBathTemp_H_degC               : LREAL := 1680.0; (* Molten steel bath temperature High warning [deg C] *)

    (* Internal Latched Alarm Flags *)
    bAlarm_O2_Press_HH             : BOOL := FALSE;   (* O2 Pressure High-High alarm bit *)
    bAlarm_O2_Press_LL             : BOOL := FALSE;   (* O2 Pressure Low-Low alarm bit *)
    bAlarm_LanceWaterDeltaT_HH     : BOOL := FALSE;   (* Lance water Delta-T High-High alarm bit *)
    bAlarm_LanceWaterLeakTrip      : BOOL := FALSE;   (* Lance acoustic/differential water leak trip bit *)
    bAlarm_HoodDraft_HH            : BOOL := FALSE;   (* Hood positive draft explosion risk alarm bit *)
    bAlarm_Offgas_O2_HH            : BOOL := FALSE;   (* Offgas O2 High-High gas recovery trip bit *)
    bAlarm_BathTemp_HH             : BOOL := FALSE;   (* Bath temperature High-High lining protection bit *)
    bAlarm_SloppingSevere          : BOOL := FALSE;   (* Trunnion acoustic severe slopping warning bit *)
    bAlarm_TmrDegraded             : BOOL := FALSE;   (* TMR sensor voting operating in degraded mode bit *)
    bAlarm_SublanceImmersionFault  : BOOL := FALSE;   (* Sublance drive or communication fault bit *)

    (* Bit-Packed Word Temporary Buffers *)
    dwStat1                        : DWORD := 16#00000000;
    dwStat2                        : DWORD := 16#00000000;
    dwAlm1                         : DWORD := 16#00000000;
    dwAlm2                         : DWORD := 16#00000000;

    (* General Loop Counters & Math Registers *)
    iIdx                           : INT := 0;
    jIdx                           : INT := 0;
    kIdx                           : INT := 0;
    mIdx                           : INT := 0;
    pIdx                           : INT := 0;
    rTmpSum                        : LREAL := 0.0;
    rTmpVal                        : LREAL := 0.0;
    rGradVal                       : LREAL := 0.0;
    rCostDiff                      : LREAL := 0.0;
END_VAR

(* ========================================================================= *)
(* PHASE 0: FIRST-SCAN DETERMINISTIC MATRIX INITIALIZATION & CONFIGURATION    *)
(* ========================================================================= *)
IF NOT bFirstScanDone THEN
    (* --------------------------------------------------------------------- *)
    (* DISCRETE STATE-SPACE DYNAMICS MATRICES (Ts = 0.050 s)                 *)
    (* x[0] = C_bath [%], x[1] = T_bath [degC], x[2] = dC/dt [%/min],        *)
    (* x[3] = FeO_slag [%], x[4] = H_foam [dB], x[5] = DP_hood [Pa]          *)
    (* u[0] = v_lance [mm/s], u[1] = Q_O2 [Nm3/min], u[2] = Flux [%],        *)
    (* u[3] = Q_bottom [Nm3/min], u[4] = Damper [%]                         *)
    (* --------------------------------------------------------------------- *)

    (* Row 0: Bath Carbon Content Dynamics C_bath [wt% C] *)
    A_mat[0, 0] := 0.99985; (* Natural carbon persistence in liquid iron *)
    A_mat[0, 1] := 0.00000; (* Negligible direct thermal volatility of carbon *)
    A_mat[0, 2] := -0.00083333; (* Integration of decarb rate: -dt/60 = -0.050/60.0 *)
    A_mat[0, 3] := -0.000025; (* Decarburization via slag FeO reduction: [C] + (FeO) -> Fe + CO *)
    A_mat[0, 4] := 0.00000; (* Foam height has no direct stoichiometric carbon effect *)
    A_mat[0, 5] := 0.00000; (* Hood draft pressure has no chemical effect *)

    (* Row 1: Molten Steel Bath Bulk Temperature Dynamics T_bath [deg C] *)
    A_mat[1, 0] := 0.00000; (* Carbon content itself does not generate sensible heat *)
    A_mat[1, 1] := 0.99975; (* Thermal inertia & vessel refractory wall heat loss *)
    A_mat[1, 2] := 0.12500; (* Exothermic heat of carbon oxidation [C] + 1/2 O2 -> CO *)
    A_mat[1, 3] := 0.01500; (* Heat release from iron oxidation to FeO *)
    A_mat[1, 4] := 0.00000; (* Acoustic foam transmission does not alter bath temperature *)
    A_mat[1, 5] := 0.00000; (* Draft suction does not directly affect bulk metal heat *)

    (* Row 2: Instantaneous Decarburization Reaction Rate dC/dt [%/min] *)
    A_mat[2, 0] := 0.01550; (* Mass-action dependence on remaining bath carbon *)
    A_mat[2, 1] := 0.00012; (* Arrhenius thermal enhancement of carbon-oxygen chemical kinetics *)
    A_mat[2, 2] := 0.94200; (* First-order relaxation time constant of decarb emulsion zone *)
    A_mat[2, 3] := 0.00450; (* Decarb enhancement by interfacial reaction with FeO-rich slag *)
    A_mat[2, 4] := -0.00085; (* Slag foaming dampens oxygen jet cavity circulation *)
    A_mat[2, 5] := 0.00000; (* Decarb rate invariant with hood draft *)

    (* Row 3: Slag Total FeO Content Dynamics FeO_slag [%] *)
    A_mat[3, 0] := -0.02500; (* High bath carbon drives rapid reduction of FeO back to metal *)
    A_mat[3, 1] := -0.00035; (* Elevated temperature favors thermodynamic FeO reduction by C *)
    A_mat[3, 2] := -0.08500; (* High decarb rate consumes FeO: [C] + (FeO) -> Fe + CO *)
    A_mat[3, 3] := 0.97800; (* Slag FeO chemical persistence and dissolution time constant *)
    A_mat[3, 4] := 0.00550; (* Foaming increases emulsion interfacial area for FeO generation *)
    A_mat[3, 5] := 0.00000; (* Hood draft has no slag thermodynamic influence *)

    (* Row 4: Slag Acoustic Foaming Attenuation Index H_foam [dB] *)
    A_mat[4, 0] := 0.00000; (* Carbon content has no direct acoustic property *)
    A_mat[4, 1] := 0.00080; (* Temperature affects slag viscosity and gas bubble drainage *)
    A_mat[4, 2] := -0.35000; (* Higher decarb generates violent gas bubbles, muffling jet noise *)
    A_mat[4, 3] := -0.18500; (* High FeO lowers slag viscosity, altering foam stability *)
    A_mat[4, 4] := 0.91500; (* Multiphase acoustic wave absorption decay dynamics *)
    A_mat[4, 5] := 0.00000; (* Hood pressure does not affect vessel trunnion sound *)

    (* Row 5: Waste Heat Boiler Hood Differential Draft Pressure DP_hood [Pa] *)
    A_mat[5, 0] := 0.00000; (* Carbon has no direct fluid mechanical effect on draft *)
    A_mat[5, 1] := 0.01500; (* Thermal buoyancy expansion of flue gases entering boiler hood *)
    A_mat[5, 2] := -14.50000; (* Violent decarb releases massive CO gas volume, raising hood pressure *)
    A_mat[5, 3] := 0.00000; (* FeO content does not affect flue gas expansion *)
    A_mat[5, 4] := 0.00000; (* Acoustic foam level does not alter flue gas mechanics *)
    A_mat[5, 5] := 0.86500; (* ID fan evacuation duct fluid pneumatic inertia time constant *)

    (* --------------------------------------------------------------------- *)
    (* INPUT COUPLING MATRIX B (6x5)                                         *)
    (* --------------------------------------------------------------------- *)
    (* B Row 0: Influence on C_bath *)
    B_mat[0, 0] := 0.000005; (* Winch speed alters lance height, shifting jet cavity decarb *)
    B_mat[0, 1] := -0.000085; (* Oxygen supply directly oxidizes carbon: primary driver *)
    B_mat[0, 2] := 0.000000; (* Flux addition has no direct stoichiometric carbon removal *)
    B_mat[0, 3] := -0.000015; (* Bottom stirring enhances steel bath turnover to jet cavity *)
    B_mat[0, 4] := 0.000000; (* Primary damper has no metallurgical effect *)

    (* B Row 1: Influence on T_bath *)
    B_mat[1, 0] := 0.001200; (* Lance position shifts post-combustion thermal radiation back to bath *)
    B_mat[1, 1] := 0.028500; (* Oxygen flow combustion heat generation *)
    B_mat[1, 2] := -0.085000; (* Endothermic dissolution of calcined lime & dolomitic fluxes *)
    B_mat[1, 3] := -0.012500; (* Bottom inert gas thermal sensible cooling effect *)
    B_mat[1, 4] := 0.000000; (* Offgas damper position does not affect bath enthalpy *)

    (* B Row 2: Influence on dC/dt *)
    B_mat[2, 0] := -0.002500; (* Lowering lance (v_lance < 0) deepens cavity, boosting decarb *)
    B_mat[2, 1] := 0.000385; (* Oxygen flow directly accelerates decarburization rate *)
    B_mat[2, 2] := -0.000150; (* Flux addition temporarily slows decarb by cooling reaction zone *)
    B_mat[2, 3] := 0.001850; (* Bottom stirring delivers fresh dissolved carbon to fireclay zone *)
    B_mat[2, 4] := 0.000000; (* Damper position has zero decarb impact *)

    (* B Row 3: Influence on Slag FeO *)
    B_mat[3, 0] := 0.008500; (* Raising lance creates 'soft blow', spraying O2 into slag -> FeO spikes *)
    B_mat[3, 1] := 0.001200; (* Excess oxygen above decarb capacity oxidizes iron to FeO *)
    B_mat[3, 2] := -0.003500; (* Adding active lime dilutes FeO concentration in liquid slag *)
    B_mat[3, 3] := -0.004200; (* Bottom stirring mixes slag and metal, accelerating FeO reduction *)
    B_mat[3, 4] := 0.000000; (* Damper position has no slag chemical effect *)

    (* B Row 4: Influence on Acoustic Foaming H_foam *)
    B_mat[4, 0] := -0.045000; (* Raising lance softens jet impact, attenuating acoustic high frequencies *)
    B_mat[4, 1] := -0.012000; (* Higher O2 blowing expands foam gas hold-up fraction *)
    B_mat[4, 2] := 0.025000; (* Dolomite/flux additions coalesce foam bubbles, breaking foam *)
    B_mat[4, 3] := 0.035000; (* Vigorous bottom stirring ruptures viscous foam emulsion *)
    B_mat[4, 4] := 0.000000; (* Damper position has no trunnion acoustic impact *)

    (* B Row 5: Influence on Hood Draft DP_hood *)
    B_mat[5, 0] := 0.000000; (* Winch velocity has no aerodynamic duct coupling *)
    B_mat[5, 1] := -0.125000; (* More O2 produces more molar gas volume, pressing against hood *)
    B_mat[5, 2] := 0.000000; (* Flux addition produces minor calcination gas *)
    B_mat[5, 3] := -0.045000; (* Bottom stirring gas joins total evacuation volume *)
    B_mat[5, 4] := -1.850000; (* Primary damper opening increases draft suction (more negative Pa) *)

    (* --------------------------------------------------------------------- *)
    (* MEASUREMENT SENSITIVITY MATRIX C (6x6) & DIRECT FEEDTHROUGH D (6x5)   *)
    (* --------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 5 DO
        FOR jIdx := 0 TO 5 DO
            IF iIdx = jIdx THEN
                C_mat[iIdx, jIdx] := 1.0;
            ELSE
                C_mat[iIdx, jIdx] := 0.0;
            END_IF;
        END_FOR;
        FOR kIdx := 0 TO 4 DO
            D_mat[iIdx, kIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* Off-diagonal measurement couplings *)
    C_mat[2, 0] := 0.002; (* Mass spec decarb measurement slight sensitivity to total carbon *)
    C_mat[4, 2] := 0.050; (* Acoustic sensor sensitivity to decarb gas generation rate *)

    (* --------------------------------------------------------------------- *)
    (* KALMAN / LUENBERGER STATE OBSERVER GAIN MATRIX L_obs (6x6)            *)
    (* --------------------------------------------------------------------- *)
    FOR iIdx := 0 TO 5 DO
        FOR jIdx := 0 TO 5 DO
            L_obs[iIdx, jIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* Diagonal innovation filter gains *)
    L_obs[0, 0] := 0.1850; (* Carbon update from sublance & mass spec integration *)
    L_obs[1, 1] := 0.1450; (* Temperature update from sublance direct immersion *)
    L_obs[2, 2] := 0.3200; (* Decarb rate innovation update from offgas mass spec *)
    L_obs[3, 3] := 0.1650; (* Slag FeO innovation update from oxygen balance model *)
    L_obs[4, 4] := 0.2850; (* Foaming height index innovation from trunnion accelerometers *)
    L_obs[5, 5] := 0.4200; (* Hood draft innovation update from boiler DP transmitter *)

    (* Cross-channel observer correction gains *)
    L_obs[0, 2] := -0.0450; (* Higher measured decarb pulls down estimated bath carbon *)
    L_obs[1, 2] := 0.0850;  (* High decarb innovation boosts bath temperature estimate *)
    L_obs[3, 2] := -0.0650; (* Higher decarb pulls down estimated slag FeO *)
    L_obs[4, 3] := 0.0750;  (* FeO correction updates acoustic foam index estimate *)

    (* --------------------------------------------------------------------- *)
    (* INITIALIZE MPC REFERENCE TRAJECTORY & ACTUATOR VECTORS                *)
    (* --------------------------------------------------------------------- *)
    x_ref[0] := rTargetTapCarbon_pct;
    x_ref[1] := rTargetTapTemperature_degC;
    x_ref[2] := 0.050;
    x_ref[3] := 17.5;
    x_ref[4] := 78.0;
    x_ref[5] := -150.0;

    FOR iIdx := 0 TO 4 DO
        FOR jIdx := 0 TO 4 DO
            u_traj[iIdx, jIdx] := u_curr[jIdx];
        END_FOR;
    END_FOR;

    FOR iIdx := 0 TO 5 DO
        FOR jIdx := 0 TO 5 DO
            x_traj[iIdx, jIdx] := x_est[jIdx];
        END_FOR;
    END_FOR;

    bConfigInitialized := TRUE;
    bFirstScanDone := TRUE;
END_IF;

(* ========================================================================= *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINE       *)
(* ========================================================================= *)
(* This phase processes 4 safety-critical instrumentation groups with         *)
(* millisecond-level discrepancy persistence timers, median mid-value         *)
(* selection, 2oo3 to 1oo2 to 1oo1 bumpless degradation, and rate slew-clamping.*)

(* ------------------------------------------------------------------------- *)
(* SENSOR GROUP 1: MAIN OXYGEN SUPPLY HEADER PRESSURE [bar]                  *)
(* Normal operating range: 12.0 to 18.0 bar(g). Discrepancy tolerance: 1.20 bar*)
(* ------------------------------------------------------------------------- *)
(* Step 1.1: Range Check (Hard Electrical & Transmitter Limits: 2.0 to 28.0 bar) *)
IF (rO2_SupplyPressure_Ch1_bar < 2.0) OR (rO2_SupplyPressure_Ch1_bar > 28.0) THEN
    rO2_Press_Ch1_DiscTimer_s := rO2_Press_Ch1_DiscTimer_s + rCycleTime_dt_s;
    IF rO2_Press_Ch1_DiscTimer_s >= 0.400 THEN
        bO2_Press_Ch1_Fail := TRUE;
    END_IF;
ELSE
    (* Inter-channel discrepancy validation relative to other channels *)
    IF NOT bO2_Press_Ch2_Fail AND NOT bO2_Press_Ch3_Fail THEN
        IF (ABS(rO2_SupplyPressure_Ch1_bar - rO2_SupplyPressure_Ch2_bar) > 1.20) AND
           (ABS(rO2_SupplyPressure_Ch1_bar - rO2_SupplyPressure_Ch3_bar) > 1.20) THEN
            rO2_Press_Ch1_DiscTimer_s := rO2_Press_Ch1_DiscTimer_s + rCycleTime_dt_s;
            IF rO2_Press_Ch1_DiscTimer_s >= 0.500 THEN
                bO2_Press_Ch1_Fail := TRUE;
            END_IF;
        ELSE
            rO2_Press_Ch1_DiscTimer_s := MAX(0.0, rO2_Press_Ch1_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bO2_Press_Ch1_Fail := FALSE;
        END_IF;
    ELSE
        rO2_Press_Ch1_DiscTimer_s := 0.0;
        bO2_Press_Ch1_Fail := FALSE;
    END_IF;
END_IF;

IF (rO2_SupplyPressure_Ch2_bar < 2.0) OR (rO2_SupplyPressure_Ch2_bar > 28.0) THEN
    rO2_Press_Ch2_DiscTimer_s := rO2_Press_Ch2_DiscTimer_s + rCycleTime_dt_s;
    IF rO2_Press_Ch2_DiscTimer_s >= 0.400 THEN
        bO2_Press_Ch2_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bO2_Press_Ch1_Fail AND NOT bO2_Press_Ch3_Fail THEN
        IF (ABS(rO2_SupplyPressure_Ch2_bar - rO2_SupplyPressure_Ch1_bar) > 1.20) AND
           (ABS(rO2_SupplyPressure_Ch2_bar - rO2_SupplyPressure_Ch3_bar) > 1.20) THEN
            rO2_Press_Ch2_DiscTimer_s := rO2_Press_Ch2_DiscTimer_s + rCycleTime_dt_s;
            IF rO2_Press_Ch2_DiscTimer_s >= 0.500 THEN
                bO2_Press_Ch2_Fail := TRUE;
            END_IF;
        ELSE
            rO2_Press_Ch2_DiscTimer_s := MAX(0.0, rO2_Press_Ch2_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bO2_Press_Ch2_Fail := FALSE;
        END_IF;
    ELSE
        rO2_Press_Ch2_DiscTimer_s := 0.0;
        bO2_Press_Ch2_Fail := FALSE;
    END_IF;
END_IF;

IF (rO2_SupplyPressure_Ch3_bar < 2.0) OR (rO2_SupplyPressure_Ch3_bar > 28.0) THEN
    rO2_Press_Ch3_DiscTimer_s := rO2_Press_Ch3_DiscTimer_s + rCycleTime_dt_s;
    IF rO2_Press_Ch3_DiscTimer_s >= 0.400 THEN
        bO2_Press_Ch3_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bO2_Press_Ch1_Fail AND NOT bO2_Press_Ch2_Fail THEN
        IF (ABS(rO2_SupplyPressure_Ch3_bar - rO2_SupplyPressure_Ch1_bar) > 1.20) AND
           (ABS(rO2_SupplyPressure_Ch3_bar - rO2_SupplyPressure_Ch2_bar) > 1.20) THEN
            rO2_Press_Ch3_DiscTimer_s := rO2_Press_Ch3_DiscTimer_s + rCycleTime_dt_s;
            IF rO2_Press_Ch3_DiscTimer_s >= 0.500 THEN
                bO2_Press_Ch3_Fail := TRUE;
            END_IF;
        ELSE
            rO2_Press_Ch3_DiscTimer_s := MAX(0.0, rO2_Press_Ch3_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bO2_Press_Ch3_Fail := FALSE;
        END_IF;
    ELSE
        rO2_Press_Ch3_DiscTimer_s := 0.0;
        bO2_Press_Ch3_Fail := FALSE;
    END_IF;
END_IF;

(* Step 1.2: O2 Pressure Health Evaluation & Voting Execution *)
iO2_Press_HealthySensors := 0;
IF NOT bO2_Press_Ch1_Fail THEN iO2_Press_HealthySensors := iO2_Press_HealthySensors + 1; END_IF;
IF NOT bO2_Press_Ch2_Fail THEN iO2_Press_HealthySensors := iO2_Press_HealthySensors + 1; END_IF;
IF NOT bO2_Press_Ch3_Fail THEN iO2_Press_HealthySensors := iO2_Press_HealthySensors + 1; END_IF;

IF iO2_Press_HealthySensors = 3 THEN
    (* 3 Healthy: Exact Median (Mid-Value) Voting *)
    IF ((rO2_SupplyPressure_Ch1_bar >= rO2_SupplyPressure_Ch2_bar AND rO2_SupplyPressure_Ch1_bar <= rO2_SupplyPressure_Ch3_bar) OR
        (rO2_SupplyPressure_Ch1_bar <= rO2_SupplyPressure_Ch2_bar AND rO2_SupplyPressure_Ch1_bar >= rO2_SupplyPressure_Ch3_bar)) THEN
        rTmpVal := rO2_SupplyPressure_Ch1_bar;
    ELSIF ((rO2_SupplyPressure_Ch2_bar >= rO2_SupplyPressure_Ch1_bar AND rO2_SupplyPressure_Ch2_bar <= rO2_SupplyPressure_Ch3_bar) OR
           (rO2_SupplyPressure_Ch2_bar <= rO2_SupplyPressure_Ch1_bar AND rO2_SupplyPressure_Ch2_bar >= rO2_SupplyPressure_Ch3_bar)) THEN
        rTmpVal := rO2_SupplyPressure_Ch2_bar;
    ELSE
        rTmpVal := rO2_SupplyPressure_Ch3_bar;
    END_IF;
ELSIF iO2_Press_HealthySensors = 2 THEN
    (* 2 Healthy: 1oo2 Average Degradation *)
    IF NOT bO2_Press_Ch1_Fail AND NOT bO2_Press_Ch2_Fail THEN
        rTmpVal := (rO2_SupplyPressure_Ch1_bar + rO2_SupplyPressure_Ch2_bar) * 0.50;
    ELSIF NOT bO2_Press_Ch1_Fail AND NOT bO2_Press_Ch3_Fail THEN
        rTmpVal := (rO2_SupplyPressure_Ch1_bar + rO2_SupplyPressure_Ch3_bar) * 0.50;
    ELSE
        rTmpVal := (rO2_SupplyPressure_Ch2_bar + rO2_SupplyPressure_Ch3_bar) * 0.50;
    END_IF;
ELSIF iO2_Press_HealthySensors = 1 THEN
    (* 1 Healthy: Fallback to lone operational sensor *)
    IF NOT bO2_Press_Ch1_Fail THEN
        rTmpVal := rO2_SupplyPressure_Ch1_bar;
    ELSIF NOT bO2_Press_Ch2_Fail THEN
        rTmpVal := rO2_SupplyPressure_Ch2_bar;
    ELSE
        rTmpVal := rO2_SupplyPressure_Ch3_bar;
    END_IF;
ELSE
    (* 0 Healthy: Freeze to last voted reading, assert fault *)
    rTmpVal := rO2_Press_Voted;
END_IF;

(* Slew-rate clamping for bumpless transition: Max 2.5 bar/s *)
IF ABS(rTmpVal - rO2_Press_Voted) > (2.50 * rCycleTime_dt_s) THEN
    IF rTmpVal > rO2_Press_Voted THEN
        rO2_Press_Voted := rO2_Press_Voted + (2.50 * rCycleTime_dt_s);
    ELSE
        rO2_Press_Voted := rO2_Press_Voted - (2.50 * rCycleTime_dt_s);
    END_IF;
ELSE
    rO2_Press_Voted := rTmpVal;
END_IF;

(* ------------------------------------------------------------------------- *)
(* SENSOR GROUP 2: LANCE COOLING WATER INLET-OUTLET DELTA T [deg C]          *)
(* Normal range: 12.0 to 24.0 deg C. Discrepancy tolerance: 3.50 deg C      *)
(* Extreme safety criticality: RTD burn-out or water boil hazard             *)
(* ------------------------------------------------------------------------- *)
(* Step 2.1: Range Check (Physical RTD Limits: 0.0 to 65.0 deg C) *)
IF (rLanceWaterDeltaT_Ch1_degC < 0.0) OR (rLanceWaterDeltaT_Ch1_degC > 65.0) THEN
    rLanceDeltaT_Ch1_DiscTimer_s := rLanceDeltaT_Ch1_DiscTimer_s + rCycleTime_dt_s;
    IF rLanceDeltaT_Ch1_DiscTimer_s >= 0.350 THEN
        bLanceDeltaT_Ch1_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bLanceDeltaT_Ch2_Fail AND NOT bLanceDeltaT_Ch3_Fail THEN
        IF (ABS(rLanceWaterDeltaT_Ch1_degC - rLanceWaterDeltaT_Ch2_degC) > 3.50) AND
           (ABS(rLanceWaterDeltaT_Ch1_degC - rLanceWaterDeltaT_Ch3_degC) > 3.50) THEN
            rLanceDeltaT_Ch1_DiscTimer_s := rLanceDeltaT_Ch1_DiscTimer_s + rCycleTime_dt_s;
            IF rLanceDeltaT_Ch1_DiscTimer_s >= 0.450 THEN
                bLanceDeltaT_Ch1_Fail := TRUE;
            END_IF;
        ELSE
            rLanceDeltaT_Ch1_DiscTimer_s := MAX(0.0, rLanceDeltaT_Ch1_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bLanceDeltaT_Ch1_Fail := FALSE;
        END_IF;
    ELSE
        rLanceDeltaT_Ch1_DiscTimer_s := 0.0;
        bLanceDeltaT_Ch1_Fail := FALSE;
    END_IF;
END_IF;

IF (rLanceWaterDeltaT_Ch2_degC < 0.0) OR (rLanceWaterDeltaT_Ch2_degC > 65.0) THEN
    rLanceDeltaT_Ch2_DiscTimer_s := rLanceDeltaT_Ch2_DiscTimer_s + rCycleTime_dt_s;
    IF rLanceDeltaT_Ch2_DiscTimer_s >= 0.350 THEN
        bLanceDeltaT_Ch2_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bLanceDeltaT_Ch1_Fail AND NOT bLanceDeltaT_Ch3_Fail THEN
        IF (ABS(rLanceWaterDeltaT_Ch2_degC - rLanceWaterDeltaT_Ch1_degC) > 3.50) AND
           (ABS(rLanceWaterDeltaT_Ch2_degC - rLanceWaterDeltaT_Ch3_degC) > 3.50) THEN
            rLanceDeltaT_Ch2_DiscTimer_s := rLanceDeltaT_Ch2_DiscTimer_s + rCycleTime_dt_s;
            IF rLanceDeltaT_Ch2_DiscTimer_s >= 0.450 THEN
                bLanceDeltaT_Ch2_Fail := TRUE;
            END_IF;
        ELSE
            rLanceDeltaT_Ch2_DiscTimer_s := MAX(0.0, rLanceDeltaT_Ch2_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bLanceDeltaT_Ch2_Fail := FALSE;
        END_IF;
    ELSE
        rLanceDeltaT_Ch2_DiscTimer_s := 0.0;
        bLanceDeltaT_Ch2_Fail := FALSE;
    END_IF;
END_IF;

IF (rLanceWaterDeltaT_Ch3_degC < 0.0) OR (rLanceWaterDeltaT_Ch3_degC > 65.0) THEN
    rLanceDeltaT_Ch3_DiscTimer_s := rLanceDeltaT_Ch3_DiscTimer_s + rCycleTime_dt_s;
    IF rLanceDeltaT_Ch3_DiscTimer_s >= 0.350 THEN
        bLanceDeltaT_Ch3_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bLanceDeltaT_Ch1_Fail AND NOT bLanceDeltaT_Ch2_Fail THEN
        IF (ABS(rLanceWaterDeltaT_Ch3_degC - rLanceWaterDeltaT_Ch1_degC) > 3.50) AND
           (ABS(rLanceWaterDeltaT_Ch3_degC - rLanceWaterDeltaT_Ch2_degC) > 3.50) THEN
            rLanceDeltaT_Ch3_DiscTimer_s := rLanceDeltaT_Ch3_DiscTimer_s + rCycleTime_dt_s;
            IF rLanceDeltaT_Ch3_DiscTimer_s >= 0.450 THEN
                bLanceDeltaT_Ch3_Fail := TRUE;
            END_IF;
        ELSE
            rLanceDeltaT_Ch3_DiscTimer_s := MAX(0.0, rLanceDeltaT_Ch3_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bLanceDeltaT_Ch3_Fail := FALSE;
        END_IF;
    ELSE
        rLanceDeltaT_Ch3_DiscTimer_s := 0.0;
        bLanceDeltaT_Ch3_Fail := FALSE;
    END_IF;
END_IF;

(* Step 2.2: Lance Delta T Health Evaluation & Voting Execution *)
iLanceDeltaT_HealthySensors := 0;
IF NOT bLanceDeltaT_Ch1_Fail THEN iLanceDeltaT_HealthySensors := iLanceDeltaT_HealthySensors + 1; END_IF;
IF NOT bLanceDeltaT_Ch2_Fail THEN iLanceDeltaT_HealthySensors := iLanceDeltaT_HealthySensors + 1; END_IF;
IF NOT bLanceDeltaT_Ch3_Fail THEN iLanceDeltaT_HealthySensors := iLanceDeltaT_HealthySensors + 1; END_IF;

IF iLanceDeltaT_HealthySensors = 3 THEN
    IF ((rLanceWaterDeltaT_Ch1_degC >= rLanceWaterDeltaT_Ch2_degC AND rLanceWaterDeltaT_Ch1_degC <= rLanceWaterDeltaT_Ch3_degC) OR
        (rLanceWaterDeltaT_Ch1_degC <= rLanceWaterDeltaT_Ch2_degC AND rLanceWaterDeltaT_Ch1_degC >= rLanceWaterDeltaT_Ch3_degC)) THEN
        rTmpVal := rLanceWaterDeltaT_Ch1_degC;
    ELSIF ((rLanceWaterDeltaT_Ch2_degC >= rLanceWaterDeltaT_Ch1_degC AND rLanceWaterDeltaT_Ch2_degC <= rLanceWaterDeltaT_Ch3_degC) OR
           (rLanceWaterDeltaT_Ch2_degC <= rLanceWaterDeltaT_Ch1_degC AND rLanceWaterDeltaT_Ch2_degC >= rLanceWaterDeltaT_Ch3_degC)) THEN
        rTmpVal := rLanceWaterDeltaT_Ch2_degC;
    ELSE
        rTmpVal := rLanceWaterDeltaT_Ch3_degC;
    END_IF;
ELSIF iLanceDeltaT_HealthySensors = 2 THEN
    IF NOT bLanceDeltaT_Ch1_Fail AND NOT bLanceDeltaT_Ch2_Fail THEN
        rTmpVal := (rLanceWaterDeltaT_Ch1_degC + rLanceWaterDeltaT_Ch2_degC) * 0.50;
    ELSIF NOT bLanceDeltaT_Ch1_Fail AND NOT bLanceDeltaT_Ch3_Fail THEN
        rTmpVal := (rLanceWaterDeltaT_Ch1_degC + rLanceWaterDeltaT_Ch3_degC) * 0.50;
    ELSE
        rTmpVal := (rLanceWaterDeltaT_Ch2_degC + rLanceWaterDeltaT_Ch3_degC) * 0.50;
    END_IF;
ELSIF iLanceDeltaT_HealthySensors = 1 THEN
    IF NOT bLanceDeltaT_Ch1_Fail THEN
        rTmpVal := rLanceWaterDeltaT_Ch1_degC;
    ELSIF NOT bLanceDeltaT_Ch2_Fail THEN
        rTmpVal := rLanceWaterDeltaT_Ch2_degC;
    ELSE
        rTmpVal := rLanceWaterDeltaT_Ch3_degC;
    END_IF;
ELSE
    rTmpVal := rLanceDeltaT_Voted;
END_IF;

(* Slew-rate clamping: Max 3.0 deg C/s *)
IF ABS(rTmpVal - rLanceDeltaT_Voted) > (3.00 * rCycleTime_dt_s) THEN
    IF rTmpVal > rLanceDeltaT_Voted THEN
        rLanceDeltaT_Voted := rLanceDeltaT_Voted + (3.00 * rCycleTime_dt_s);
    ELSE
        rLanceDeltaT_Voted := rLanceDeltaT_Voted - (3.00 * rCycleTime_dt_s);
    END_IF;
ELSE
    rLanceDeltaT_Voted := rTmpVal;
END_IF;

(* ------------------------------------------------------------------------- *)
(* SENSOR GROUP 3: TRUNNION PIEZO ACOUSTIC ACCELEROMETERS [dB]               *)
(* Normal range: 60.0 to 110.0 dB. Discrepancy tolerance: 8.0 dB             *)
(* Critical for acoustic slopping and slag foaming early warning             *)
(* ------------------------------------------------------------------------- *)
(* Step 3.1: Range Check (Accelerometer Signal Limits: 30.0 to 135.0 dB) *)
IF (rTrunnionAcoustic_Ch1_dB < 30.0) OR (rTrunnionAcoustic_Ch1_dB > 135.0) THEN
    rTrunnionAcoustic_Ch1_DiscTimer_s := rTrunnionAcoustic_Ch1_DiscTimer_s + rCycleTime_dt_s;
    IF rTrunnionAcoustic_Ch1_DiscTimer_s >= 0.500 THEN
        bTrunnionAcoustic_Ch1_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bTrunnionAcoustic_Ch2_Fail AND NOT bTrunnionAcoustic_Ch3_Fail THEN
        IF (ABS(rTrunnionAcoustic_Ch1_dB - rTrunnionAcoustic_Ch2_dB) > 8.0) AND
           (ABS(rTrunnionAcoustic_Ch1_dB - rTrunnionAcoustic_Ch3_dB) > 8.0) THEN
            rTrunnionAcoustic_Ch1_DiscTimer_s := rTrunnionAcoustic_Ch1_DiscTimer_s + rCycleTime_dt_s;
            IF rTrunnionAcoustic_Ch1_DiscTimer_s >= 0.600 THEN
                bTrunnionAcoustic_Ch1_Fail := TRUE;
            END_IF;
        ELSE
            rTrunnionAcoustic_Ch1_DiscTimer_s := MAX(0.0, rTrunnionAcoustic_Ch1_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bTrunnionAcoustic_Ch1_Fail := FALSE;
        END_IF;
    ELSE
        rTrunnionAcoustic_Ch1_DiscTimer_s := 0.0;
        bTrunnionAcoustic_Ch1_Fail := FALSE;
    END_IF;
END_IF;

IF (rTrunnionAcoustic_Ch2_dB < 30.0) OR (rTrunnionAcoustic_Ch2_dB > 135.0) THEN
    rTrunnionAcoustic_Ch2_DiscTimer_s := rTrunnionAcoustic_Ch2_DiscTimer_s + rCycleTime_dt_s;
    IF rTrunnionAcoustic_Ch2_DiscTimer_s >= 0.500 THEN
        bTrunnionAcoustic_Ch2_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bTrunnionAcoustic_Ch1_Fail AND NOT bTrunnionAcoustic_Ch3_Fail THEN
        IF (ABS(rTrunnionAcoustic_Ch2_dB - rTrunnionAcoustic_Ch1_dB) > 8.0) AND
           (ABS(rTrunnionAcoustic_Ch2_dB - rTrunnionAcoustic_Ch3_dB) > 8.0) THEN
            rTrunnionAcoustic_Ch2_DiscTimer_s := rTrunnionAcoustic_Ch2_DiscTimer_s + rCycleTime_dt_s;
            IF rTrunnionAcoustic_Ch2_DiscTimer_s >= 0.600 THEN
                bTrunnionAcoustic_Ch2_Fail := TRUE;
            END_IF;
        ELSE
            rTrunnionAcoustic_Ch2_DiscTimer_s := MAX(0.0, rTrunnionAcoustic_Ch2_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bTrunnionAcoustic_Ch2_Fail := FALSE;
        END_IF;
    ELSE
        rTrunnionAcoustic_Ch2_DiscTimer_s := 0.0;
        bTrunnionAcoustic_Ch2_Fail := FALSE;
    END_IF;
END_IF;

IF (rTrunnionAcoustic_Ch3_dB < 30.0) OR (rTrunnionAcoustic_Ch3_dB > 135.0) THEN
    rTrunnionAcoustic_Ch3_DiscTimer_s := rTrunnionAcoustic_Ch3_DiscTimer_s + rCycleTime_dt_s;
    IF rTrunnionAcoustic_Ch3_DiscTimer_s >= 0.500 THEN
        bTrunnionAcoustic_Ch3_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bTrunnionAcoustic_Ch1_Fail AND NOT bTrunnionAcoustic_Ch2_Fail THEN
        IF (ABS(rTrunnionAcoustic_Ch3_dB - rTrunnionAcoustic_Ch1_dB) > 8.0) AND
           (ABS(rTrunnionAcoustic_Ch3_dB - rTrunnionAcoustic_Ch2_dB) > 8.0) THEN
            rTrunnionAcoustic_Ch3_DiscTimer_s := rTrunnionAcoustic_Ch3_DiscTimer_s + rCycleTime_dt_s;
            IF rTrunnionAcoustic_Ch3_DiscTimer_s >= 0.600 THEN
                bTrunnionAcoustic_Ch3_Fail := TRUE;
            END_IF;
        ELSE
            rTrunnionAcoustic_Ch3_DiscTimer_s := MAX(0.0, rTrunnionAcoustic_Ch3_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bTrunnionAcoustic_Ch3_Fail := FALSE;
        END_IF;
    ELSE
        rTrunnionAcoustic_Ch3_DiscTimer_s := 0.0;
        bTrunnionAcoustic_Ch3_Fail := FALSE;
    END_IF;
END_IF;

(* Step 3.2: Acoustic Health Evaluation & Voting Execution *)
iTrunnionAcoustic_HealthySensors := 0;
IF NOT bTrunnionAcoustic_Ch1_Fail THEN iTrunnionAcoustic_HealthySensors := iTrunnionAcoustic_HealthySensors + 1; END_IF;
IF NOT bTrunnionAcoustic_Ch2_Fail THEN iTrunnionAcoustic_HealthySensors := iTrunnionAcoustic_HealthySensors + 1; END_IF;
IF NOT bTrunnionAcoustic_Ch3_Fail THEN iTrunnionAcoustic_HealthySensors := iTrunnionAcoustic_HealthySensors + 1; END_IF;

IF iTrunnionAcoustic_HealthySensors = 3 THEN
    IF ((rTrunnionAcoustic_Ch1_dB >= rTrunnionAcoustic_Ch2_dB AND rTrunnionAcoustic_Ch1_dB <= rTrunnionAcoustic_Ch3_dB) OR
        (rTrunnionAcoustic_Ch1_dB <= rTrunnionAcoustic_Ch2_dB AND rTrunnionAcoustic_Ch1_dB >= rTrunnionAcoustic_Ch3_dB)) THEN
        rTmpVal := rTrunnionAcoustic_Ch1_dB;
    ELSIF ((rTrunnionAcoustic_Ch2_dB >= rTrunnionAcoustic_Ch1_dB AND rTrunnionAcoustic_Ch2_dB <= rTrunnionAcoustic_Ch3_dB) OR
           (rTrunnionAcoustic_Ch2_dB <= rTrunnionAcoustic_Ch1_dB AND rTrunnionAcoustic_Ch2_dB >= rTrunnionAcoustic_Ch3_dB)) THEN
        rTmpVal := rTrunnionAcoustic_Ch2_dB;
    ELSE
        rTmpVal := rTrunnionAcoustic_Ch3_dB;
    END_IF;
ELSIF iTrunnionAcoustic_HealthySensors = 2 THEN
    IF NOT bTrunnionAcoustic_Ch1_Fail AND NOT bTrunnionAcoustic_Ch2_Fail THEN
        rTmpVal := (rTrunnionAcoustic_Ch1_dB + rTrunnionAcoustic_Ch2_dB) * 0.50;
    ELSIF NOT bTrunnionAcoustic_Ch1_Fail AND NOT bTrunnionAcoustic_Ch3_Fail THEN
        rTmpVal := (rTrunnionAcoustic_Ch1_dB + rTrunnionAcoustic_Ch3_dB) * 0.50;
    ELSE
        rTmpVal := (rTrunnionAcoustic_Ch2_dB + rTrunnionAcoustic_Ch3_dB) * 0.50;
    END_IF;
ELSIF iTrunnionAcoustic_HealthySensors = 1 THEN
    IF NOT bTrunnionAcoustic_Ch1_Fail THEN
        rTmpVal := rTrunnionAcoustic_Ch1_dB;
    ELSIF NOT bTrunnionAcoustic_Ch2_Fail THEN
        rTmpVal := rTrunnionAcoustic_Ch2_dB;
    ELSE
        rTmpVal := rTrunnionAcoustic_Ch3_dB;
    END_IF;
ELSE
    rTmpVal := rTrunnionAcoustic_Voted;
END_IF;

(* Slew-rate clamping: Max 10.0 dB/s *)
IF ABS(rTmpVal - rTrunnionAcoustic_Voted) > (10.00 * rCycleTime_dt_s) THEN
    IF rTmpVal > rTrunnionAcoustic_Voted THEN
        rTrunnionAcoustic_Voted := rTrunnionAcoustic_Voted + (10.00 * rCycleTime_dt_s);
    ELSE
        rTrunnionAcoustic_Voted := rTrunnionAcoustic_Voted - (10.00 * rCycleTime_dt_s);
    END_IF;
ELSE
    rTrunnionAcoustic_Voted := rTmpVal;
END_IF;

(* ------------------------------------------------------------------------- *)
(* SENSOR GROUP 4: OFFGAS MASS SPECTROMETER CO CONCENTRATION [% vol CO]       *)
(* Normal range: 0.0 to 80.0 vol% CO. Discrepancy tolerance: 4.50 vol% CO   *)
(* Determines dynamic decarburization rate dC/dt & OG gas recovery readiness *)
(* ------------------------------------------------------------------------- *)
(* Step 4.1: Range Check (Mass Spec Output Limits: 0.0 to 95.0 vol% CO) *)
IF (rOffgas_CO_Ch1_pct < 0.0) OR (rOffgas_CO_Ch1_pct > 95.0) THEN
    rOffgas_CO_Ch1_DiscTimer_s := rOffgas_CO_Ch1_DiscTimer_s + rCycleTime_dt_s;
    IF rOffgas_CO_Ch1_DiscTimer_s >= 0.500 THEN
        bOffgas_CO_Ch1_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bOffgas_CO_Ch2_Fail AND NOT bOffgas_CO_Ch3_Fail THEN
        IF (ABS(rOffgas_CO_Ch1_pct - rOffgas_CO_Ch2_pct) > 4.50) AND
           (ABS(rOffgas_CO_Ch1_pct - rOffgas_CO_Ch3_pct) > 4.50) THEN
            rOffgas_CO_Ch1_DiscTimer_s := rOffgas_CO_Ch1_DiscTimer_s + rCycleTime_dt_s;
            IF rOffgas_CO_Ch1_DiscTimer_s >= 0.600 THEN
                bOffgas_CO_Ch1_Fail := TRUE;
            END_IF;
        ELSE
            rOffgas_CO_Ch1_DiscTimer_s := MAX(0.0, rOffgas_CO_Ch1_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bOffgas_CO_Ch1_Fail := FALSE;
        END_IF;
    ELSE
        rOffgas_CO_Ch1_DiscTimer_s := 0.0;
        bOffgas_CO_Ch1_Fail := FALSE;
    END_IF;
END_IF;

IF (rOffgas_CO_Ch2_pct < 0.0) OR (rOffgas_CO_Ch2_pct > 95.0) THEN
    rOffgas_CO_Ch2_DiscTimer_s := rOffgas_CO_Ch2_DiscTimer_s + rCycleTime_dt_s;
    IF rOffgas_CO_Ch2_DiscTimer_s >= 0.500 THEN
        bOffgas_CO_Ch2_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bOffgas_CO_Ch1_Fail AND NOT bOffgas_CO_Ch3_Fail THEN
        IF (ABS(rOffgas_CO_Ch2_pct - rOffgas_CO_Ch1_pct) > 4.50) AND
           (ABS(rOffgas_CO_Ch2_pct - rOffgas_CO_Ch3_pct) > 4.50) THEN
            rOffgas_CO_Ch2_DiscTimer_s := rOffgas_CO_Ch2_DiscTimer_s + rCycleTime_dt_s;
            IF rOffgas_CO_Ch2_DiscTimer_s >= 0.600 THEN
                bOffgas_CO_Ch2_Fail := TRUE;
            END_IF;
        ELSE
            rOffgas_CO_Ch2_DiscTimer_s := MAX(0.0, rOffgas_CO_Ch2_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bOffgas_CO_Ch2_Fail := FALSE;
        END_IF;
    ELSE
        rOffgas_CO_Ch2_DiscTimer_s := 0.0;
        bOffgas_CO_Ch2_Fail := FALSE;
    END_IF;
END_IF;

IF (rOffgas_CO_Ch3_pct < 0.0) OR (rOffgas_CO_Ch3_pct > 95.0) THEN
    rOffgas_CO_Ch3_DiscTimer_s := rOffgas_CO_Ch3_DiscTimer_s + rCycleTime_dt_s;
    IF rOffgas_CO_Ch3_DiscTimer_s >= 0.500 THEN
        bOffgas_CO_Ch3_Fail := TRUE;
    END_IF;
ELSE
    IF NOT bOffgas_CO_Ch1_Fail AND NOT bOffgas_CO_Ch2_Fail THEN
        IF (ABS(rOffgas_CO_Ch3_pct - rOffgas_CO_Ch1_pct) > 4.50) AND
           (ABS(rOffgas_CO_Ch3_pct - rOffgas_CO_Ch2_pct) > 4.50) THEN
            rOffgas_CO_Ch3_DiscTimer_s := rOffgas_CO_Ch3_DiscTimer_s + rCycleTime_dt_s;
            IF rOffgas_CO_Ch3_DiscTimer_s >= 0.600 THEN
                bOffgas_CO_Ch3_Fail := TRUE;
            END_IF;
        ELSE
            rOffgas_CO_Ch3_DiscTimer_s := MAX(0.0, rOffgas_CO_Ch3_DiscTimer_s - rCycleTime_dt_s * 2.0);
            bOffgas_CO_Ch3_Fail := FALSE;
        END_IF;
    ELSE
        rOffgas_CO_Ch3_DiscTimer_s := 0.0;
        bOffgas_CO_Ch3_Fail := FALSE;
    END_IF;
END_IF;

(* Step 4.2: Offgas CO Health Evaluation & Voting Execution *)
iOffgas_CO_HealthySensors := 0;
IF NOT bOffgas_CO_Ch1_Fail THEN iOffgas_CO_HealthySensors := iOffgas_CO_HealthySensors + 1; END_IF;
IF NOT bOffgas_CO_Ch2_Fail THEN iOffgas_CO_HealthySensors := iOffgas_CO_HealthySensors + 1; END_IF;
IF NOT bOffgas_CO_Ch3_Fail THEN iOffgas_CO_HealthySensors := iOffgas_CO_HealthySensors + 1; END_IF;

IF iOffgas_CO_HealthySensors = 3 THEN
    IF ((rOffgas_CO_Ch1_pct >= rOffgas_CO_Ch2_pct AND rOffgas_CO_Ch1_pct <= rOffgas_CO_Ch3_pct) OR
        (rOffgas_CO_Ch1_pct <= rOffgas_CO_Ch2_pct AND rOffgas_CO_Ch1_pct >= rOffgas_CO_Ch3_pct)) THEN
        rTmpVal := rOffgas_CO_Ch1_pct;
    ELSIF ((rOffgas_CO_Ch2_pct >= rOffgas_CO_Ch1_pct AND rOffgas_CO_Ch2_pct <= rOffgas_CO_Ch3_pct) OR
           (rOffgas_CO_Ch2_pct <= rOffgas_CO_Ch1_pct AND rOffgas_CO_Ch2_pct >= rOffgas_CO_Ch3_pct)) THEN
        rTmpVal := rOffgas_CO_Ch2_pct;
    ELSE
        rTmpVal := rOffgas_CO_Ch3_pct;
    END_IF;
ELSIF iOffgas_CO_HealthySensors = 2 THEN
    IF NOT bOffgas_CO_Ch1_Fail AND NOT bOffgas_CO_Ch2_Fail THEN
        rTmpVal := (rOffgas_CO_Ch1_pct + rOffgas_CO_Ch2_pct) * 0.50;
    ELSIF NOT bOffgas_CO_Ch1_Fail AND NOT bOffgas_CO_Ch3_Fail THEN
        rTmpVal := (rOffgas_CO_Ch1_pct + rOffgas_CO_Ch3_pct) * 0.50;
    ELSE
        rTmpVal := (rOffgas_CO_Ch2_pct + rOffgas_CO_Ch3_pct) * 0.50;
    END_IF;
ELSIF iOffgas_CO_HealthySensors = 1 THEN
    IF NOT bOffgas_CO_Ch1_Fail THEN
        rTmpVal := rOffgas_CO_Ch1_pct;
    ELSIF NOT bOffgas_CO_Ch2_Fail THEN
        rTmpVal := rOffgas_CO_Ch2_pct;
    ELSE
        rTmpVal := rOffgas_CO_Ch3_pct;
    END_IF;
ELSE
    rTmpVal := rOffgas_CO_Voted;
END_IF;

(* Slew-rate clamping: Max 15.0 % vol/s *)
IF ABS(rTmpVal - rOffgas_CO_Voted) > (15.00 * rCycleTime_dt_s) THEN
    IF rTmpVal > rOffgas_CO_Voted THEN
        rOffgas_CO_Voted := rOffgas_CO_Voted + (15.00 * rCycleTime_dt_s);
    ELSE
        rOffgas_CO_Voted := rOffgas_CO_Voted - (15.00 * rCycleTime_dt_s);
    END_IF;
ELSE
    rOffgas_CO_Voted := rTmpVal;
END_IF;

(* TMR Overall Health Alarm Flag *)
bAlarm_TmrDegraded := (iO2_Press_HealthySensors < 3) OR (iLanceDeltaT_HealthySensors < 3) OR
                       (iTrunnionAcoustic_HealthySensors < 3) OR (iOffgas_CO_HealthySensors < 3);

(* ========================================================================= *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE OBSERVER             *)
(* ========================================================================= *)
(* Real-time thermodynamic, fluid-mechanical, compressible flow, and          *)
(* metallurgical reaction kinetics coupling to 6x6 discrete state observer.  *)

(* ------------------------------------------------------------------------- *)
(* STEP 2.1: TOTAL LIQUID STEEL MASS & ENTHALPY INERTIA EVALUATION           *)
(* ------------------------------------------------------------------------- *)
rTotalSteelMass_t := rHotMetalChargeWeight_t + (rScrapChargeWeight_t * 0.94);
IF rTotalSteelMass_t < 150.0 THEN
    rTotalSteelMass_t := 300.0; (* Safety clamping to nominal 300t capacity *)
END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 2.2: SUPERSONIC MULTI-HOLE LAVAL NOZZLE GAS DYNAMICS                 *)
(* Calculates Mach number, nozzle exit velocity, jet momentum, and dynamic   *)
(* penetration cavity depth Lp [mm] based on Koria-Lange formulation.       *)
(* ------------------------------------------------------------------------- *)
(* Header pressure absolute [Pa]: 1 bar = 100,000 Pa *)
rTmpVal := (rO2_Press_Voted + 1.013) / 1.013;
IF rTmpVal < 1.893 THEN
    (* Sub-critical unchoked flow *)
    rLavalMachNumber := 1.00;
ELSE
    (* Isentropic supersonic expansion: gamma = 1.40 for pure O2 *)
    (* M = SQRT( (2 / (gamma - 1)) * [ (P0 / P)^((gamma-1)/gamma) - 1 ] ) *)
    rLavalMachNumber := SQRT(5.0 * (EXPT(rTmpVal, 0.285714) - 1.0));
    IF rLavalMachNumber > 2.45 THEN rLavalMachNumber := 2.45; END_IF;
    IF rLavalMachNumber < 1.20 THEN rLavalMachNumber := 1.20; END_IF;
END_IF;

(* Supersonic gas exit velocity v_exit = M * SQRT(gamma * R_spec * T_exit) *)
(* For O2: R_spec = 259.8 J/kg-K. T_exit ~ 185 K under Mach 2.2 expansion *)
rLavalExitVelocity_ms := rLavalMachNumber * SQRT(1.40 * 259.8 * (rO2_HeaderTemperature_degC + 273.15) * 0.5079);

(* Koria-Lange Supersonic Jet Cavity Penetration Depth Lp [mm] *)
(* Throat diameter d_t = 38.5 mm, 6-hole nozzle, inclination theta = 12.0 deg *)
(* Liquid iron density rho_m = 6980 kg/m3 *)
IF rLanceHeightActual_Z_mm > 500.0 THEN
    rCavityPenetrationDepth_mm := 4.46e-3 * SQRT((rO2_Press_Voted * 1482.25) / (9.81 * 6.980)) *
                                  EXPT(rO2_FlowSetpoint_Nm3min / rLanceHeightActual_Z_mm, 0.667) *
                                  EXP(-0.0014 * 12.0) * 1000.0;
    (* Dynamic cavity diameter at bath surface *)
    rCavityDiameter_mm := 2.0 * rLanceHeightActual_Z_mm * TAN(0.2094) + 250.0; (* 12 deg half-angle expansion *)
ELSE
    rCavityPenetrationDepth_mm := 150.0;
    rCavityDiameter_mm := 500.0;
END_IF;

(* Clamp cavity depth to physical vessel bath depth ceiling (max 1400 mm) *)
IF rCavityPenetrationDepth_mm > 1200.0 THEN rCavityPenetrationDepth_mm := 1200.0; END_IF;
IF rCavityPenetrationDepth_mm < 50.0 THEN rCavityPenetrationDepth_mm := 50.0; END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 2.3: REAL-TIME OFFGAS MASS SPECTROMETRY & TOTAL FLOW CALCULATION     *)
(* Total evacuation flow via continuous Nitrogen mass balance across hood:   *)
(* Q_offgas * (%N2 / 100) = Q_bottom_N2 + Q_ingress_air * 0.7808            *)
(* ------------------------------------------------------------------------- *)
IF rOffgas_N2_Conc_pct > 1.50 THEN
    rTmpVal := (rBottomNitrogenFlowActual_Nm3min * 60.0) + (rAirIngressFlow_Nm3h * 0.7808);
    rOffgasTotalFlowCalc_Nm3h := (rTmpVal / (rOffgas_N2_Conc_pct / 100.0));
ELSE
    rOffgasTotalFlowCalc_Nm3h := rOffgasTotalFlowRaw_Nm3h;
END_IF;

(* Filtered offgas flow bounded to realistic duct capacities: 40,000 to 240,000 Nm3/h *)
IF rOffgasTotalFlowCalc_Nm3h < 40000.0 THEN rOffgasTotalFlowCalc_Nm3h := 40000.0; END_IF;
IF rOffgasTotalFlowCalc_Nm3h > 240000.0 THEN rOffgasTotalFlowCalc_Nm3h := 240000.0; END_IF;

(* Instantaneous Decarburization Rate dC/dt [%/min] derived from offgas CO + CO2 carbon flux: *)
(* Molar carbon: 12.011 g/mol, Molar volume standard: 22.414 Nm3/kmol *)
(* dC/dt = (12.011 / 22.414) * (Q_offgas / 60.0) * ((%CO + %CO2)/100.0) / (W_steel * 1000.0) * 100.0 *)
rInstantaneousDecarbRate_pctmin := (12.011 / 22.414) * (rOffgasTotalFlowCalc_Nm3h / 60.0) *
                                  ((rOffgas_CO_Voted + rOffgas_CO2_Conc_pct) / 100.0) /
                                  (rTotalSteelMass_t * 10.0);
IF rInstantaneousDecarbRate_pctmin < 0.0 THEN rInstantaneousDecarbRate_pctmin := 0.0; END_IF;
IF rInstantaneousDecarbRate_pctmin > 0.45 THEN rInstantaneousDecarbRate_pctmin := 0.45; END_IF;
rCalculatedDecarbRate_pctmin := rInstantaneousDecarbRate_pctmin;

(* Post-Combustion Ratio PCR [%] in converter mouth and waste heat boiler hood *)
IF (rOffgas_CO_Voted + rOffgas_CO2_Conc_pct) > 1.0 THEN
    rPostCombustionRatio_calc := (rOffgas_CO2_Conc_pct / (rOffgas_CO_Voted + rOffgas_CO2_Conc_pct)) * 100.0;
ELSE
    rPostCombustionRatio_calc := 0.0;
END_IF;
rPostCombustionRatio_pct := rPostCombustionRatio_calc;

(* Calorific Lower Heating Value (LHV) of offgas: CO = 12.636 MJ/Nm3, H2 = 10.788 MJ/Nm3 *)
rGasCalorificValue_MJNm3 := (rOffgas_CO_Voted * 0.12636) + (rOffgas_H2_Conc_pct * 0.10788);

(* ------------------------------------------------------------------------- *)
(* STEP 2.4: SLAG-METAL REACTION EQUILIBRIUM & CHEMICAL KINETICS             *)
(* Basicities B2, B3, dephosphorization partition LP, dynamic FeO formation *)
(* ------------------------------------------------------------------------- *)
(* Slag Binary Basicity B2 = %CaO / %SiO2 *)
IF rDynamicSlagSiO2_pct > 0.5 THEN
    rSlagBasicity_B2 := rDynamicSlagCaO_pct / rDynamicSlagSiO2_pct;
ELSE
    rSlagBasicity_B2 := 3.50;
END_IF;

(* Slag Ternary Basicity B3 = %CaO / (%SiO2 + 2.5) *)
rSlagBasicity_B3 := rDynamicSlagCaO_pct / (rDynamicSlagSiO2_pct + 2.5);

(* Healy Dephosphorization Partition LP = (%P) / [%P] *)
(* log10(LP) = 22,350 / T_bath - 16.0 + 0.08 * %CaO + 2.5 * log10(%FeO) *)
rTmpVal := (22350.0 / (x_est[1] + 273.15)) - 16.0 + (0.08 * rDynamicSlagCaO_pct) + (2.5 * (LN(MAX(2.0, x_est[3])) / 2.302585));
IF rTmpVal > 4.5 THEN rTmpVal := 4.5; END_IF;
IF rTmpVal < 0.5 THEN rTmpVal := 0.5; END_IF;
rDephosphorizationPartition_Lp := EXPT(10.0, rTmpVal);

(* Dynamic Oxygen Accumulation in Slag (determining FeO concentration) *)
(* O2 supplied - O2 consumed in decarb - O2 consumed in Si/Mn/P oxidation *)
rTmpVal := (rO2_FlowSetpoint_Nm3min / 60.0 * 1.429) - (* kg O2/s supplied *)
           (rInstantaneousDecarbRate_pctmin / 60.0 * (rTotalSteelMass_t * 1000.0) / 100.0 * (16.0 / 12.011) * (1.0 + rPostCombustionRatio_calc / 100.0));
rDynamicOxygenAccumulation_kg := rDynamicOxygenAccumulation_kg + (rTmpVal * rCycleTime_dt_s);
IF rDynamicOxygenAccumulation_kg < 0.0 THEN rDynamicOxygenAccumulation_kg := 0.0; END_IF;

(* Approximate Slag FeO from accumulated oxygen mass *)
IF rDynamicSlagMass_t > 5.0 THEN
    rDynamicSlagFeO_pct := (rDynamicOxygenAccumulation_kg * (71.844 / 16.0) / (rDynamicSlagMass_t * 1000.0)) * 100.0 + 5.0;
ELSE
    rDynamicSlagFeO_pct := 14.5;
END_IF;
IF rDynamicSlagFeO_pct < 6.0 THEN rDynamicSlagFeO_pct := 6.0; END_IF;
IF rDynamicSlagFeO_pct > 38.0 THEN rDynamicSlagFeO_pct := 38.0; END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 2.5: ACOUSTIC SLOPPING SURVEILLANCE & ATTENUATION INDEX              *)
(* Drop in high-frequency acoustic noise indicates muffling by foam layer.   *)
(* ------------------------------------------------------------------------- *)
rAcousticAttenuation_dB := MAX(0.0, rAcousticBaselineQuiet_dB - rTrunnionAcoustic_Voted);
rAcousticFoamIndex_dB := rTrunnionAcoustic_Voted;

(* Slopping Severity Score [0.0..10.0]: Combined Acoustic & Hood Draft Fluctuations *)
rTmpVal := (rAcousticAttenuation_dB / 25.0) * 6.0 + (MAX(0.0, rHoodDraftPressure_Pa + 100.0) / 100.0) * 4.0;
IF rTmpVal > 10.0 THEN rTmpVal := 10.0; END_IF;
IF rTmpVal < 0.0 THEN rTmpVal := 0.0; END_IF;
rSloppingSeverityIndex := rTmpVal;

(* Slopping Alarm Bit & Automatic Anti-Slopping Flag *)
IF (rSloppingSeverityIndex >= 6.5) OR (rAcousticAttenuation_dB > 18.0) THEN
    bAlarm_SloppingSevere := TRUE;
    bAntiSloppingActive := TRUE;
    rAntiSloppingCooldownTimer_s := 15.0; (* Persist suppression for 15s *)
ELSE
    IF rAntiSloppingCooldownTimer_s > 0.0 THEN
        rAntiSloppingCooldownTimer_s := rAntiSloppingCooldownTimer_s - rCycleTime_dt_s;
        bAntiSloppingActive := TRUE;
    ELSE
        bAlarm_SloppingSevere := FALSE;
        bAntiSloppingActive := FALSE;
    END_IF;
END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 2.6: BOTTOM-STIRRING INERT GAS THERMO-HYDRAULIC ENERGY DISSIPATION   *)
(* Specific stirring power epsilon_dot [W/t] (Sundberg / Nakanishi)          *)
(* ------------------------------------------------------------------------- *)
rTmpVal := rBottomArgonFlowActual_Nm3min + rBottomNitrogenFlowActual_Nm3min;
IF rTmpVal > 0.1 THEN
    (* Bath height H_bath ~ 1.55 m, ferrostatic pressure term *)
    rStirringEnergyDensity_Wt := 28.5 * (rTmpVal / rTotalSteelMass_t) * (x_est[1] + 273.15) *
                                 (LN(1.0 + (6980.0 * 9.81 * 1.55 / 101325.0)) + (1.0 - 298.15 / (x_est[1] + 273.15)));
ELSE
    rStirringEnergyDensity_Wt := 0.0;
END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 2.7: DYNAMIC SUBLANCE IN-BLOW LIQUIDUS ARREST CALCULATION             *)
(* TSC probe liquidus arrest temperature T_liq directly converts to %C.     *)
(* Fe-C Phase Diagram: %C = 4.30 - 0.00762 * (1538 - T_liq)                 *)
(* ------------------------------------------------------------------------- *)
IF bSublanceBathContact_Sig AND (rSublanceLiquidusTemp_degC > 1400.0) AND (rSublanceLiquidusTemp_degC < 1538.0) THEN
    rSublanceLiquidusCalculatedC_pct := 4.30 - (0.00762 * (1538.0 - rSublanceLiquidusTemp_degC)) -
                                        (0.0000045 * EXPT(1538.0 - rSublanceLiquidusTemp_degC, 2.0));
    IF rSublanceLiquidusCalculatedC_pct < 0.02 THEN rSublanceLiquidusCalculatedC_pct := 0.02; END_IF;
    IF rSublanceLiquidusCalculatedC_pct > 1.80 THEN rSublanceLiquidusCalculatedC_pct := 1.80; END_IF;
    bSublanceSampleValid := TRUE;
    rSublanceLatchedCarbon_pct := rSublanceLiquidusCalculatedC_pct;
    rSublanceLatchedTemp_degC := rSublanceBathTemp_degC;
    rSublanceLatchedOxygen_ppm := rSublanceOxygenActivity_ppm;
    bSublanceAcquisitionSuccessful := TRUE;
END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 2.8: SYNTHESIZE MEASUREMENT VECTOR y_meas[6]                         *)
(* ------------------------------------------------------------------------- *)
IF bSublanceAcquisitionSuccessful AND (rSublanceLatchedCarbon_pct > 0.01) THEN
    y_meas[0] := rSublanceLatchedCarbon_pct; (* High-precision sublance ground truth *)
ELSE
    (* Estimate from integrated decarb rate *)
    y_meas[0] := MAX(0.03, x_est[0] - (rCalculatedDecarbRate_pctmin * (rCycleTime_dt_s / 60.0)));
END_IF;

IF bSublanceAcquisitionSuccessful AND (rSublanceLatchedTemp_degC > 1450.0) THEN
    y_meas[1] := rSublanceLatchedTemp_degC;
ELSE
    y_meas[1] := x_est[1];
END_IF;

y_meas[2] := rCalculatedDecarbRate_pctmin;
y_meas[3] := rDynamicSlagFeO_pct;
y_meas[4] := rAcousticFoamIndex_dB;
y_meas[5] := rHoodDraftPressure_Pa;

(* ------------------------------------------------------------------------- *)
(* STEP 2.9: DISCRETE STATE PROPAGATION & KALMAN OBSERVER INNOVATION UPDATE  *)
(* x_pred = A * x_est + B * u_prev                                          *)
(* y_est  = C * x_pred + D * u_prev                                          *)
(* innov  = y_meas - y_est                                                  *)
(* x_est  = x_pred + L_obs * innov                                          *)
(* ------------------------------------------------------------------------- *)
(* Matrix Multiplication: x_pred = A * x_est + B * u_prev *)
FOR iIdx := 0 TO 5 DO
    rTmpSum := 0.0;
    FOR jIdx := 0 TO 5 DO
        rTmpSum := rTmpSum + (A_mat[iIdx, jIdx] * x_est[jIdx]);
    END_FOR;
    FOR kIdx := 0 TO 4 DO
        rTmpSum := rTmpSum + (B_mat[iIdx, kIdx] * u_prev[kIdx]);
    END_FOR;
    x_pred[iIdx] := rTmpSum;
END_FOR;

(* Matrix Multiplication: y_est = C * x_pred *)
FOR iIdx := 0 TO 5 DO
    rTmpSum := 0.0;
    FOR jIdx := 0 TO 5 DO
        rTmpSum := rTmpSum + (C_mat[iIdx, jIdx] * x_pred[jIdx]);
    END_FOR;
    y_est[iIdx] := rTmpSum;
    innov[iIdx] := y_meas[iIdx] - y_est[iIdx];
END_FOR;

(* Observer State Correction: x_est = x_pred + L_obs * innov *)
FOR iIdx := 0 TO 5 DO
    rTmpSum := 0.0;
    FOR jIdx := 0 TO 5 DO
        rTmpSum := rTmpSum + (L_obs[iIdx, jIdx] * innov[jIdx]);
    END_FOR;
    x_est[iIdx] := x_pred[iIdx] + rTmpSum;
END_FOR;

(* Physical Sanity Clamping on Estimated State Vector *)
IF x_est[0] < 0.020 THEN x_est[0] := 0.020; END_IF;   (* Bath Carbon min 0.02% *)
IF x_est[0] > 5.000 THEN x_est[0] := 5.000; END_IF;   (* Bath Carbon max 5.0% *)
IF x_est[1] < 1200.0 THEN x_est[1] := 1200.0; END_IF; (* Bath Temp min 1200 deg C *)
IF x_est[1] > 1750.0 THEN x_est[1] := 1750.0; END_IF; (* Bath Temp max 1750 deg C *)
IF x_est[2] < 0.000 THEN x_est[2] := 0.000; END_IF;   (* Decarb rate min 0.0 %/min *)
IF x_est[2] > 0.450 THEN x_est[2] := 0.450; END_IF;   (* Decarb rate max 0.45 %/min *)
IF x_est[3] < 5.00 THEN x_est[3] := 5.00; END_IF;     (* Slag FeO min 5% *)
IF x_est[3] > 45.00 THEN x_est[3] := 45.00; END_IF;   (* Slag FeO max 45% *)
IF x_est[4] < 30.00 THEN x_est[4] := 30.00; END_IF;   (* Acoustic index min 30 dB *)
IF x_est[4] > 125.00 THEN x_est[4] := 125.00; END_IF; (* Acoustic index max 125 dB *)
IF x_est[5] < -600.0 THEN x_est[5] := -600.0; END_IF; (* Hood draft min -600 Pa *)
IF x_est[5] > 200.0 THEN x_est[5] := 200.0; END_IF;   (* Hood draft max +200 Pa *)

(* Map to Output Variables *)
rEstimatedBathCarbon_pct := x_est[0];
rEstimatedBathTemp_degC := x_est[1];
rEstimatedSlagFeO_pct := x_est[3];

(* ========================================================================= *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) ENGINE           *)
(* ========================================================================= *)
(* Unrolled 10-iteration Projected Gradient Descent (PGD) over Horizon N = 5  *)
(* Evaluates adjoint costate backpropagation: lambda_k = 2*Q*e_x + A^T*lambda *)
(* Optimizes 5 control inputs: Lance winch v_lance, O2 flow Q_O2, Flux gate,  *)
(* Bottom stirring Q_bottom, and Offgas hood damper position.                 *)

(* ------------------------------------------------------------------------- *)
(* STEP 3.1: DYNAMIC REFERENCE TARGET TRAJECTORY UPDATE                      *)
(* Dynamic targets evolve based on current blowing stage and heat recipe.    *)
(* ------------------------------------------------------------------------- *)
x_ref[0] := rTargetTapCarbon_pct;       (* Target endpoint carbon wt% C *)
x_ref[1] := rTargetTapTemperature_degC;  (* Target endpoint liquid steel temp *)

(* Context-dependent reference decarburization rate *)
IF x_est[0] > 0.60 THEN
    x_ref[2] := 0.320; (* High carbon regime: Max sustained decarb rate *)
ELSIF x_est[0] > 0.20 THEN
    x_ref[2] := 0.200; (* Medium carbon transition *)
ELSE
    x_ref[2] := 0.045; (* Low carbon regime: Decelerate decarb to prevent Fe oxidation *)
END_IF;

(* Context-dependent reference slag FeO *)
IF iFsmState = cSTATE_SLAG_SPLASHING_COAT THEN
    x_ref[3] := 13.0; (* Lower FeO required for viscous refractory coating *)
ELSE
    x_ref[3] := 17.5; (* Standard dephosphorization slag FeO *)
END_IF;

x_ref[4] := 78.0;   (* Target trunnion acoustic transmission index [dB] *)
x_ref[5] := -150.0; (* Target waste heat hood draft differential pressure [Pa] *)

(* Control input nominal operating targets u_ref *)
u_ref[0] := 0.0;     (* Winch target velocity 0 mm/s (hold elevation) *)
IF (iFsmState = cSTATE_MAIN_DECARB_DEEP_BLOW) OR (iFsmState = cSTATE_SLAG_FOAM_SLOP_SUPPRESS) THEN
    u_ref[1] := 920.0; (* 920 Nm3/min supersonic main blow *)
ELSIF iFsmState = cSTATE_ENDPOINT_FINE_TRIM_BLOW THEN
    u_ref[1] := 720.0; (* Reduced flow fine trim blow *)
ELSIF iFsmState = cSTATE_LANCE_IGNITION_SOFT_BLOW THEN
    u_ref[1] := 600.0; (* Soft blow ignition flow *)
ELSE
    u_ref[1] := 200.0;
END_IF;

u_ref[2] := 0.0;     (* Nominal flux feeder gate closed *)
u_ref[3] := 18.0;    (* Nominal bottom stirring flow [Nm3/min] *)
u_ref[4] := 45.0;    (* Nominal primary draft damper 45% *)

(* ------------------------------------------------------------------------- *)
(* STEP 3.2: 10-ITERATION UNROLLED PROJECTED GRADIENT DESCENT OPTIMIZATION   *)
(* ------------------------------------------------------------------------- *)
FOR pIdx := 1 TO 10 DO
    (* Sub-step 3.2.1: Forward State Rollout Over Horizon N = 5 *)
    (* Initialize root state x_traj[0, :] with current estimated state *)
    FOR iIdx := 0 TO 5 DO
        x_traj[0, iIdx] := x_est[iIdx];
    END_FOR;

    (* Forward state rollout: x_traj[k+1] = A * x_traj[k] + B * u_traj[k] *)
    FOR kIdx := 0 TO 4 DO
        FOR iIdx := 0 TO 5 DO
            rTmpSum := 0.0;
            FOR jIdx := 0 TO 5 DO
                rTmpSum := rTmpSum + (A_mat[iIdx, jIdx] * x_traj[kIdx, jIdx]);
            END_FOR;
            FOR mIdx := 0 TO 4 DO
                rTmpSum := rTmpSum + (B_mat[iIdx, mIdx] * u_traj[kIdx, mIdx]);
            END_FOR;
            x_traj[kIdx + 1, iIdx] := rTmpSum;
        END_FOR;
    END_FOR;

    (* Sub-step 3.2.2: Adjoint Costate Backpropagation & Gradient Calculation *)
    (* Costate lambda at terminal horizon step 5: lambda_5 = 2 * P * (x_5 - x_ref) *)
    (* Note: Using scalar buffers to avoid dynamic allocation *)
    (* We compute gradients grad_u[k, m] = dJ/du[k, m] across k = 4 DOWNTO 0 *)

    (* Horizon Step k = 4 *)
    FOR mIdx := 0 TO 4 DO
        (* Tracking penalty gradient: 2 * R[m] * (u[4, m] - u_ref[m]) *)
        rGradVal := 2.0 * R_diag[mIdx] * (u_traj[4, mIdx] - u_ref[mIdx]);
        (* Slew penalty gradient: 2 * R_delta[m] * (u[4, m] - u[3, m]) *)
        rGradVal := rGradVal + 2.0 * R_delta_diag[mIdx] * (u_traj[4, mIdx] - u_traj[3, mIdx]);
        (* Terminal state sensitivity: SUM_i B[i, m] * 2 * P[i] * (x[5, i] - x_ref[i]) *)
        FOR iIdx := 0 TO 5 DO
            rGradVal := rGradVal + (B_mat[iIdx, mIdx] * 2.0 * P_diag[iIdx] * (x_traj[5, iIdx] - x_ref[iIdx]));
        END_FOR;
        grad_u[4, mIdx] := rGradVal;
    END_FOR;

    (* Horizon Step k = 3 *)
    FOR mIdx := 0 TO 4 DO
        rGradVal := 2.0 * R_diag[mIdx] * (u_traj[3, mIdx] - u_ref[mIdx]);
        rGradVal := rGradVal + 2.0 * R_delta_diag[mIdx] * (u_traj[3, mIdx] - u_traj[2, mIdx]);
        rGradVal := rGradVal - 2.0 * R_delta_diag[mIdx] * (u_traj[4, mIdx] - u_traj[3, mIdx]);
        FOR iIdx := 0 TO 5 DO
            rTmpVal := 2.0 * Q_diag[iIdx] * (x_traj[4, iIdx] - x_ref[iIdx]);
            FOR jIdx := 0 TO 5 DO
                rTmpVal := rTmpVal + (A_mat[jIdx, iIdx] * 2.0 * P_diag[jIdx] * (x_traj[5, jIdx] - x_ref[jIdx]));
            END_FOR;
            rGradVal := rGradVal + (B_mat[iIdx, mIdx] * rTmpVal);
        END_FOR;
        grad_u[3, mIdx] := rGradVal;
    END_FOR;

    (* Horizon Step k = 2 *)
    FOR mIdx := 0 TO 4 DO
        rGradVal := 2.0 * R_diag[mIdx] * (u_traj[2, mIdx] - u_ref[mIdx]);
        rGradVal := rGradVal + 2.0 * R_delta_diag[mIdx] * (u_traj[2, mIdx] - u_traj[1, mIdx]);
        rGradVal := rGradVal - 2.0 * R_delta_diag[mIdx] * (u_traj[3, mIdx] - u_traj[2, mIdx]);
        FOR iIdx := 0 TO 5 DO
            rTmpVal := 2.0 * Q_diag[iIdx] * (x_traj[3, iIdx] - x_ref[iIdx]);
            FOR jIdx := 0 TO 5 DO
                rTmpVal := rTmpVal + (A_mat[jIdx, iIdx] * 2.0 * Q_diag[jIdx] * (x_traj[4, jIdx] - x_ref[jIdx]));
            END_FOR;
            rGradVal := rGradVal + (B_mat[iIdx, mIdx] * rTmpVal);
        END_FOR;
        grad_u[2, mIdx] := rGradVal;
    END_FOR;

    (* Horizon Step k = 1 *)
    FOR mIdx := 0 TO 4 DO
        rGradVal := 2.0 * R_diag[mIdx] * (u_traj[1, mIdx] - u_ref[mIdx]);
        rGradVal := rGradVal + 2.0 * R_delta_diag[mIdx] * (u_traj[1, mIdx] - u_traj[0, mIdx]);
        rGradVal := rGradVal - 2.0 * R_delta_diag[mIdx] * (u_traj[2, mIdx] - u_traj[1, mIdx]);
        FOR iIdx := 0 TO 5 DO
            rTmpVal := 2.0 * Q_diag[iIdx] * (x_traj[2, iIdx] - x_ref[iIdx]);
            FOR jIdx := 0 TO 5 DO
                rTmpVal := rTmpVal + (A_mat[jIdx, iIdx] * 2.0 * Q_diag[jIdx] * (x_traj[3, jIdx] - x_ref[jIdx]));
            END_FOR;
            rGradVal := rGradVal + (B_mat[iIdx, mIdx] * rTmpVal);
        END_FOR;
        grad_u[1, mIdx] := rGradVal;
    END_FOR;

    (* Horizon Step k = 0 (Immediate Action Step) *)
    FOR mIdx := 0 TO 4 DO
        rGradVal := 2.0 * R_diag[mIdx] * (u_traj[0, mIdx] - u_ref[mIdx]);
        rGradVal := rGradVal + 2.0 * R_delta_diag[mIdx] * (u_traj[0, mIdx] - u_prev[mIdx]);
        rGradVal := rGradVal - 2.0 * R_delta_diag[mIdx] * (u_traj[1, mIdx] - u_traj[0, mIdx]);
        FOR iIdx := 0 TO 5 DO
            rTmpVal := 2.0 * Q_diag[iIdx] * (x_traj[1, iIdx] - x_ref[iIdx]);
            FOR jIdx := 0 TO 5 DO
                rTmpVal := rTmpVal + (A_mat[jIdx, iIdx] * 2.0 * Q_diag[jIdx] * (x_traj[2, jIdx] - x_ref[jIdx]));
            END_FOR;
            rGradVal := rGradVal + (B_mat[iIdx, mIdx] * rTmpVal);
        END_FOR;
        grad_u[0, mIdx] := rGradVal;
    END_FOR;

    (* Sub-step 3.2.3: Projected Gradient Descent Step & Box Constraint Clamping *)
    FOR kIdx := 0 TO 4 DO
        FOR mIdx := 0 TO 4 DO
            (* PGD update: u = u - alpha * grad *)
            u_traj[kIdx, mIdx] := u_traj[kIdx, mIdx] - (rMpcStepSize_alpha * grad_u[kIdx, mIdx]);
            (* Box constraints clamping [u_min, u_max] *)
            IF u_traj[kIdx, mIdx] < u_min[mIdx] THEN
                u_traj[kIdx, mIdx] := u_min[mIdx];
            ELSIF u_traj[kIdx, mIdx] > u_max[mIdx] THEN
                u_traj[kIdx, mIdx] := u_max[mIdx];
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* ------------------------------------------------------------------------- *)
(* STEP 3.3: EXTRACT RECEDING HORIZON OPTIMAL CONTROL u_opt = u_traj[0]      *)
(* Apply slew rate clamping relative to previous scan cycle u_prev           *)
(* ------------------------------------------------------------------------- *)
FOR mIdx := 0 TO 4 DO
    rTmpVal := u_traj[0, mIdx];
    rTmpSum := delta_u_max[mIdx] * (rCycleTime_dt_s / 0.050);
    IF ABS(rTmpVal - u_prev[mIdx]) > rTmpSum THEN
        IF rTmpVal > u_prev[mIdx] THEN
            u_opt[mIdx] := u_prev[mIdx] + rTmpSum;
        ELSE
            u_opt[mIdx] := u_prev[mIdx] - rTmpSum;
        END_IF;
    ELSE
        u_opt[mIdx] := rTmpVal;
    END_IF;
    u_curr[mIdx] := u_opt[mIdx];
    u_prev[mIdx] := u_curr[mIdx];
END_FOR;

(* ------------------------------------------------------------------------- *)
(* STEP 3.4: PHYSICAL ACTUATOR COMMAND MAPPING & OVERRIDES                   *)
(* ------------------------------------------------------------------------- *)
(* u_opt[0]: Lance Winch Velocity Command [mm/s] *)
rLanceWinchSpeedCmd_mms := u_opt[0];
IF rLanceWinchSpeedCmd_mms > 2.0 THEN
    iLanceWinchDirectionCmd := 1;  (* Lower lance *)
ELSIF rLanceWinchSpeedCmd_mms < -2.0 THEN
    iLanceWinchDirectionCmd := -1; (* Raise lance *)
ELSE
    iLanceWinchDirectionCmd := 0;  (* Hold position *)
END_IF;

(* u_opt[1]: Supersonic Oxygen Flow Rate Setpoint [Nm3/min] *)
rO2_FlowSetpoint_Nm3min := u_opt[1];
(* Percentage control valve command: 0 to 1100 Nm3/min mapped to 0..100% *)
rO2_MainFlowControlValve_pct := (rO2_FlowSetpoint_Nm3min / 1100.0) * 100.0;
IF rO2_MainFlowControlValve_pct < 0.0 THEN rO2_MainFlowControlValve_pct := 0.0; END_IF;
IF rO2_MainFlowControlValve_pct > 100.0 THEN rO2_MainFlowControlValve_pct := 100.0; END_IF;

(* u_opt[2]: Flux Vibratory Feeder Drive Commands [%] *)
IF iFsmState = cSTATE_SILICON_OXIDATION_FLUX THEN
    rLimeVibratoryFeederCmd_pct := u_opt[2] * 0.70;
    rDoloVibratoryFeederCmd_pct := u_opt[2] * 0.30;
ELSIF bAntiSloppingActive THEN
    rLimeVibratoryFeederCmd_pct := 15.0; (* Small lime addition to suppress foam *)
    rDoloVibratoryFeederCmd_pct := 0.0;
ELSE
    rLimeVibratoryFeederCmd_pct := 0.0;
    rDoloVibratoryFeederCmd_pct := 0.0;
END_IF;

(* u_opt[3]: Bottom Inert Gas Stirring Flow Command [Nm3/min] *)
rBottomGasFlowCmd_Nm3min := u_opt[3];
IF bAntiSloppingActive THEN
    (* Boost bottom gas to 28 Nm3/min to break surface foam bubbles *)
    rBottomGasFlowCmd_Nm3min := MAX(rBottomGasFlowCmd_Nm3min, 28.0);
END_IF;

(* Gas Type Selection Logic: Nitrogen early, Argon late *)
IF (x_est[0] < 0.40) OR (iFsmState >= cSTATE_SUBLANCE_IMMERSION_DIP) THEN
    iBottomGasTypeSelected := 2; (* Argon: Prevent Nitrogen pickup in clean steel *)
ELSE
    iBottomGasTypeSelected := 1; (* Nitrogen: Cost-effective stirring *)
END_IF;

(* u_opt[4]: Primary Waste Heat Boiler Draft Damper [%] *)
rPrimaryOffgasDamperCmd_pct := u_opt[4];
IF rPrimaryOffgasDamperCmd_pct < 10.0 THEN rPrimaryOffgasDamperCmd_pct := 10.0; END_IF;
IF rPrimaryOffgasDamperCmd_pct > 100.0 THEN rPrimaryOffgasDamperCmd_pct := 100.0; END_IF;

(* ========================================================================= *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)     *)
(* ========================================================================= *)
(* Complete sequence management from charging, ignition, silicon oxidation,   *)
(* supersonic deep blow, acoustic anti-slopping, sublance in-blow dip,       *)
(* endpoint trim, bottom rinse, tapping, slag splashing to emergency trip.  *)

(* Update state execution timer and edge detection *)
IF iFsmState <> iFsmPrevState THEN
    rFsmStateTimer_s := 0.0;
    bFsmStateFirstScan := TRUE;
    iFsmPrevState := iFsmState;
ELSE
    rFsmStateTimer_s := rFsmStateTimer_s + rCycleTime_dt_s;
    bFsmStateFirstScan := FALSE;
END_IF;
rStateElapsedTime_s := rFsmStateTimer_s;
iCurrentFsmState := iFsmState;

(* Global Interlock Guard: Catastrophic Lance Water Leak or Emergency Stop *)
IF bEmergencyTripCmd OR bAlarm_LanceWaterLeakTrip OR (rLanceDeltaT_Voted >= rLanceDeltaT_HH_degC) THEN
    IF iFsmState <> cSTATE_EMERGENCY_LEAK_TRIP THEN
        iFsmState := cSTATE_EMERGENCY_LEAK_TRIP;
    END_IF;
END_IF;

CASE iFsmState OF

    (* --------------------------------------------------------------------- *)
    (* STATE 0: STATE_IDLE                                                   *)
    (* --------------------------------------------------------------------- *)
    0: (* cSTATE_IDLE *)
        (* Actuator Safe Parking *)
        bO2_MainEmergencyShutoffValve := FALSE;
        rO2_MainFlowControlValve_pct := 0.0;
        rO2_FlowSetpoint_Nm3min := 0.0;
        rLanceTargetElevation_mm := 5000.0; (* Upper parking position *)
        rLanceWinchSpeedCmd_mms := 0.0;
        iLanceWinchDirectionCmd := 0;
        bLanceNitrogenPurgeValve := FALSE;
        rLimeVibratoryFeederCmd_pct := 0.0;
        rDoloVibratoryFeederCmd_pct := 0.0;
        rIronOreVibratoryFeederCmd_pct := 0.0;
        bFluxBatchDischargeGateOpen := FALSE;
        rSkirtElevationCmd_mm := 1200.0; (* Skirt fully raised *)
        bNitrogenSealingCurtainCmd := FALSE;
        bGasRecoveryThreeWayValveCmd := FALSE; (* Flare stack *)
        rPrimaryOffgasDamperCmd_pct := 15.0;   (* Minimal purge draft *)
        iBottomGasTypeSelected := 1;          (* Standby Nitrogen *)
        rBottomGasFlowCmd_Nm3min := 3.0;      (* Standby plug cooling flow *)
        bSublanceCycleInProgress := FALSE;
        bHeatCompleteReadyToTap := FALSE;

        (* Reset heat accumulation registers on state entry *)
        IF bFsmStateFirstScan THEN
            rHeatTotalOxygenConsumed_Nm3 := 0.0;
            rHeatTotalBlowTime_s := 0.0;
            bSublanceTriggerDone := FALSE;
            bSublanceAcquisitionSuccessful := FALSE;
            rDynamicOxygenAccumulation_kg := 0.0;
            bTappingSlagDartDropped := FALSE;
        END_IF;

        (* Transition: Auto sequence started and crane clearance confirmed *)
        IF bAutoSequenceStartCmd AND NOT bSequenceHoldCmd THEN
            iFsmState := cSTATE_SCRAP_HOTMETAL_CHARGE; (* Proceed to State 1 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 1: STATE_SCRAP_AND_HOT_METAL_CHARGING_TILT                      *)
    (* --------------------------------------------------------------------- *)
    1: (* cSTATE_SCRAP_HOTMETAL_CHARGE *)
        (* Vessel tilts towards charging floor (-55 deg for scrap, -45 for hot metal) *)
        bO2_MainEmergencyShutoffValve := FALSE;
        rO2_FlowSetpoint_Nm3min := 0.0;
        rLanceTargetElevation_mm := 5000.0; (* Lance safely locked high in tower *)
        rSkirtElevationCmd_mm := 1200.0;    (* Skirt raised *)
        bNitrogenSealingCurtainCmd := FALSE;
        rPrimaryOffgasDamperCmd_pct := 25.0;(* Moderate secondary charging hood evacuation *)
        iBottomGasTypeSelected := 1;        (* Nitrogen *)
        rBottomGasFlowCmd_Nm3min := 4.5;    (* Nitrogen flow to prevent tuyere clogging *)

        (* Charging Completion Verification *)
        (* Hot metal weight must exceed 180t, scrap weight must exceed 40t *)
        IF (rHotMetalChargeWeight_t >= 180.0) AND (rScrapChargeWeight_t >= 40.0) AND (rFsmStateTimer_s >= 25.0) THEN
            (* Operator / automation rotates vessel back to vertical *)
            IF ABS(rVesselTiltAngle_deg) <= 1.0 THEN
                iFsmState := cSTATE_VERTICAL_LOCK_HOOD_DOWN; (* Proceed to State 2 *)
            END_IF;
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 2: STATE_CONVERTER_VERTICAL_LOCK_AND_HOOD_LOWER                 *)
    (* --------------------------------------------------------------------- *)
    2: (* cSTATE_VERTICAL_LOCK_HOOD_DOWN *)
        (* Mechanical pin locks engage, movable skirt lowers over mouth *)
        rSkirtElevationCmd_mm := 0.0; (* Full seal position *)
        bNitrogenSealingCurtainCmd := TRUE; (* Activate N2 skirt curtain purge *)
        rPrimaryOffgasDamperCmd_pct := 40.0; (* ID fan pull establish negative draft *)
        iBottomGasTypeSelected := 1; (* Nitrogen bottom stirring *)
        rBottomGasFlowCmd_Nm3min := 8.0;

        (* Transition Interlocks: Vessel locked vertical, skirt seated, draft negative *)
        IF bVesselVerticalLock_Z AND bSkirtFullyLowered_LS AND (rHoodDraftPressure_Pa < -25.0) AND (rFsmStateTimer_s >= 6.0) THEN
            iFsmState := cSTATE_LANCE_IGNITION_SOFT_BLOW; (* Proceed to State 3 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 3: STATE_OXYGEN_LANCE_IGNITION_SOFT_BLOW_HIGH_LANCE             *)
    (* --------------------------------------------------------------------- *)
    3: (* cSTATE_LANCE_IGNITION_SOFT_BLOW *)
        (* Soft blowing at high lance elevation (3200 mm) to ignite hot metal *)
        rLanceTargetElevation_mm := 3200.0;
        rO2_FlowSetpoint_Nm3min := 650.0; (* Ignition flow *)
        bO2_MainEmergencyShutoffValve := TRUE;
        bNitrogenSealingCurtainCmd := TRUE;
        iBottomGasTypeSelected := 1;
        rBottomGasFlowCmd_Nm3min := 10.0;
        rPrimaryOffgasDamperCmd_pct := 55.0;
        bGasRecoveryThreeWayValveCmd := FALSE; (* Flare stack combustion *)

        (* Integrate oxygen volume & blow duration *)
        rHeatTotalOxygenConsumed_Nm3 := rHeatTotalOxygenConsumed_Nm3 + (rO2_FlowSetpoint_Nm3min * (rCycleTime_dt_s / 60.0));
        rHeatTotalBlowTime_s := rHeatTotalBlowTime_s + rCycleTime_dt_s;

        (* Ignition Confirmation: Offgas CO > 12% and bath temp rises, or 45s timer *)
        IF ((rOffgas_CO_Voted > 12.0) OR (rFsmStateTimer_s >= 45.0)) AND (rLanceHeightActual_Z_mm <= 3350.0) THEN
            iFsmState := cSTATE_SILICON_OXIDATION_FLUX; (* Proceed to State 4 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 4: STATE_SILICON_OXIDATION_AND_FLUX_ADDITION_RUN                *)
    (* --------------------------------------------------------------------- *)
    4: (* cSTATE_SILICON_OXIDATION_FLUX *)
        (* Lance descends to intermediate height (2400 mm), batch feed lime & dolo *)
        rLanceTargetElevation_mm := 2400.0;
        rO2_FlowSetpoint_Nm3min := 850.0;
        bO2_MainEmergencyShutoffValve := TRUE;
        bFluxBatchDischargeGateOpen := TRUE;
        rLimeVibratoryFeederCmd_pct := 65.0; (* Active calcined lime *)
        rDoloVibratoryFeederCmd_pct := 35.0; (* Light-burned dolomite *)
        iBottomGasTypeSelected := 1;         (* Nitrogen *)
        rBottomGasFlowCmd_Nm3min := 14.0;
        rPrimaryOffgasDamperCmd_pct := 65.0;

        rHeatTotalOxygenConsumed_Nm3 := rHeatTotalOxygenConsumed_Nm3 + (rO2_FlowSetpoint_Nm3min * (rCycleTime_dt_s / 60.0));
        rHeatTotalBlowTime_s := rHeatTotalBlowTime_s + rCycleTime_dt_s;

        (* Silicon oxidation typically finishes at ~180s when Si < 0.05% and slag basicity forms *)
        IF (rFsmStateTimer_s >= 160.0) OR (rHeatTotalOxygenConsumed_Nm3 >= 2800.0) THEN
            bFluxBatchDischargeGateOpen := FALSE;
            rLimeVibratoryFeederCmd_pct := 0.0;
            rDoloVibratoryFeederCmd_pct := 0.0;
            iFsmState := cSTATE_MAIN_DECARB_DEEP_BLOW; (* Proceed to State 5 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 5: STATE_MAIN_DECARBURIZATION_SUPERSONIC_DEEP_BLOW              *)
    (* --------------------------------------------------------------------- *)
    5: (* cSTATE_MAIN_DECARB_DEEP_BLOW *)
        (* Deep supersonic blowing: Lance at 1550 mm, 920 Nm3/min Mach 2.2 jet *)
        rLanceTargetElevation_mm := 1550.0;
        rO2_FlowSetpoint_Nm3min := 920.0;
        bO2_MainEmergencyShutoffValve := TRUE;
        rPrimaryOffgasDamperCmd_pct := 75.0;

        (* Switch to Argon bottom stirring when bath carbon drops below 0.45% *)
        IF x_est[0] <= 0.45 THEN
            iBottomGasTypeSelected := 2; (* Argon *)
            rBottomGasFlowCmd_Nm3min := 20.0;
        ELSE
            iBottomGasTypeSelected := 1; (* Nitrogen *)
            rBottomGasFlowCmd_Nm3min := 16.0;
        END_IF;

        rHeatTotalOxygenConsumed_Nm3 := rHeatTotalOxygenConsumed_Nm3 + (rO2_FlowSetpoint_Nm3min * (rCycleTime_dt_s / 60.0));
        rHeatTotalBlowTime_s := rHeatTotalBlowTime_s + rCycleTime_dt_s;

        (* Check for Slag Slopping Transition *)
        IF bAntiSloppingActive OR (rSloppingSeverityIndex >= 6.5) THEN
            iFsmState := cSTATE_SLAG_FOAM_SLOP_SUPPRESS; (* Divert to State 6 *)
        (* Transition to Sublance Immersion at ~82% planned blow volume *)
        ELSIF (rHeatTotalOxygenConsumed_Nm3 >= (rTotalPlannedO2Volume_Nm3 * 0.82)) AND NOT bSublanceTriggerDone THEN
            iFsmState := cSTATE_SUBLANCE_IMMERSION_DIP; (* Proceed to State 7 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 6: STATE_SLAG_FOAMING_CONTROL_AND_SLOPPING_SUPPRESSION          *)
    (* --------------------------------------------------------------------- *)
    6: (* cSTATE_SLAG_FOAM_SLOP_SUPPRESS *)
        (* Anti-slopping intervention: Elevate lance by 250 mm, throttle O2 by 18%, *)
        (* boost bottom stirring gas, feed small dolomite batch to break foam *)
        rLanceTargetElevation_mm := 1850.0; (* Temporary elevation *)
        rO2_FlowSetpoint_Nm3min := 750.0;   (* Throttled flow *)
        bO2_MainEmergencyShutoffValve := TRUE;
        rDoloVibratoryFeederCmd_pct := 20.0;(* Dolomitic flux foam suppression *)
        rBottomGasFlowCmd_Nm3min := 26.0;   (* Strong stirring to break bubbles *)
        rPrimaryOffgasDamperCmd_pct := 85.0;(* Open damper to mitigate pressure spike *)

        rHeatTotalOxygenConsumed_Nm3 := rHeatTotalOxygenConsumed_Nm3 + (rO2_FlowSetpoint_Nm3min * (rCycleTime_dt_s / 60.0));
        rHeatTotalBlowTime_s := rHeatTotalBlowTime_s + rCycleTime_dt_s;

        (* Return to Main Decarb once foam index recovers *)
        IF NOT bAntiSloppingActive AND (rAcousticAttenuation_dB < 10.0) AND (rFsmStateTimer_s >= 20.0) THEN
            rDoloVibratoryFeederCmd_pct := 0.0;
            iFsmState := cSTATE_MAIN_DECARB_DEEP_BLOW; (* Return to State 5 *)
        ELSIF (rHeatTotalOxygenConsumed_Nm3 >= (rTotalPlannedO2Volume_Nm3 * 0.82)) AND NOT bSublanceTriggerDone THEN
            rDoloVibratoryFeederCmd_pct := 0.0;
            iFsmState := cSTATE_SUBLANCE_IMMERSION_DIP; (* Proceed to State 7 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 7: STATE_DYNAMIC_SUBLANCE_IMMERSION_SAMPLE_ACQUIRE              *)
    (* --------------------------------------------------------------------- *)
    7: (* cSTATE_SUBLANCE_IMMERSION_DIP *)
        (* Dynamic in-blow sublance immersion: Drive sublance into bath while blowing *)
        bSublanceCycleInProgress := TRUE;
        rLanceTargetElevation_mm := 1600.0;
        rO2_FlowSetpoint_Nm3min := 820.0; (* Hold stable blowing during probe dip *)
        bO2_MainEmergencyShutoffValve := TRUE;
        iBottomGasTypeSelected := 2;     (* Argon *)
        rBottomGasFlowCmd_Nm3min := 18.0;

        rHeatTotalOxygenConsumed_Nm3 := rHeatTotalOxygenConsumed_Nm3 + (rO2_FlowSetpoint_Nm3min * (rCycleTime_dt_s / 60.0));
        rHeatTotalBlowTime_s := rHeatTotalBlowTime_s + rCycleTime_dt_s;

        (* Sublance drive motion sequence *)
        IF rFsmStateTimer_s < 4.0 THEN
            rSublanceWinchSpeedCmd_mms := 600.0; (* High speed entry *)
            iSublanceWinchDirectionCmd := 1;     (* Downward immersion *)
        ELSIF rFsmStateTimer_s < 8.5 THEN
            rSublanceWinchSpeedCmd_mms := 0.0;   (* Immersion dwell 4.5s for liquidus curve *)
            iSublanceWinchDirectionCmd := 0;
        ELSE
            rSublanceWinchSpeedCmd_mms := 800.0; (* Rapid hoist retract *)
            iSublanceWinchDirectionCmd := -1;
        END_IF;

        (* Sublance cycle complete after 14 seconds *)
        IF rFsmStateTimer_s >= 14.0 THEN
            bSublanceCycleInProgress := FALSE;
            bSublanceTriggerDone := TRUE;
            rSublanceWinchSpeedCmd_mms := 0.0;
            iSublanceWinchDirectionCmd := 0;
            (* Recalculate remaining oxygen blow volume based on sublance C and T *)
            rRemainingBlowO2Volume_Nm3 := MAX(350.0, (x_est[0] - rTargetTapCarbon_pct) * (rTotalSteelMass_t * 1000.0 / 100.0) * (22.414 / 12.011) * 0.95);
            iFsmState := cSTATE_ENDPOINT_FINE_TRIM_BLOW; (* Proceed to State 8 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 8: STATE_ENDPOINT_PREDICTION_FINE_O2_TRIM_BLOW                  *)
    (* --------------------------------------------------------------------- *)
    8: (* cSTATE_ENDPOINT_FINE_TRIM_BLOW *)
        (* Fine trim blow with reduced flow (720 Nm3/min) to land precisely at tap C & T *)
        rLanceTargetElevation_mm := 1500.0; (* Deep trim penetration *)
        rO2_FlowSetpoint_Nm3min := 720.0;
        bO2_MainEmergencyShutoffValve := TRUE;
        iBottomGasTypeSelected := 2; (* Argon *)
        rBottomGasFlowCmd_Nm3min := 22.0;
        rPrimaryOffgasDamperCmd_pct := 65.0;

        rHeatTotalOxygenConsumed_Nm3 := rHeatTotalOxygenConsumed_Nm3 + (rO2_FlowSetpoint_Nm3min * (rCycleTime_dt_s / 60.0));
        rHeatTotalBlowTime_s := rHeatTotalBlowTime_s + rCycleTime_dt_s;

        (* Endpoint Reached: Estimated carbon <= target carbon OR remaining O2 exhausted *)
        IF (x_est[0] <= rTargetTapCarbon_pct) OR (rFsmStateTimer_s >= 95.0) THEN
            bO2_MainEmergencyShutoffValve := FALSE; (* Shut off main oxygen *)
            rO2_FlowSetpoint_Nm3min := 0.0;
            bLanceNitrogenPurgeValve := TRUE;       (* Flush nozzle tip with N2 *)
            iFsmState := cSTATE_BOTTOM_STIR_RINSE;  (* Proceed to State 9 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 9: STATE_BOTTOM_STIRRING_HOMOGENIZATION_RINSE                   *)
    (* --------------------------------------------------------------------- *)
    9: (* cSTATE_BOTTOM_STIR_RINSE *)
        (* Pure Argon rinse stirring (25 Nm3/min) to homogenize bath & float inclusions *)
        bO2_MainEmergencyShutoffValve := FALSE;
        rO2_FlowSetpoint_Nm3min := 0.0;
        rLanceTargetElevation_mm := 2800.0; (* Hoist lance out of emulsion *)
        iBottomGasTypeSelected := 2;        (* Pure Argon *)
        rBottomGasFlowCmd_Nm3min := 25.0;   (* Vigorous rinse flow *)
        bGasRecoveryThreeWayValveCmd := FALSE; (* Switch offgas recovery to flare *)
        rPrimaryOffgasDamperCmd_pct := 35.0;

        (* Rinse duration: 90 seconds for deep chemical equilibrium *)
        IF rFsmStateTimer_s >= 75.0 THEN
            bLanceNitrogenPurgeValve := FALSE;
            iFsmState := cSTATE_LANCE_RETRACT_VERIFY; (* Proceed to State 10 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 10: STATE_LANCE_RETRACT_AND_BATH_TEMPERATURE_VERIFY            *)
    (* --------------------------------------------------------------------- *)
    10: (* cSTATE_LANCE_RETRACT_VERIFY *)
        (* Lance full retract to tower park position, skirt raises, final TSC dip *)
        rLanceTargetElevation_mm := 5000.0;
        rSkirtElevationCmd_mm := 1200.0; (* Raise movable skirt *)
        bNitrogenSealingCurtainCmd := FALSE;
        iBottomGasTypeSelected := 2;     (* Argon maintain tuyeres *)
        rBottomGasFlowCmd_Nm3min := 6.0;
        rPrimaryOffgasDamperCmd_pct := 20.0;

        (* Verification complete, signal tapping authorization *)
        IF (rLanceHeightActual_Z_mm >= 4800.0) AND (rSkirtPositionActual_mm >= 1100.0) AND (rFsmStateTimer_s >= 15.0) THEN
            bHeatCompleteReadyToTap := TRUE;
            IF rVesselTiltAngle_deg >= 10.0 THEN
                iFsmState := cSTATE_VESSEL_TILT_TAPPING; (* Proceed to State 11 *)
            END_IF;
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 11: STATE_VESSEL_TILT_STEEL_TAPPING_AND_ALLOY_TRIM              *)
    (* --------------------------------------------------------------------- *)
    11: (* cSTATE_VESSEL_TILT_TAPPING *)
        (* Converter tilts to +95 deg tapping angle into teeming ladle below *)
        bHeatCompleteReadyToTap := FALSE;
        rTappingTimer_s := rTappingTimer_s + rCycleTime_dt_s;
        rLanceTargetElevation_mm := 5000.0;
        rSkirtElevationCmd_mm := 1200.0;
        iBottomGasTypeSelected := 2; (* Argon shielding *)
        rBottomGasFlowCmd_Nm3min := 4.0;

        (* Deploy pneumatic slag dart / stopper when 90% of heat has drained (~240s) *)
        IF (rFsmStateTimer_s >= 240.0) AND NOT bTappingSlagDartDropped THEN
            bTappingSlagDartDropped := TRUE; (* Stop slag carryover into ladle *)
        END_IF;

        (* Tapping complete: Vessel returns to vertical (0.0 deg) *)
        IF (rFsmStateTimer_s >= 300.0) AND (ABS(rVesselTiltAngle_deg) <= 2.0) THEN
            iFsmState := cSTATE_SLAG_SPLASHING_COAT; (* Proceed to State 12 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 12: STATE_SLAG_SPLASHING_REFRACTORY_COATING_CYCLE               *)
    (* --------------------------------------------------------------------- *)
    12: (* cSTATE_SLAG_SPLASHING_COAT *)
        (* High-pressure Nitrogen blowing (850 Nm3/min N2) to coat vessel walls *)
        rLanceTargetElevation_mm := 1700.0;
        bLanceNitrogenPurgeValve := TRUE; (* Feed high-pressure N2 through lance *)
        rO2_MainEmergencyShutoffValve := FALSE; (* O2 strictly closed *)
        rO2_FlowSetpoint_Nm3min := 0.0;
        rSkirtElevationCmd_mm := 250.0;   (* Semi-lowered skirt *)
        rPrimaryOffgasDamperCmd_pct := 70.0;
        iBottomGasTypeSelected := 1;      (* Nitrogen *)
        rBottomGasFlowCmd_Nm3min := 15.0;

        (* Splashing cycle timer: 180 seconds target *)
        rSlagSplashingTimer_s := rSlagSplashingTimer_s + rCycleTime_dt_s;
        IF rSlagSplashingTimer_s >= rSlagSplashingTargetTime_s THEN
            bLanceNitrogenPurgeValve := FALSE;
            rSlagSplashingTimer_s := 0.0;
            iFsmState := cSTATE_IDLE; (* Cycle complete! Return to State 0 *)
        END_IF;

    (* --------------------------------------------------------------------- *)
    (* STATE 13: STATE_EMERGENCY_LANCE_WATER_LEAK_OR_HOOD_TRIP               *)
    (* --------------------------------------------------------------------- *)
    13: (* cSTATE_EMERGENCY_LEAK_TRIP *)
        (* Fail-Safe Emergency Trip: Immediate O2 shutoff, N2 lance purge, *)
        (* emergency high-speed lance hoist, open damper, gas recovery abort *)
        bEmergencyShutdownActive := TRUE;
        bO2_MainEmergencyShutoffValve := FALSE; (* Immediate hardwired cut *)
        rO2_MainFlowControlValve_pct := 0.0;
        rO2_FlowSetpoint_Nm3min := 0.0;
        bLanceNitrogenPurgeValve := TRUE;       (* Purge nozzle cavities *)
        rLanceTargetElevation_mm := 5000.0;     (* Emergency hoist park *)
        rLanceWinchSpeedCmd_mms := -45.0;       (* Max emergency retract speed *)
        iLanceWinchDirectionCmd := -1;          (* Hoist *)
        rLimeVibratoryFeederCmd_pct := 0.0;
        rDoloVibratoryFeederCmd_pct := 0.0;
        bFluxBatchDischargeGateOpen := FALSE;
        bGasRecoveryThreeWayValveCmd := FALSE;  (* Abort to flare stack *)
        rPrimaryOffgasDamperCmd_pct := 100.0;   (* Max draft evacuation *)
        rSkirtElevationCmd_mm := 1200.0;        (* Hoist skirt *)
        bSublanceCycleInProgress := FALSE;
        rSublanceWinchSpeedCmd_mms := -50.0;    (* Emergency hoist sublance *)
        iSublanceWinchDirectionCmd := -1;

        (* Latch emergency state until operator acknowledges alarms & confirms safe conditions *)
        IF bAlarmAcknowledgeCmd AND NOT bEmergencyTripCmd AND NOT bAlarm_LanceWaterLeakTrip AND
           (rLanceDeltaT_Voted < rLanceDeltaT_H_degC) AND (rLanceHeightActual_Z_mm >= 4800.0) THEN
            bEmergencyShutdownActive := FALSE;
            bLanceNitrogenPurgeValve := FALSE;
            iFsmState := cSTATE_IDLE; (* Reset to State 0 *)
        END_IF;

    ELSE
        iFsmState := cSTATE_IDLE; (* Fallback safety *)
END_CASE;

(* ========================================================================= *)
(* PHASE 5: ISA-18.2 MULTI-TIERED ALARM ENGINE & STATUS WORD REGISTERS       *)
(* ========================================================================= *)
(* Rigorous limit monitoring with deadband hysteresis, OG gas recovery       *)
(* switchover permissives, and IEEE/IEC bit-packed 32-bit DWORD words.       *)

(* ------------------------------------------------------------------------- *)
(* STEP 5.1: CRITICAL LANCE WATER LEAK PROTECTION LOGIC                      *)
(* Immediate detection of water leaks into liquid steel: acoustic + dP/mass  *)
(* ------------------------------------------------------------------------- *)
(* Ultrasonic Acoustic Water Leak Sensor Check (Piezo resonance: threshold 650 mV) *)
IF (rLanceWaterLeakAcoustic_raw > 650.0) OR (rLanceWaterSupplyFlow_m3h < 320.0) THEN
    rWaterLeakConfirmTimer_s := rWaterLeakConfirmTimer_s + rCycleTime_dt_s;
    IF rWaterLeakConfirmTimer_s >= 0.200 THEN (* 200 ms confirmation *)
        bCriticalWaterLeakDetected := TRUE;
        bAlarm_LanceWaterLeakTrip := TRUE;
    END_IF;
ELSE
    IF NOT bAlarm_LanceWaterLeakTrip THEN
        rWaterLeakConfirmTimer_s := 0.0;
    END_IF;
END_IF;

(* Reset water leak alarm when operator acknowledges and acoustic sensor normalizes *)
IF bAlarmAcknowledgeCmd AND (rLanceWaterLeakAcoustic_raw < 350.0) AND (rLanceWaterSupplyFlow_m3h >= 400.0) THEN
    bCriticalWaterLeakDetected := FALSE;
    bAlarm_LanceWaterLeakTrip := FALSE;
    rWaterLeakConfirmTimer_s := 0.0;
END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 5.2: ISA-18.2 MULTI-TIERED LIMIT ALARM MONITORING WITH DEADBANDS     *)
(* ------------------------------------------------------------------------- *)
(* 5.2.1: Main O2 Supply Header Pressure [bar] *)
IF rO2_Press_Voted >= rO2_Press_HH_bar THEN
    bAlarm_O2_Press_HH := TRUE;
ELSIF rO2_Press_Voted <= (rO2_Press_HH_bar - rO2_Press_Hyst_bar) THEN
    IF bAlarmAcknowledgeCmd THEN bAlarm_O2_Press_HH := FALSE; END_IF;
END_IF;

IF rO2_Press_Voted <= rO2_Press_LL_bar THEN
    bAlarm_O2_Press_LL := TRUE;
ELSIF rO2_Press_Voted >= (rO2_Press_LL_bar + rO2_Press_Hyst_bar) THEN
    IF bAlarmAcknowledgeCmd THEN bAlarm_O2_Press_LL := FALSE; END_IF;
END_IF;

(* 5.2.2: Lance Cooling Water Delta T [deg C] *)
IF rLanceDeltaT_Voted >= rLanceDeltaT_HH_degC THEN
    bAlarm_LanceWaterDeltaT_HH := TRUE;
ELSIF rLanceDeltaT_Voted <= (rLanceDeltaT_HH_degC - rLanceDeltaT_Hyst_degC) THEN
    IF bAlarmAcknowledgeCmd THEN bAlarm_LanceWaterDeltaT_HH := FALSE; END_IF;
END_IF;

(* 5.2.3: Waste Heat Boiler Hood Draft Pressure [Pa] *)
IF rHoodDraftPressure_Pa >= rHoodDraft_HH_Pa THEN
    bAlarm_HoodDraft_HH := TRUE;
ELSIF rHoodDraftPressure_Pa <= (rHoodDraft_HH_Pa - rHoodDraft_Hyst_Pa) THEN
    IF bAlarmAcknowledgeCmd THEN bAlarm_HoodDraft_HH := FALSE; END_IF;
END_IF;

(* 5.2.4: Offgas Mass Spectrometer Oxygen Concentration [% vol O2] *)
IF rOffgas_O2_Conc_pct >= rOffgas_O2_HH_pct THEN
    bAlarm_Offgas_O2_HH := TRUE;
ELSIF rOffgas_O2_Conc_pct <= (rOffgas_O2_HH_pct - rOffgas_O2_Hyst_pct) THEN
    IF bAlarmAcknowledgeCmd THEN bAlarm_Offgas_O2_HH := FALSE; END_IF;
END_IF;

(* 5.2.5: Molten Steel Bath Bulk Temperature [deg C] *)
IF x_est[1] >= rBathTemp_HH_degC THEN
    bAlarm_BathTemp_HH := TRUE;
ELSIF x_est[1] <= (rBathTemp_HH_degC - 10.0) THEN
    IF bAlarmAcknowledgeCmd THEN bAlarm_BathTemp_HH := FALSE; END_IF;
END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 5.3: SUPPRESSED-COMBUSTION OG GAS RECOVERY SWITCHOVER LOGIC          *)
(* Criteria for recovery into LD gas holder:                                  *)
(* 1. CO >= 35.0 vol%                                                        *)
(* 2. O2 <= 1.00 vol%                                                        *)
(* 3. Skirt fully seated (0 mm) and nitrogen sealing curtain active          *)
(* 4. Active blowing states (Main Decarb, Foaming, or Trim Blow)             *)
(* 5. No positive pressure draft hazard in hood                              *)
(* ------------------------------------------------------------------------- *)
IF (rOffgas_CO_Voted >= 35.0) AND (rOffgas_O2_Conc_pct <= 1.00) AND
   bSkirtFullyLowered_LS AND (rHoodDraftPressure_Pa < -30.0) AND
   ((iFsmState = cSTATE_MAIN_DECARB_DEEP_BLOW) OR
    (iFsmState = cSTATE_SLAG_FOAM_SLOP_SUPPRESS) OR
    (iFsmState = cSTATE_SUBLANCE_IMMERSION_DIP) OR
    (iFsmState = cSTATE_ENDPOINT_FINE_TRIM_BLOW)) THEN
    rGasRecoveryEligibleTimer_s := rGasRecoveryEligibleTimer_s + rCycleTime_dt_s;
    IF rGasRecoveryEligibleTimer_s >= 10.0 THEN (* 10s stability proof *)
        bGasRecoveryPermissive := TRUE;
        bGasRecoveryThreeWayValveCmd := TRUE; (* Route to LD Gas Holder *)
    END_IF;
ELSE
    rGasRecoveryEligibleTimer_s := 0.0;
    bGasRecoveryPermissive := FALSE;
    bGasRecoveryThreeWayValveCmd := FALSE; (* Route to Flare Stack *)
END_IF;

(* Emergency Abort on High O2 in Gas Recovery: Immediate switch to flare *)
IF bAlarm_Offgas_O2_HH OR (rOffgas_O2_Conc_pct > 1.80) THEN
    bGasRecoveryThreeWayValveCmd := FALSE;
    bGasRecoveryPermissive := FALSE;
    rGasRecoveryEligibleTimer_s := 0.0;
END_IF;

(* ------------------------------------------------------------------------- *)
(* STEP 5.4: BIT-PACKED 32-BIT DWORD STATUS & ALARM WORDS                    *)
(* ------------------------------------------------------------------------- *)
(* 5.4.1: StatusWord1 - Converter Operational & Process Status *)
dwStat1 := 16#00000000;
IF bVesselVerticalLock_Z THEN dwStat1 := dwStat1 OR 16#00000001; END_IF;        (* Bit 0 *)
IF bSkirtFullyLowered_LS THEN dwStat1 := dwStat1 OR 16#00000002; END_IF;         (* Bit 1 *)
IF bO2_MainEmergencyShutoffValve THEN dwStat1 := dwStat1 OR 16#00000004; END_IF;  (* Bit 2 *)
IF rOffgas_CO_Voted > 10.0 THEN dwStat1 := dwStat1 OR 16#00000008; END_IF;        (* Bit 3 *)
IF bFluxBatchDischargeGateOpen THEN dwStat1 := dwStat1 OR 16#00000010; END_IF;    (* Bit 4 *)
IF iFsmState = cSTATE_MAIN_DECARB_DEEP_BLOW THEN dwStat1 := dwStat1 OR 16#00000020; END_IF; (* Bit 5 *)
IF bAntiSloppingActive THEN dwStat1 := dwStat1 OR 16#00000040; END_IF;            (* Bit 6 *)
IF bSublanceCycleInProgress THEN dwStat1 := dwStat1 OR 16#00000080; END_IF;       (* Bit 7 *)
IF bSublanceAcquisitionSuccessful THEN dwStat1 := dwStat1 OR 16#00000100; END_IF; (* Bit 8 *)
IF iFsmState = cSTATE_ENDPOINT_FINE_TRIM_BLOW THEN dwStat1 := dwStat1 OR 16#00000200; END_IF; (* Bit 9 *)
IF iFsmState = cSTATE_BOTTOM_STIR_RINSE THEN dwStat1 := dwStat1 OR 16#00000400; END_IF; (* Bit 10 *)
IF bLanceUpperParkLimit_LS THEN dwStat1 := dwStat1 OR 16#00000800; END_IF;        (* Bit 11 *)
IF iFsmState = cSTATE_VESSEL_TILT_TAPPING THEN dwStat1 := dwStat1 OR 16#00001000; END_IF; (* Bit 12 *)
IF iFsmState = cSTATE_SLAG_SPLASHING_COAT THEN dwStat1 := dwStat1 OR 16#00002000; END_IF; (* Bit 13 *)
IF bGasRecoveryThreeWayValveCmd THEN dwStat1 := dwStat1 OR 16#00004000; END_IF;   (* Bit 14 *)
IF bNitrogenSealingCurtainCmd THEN dwStat1 := dwStat1 OR 16#00008000; END_IF;     (* Bit 15 *)
(* Pack 4-bit FSM state index into Bits 16..19 *)
dwStat1 := dwStat1 OR SHL(DINT_TO_DWORD(INT_TO_DINT(iFsmState AND 16#0F)), 16);
IF bAutoSequenceStartCmd THEN dwStat1 := dwStat1 OR 16#00100000; END_IF;          (* Bit 20 *)
IF bHeatCompleteReadyToTap THEN dwStat1 := dwStat1 OR 16#00200000; END_IF;        (* Bit 21 *)
IF bTappingSlagDartDropped THEN dwStat1 := dwStat1 OR 16#00400000; END_IF;        (* Bit 22 *)
IF iBottomGasTypeSelected = 2 THEN dwStat1 := dwStat1 OR 16#00800000; END_IF;     (* Bit 23: Argon *)
IF bLanceNitrogenPurgeValve THEN dwStat1 := dwStat1 OR 16#01000000; END_IF;        (* Bit 24 *)
IF bFirstScanDone THEN dwStat1 := dwStat1 OR 16#02000000; END_IF;                  (* Bit 25 *)
dStatusWord1 := dwStat1;

(* 5.4.2: StatusWord2 - Subsystem Interlocks & Sensor Redundancy Health *)
dwStat2 := 16#00000000;
IF NOT bO2_Press_Ch1_Fail AND NOT bO2_Press_Ch2_Fail THEN dwStat2 := dwStat2 OR 16#00000001; END_IF;
IF NOT bLanceDeltaT_Ch1_Fail AND NOT bLanceDeltaT_Ch2_Fail THEN dwStat2 := dwStat2 OR 16#00000002; END_IF;
IF rHoodDraftPressure_Pa < 0.0 THEN dwStat2 := dwStat2 OR 16#00000004; END_IF;
IF NOT bOffgas_CO_Ch1_Fail AND NOT bOffgas_CO_Ch2_Fail THEN dwStat2 := dwStat2 OR 16#00000008; END_IF;
IF NOT bTrunnionAcoustic_Ch1_Fail AND NOT bTrunnionAcoustic_Ch2_Fail THEN dwStat2 := dwStat2 OR 16#00000010; END_IF;
IF bSublanceProbeReady THEN dwStat2 := dwStat2 OR 16#00000020; END_IF;
IF rBottomGasHeaderPress_bar >= 8.0 THEN dwStat2 := dwStat2 OR 16#00000040; END_IF;
IF rLimeHopperWeight_kg >= 1500.0 THEN dwStat2 := dwStat2 OR 16#00000080; END_IF;
IF rDoloHopperWeight_kg >= 1000.0 THEN dwStat2 := dwStat2 OR 16#00000100; END_IF;
IF bGasRecoveryPermissive THEN dwStat2 := dwStat2 OR 16#00000200; END_IF;
(* Pack 3-bit healthy channel counts *)
dwStat2 := dwStat2 OR SHL(DINT_TO_DWORD(INT_TO_DINT(iO2_Press_HealthySensors AND 16#07)), 12);
dwStat2 := dwStat2 OR SHL(DINT_TO_DWORD(INT_TO_DINT(iLanceDeltaT_HealthySensors AND 16#07)), 15);
dwStat2 := dwStat2 OR SHL(DINT_TO_DWORD(INT_TO_DINT(iTrunnionAcoustic_HealthySensors AND 16#07)), 18);
dwStat2 := dwStat2 OR SHL(DINT_TO_DWORD(INT_TO_DINT(iOffgas_CO_HealthySensors AND 16#07)), 21);
dStatusWord2 := dwStat2;

(* 5.4.3: AlarmWord1 - High Severity Emergency Trips & Interlocks *)
dwAlm1 := 16#00000000;
IF bEmergencyTripCmd THEN dwAlm1 := dwAlm1 OR 16#00000001; END_IF;                 (* Bit 0 *)
IF bAlarm_LanceWaterDeltaT_HH THEN dwAlm1 := dwAlm1 OR 16#00000002; END_IF;        (* Bit 1 *)
IF bAlarm_LanceWaterLeakTrip THEN dwAlm1 := dwAlm1 OR 16#00000004; END_IF;         (* Bit 2 *)
IF bAlarm_O2_Press_HH THEN dwAlm1 := dwAlm1 OR 16#00000008; END_IF;                (* Bit 3 *)
IF bAlarm_O2_Press_LL THEN dwAlm1 := dwAlm1 OR 16#00000010; END_IF;                (* Bit 4 *)
IF bAlarm_HoodDraft_HH THEN dwAlm1 := dwAlm1 OR 16#00000020; END_IF;               (* Bit 5 *)
IF rHoodDraftPressure_Pa <= rHoodDraft_LL_Pa THEN dwAlm1 := dwAlm1 OR 16#00000040; END_IF; (* Bit 6 *)
IF bAlarm_Offgas_O2_HH THEN dwAlm1 := dwAlm1 OR 16#00000080; END_IF;               (* Bit 7 *)
IF bAlarm_BathTemp_HH THEN dwAlm1 := dwAlm1 OR 16#00000100; END_IF;                (* Bit 8 *)
IF bLanceLowerSafetyInterlock_LS THEN dwAlm1 := dwAlm1 OR 16#00000200; END_IF;     (* Bit 9 *)
IF (rLanceWaterSupplyPress_bar < 8.0) THEN dwAlm1 := dwAlm1 OR 16#00000400; END_IF; (* Bit 10 *)
IF NOT bVesselVerticalLock_Z AND (iFsmState >= 3) AND (iFsmState <= 9) THEN
    dwAlm1 := dwAlm1 OR 16#00000800; (* Bit 11: Vessel lock failure during blow *)
END_IF;
IF NOT bSkirtFullyLowered_LS AND (iFsmState >= 3) AND (iFsmState <= 8) THEN
    dwAlm1 := dwAlm1 OR 16#00001000; (* Bit 12: Skirt seal loss during blow *)
END_IF;
IF (rBottomGasHeaderPress_bar < 4.0) THEN dwAlm1 := dwAlm1 OR 16#00002000; END_IF;(* Bit 13 *)
IF bEmergencyShutdownActive THEN dwAlm1 := dwAlm1 OR 16#00008000; END_IF;          (* Bit 15 *)
dAlarmWord1 := dwAlm1;

(* 5.4.4: AlarmWord2 - Process Warnings & Degradations *)
dwAlm2 := 16#00000000;
IF (rO2_Press_Voted >= rO2_Press_H_bar) THEN dwAlm2 := dwAlm2 OR 16#00000001; END_IF;      (* Bit 0 *)
IF (rO2_Press_Voted <= rO2_Press_L_bar) THEN dwAlm2 := dwAlm2 OR 16#00000002; END_IF;      (* Bit 1 *)
IF (rLanceDeltaT_Voted >= rLanceDeltaT_H_degC) THEN dwAlm2 := dwAlm2 OR 16#00000004; END_IF;(* Bit 2 *)
IF (rHoodDraftPressure_Pa >= rHoodDraft_H_Pa) THEN dwAlm2 := dwAlm2 OR 16#00000008; END_IF; (* Bit 3 *)
IF (rOffgas_O2_Conc_pct >= rOffgas_O2_H_pct) THEN dwAlm2 := dwAlm2 OR 16#00000010; END_IF;  (* Bit 4 *)
IF (x_est[1] >= rBathTemp_H_degC) THEN dwAlm2 := dwAlm2 OR 16#00000020; END_IF;             (* Bit 5 *)
IF bAlarm_SloppingSevere THEN dwAlm2 := dwAlm2 OR 16#00000040; END_IF;                      (* Bit 6 *)
IF bAlarm_TmrDegraded THEN dwAlm2 := dwAlm2 OR 16#00000080; END_IF;                         (* Bit 7 *)
IF bSublanceImmersionFault THEN dwAlm2 := dwAlm2 OR 16#00000100; END_IF;                    (* Bit 8 *)
IF x_est[3] > 28.0 THEN dwAlm2 := dwAlm2 OR 16#00000200; END_IF;                            (* Bit 9: High FeO *)
IF rSlagBasicity_B2 < 2.80 THEN dwAlm2 := dwAlm2 OR 16#00000400; END_IF;                    (* Bit 10: Low basicity *)
IF (x_est[2] < 0.08) AND (iFsmState = cSTATE_MAIN_DECARB_DEEP_BLOW) THEN
    dwAlm2 := dwAlm2 OR 16#00000800; (* Bit 11: Low decarb rate *)
END_IF;
IF rPostCombustionRatio_calc > 24.0 THEN dwAlm2 := dwAlm2 OR 16#00001000; END_IF;           (* Bit 12: High PCR *)
IF (rBottomGasHeaderPress_bar > 22.0) THEN dwAlm2 := dwAlm2 OR 16#00002000; END_IF;        (* Bit 13: Porous plug clogged *)
IF (rLimeHopperWeight_kg < 500.0) THEN dwAlm2 := dwAlm2 OR 16#00004000; END_IF;            (* Bit 14: Low lime *)
IF (dCampaignHeatNumber >= 5000) THEN dwAlm2 := dwAlm2 OR 16#00008000; END_IF;              (* Bit 15: Lining inspection *)
dAlarmWord2 := dwAlm2;

(* Map Cumulative Integrators to Output Registers *)
rTotalOxygenBlown_Nm3 := rHeatTotalOxygenConsumed_Nm3;
rTotalBlowDuration_s := rHeatTotalBlowTime_s;

END_FUNCTION_BLOCK