(* =====================================================================================================================
 * PHASE 2: ADVANCED CYBER-PHYSICAL OBSERVERS & MULTI-PHYSICS ESTIMATORS
 * Subsystems:
 *   2.1: 4-Tie-Bar Strain Elongation, Platen Parallelism Tilt & Thermal Mold Expansion
 *   2.2: 8-Zone Ceramic Barrel Heating PID with Non-Linear Cross-WLF Viscosity Feedforward
 *   2.3: In-Mold Piezoelectric Cavity Pressure V/P Switchover Cascade & Dynamic Overshoot Mitigation
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.1: 4 TIE-BAR DYNAMIC STRAIN ELONGATION, PLATEN BALANCING & THERMAL OBSERVER
 * Clamping Force: 16,000 kN nominal, 4x 220 mm solid alloy tie-bars, full-bridge extensometers
 * --------------------------------------------------------------------------------------------------------------------- *)
rTB_Strain_CH1 := rTieBar_Strain_CH1_In;
rTB_Strain_CH2 := rTieBar_Strain_CH2_In;
rTB_Strain_CH3 := rTieBar_Strain_CH3_In;
rTB_Strain_CH4 := rTieBar_Strain_CH4_In;

(* Range and sanity verification on strain channels *)
IF rTB_Strain_CH1 < 0.0 THEN rTB_Strain_CH1 := 0.0; END_IF;
IF rTB_Strain_CH2 < 0.0 THEN rTB_Strain_CH2 := 0.0; END_IF;
IF rTB_Strain_CH3 < 0.0 THEN rTB_Strain_CH3 := 0.0; END_IF;
IF rTB_Strain_CH4 < 0.0 THEN rTB_Strain_CH4 := 0.0; END_IF;

(* Calculate Tensile Force per Tie-Bar using Hooke's Law: F = (E * A / L) * Delta_L *)
(* Constant K_tb = (E * A / L) = (210,000 N/mm2 * 38,013.27 mm2 / 3,500 mm) = 2,280,796 N/mm = 2,280.8 kN/mm = 2.2808 kN/um *)
rTB_Force_CH1 := 2.280796 * rTB_Strain_CH1;
rTB_Force_CH2 := 2.280796 * rTB_Strain_CH2;
rTB_Force_CH3 := 2.280796 * rTB_Strain_CH3;
rTB_Force_CH4 := 2.280796 * rTB_Strain_CH4;

(* Total Measured Clamp Force and Mean Strain *)
rTB_TotalClampForce := rTB_Force_CH1 + rTB_Force_CH2 + rTB_Force_CH3 + rTB_Force_CH4;
rTB_MeanStrain := (rTB_Strain_CH1 + rTB_Strain_CH2 + rTB_Strain_CH3 + rTB_Strain_CH4) * 0.25;

(* Moving Platen Parallelism & Angular Tilt Vectors *)
(* Horizontal Platen Tilt: Operator Side (CH1+CH3) vs Non-Operator Side (CH2+CH4) *)
rPlaten_Tilt_Horizontal := ((rTB_Strain_CH1 + rTB_Strain_CH3) - (rTB_Strain_CH2 + rTB_Strain_CH4)) * 0.5;

(* Vertical Platen Tilt: Top Half (CH1+CH2) vs Bottom Half (CH3+CH4) *)
rPlaten_Tilt_Vertical := ((rTB_Strain_CH1 + rTB_Strain_CH2) - (rTB_Strain_CH3 + rTB_Strain_CH4)) * 0.5;

(* Torsional Diagonal Tilt: (CH1+CH4) vs (CH2+CH3) *)
rPlaten_Tilt_Diagonal := ((rTB_Strain_CH1 + rTB_Strain_CH4) - (rTB_Strain_CH2 + rTB_Strain_CH3)) * 0.5;

(* Peak-to-Peak Platen Elongation Spread *)
rTemp_A := MAX(MAX(rTB_Strain_CH1, rTB_Strain_CH2), MAX(rTB_Strain_CH3, rTB_Strain_CH4));
rTemp_B := MIN(MIN(rTB_Strain_CH1, rTB_Strain_CH2), MIN(rTB_Strain_CH3, rTB_Strain_CH4));
rPlaten_MaxDeviation := rTemp_A - rTemp_B;
rPlaten_ParallelismTilt_Out := rPlaten_MaxDeviation;

(* Thermal Expansion Compensation of Mold Platens & Tie-Bars *)
(* Delta_L_thermal = Alpha * L_gauge * (T_platen - T_ref) *)
rTemp_Delta := rPlaten_MetalTemp_In - rPlaten_RefTemp;
IF rTemp_Delta > -30.0 AND rTemp_Delta < 150.0 THEN
    rMold_ThermalElongation_Delta := rTB_ThermalExpansionCoeff * rTB_GaugeLength * rTemp_Delta;
    (* Dynamic closed-loop mold height trim to maintain constant locking tonnage despite thermal growth *)
    rMoldHeight_TrimAccumulator := -1.0 * rMold_ThermalElongation_Delta;
ELSE
    rMold_ThermalElongation_Delta := 0.0;
END_IF;

rServo_MoldHeight_Delta_Out := rMoldHeight_TrimAccumulator;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.2: 8-ZONE BARREL CERAMIC HEATING WITH CROSS-WLF NON-LINEAR VISCOSITY FEEDFORWARD
 * Zones: 1 (Feed), 2 (Rear), 3 (Mid-Rear), 4 (Middle), 5 (Mid-Front), 6 (Front), 7 (Adapter), 8 (Nozzle)
 * Constitutive Rheological Model: Cross-WLF with viscous shear heating power subtraction
 * --------------------------------------------------------------------------------------------------------------------- *)
rBarrel_PV_Z1 := rBarrelTemp_Zone1_Feed_In;
rBarrel_PV_Z2 := rBarrelTemp_Zone2_Rear_In;
rBarrel_PV_Z3 := rBarrelTemp_Zone3_MidRear_In;
rBarrel_PV_Z4 := rBarrelTemp_Zone4_Middle_In;
rBarrel_PV_Z5 := rBarrelTemp_Zone5_MidFront_In;
rBarrel_PV_Z6 := rBarrelTemp_Zone6_Front_In;
rBarrel_PV_Z7 := rBarrelTemp_Zone7_Adapter_In;
rBarrel_PV_Z8 := rBarrelTemp_Zone8_Nozzle_In;

(* Non-Linear Cross-WLF Viscosity Calculation *)
(* Absolute Polymer Temperature in Kelvin *)
rTemp_A := rMeltTemp_Voted_Val + 273.15;
IF rTemp_A < 350.0 THEN rTemp_A := 350.0; END_IF;

(* WLF Arrhenius Temperature Shift Factor a_T *)
rTemp_B := rTemp_A - rWLF_TStar;
IF (rWLF_C2 + rTemp_B) > 5.0 THEN
    rTemp_C := EXP(-1.0 * (rWLF_C1 * rTemp_B) / (rWLF_C2 + rTemp_B));
ELSE
    rTemp_C := 1.0;
END_IF;

(* Pressure Dependence Viscosity Factor b_P *)
rTemp_Delta := EXP(rWLF_D3_PresCoeff * rMeltPres_Voted_Val);

(* Current Zero-Shear Viscosity Eta_0(T, P) *)
rTemp_Sum := rWLF_Eta0_Ref * rTemp_C * rTemp_Delta;
IF rTemp_Sum < 50.0 THEN rTemp_Sum := 50.0; END_IF;

(* Extruder Screw Channel Shear Rate Calculation: Gamma_Dot = (PI * D_screw * N_screw) / (h_channel * 60) *)
IF rServo_ScrewRPM_Cmd_Out > 0.5 THEN
    rPolymer_ShearRate := (3.1415926 * (rScrew_Diameter * 0.001) * (rServo_ScrewRPM_Cmd_Out / 60.0)) / (rScrew_ChannelDepth * 0.001);
ELSE
    rPolymer_ShearRate := 0.1;
END_IF;

(* Cross-WLF Apparent Dynamic Viscosity: Eta = Eta_0 / [1 + (Eta_0 * Gamma_Dot / Tau_star)^(1-n)] *)
rTemp_Diff := (rTemp_Sum * rPolymer_ShearRate) / rWLF_TauStar;
IF rTemp_Diff > 0.0 THEN
    rTemp_AbsDiff := 1.0 + EXPT(rTemp_Diff, (1.0 - rWLF_PowerLawIndex));
    rPolymer_DynamicViscosity := rTemp_Sum / rTemp_AbsDiff;
ELSE
    rPolymer_DynamicViscosity := rTemp_Sum;
END_IF;

rMeltViscosity_Shear_Out := rPolymer_DynamicViscosity;

(* Viscous Shear Heating Energy Dissipation: Q_visc = Eta * (Gamma_Dot)^2 * Volume_channel [W] *)
rShear_DissipationPower := rPolymer_DynamicViscosity * (rPolymer_ShearRate * rPolymer_ShearRate) * rScrew_ChannelVolume;

(* Feedforward Heat Subtraction Factor (Reduces external heater duty during high-speed dosing) *)
rFeedforward_ThermalPower := (rShear_DissipationPower / 15000.0) * 100.0;
IF rFeedforward_ThermalPower > 45.0 THEN
    rFeedforward_ThermalPower := 45.0;
ELSIF rFeedforward_ThermalPower < 0.0 THEN
    rFeedforward_ThermalPower := 0.0;
END_IF;

(* --- Zone 1 PID Loop (Feed Throat Water-Cooled / SSR) --- *)
rPID_Err_Z1 := rBarrel_SP_Z1 - rBarrel_PV_Z1;
rPID_Integ_Z1 := rPID_Integ_Z1 + ((rPID_Err_Z1 + rPID_ErrPrev_Z1) * 0.5 * (rPID_Kp_Zones / rPID_Ti_Zones) * rScanTime_Ts);
IF rPID_Integ_Z1 > rPID_Integ_Limit THEN rPID_Integ_Z1 := rPID_Integ_Limit;
ELSIF rPID_Integ_Z1 < -rPID_Integ_Limit THEN rPID_Integ_Z1 := -rPID_Integ_Limit; END_IF;
rPID_Deriv_Z1 := rPID_Deriv_Z1 + (rScanTime_Ts / (rPID_DerivFilter_Tau + rScanTime_Ts)) *
                 ((-1.0 * (rBarrel_PV_Z1 - rPID_ErrPrev_Z1) * (rPID_Kp_Zones * rPID_Td_Zones / rScanTime_Ts)) - rPID_Deriv_Z1);
rPID_ErrPrev_Z1 := rPID_Err_Z1;
rPID_Out_Z1 := (rPID_Kp_Zones * rPID_Err_Z1) + rPID_Integ_Z1 + rPID_Deriv_Z1;
IF rPID_Out_Z1 > 100.0 THEN rPID_Out_Z1 := 100.0; ELSIF rPID_Out_Z1 < 0.0 THEN rPID_Out_Z1 := 0.0; END_IF;
rHeaterDuty_Zone1_Out := rPID_Out_Z1;

(* --- Zone 2 PID Loop (Rear Compression Zone) --- *)
rPID_Err_Z2 := rBarrel_SP_Z2 - rBarrel_PV_Z2;
rPID_Integ_Z2 := rPID_Integ_Z2 + ((rPID_Err_Z2 + rPID_ErrPrev_Z2) * 0.5 * (rPID_Kp_Zones / rPID_Ti_Zones) * rScanTime_Ts);
IF rPID_Integ_Z2 > rPID_Integ_Limit THEN rPID_Integ_Z2 := rPID_Integ_Limit;
ELSIF rPID_Integ_Z2 < -rPID_Integ_Limit THEN rPID_Integ_Z2 := -rPID_Integ_Limit; END_IF;
rPID_Deriv_Z2 := rPID_Deriv_Z2 + (rScanTime_Ts / (rPID_DerivFilter_Tau + rScanTime_Ts)) *
                 ((-1.0 * (rBarrel_PV_Z2 - rPID_ErrPrev_Z2) * (rPID_Kp_Zones * rPID_Td_Zones / rScanTime_Ts)) - rPID_Deriv_Z2);
rPID_ErrPrev_Z2 := rPID_Err_Z2;
rPID_Out_Z2 := (rPID_Kp_Zones * rPID_Err_Z2) + rPID_Integ_Z2 + rPID_Deriv_Z2;
IF rPID_Out_Z2 > 100.0 THEN rPID_Out_Z2 := 100.0; ELSIF rPID_Out_Z2 < 0.0 THEN rPID_Out_Z2 := 0.0; END_IF;
rHeaterDuty_Zone2_Out := rPID_Out_Z2;

(* --- Zone 3 PID Loop (Middle-Rear Plasticizing with Shear Compensation) --- *)
rPID_Err_Z3 := rBarrel_SP_Z3 - rBarrel_PV_Z3;
rPID_Integ_Z3 := rPID_Integ_Z3 + ((rPID_Err_Z3 + rPID_ErrPrev_Z3) * 0.5 * (rPID_Kp_Zones / rPID_Ti_Zones) * rScanTime_Ts);
IF rPID_Integ_Z3 > rPID_Integ_Limit THEN rPID_Integ_Z3 := rPID_Integ_Limit;
ELSIF rPID_Integ_Z3 < -rPID_Integ_Limit THEN rPID_Integ_Z3 := -rPID_Integ_Limit; END_IF;
rPID_Deriv_Z3 := rPID_Deriv_Z3 + (rScanTime_Ts / (rPID_DerivFilter_Tau + rScanTime_Ts)) *
                 ((-1.0 * (rBarrel_PV_Z3 - rPID_ErrPrev_Z3) * (rPID_Kp_Zones * rPID_Td_Zones / rScanTime_Ts)) - rPID_Deriv_Z3);
rPID_ErrPrev_Z3 := rPID_Err_Z3;
rPID_Out_Z3 := (rPID_Kp_Zones * rPID_Err_Z3) + rPID_Integ_Z3 + rPID_Deriv_Z3 - (rFeedforward_ThermalPower * 0.40);
IF rPID_Out_Z3 > 100.0 THEN rPID_Out_Z3 := 100.0; ELSIF rPID_Out_Z3 < 0.0 THEN rPID_Out_Z3 := 0.0; END_IF;
rHeaterDuty_Zone3_Out := rPID_Out_Z3;

(* --- Zone 4 PID Loop (Middle Plasticizing with Shear Compensation) --- *)
rPID_Err_Z4 := rBarrel_SP_Z4 - rBarrel_PV_Z4;
rPID_Integ_Z4 := rPID_Integ_Z4 + ((rPID_Err_Z4 + rPID_ErrPrev_Z4) * 0.5 * (rPID_Kp_Zones / rPID_Ti_Zones) * rScanTime_Ts);
IF rPID_Integ_Z4 > rPID_Integ_Limit THEN rPID_Integ_Z4 := rPID_Integ_Limit;
ELSIF rPID_Integ_Z4 < -rPID_Integ_Limit THEN rPID_Integ_Z4 := -rPID_Integ_Limit; END_IF;
rPID_Deriv_Z4 := rPID_Deriv_Z4 + (rScanTime_Ts / (rPID_DerivFilter_Tau + rScanTime_Ts)) *
                 ((-1.0 * (rBarrel_PV_Z4 - rPID_ErrPrev_Z4) * (rPID_Kp_Zones * rPID_Td_Zones / rScanTime_Ts)) - rPID_Deriv_Z4);
rPID_ErrPrev_Z4 := rPID_Err_Z4;
rPID_Out_Z4 := (rPID_Kp_Zones * rPID_Err_Z4) + rPID_Integ_Z4 + rPID_Deriv_Z4 - (rFeedforward_ThermalPower * 0.70);
IF rPID_Out_Z4 > 100.0 THEN rPID_Out_Z4 := 100.0; ELSIF rPID_Out_Z4 < 0.0 THEN rPID_Out_Z4 := 0.0; END_IF;
rHeaterDuty_Zone4_Out := rPID_Out_Z4;

(* --- Zone 5 PID Loop (Middle-Front Homogenizing with Shear Compensation) --- *)
rPID_Err_Z5 := rBarrel_SP_Z5 - rBarrel_PV_Z5;
rPID_Integ_Z5 := rPID_Integ_Z5 + ((rPID_Err_Z5 + rPID_ErrPrev_Z5) * 0.5 * (rPID_Kp_Zones / rPID_Ti_Zones) * rScanTime_Ts);
IF rPID_Integ_Z5 > rPID_Integ_Limit THEN rPID_Integ_Z5 := rPID_Integ_Limit;
ELSIF rPID_Integ_Z5 < -rPID_Integ_Limit THEN rPID_Integ_Z5 := -rPID_Integ_Limit; END_IF;
rPID_Deriv_Z5 := rPID_Deriv_Z5 + (rScanTime_Ts / (rPID_DerivFilter_Tau + rScanTime_Ts)) *
                 ((-1.0 * (rBarrel_PV_Z5 - rPID_ErrPrev_Z5) * (rPID_Kp_Zones * rPID_Td_Zones / rScanTime_Ts)) - rPID_Deriv_Z5);
rPID_ErrPrev_Z5 := rPID_Err_Z5;
rPID_Out_Z5 := (rPID_Kp_Zones * rPID_Err_Z5) + rPID_Integ_Z5 + rPID_Deriv_Z5 - (rFeedforward_ThermalPower * 1.00);
IF rPID_Out_Z5 > 100.0 THEN rPID_Out_Z5 := 100.0; ELSIF rPID_Out_Z5 < 0.0 THEN rPID_Out_Z5 := 0.0; END_IF;
rHeaterDuty_Zone5_Out := rPID_Out_Z5;

(* --- Zone 6 PID Loop (Front Metering Zone with Shear Compensation) --- *)
rPID_Err_Z6 := rBarrel_SP_Z6 - rBarrel_PV_Z6;
rPID_Integ_Z6 := rPID_Integ_Z6 + ((rPID_Err_Z6 + rPID_ErrPrev_Z6) * 0.5 * (rPID_Kp_Zones / rPID_Ti_Zones) * rScanTime_Ts);
IF rPID_Integ_Z6 > rPID_Integ_Limit THEN rPID_Integ_Z6 := rPID_Integ_Limit;
ELSIF rPID_Integ_Z6 < -rPID_Integ_Limit THEN rPID_Integ_Z6 := -rPID_Integ_Limit; END_IF;
rPID_Deriv_Z6 := rPID_Deriv_Z6 + (rScanTime_Ts / (rPID_DerivFilter_Tau + rScanTime_Ts)) *
                 ((-1.0 * (rBarrel_PV_Z6 - rPID_ErrPrev_Z6) * (rPID_Kp_Zones * rPID_Td_Zones / rScanTime_Ts)) - rPID_Deriv_Z6);
rPID_ErrPrev_Z6 := rPID_Err_Z6;
rPID_Out_Z6 := (rPID_Kp_Zones * rPID_Err_Z6) + rPID_Integ_Z6 + rPID_Deriv_Z6 - (rFeedforward_ThermalPower * 0.60);
IF rPID_Out_Z6 > 100.0 THEN rPID_Out_Z6 := 100.0; ELSIF rPID_Out_Z6 < 0.0 THEN rPID_Out_Z6 := 0.0; END_IF;
rHeaterDuty_Zone6_Out := rPID_Out_Z6;

(* --- Zone 7 PID Loop (Nozzle Adapter Body) --- *)
rPID_Err_Z7 := rBarrel_SP_Z7 - rBarrel_PV_Z7;
rPID_Integ_Z7 := rPID_Integ_Z7 + ((rPID_Err_Z7 + rPID_ErrPrev_Z7) * 0.5 * (rPID_Kp_Zones / rPID_Ti_Zones) * rScanTime_Ts);
IF rPID_Integ_Z7 > rPID_Integ_Limit THEN rPID_Integ_Z7 := rPID_Integ_Limit;
ELSIF rPID_Integ_Z7 < -rPID_Integ_Limit THEN rPID_Integ_Z7 := -rPID_Integ_Limit; END_IF;
rPID_Deriv_Z7 := rPID_Deriv_Z7 + (rScanTime_Ts / (rPID_DerivFilter_Tau + rScanTime_Ts)) *
                 ((-1.0 * (rBarrel_PV_Z7 - rPID_ErrPrev_Z7) * (rPID_Kp_Zones * rPID_Td_Zones / rScanTime_Ts)) - rPID_Deriv_Z7);
rPID_ErrPrev_Z7 := rPID_Err_Z7;
rPID_Out_Z7 := (rPID_Kp_Zones * rPID_Err_Z7) + rPID_Integ_Z7 + rPID_Deriv_Z7;
IF rPID_Out_Z7 > 100.0 THEN rPID_Out_Z7 := 100.0; ELSIF rPID_Out_Z7 < 0.0 THEN rPID_Out_Z7 := 0.0; END_IF;
rHeaterDuty_Zone7_Out := rPID_Out_Z7;

(* --- Zone 8 PID Loop (Injection Nozzle Tip) --- *)
rPID_Err_Z8 := rBarrel_SP_Z8 - rBarrel_PV_Z8;
rPID_Integ_Z8 := rPID_Integ_Z8 + ((rPID_Err_Z8 + rPID_ErrPrev_Z8) * 0.5 * (rPID_Kp_Zones / rPID_Ti_Zones) * rScanTime_Ts);
IF rPID_Integ_Z8 > rPID_Integ_Limit THEN rPID_Integ_Z8 := rPID_Integ_Limit;
ELSIF rPID_Integ_Z8 < -rPID_Integ_Limit THEN rPID_Integ_Z8 := -rPID_Integ_Limit; END_IF;
rPID_Deriv_Z8 := rPID_Deriv_Z8 + (rScanTime_Ts / (rPID_DerivFilter_Tau + rScanTime_Ts)) *
                 ((-1.0 * (rBarrel_PV_Z8 - rPID_ErrPrev_Z8) * (rPID_Kp_Zones * rPID_Td_Zones / rScanTime_Ts)) - rPID_Deriv_Z8);
rPID_ErrPrev_Z8 := rPID_Err_Z8;
rPID_Out_Z8 := (rPID_Kp_Zones * rPID_Err_Z8) + rPID_Integ_Z8 + rPID_Deriv_Z8;
IF rPID_Out_Z8 > 100.0 THEN rPID_Out_Z8 := 100.0; ELSIF rPID_Out_Z8 < 0.0 THEN rPID_Out_Z8 := 0.0; END_IF;
rHeaterDuty_Zone8_Out := rPID_Out_Z8;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUBSECTION 2.3: IN-MOLD PIEZOELECTRIC CAVITY PRESSURE V/P SWITCHOVER CASCADE & ANTI-OVERSHOOT
 * Kistler/Priamus In-Mold Transducer Integration with Dynamic Derivative Rate-of-Rise Detection
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Numerical Backward Difference Filter for Dynamic Rate of Pressure Rise dP_cav/dt *)
rTemp_A := (rCavPres_Voted_Val - rCavPres_Prev_Voted) / rScanTime_Ts;
rCavPres_Derivative := rCavPres_Derivative + (0.28 * (rTemp_A - rCavPres_Derivative));

(* Cavity Pressure Time-Integral Accumulator *)
IF (iFSM_State = 5) OR (iFSM_State = 6) OR (iFSM_State = 7) THEN
    rCavPres_Integral := rCavPres_Integral + (rCavPres_Voted_Val * rScanTime_Ts);
ELSE
    rCavPres_Integral := 0.0;
END_IF;

(* Track Cycle Peak Cavity Pressure & Overshoot *)
IF rCavPres_Voted_Val > rCavity_PeakObservedPressure THEN
    rCavity_PeakObservedPressure := rCavPres_Voted_Val;
END_IF;

IF rCavity_PeakObservedPressure > rRecipe_HoldPressure_In THEN
    rCavity_PeakOvershoot_Out := rCavity_PeakObservedPressure - rRecipe_HoldPressure_In;
ELSE
    rCavity_PeakOvershoot_Out := 0.0;
END_IF;

(* Multi-Criteria V/P Switchover Evaluation *)
IF (iFSM_State = 5) AND (NOT bVP_SwitchoverLatched) THEN
    (* Criterion 1: Quartz Cavity Pressure Setpoint Reached *)
    IF rCavPres_Voted_Val >= rRecipe_CavityVPOvershoot_In THEN
        bVP_TriggeredByCavity := TRUE;
        bVP_SwitchoverLatched := TRUE;
    (* Criterion 2: Dynamic Pressure Inflection Spike (Cavity Volumetric Fill Front Reaches Transducer) *)
    ELSIF (rCavPres_Derivative >= rVP_RateThreshold) AND (rCavPres_Voted_Val >= 180.0) THEN
        bVP_TriggeredByRate := TRUE;
        bVP_SwitchoverLatched := TRUE;
    (* Criterion 3: Machine Stroke Linear Position Safety Limit Reached *)
    ELSIF rScrewPos_Voted_Val <= rVP_ScrewPosFallback THEN
        bVP_TriggeredByPosition := TRUE;
        bVP_SwitchoverLatched := TRUE;
    (* Criterion 4: Nozzle Melt Pressure Safety Ceiling Exceeded (Hydraulic/Mold Protection) *)
    ELSIF rMeltPres_Voted_Val >= rVP_MeltPresFallback THEN
        bVP_TriggeredByMeltPres := TRUE;
        bVP_SwitchoverLatched := TRUE;
    END_IF;

    (* If Switchover Just Triggered, Snapshot State *)
    IF bVP_SwitchoverLatched THEN
        rVP_TransferCavityPressure := rCavPres_Voted_Val;
        rVP_TransferScrewPosition := rScrewPos_Voted_Val;
        rVP_TransferTimeStamp := rFSM_StateTimer;
    END_IF;
END_IF;

(* Dynamic Anti-Overshoot Servo Deceleration Dampening *)
(* As cavity pressure approaches V/P transfer target, actively damp injection velocity to prevent peak spike overshoot *)
IF (iFSM_State = 5) THEN
    rTemp_A := rCavPres_Voted_Val - (rRecipe_CavityVPOvershoot_In * 0.82);
    IF rTemp_A > 0.0 THEN
        rTemp_B := rTemp_A * rVP_DampingGain_Kd;
    ELSE
        rTemp_B := 0.0;
    END_IF;

    IF rCavPres_Derivative > 20000.0 THEN
        rTemp_C := (rCavPres_Derivative - 20000.0) * rVP_RateDampingGain_Kr;
    ELSE
        rTemp_C := 0.0;
    END_IF;

    rCavPres_DampenedVelocity := MAX(4.0, u_Cmd[1] - rTemp_B - rTemp_C);
ELSE
    rCavPres_DampenedVelocity := u_Cmd[1];
END_IF;
