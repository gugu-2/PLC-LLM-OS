# Phase 2 Builder for FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration
import os, sys

def get_phase2_code():
    lines = []
    lines.append("""(*
====================================================================================================
PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (Ts = 10.0 [ms])
Mathematical Structure:
  1. Sensor Fusion & Physical Variable Calculation from Voted Channels
  2. Nonlinear Biophysical Constitutive Model Updates (Mooney Viscosity, Wall Shear, Film Theory)
  3. A-Priori State Propagation: x_pred[k+1] = A * x[k] + B * u[k]
  4. Output Measurement Prediction: y_pred[k] = C * x_pred[k+1] + D * u[k]
  5. Innovation Residual Computation: e[k] = y_meas[k] - y_pred[k]
  6. A-Posteriori Luenberger State Correction: x_est[k+1] = x_pred[k+1] + L * e[k]
  7. Physical Non-Negative Projection Clamping & Diagnostics Output Mapping
====================================================================================================
*)

(* -------------------------------------------------------------------------------------------------
 * 1. Physical Process Variable Construction from Voted Transducers
 * ------------------------------------------------------------------------------------------------- *)
rRaw_TMP_bar := (rVoted_PT_Feed_bar + rVoted_PT_Ret_bar) * 0.5 - rVoted_PT_Perm_bar;
rRaw_PermeateFlux_LMH := rFT_Perm_Flow_Lh / MAX(0.1, rCassette_MembraneArea_m2);

arrY_Meas[1] := rRaw_TMP_bar;
arrY_Meas[2] := rRaw_PermeateFlux_LMH;
arrY_Meas[3] := rVoted_AT_UV_gL;
arrY_Meas[4] := rVoted_FT_Feed_Lh;
arrY_Meas[5] := rTT_Ret_Temp_degC;
arrY_Meas[6] := (rWT_BufferScale_kg - rWT_PermeateScale_kg) * 1000.0;

(* -------------------------------------------------------------------------------------------------
 * 2. Nonlinear Biophysical Constitutive Relations
 * ------------------------------------------------------------------------------------------------- *)
(* Ross-Minton / Mooney Dynamic Viscosity Prediction for Concentrated Monoclonal Antibodies *)
(* eta(C) = eta_0 * exp( [eta] * C / (1 - k_crowd * C) ) *)
rDynamicViscosity_cP := 1.025 * EXP((0.00785 * arrX_State[3]) / MAX(0.15, 1.0 - (0.00345 * arrX_State[3])));
IF rDynamicViscosity_cP > 50.0 THEN
    rDynamicViscosity_cP := 50.0;
ELSIF rDynamicViscosity_cP < 0.85 THEN
    rDynamicViscosity_cP := 0.85;
END_IF;
rCalc_FluidViscosity_cP := rDynamicViscosity_cP;

(* Normalized Water Permeability Temperature Viscosity Correction Factor (Ref: 20.0 deg C) *)
rNWP_Temperature_Factor := 1.0 / MAX(0.5, 1.0 + (0.0242 * (rTT_Ret_Temp_degC - 20.0)));
rCalc_Current_NWP_LMHbar := (rRaw_PermeateFlux_LMH * rNWP_Temperature_Factor) / MAX(0.10, rRaw_TMP_bar);

(* Real-Time Cumulative Volumetric Mass Balance Integration *)
rTotalPermeateVolume_L := rTotalPermeateVolume_L + (rFT_Perm_Flow_Lh * (rCycleTime_s / 3600.0));
rTotalBufferAdded_L := rTotalBufferAdded_L + (rFT_Buffer_Flow_Lh * (rCycleTime_s / 3600.0));
rCalc_PermeateAccumVol_L := rTotalPermeateVolume_L;
rCalc_BufferAddedVol_L := rTotalBufferAdded_L;

rCurrentRetentateVol_L := MAX(1.0, rInitialHoldUpVol_L - rTotalPermeateVolume_L + rTotalBufferAdded_L);
rCalc_ConcentrationFactor := rInitialHoldUpVol_L / rCurrentRetentateVol_L;

(* -------------------------------------------------------------------------------------------------
 * 3. A-Priori Discrete State Propagation: x_pred[k+1] = A * x[k] + B * u[k]
 * ------------------------------------------------------------------------------------------------- *)
FOR iLoopIndex := 1 TO 8 DO
    arrX_Pred[iLoopIndex] := 0.0;
    FOR jLoopIndex := 1 TO 8 DO
        arrX_Pred[iLoopIndex] := arrX_Pred[iLoopIndex] + (arrA_Matrix[iLoopIndex, jLoopIndex] * arrX_State[jLoopIndex]);
    END_FOR;
    FOR jLoopIndex := 1 TO 6 DO
        arrX_Pred[iLoopIndex] := arrX_Pred[iLoopIndex] + (arrB_Matrix[iLoopIndex, jLoopIndex] * arrU_Act[jLoopIndex]);
    END_FOR;
END_FOR;

(* -------------------------------------------------------------------------------------------------
 * 4. Output Measurement Vector Prediction: y_pred[k] = C * x_pred[k+1] + D * u[k]
 * ------------------------------------------------------------------------------------------------- *)
FOR iLoopIndex := 1 TO 6 DO
    arrY_Pred[iLoopIndex] := 0.0;
    FOR jLoopIndex := 1 TO 8 DO
        arrY_Pred[iLoopIndex] := arrY_Pred[iLoopIndex] + (arrC_Matrix[iLoopIndex, jLoopIndex] * arrX_Pred[jLoopIndex]);
    END_FOR;
    FOR jLoopIndex := 1 TO 6 DO
        arrY_Pred[iLoopIndex] := arrY_Pred[iLoopIndex] + (arrD_Matrix[iLoopIndex, jLoopIndex] * arrU_Act[jLoopIndex]);
    END_FOR;
END_FOR;

(* -------------------------------------------------------------------------------------------------
 * 5. Innovation Residual Vector: e[k] = y_meas[k] - y_pred[k]
 * ------------------------------------------------------------------------------------------------- *)
FOR iLoopIndex := 1 TO 6 DO
    arrInnov_e[iLoopIndex] := arrY_Meas[iLoopIndex] - arrY_Pred[iLoopIndex];
END_FOR;

(* -------------------------------------------------------------------------------------------------
 * 6. A-Posteriori Luenberger State Correction: x_est[k+1] = x_pred[k+1] + L * e[k]
 * ------------------------------------------------------------------------------------------------- *)
FOR iLoopIndex := 1 TO 8 DO
    arrX_State[iLoopIndex] := arrX_Pred[iLoopIndex];
    FOR jLoopIndex := 1 TO 6 DO
        arrX_State[iLoopIndex] := arrX_State[iLoopIndex] + (arrL_Gain[iLoopIndex, jLoopIndex] * arrInnov_e[jLoopIndex]);
    END_FOR;
END_FOR;

(* -------------------------------------------------------------------------------------------------
 * 7. Physical Bounded Projection & Telemetry Output Mapping
 * ------------------------------------------------------------------------------------------------- *)
(* State 1: TMP >= 0.0 [bar] *)
IF arrX_State[1] < 0.0 THEN
    arrX_State[1] := 0.0;
ELSIF arrX_State[1] > 6.0 THEN
    arrX_State[1] := 6.0;
END_IF;

(* State 2: Permeate Flux >= 0.0 [LMH] *)
IF arrX_State[2] < 0.0 THEN
    arrX_State[2] := 0.0;
ELSIF arrX_State[2] > 250.0 THEN
    arrX_State[2] := 250.0;
END_IF;

(* State 3: mAb Concentration >= 0.0 [g/L] *)
IF arrX_State[3] < 0.0 THEN
    arrX_State[3] := 0.0;
ELSIF arrX_State[3] > 350.0 THEN
    arrX_State[3] := 350.0;
END_IF;

(* State 4: Gel Resistance >= 0.05 [10^11 m-1] *)
IF arrX_State[4] < 0.05 THEN
    arrX_State[4] := 0.05;
ELSIF arrX_State[4] > 50.0 THEN
    arrX_State[4] := 50.0;
END_IF;

(* State 5: Retentate Wall Shear Rate >= 0.0 [s-1] *)
IF arrX_State[5] < 0.0 THEN
    arrX_State[5] := 0.0;
ELSIF arrX_State[5] > 25000.0 THEN
    arrX_State[5] := 25000.0;
END_IF;

(* State 6: Diafiltration Counter >= 0.0 [DV] *)
IF arrX_State[6] < 0.0 THEN
    arrX_State[6] := 0.0;
ELSIF arrX_State[6] > 20.0 THEN
    arrX_State[6] := 20.0;
END_IF;

(* State 7: Process Temperature [deg C] *)
IF arrX_State[7] < -5.0 THEN
    arrX_State[7] := -5.0;
ELSIF arrX_State[7] > 95.0 THEN
    arrX_State[7] := 95.0;
END_IF;

(* Map Estimated States to Function Block Outputs *)
rEst_TMP_bar := arrX_State[1];
rEst_PermeateFlux_LMH := arrX_State[2];
rEst_ProteinConc_gL := arrX_State[3];
rEst_GelResistance_m1 := arrX_State[4];
rEst_WallShearRate_s1 := arrX_State[5];
rEst_DV_ExchangeCounter := arrX_State[6];
rEst_RecircTemp_degC := arrX_State[7];
rEst_SumpWeightDev_g := arrX_State[8];""")

    return "\n".join(lines)

print("Phase 2 builder ready")
