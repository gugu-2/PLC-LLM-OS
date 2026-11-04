# brain_scratch/can_seamer_builder/part3_observers.py

PART3_OBSERVERS = """
(* ==========================================================================================
 * PHASE 3: CYBER-PHYSICAL OBSERVERS & MULTI-PHYSICS PROCESS ESTIMATORS
 * ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
 * 1. Double-Seam Mechanical Overlap & Hermetic Tightness Estimator
 * Mathematical Formulation:
 *   Overlap% = [(CH + BH + 1.1*te - SL) / (SL - (2.2*te + 1.1*tb))] * 100%
 *   Tightness% = [1.0 - (SeamThickness - (2*tb + 3*te)) / (3*te)] * 100%
 * ------------------------------------------------------------------------------------------ *)
rSeam_CoverHook_CH_mm := MAX(1.20, MIN(2.40, 1.95 + rSeamingRoll_1stOp_CamTrim_mm * 0.45));
rSeam_BodyHook_BH_mm  := MAX(1.20, MIN(2.40, 1.92 + (rVoted_Chuck_AxialLoad_kN - 5.50) * 0.045));
rSeam_SeamLength_SL_mm := MAX(2.50, MIN(3.50, rLaser_SeamHeight_mm));

(* Denominator protection against divide-by-zero *)
IF (rSeam_SeamLength_SL_mm - (2.2 * rSheetThick_End_te_mm + 1.1 * rSheetThick_Body_tb_mm)) > 0.10 THEN
    rSeam_TheoreticalOverlap_Pct := ((rSeam_CoverHook_CH_mm + rSeam_BodyHook_BH_mm + 
                                     (1.1 * rSheetThick_End_te_mm) - rSeam_SeamLength_SL_mm) / 
                                     (rSeam_SeamLength_SL_mm - (2.2 * rSheetThick_End_te_mm + 1.1 * rSheetThick_Body_tb_mm))) * 100.0;
ELSE
    rSeam_TheoreticalOverlap_Pct := 75.0;
END_IF;

(* Bound Overlap Percentage [0.0% to 100.0%] *)
rSeam_TheoreticalOverlap_Pct := MAX(0.0, MIN(100.0, rSeam_TheoreticalOverlap_Pct));

(* Double Seam Tightness Rating (Compression of Sealing Compound in Seam Folds) *)
IF (3.0 * rSheetThick_End_te_mm) > 0.05 THEN
    rSeam_TightnessRating_Pct := (1.0 - ((rLaser_SeamThickness_mm - (2.0 * rSheetThick_Body_tb_mm + 3.0 * rSheetThick_End_te_mm)) / 
                                 (3.0 * rSheetThick_End_te_mm))) * 100.0;
ELSE
    rSeam_TightnessRating_Pct := 80.0;
END_IF;
rSeam_TightnessRating_Pct := MAX(0.0, MIN(100.0, rSeam_TightnessRating_Pct));

(* ------------------------------------------------------------------------------------------
 * 2. Cryogenic LN2 Flash Vaporization Kinetics & Residual Oxygen Headspace Observer
 * Thermodynamics:
 *   Liquid N2 pulsed mass: m_LN2 = rho_LN2 * C_d * A_nozzle * sqrt(2*deltaP/rho) * t_pulse
 *   Gas Expansion: 1 mL liquid LN2 expands to ~694 mL gaseous N2 at 20 deg C, 1 atm.
 *   Headspace Oxygen Purge (Exponential Dilution Law):
 *     O2_residual(t) = O2_initial * exp( - V_N2_expanded / V_headspace )
 * ------------------------------------------------------------------------------------------ *)
(* Dynamic dosing pulse calculation: nominal pulse scaled by line speed and pressure *)
rLN2_DoseMass_mg := 85.0 * (rSP_Turret_Speed_RPM / MAX(10.0, rTurret_Speed_Actual_RPM)) * 
                    SQRT(MAX(0.5, rVoted_LN2_Pressure_bar) / 2.50) * (rLN2_InjectorPulse_ms / 14.50);
rLN2_DoseMass_mg := MAX(15.0, MIN(220.0, rLN2_DoseMass_mg));

(* Generated gaseous N2 volume at 20 deg C [mL] *)
rN2_GasVolume_STP_mL := (rLN2_DoseMass_mg / 1000.0) / (rLN2_Density_kg_m3 / 1000.0) * rLN2_VaporExpansionRatio;

(* Exponential oxygen dilution in headspace *)
IF rHeadspace_Volume_mL > 1.0 THEN
    rResidual_Oxygen_Pct := rHeadspace_InitialO2_Pct * EXP(-1.0 * (rN2_GasVolume_STP_mL / rHeadspace_Volume_mL));
ELSE
    rResidual_Oxygen_Pct := 0.50;
END_IF;
rResidual_Oxygen_Pct := MAX(0.05, MIN(20.95, rResidual_Oxygen_Pct));

(* Dynamic Headspace Pressure Estimation: Ideal gas expansion + elastic can dome deflection *)
(* P_internal = P_atm + (n_N2 * R * T / V_headspace) + K_can * Deflection *)
rCan_InternalPressure_bar := 1.013 + ((rN2_GasVolume_STP_mL / MAX(5.0, rHeadspace_Volume_mL)) * 0.285) + 
                             (rCan_HeadspaceDeflection_mm * 0.950);
rCan_InternalPressure_bar := MAX(0.80, MIN(4.50, rCan_InternalPressure_bar));

(* ------------------------------------------------------------------------------------------
 * 3. Acoustic Dome Membrane Vibration & Resonant Frequency Mechanics
 * Clamped Circular Membrane Model:
 *   f_0 = (2.4048 / (2*pi*R)) * sqrt( sigma_tension / rho_surface )
 *   where radial stress sigma_tension = (P_internal * R) / (2 * t_end)
 * ------------------------------------------------------------------------------------------ *)
IF (2.0 * rSheetThick_End_te_mm / 1000.0) > 0.0001 AND rCan_Lid_SurfaceDensity_kg_m2 > 0.01 THEN
    (* Analytical prediction of fundamental modal frequency f0 [kHz] *)
    rAcoustic_Model_Freq_kHz := ((2.4048 / (2.0 * 3.14159265 * rCan_Lid_Radius_m)) * 
                                SQRT(MAX(100.0, (rCan_InternalPressure_bar - 1.013) * 100000.0 * rCan_Lid_Radius_m / 
                                (2.0 * (rSheetThick_End_te_mm / 1000.0) * rCan_Lid_SurfaceDensity_kg_m2)))) / 1000.0;
ELSE
    rAcoustic_Model_Freq_kHz := 3.15;
END_IF;
rAcoustic_Model_Freq_kHz := MAX(1.80, MIN(4.50, rAcoustic_Model_Freq_kHz));

(* Innovation error between measured acoustic resonance and physics model *)
rAcoustic_Freq_Deviation_kHz := rVoted_AcousticResonance_kHz - rAcoustic_Model_Freq_kHz;

(* Flag acoustic defect if resonance deviates > 0.45 kHz or ring-down decay is truncated *)
IF ABS(rAcoustic_Freq_Deviation_kHz) > 0.450 OR rAcoustic_ImpulseDecay_ms < 6.0 THEN
    bAcoustic_Defect_Detected := TRUE;
ELSE
    bAcoustic_Defect_Detected := FALSE;
END_IF;

(* ------------------------------------------------------------------------------------------
 * 4. Turret 18th-Order Spatially Periodic Torque Ripple Estimator & Active Feedforward
 * Spatial Fourier Harmonics:
 *   theta = rTurret_Angular_Pos_Deg * (pi / 180)
 *   tau_ripple(theta) = A1*cos(18*theta) + B1*sin(18*theta) + A2*cos(36*theta) + B2*sin(36*theta)
 * ------------------------------------------------------------------------------------------ *)
rSpatial_Angle_Rad := rTurret_Angular_Pos_Deg * (3.14159265 / 180.0);

(* 18th Harmonic (fundamental pocket tooth pitch: 360 deg / 18 heads = 20 deg per head) *)
rTorqueRipple_Harmonic1_Nm := 12.50 * COS(18.0 * rSpatial_Angle_Rad) + 8.20 * SIN(18.0 * rSpatial_Angle_Rad);

(* 36th Harmonic (2nd order cam roll engagement harmonics) *)
rTorqueRipple_Harmonic2_Nm := 4.80 * COS(36.0 * rSpatial_Angle_Rad) - 3.10 * SIN(36.0 * rSpatial_Angle_Rad);

(* 54th Harmonic (3rd order seaming chuck contact transients) *)
rTorqueRipple_Harmonic3_Nm := 1.75 * COS(54.0 * rSpatial_Angle_Rad) + 1.25 * SIN(54.0 * rSpatial_Angle_Rad);

(* Active Cancellation Torque Feedforward Command *)
rTorqueRipple_Comp_Nm := -1.0 * (rTorqueRipple_Harmonic1_Nm + rTorqueRipple_Harmonic2_Nm + rTorqueRipple_Harmonic3_Nm);
rTorqueRipple_Comp_Nm := MAX(-25.0, MIN(25.0, rTorqueRipple_Comp_Nm));

(* ------------------------------------------------------------------------------------------
 * 5. Aseptic Steam Barrier Heat Balance & F0 Thermal Sterilization Accumulator
 * Bigelow Lethality Model:
 *   L = 10 ^ ((T - 121.11 deg C) / z_value)  where z = 10.0 deg C
 *   F0 = Integral [ L(t) dt ]
 * ------------------------------------------------------------------------------------------ *)
IF rVoted_SteamBarrier_Temp_degC >= 100.0 THEN
    rF0_Lethality_Rate_min_s := (EXPT(10.0, (rVoted_SteamBarrier_Temp_degC - 121.11) / 10.0)) / 60.0;
    rThermalBarrier_F0_Accum := rThermalBarrier_F0_Accum + (rF0_Lethality_Rate_min_s * rDeltaT);
ELSE
    rF0_Lethality_Rate_min_s := 0.0;
END_IF;

(* Bound F0 accumulator *)
rThermalBarrier_F0_Accum := MIN(9999.9, rThermalBarrier_F0_Accum);

(* Saturated Steam Condensation Rate [kg/h] *)
rSteam_Condensate_Flow_kg_h := 3.50 + ((rVoted_SteamBarrier_Temp_degC - 100.0) * 0.085);

(* ------------------------------------------------------------------------------------------
 * 6. Individual 18-Head Statistical Profiling & Predictive Wear Modeling
 * Continuously track each seaming station to detect spindle runout, spring fatigue,
 * bearing brinelling, and roll groove profile erosion.
 * ------------------------------------------------------------------------------------------ *)
IF iActive_Head_ID >= 1 AND iActive_Head_ID <= 18 THEN
    (* Exponential moving average of active chuck axial load (alpha = 0.05) *)
    aHead_AxialLoad_Mean[iActive_Head_ID] := (0.05 * rVoted_Chuck_AxialLoad_kN) + 
                                            (0.95 * aHead_AxialLoad_Mean[iActive_Head_ID]);

    (* Running sample variance calculation: sigma^2 = (1-alpha)*sigma^2 + alpha*(x - mu)^2 *)
    aHead_AxialLoad_Variance[iActive_Head_ID] := (0.95 * aHead_AxialLoad_Variance[iActive_Head_ID]) + 
                                                (0.05 * EXPT(rVoted_Chuck_AxialLoad_kN - aHead_AxialLoad_Mean[iActive_Head_ID], 2));

    (* Peak & Minimum Load Latching *)
    IF rVoted_Chuck_AxialLoad_kN > aHead_AxialLoad_Peak[iActive_Head_ID] THEN
        aHead_AxialLoad_Peak[iActive_Head_ID] := rVoted_Chuck_AxialLoad_kN;
    END_IF;
    IF rVoted_Chuck_AxialLoad_kN < aHead_AxialLoad_Min[iActive_Head_ID] AND rVoted_Chuck_AxialLoad_kN > 1.0 THEN
        aHead_AxialLoad_Min[iActive_Head_ID] := rVoted_Chuck_AxialLoad_kN;
    END_IF;

    (* Historical Laser & Acoustic Metrology Tracking *)
    aHead_SeamThickness_Hist[iActive_Head_ID] := (0.05 * rLaser_SeamThickness_mm) + 
                                                (0.95 * aHead_SeamThickness_Hist[iActive_Head_ID]);
    aHead_SeamHeight_Hist[iActive_Head_ID]    := (0.05 * rLaser_SeamHeight_mm) + 
                                                (0.95 * aHead_SeamHeight_Hist[iActive_Head_ID]);
    aHead_Countersink_Hist[iActive_Head_ID]   := (0.05 * rLaser_CountersinkDepth_mm) + 
                                                (0.95 * aHead_Countersink_Hist[iActive_Head_ID]);
    aHead_ResonanceFreq_Hist[iActive_Head_ID] := (0.05 * rVoted_AcousticResonance_kHz) + 
                                                (0.95 * aHead_ResonanceFreq_Hist[iActive_Head_ID]);

    (* Increment cycle counter *)
    aHead_TotalCycles[iActive_Head_ID] := aHead_TotalCycles[iActive_Head_ID] + 1;

    (* Multi-Factor Mechanical Wear Index Formulation:
     *   Wear% = Cycles_factor(40%) + Load_Deviation_factor(35%) + Variance_instability_factor(25%) *)
    aHead_WearIndex_Pct[iActive_Head_ID] := ((DINT_TO_REAL(aHead_TotalCycles[iActive_Head_ID]) / 2500000.0) * 40.0) + 
                                            ((ABS(aHead_AxialLoad_Mean[iActive_Head_ID] - 5.50) / 1.50) * 35.0) + 
                                            ((aHead_AxialLoad_Variance[iActive_Head_ID] / 0.150) * 25.0);
    aHead_WearIndex_Pct[iActive_Head_ID] := MAX(0.0, MIN(100.0, aHead_WearIndex_Pct[iActive_Head_ID]));

    (* Check for Individual Head Predictive Wear Alarm (> 80%) *)
    IF aHead_WearIndex_Pct[iActive_Head_ID] > 80.0 THEN
        bAlarm_IndividualHead_WearWarn := TRUE;
        dwHead_Defect_Mask := dwHead_Defect_Mask OR SHL(DWORD#16#00000001, (iActive_Head_ID - 1));
    END_IF;
END_IF;
"""
