# part3_observers.py
# Generates Phase 3: Cyber-Physical Observers (Consolidation, Heat Exchanger, Conductivity, Turbidity, Peristaltic)

def get_part3():
    return '''(* ==========================================================================================
 * PHASE 3: CYBER-PHYSICAL OBSERVERS & MULTI-PHYSICS PROCESS ESTIMATORS
 * ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
 * 3.1: TERZAGHI CAKE CONSOLIDATION & DARCY POROUS MEDIA DEWATERING OBSERVER
 * Calculates: Dynamic specific cake resistance, pore fluid drainage rate, ram compression
 * strain, and in-situ residual moisture percentage M(t) during 50-bar pressing.
 * ------------------------------------------------------------------------------------------ *)
(* Bounding dry textile batch weight [20.0 kg to 75.0 kg] *)
IF rBatchDryWeight_kg < 20.0 THEN
    rBatchDryWeight_kg := 50.0;
ELSIF rBatchDryWeight_kg > 75.0 THEN
    rBatchDryWeight_kg := 75.0;
END_IF;

(* Calculate uncompressed cake compression strain Epsilon = (Z0 - Z) / Z0 *)
IF rPress_RamPosition_mm > 0.0 AND rPress_RamPosition_mm < rCake_InitialHeight_mm THEN
    rCake_CompressionStrain := (rCake_InitialHeight_mm - rPress_RamPosition_mm) / rCake_InitialHeight_mm;
ELSE
    rCake_CompressionStrain := 0.0;
END_IF;

(* Specific cake resistance alpha increases non-linearly with compaction and hydraulic pressure *)
(* alpha = alpha_0 * (1 + s_comp * (P_press / 10)^n) *)
IF rTMR4_VotedVal > 0.5 THEN
    rCake_SpecificResistance := 4.50E+10 * (1.0 + (0.42 * (rTMR4_VotedVal / 10.0) * (rTMR4_VotedVal / 10.0)));
    (* Dynamic permeability K_p = K_0 * (1 - Epsilon)^3.5 *)
    IF rCake_CompressionStrain < 0.95 THEN
        rCake_Permeability_m2 := 1.25E-11 * (1.0 - rCake_CompressionStrain) * (1.0 - rCake_CompressionStrain);
    ELSE
        rCake_Permeability_m2 := 1.25E-13;
    END_IF;
ELSE
    rCake_SpecificResistance := 4.50E+10;
    rCake_Permeability_m2 := 1.25E-11;
END_IF;

(* Darcy pore fluid expression rate [L/s]: Q_drain = Area * dP / (mu * (alpha * w + R_m)) *)
(* Effective basket drainage area = 0.95 m2, water viscosity at 50 deg C = 0.000547 Pa*s *)
IF rTMR4_VotedVal > 1.0 AND rPress_RamPosition_mm > 50.0 THEN
    (* Expressed flow calculated from pressure differential and membrane cushion *)
    rCake_FiltrateFlow_Lps := (0.95 * (rTMR4_VotedVal * 1.0E+05)) /
                              (0.000547 * ((rCake_SpecificResistance * (rBatchDryWeight_kg / 0.95)) + 1.8E+09)) * 1000.0;
    
    (* Blend flowmeter reading with Darcy theoretical model (80% flowmeter, 20% model) *)
    IF rFlow_PressFiltrate_Lmin > 0.1 THEN
        rCake_FiltrateFlow_Lps := (0.80 * (rFlow_PressFiltrate_Lmin / 60.0)) + (0.20 * rCake_FiltrateFlow_Lps);
    END_IF;
ELSE
    rCake_FiltrateFlow_Lps := 0.0;
END_IF;

(* Integrate cumulative expressed water volume during active pressing states (States 8, 9, 10) *)
IF (iState = 9) THEN
    rCake_FiltrateVol_L := rCake_FiltrateVol_L + (rCake_FiltrateFlow_Lps * rDeltaTime_s);
    (* Instantaneous mass of water remaining inside textile cake [kg] (1 L water approx 1.0 kg) *)
    rCake_WaterMass_kg := ((rBatchDryWeight_kg * (rCake_InitialMoisture / 100.0)) - rCake_FiltrateVol_L);
    IF rCake_WaterMass_kg < (rBatchDryWeight_kg * 0.35) THEN
        rCake_WaterMass_kg := rBatchDryWeight_kg * 0.35; (* Physical minimum bound approx 35% residual moisture *)
    END_IF;
    
    (* Dynamic Observed Cake Moisture: M(t) = (WaterMass / DryMass) * 100 % *)
    rCake_CurrentMoisture := (rCake_WaterMass_kg / rBatchDryWeight_kg) * 100.0;
    
    (* Consolidation rate derivative: dM/dt [%/s] *)
    rConsolidationRate_pct_s := - (rCake_FiltrateFlow_Lps / rBatchDryWeight_kg) * 100.0;
ELSIF (iState = 1) OR (iState = 8) THEN
    (* Reset baseline prior to press stroke *)
    rCake_InitialMoisture := 220.0;
    rCake_CurrentMoisture := 220.0;
    rCake_FiltrateVol_L := 0.0;
    rCake_WaterMass_kg := rBatchDryWeight_kg * 2.20;
    rConsolidationRate_pct_s := 0.0;
END_IF;
rEstimatedCakeMoisture_pct := rCake_CurrentMoisture;
rObserved_FiltrateTotalVolume_L := rCake_FiltrateVol_L;


(* ------------------------------------------------------------------------------------------
 * 3.2: PLATE HEAT EXCHANGER (PHE) EFFECTIVENESS & LMTD THERMAL OBSERVER
 * Calculates: Recovered thermal power [kW], Log Mean Temperature Difference (LMTD),
 * overall heat transfer coefficient U [W/(m2*K)], and bio-fouling resistance Rf.
 * ------------------------------------------------------------------------------------------ *)
(* Process temperatures around PHE:
 * Hot side inlet (Effluent greywater from wash): rPHE_HotInletTemp_degC ~ rTMR1_VotedVal - 8.0
 * Hot side outlet (Greywater to sewer): rPHE_HotOutletTemp_degC ~ 28.0 deg C
 * Cold side inlet (Fresh city water): rPHE_ColdInletTemp_degC ~ 14.5 deg C
 * Cold side outlet (Pre-heated rinse water): rPHE_ColdOutletTemp_degC = rTMR5_VotedVal *)
rPHE_HotInletTemp_degC  := rTMR1_VotedVal - 8.0;
rPHE_HotOutletTemp_degC := 28.0;
rPHE_ColdInletTemp_degC := 14.5;
rPHE_ColdOutletTemp_degC:= rTMR5_VotedVal;

(* Temperature approach differences for counter-flow heat exchanger *)
rPHE_DeltaT1 := rPHE_HotInletTemp_degC - rPHE_ColdOutletTemp_degC;
rPHE_DeltaT2 := rPHE_HotOutletTemp_degC - rPHE_ColdInletTemp_degC;

(* Sanity clamping approach deltas to prevent numerical divergence *)
IF rPHE_DeltaT1 < 1.0 THEN
    rPHE_DeltaT1 := 1.0;
END_IF;
IF rPHE_DeltaT2 < 1.0 THEN
    rPHE_DeltaT2 := 1.0;
END_IF;

(* Log Mean Temperature Difference (LMTD) calculation *)
IF ABS(rPHE_DeltaT1 - rPHE_DeltaT2) > 0.5 THEN
    rPHE_LMTD := (rPHE_DeltaT1 - rPHE_DeltaT2) / LN(rPHE_DeltaT1 / rPHE_DeltaT2);
ELSE
    rPHE_LMTD := (rPHE_DeltaT1 + rPHE_DeltaT2) * 0.5;
END_IF;

(* Thermal power absorbed by cold fresh water stream [kW]:
 * Q_cold = m_dot * C_p * (T_cold_out - T_cold_in)
 * C_p water = 4.184 kJ/(kg*K), flow in m3/h -> kg/s *)
IF rFlow_FreshWater_m3h > 0.1 AND (rPHE_ColdOutletTemp_degC > rPHE_ColdInletTemp_degC) THEN
    rPHE_HeatTransfer_kW := (rFlow_FreshWater_m3h * 1000.0 / 3600.0) * 4.184 *
                            (rPHE_ColdOutletTemp_degC - rPHE_ColdInletTemp_degC);
ELSE
    rPHE_HeatTransfer_kW := 0.0;
END_IF;
rObserved_HeatRecovery_kW := rPHE_HeatTransfer_kW;

(* Dynamic Overall Heat Transfer Coefficient U [W/(m2*K)] *)
(* Total effective plate heat transfer surface area = 42.0 m2 *)
IF (rPHE_LMTD > 2.0) AND (rPHE_HeatTransfer_kW > 5.0) THEN
    rPHE_HeatTransferCoeff_U := (rPHE_HeatTransfer_kW * 1000.0) / (42.0 * rPHE_LMTD);
    (* Fouling Resistance Factor: Rf = (1/U) - (1/U_clean) [(m2*K)/W] *)
    IF rPHE_HeatTransferCoeff_U < rPHE_CleanU_Benchmark THEN
        rPHE_FoulingResistance := (1.0 / rPHE_HeatTransferCoeff_U) - (1.0 / rPHE_CleanU_Benchmark);
    ELSE
        rPHE_FoulingResistance := 0.0;
    END_IF;
ELSE
    rPHE_HeatTransferCoeff_U := rPHE_CleanU_Benchmark;
    rPHE_FoulingResistance := 0.0;
END_IF;


(* ------------------------------------------------------------------------------------------
 * 3.3: INDUCTIVE CONDUCTIVITY TEMPERATURE COMPENSATION & ALKALI OBSERVER
 * Calculates: Normalized conductivity at 25.0 deg C [uS/cm], and active caustic soda (NaOH)
 * concentration percentage [wt%] via high-order polynomial regression.
 * ------------------------------------------------------------------------------------------ *)
(* Non-linear temperature compensation coefficient: alpha(T) = 0.0215 + 0.00015 * (T - 25.0) *)
rCond_TempCoeff_pct_K := 0.0215 + (0.00015 * (rTMR1_VotedVal - 25.0));

(* Temperature compensation formula: K_25 = K_T / [1 + alpha * (T - 25.0)] *)
IF (1.0 + (rCond_TempCoeff_pct_K * (rTMR1_VotedVal - 25.0))) > 0.2 THEN
    rCond_Normalized_uS := rTMR3_VotedVal / (1.0 + (rCond_TempCoeff_pct_K * (rTMR1_VotedVal - 25.0)));
ELSE
    rCond_Normalized_uS := rTMR3_VotedVal;
END_IF;

(* Caustic Soda (NaOH 50% technical grade) concentration polynomial model:
 * wt% NaOH = c0 + c1*(K_25*1e-4) + c2*(K_25*1e-4)^2 + c3*(K_25*1e-4)^3 *)
rTempSum := rCond_Normalized_uS * 1.0E-04;
rAlkali_Concentration_wt := 0.045 + (1.285 * rTempSum) + (0.082 * rTempSum * rTempSum) - (0.0035 * rTempSum * rTempSum * rTempSum);
IF rAlkali_Concentration_wt < 0.0 THEN
    rAlkali_Concentration_wt := 0.0;
ELSIF rAlkali_Concentration_wt > 15.0 THEN
    rAlkali_Concentration_wt := 15.0;
END_IF;
rObserved_AlkaliConcentration_pct := rAlkali_Concentration_wt;


(* ------------------------------------------------------------------------------------------
 * 3.4: RECLAIMED GREYWATER TURBIDITY & FILTRATION SETTLING QUALITY OBSERVER
 * Evaluates water recycle purity in Nephelometric Turbidity Units [NTU].
 * Quality threshold interlock: Diverts water to industrial sewer drain if NTU > 150.0.
 * ------------------------------------------------------------------------------------------ *)
IF (rTMR6_VotedVal >= rTurbidity_Severe_Trip) OR (rPH_RinseBath < 5.0) OR (rPH_RinseBath > 10.5) THEN
    (* Water too contaminated with soil, unreacted bleach or particulate: Divert to drain *)
    bValve_ReclaimDivertToDrain := TRUE;
ELSE
    (* High-grade reclaim water suitable for counter-flow heat recovery & pre-wash reuse *)
    bValve_ReclaimDivertToDrain := FALSE;
END_IF;


(* ------------------------------------------------------------------------------------------
 * 3.5: 12-CHANNEL PERISTALTIC CHEMICAL DOSING MANIFOLD TUBE FATIGUE OBSERVER
 * Tracks accumulated revolutions, pumped liters, and mechanical fatigue wear index
 * for each elastomeric Santoprene / Marprene peristaltic tubing element.
 * ------------------------------------------------------------------------------------------ *)
(* Channel 1: Caustic Soda 50% Bulk *)
IF rDosing_Alkali_Lmin > 0.01 THEN
    rPeristaltic_Volume_L[1] := rPeristaltic_Volume_L[1] + (rDosing_Alkali_Lmin * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[1] := rPeristaltic_TotalRev[1] + ((rDosing_Alkali_Lmin / 0.045) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[1]:= rPeristaltic_TotalRev[1] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 2: Caustic Soda 50% Fine Trim *)
IF rDosing_Alkali_Lmin > 5.0 THEN
    rPeristaltic_Volume_L[2] := rPeristaltic_Volume_L[2] + ((rDosing_Alkali_Lmin - 5.0) * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[2] := rPeristaltic_TotalRev[2] + (((rDosing_Alkali_Lmin - 5.0) / 0.020) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[2]:= rPeristaltic_TotalRev[2] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 3: Non-Ionic Surfactant Detergent Bulk *)
IF rDosing_Detergent_Lmin > 0.01 THEN
    rPeristaltic_Volume_L[3] := rPeristaltic_Volume_L[3] + (rDosing_Detergent_Lmin * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[3] := rPeristaltic_TotalRev[3] + ((rDosing_Detergent_Lmin / 0.035) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[3]:= rPeristaltic_TotalRev[3] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 4: Non-Ionic Surfactant Detergent Trim *)
IF rDosing_Detergent_Lmin > 4.0 THEN
    rPeristaltic_Volume_L[4] := rPeristaltic_Volume_L[4] + ((rDosing_Detergent_Lmin - 4.0) * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[4] := rPeristaltic_TotalRev[4] + (((rDosing_Detergent_Lmin - 4.0) / 0.015) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[4]:= rPeristaltic_TotalRev[4] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 5: Hydrogen Peroxide / Bleaching Agent *)
IF rDosing_Bleach_Lmin > 0.01 THEN
    rPeristaltic_Volume_L[5] := rPeristaltic_Volume_L[5] + (rDosing_Bleach_Lmin * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[5] := rPeristaltic_TotalRev[5] + ((rDosing_Bleach_Lmin / 0.030) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[5]:= rPeristaltic_TotalRev[5] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 6: Peracetic Acid (PAA) Low-Temp Disinfectant *)
IF (iBatchRecipeID = 3) AND (rDosing_Bleach_Lmin > 1.0) THEN
    rPeristaltic_Volume_L[6] := rPeristaltic_Volume_L[6] + (1.2 * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[6] := rPeristaltic_TotalRev[6] + ((1.2 / 0.020) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[6]:= rPeristaltic_TotalRev[6] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 7: Organic Acid Sour Neutralizer Bulk *)
IF rDosing_AcidSour_Lmin > 0.01 THEN
    rPeristaltic_Volume_L[7] := rPeristaltic_Volume_L[7] + (rDosing_AcidSour_Lmin * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[7] := rPeristaltic_TotalRev[7] + ((rDosing_AcidSour_Lmin / 0.030) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[7]:= rPeristaltic_TotalRev[7] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 8: Organic Acid Sour Neutralizer Fine Trim *)
IF rDosing_AcidSour_Lmin > 3.0 THEN
    rPeristaltic_Volume_L[8] := rPeristaltic_Volume_L[8] + ((rDosing_AcidSour_Lmin - 3.0) * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[8] := rPeristaltic_TotalRev[8] + (((rDosing_AcidSour_Lmin - 3.0) / 0.012) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[8]:= rPeristaltic_TotalRev[8] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 9: Cationic Fabric Softener *)
IF rDosing_Softener_Lmin > 0.01 THEN
    rPeristaltic_Volume_L[9] := rPeristaltic_Volume_L[9] + (rDosing_Softener_Lmin * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[9] := rPeristaltic_TotalRev[9] + ((rDosing_Softener_Lmin / 0.025) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[9]:= rPeristaltic_TotalRev[9] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 10: Anti-Static Conditioning Lubricant *)
IF rDosing_Softener_Lmin > 2.0 THEN
    rPeristaltic_Volume_L[10] := rPeristaltic_Volume_L[10] + (0.5 * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[10] := rPeristaltic_TotalRev[10] + ((0.5 / 0.010) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[10]:= rPeristaltic_TotalRev[10] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 11: Optical Fluorescent Brightener (OBX) *)
IF (iBatchRecipeID = 1) AND (iState = 5) THEN
    rPeristaltic_Volume_L[11] := rPeristaltic_Volume_L[11] + (0.15 * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[11] := rPeristaltic_TotalRev[11] + ((0.15 / 0.008) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[11]:= rPeristaltic_TotalRev[11] / rPeristaltic_MaxRevLife;
END_IF;

(* Channel 12: Laundry Starch / Sizing Agent *)
IF (iBatchRecipeID = 4) AND (iState = 7) THEN
    rPeristaltic_Volume_L[12] := rPeristaltic_Volume_L[12] + (0.80 * (rDeltaTime_s / 60.0));
    rPeristaltic_TotalRev[12] := rPeristaltic_TotalRev[12] + ((0.80 / 0.020) * (rDeltaTime_s / 60.0));
    rPeristaltic_WearRatio[12]:= rPeristaltic_TotalRev[12] / rPeristaltic_MaxRevLife;
END_IF;
'''

if __name__ == "__main__":
    p3 = get_part3()
    print(f"Part 3 length: {len(p3)} characters")
